"""Mede o "padrão de filme" no vídeo de referência inteiro (gravação de tela dos Reels da @kauanysaales)
e grava o alvo de cor usado pelo cor_estilo.py (cor-alvo-referencia.json).

Uso:  python3 -I medir_referencia.py <gravacao_referencia.mp4> [--passo 2]

O que faz: tira um quadro a cada `passo` segundos, descarta as telas de grade do perfil (fundo branco
do app), recorta só a área do vídeo (sem barra de status, ícones da direita e legenda do post),
ignora o branco puro das legendas e mede, em cada quadro, três regiões:
PELE (tom de pele), NEUTROS (paredes/claros sem cor) e SOMBRAS (8% mais escuros).
Guarda a mediana de tudo (resistente a quadros fora do padrão) + preto/branco e saturação da pele.
"""
import argparse, json, os, subprocess
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
WR, WG, WB = 0.2126, 0.7152, 0.0722

ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--passo", type=float, default=2)
a = ap.parse_args()
W0, H0 = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                                  "-of", "csv=p=0", a.video], capture_output=True, text=True).stdout.strip().split(","))
# área útil (proporções da tela do iPhone gravada): sem status/topo, sem ícones da direita, sem rodapé do post
x0, x1, y0, y1 = 0, int(W0 * 0.86), int(H0 * 0.11), int(H0 * 0.80)
w, h = 270, int(270 * (y1 - y0) / (x1 - x0)) // 2 * 2
r = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf",
                    f"fps=1/{a.passo},crop={x1-x0}:{y1-y0}:{x0}:{y0},scale={w}:{h},format=rgb24", "-f", "rawvideo", "-"],
                   capture_output=True)
fr = np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w, 3).astype(np.float32)

res = {"pele": [], "neutro": [], "sombra": [], "satpele": [], "preto": [], "branco": [], "Lpele": []}
usados = 0
for f in fr:
    L = WR * f[..., 0] + WG * f[..., 1] + WB * f[..., 2]
    mx, mn = f.max(-1), f.min(-1); sat = (mx - mn) / np.maximum(mx, 1)
    if ((L > 235) & (sat < 0.06)).mean() > 0.20:   # tela de grade do perfil / fundo branco do app
        continue
    Y = 0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2]
    Cr = (f[..., 0] - Y) * 0.713 + 128; Cb = (f[..., 2] - Y) * 0.564 + 128
    texto = (mn > 245)                                   # legenda branca
    pele = (Cr > 135) & (Cr < 175) & (Cb > 85) & (Cb < 130) & (Y > 80) & ~texto
    neutro = (sat < 0.15) & (L > np.percentile(L, 60)) & ~texto
    sombra = L < np.percentile(L, 8)
    if pele.mean() < 0.05 or neutro.mean() < 0.02:
        continue
    usados += 1
    res["pele"].append(f[pele].mean(0)); res["neutro"].append(f[neutro].mean(0)); res["sombra"].append(f[sombra].mean(0))
    res["satpele"].append(sat[pele].mean()); res["Lpele"].append(L[pele].mean())
    res["preto"].append(np.percentile(L[~texto], 1)); res["branco"].append(np.percentile(L[~texto], 99))

med = {k: np.median(np.array(v), axis=0) for k, v in res.items()}
rel = lambda c: (c[0] / c[1], c[2] / c[1])
out = {
    "_origem": f"Medido no vídeo de referência inteiro ({usados} quadros úteis de {len(fr)}, 1 a cada {a.passo:g} s), mediana.",
    "ref_pele": [round(float(x)) for x in med["pele"]], "ref_neutro": [round(float(x)) for x in med["neutro"]],
    "ref_sombra": [round(float(x)) for x in med["sombra"]], "ref_satpele": round(float(med["satpele"]), 3),
    "ref_preto": round(float(med["preto"])), "ref_branco": round(float(med["branco"])),
}
print(json.dumps(out, ensure_ascii=False, indent=1))
print("proporções pele R/G, B/G:", np.round(rel(med["pele"]), 3), " neutro:", np.round(rel(med["neutro"]), 3),
      " sombra:", np.round(rel(med["sombra"]), 3))
json.dump(out, open(os.path.join(AQUI, "medidas-referencia.json"), "w"), ensure_ascii=False, indent=1)
