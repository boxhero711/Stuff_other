#!/usr/bin/env python3
"""Brooklyn Vice clipper: trim, reframe, brand, intro/outro, loudness.

Examples
  # 9:16 Short from our own capture, with host voiceover
  python3 edit/clip.py capture/session1.mp4 --start 01:12 --end 01:41 \
      --format short --vo vo/ep01.wav --name ep01-parking

  # 16:9 long-form segment from an approved source, game audio muted
  python3 edit/clip.py sources/creatorx-0412.mp4 --start 30 --end 95 \
      --format long --game-audio mute --vo vo/recap01.wav --name recap01-seg1

What it does
  1. Checks the source (CLAUDE.md 2.6): files in capture/ are our own footage.
     Files in sources/ must have a sources.csv row (local_file column) with an
     approved file route (1, 2 or 3), a saved permission file, a post-release
     date, and the target platform allowed. Anything else is refused.
  2. Trims, reframes (short: 1080x1920, long: 1920x1080), 30 fps.
  3. Adds the corner tag for the whole clip and the lower third from 1s to 6s.
  4. Mixes game audio (duck by default, or mute/keep) under the voiceover.
  5. Short: clip then 1.5s outro card. Long: 2.5s intro card, clip, 20s end card.
  6. Normalizes loudness to -14 LUFS and writes out/<name>.mp4 + out/<name>.json.

A clip with no --vo is written as <name>_DRAFT.mp4. The voice layer is required
to ship (CLAUDE.md section 3). This script never uploads anything.
"""
import argparse, csv, datetime, json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = os.path.join(ROOT, "brand", "export")
STINGERS = os.path.join(ROOT, "edit", "stingers")
RELEASE = datetime.date(2026, 11, 19)
FPS = 30
SIZES = {"short": (1080, 1920), "long": (1920, 1080)}
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
       "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]


def die(msg):
    sys.exit(f"BLOCKED: {msg}")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ffmpeg failed:\n{' '.join(cmd)}\n{r.stderr[-3000:]}")


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type:format=duration",
                        "-of", "json", path], capture_output=True, text=True)
    if r.returncode:
        die(f"cannot read {path}")
    j = json.loads(r.stdout)
    return {"audio": any(s["codec_type"] == "audio" for s in j["streams"]),
            "duration": float(j["format"]["duration"])}


def ts(v):
    """'90', '1:30', '00:01:30.5' -> seconds."""
    sec = 0.0
    for part in str(v).split(":"):
        sec = sec * 60 + float(part)
    return sec


# ---------- 1. source check ----------
def check_source(src, platform):
    rel = os.path.relpath(os.path.abspath(src), ROOT)
    if rel.startswith("capture" + os.sep):
        return {"kind": "own capture", "file": rel, "credit_line": "", "route": "own"}
    if not rel.startswith("sources" + os.sep):
        die(f"{rel} is not in capture/ or sources/. Put approved files there first.")
    with open(os.path.join(ROOT, "compliance", "sources.csv"), newline="") as f:
        rows = [r for r in csv.DictReader(f) if r.get("local_file", "").strip() == rel]
    if not rows:
        die(f"{rel} has no row in compliance/sources.csv (local_file column).")
    row = rows[0]
    route = row.get("route", "").strip()
    if route not in ("1", "2", "3"):
        die(f"route '{route}' is not an approved file route. Route 4 (YouTube Remix) happens inside YouTube.")
    perm = row.get("permission_file", "").strip()
    if not perm or not os.path.exists(os.path.join(ROOT, perm)):
        die(f"permission file '{perm}' is missing. Save it under compliance/permissions/.")
    try:
        posted = datetime.date.fromisoformat(row.get("source_posted_date", "").strip())
    except ValueError:
        die("source_posted_date must be YYYY-MM-DD.")
    if posted < RELEASE:
        die(f"source posted {posted}, before the {RELEASE} release. Pre-release footage is never allowed.")
    allowed = row.get("platforms_allowed", "").lower()
    wanted = ["youtube", "instagram"] if platform == "both" else [platform]
    for p in wanted:
        if p not in allowed:
            die(f"permission does not cover {p} (platforms_allowed: '{allowed}').")
    return {"kind": "approved source", "file": rel, "route": route, "url": row.get("video_url", ""),
            "uploader": row.get("uploader", ""), "credit_line": row.get("credit_line", ""),
            "tags_required": row.get("tags_required", ""),
            "monetization_allowed": row.get("monetization_allowed", "")}


