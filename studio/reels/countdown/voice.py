import sys, types, json, wave
import numpy as np
for m in ['espeakng_loader','phonemizer','phonemizer.backend','phonemizer.backend.espeak','phonemizer.backend.espeak.wrapper']:
    sys.modules[m]=types.ModuleType(m)
sys.modules['phonemizer.backend.espeak.wrapper'].EspeakWrapper=object
sys.path.insert(0,'src/src')
import importlib.metadata as im
_v=im.version; im.version=lambda n: "0.0.0" if "kokoro" in n else _v(n)
import kokoro_onnx.tokenizer as tk
tk.Tokenizer.__init__=lambda self, espeak_config=None, vocab=None: setattr(self,'vocab',vocab or tk.DEFAULT_VOCAB)
from kokoro_onnx import Kokoro
sys.path.insert(0, sys.argv[1]); from script import LINES
out_dir=sys.argv[2]
k=Kokoro('v11/kokoro-v1.0.onnx','voices-v1.0.bin')
meta=[]
for li,line in enumerate(LINES):
    words=[w for ch in line for w in ch]
    ph=" ".join(w[1] for w in words)
    known=k.tokenizer.known(ph)
    assert known==ph, (li, ph, known)
    audio,sr,spoken=k.create_timed(ph, voice='af_bella', speed=1.08, is_phonemes=True, sentence_pause=0.18, clause_pause=0.08)
    audio=np.asarray(audio,dtype=np.float32)
    # word starts: walk the spoken phonemes, a space ends a word
    starts=[]; wi=0; at_word_start=True
    for t in spoken:
        if t.phoneme==" ":
            at_word_start=True; continue
        if at_word_start:
            starts.append(round(t.start,3)); at_word_start=False
    assert len(starts)==len(words), (li, len(starts), len(words), [t.phoneme for t in spoken][:20])
    with wave.open(f'{out_dir}/line{li}.wav','wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(audio,-1,1)*32767).astype(np.int16).tobytes())
    meta.append({"dur": round(len(audio)/sr,3), "starts": starts})
    print(li, meta[-1]["dur"], starts[:6])
json.dump(meta, open(f'{out_dir}/timing.json','w'))
