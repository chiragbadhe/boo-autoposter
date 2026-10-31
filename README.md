# Boo autopost

Posts the next carousel from `queue/` to Instagram twice a day (8:47 AM and 6:47 PM IST), using GitHub Actions and the Instagram API. Nothing runs on your computer.

## How it works

1. Each post is a folder in `queue/`, e.g. `queue/001-linktree/`, holding `01.jpg`, `02.jpg`… (JPEG, 1080×1350) and `caption.txt`.
2. On each run the workflow takes the first folder by name, posts it (1 image = single post, 2–20 = carousel), then moves it to `posted/`.
3. Empty queue = the run does nothing. Name folders `001-…`, `002-…` so they post in order.

## One-time setup (about 10 minutes)

1. **Make a GitHub repository** (it must be **public**: Meta downloads the images from a public link, served by the free jsDelivr CDN). Upload everything in this folder, including the hidden `.github` folder.
2. **Add your keys as secrets**, never in a file: repo → Settings → Secrets and variables → Actions → New repository secret:
   - `IG_ACCESS_TOKEN`: your long-lived access token
   - `IG_USER_ID`: your Instagram professional account ID
3. **Pick your API host** (Settings → Secrets and variables → Actions → Variables tab), only if needed:
   - Token from **Instagram Login** (starts with `IG…`): nothing to do, the default `graph.instagram.com` is right.
   - Token from **Facebook Login / a Facebook Page** (starts with `EAA…`): add variable `GRAPH_HOST` = `graph.facebook.com`.
   - Optional `GRAPH_VERSION`, e.g. `v23.0`. Left empty, Meta uses its default version.
4. **Test without posting**: Actions → Boo autopost → Run workflow → keep "Dry run" ticked. The log shows which folder and image links it would post. Open one image link to check it loads.
5. **Post for real once**: Run workflow again with "Dry run" unticked. The Linktree carousel goes live and its folder moves to `posted/`.
6. From now on it runs on schedule by itself.

## Your token expires

Long-lived Instagram tokens last about 60 days. Before then, refresh it in the Meta developer dashboard (or with the refresh-token endpoint) and paste the new value into the `IG_ACCESS_TOKEN` secret. A run with an expired token fails with a clear "Graph API error 190" in the log and posts nothing.

## Changing the schedule

Edit the two `cron` lines in `.github/workflows/post.yml` (times are UTC; IST = UTC + 5:30). One line = once a day. GitHub can start scheduled runs a few minutes late, and pauses schedules in repos with no activity for 60 days; each post's commit counts as activity.

## Adding posts

Ask Boo (Claude) for the next carousel: you get the slides as JPEGs plus `caption.txt`. Put them in a new numbered folder in `queue/` and commit. Keep a few days of posts queued.

## Rules this follows

- JPEG only, up to 20 images per carousel; the first image's shape (4:5 here) is used for the whole carousel.
- Instagram allows far more API posts per day than two, so twice daily is safe.
- Posts are fully public the moment they publish: check each queued folder before it reaches the front of the queue.

## Daily content (the studio)

`studio/` is how new posts get made automatically:

- `studio/render.py` turns a short post description into on-brand 1080×1350 JPEGs (Boo, Fredoka, the series colours).
- `studio/topics.md` is the topic plan, worked through top to bottom. Edit, reorder or add topics any time.
- `studio/GENERATOR.md` is the procedure the daily Claude run follows: research, write, render, check, push.
- `studio/log.md` records every generated post and the sources behind it.

The daily run keeps about **3 days of posts queued**. That buffer is your review window: open `queue/` on GitHub, and delete or replace any folder before its turn. Whatever is still there gets posted.
