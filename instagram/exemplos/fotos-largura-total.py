"""Fotos de antes e depois no estilo que ela mostrou (prints da @dra.luiseferrao, 23/11/2026):
1) ela em tela cheia; 2) entra a foto ocupando TODA A LARGURA na parte de cima, com a parte de baixo
se fundindo suavemente no vídeo, e a CABEÇA DELA NA FRENTE da foto; 3) zoom suave na foto;
4) na saída, animação de zoom e volta para ela em tela cheia.

Uso: python3 -I fotos2.py <nome> [--exemplo INI FIM]
"""
import os, re, sys
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
sys.path.insert(0, AQUI)
import montar_lote as ml
from fotos import PLANO, janelas, F

AFOTO = 1150        # altura máxima da faixa da foto (px): desce até a altura da cabeça dela
FUSAO = 70          # emenda BEM FININHA no pé da foto (ela: a de 300 px invadia a foto)
DESCER = 60         # ela desce só um pouco: a cabeça entra NA FRENTE da parte de baixo da foto
SAIDA = 0.5         # duração da animação de zoom na volta para a tela cheia


def mascara_fusao(w, h, pasta, k):
    m = Image.new("L", (w, h), 255)
    for y in range(h - FUSAO, h):
        v = int(255 * (1 - (y - (h - FUSAO)) / FUSAO) ** 1.6)
        m.paste(v, (0, y, w, y + 1))
    m.save(f"{pasta}/mfus{k}.png")


def aplicar(nome, exemplo=None):
    pasta = f"edicao/{nome}"
    com = f"{pasta}/com-fundo.mkv"
    total = float(ml.saida("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", com))
    ws = ml.palavras_cortado(pasta)
    J = janelas(nome, ws, total)
    # volta com zoom: k = 1 + 0,10 nos primeiros 0,5 s depois de cada foto, diminuindo até 1
    volta = "+".join(f"between(t,{b:.3f},{b+SAIDA:.3f})*(1-(t-{b:.3f})/{SAIDA})" for _, b, *_ in J) or "0"
    kz = f"(1+0.10*({volta}))"
    ins = ["-i", com, "-i", f"{pasta}/mascara.mkv"]
    fc = (f"[0:v]split=3[b0][vs][vp];"
          f"[b0]scale=w='trunc(1080*{kz}/2)*2':h='trunc(1920*{kz}/2)*2':eval=frame,crop=1080:1920:'(iw-1080)/2':'(ih-1920)*0.4'[base];"
          f"color=black:s=1080x1920:r=30[preto];[preto][vs]overlay=0:{DESCER}:shortest=1[cena0];"
          f"[1:v]format=gray[m];[vp]format=rgba[vpr];[vpr][m]alphamerge[pes];")
    ult, idx = "cena0", 2
    for k, (a, b, foto, foco, _, _) in enumerate(J):
        im = Image.open(F + foto); h = min(AFOTO, int(1080 * im.height / im.width)) // 2 * 2
        mascara_fusao(1080, h, pasta, k)
        fx = {"antes": 0.25, "depois": 0.75}.get(foco, 0.5)
        dur = max(b - a, 0.1)
        z = f"(1+0.08*clip((t-{a:.3f})/{dur:.3f}\\,0\\,1))"
        ins += ["-loop", "1", "-framerate", "30", "-i", F + foto, "-loop", "1", "-i", f"{pasta}/mfus{k}.png"]
        en = f"between(t,{a:.3f},{b:.3f})"
        fc += (f"[{idx}:v]scale=w='trunc(1080*{z}/2)*2':h=-2:eval=frame:flags=lanczos,crop=1080:{h}:'(iw-1080)*{fx}':'(ih-{h})*0.45',"
               f"format=rgba,fade=t=in:st={a:.3f}:d=0.2:alpha=1[f{k}];[{idx+1}:v]format=gray[mf{k}];[f{k}][mf{k}]alphamerge[c{k}];"
               f"[{ult}][c{k}]overlay=0:0:enable='{en}'[cena{k+1}];")
        ult, idx = f"cena{k+1}", idx + 2
    fc += f"[{ult}][pes]overlay=0:{DESCER}:shortest=1[comfoto];"
    janela = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b, *_ in J)
    fc += f"[base][comfoto]overlay=0:0:enable='{janela}',format=yuv420p[v]"
    t_args = ["-ss", f"{exemplo[0]}", "-t", f"{exemplo[1]-exemplo[0]}"] if exemplo else ["-t", f"{total:.3f}"]
    saida_v = f"{pasta}/com-fotos{'-exemplo' if exemplo else ''}.mkv"
    ml.sh("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-map", "0:a", *t_args,
          "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-c:a", "copy", saida_v)
    # legendas (mesma altura; ela desceu só 150 px) + textos da foto
    leg = ml.legendas(nome, [("ed", w) for w in ws], lambda f, t: t, total).split("\n")
    ts = lambda x: f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
    for k, (a, b, foto, _, baixo, titulo) in enumerate(J):
        im = Image.open(F + foto); h = min(AFOTO, int(1080 * im.height / im.width))
        if baixo:
            leg.append(f"Dialogue: 3,{ts(a)},{ts(b)},Fala,,0,0,0,,{{\\an3\\pos(1040,{h - FUSAO + 40})\\fs40\\shad2\\fad(200,0)}}{baixo}")
        if titulo:
            leg.append(f"Dialogue: 3,{ts(a)},{ts(b)},Fala,,0,0,0,,{{\\an7\\pos(40,60)\\fs44\\shad2\\fad(200,0)}}{titulo}")
    arq = f"{pasta}/legendas-fotos.ass"; open(arq, "w").write("\n".join(leg) + "\n")
    return saida_v, arq, total


if __name__ == "__main__":
    nome = sys.argv[1]
    ex = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 and sys.argv[2] == "--exemplo" else None
    v, arq, total = aplicar(nome, ex)
    if ex:   # legenda deslocada para o recorte do exemplo
        out = f"edicao/{nome}/exemplo-fotos.mp4"
        ml.sh("ffmpeg", "-v", "error", "-y", "-i", v, "-filter_complex",
              f"[0:v]setpts=PTS+{ex[0]}/TB,noise=c0s=2:c0f=t,ass={arq}:fontsdir={ml.IG}/fontes,setpts=PTS-STARTPTS[v]",
              "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p",
              "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", out)
        print("exemplo:", out)
    else:
        import fotos
        fotos.exportar(nome, total)
