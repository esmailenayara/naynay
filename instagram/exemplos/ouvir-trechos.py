import sys, os, re, subprocess, wave, numpy as np
sys.path.insert(0, os.getcwd())
import montar_lote as ml
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
nome = sys.argv[1]
for f, jan in ml.VIDEOS[nome]:
    w = wave.open(f"audio/{f}.wav"); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    for a, b in ml.falas(f, jan):
        seg, _ = m.transcribe(x[int(a*sr):int(b*sr)], language="pt", initial_prompt="Método N.E. Face")
        print(f"{f} {a:6.2f}-{b:6.2f}:", " ".join(s.text.strip() for s in seg), flush=True)
