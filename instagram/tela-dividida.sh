#!/usr/bin/env bash
# Monta as telas divididas no estilo da referência (vídeo vertical 1080x1920).
# Uso:
#   ./tela-dividida.sh cartao     <fala> <imagem>            <saida.mp4> [segundos]
#   ./tela-dividida.sh comparacao <fala> <imagem1> <imagem2> <saida.mp4> [segundos]
#   ./tela-dividida.sh metade     <fala> <imagem>            <saida.mp4> [segundos]
# <fala> = vídeo dela falando (ou foto, para teste). As imagens podem ser fotos ou vídeos.
#
# Opções (variáveis antes do comando):
#   FRENTE=1  (padrão no cartão e na comparação) recorta a pessoa e põe a cabeça dela NA FRENTE
#             do cartão, como na referência. FRENTE=0 desliga.
#   DESCER=px desce a pessoa (ex.: DESCER=300). O espaço de cima vira fundo desfocado, sem emenda.
#   CARTAO_Y=px altura do topo do cartão (padrão 190).
# Regra: a imagem NUNCA corta a cabeça dela. Ou fica atrás da cabeça (FRENTE=1) ou inteira acima.
# Aplica o filtro de cor (filtro-cor.txt) em tudo. Legendas entram depois, com o .ass.
set -euo pipefail
cd "$(dirname "$0")"
M="${MASCARAS:-/tmp/mascaras-instagram}"; [ -f "$M/descer.png" ] || python3 -I mascaras.py "$M" >/dev/null
modo=$1; shift
COR=$(tr -d '\n' < filtro-cor.txt)
D=${DESCER:-0}; Y=${CARTAO_Y:-190}

entrada() {  # foto vira vídeo; vídeo entra como está
  case "${1,,}" in *.jpg|*.jpeg|*.png|*.webp) echo "-loop 1 -framerate 30 -t $DUR -i $1";; *) echo "-i $1";; esac
}
cobrir() { echo "scale=$1:$2:force_original_aspect_ratio=increase,crop=$1:$2,setsar=1"; }

# Fundo com a fala (entrada 0). Com DESCER, a pessoa desce e o topo vira a própria imagem desfocada.
fundo_fala() {
  if [ "$D" = 0 ]; then echo "[0:v]$(cobrir 1080 1920),$COR,split[fundo][fala];"
  else echo "[0:v]$(cobrir 1080 1920),$COR,split=3[p][q][fala];movie=$M/descer.png,format=gray[dm];[p]format=rgba[pr];[pr][dm]alphamerge[pm];[q]gblur=sigma=40,eq=brightness=-0.08[borrado];[borrado][pm]overlay=0:$D[fundo];"; fi
}
# Pessoa recortada por cima de tudo (entrada = máscara gerada pelo recorte.py)
pessoa() {  # $1 = rótulo do quadro de baixo, $2 = índice da entrada da máscara
  echo "[fala]format=rgba[fr];[$2:v]format=gray[pmask];[fr][pmask]alphamerge[pessoa];[$1][pessoa]overlay=0:$D"
}

case $modo in
  cartao)
    fala=$1 img=$2 saida=$3 DUR=${4:-5}; FR=${FRENTE:-1}
    ins="$(entrada "$fala") $(entrada "$img") -loop 1 -i $M/cartao.png -loop 1 -i $M/cartao-sombra.png"
    fc="$(fundo_fala)
        [1:v]$(cobrir 860 640),$COR,format=rgba[c];[2:v]format=gray[m];[c][m]alphamerge[card];
        [fundo][3:v]overlay=70:$((Y-40))[f1];[f1][card]overlay=110:$Y:shortest=1[f2]" ;;
  comparacao)
    fala=$1 a=$2 b=$3 saida=$4 DUR=${5:-5}; FR=${FRENTE:-1}
    ins="$(entrada "$fala") $(entrada "$a") $(entrada "$b") -loop 1 -i $M/comparacao.png -loop 1 -i $M/comparacao-sombra.png"
    fc="$(fundo_fala)
        [1:v]$(cobrir 500 620)[a];[2:v]$(cobrir 500 620)[b];[a][b]hstack,$COR,format=rgba[c];
        [3:v]format=gray[m];[c][m]alphamerge[card];
        [fundo][4:v]overlay=0:$((Y-40))[f1];[f1][card]overlay=40:$Y:shortest=1[f2]" ;;
  metade)
    fala=$1 img=$2 saida=$3 DUR=${4:-5}; FR=${FRENTE:-0}
    ins="$(entrada "$fala") $(entrada "$img") -loop 1 -i $M/metade.png"
    fc="color=black:s=1080x1920:r=30[preto];
        [0:v]$(cobrir 1080 1160),$COR[baixo];
        [1:v]$(cobrir 1080 860),$COR,format=rgba[c];[2:v]format=gray[m];[c][m]alphamerge[cima];
        [preto][baixo]overlay=0:760:shortest=1[f1];[f1][cima]overlay=0:0[f2]"
    [ "$FR" = 1 ] && { echo "FRENTE=1 não se aplica ao modo metade (a pessoa já fica abaixo da imagem)"; FR=0; } ;;
  *) echo "modo desconhecido: $modo"; exit 1 ;;
esac

if [ "$FR" = 1 ]; then
  masc=$(mktemp --suffix=.mkv)
  python3 -I recorte.py "$fala" "$masc" "$DUR" >/dev/null
  n=$(( $(grep -o -- '-i ' <<<"$ins" | wc -l) ))
  ins="$ins -i $masc"
  fc="$fc;$(pessoa f2 $n)"
else
  fc="${fc%\[f2\]}"
  [ "$modo" != metade ] && fc="$fc;[fala]nullsink"
fi

# -t limita a duração quando tudo é foto; com vídeo, o vídeo da fala manda.
ffmpeg -v error -y $ins -filter_complex "$(echo "$fc" | tr -d '\n' | tr -s ' ')" \
  -map 0:a? -t "$DUR" -r 30 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k "$saida"
[ "${masc:-}" ] && rm -f "$masc"
echo "pronto: $saida"
