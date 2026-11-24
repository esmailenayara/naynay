"""Coloca as fotos de antes e depois nos vídeos NE Face (depois da edição bruta aprovada).

Cada foto JÁ É uma montagem antes × depois: entra INTEIRA num cartão de cantos arredondados no alto
(encaixada, sem cortar), com zoom suave (no antes, no depois ou no centro). Enquanto a foto está na
tela, ela desce 250 px (a cabeça fica inteira abaixo do cartão: a foto aparece sem nada na frente) e
a legenda vai para logo abaixo do cartão (como na referência). Textos opcionais no cartão:
"Resultado imediato" (canto de baixo) e um título (nome do caso / "Dia 1 → 3 anos depois").

Uso:  python3 -I fotos.py <nome> [...]      (precisa de edicao/<nome>/com-fundo.mkv, mascara.mkv, cortado.json)
"""
import json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
sys.path.insert(0, AQUI)
import montar_lote as ml

F = "../fotos/"
DESCER, TOPO, LMAX, AMAX = 250, 150, 1000, 640
Y_LEG_CARTAO = TOPO + AMAX + 90          # legenda logo abaixo do cartão
RI = "Resultado imediato"
# (começa na frase, termina na frase [None = fim], foto, foco: antes/depois/None, texto de baixo, título)
PLANO = {
 "carla": [("quantos ml", "a carla chegou", "carla-2-lado-esq.jpg", None, None, None),   # desde a pergunta (pedido dela)
           ("a carla chegou", "e eu utilizei", "carla-1-frente.jpg", "antes", None, None),
           ("e eu utilizei", "aqui eu preenchi", "carla-2-lado-esq.jpg", None, None, None),
           ("aqui eu preenchi", "e hoje", "carla-3-lado-dir.jpg", "depois", None, None),
           ("e hoje", "e voce", "carla-1-frente.jpg", "depois", None, None)],
 "juliana": [("e foi isso", "e com o", "juliana-perfil.jpg", "antes", None, None),
             ("e com o", "reparem", "juliana-perfil.jpg", None, RI, None),
             ("reparem", "e voce", "juliana-perfil.jpg", "depois", RI, None)],
 "monique": [("3 anos", "ao longo", "monique-dia1-hoje.jpg", None, None, "Dia 1 → 3 anos depois"),
             ("ao longo", "entao veio", "monique-dia1-hoje.jpg", None, None, None),
             ("entao veio", "e essa ultima", "monique-ultima-etapa.jpg", None, None, None),
             ("e essa ultima", "a harmonizacao", "monique-ultima-etapa.jpg", "depois", None, None)],
 "gabriela": [("ela nao queria", "e quem", "gabriela-mae.jpg", "antes", None, None),
              ("e com o meu", "e o resultado", "gabriela-mae.jpg", None, RI, None),
              ("e o resultado", "as vezes", "gabriela-mae.jpg", "depois", RI, None)],
 "renata": [("repara", "a esquerda", "renata.jpg", None, None, None),
            ("a esquerda", "e agora", "renata.jpg", "antes", None, None),
            ("e agora", "e isso tudo", "renata.jpg", "depois", None, None),
            ("e isso tudo", None, "renata.jpg", None, None, None)],
 "julie": [("ela ja nao", "o olhar transmitia", "julie-1-frente.jpg", None, None, None),
           ("o olhar transmitia", "e com o", "julie-1-frente.jpg", "antes", None, None),
           ("e com o", "isso de todos", "julie-2-lado-dir.jpg", "depois", None, None),
           ("isso de todos", "e hoje", "julie-3-lado-esq.jpg", "depois", None, None),
           ("e hoje", None, "julie-1-frente.jpg", None, None, None)],
 # montagem: os 6 casos em sequência durante "Rostos mais leves ... mais seguras"
 "final": [("rostos mais leves", "todos esses", ["carla-1-frente.jpg", "juliana-perfil.jpg", "monique-ultima-etapa.jpg",
            "gabriela-mae.jpg", "renata.jpg", "julie-1-frente.jpg"], None,
            [None, RI, None, RI, None, None], [None] * 6)],   # sem nomes nas fotos (pedido dela)
}


