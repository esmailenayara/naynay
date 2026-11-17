"""COR POR REFERÊNCIA — deixa qualquer vídeo dela com a cor da 1ª edição aprovada (teste 1).

Não é um filtro fixo: para cada vídeo novo, lê o ORIGINAL, mede luz, sombra e cor de cada canal
(R, G, B) e calcula a curva que leva aquele vídeo até a cor aprovada (casamento de histograma por
canal + ajuste fino de saturação). Assim, vídeo mais claro, mais escuro, mais frio ou mais quente
chega sempre no mesmo resultado.

Uso:
  python3 -I cor.py ajustar <bruto.mov> <pasta_saida> [--recorte "crop=...,scale=1080:1920"] [--inicio S --fim S]
      -> grava <pasta_saida>/cor.cube e <pasta_saida>/cor-filtro.txt (cadeia pronta para o ffmpeg)
         e imprime a comparação medida (antes / alvo / depois).
  python3 -I cor.py alvo <bruto_aprovado.mov> [--recorte ...]
      -> (só para recriar o alvo) mede a cor aprovada e grava cor-alvo.json ao lado deste script.

Na edição, a cor entra assim (sempre nesta ordem, depois do enquadramento):
  ...,<recorte>,$(cat <pasta_saida>/cor-filtro.txt)
Na exportação final, mantenha a marcação HDR do iPhone (ver ESTILO.md, seção 2).
Faça um "ajustar" por arquivo bruto (cada gravação tem a sua luz). Se a luz mudar muito dentro
do mesmo arquivo, rode por trecho com --inicio/--fim.
"""
import argparse, json, os, subprocess, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(AQUI, "cor-alvo.json")
RECORTE_PADRAO = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
# Textura do visual aprovado (vinheta + brilho suave nas luzes). É espacial, não muda a "cor";
# entra antes da curva, e a curva é calculada já contando com ela.
EFEITOS = ("format=gbrp,vignette=angle=0.45,split[_b][_g];[_g]curves=master='0/0 0.55/0.05 1/1',"
           "gblur=sigma=28[_g2];[_b][_g2]blend=all_mode=screen:all_opacity=0.22,format=rgb24")
# Receita exata da 1ª edição aprovada (usada só para medir o alvo).
APROVADA = ("format=gbrp,curves=master='0/0 0.15/0.06 0.45/0.33 0.75/0.66 0.92/0.88 1/1',"
            "colorbalance=rh=0.02:bh=-0.03,huesaturation=saturation=0.35:colors=r+y+m,"
            "huesaturation=saturation=0.15,format=rgb24," + open(os.path.join(AQUI, "filtro-cor.txt")).read().replace("\n", ""))
Q = np.linspace(0.5, 99.5, 100)


def quadros(video, filtro, n=24, ini=None, fim=None):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                               capture_output=True, text=True).stdout)
    a, b = ini or 0.5, min(fim or dur, dur) - 0.3
    out = []
    for t in np.linspace(a, b, n):
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
                            "-filter_complex", f"{filtro},scale=270:480,format=rgb24", "-f", "rawvideo", "-"],
                           capture_output=True)
        if len(r.stdout) == 270 * 480 * 3:
            out.append(np.frombuffer(r.stdout, np.uint8).reshape(480, 270, 3))
    if not out: sys.exit("não consegui ler quadros do vídeo")
    return np.stack(out).astype(np.float32)


def saturacao(px):  # média de (max-min)/max, igual à medida usada no estudo da referência
    mx, mn = px.max(-1), px.min(-1)
    return float(np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0).mean())


def medir(px):
    return {"q": [np.percentile(px[..., c], Q).tolist() for c in range(3)], "sat": saturacao(px / 255)}


def resumo(px):
    L = 0.2126 * px[..., 0] + 0.7152 * px[..., 1] + 0.0722 * px[..., 2]
    p = np.percentile(L / 255, [2, 50, 98])
    return f"preto {p[0]:.3f}  meio {p[1]:.3f}  branco {p[2]:.3f}  sat {saturacao(px / 255):.3f}  RGB médio {np.round(px.reshape(-1,3).mean(0)).astype(int).tolist()}"


