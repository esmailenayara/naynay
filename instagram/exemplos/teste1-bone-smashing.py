"""Edição do vídeo-teste 1 (bone smashing). Rodar: python3 -I montar.py"""
import json, os, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
IG = "/home/user/naynay/instagram"
os.chdir(AQUI)
def sh(*a): subprocess.run(list(a), check=True)

COR = open(f"{IG}/filtro-cor.txt").read().replace("\n", "")
PRE = ("format=gbrp,curves=master='0/0 0.15/0.06 0.45/0.33 0.75/0.66 0.92/0.88 1/1',"
       "colorbalance=rh=0.02:bh=-0.03,huesaturation=saturation=0.35:colors=r+y+m,huesaturation=saturation=0.15,format=rgb24")
DUR_TOTAL = 84.775

# --- 1. Trechos de fala (complemento dos silêncios), com folga ---
sil = [(0, .880), (5.221, 5.674), (8.612, 8.956), (15.869, 16.472), (19.620, 20.048), (23.160, 23.702),
       (35.791, 36.086), (37.210, 37.806), (39.648, 40.193), (43.070, 43.564), (45.586, 46.431),
       (50.455, 50.841), (51.768, 52.412), (59.030, 60.223), (66.935, 67.256), (76.317, 76.568), (78.866, 79.904)]
fala, t = [], 0.0
for a, b in sil:
    if a > t: fala.append([t, a])
    t = b
fala.append([t, DUR_TOTAL])
seg = [[max(0, a - .07), min(DUR_TOTAL, b + .10)] for a, b in fala]

# zoom alternado por trecho (esconde os cortes); trechos 5-6 = cartão (sem zoom)
ZOOM = [1.0, 1.12, 1.0, 1.12, 1.0, 1.0, 1.0, 1.12, 1.0, 1.12, 1.0, 1.12, 1.0, 1.0, 1.12, 1.0, 1.12]
assert len(ZOOM) == len(seg), (len(ZOOM), len(seg))

def novo(tv):  # tempo do bruto -> tempo do vídeo editado
    acc = 0.0
    for a, b in seg:
        if tv < a: return acc
        if tv <= b: return acc + tv - a
        acc += b - a
    return acc

os.makedirs("trechos", exist_ok=True)
lista = []
for i, ((a, b), z) in enumerate(zip(seg, ZOOM)):
    w, h = 1024 / z, 1820 / z
    x = min(max(520 - w / 2, 0), 1080 - w); y = min(max(560 - h * 0.30, 0), 1820 - h)
    base = f"crop={w:.0f}:{h:.0f}:{x:.0f}:{y:.0f},scale=1080:1920:flags=lanczos,setsar=1"
    if i > 0 and i % 2 == 1:   # aproximação: empurra 7% para dentro em 0,45 s (suave no fim)
        p = "min(t/0.45\\,1)"
        k = f"(1+0.07*{p}*(2-{p}))"
        base += (f",scale=w='trunc(1080*{k}/2)*2':h='trunc(1920*{k}/2)*2':eval=frame:flags=bicubic,"
                 f"crop=1080:1920:'(iw-1080)/2':'(ih-1920)*0.3'")
    vf = f"{base},{PRE},{COR}"
    if i > 0 and i % 2 == 0:   # brilho: clarão suave que se apaga em 0,3 s
        vf += (",split[a][b];[b]gblur=sigma=30[g];"
               "[a][g]blend=c0_expr='min(255\\,A+B*0.4*max(0\\,1-T/0.3))':c1_expr=A:c2_expr=A")
    out = f"trechos/{i:02d}.mp4"
    lista.append(f"file '{out}'")
    if os.path.exists(out): continue
    sh("ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", "bruto.bin", "-filter_complex", vf,
       "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-c:a", "pcm_s16le", "-ar", "48000", out)
open("lista.txt", "w").write("\n".join(lista))
os.path.exists("corte.mkv") or sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "lista.txt", "-c", "copy", "corte.mkv")

