# Daily generator: how Boo's content gets made

This file is the procedure for the daily content run. It only ADDS posts to `queue/`. Posting is done separately by the GitHub Actions workflow, which takes the oldest folder twice a day.

## 1. How many posts to make

- Count the folders in `queue/`. Keep **6 queued** (3 days at two posts a day): make `6 − count` new posts, at most 3 in one run. If 6 or more are queued, make none and stop.
- The 3-day buffer is the owner's review window: anything they delete or edit in `queue/` before its turn never goes out as generated.

## 2. Picking topics

- Take topics from `studio/topics.md` from the top, skipping any slug that already appears at the end of a folder name in `queue/` or `posted/`.
- Avoid two posts from the same series back to back where the list allows.
- When the list is used up, pick a new beginner-friendly tech topic yourself, rotating series (ai, web, data, cloud, security, careers), and append it to `topics.md`.

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
- **Caption:** a hook line with one emoji, 2–4 short lines that recap the post, a "Swipe through" line, then "Follow @chirag.zip for more tech, explained in cartoons. This page is run by Boo, my AI agent." and 8–12 relevant lowercase hashtags ending with `#chiragzip #boo`. Emoji are fine in captions only.

## 4. Rendering

1. Write the post as JSON (format in the docstring of `studio/render.py`) to a scratch file outside the repo.
2. The new folder is `queue/NNN-<slug>`, where NNN is one more than the highest number in `queue/` and `posted/`, zero-padded to 3 digits.
3. Run `python3 studio/render.py <post.json> queue/NNN-<slug>`. Exit code 2 means text overflowed: shorten the slides it names and rerun until it exits 0.
4. Open every rendered JPEG and look at it. Fix anything cramped, cut off or misspelled, then re-render.

## 5. Saving

- Append one line per post to `studio/log.md`: date, folder, series, one-line summary, and the sources you checked.
- Commit only new files under `queue/` plus `studio/topics.md` and `studio/log.md`, message `Queue: <folder names>`, and push to the default branch.
- Never edit `.github/`, `scripts/`, `posted/` or any secret, and never post to Instagram directly.
