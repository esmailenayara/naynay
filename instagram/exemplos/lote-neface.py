"""NE Face — edição bruta dos 6 casos (cortes, cor aprovada, fundo desfocado, transições, legendas, música).
Uso: python3 -I montar_lote.py [nome ...]   (sem nome = todos)"""
import json, os, re, shutil, subprocess, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
IG = "/home/user/naynay/instagram"
def sh(*a): subprocess.run(list(a), check=True)
def saida(*a): return subprocess.run(list(a), capture_output=True, text=True).stdout
REC = "scale=1080:1920:flags=lanczos"
# COR "FOTO PROFISSIONAL" (opção 2, aprovada por ela em 23/11/2026):
# 1) conversão CORRETA do HDR (HLG) do iPhone para vídeo normal; 2) contraste leve, toque quente;
# 3) cantos levemente escurecidos e brilho suave nas luzes; 4) nitidez. O grão fino entra no fim.
TOM = ("zscale=t=linear:npl=200,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
       "zscale=t=bt709:m=bt709:r=tv,format=rgb24")
ACAB = ("curves=master='0/0 0.25/0.22 0.5/0.5 0.75/0.79 1/1',colorbalance=rm=0.02:bm=-0.02,"
        "format=gbrp,vignette=angle=0.45,split[_b][_g];[_g]curves=master='0/0 0.55/0.05 1/1',gblur=sigma=28[_g2];"
        "[_b][_g2]blend=all_mode=screen:all_opacity=0.15,format=rgb24,unsharp=5:5:0.6:5:5:0,"
        "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p")
BRILHO = "0.88"   # cenário claro (parede e roupa brancas): 1,0 ficou "estourado" para ela
Y_FALA = 1430     # nestes vídeos ela aparece mais baixa: legenda na altura do colo, nunca no rosto

# arquivo, janelas a manter (None = tudo). Janelas tiram as tentativas repetidas.
VIDEOS = {
 "carla":    [("v32", None), ("v31", None), ("v30", None), ("v29", None)],
 "juliana":  [("v20", None), ("v19", None), ("v18", None), ("v17", None), ("v16", [(5.4, 99)]),
              ("v15", [(4.2, 7.35), (28.0, 99)]), ("v14", [(13.0, 99)])],
 "monique":  [("v28", None), ("v27", None), ("v26", [(14.1, 99)]), ("v25", [(28.4, 99)]),
              ("v24", [(8.2, 99)]), ("v23", [(23.4, 99)]), ("v22", None), ("v21", [(0, 18.95)])],
 "gabriela": [("v13", None), ("v12", [(20.9, 99)]), ("v11", [(13.2, 99)]), ("v10", None), ("v09", None), ("v08", None)],
 "renata":   [("v07", None), ("v06", [(16.05, 99)]), ("v05", None), ("v04", [(6.5, 99)])],
 "julie":    [("v03", None), ("v02", [(31.1, 99)]), ("v01", [(24.3, 99)])],
 "final":    [("f5", [(8.1, 99)]), ("f4", None), ("f2", [(8.6, 99)]), ("f1", [(0, 9.5), (23.5, 99)])],
}
# palavras de destaque (entram sozinhas, depois da frase)
DESTAQUE = {
 "carla": ["3 ml", "ne face", "firme", "lugar certo"],
 "juliana": ["proprio perfil", "equilibrio", "ne face", "proprio perfil"],
 "monique": ["3 anos", "acompanhamento", "casamento", "ne face", "consulta"],
 "gabriela": ["tirar foto", "se ver", "ne face", "se gostar"],
 "renata": ["peso", "leve", "ne face", "pesou"],
 "julie": ["oculos escuros", "ne face", "leveza", "acessorio"],
 "final": ["mudanca", "seguras", "ne face", "17 ml", "consulta", "para voce"],
}
# correções do texto da legenda: (arquivo, sequência como foi transcrita) -> sequência certa (mesmo nº de palavras)
CORR = [
 ("v20", "o perfil ao lado", "O perfil é-o lado"), ("v19", "parece", "aparece"), ("v12", "dizer", "dizia"),
 ("v07", "a esquerda", "À esquerda"), ("v07", "anotar", "notar"), ("v28", "a esquerda", "À esquerda"),
 ("v28", "a direita", "à direita"), ("v23", "vosto", "rosto"), ("v04", "agente", "agende"),
 ("v16", "e como o", "E com o"), ("v02", "e como o", "E com o"), ("v14", "olhe o seu", "eu-olho o seu"),
 ("v29", "so no lugar", "só do lugar"), ("v06", "e agora", "E agora,"),
]
SEM_ACENTO = lambda s: "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")
norm = lambda w: re.sub(r"[^\w]", "", SEM_ACENTO(w))