def curvas(src, alvo):
    xs = np.arange(256, dtype=np.float32)
    lut = []
    for c in range(3):
        s = np.maximum.accumulate(np.array(src["q"][c]) + np.arange(100) * 1e-4)  # estritamente crescente
        t = np.maximum.accumulate(np.array(alvo["q"][c]))
        y = np.interp(xs, s, t)
        # pontas: segue a inclinação em vez de achatar (evita "estourar" ou "chapar")
        lo, hi = xs < s[0], xs > s[-1]
        k0 = (t[3] - t[0]) / max(s[3] - s[0], 1e-3); k1 = (t[-1] - t[-4]) / max(s[-1] - s[-4], 1e-3)
        y[lo] = t[0] - (s[0] - xs[lo]) * k0; y[hi] = t[-1] + (xs[hi] - s[-1]) * k1
        y = np.convolve(np.pad(y, 4, mode="edge"), np.ones(9) / 9, mode="valid")  # suaviza (sem degraus)
        lut.append(np.clip(y, 0, 255))
    return np.stack(lut, -1)


def aplicar(px, lut, sat=1.0):
    o = np.stack([np.interp(px[..., c], np.arange(256), lut[:, c]) for c in range(3)], -1)
    if sat != 1.0:  # mesmo cálculo do eq=saturation do ffmpeg (escala o croma)
        Y = 0.299 * o[..., 0] + 0.587 * o[..., 1] + 0.114 * o[..., 2]
        o = Y[..., None] + (o - Y[..., None]) * sat
    return np.clip(o, 0, 255)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("modo", choices=["alvo", "ajustar"]); ap.add_argument("video"); ap.add_argument("saida", nargs="?")
    ap.add_argument("--recorte", default=RECORTE_PADRAO); ap.add_argument("--inicio", type=float); ap.add_argument("--fim", type=float)
    a = ap.parse_args()
    if a.modo == "alvo":
        px = quadros(a.video, f"{a.recorte},{APROVADA}", 32, a.inicio, a.fim)
        json.dump(medir(px), open(ALVO, "w")); print("alvo gravado:", ALVO, "\n ", resumo(px)); return
    alvo = json.load(open(ALVO))
    os.makedirs(a.saida, exist_ok=True)
    px = quadros(a.video, f"{a.recorte},{EFEITOS}", 24, a.inicio, a.fim)
    lut = curvas(medir(px), alvo)
    # ajuste fino de saturação: procura o fator que iguala a saturação do alvo
    sat = 1.0
    for _ in range(12):
        s = saturacao(aplicar(px, lut, sat) / 255); sat *= (alvo["sat"] / max(s, 1e-4)) ** 0.8
    # calibrado no teste 1: o eq do ffmpeg (YUV de faixa limitada) satura ~5% a mais que a conta acima
    sat = float(np.clip(sat * 0.95, 0.6, 1.6))
    cube = os.path.join(os.path.abspath(a.saida), "cor.cube")
    with open(cube, "w") as f:
        f.write("TITLE \"cor aprovada\"\nLUT_1D_SIZE 256\n")
        for v in lut / 255: f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
    filtro = f"{EFEITOS},lut1d=file='{cube}',format=yuv420p,eq=saturation={sat:.3f}"
    open(os.path.join(a.saida, "cor-filtro.txt"), "w").write(filtro)
    depois = aplicar(px, lut, sat)
    alvo_px = None
    print("ANTES :", resumo(px))
    print("DEPOIS:", resumo(depois))
    L = lambda q: 0.2126 * np.array(q[0]) + 0.7152 * np.array(q[1]) + 0.0722 * np.array(q[2])
    la = L(alvo["q"]) / 255
    print(f"ALVO  : preto {la[1]:.3f}  meio {la[49]:.3f}  branco {la[97]:.3f}  sat {alvo['sat']:.3f}")
    print("filtro gravado em", os.path.join(a.saida, "cor-filtro.txt"))


if __name__ == "__main__":
    main()
