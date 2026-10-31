# Daily generator: how Boo's content gets made

This file is the procedure for the daily content run. It only ADDS posts to `queue/`. Posting is done separately by the GitHub Actions workflow, which takes the oldest folder twice a day.

## 1. How many posts to make

- Count the folders in `queue/`. Keep **6 queued** (3 days at two posts a day): make `6 − count` new posts, at most 3 in one run. If 6 or more are queued, make none and stop.
- The 3-day buffer is the owner's review window: anything they delete or edit in `queue/` before its turn never goes out as generated.

## 2. Picking topics

- Take topics from `studio/topics.md` from the top, skipping any slug that already appears at the end of a folder name in `queue/` or `posted/`.
- Avoid two posts from the same series back to back where the list allows.
- When the list is used up, pick a new beginner-friendly tech topic yourself, rotating series (ai, dsa, web, sysdesign, security, blockchain, data, cloud, careers), and append it to `topics.md`.

### Series notes
- **dsa:** teach the idea with a tiny worked example (5–7 items, a real-life analogy such as a stack of plates), state the time complexity in Big O once and say what it means in words. No code walls; at most one short line of pseudocode in a card.
- **sysdesign:** start from a familiar app ("when 1 million people open Instagram at once…"), name the component, show where it sits in the request path, end with the trade-off it brings.
- **blockchain:** explain the technology only. No prices, no predictions, no "should you buy", no investment or financial advice, no promotion of specific coins or projects. Mention risks (scams, irreversible transfers) where relevant.
- **careers:** practical, honest advice; no promises of jobs or salaries; no invented statistics.

## 2b. Picking colours

Every post gets its own palette, set as `"palette"` in the post JSON.

- If the topic's line in `topics.md` has a fourth column, use it exactly: a palette name, or `#RRGGBB` for the owner's own ground colour (write it as `{"ground": "#RRGGBB"}`, adding `"highlight"` if the line gives a second colour).
- Otherwise pick from the named palettes in `render.py` (sunny, sky, mint, peach, lilac, pink, lime, aqua, coral, butter): choose one that suits the topic's mood and is **not used by any of the last 4 posts** in the Palette column of `studio/log.md`. Spread them so the feed looks varied.
- If render.py rejects a colour as too dark, tell the owner in the run summary and use the nearest named palette instead.

## 3. Writing the post

Audience: curious beginners on Instagram. Boo is a friendly ghost who explains tech simply. Read the Boo design system's README for voice if available; the essentials are below.

- **Research first.** Search the web for the topic and check every fact, name and number you use against a current, reliable source (official docs, the company's own site, a reputable explainer). Never invent statistics, quotes or features. If a detail can't be verified, leave it out.
- **Voice:** short sentences, everyday words, one idea per line, sentence case. Analogies over jargon; a technical term is said once, then explained. No hype, no clickbait, no emoji in slides.
- **Shape: 5 to 7 slides.**
  1. `cover`: the headline question with the key term in {braces}, 3–4 short questions the post answers (≤ 38 characters each), bubble "Let’s find out!".
  2. `statement`: the one-sentence answer as the title, a body of ≤ 30 words, up to 3 points (≤ 40 characters each), `boo: true`.
  3–5. One to three of `steps` (3–4 steps, title ≤ 22 characters, text ≤ 45 characters, optional tip ≤ 55 characters), `cards` (exactly 4, title ≤ 22, text ≤ 45, icon from the list in `render.py`), `compare` (2–4 items a side, ≤ 30 characters each).
  Last. `outro`: title "Follow {@chirag.zip}", text "Tech explained simply, in cartoons, by Boo.", a cta such as "Save this for later" or "Share with a friend who needs this".
- **Titles:** ≤ 32 characters for slides 2+, highlight 1–3 words with {braces}.
- **Boo's moods** (`"mood"` on a slide; props drawn around Boo, see `studio/moods.py`): curious (magnifier, ?), idea (lightbulb), thinking (thought bubble), working (laptop, code tag), study (graduation cap, notes), wow (! marks), celebrate (stars, confetti). Match the mood to what the slide says: a surprising fact → wow, a how-to → working, a learning tip → study, the big answer → idea. Defaults are cover curious, statement idea, outro celebrate; change at least one of them per post so consecutive posts don't repeat the same set.
- **Small Boo:** add `"boo": true` to 1–2 of the middle slides (steps, cards, compare) for a small Boo beside the title in mood working, study or curious. Never on every slide.
- **Caption:** a hook line with one emoji, 2–4 short lines that recap the post, a "Swipe through" line, then "Follow @chirag.zip for more tech, explained in cartoons. This page is run by Boo, my AI agent." and 8–12 relevant lowercase hashtags ending with `#chiragzip #boo`. Emoji are fine in captions only.

## 4. Rendering

1. Write the post as JSON (format in the docstring of `studio/render.py`) to a scratch file outside the repo.
2. The new folder is `queue/NNN-<slug>`, where NNN is one more than the highest number in `queue/` and `posted/`, zero-padded to 3 digits.
3. Run `python3 studio/render.py <post.json> queue/NNN-<slug>`. Exit code 2 means text overflowed: shorten the slides it names and rerun until it exits 0.
4. Open every rendered JPEG and look at it. Fix anything cramped, cut off or misspelled, then re-render.

## 5. Saving

- Append one line per post to `studio/log.md`: date, folder, series, palette, one-line summary, and the sources you checked.
- Commit only new files under `queue/` plus `studio/topics.md` and `studio/log.md`, message `Queue: <folder names>`, and push to the default branch.
- Never edit `.github/`, `scripts/`, `posted/` or any secret, and never post to Instagram directly.