# ---------- 2. stingers (built once, cached) ----------
def whoosh(dur):
    """Original synthesized whoosh plus low hit. No third-party audio."""
    return (f"anoisesrc=d={dur}:c=pink:a=0.5:r=48000,highpass=f=400,lowpass=f=6000,"
            f"afade=t=in:d={dur*0.6:.2f},afade=t=out:st={dur*0.6:.2f}:d={dur*0.4:.2f},volume=0.6[n];"
            f"sine=f=55:d={dur}:r=48000,afade=t=out:st=0.05:d={dur-0.05:.2f},volume=1.2[b];"
            f"[n][b]amix=inputs=2:normalize=0,aformat=channel_layouts=stereo,apad=whole_dur={dur}")


def card(png, out, w, h, dur, fade_in, fade_out, zoom=True, sfx=True):
    frames = int(dur * FPS)
    v = (f"[0:v]scale={w*2}:{h*2},"
         + (f"zoompan=z='1.08-0.08*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps={FPS},"
            if zoom else f"scale={w}:{h},fps={FPS},")
         + f"format=yuv420p,setsar=1")
    if fade_in:
        v += f",fade=t=in:d={fade_in}"
    if fade_out:
        v += f",fade=t=out:st={dur-fade_out:.2f}:d={fade_out}"
    a = whoosh(min(dur, 1.2)) if sfx else f"anullsrc=r=48000:cl=stereo"
    run(["ffmpeg", "-y", "-loop", "1", "-t", str(dur), "-i", png,
         "-filter_complex", f"{v}[v];{a},atrim=0:{dur}[a]", "-map", "[v]", "-map", "[a]",
         "-t", str(dur)] + ENC + [out])


def stingers():
    os.makedirs(STINGERS, exist_ok=True)
    want = {
        "intro-16x9.mp4": lambda o: card(f"{BRAND}/title-16x9.png", o, 1920, 1080, 2.5, 0.3, 0.4),
        "outro-9x16.mp4": lambda o: card(f"{BRAND}/title-9x16.png", o, 1080, 1920, 1.5, 0.2, 0.3),
        "endcard-16x9.mp4": lambda o: card(f"{BRAND}/end-card.png", o, 1920, 1080, 20, 0.5, 0.8, zoom=False, sfx=False),
    }
    for name, make in want.items():
        out = os.path.join(STINGERS, name)
        newest_brand = max(os.path.getmtime(os.path.join(BRAND, f)) for f in os.listdir(BRAND))
        if not os.path.exists(out) or os.path.getmtime(out) < newest_brand:
            print("building stinger", name)
            make(out)


# ---------- 3. body ----------
def body(src, info, a, out, tmp):
    w, h = SIZES[a.format]
    start, end = ts(a.start), ts(a.end)
    if end <= start:
        die("--end must be after --start.")
    dur = end - start
    lt = f"{BRAND}/lower-third-{'9x16' if a.format == 'short' else '16x9'}.png"
    if a.name_text:
        lt = os.path.join(tmp, "lt.png")
        asset = "lower-third-9x16" if a.format == "short" else "lower-third-16x9"
        subprocess.run(["node", os.path.join(ROOT, "brand", "render.js"), asset, "--name", a.name_text,
                        "--role", a.role_text, "--out", lt], check=True, capture_output=True)

    if a.format == "short" and a.reframe == "blur":
        frame = (f"[0:v]split[a][b];[a]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},boxblur=30:2[bg];"
                 f"[b]scale={w}:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[f0]")
    elif a.format == "short":
        frame = f"[0:v]scale=-2:{h},crop={w}:{h}:(iw-{w})*{a.crop_x}:0[f0]"
    else:
        frame = f"[0:v]scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2[f0]"
    bug_y = 140 if a.format == "short" else 40   # below the Shorts top bar
    v = (frame + f";[f0]fps={FPS},setsar=1[f1];"
         f"[1:v]format=rgba,scale=iw*{0.9 if a.format == 'short' else 0.75}:-1,colorchannelmixer=aa=0.92[bug];"
         f"[f1][bug]overlay=40:{bug_y}[f2];"
         f"[2:v]format=rgba,fade=t=in:st=1:d=0.3:alpha=1,fade=t=out:st=5.6:d=0.4:alpha=1[lt];"
         f"[f2][lt]overlay=0:0:enable='between(t,1,6)',format=yuv420p[v]")

    inputs = ["-ss", str(start), "-t", str(dur), "-i", src,
              "-loop", "1", "-t", str(dur), "-i", f"{BRAND}/bug.png",
              "-loop", "1", "-t", str(dur), "-i", lt]
    gain = {"keep": 1.0, "duck": 0.18 if a.vo else 0.6, "mute": 0.0}[a.game_audio]
    if info["audio"] and gain > 0:
        game = f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={gain}[g]"
    else:
        game = f"anullsrc=r=48000:cl=stereo,atrim=0:{dur}[g]"
    if a.vo:
        inputs += ["-i", a.vo]
        aud = (f"{game};[3:a]aformat=sample_rates=48000:channel_layouts=stereo,apad[vo];"
               f"[g][vo]amix=inputs=2:normalize=0:duration=first,atrim=0:{dur}[a]")
    else:
        aud = f"{game};[g]apad,atrim=0:{dur}[a]"
    run(["ffmpeg", "-y"] + inputs + ["-filter_complex", f"{v};{aud}", "-map", "[v]", "-map", "[a]",
                                     "-t", str(dur)] + ENC + [out])
    return dur


