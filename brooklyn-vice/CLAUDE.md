# Brooklyn Vice

GTA 6 clip channel for YouTube (Shorts + long-form) and Instagram Reels. This file is the project brief and the standing rules for Claude Code. Read it before any task.

Status: planning. Last updated 2026-11-15. GTA VI launches 2026-11-19 on PS5 and Xbox Series X|S. No PC version announced.

Not legal advice. Before spending money on this, have a media/IP attorney review section 2 and the branding.

## 1. What we are building

A repeatable pipeline that turns GTA 6 gameplay into short, edited, commentated clips under one brand: Brooklyn Vice.

Working assumptions (change these here if they are wrong):

* Footage source is GTA 6 videos already posted on YouTube by other creators. Each source must come through one of the approved routes in 2.6.
* Our own captured gameplay is the fallback when no approved source exists.
* Every clip carries our own voice, text, and edit. No raw re-uploads.
* A human approves every post. Nothing auto-publishes without passing the compliance gate in section 4.
* The channel is entertainment. It does not advertise BoxHero, OTB, or any product (see 2.1).

## 2. Compliance rules

Three separate rule sets apply. Passing one does not mean passing the others.

### 2.1 Rockstar / Take-Two (the copyright owner)

Source: https://support.rockstargames.com/articles/200153756/rockstar-games-video-policy (last updated Jan 10, 2025). Re-read the live page at launch. It can change.

Allowed by the policy:

* Gameplay footage and clips, machinima.
* Cutscenes inside a larger playthrough or narrated Let's Play.

Removed by the policy:

* Pre-release or leaked footage of any kind, including early unboxing. Nothing from the game goes up before the official release time.
* Spoilers: the ending, edited cutscene or plot-dialogue compilations, big story reveals. No end date is given for this rule.
* Isolated cinematics.
* In-game TV shows, radio, or comedy performances posted in isolation.
* Cheats, money glitches, exploits, account selling, mod menus for online modes.
* Promotion of unauthorized mods or ports.

Known gaps between the policy and this project. These are the real risks:

* The policy covers "occasional, non-commercial" use by individual fans. "Non-commercial" is defined as not making money from the footage and not using it to promote a product or service. A monetized, high-volume channel is outside the written permission. Monetized gameplay channels are widely tolerated in practice, but that is tolerance, not a license. Take-Two can remove anything at any time.
* Because of that definition, never use game footage in an ad, a sponsor read for our own businesses, or a boosted/paid post.
* Questions go to copyright@take2games.com. Consider emailing them to describe the channel and ask.

### 2.2 Trademark and branding

* Do not use the official Grand Theft Auto VI logo, Rockstar logo, or official key art in channel art, avatars, banners, watermarks, or merch. The current mockup has the GTA VI logo in the top right. Remove it from anything that represents the channel.
* Do not imply affiliation. Channel description and About page carry: "Unofficial fan channel. Not affiliated with or endorsed by Rockstar Games or Take-Two Interactive."
* Saying "GTA 6" in plain text in titles and descriptions to describe the content is normal practice.
* The look (neon pink/cyan, sunset, graffiti lettering, Brooklyn landmarks) is ours to use. Keep the Brooklyn elements dominant so the brand stands on its own.
* No merch with game characters, game logos, or game screenshots.
* Only real people who have agreed to it appear in channel art.

### 2.3 Music

* GTA radio stations play licensed commercial tracks. They trigger Content ID claims and Instagram mutes.
* Capture with in-game radio off, or strip game music in the edit.
* Use only music we have a license for (YouTube Audio Library, a paid library with a social license) or platform-native audio added inside the app.

### 2.4 YouTube

Sources: https://support.google.com/youtube/answer/1311392 (channel monetization policies). Check the live page. It was rewritten in July 2026.

