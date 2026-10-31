# Boo's voice (reels)

Chosen by Chirag on 2026-10-31: **option C, bright and bubbly baby ghost**.

- Model: Kokoro v1.0 (kokoro-onnx), voice `af_bella`, speed `1.08`
- Pitch: raised about 3 semitones after synthesis, keeping the length:
  `ffmpeg -i in.wav -af "asetrate=24000*1.19,aresample=48000,atempo=1/1.19" out.wav`
- Text is fed as phonemes (espeak-style American IPA) so names like "chirag dot zip" (`tʃɪɹˈɑːɡ dˈɑːt zˈɪp`) are said right.

Script style: fun and casual. No spoken intro: the reel opens straight on the first explanation line (the hook is the topic itself). Boo uses everyday analogies (lockers, treasure hunts), short punchy lines, and a little sound effect word now and then ("Zoom!", "Ugh.", "Easy peasy!").

Ending: no spoken sign-off. Boo celebrates on screen with "Follow @chirag.zip" while the signature jingle plays: `studio/assets/boo_jingle.wav` (3.8 s, a ghostly "woo" slide into a sparkly chime, composed for Boo). Mix it at 80% volume, starting about 0.5 s after the last line.
Facts stay accurate: every claim is checked before it's voiced.