# ---------- 4. assemble ----------
def assemble(parts, out):
    ins = sum((["-i", p] for p in parts), [])
    n = len(parts)
    streams = "".join(f"[{i}:v][{i}:a]" for i in range(n))
    run(["ffmpeg", "-y"] + ins + ["-filter_complex",
         f"{streams}concat=n={n}:v=1:a=1[v][a0];[a0]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]",
         "-map", "[v]", "-map", "[a]", "-movflags", "+faststart"] + ENC + [out])


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source")
    p.add_argument("--start", required=True)
    p.add_argument("--end", required=True)
    p.add_argument("--format", choices=["short", "long"], default="short")
    p.add_argument("--platform", choices=["youtube", "instagram", "both"], default="both")
    p.add_argument("--vo", help="host voiceover file (wav/mp3/m4a)")
    p.add_argument("--game-audio", choices=["duck", "mute", "keep"], default="duck",
                   help="duck (default) lowers game audio under the VO. Use mute if game radio is audible.")
    p.add_argument("--reframe", choices=["crop", "blur"], default="crop", help="short only")
    p.add_argument("--crop-x", type=float, default=0.5, help="short crop: 0 = left edge, 1 = right edge")
    p.add_argument("--name-text", help="lower-third name (default: template text)")
    p.add_argument("--role-text", default="Brooklyn Vice Live")
    p.add_argument("--no-intro", action="store_true", help="long only: skip the intro card")
    p.add_argument("--name", required=True, help="output name, e.g. ep01-parking")
    a = p.parse_args()

    if not shutil.which("ffmpeg"):
        die("ffmpeg is not installed (run ./setup.sh).")
    if not os.path.exists(a.source):
        die(f"{a.source} not found.")
    src_info = check_source(a.source, a.platform)
    info = probe(a.source)
    if ts(a.end) > info["duration"] + 0.05:
        die(f"--end is past the end of the source ({info['duration']:.1f}s).")
    if a.vo and not os.path.exists(a.vo):
        die(f"voiceover {a.vo} not found.")

    stingers()
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    name = a.name + ("" if a.vo else "_DRAFT")
    out = os.path.join(ROOT, "out", name + ".mp4")
    with tempfile.TemporaryDirectory() as tmp:
        b = os.path.join(tmp, "body.mp4")
        dur = body(a.source, info, a, b, tmp)
        if a.format == "short":
            parts = [b, f"{STINGERS}/outro-9x16.mp4"]
        else:
            parts = ([] if a.no_intro else [f"{STINGERS}/intro-16x9.mp4"]) + [b, f"{STINGERS}/endcard-16x9.mp4"]
        assemble(parts, out)

    meta = {
        "name": name, "file": os.path.relpath(out, ROOT), "format": a.format, "platform": a.platform,
        "created": datetime.datetime.now().isoformat(timespec="seconds"),
        "source": src_info, "trim": {"start": ts(a.start), "end": ts(a.end), "seconds": round(dur, 2)},
        "voiceover": a.vo or None, "game_audio": a.game_audio,
        "music_source": "none (synthesized stinger sfx only)",
        "layers": {"footage": True, "voice": bool(a.vo), "edit": True, "frame": True},
        "ready_for_gate": bool(a.vo),
    }
    with open(os.path.join(ROOT, "out", name + ".json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"wrote {meta['file']} ({probe(out)['duration']:.1f}s)")
    if src_info.get("credit_line"):
        print("credit line for the description:", src_info["credit_line"])
    if not a.vo:
        print("DRAFT: no voiceover. A clip without the voice layer does not ship (CLAUDE.md section 3).")


if __name__ == "__main__":
    main()
