"""IGUALA A COR de um vídeo a outro já aprovado, gravado no MESMO lugar (mesma luz e roupa).

Uso: python3 -I igualar_cor.py <bruto_novo> "<cadeia de cor do novo>" <video_aprovado_sem_legenda> <pasta_saida>
  <cadeia de cor do novo> = filtro aplicado ao bruto antes do ajuste (ex.: conversão HDR + acabamento),
  <video_aprovado_sem_legenda> = o corte já colorido do vídeo aprovado (corte.mkv, sem legenda e sem desfoque).
Grava <pasta_saida>/igualar.cube e <pasta_saida>/igualar-filtro.txt (pedaço a acrescentar no fim da cadeia).

Como funciona: casamento de histograma canal por canal (R, G, B) entre quadros dos dois vídeos e depois
refino com o resultado real (4 rodadas). Só faz sentido entre gravações do mesmo cenário: com cenário
diferente, o conteúdo muda o histograma (ver ESTILO.md, seção 2).
Criado em 26/11/2026: o vídeo do preenchimento saía vermelho/amarelado mesmo com a cor da perfiloplastia
aprovada, porque a luz daquela gravação estava diferente.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cor

bruto, cadeia, aprovado, pasta = sys.argv[1:5]
os.makedirs(pasta, exist_ok=True)
cube = os.path.join(os.path.abspath(pasta), "igualar.cube")
REC = "scale=1080:1920:flags=lanczos"
alvo = cor.medir(cor.quadros(aprovado, "null", 24))


def lut_filtro():
    return f",format=rgb24,lut1d=file='{cube}',scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"


def gravar(lut):
    with open(cube, "w") as f:
        f.write('TITLE "igualar"\nLUT_1D_SIZE 256\n')
        for v in np.clip(lut, 0, 255) / 255: f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")


base = cor.quadros(bruto, f"{REC},{cadeia}", 24)
lut = cor.curvas(cor.medir(base), alvo)
for rodada in range(4):
    gravar(lut)
    real = cor.quadros(bruto, f"{REC},{cadeia}{lut_filtro()}", 24)
    corr = cor.curvas(cor.medir(real), alvo)
    lut = np.stack([np.interp(lut[:, c], np.arange(256), corr[:, c]) for c in range(3)], -1)
gravar(lut)
real = cor.quadros(bruto, f"{REC},{cadeia}{lut_filtro()}", 24)
open(os.path.join(pasta, "igualar-filtro.txt"), "w").write(lut_filtro())
dif = np.abs(np.array(cor.medir(real)["q"]) - np.array(alvo["q"]))[:, 3:97].mean() / 255
print("ANTES :", cor.resumo(base)); print("DEPOIS:", cor.resumo(real))
print("ALVO  :", cor.resumo(cor.quadros(aprovado, "null", 24)))
print(f"diferença média para o vídeo aprovado: {dif*100:.1f}% ->", "OK" if dif < 0.015 else "NÃO BATEU")