def achar(ws, frase, depois_de=0.0):
    alvo = frase.split()
    for i in range(len(ws) - len(alvo) + 1):
        if ws[i]["ini"] >= depois_de - 0.01 and [ml.norm(w["texto"]) for w in ws[i:i + len(alvo)]] == alvo:
            return ws[i]["ini"]
    raise SystemExit(f"frase não encontrada: {frase!r}")


def janelas(nome, ws, total):
    out, t = [], 0.0
    for ini, fim, foto, foco, baixo, titulo in PLANO[nome]:
        a = achar(ws, ini, t); b = achar(ws, fim, a) if fim else total
        if isinstance(foto, list):   # montagem: divide o trecho igualmente
            n = len(foto); d = (b - a) / n
            for k in range(n):
                out.append((a + k * d, a + (k + 1) * d, foto[k], foco, baixo[k], titulo[k]))
        else:
            out.append((a, b, foto, foco, baixo, titulo))
        t = a
    return out


def cartao(foto, pasta, k):
    im = Image.open(F + foto).convert("RGB")
    esc = min(LMAX / im.width, AMAX / im.height); w, h = int(im.width * esc) // 2 * 2, int(im.height * esc) // 2 * 2
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=255)
    m.save(f"{pasta}/mcart{k}.png")
    b = 40; s = Image.new("RGBA", (w + 2 * b, h + 2 * b), (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle([b, b + 12, b + w, b + h + 12], 30, fill=(0, 0, 0, 130))
    s.filter(ImageFilter.GaussianBlur(16)).save(f"{pasta}/scart{k}.png")
    return w, h


def aplicar(nome):
    pasta = f"edicao/{nome}"
    com = f"{pasta}/com-fundo.mkv"
    total = float(ml.saida("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", com))
    ws = ml.palavras_cortado(pasta)
    J = janelas(nome, ws, total)
    so = f"{pasta}/so-fundo.mkv"   # parede desfocada SEM a pessoa (preenche o espaço quando ela desce)
    if not os.path.exists(so):
        ml.sh("python3", "-I", f"{ml.IG}/desfoque.py", f"{pasta}/corte.mkv", f"{pasta}/mascara.mkv", so, "30", "so-fundo")
    ins = ["-i", com, "-i", f"{pasta}/mascara.mkv", "-i", so]
    fc = ("[0:v]split=2[base][vp];[2:v]scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,eq=brightness=-0.06[fill];"
          "[1:v]format=gray[m];[vp]format=rgba[vpr];[vpr][m]alphamerge[pes];"
          f"[fill][pes]overlay=0:{DESCER}[cena0];")
    ult, idx = "cena0", 3
    for k, (a, b, foto, foco, _, _) in enumerate(J):
        w, h = cartao(foto, pasta, k)
        x = (1080 - w) // 2
        fx = {"antes": 0.25, "depois": 0.75}.get(foco, 0.5)
        dur = max(b - a, 0.1)
        ins += ["-loop", "1", "-framerate", "30", "-i", F + foto, "-loop", "1", "-i", f"{pasta}/mcart{k}.png",
                "-loop", "1", "-i", f"{pasta}/scart{k}.png"]
        z = f"(1+0.07*clip((t-{a:.3f})/{dur:.3f}\\,0\\,1))"   # zoom suave ao longo da janela
        fc += (f"[{idx}:v]scale={w}*{z}:{h}*{z}:eval=frame,crop={w}:{h}:'(iw-{w})*{fx}':'(ih-{h})*0.5',"
               f"format=rgba[f{k}];[{idx+1}:v]format=gray[mk{k}];[f{k}][mk{k}]alphamerge[c{k}];"
               f"[{ult}][{idx+2}:v]overlay={x-40}:{TOPO-40}:enable='between(t,{a:.3f},{b:.3f})'[s{k}];"
               f"[s{k}][c{k}]overlay={x}:{TOPO}:enable='between(t,{a:.3f},{b:.3f})'[cena{k+1}];")
        ult, idx = f"cena{k+1}", idx + 3
    janela = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b, *_ in J)
    fc += f"[base][{ult}]overlay=0:0:enable='{janela}',format=yuv420p[v]"
    sh = ml.sh
    sh("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-map", "0:a", "-t", f"{total:.3f}",
       "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-c:a", "copy", f"{pasta}/com-fotos.mkv")
    # legendas: abaixo do cartão quando tem foto; textos do cartão
    leg = ml.legendas(nome, [("ed", w) for w in ws], lambda f, t: t, total)
    linhas = []
    for l in leg.split("\n"):
        if l.startswith("Dialogue"):
            p = l.split(",", 9); t0 = sum(float(x) * m for x, m in zip(p[1].split(":"), (3600, 60, 1)))
            if any(a - 0.01 <= t0 < b for a, b, *_ in J):
                l = re.sub(r"\\pos\(540,\d+\)", f"\\\\pos(540,{Y_LEG_CARTAO})", l)
                if p[3] in ("Destaque", "DestaqueBrilho") and "\\fs" not in l:
                    l = l.replace("\\blur", "\\fs150\\blur", 1)
        linhas.append(l)
    ts = lambda x: f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
    for k, (a, b, foto, _, baixo, titulo) in enumerate(J):
        w, h = Image.open(f"{pasta}/mcart{k}.png").size; x = (1080 - w) // 2
        if baixo:
            linhas.append(f"Dialogue: 3,{ts(a)},{ts(b)},Fala,,0,0,0,,{{\\an3\\pos({x + w - 24},{TOPO + h - 20})\\fs38\\shad2\\fad(150,0)}}{baixo}")
        if titulo:
            linhas.append(f"Dialogue: 3,{ts(a)},{ts(b)},Fala,,0,0,0,,{{\\an7\\pos({x + 24},{TOPO + 18})\\fs40\\shad2\\fad(150,0)}}{titulo}")
    open(f"{pasta}/legendas-fotos.ass", "w").write("\n".join(linhas) + "\n")
    print(nome, "janelas:", [(round(a, 1), round(b, 1), f) for a, b, f, *_ in J], flush=True)
    return total


def exportar(nome, total):
    pasta = f"edicao/{nome}"; IG = ml.IG
    af = (f"[0:a]highpass=f=80,afftdn=nf=-25,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,"
          f"loudnorm=I=-15:TP=-2:LRA=7,aresample=48000,apad=whole_dur={total:.2f},asplit[voz][chave];"
          f"[1:a]aresample=48000,atrim=0:{total:.2f},volume=0.22,afade=t=in:d=1,afade=t=out:st={total-1.5:.2f}:d=1.5[mus];"
          f"[mus][chave]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[musb];"
          f"[voz][musb]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=8,aresample=48000[a]")
    ml.sh("ffmpeg", "-v", "error", "-y", "-i", f"{pasta}/com-fotos.mkv", "-i", os.path.join(AQUI, "../../musica/gymnopedie.mp3"),
          "-filter_complex", f"[0:v]noise=c0s=2:c0f=t,ass={pasta}/legendas-fotos.ass:fontsdir={IG}/fontes[v];{af}",
          "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p", "-r", "30",
          "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
          "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", f"{pasta}/{nome}-com-fotos.mp4")
    print(f"pronto: {pasta}/{nome}-com-fotos.mp4", flush=True)


if __name__ == "__main__":
    for nome in sys.argv[1:]:
        exportar(nome, aplicar(nome))
