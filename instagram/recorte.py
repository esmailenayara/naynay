"""Recorta a pessoa do fundo, quadro a quadro, e gera um vídeo de máscara (branco = pessoa).

Usado pela tela dividida para a cabeça dela ficar NA FRENTE do cartão, como na referência.
Uso:  python3 -I recorte.py <entrada (vídeo ou foto)> <mascara.mkv> [segundos, só para foto]
A entrada é enquadrada em 1080x1920 do mesmo jeito que o tela-dividida.sh faz.
Modelo: Robust Video Matting (mobilenetv3), baixado sozinho na primeira vez.
Precisa de:  pip install onnxruntime
"""
import os, subprocess, sys, urllib.request
import numpy as np
import onnxruntime as ort

W, H = 1080, 1920
URL = "https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3_fp32.onnx"
modelo = os.path.expanduser("~/.cache/rvm_mobilenetv3_fp32.onnx")
if not os.path.exists(modelo):
    os.makedirs(os.path.dirname(modelo), exist_ok=True); urllib.request.urlretrieve(URL, modelo)

ent, saida = sys.argv[1], sys.argv[2]
foto = ent.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
cobrir = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
ler = ["ffmpeg", "-v", "error"] + (["-loop", "1", "-framerate", "30", "-t", sys.argv[3] if len(sys.argv) > 3 else "5"] if foto else []) \
      + ["-i", ent, "-vf", cobrir, "-r", "30", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
gravar = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", "30",
          "-i", "-", "-c:v", "ffv1", saida]
pl, pg = subprocess.Popen(ler, stdout=subprocess.PIPE), subprocess.Popen(gravar, stdin=subprocess.PIPE)

s = ort.InferenceSession(modelo, providers=["CPUExecutionProvider"])
rec = [np.zeros((1, 1, 1, 1), np.float32)] * 4
ds = np.array([0.25], np.float32)
n = 0
while True:
    buf = pl.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    src = np.frombuffer(buf, np.uint8).reshape(H, W, 3).transpose(2, 0, 1)[None].astype(np.float32) / 255
    # numa foto, repete o 1º quadro algumas vezes para o modelo "assentar"
    for _ in range(4 if (foto and n == 0) else 1):
        fgr, pha, *rec = s.run(None, {"src": src, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3], "downsample_ratio": ds})
    pg.stdin.write((pha[0, 0] * 255).clip(0, 255).astype(np.uint8).tobytes()); n += 1
pg.stdin.close(); pg.wait()
print(f"máscara pronta: {saida} ({n} quadros)")
