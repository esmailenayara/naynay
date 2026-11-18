"""NÃO USAR — a Dra. REPROVOU este visual em 18/11/2026 ("ficou horrível"). Guardado só como histórico.
A cor oficial é a do cor.py (1ª edição do teste 1). Ver ESTILO.md, seção 2.

COR NO ESTILO DOS PRINTS DE REFERÊNCIA — o padrão de cor dos vídeos dela.

Ela escolheu (17/11/2026) a cor de dois prints dos Reels da referência (@kauanysaales):
pele rosada e neutra (nada de amarelo/laranja), paredes num bege suave, sombras escuras e limpas
(quase pretas, sem marrom), contraste "de cinema". Os valores medidos estão em cor-alvo-referencia.json (medido no vídeo de referência inteiro por medir_referencia.py).

Como o cenário dela é diferente do da referência (parede branca, roupa clara), NÃO dá para copiar
o histograma. Este script mede no ORIGINAL de cada vídeo três regiões: PELE, NEUTROS (paredes/branco)
e SOMBRAS, e monta uma LUT 3D que leva cada região até o tom da referência:
  1) curva de luminância (sombra, pele, neutro e branco no brilho certo);
  2) cor de cada faixa de tom (sombra / pele / neutro) com o equilíbrio R-G-B da referência;
  3) saturação da pele igual à da referência.
Depois renderiza de verdade pelo ffmpeg, mede de novo e corrige (4 rodadas). No fim diz OK ou NÃO BATEU.

Uso:  python3 -I cor_estilo.py <bruto.mov> <pasta_saida> [--recorte "crop=...,scale=1080:1920"] [--inicio S --fim S]
      -> <pasta_saida>/estilo.cube e <pasta_saida>/cor-filtro.txt
Na edição:  ...,<recorte>,$(cat <pasta_saida>/cor-filtro.txt)
"""
import argparse, json, os, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import cor  # reaproveita a leitura de quadros e os efeitos de textura

ALVO = json.load(open(os.path.join(AQUI, "cor-alvo-referencia.json")))
WR, WG, WB = 0.2126, 0.7152, 0.0722


def mascaras(px):
    a = px.astype(np.float32)
    L = WR * a[..., 0] + WG * a[..., 1] + WB * a[..., 2]
    Y = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    Cr = (a[..., 0] - Y) * 0.713 + 128; Cb = (a[..., 2] - Y) * 0.564 + 128
    mx, mn = a.max(-1), a.min(-1); sat = (mx - mn) / np.maximum(mx, 1)
    return {"pele": (Cr > 135) & (Cr < 175) & (Cb > 85) & (Cb < 130) & (Y > 80),
            "neutro": (sat < 0.15) & (L > np.percentile(L, 60)),
            "sombra": L < np.percentile(L, 8)}


def medir(px, m):
    a = px.astype(np.float32)
    r = {k: a[v].mean(0) for k, v in m.items()}
    mx, mn = a.max(-1), a.min(-1); sat = (mx - mn) / np.maximum(mx, 1)
    r["satpele"] = float(sat[m["pele"]].mean())
    return r


lum = lambda c: WR * c[0] + WG * c[1] + WB * c[2]


def lut3d(par, n=33):
    """Curva de brilho para tudo + correção de cor SELETIVA:
    a cor da pele só mexe no que tem tom de pele, a dos neutros só no que é quase sem cor
    (parede, branco) e a das sombras só no que é escuro. Assim a camisa azul e a parede não
    ficam rosadas/lilás por tabela."""
    g = np.linspace(0, 255, n, dtype=np.float32)
    B, G, R = np.meshgrid(g, g, g, indexing="ij")          # ordem do .cube: R varia mais rápido
    Y = WR * R + WG * G + WB * B
    Yo = np.interp(Y, par["xin"], par["yout"])
    k = Yo / np.maximum(Y, 1)
    cr, cg, cb = (R - Y) * k, (G - Y) * k, (B - Y) * k
    # pesos de cada região (calculados na cor de ENTRADA)
    mx = np.maximum(np.maximum(R, G), B); mn = np.minimum(np.minimum(R, G), B)
    sat = (mx - mn) / np.maximum(mx, 1)
    ang = np.arctan2(B - Y, R - Y); d = np.angle(np.exp(1j * (ang - par["ang_pele"])))
    w_pele = np.exp(-(d / 0.6) ** 2) * np.clip((sat - 0.04) / 0.08, 0, 1) * np.clip((Y - 40) / 40, 0, 1)
    w_neutro = np.exp(-(sat / 0.10) ** 2) * np.clip((Y - par["xin"][2]) / 40, 0, 1)
    w_sombra = np.clip((par["xin"][1] * 1.8 - Y) / max(par["xin"][1], 1), 0, 1)
    tot = np.maximum(1, w_pele + w_neutro + w_sombra)
    w_pele, w_neutro, w_sombra = w_pele / tot, w_neutro / tot, w_sombra / tot
    s_pele = 1 + (par["sat"] - 1) * w_pele                  # saturação só na pele
    cr, cg, cb = cr * s_pele, cg * s_pele, cb * s_pele
    dR = w_sombra * par["dR"][0] + w_pele * par["dR"][1] + w_neutro * par["dR"][2]
    dB = w_sombra * par["dB"][0] + w_pele * par["dB"][1] + w_neutro * par["dB"][2]
    dG = -(WR * dR + WB * dB) / WG                           # desloca a cor sem mudar o brilho
    out = np.stack([Yo + cr + dR, Yo + cg + dG, Yo + cb + dB], -1)
    return np.clip(out, 0, 255) / 255


