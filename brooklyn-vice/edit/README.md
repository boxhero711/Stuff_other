# Edit pipeline

`clip.py` turns a source file into a branded clip with our intro and outro. It never uploads.

## Quick start

```bash
# Short (9:16) from our own capture, with host voiceover
python3 edit/clip.py capture/session1.mp4 --start 1:12 --end 1:41 --format short --vo vo/ep01.wav --name ep01-parking

# Long-form (16:9) from an approved source, game audio muted, host name in the lower third
python3 edit/clip.py sources/creatorx-0412.mp4 --start 30 --end 95 --format long --game-audio mute \
    --vo vo/recap01.wav --name-text "HOST NAME" --name recap01-seg1
```

Output: `out/<name>.mp4` plus `out/<name>.json` (source, credit line, layers, trim). No `--vo` means the file is written as `<name>_DRAFT.mp4`. The voice layer is required to ship.

## What goes where

| Format | Order | Size |
|---|---|---|
| short | clip, then 1.5s outro card (`title-9x16`) | 1080x1920 |
| long | 2.5s intro card (`title-16x9`), clip, 20s end card | 1920x1080 |

On every clip: the corner tag (`bug.png`) for the whole clip, and the lower third from 1s to 6s. The intro and outro cards are built once into `edit/stingers/` and rebuilt when the brand files change. Their whoosh sound is synthesized by ffmpeg, so there's no third-party audio.

## Source rules (enforced)

* `capture/` is our own console footage. Allowed.
* `sources/` files need a row in `compliance/sources.csv` with `local_file` set to the path, route 1, 2 or 3, an existing `permission_file`, `source_posted_date` on or after 2026-11-19, and the target platform in `platforms_allowed`. Otherwise the script stops with `BLOCKED`.
* Ask creators to send their original files. Do not download from YouTube with third-party tools (CLAUDE.md 2.6).

## Options

| Option | Default | Notes |
|---|---|---|
| `--game-audio` | duck | `duck` lowers game audio under the VO. `mute` if game radio is audible (CLAUDE.md 2.3). |
| `--reframe` | crop | Short only. `blur` fits the full frame over a blurred copy. |
| `--crop-x` | 0.5 | Short crop position. 0 is the left edge, 1 the right. |
| `--platform` | both | Checked against the source permission. |
| `--no-intro` | off | Long only. |

Loudness is normalized to -14 LUFS, true peak -1.5 dB.

## Not built yet

Burned-in captions from a Whisper transcript of the VO (build order step 2) and the compliance gate (`compliance/gate.py`, step 3).