# --- 2. Fundo desfocado (efeito "modo retrato"): pessoa nítida, consultório em desfoque ---
if not os.path.exists("mascara.mkv"):
    sh("python3", "-I", f"{IG}/recorte.py", "corte.mkv", "mascara.mkv")
sh("python3", "-I", f"{IG}/desfoque.py", "corte.mkv", "mascara.mkv", "fundo.mkv", "10")
sh("ffmpeg", "-v", "error", "-y", "-i", "fundo.mkv", "-i", "corte.mkv", "-map", "0:v", "-map", "1:a", "-c", "copy", "com-cartao.mkv")
C0 = C1 = -1
# --- 3. Legendas ---
P = json.load(open("palavras.json"))
ini = lambda i: novo(P[i]["ini"]); fim = lambda i: novo(P[i]["fim"])
def ts(x):
    x = max(0, x); h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"
cab = open(f"{IG}/legendas-modelo.ass").read().split("[Events]")[0]
HALO = r"\3c&H1A2430&\3a&H70&\bord4\blur8"
ev = ["[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
def dlg(a, b, estilo, txt, camada=0):
    if estilo in ("Fala", "Apoio") and txt.startswith("{"): txt = "{" + HALO + txt[1:]
    ev.append(f"Dialogue: {camada},{ts(a)},{ts(b)},{estilo},,0,0,0,,{txt}")

# (palavra inicial, palavra final, texto, tipo)  F=fala  D=destaque (com apoio)  L=lista
C = [
 (0,1,"Tem influenciador","F"),(2,2,"ensinando","F"),(3,5,"o seu filho","F"),(6,7,"a bater","F"),(8,10,"no próprio rosto","F"),
 (11,13,"com o|martelo","D"),
 (14,15,"Os pesquisadores","F"),(16,17,"da USP","F"),(18,18,"mediram","F"),(19,21,"o tamanho disso.","F"),
 (22,22,"Sim,","F"),(23,25,"você ouviu direito.","F"),(26,30,"o nome é|bone smashing","D"),
 (31,32,"bater com","F"),(33,34,"o martelo","F"),(35,37,"ou objeto duro","F"),(38,39,"para esculpir","F"),(40,41,"a mandíbula.","F"),
 (42,44,"Mas o que","F"),(45,46,"os profissionais","F"),(47,49,"da saúde descrevem","F"),(50,52,"é outra coisa.","F"),
 (53,53,"Fratura,","F"),(54,56,"lesão de nervo","F"),(57,60,"e problema na mordida.","F"),
 (61,63,"O estudo saiu","F"),(64,66,"agora em outubro.","F"),
 (67,69,"Em três meses","F"),(70,73,"foram 2,5 milhões","F"),(74,75,"de interações.","F"),(76,76,"Estimados","F"),
 (77,78,"32 milhões","F"),(79,80,"de alcance.","F"),(81,83,"E 98%","F"),(84,85,"desse conteúdo","F"),(86,88,"vem de homens.","F"),
 (89,91,"Mas por que","F"),(92,93,"alguém acreditaria","F"),(94,94,"nisso?","F"),
 (95,97,"Porque usam","F"),(98,100,"uma ideia real,","F"),(101,103,"de forma|torta","D"),
 (104,106,"A de que","F"),(107,110,"o osso se adapta","F"),(111,112,"à carga.","F"),
 (113,116,"Só que se adaptar","F"),(117,118,"não é","F"),(119,120,"levar pancada.","F"),
 (121,123,"E o inchaço","F"),(124,126,"que aparece depois","F"),(127,129,"é|inflamação","D"),
 (130,131,"O estudo","F"),(132,133,"mediu alcance,","F"),(134,136,"não quantas pessoas","F"),(137,138,"se machucaram.","F"),
 (139,141,"Mas mesmo assim,","F"),(142,144,"isso já muda","F"),(145,146,"duas coisas","F"),(147,148,"para você.","F"),
 (149,149,"Primeiro,","F"),(150,152,"o contorno facial","F"),(153,155,"não se modela","F"),(156,157,"em casa.","F"),
 (158,160,"Dor ou inchaço","F"),(161,164,"depois de uma pancada","F"),(165,169,"é caso de|pronto-socorro","D"),
 (170,171,"Não pode","F"),(172,173,"esperar passar.","F"),
 (174,174,"Segundo,","F"),(175,177,"quem tem sobrinho,","F"),(178,180,"filho, irmão","F"),(181,182,"precisa saber","F"),(183,185,"que isso existe.","F"),
 (186,187,"O conteúdo","F"),(188,190,"que mais engaja","F"),(191,193,"é o|tutorial","D"),
 (194,196,"Aquele que ensina","F"),(197,198,"como fazer.","F"),
 (199,200,"Rosto bonito","F"),(201,203,"não se constrói","F"),(204,205,"em|casa","D"),
 (206,208,"Manda esse vídeo","F"),(209,213,"para todo pai e mãe","F"),(214,215,"de adolescente.","F"),
]
for n, (a, b, txt, tipo) in enumerate(C):
    t0 = ini(a)
    t1 = ini(C[n + 1][0]) if n + 1 < len(C) else novo(DUR_TOTAL)
    if tipo == "D":
        apoio, palavra = txt.split("|")
        fs = "" if len(palavra) <= 9 else rf"\fs{int(200 * 9 / len(palavra))}"
        dlg(t0, t1, "Apoio", rf"{{\pos(300,1060)\fad(120,0)}}{apoio}", 2)
        dlg(t0, t1, "DestaqueBrilho", rf"{{\pos(540,1170){fs}\blur18\fad(250,0)}}{palavra}", 0)
        dlg(t0, t1, "Destaque", rf"{{\pos(540,1170){fs}\blur10\fad(200,0)\t(0,280,\blur0.6)}}{palavra}", 1)
    elif tipo == "L":
        itens = txt.split("|"); comecos = [ini(53), ini(54), ini(57)]
        for k, (it, tk) in enumerate(zip(itens, comecos)):
            dlg(tk, t1, "Lista", rf"{{\pos(540,{1060 + k * 115})\fad(300,0)}}{it}")
    else:
        y = 1180
        dlg(t0, t1, "Fala", rf"{{\pos(540,{y})\fad(60,0)}}{txt}")

# flash branco nas viradas de assunto
for tf in (ini(149), ini(174)):  # viradas de assunto
    dlg(tf - 0.05, tf + 0.25, "Risco", r"{\pos(0,0)\1c&HFFFFFF&\bord0\shad0\fad(0,220)\p1}m 0 0 l 1080 0 1080 1920 0 1920", 5)
open("legendas.ass", "w").write(cab + "\n".join(ev) + "\n")

# --- 4. Áudio: voz tratada + música por baixo, abaixando quando ela fala ---
TOTAL = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "com-cartao.mkv"],
                             capture_output=True, text=True).stdout)
musica = "../musica/gymnopedie.mp3"
af = (f"[0:a]highpass=f=80,afftdn=nf=-25,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,"
      f"loudnorm=I=-15:TP=-2:LRA=7,asplit[voz][chave];"
      f"[1:a]atrim=0:{TOTAL:.2f},volume=0.22,afade=t=in:d=1,afade=t=out:st={TOTAL-1.5:.2f}:d=1.5[mus];"
      f"[mus][chave]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[musb];"
      f"[voz][musb]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=8[a]")

# --- 5. Final ---
sh("ffmpeg", "-v", "error", "-y", "-i", "com-cartao.mkv", "-i", musica, "-filter_complex",
   f"[0:v]ass=legendas.ass:fontsdir={IG}/fontes[v];{af}", "-map", "[v]", "-map", "[a]",
   "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
   "-color_primaries", "bt2020", "-color_trc", "arib-std-b67", "-color_range", "tv",
   "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "final3.mp4")
print("pronto: final3.mp4", round(TOTAL, 1), "s")