def falas(f, janelas):
    dur = float(saida("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"brutos/{f}.bin"))
    log = subprocess.run(["ffmpeg", "-i", f"audio/{f}.wav", "-af", "silencedetect=noise=-30dB:d=0.3", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    ss = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
    se = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
    reg, t = [], 0.0
    for a, b in zip(ss, se + [dur] * (len(ss) - len(se))):
        if a - t > 0.15: reg.append([t, a])
        t = b
    if dur - t > 0.15: reg.append([t, dur])
    P = json.load(open(f"audio/{f}.json"))
    reg = [r for r in reg if any(w["ini"] < r[1] and w["fim"] > r[0] for w in P)]
    seg = [[max(0, a - 0.08), min(dur, b + 0.10)] for a, b in reg]
    if janelas:
        out = []
        for a, b in seg:
            for ja, jb in janelas:
                x, y = max(a, ja), min(b, jb)
                if y - x > 0.12: out.append([x, y])
        seg = out
    return seg


def palavras(f, seg):
    P = json.load(open(f"audio/{f}.json"))
    ws = [dict(w) for w in P if any(a <= (w["ini"] + w["fim"]) / 2 <= b for a, b in seg)]
    for arq, de, para in CORR:
        if arq != f: continue
        de_ = de.split(); para_ = para.split()
        for i in range(len(ws) - len(de_) + 1):
            if [norm(w["texto"]) for w in ws[i:i + len(de_)]] == [norm(x) for x in de_]:
                for k, x in enumerate(para_):
                    pont = re.findall(r"[,.?!]+$", ws[i + k]["texto"])
                    ws[i + k]["texto"] = x.replace("-", " ") + (pont[0] if pont and not re.search(r"[,.?!]$", x) else "")
                break
    for w in ws:
        w["texto"] = w["texto"].replace("nfase", "N.E. Face").replace("NFase", "N.E. Face").replace("...", ".")
    return ws


def palavras_cortado(pasta):
    js = f"{pasta}/cortado.json"
    if not os.path.exists(js):
        sh("ffmpeg", "-v", "error", "-y", "-i", f"{pasta}/corte.mkv", "-vn", "-ac", "1", "-ar", "16000", f"{pasta}/cortado.wav")
        with open(js, "w") as o:
            subprocess.run(["python3", "-I", f"{IG}/transcrever.py", f"{pasta}/cortado.wav", DICA], stdout=o, check=True)
    ws = json.load(open(js))
    for de, para in CORR_GERAL:
        de_ = de.split(); para_ = para.split()
        for i in range(len(ws) - len(de_) + 1):
            if [norm(w["texto"]) for w in ws[i:i + len(de_)]] == [norm(x) for x in de_]:
                for k, x in enumerate(para_):
                    pont = re.findall(r"[,.?!]+$", ws[i + k]["texto"])
                    ws[i + k]["texto"] = x.replace("-", " ") + (pont[0] if pont and not re.search(r"[,.?!]$", x) else "")
    for w in ws:
        w["texto"] = re.sub(r"(?i)n\s?face|nfase|ne fase", "N.E. Face", w["texto"]).replace("...", ".")
    for i in range(len(ws) - 1):   # "NE" + "Face" -> "N.E." + "Face"
        if norm(ws[i]["texto"]) == "ne" and norm(ws[i + 1]["texto"]).startswith("face"):
            ws[i]["texto"] = "N.E."
    return [w for w in ws if w["texto"].strip("_,.?! ")]


DICA = "Método NE Face: um olhar global, um resultado natural, a medida certa para você. Carla, Juliana, Monique, Gabriela, Renata, Julie. 3 ml, 17 ml."
CORR_GERAL = [(de, para) for _, de, para in CORR] + [
 ("rostas mais", "Rostos mais"), ("rostes mais", "Rostos mais"), ("perfizem em", "Perfis em"),
 ("gostado que vem", "gostaram do-que veem"), ("do que vem", "do que veem"), ("medida e certa", "medida é-certa certa"),
 ("contornes mais", "contornos mais"), ("perfez em", "Perfis em"), ("quantas ml", "Quantos ml"),
 ("com o o metodo", "com o _ método"), ("de foto e de lado", "de foto _ de lado"), ("escondiam que ela", "escondiam o-que ela"),
 ("tirar a foto", "tirar _ foto"),
]


LIGACAO = {"de", "a", "o", "e", "que", "do", "da", "no", "na", "em", "com", "os", "as", "um", "uma", "se", "eu", "te", "me", "para", "pra", "mais"}


def legendas(nome, itens, novo, total):
    """itens: lista de (arquivo, palavra). 1–3 palavras por legenda; destaque sozinho depois da frase."""
    alvo = [d.split() for d in DESTAQUE.get(nome, [])]
    cab = open(f"{IG}/legendas-modelo.ass").read().split("[Events]")[0]
    HALO = r"\3c&H1A2430&\3a&H70&\bord4\blur8"
    blocos, atual, i = [], [], 0
    def fecha():
        nonlocal atual
        if atual: blocos.append(("F", atual)); atual = []
    while i < len(itens):
        if alvo and [norm(itens[j][1]["texto"]) for j in range(i, min(i + len(alvo[0]), len(itens)))] == alvo[0]:
            fecha(); blocos.append(("D", itens[i:i + len(alvo[0])])); i += len(alvo[0]); alvo.pop(0); continue
        atual.append(itens[i])
        txt = itens[i][1]["texto"]
        prox = norm(itens[i + 1][1]["texto"]) if i + 1 < len(itens) else ""
        # não quebra antes de "ml" nem depois de palavrinha de ligação (de, a, o, e, que...)
        preso = prox in ("ml",) or txt == "N.E." or norm(txt) in LIGACAO or re.fullmatch(r"\d+", norm(txt) or "x")
        if ((re.search(r"[,.?!]$", txt) and txt != "N.E.") or (len(atual) >= 3 and not preso) or len(atual) >= 4
                or (i + 1 < len(itens) and itens[i + 1][0] != itens[i][0])):
            fecha()
        i += 1
    fecha()
    def ts(x): x = max(0, x); return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
    ev = ["[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for k, (tipo, ws) in enumerate(blocos):
        t0 = novo(ws[0][0], ws[0][1]["ini"])
        t1 = novo(blocos[k + 1][1][0][0], blocos[k + 1][1][0][1]["ini"]) if k + 1 < len(blocos) else total
        if t1 - t0 < 0.05: continue
        txt = " ".join(w["texto"] for _, w in ws)
        if tipo == "D":
            pal = re.sub(r"[,.?!]+$", "", txt); fs = "" if len(pal) <= 9 else rf"\fs{int(220 * 9 / len(pal))}"
            ev.append(f"Dialogue: 0,{ts(t0)},{ts(t1)},DestaqueBrilho,,0,0,0,,{{\\pos(540,{Y_FALA-10}){fs}\\blur18\\fad(250,0)}}{pal}")
            ev.append(f"Dialogue: 1,{ts(t0)},{ts(t1)},Destaque,,0,0,0,,{{\\pos(540,{Y_FALA-10}){fs}\\blur10\\fad(200,0)\\t(0,280,\\blur0.6)}}{pal}")
        else:
            txt = txt[0].upper() + txt[1:] if k == 0 else txt
            ev.append(f"Dialogue: 0,{ts(t0)},{ts(t1)},Fala,,0,0,0,,{{{HALO}\\pos(540,{Y_FALA})\\fad(60,0)}}{txt}")
    return cab + "\n".join(ev) + "\n"


def montar(nome):
    pasta = f"edicao/{nome}"; os.makedirs(f"{pasta}/trechos", exist_ok=True)
    partes = VIDEOS[nome]
    # cor: mesma sessão de gravação -> um ajuste por vídeo, calculado no arquivo mais longo
    maior = max(partes, key=lambda p: os.path.getsize(f"brutos/{p[0]}.bin"))[0]
    cor = f"{TOM},{ACAB}"
    SEG = {f: falas(f, j) for f, j in partes}
    lista, gi = [], 0
    for f, _ in partes:
        for a, b in SEG[f]:
            z = 1.0 if gi % 2 == 0 else 1.12
            w, h = 1080 / z, 1920 / z
            x = min(max(540 - w / 2, 0), 1080 - w); y = min(max(940 - h * 0.45, 0), 1920 - h)
            base = f"{REC},crop={w:.0f}:{h:.0f}:{x:.0f}:{y:.0f},scale=1080:1920:flags=lanczos,setsar=1"
            if gi > 0 and gi % 2 == 1:
                p = "min(t/0.45\\,1)"; kz = f"(1+0.07*{p}*(2-{p}))"
                base += (f",scale=w='trunc(1080*{kz}/2)*2':h='trunc(1920*{kz}/2)*2':eval=frame:flags=bicubic,"
                         f"crop=1080:1920:'(iw-1080)/2':'(ih-1920)*0.45'")
            vf = f"{base},{cor}"
            if gi > 0 and gi % 2 == 0:
                vf += (",split[a][b];[b]gblur=sigma=30[g];"
                       "[a][g]blend=c0_expr='min(255\\,A+B*0.4*max(0\\,1-T/0.3))':c1_expr=A:c2_expr=A")
            out = f"{pasta}/trechos/{gi:02d}.mp4"; lista.append(f"file 'trechos/{gi:02d}.mp4'")
            if not os.path.exists(out):
                sh("ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", f"brutos/{f}.bin",
                   "-filter_complex", vf, "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                   "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1", out)
            gi += 1
    open(f"{pasta}/lista.txt", "w").write("\n".join(lista))
    corte = f"{pasta}/corte.mkv"
    os.path.exists(corte) or sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{pasta}/lista.txt", "-c", "copy", corte)

    def novo(f, tv):
        acc = 0.0
        for g, _ in partes:
            for a, b in SEG[g]:
                if g == f:
                    if tv < a: return acc
                    if tv <= b: return acc + tv - a
                acc += b - a
            if g == f: return acc
        return acc

    if ETAPA == "corte":
        print(nome + ": " + " ".join(w["texto"] for w in palavras_cortado(pasta)), flush=True); return
    com = f"{pasta}/com-fundo.mkv"
    if not os.path.exists(com):
        os.path.exists(f"{pasta}/mascara.mkv") or sh("python3", "-I", f"{IG}/recorte.py", corte, f"{pasta}/mascara.mkv")
        sh("python3", "-I", f"{IG}/desfoque.py", corte, f"{pasta}/mascara.mkv", f"{pasta}/fundo.mkv", "10")
        sh("ffmpeg", "-v", "error", "-y", "-i", f"{pasta}/fundo.mkv", "-i", corte, "-map", "0:v", "-map", "1:a", "-c", "copy", com)
        os.remove(f"{pasta}/fundo.mkv")
    total = float(saida("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", com))
    itens = [("ed", w) for w in palavras_cortado(pasta)]
    open(f"{pasta}/legendas.ass", "w").write(legendas(nome, itens, lambda f, t: t, total))
    musica = "../../musica/gymnopedie.mp3"
    af = (f"[0:a]highpass=f=80,afftdn=nf=-25,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,"
          f"loudnorm=I=-15:TP=-2:LRA=7,aresample=48000,apad=whole_dur={total:.2f},asplit[voz][chave];"
          f"[1:a]aresample=48000,atrim=0:{total:.2f},volume=0.22,afade=t=in:d=1,afade=t=out:st={total-1.5:.2f}:d=1.5[mus];"
          f"[mus][chave]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[musb];"
          f"[voz][musb]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=8,aresample=48000[a]")
    final = f"{pasta}/{nome}-bruto.mp4"
    sh("ffmpeg", "-v", "error", "-y", "-i", com, "-i", os.path.join(AQUI, "../../musica/gymnopedie.mp3"), "-filter_complex",
       f"[0:v]scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,noise=c0s=2:c0f=t,ass={pasta}/legendas.ass:fontsdir={IG}/fontes[v];{af}", "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p", "-r", "30",
       "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", final)
    shutil.rmtree(f"{pasta}/trechos", ignore_errors=True)
    print(f"pronto: {final} ({total:.1f} s)", flush=True)


ETAPA = "tudo"
if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] in ("--corte", "--tudo"): ETAPA = args.pop(0)[2:]
    for nome in (args or list(VIDEOS)):
        montar(nome)