* Reused content policy: clips and compilations can monetize only with clear original value added, such as commentary, storyline, or substantial editing. It applies even with the owner's permission. A few violating videos can demonetize the whole channel.
* Inauthentic content policy: templated, repetitive, or mass-produced uploads cannot monetize. This is the main threat to a "farm". Each video must be recognizably different in content, not just in footage.
* AI disclosure: label altered or synthetic content where required. AI voiceover reading generic scripts is the pattern that gets flagged. Use a real host voice.
* GTA content is violent. Expect limited ads or age restriction on some uploads. Keep thumbnails and the first seconds clean.
* One channel. Do not run duplicate channels with the same content.

### 2.5 Instagram

* Since April 30, 2026, accounts that mostly post content they did not create are removed from recommendations (Explore, suggested feed, Reels). Followers still see posts. New viewers do not.
* Watermarks, crops, and speed changes do not count as original. Voiceover, green screen, on-screen text, and commentary do.
* Our own captured and edited gameplay with our voice on it is the safe format.
* No TikTok or CapCut watermarks on uploads.

### 2.6 Clipping from YouTube videos (primary source)

This is the highest-risk part of the project. Read it twice.

Every YouTube video of GTA 6 has two rights holders: Rockstar (the game) and the uploader (their voice, face, edit, and selection). Rockstar's fan policy covers a person posting their own gameplay. It does not give us rights to someone else's video. The uploader has to.

Approved routes. A source video must fit one of these:

1. Written permission from the uploader. Email or DM is fine. It must name our channel, the platforms (YouTube and Instagram), and whether we may monetize. Save it in `/compliance/permissions/`.
2. A creator's clipping program. Many streamers run these and publish terms, sometimes paying per view. Save a copy of the terms. Follow them exactly (required tags, credit, platforms allowed).
3. Creative Commons (CC BY) videos. Filter YouTube search by Creative Commons. Credit the uploader as the license requires. Note that the CC license only covers the uploader's layer.
4. YouTube's own Remix tools for Shorts (Cut, Green Screen). These stay on YouTube, link back to the source, and only work where the uploader left remixing on. They cannot be exported to Instagram.

Not approved:

* Downloading videos with third-party tools without permission. YouTube's Terms of Service prohibit downloading except through features YouTube provides or with permission from YouTube and the rights holder.
* "Credit to owner" or "no copyright intended" in place of permission. Credit is not a license.
* Relying on fair use as the business model. Fair use is a defense decided case by case in court. It is not something we can check off in advance. Heavy commentary and short excerpts help, but they do not make a clip farm safe.
* Clips from Rockstar's own trailers and official videos re-cut as content.
* Clips from leak channels or any pre-release footage.

Consequences if we skip this:

* Uploaders can file takedowns. Three active copyright strikes terminates a YouTube channel. Instagram disables repeat-infringer accounts.
* Even with permission, the YouTube reused content policy still applies. Clips need commentary or real editing to monetize.
* Instagram detects matching copies and shows the original in recommendations instead of ours. An account that mostly posts others' work loses recommendations entirely.

Source registry: every source video gets a row in `/compliance/sources.csv` before any download. Fields: video URL, uploader, route (1 to 4), permission file path, monetization allowed (y/n), platforms allowed, credit line required, date.

Outreach is part of the job. Build a list of mid-size GTA creators, pitch them a clipping deal (we cut and post, they get credit, a tag, and a link), and work from signed-up creators only.

## 3. Content format

Every clip has four layers. A clip missing any layer does not ship.

1. Footage: an approved source clip, kept short, reframed to 9:16 for Shorts/Reels or 16:9 for long-form.
2. Voice: host commentary, recorded for that clip.
3. Edit: cuts, zooms, captions, sound design.
4. Frame: Brooklyn Vice title card, lower third, end card.

Series ideas (each needs its own angle, not one template with swapped footage):

* A New Yorker reacts to Vice City.
* Brooklyn rules vs Leonida rules.
* One detail you missed. Gameplay systems and world details, never story.
* Stunt or fail of the day, with a call on what went wrong.
* Weekly long-form recap built from the week's best moments with new commentary.

