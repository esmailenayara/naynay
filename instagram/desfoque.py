"""Desfoca o fundo atrás da pessoa ("modo retrato"), como nos vídeos da referência.

Uso:  python3 -I desfoque.py <video.mkv> <mascara.mkv> <saida.mkv> [intensidade=22] [so-fundo]
      "so-fundo" = grava só o fundo desfocado, SEM a pessoa (usado para preencher o espaço quando ela
      desce na tela por causa de um cartão de foto).
A máscara vem do recorte.py (mesmo tamanho e número de quadros do vídeo).

Por que não basta um gblur no ffmpeg: o desfoque "espalha" o cabelo escuro no fundo e cria
uma sombra em volta da cabeça. Aqui o fundo é desfocado SEM a pessoa (desfoque normalizado
pela máscara), então a borda fica limpa.
Precisa de:  pip install opencv-python-headless
"""
import subprocess, sys
import cv2
import numpy as np

ent, masc, saida = sys.argv[1:4]
sigma = float(sys.argv[4]) if len(sys.argv) > 4 else 22
so_fundo = len(sys.argv) > 5 and sys.argv[5] == "so-fundo"
W, H = 1080, 1920
info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                       "-of", "csv=p=0", ent], capture_output=True, text=True).stdout.split(",")
W, H = int(info[0]), int(info[1])
lv = subprocess.Popen(["ffmpeg", "-v", "error", "-i", ent, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
lm = subprocess.Popen(["ffmpeg", "-v", "error", "-i", masc, "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
gv = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30",
                       "-i", "-", "-c:v", "ffv1", saida], stdin=subprocess.PIPE)
pequeno = (W // 4, H // 4)  # desfoca em 1/4 da resolução: mais rápido e igual a olho nu
while True:
    bv, bm = lv.stdout.read(W * H * 3), lm.stdout.read(W * H)
    if len(bv) < W * H * 3 or len(bm) < W * H: break
    f = np.frombuffer(bv, np.uint8).reshape(H, W, 3).astype(np.float32)
    m = np.frombuffer(bm, np.uint8).reshape(H, W).astype(np.float32) / 255
    fundo_peso = cv2.resize(1 - cv2.dilate(m, np.ones((15, 15), np.uint8)), pequeno, interpolation=cv2.INTER_AREA)
    fp = cv2.resize(f, pequeno, interpolation=cv2.INTER_AREA) * fundo_peso[..., None]
    s = sigma / 4
    num = cv2.GaussianBlur(fp, (0, 0), s); den = cv2.GaussianBlur(fundo_peso, (0, 0), s)[..., None]
    borrado = cv2.resize(num / np.maximum(den, 1e-3), (W, H), interpolation=cv2.INTER_LINEAR)
    a = cv2.GaussianBlur(m, (0, 0), 1.2)[..., None]
    if so_fundo:
        # buraco grande (a pessoa inteira): "pinta" com a parede ao redor numa versão bem pequena e amplia
        pq = (W // 16, H // 16)
        fpq = cv2.resize(f, pq, interpolation=cv2.INTER_AREA).clip(0, 255).astype(np.uint8)
        mpq = (cv2.resize(cv2.dilate(m, np.ones((41, 41), np.uint8)), pq, interpolation=cv2.INTER_AREA) > 0.05).astype(np.uint8)
        pint = cv2.inpaint(fpq, mpq, 6, cv2.INPAINT_TELEA)
        out = cv2.GaussianBlur(cv2.resize(pint.astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC), (0, 0), 25)
    else:
        out = f * a + borrado * (1 - a)
    gv.stdin.write(out.clip(0, 255).astype(np.uint8).tobytes())
gv.stdin.close(); gv.wait()
print("fundo desfocado:", saida)
