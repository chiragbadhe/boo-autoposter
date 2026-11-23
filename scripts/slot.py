#!/usr/bin/env python3
"""Decide whether this scheduled run should post, so the feed looks human.

Each day (IST) gets 1, 2 or 3 posts, chosen at random but fixed for that day:
the date seeds the random generator, so every run on the same day agrees on
which of the day's slots post. Slots are the cron lines in post.yml, matched
by the cron string GitHub passes in SCHEDULE.

Environment:
  SCHEDULE    the cron string that fired this run (github.event.schedule);
              empty for a manual run, which always posts.
  SLOTS       the cron strings, one per line, in time order.
Writes go=true|false and delay=<seconds> to GITHUB_OUTPUT.
"""
import datetime
import os
import random

WEIGHTS = {1: 30, 2: 45, 3: 25}   # how often a day gets 1, 2 or 3 posts


def main():
    schedule = os.environ.get("SCHEDULE", "").strip()
    slots = [s.strip() for s in os.environ.get("SLOTS", "").splitlines() if s.strip()]
    ist = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5, minutes=30)
    day = ist.strftime("%Y-%m-%d")
    rng = random.Random(f"boo-{day}")
    count = rng.choices(list(WEIGHTS), weights=list(WEIGHTS.values()))[0]
    chosen = sorted(rng.sample(range(len(slots)), min(count, len(slots))))

    if not schedule:
        go, why = True, "manual run"
    elif schedule not in slots:
        go, why = True, f"unknown slot {schedule!r}, posting to be safe"
    else:
        idx = slots.index(schedule)
        go = idx in chosen
        why = f"slot {idx + 1} of {len(slots)}"
    # A random wait so the minute differs every time (manual runs don't wait).
    delay = random.randint(0, 25 * 60) if (go and schedule) else 0

    print(f"{day} IST: {count} post(s) today in slots {[i + 1 for i in chosen]}; "
          f"this run ({why}): {'POST' if go else 'skip'}"
          + (f" after {delay // 60} min" if delay else ""))
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(f"go={'true' if go else 'false'}\ndelay={delay}\n")


if __name__ == "__main__":
    main()
