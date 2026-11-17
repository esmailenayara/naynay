#!/usr/bin/env bash
# Monta as telas divididas no estilo da referência (vídeo vertical 1080x1920).
# Uso:
#   ./tela-dividida.sh cartao     <fala> <imagem>            <saida.mp4> [segundos]
#   ./tela-dividida.sh comparacao <fala> <imagem1> <imagem2> <saida.mp4> [segundos]
#   ./tela-dividida.sh metade     <fala> <imagem>            <saida.mp4> [segundos]
# <fala> = vídeo dela falando (ou foto, para teste). As imagens podem ser fotos ou vídeos.
# DESCER=380 ./tela-dividida.sh cartao ...  -> desce a pessoa 380 px (use quando o rosto ficar atrás do cartão).
# Aplica o filtro de cor (filtro-cor.txt) em tudo. Legendas entram depois, com o .ass.
set -euo pipefail
cd "$(dirname "$0")"
M="${MASCARAS:-/tmp/mascaras-instagram}"; [ -f "$M/descer.png" ] || python3 -I mascaras.py "$M" >/dev/null
modo=$1; shift
COR=$(tr -d '\n' < filtro-cor.txt)

entrada() {  # foto vira vídeo; vídeo entra como está
  case "${1,,}" in *.jpg|*.jpeg|*.png|*.webp) echo "-loop 1 -framerate 30 -t $DUR -i $1";; *) echo "-i $1";; esac
}
# Fundo com a fala. DESCER=px empurra a pessoa para baixo (o rosto não fica atrás do cartão);
# o espaço de cima é preenchido com a própria imagem desfocada e escurecida.
fundo_fala() {
  local d=${DESCER:-0}
  if [ "$d" = 0 ]; then echo "[0:v]$(cobrir 1080 1920),$COR[fundo];"
  else echo "[0:v]$(cobrir 1080 1920),$COR,split[p][q];movie=$M/descer.png,format=gray[dm];[p]format=rgba[pr];[pr][dm]alphamerge[pm];[q]gblur=sigma=40,eq=brightness=-0.08[borrado];[borrado][pm]overlay=0:$d[fundo];"; fi
}
cobrir() { echo "scale=$1:$2:force_original_aspect_ratio=increase,crop=$1:$2,setsar=1"; }

case $modo in
  cartao)
    fala=$1 img=$2 saida=$3 DUR=${4:-5}
    ins="$(entrada "$fala") $(entrada "$img") -loop 1 -i $M/cartao.png -loop 1 -i $M/cartao-sombra.png"
    fc="$(fundo_fala)
        [1:v]$(cobrir 860 640),$COR,format=rgba[c];[2:v]format=gray[m];[c][m]alphamerge[card];
        [fundo][3:v]overlay=70:150[f1];[f1][card]overlay=110:190:shortest=1" ;;
  comparacao)
    fala=$1 a=$2 b=$3 saida=$4 DUR=${5:-5}
    ins="$(entrada "$fala") $(entrada "$a") $(entrada "$b") -loop 1 -i $M/comparacao.png -loop 1 -i $M/comparacao-sombra.png"
    fc="$(fundo_fala)
        [1:v]$(cobrir 500 620)[a];[2:v]$(cobrir 500 620)[b];[a][b]hstack,$COR,format=rgba[c];
        [3:v]format=gray[m];[c][m]alphamerge[card];
        [fundo][4:v]overlay=0:150[f1];[f1][card]overlay=40:190:shortest=1" ;;
  metade)
    fala=$1 img=$2 saida=$3 DUR=${4:-5}
    ins="$(entrada "$fala") $(entrada "$img") -loop 1 -i $M/metade.png"
    fc="color=black:s=1080x1920:r=30[preto];
        [0:v]$(cobrir 1080 1260),$COR[baixo];
        [1:v]$(cobrir 1080 860),$COR,format=rgba[c];[2:v]format=gray[m];[c][m]alphamerge[cima];
        [preto][baixo]overlay=0:660:shortest=1[f1];[f1][cima]overlay=0:0" ;;
  *) echo "modo desconhecido: $modo"; exit 1 ;;
esac

# -t limita a duração quando tudo é foto; com vídeo, o vídeo da fala manda.
ffmpeg -v error -y $ins -filter_complex "$(echo "$fc" | tr -d '\n' | tr -s ' ')" \
  -map 0:a? -t "$DUR" -r 30 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k "$saida"
echo "pronto: $saida"
