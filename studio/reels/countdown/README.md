# Countdown reel (Boo style)

A fast "top N" list reel, 1080×1920, about 30–40 s:

- **Header** (top-left): orange bar, the list title, "@chirag.zip · explained by Boo".
- **Hook**: N dark icon tiles pop in; the last tile is a "?" with a LAST sticker ("Don't skip the last one!").
- **Carousel** (top half): one white card per item: icon tile, number chip, a small cartoon diagram, title with an orange underline, a one-line description. Neighbouring cards sit blurred to the sides; a "#01 Number one" pill and pagination dots track the position. A whoosh plays on each slide.
- **Boo** (bottom-left) changes mood per item and does a little squash on every word.
- **Captions** (bottom-right) appear word by word, synced to Boo's voice: small words above, the keyword huge in orange with an outline.
- **Ending**: a summary card of all items, Boo celebrates, "Save THIS!" then "follow @chirag.zip", over the signature jingle. No spoken sign-off.

## Files

- `script.py`: the content. `LINES` = the hook plus one line per item; each line is a list of caption chunks, each chunk a list of `(display word, phonemes, big?)`. `ITEMS` = card data (name, number word, description, summary tag, icon). `MOODS` = Boo's mood per line.
- `voice.py`: voices every line with Boo's voice settings (see `studio/VOICE.md`) and writes `lineN.wav` plus `timing.json` (start time of every word). It needs the **timing-capable** Kokoro export: `model-files-v1.1/kokoro-v1.0.onnx` from the kokoro-onnx GitHub releases. Afterwards pitch each line up: `ffmpeg -i lineN.wav -af "asetrate=24000*1.19,aresample=48000,atempo=1/1.19" cuteN.wav`.
- `build.py`: builds `reel.html` and `timeline.json` from the script and timings (needs `../../moods.py`, and `boo.png`, `Fredoka.ttf`, `boo_jingle.wav` from `studio/assets/` copied next to it).
- `film.py`: `python3 film.py test 3.5 9 …` saves still frames; `python3 film.py full` renders `tmp_video.mp4` at 30 fps.
- Mix: the voice lines at their start times, a soft whoosh before each card, pops on the hook tiles, a ding on LAST, and the jingle 0.2 s after the last line at 80%. Normalise to −14 LUFS.

Icons available for cards: array, stack, queue, hash, tree, graph (add more in `ICON` and `illo()` in build.py).

First made: `queue/009-data-structures-countdown` (6 data structures every coder needs).