def gravar_cube(par, caminho):
    t = lut3d(par).reshape(-1, 3)
    with open(caminho, "w") as f:
        f.write('TITLE "estilo prints"\nLUT_3D_SIZE 33\n')
        for v in t: f.write(f"{v[0]:.5f} {v[1]:.5f} {v[2]:.5f}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("saida")
    ap.add_argument("--recorte", default=cor.RECORTE_PADRAO); ap.add_argument("--inicio", type=float); ap.add_argument("--fim", type=float)
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)
    cube = os.path.join(os.path.abspath(a.saida), "estilo.cube")
    q = lambda filtro: cor.quadros(a.video, f"{a.recorte},{filtro}", 20, a.inicio, a.fim)
    base = q(cor.EFEITOS)
    m = mascaras(base)                                       # regiões fixas (mesmos quadros em todas as medições)
    src = medir(base, m)
    al = {k: np.array(ALVO[k], np.float32) for k in ("pele", "neutro", "sombra")}
    xin = [0, lum(src["sombra"]), lum(src["pele"]), lum(src["neutro"]), 255]
    yout = [0, lum(al["sombra"]), lum(al["pele"]), lum(al["neutro"]), ALVO["branco"]]
    for i in range(1, 5):  # garante crescente
        xin[i] = max(xin[i], xin[i - 1] + 4); yout[i] = max(yout[i], yout[i - 1] + 2)
    sp = src["pele"]; yp = lum(sp)
    par = {"xin": xin, "yout": yout, "sat": 1.0, "dR": [0, 0, 0], "dB": [0, 0, 0],
           "ang_pele": float(np.arctan2(sp[2] - yp, sp[0] - yp))}
    filtro = f"{cor.EFEITOS},lut3d=file='{cube}':interp=tetrahedral,format=yuv420p"
    for rodada in range(6):
        gravar_cube(par, cube)
        real = medir(q(filtro), m)
        for j, reg in enumerate(("sombra", "pele", "neutro")):
            t, r = al[reg], real[reg]
            par["yout"][j + 1] += 0.8 * (lum(t) - lum(r))
            # cor = diferença para a luminância (R-Y, B-Y); corrige o que falta
            par["dR"][j] += 0.8 * ((t[0] - lum(t)) - (r[0] - lum(r)))
            par["dB"][j] += 0.8 * ((t[2] - lum(t)) - (r[2] - lum(r)))
        par["sat"] = float(np.clip(par["sat"] * (ALVO["satpele"] / max(real["satpele"], 1e-3)) ** 0.7, 0.5, 1.8))
        for i in range(1, 5): par["yout"][i] = max(par["yout"][i], par["yout"][i - 1] + 2)
    gravar_cube(par, cube)
    real = medir(q(filtro), m)
    # grão de filme sutil (só no brilho, muda a cada quadro), aplicado depois de medir
    open(os.path.join(a.saida, "cor-filtro.txt"), "w").write(f"{filtro},noise=c0s={ALVO.get('grao', 6)}:c0f=t")
    json.dump({k: (float(v) if np.isscalar(v) else [float(x) for x in v]) for k, v in par.items()},
              open(os.path.join(a.saida, "parametros.json"), "w"))
    fmt = lambda c: "(" + ",".join(f"{x:.0f}" for x in c) + ")"
    erro = 0
    for reg in ("pele", "neutro", "sombra"):
        e = np.abs(real[reg] - al[reg]).max(); erro = max(erro, e)
        print(f"{reg:7s} antes {fmt(src[reg])}  depois {fmt(real[reg])}  alvo {fmt(al[reg])}  (dif. máx {e:.0f})")
    print(f"sat. pele antes {src['satpele']:.3f}  depois {real['satpele']:.3f}  alvo {ALVO['satpele']:.3f}")
    ok = erro <= 8 and abs(real["satpele"] - ALVO["satpele"]) < 0.03
    print("->", "OK" if ok else "NÃO BATEU: investigue antes de editar", "| filtro em", os.path.join(a.saida, "cor-filtro.txt"))


if __name__ == "__main__":
    main()
