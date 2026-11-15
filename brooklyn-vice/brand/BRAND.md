# Brooklyn Vice brand kit

Everything here is our own work. It has no Rockstar or GTA logos, key art, or game characters. It has no real people. The host photo is a slot you fill with a photo of a host who has agreed to appear.

## Palette

| Token | Hex | Use |
|---|---|---|
| Night | `#12061f` | Backgrounds, text boxes |
| Plum | `#2a1146` | Skyline, secondary backgrounds |
| Violet | `#5b1d8a` | Sky, gradients |
| Pink | `#ff2ea6` | Primary accent, borders, graffiti tags |
| Cyan | `#19e3ff` | Secondary accent, labels |
| Sunset | `#ff8a3d` | Sun, warm highlights |
| Gold | `#ffc94a` | Highlight word in thumbnail headlines |
| White | `#ffffff` | Logo and headline text |

"Vice" gradient: pink `#ff2ea6` to cyan `#19e3ff`, left to right.

## Type

All fonts are in `fonts/` with their licenses (SIL OFL or Apache 2.0). They are free for commercial use.

| Font | Role |
|---|---|
| Rubik Wet Paint | "BROOKLYN" in the logo. Drippy paint letters. |
| Permanent Marker | "VICE" in the logo. Brush script. |
| Anton | Thumbnail and Shorts headlines. Uppercase. |
| Sedgwick Ave Display | Graffiti taglines ("Same hustle. New city.") |
| Inter | Labels, lower-third roles, small UI text |

## Logo

Crown over "BROOKLYN" in white wet paint, "VICE" in the gradient brush script below it, with a gradient swoosh underline. Small uses get the one-line version: crown, then BROOKLYN VICE on a black tab with a pink left edge. The avatar and watermark use the crown over a "BV" monogram.

Rules:
* Keep the black outline on the logo over any background.
* Never place a GTA or Rockstar logo next to ours.
* The sign, bridge and skyline are what make the brand Brooklyn. Keep them. Palms are the Vice City nod and stay at the edges.

## Files in `export/`

| File | Size | Where it goes |
|---|---|---|
| `avatar.png` | 800x800 | YouTube profile picture, Instagram profile picture |
| `banner.png` | 2560x1440 | YouTube banner. Logo and text sit in the 1546x423 safe area. |
| `banner-safe.png` | 2560x1440 | Same banner with the safe area drawn on it. For checking only. Do not upload. |
| `watermark.png` | 150x150 | YouTube video watermark (Studio > Customization > Branding) |
| `title-16x9.png` | 1920x1080 | Long-form intro card (1 to 2 seconds) |
| `title-9x16.png` | 1080x1920 | Shorts and Reels intro or outro card |
| `lower-third-16x9.png` | 1920x1080, transparent | Host name overlay for long-form |
| `lower-third-9x16.png` | 1080x1920, transparent | Host name overlay for Shorts, placed above the Shorts UI |
| `end-card.png` | 1920x1080 | Last 20 seconds of long-form. YouTube end-screen elements go on the two frames (videos) and the circle (subscribe). |
| `thumbnail.png` | 1280x720 | Example thumbnail with the host slot empty |
| `shorts-cover.png` | 1080x1920 | Example Shorts and Reels cover |

## Making a new thumbnail

```bash
node brand/render.js thumbnail --text "Brooklyn|*rules*|in Leonida" --bg clips/frame.png --host brand/host/host-cutout.png --out out/thumbs/ep01.png
```

Headline markup: `|` breaks a line, `*word*` is gold, `_word_` is pink, `~word~` is cyan. Use `--size` to change the font size (default 128). `shorts-cover` takes the same options. The lower thirds take `--name` and `--role`.

Thumbnail rules:
* Three to five words. One highlighted word.
* The background is a gameplay frame from an approved source or our own capture. No official art or trailer frames.
* No story spoilers. No gore, guns aimed at the camera, or blood in the frame. Thumbnails like that get limited ads.
* The host face shows a real reaction. It must match what happens in the video.

## From the mockup: kept and dropped

Kept: the neon pink and cyan, sunset, Brooklyn sign, Brooklyn Bridge, palms, graffiti taglines, crown, the drip "BROOKLYN" and brush "VICE" lockup.

Dropped:
* The GTA VI logo (section 2.2).
* The generated photo of a person. Real people only, with consent. Use the host slot.
* "Good people ship things". It reads like a company tagline, and the channel does not promote a business (section 1).
* Cigar, cash stacks, and supercar props. They lower ad suitability, and the cash stack reads as a money-glitch promise.

## Regenerating

```bash
node brand/render.js           # all assets
node brand/render.js banner    # one asset
```

Needs Node and Playwright with Chromium (preinstalled in the cloud container).