Spoiler rule for all series: free-roam, world, and mechanics content only. No mission cutscenes, no story beats in titles or thumbnails.

Cadence target: quality first. Start at 1 short per day and 1 long-form per week. Raise volume only if each video still passes the "recognizably different" test.

Copy style for titles, captions, on-screen text: plain short sentences. No em-dash asides. No "not X but Y". No setup-then-payoff. State the point flat.

## 4. Compliance gate (every post)

A post is blocked unless all answers are yes.

* [ ] Source video has a row in `sources.csv` with an approved route and a saved permission or license
* [ ] Source footage was posted after official release and is not from a leak
* [ ] Credit line and tags match what the uploader or program requires
* [ ] Platform is one the permission covers
* [ ] No ending, story reveal, isolated cutscene, or cutscene compilation
* [ ] No isolated in-game TV, radio, or comedy show
* [ ] No cheat, glitch, exploit, or mod promotion
* [ ] No game radio or unlicensed music in the audio
* [ ] Original voice commentary present
* [ ] Not a near-duplicate of a prior upload (script and structure differ)
* [ ] No official GTA or Rockstar logo in thumbnail or frame
* [ ] No product promotion or sponsor tied to the footage
* [ ] AI/altered content label set correctly
* [ ] Human reviewer initials and date logged

Log every post in `/compliance/log.csv`: date, platform, URL, footage source, music source, reviewer, any claim or strike received.

If a claim, strike, or takedown arrives: stop the series it came from, log it, do not re-upload, do not file a counter-notice without attorney review.

## 5. Pipeline (to build in Claude Code)

```
brooklyn-vice/
  CLAUDE.md                 this file
  outreach/                 creator list, pitch templates, deal status
  sources/                  approved source videos (gitignored)
  capture/                  our own console captures, fallback (gitignored)
  clips/                    selected moments, trimmed
  scripts/                  commentary scripts per clip (markdown)
  vo/                       recorded voiceover
  edit/                     ffmpeg/Remotion templates, caption styles
  out/                      rendered 9:16 and 16:9 files
  publish/                  queue + metadata (title, description, tags)
  compliance/
    gate.py                 runs the section 4 checklist, blocks on failure
    log.csv
    sources.csv             registry of approved source videos
    permissions/
  brand/                    fonts, colors, title cards, lower thirds (see brand/BRAND.md)
  channel/                  YouTube setup steps and growth playbook
  docs/                     policy snapshots with date saved
```

Build order:

1. `brand/`: palette, type, title card, lower third, end card. No Rockstar assets.
2. `edit/`: ffmpeg pipeline for trim, reframe to 9:16, burn captions (Whisper transcript of our VO), loudness normalize, strip game music track.
3. `compliance/gate.py`: checklist as code, plus duplicate-script check and audio fingerprint check against a blocklist.
4. `publish/`: metadata generator, then upload queue. YouTube Data API and Instagram Graph API. Uploads stay as drafts or scheduled until a human approves.
5. `docs/`: script that saves dated copies of the Rockstar, YouTube, and Instagram policy pages weekly and flags diffs.

Rules for Claude Code in this repo:

* Never download a video unless its URL is in `compliance/sources.csv` with an approved route. No bulk scraping of YouTube, Twitch, Kick, or TikTok.
* Never publish. Queue only.
* Never generate thumbnails or art containing GTA/Rockstar logos, game characters, or real people.
* If a task conflicts with section 2, stop and say so.

## 6. Open decisions

* Who is the host voice?
* Capture setup: PS5 or Xbox, capture card, radio-off settings.
* Which creators do we pitch first, and what do we offer them (credit only, rev share, flat fee)?
* Do we join existing paid clipping programs, or only run our own deals?
* Monetization goal: YPP ad revenue, or audience first?
* Attorney review of section 2 and the brand name.
* Email to copyright@take2games.com: send or not.
