"""Gera as máscaras (PNG) usadas nas telas divididas. Uso: python3 -I mascaras.py <pasta_saida>"""
import sys, os
from PIL import Image, ImageDraw, ImageFilter
out = sys.argv[1]; os.makedirs(out, exist_ok=True)

def cartao(w, h, r, nome):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w-1, h-1], r, fill=255)
    m.save(f"{out}/{nome}.png")

def sombra(w, h, r, borda, nome):
    W, H = w+2*borda, h+2*borda
    m = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(m).rounded_rectangle([borda, borda+12, borda+w, borda+h+12], r, fill=(0, 0, 0, 120))
    m.filter(ImageFilter.GaussianBlur(borda/2.5)).save(f"{out}/{nome}.png")

def emenda(w, h, faixa, nome):
    """Branco em cima, esmaecendo para transparente nos últimos `faixa` px (emenda suave)."""
    m = Image.new("L", (w, h), 255); d = ImageDraw.Draw(m)
    for i in range(faixa):
        y = h - faixa + i; d.line([(0, y), (w, y)], fill=int(255*(1-i/faixa)))
    m.save(f"{out}/{nome}.png")

cartao(860, 640, 36, "cartao");        sombra(860, 640, 36, 40, "cartao-sombra")
cartao(1000, 620, 30, "comparacao");   sombra(1000, 620, 30, 40, "comparacao-sombra")
emenda(1080, 860, 90, "metade")
# fundo "descido": transparente no topo, esmaecendo para opaco em 140 px (sem linha dura)
m = Image.new("L", (1080, 1920), 255); d = ImageDraw.Draw(m)
for i in range(140): d.line([(0, i), (1080, i)], fill=int(255*i/140))
m.save(f"{out}/descer.png")
print("ok")
