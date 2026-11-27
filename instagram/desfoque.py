"""Desfoca o fundo atrás da pessoa ("modo retrato"), como nos vídeos da referência.

Uso:  python3 -I desfoque.py <video.mkv> <mascara.mkv> <saida.mkv> [intensidade=22] [so-fundo] [cordao=X0:X1]
      "so-fundo" = grava só o fundo desfocado, SEM a pessoa (usado para preencher o espaço quando ela
      desce na tela por causa de um cartão de foto).
      "cordao=X0:X1" = há um cordão/corrente fino pendurado atrás dela entre as colunas X0 e X1 (pixels).
      Quando ele encosta na cabeça, o recorte acha que é o contorno do cabelo e o deixa nítido: vira uma
      "linha" ao lado do rosto. Com essa opção ele é achado pelas contas (variação vertical) e desfocado.
      Usado no vídeo do preenchimento (cordao=270:390).
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
extras = sys.argv[5:]
so_fundo = "so-fundo" in extras
cordao = next((tuple(int(v) for v in e.split("=")[1].split(":")) for e in extras if e.startswith("cordao=")), None)


def tirar_cordao(f, m):
    """Zera a máscara onde o cordão aparece E a borda do recorte está em cima dele (orelha/cabelo ficam)."""
    x0, x1 = cordao
    g = cv2.cvtColor(f.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32)
    hp = cv2.blur(np.abs(g - cv2.blur(g, (1, 9))), (5, 1))       # contas = muita variação na vertical
    xc = x0 + int(np.argmax(hp[H * 23 // 100:H * 55 // 100, x0:x1].mean(0)))
    vis = cv2.blur(hp[:, xc - 3:xc + 4].mean(1, keepdims=True), (1, 31)).ravel()
    viz = cv2.blur(np.concatenate([hp[:, xc - 30:xc - 12], hp[:, xc + 12:xc + 30]], 1).mean(1, keepdims=True), (1, 31)).ravel()
    lin = (vis > 6) & (vis > 2.2 * viz)
    # e as contas se repetem a cada 5-10 px na vertical (sobrancelha, brinco e borda do rosto, não)
    sg = g[:, xc - 2:xc + 3].mean(1); sg = sg - cv2.blur(sg[:, None], (1, 15)).ravel()
    jan = lambda v: cv2.blur(v[:, None].astype(np.float32), (1, 33)).ravel()
    e = jan(sg * sg) + 1e-3
    per = np.max([jan(np.concatenate([sg[:-L] * sg[L:], np.zeros(L)])) / e for L in range(5, 11)], 0)
    lin &= per > 0.45
    # fecha buracos curtos (fios de cabelo passando na frente de um pedaço do cordão)
    lin = cv2.morphologyEx(lin.astype(np.uint8)[:, None], cv2.MORPH_CLOSE, np.ones((61, 1), np.uint8)).ravel().astype(bool)
    faixa = m[:, max(xc - 60, 0):xc + 13] > 0.5
    borda = np.where(faixa.any(1), faixa.argmax(1) + max(xc - 60, 0), 10**6)   # 1ª coluna dela em cada linha
    lin &= borda >= xc - 12
    lin = cv2.dilate(lin.astype(np.uint8)[:, None], np.ones((9, 1), np.uint8)).ravel().astype(bool)
    # apaga SÓ a faixa estreita do cordão e só nos pixels sem cor de pele (contas cinza/branco/preto):
    # apagar tudo à esquerda cortava a testa dela quando o rosto encostava no cordão
    a0, a1 = xc - 8, xc + 6
    hsv = cv2.cvtColor(f[:, a0:a1].astype(np.uint8), cv2.COLOR_RGB2HSV)
    conta = ((hsv[..., 1] < 80) | (hsv[..., 2] < 60)).astype(np.float32)
    conta = cv2.dilate(conta, np.ones((3, 3), np.uint8))
    m[:, a0:a1] *= 1 - conta * lin[:, None]
    return m
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
    if cordao: m = tirar_cordao(f, m.copy())
    # fica só com a PESSOA (a maior mancha da máscara): faixas da parede, quadros etc. que o recorte
    # confundiu com ela eram deixados nítidos e viravam uma "linha" ao lado do rosto
    pq = cv2.resize((m > 0.5).astype(np.uint8), (W // 4, H // 4), interpolation=cv2.INTER_NEAREST)
    n, rot, est, _ = cv2.connectedComponentsWithStats(pq, 8)
    if n > 2:
        maior = 1 + int(np.argmax(est[1:, cv2.CC_STAT_AREA]))
        manter = cv2.dilate((rot == maior).astype(np.uint8), np.ones((5, 5), np.uint8))
        m = m * cv2.resize(manter, (W, H), interpolation=cv2.INTER_NEAREST).astype(np.float32)
    # tira também coisas FINAS em pé grudadas no contorno dela (ex.: cordão/corrente pendurado ao lado da
    # cabeça): a "abertura" horizontal some com tudo que tiver menos de ~24 px de largura
    fino = (m > 0.5).astype(np.uint8)
    largo = cv2.dilate(cv2.morphologyEx(fino, cv2.MORPH_OPEN, np.ones((1, 25), np.uint8)), np.ones((5, 5), np.uint8))
    m = m * cv2.GaussianBlur(np.maximum(largo, 1 - fino).astype(np.float32), (0, 0), 1.5)
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
