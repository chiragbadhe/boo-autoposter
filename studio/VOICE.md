# Boo's voice (reels)

Chosen by Chirag on 2026-10-31: **option C, bright and bubbly baby ghost**.

- Model: Kokoro v1.0 (kokoro-onnx), voice `af_bella`, speed `1.08`
- Pitch: raised about 3 semitones after synthesis, keeping the length:
  `ffmpeg -i in.wav -af "asetrate=24000*1.19,aresample=48000,atempo=1/1.19" out.wav`
- Text is fed as phonemes (espeak-style American IPA) so names like "chirag dot zip" (`tʃɪɹˈɑːɡ dˈɑːt zˈɪp`) are said right.

Script style: fun and casual. Boo opens with "Boo! Did I scare you?", uses everyday analogies (lockers, treasure hunts), short punchy lines, a little sound effect word now and then ("Zoom!", "Ugh.", "Easy peasy!"), and signs off with "Follow chirag dot zip for more spooky smart tech. Boo!"
Facts stay accurate: every claim is checked before it's voiced.
