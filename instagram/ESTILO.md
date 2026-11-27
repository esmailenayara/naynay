# Estilo de edição dos vídeos do Instagram (Reels)

> **Para o Claude:** quando a Dra. Nayara Esmaile enviar vídeos para editar, siga este guia
> do começo ao fim, sem perguntar de novo o que já está decidido aqui. Ela não é programadora:
> fale em português simples e mostre o resultado (prints e o vídeo final) antes de considerar pronto.

## 0. Checklist de TODO vídeo (aprovado por ela no teste 1, 18/11/2026)

Todo vídeo que ela pedir para editar sai com **tudo isto**, sem perguntar de novo:

1. **Cor "foto profissional"** (seção 2): conversão correta do HDR do iPhone + acabamento da opção 2, exportado como vídeo normal.
2. **Fundo levemente desfocado** (`recorte.py` + `desfoque.py`, intensidade 10).
3. **Legendas só brancas, 2 estilos:** `Fala` (1 a 3 palavras, meio da tela, halo escuro suave) e
   `Destaque` (palavra forte grande com brilho). **Primeiro a frase, depois o destaque sozinho, no
   mesmo lugar.** Nenhuma legenda em cima de outra. Sem título, sem cursiva, sem outras cores.
4. **Pausas cortadas** e **transição em toda emenda**, alternando aproximação e brilho suave, mais o
   enquadramento alternado 100%/112%. Flash branco nas viradas de assunto.
5. **Áudio:** voz tratada, música instrumental baixinha que abaixa quando ela fala, **até o último
   segundo** (confira a duração). Crédito da música para a legenda do post.
6. **Legenda que ela grava embaixo:** lida para corrigir a transcrição e **removida** do final.
7. **Tela dividida** quando ela mandar imagens (seção 5b), com a cabeça dela nunca cortada.
8. **Exportação:** 1080×1920, 30 fps, **vídeo normal SDR bt709** (nunca marcado como HDR), crf 15, áudio AAC.
9. Entregar o vídeo + o texto do crédito da música. O que ela aprovar ou reprovar, **anotar aqui**.

Modelos prontos para adaptar: `instagram/exemplos/teste1-bone-smashing.py` (um vídeo) e
`instagram/exemplos/lote-neface.py` (vários vídeos gravados em partes: agrupa as partes, escolhe a
última tentativa, corta, legenda e exporta todos).

### Preparação de uma sessão nova (uma vez por sessão)

```bash
pip install faster-whisper onnxruntime opencv-python-headless fonttools
```

- `ffmpeg` já vem no ambiente. O modelo de recorte (Robust Video Matting) baixa sozinho do GitHub na
  1ª vez, e o de transcrição (Whisper "small") baixa sozinho do Hugging Face.
- Música: `incompetech.com` funciona daqui. Pixabay bloqueia o acesso automático.
- Os vídeos brutos são grandes: guarde no scratchpad, **nunca no git**.

## 1. De onde veio o estilo

Referência escolhida por ela: os Reels de **@kauanysaales** (gravação de tela de 4 min, analisada
em 17/11/2026). O objetivo é ficar com **o mesmo acabamento profissional**, não copiar o conteúdo.
O que define o estilo:

- Imagem **macia, quente e "cinematográfica"**: pretos levemente lavados, brancos que nunca estouram,
  sombras puxadas para o marrom, pele viva e fundo menos saturado, com um brilho suave nas luzes.
- **Legendas curtas no meio da tela** (1 a 3 palavras por vez) e, nos momentos fortes, **uma palavra
  enorme em itálico com brilho branco**.
- Títulos em **serifa elegante cor creme** e listas em **letra cursiva fina** que vão surgindo linha a linha.
- **Voz limpa e na frente**, com uma **música instrumental bem baixinha** por baixo.
- Cortes rápidos sem pausas, transições suaves e um ou outro trecho em **preto e branco** para emoção.

## 2. Cor — "FOTO PROFISSIONAL" (opção 2, aprovada em 23/11/2026)

> **Decisão dela (23/11/2026), vale para todos os vídeos:** imagem com cara de fotografia profissional,
> **nada de claro/lavado**. A causa de tudo estar "muito claro" e com "qualidade ruim" era **técnica**:
> o iPhone grava em **HDR (HLG, bt2020, 10 bits)** e eu tratava o vídeo como comum (ficava lavado) e
> ainda exportava marcado como HDR (o celular mostrava **mais claro** do que o ajustado). Tudo o que
> foi feito antes disso (cor do teste 1, `cor.py`, `cor_estilo.py`, "padrão de filme") é **histórico**:
> não use nos vídeos novos.

**A receita (sempre, nesta ordem, depois do enquadramento em 1080×1920):**

1. **Converter o HDR corretamente** (zscale + tonemap):
   `zscale=t=linear:npl=200,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=rgb24`
2. **Acabamento da opção 2:** contraste leve e toque quente
   `curves=master='0/0 0.25/0.22 0.5/0.5 0.75/0.79 1/1',colorbalance=rm=0.02:bm=-0.02`, depois
   vinheta suave + brilho leve nas luzes (screen 15%) + nitidez `unsharp=5:5:0.6:5:5:0`, e conversão
   para YUV com matriz bt709 (`scale=out_color_matrix=bt709:out_range=tv,format=yuv420p`).
   (Receita pronta em `exemplos/lote-neface.py`: variáveis `TOM` e `ACAB`.)
3. **Fundo desfocado** (abaixo), legendas e, na exportação, **grão fino** `noise=c0s=2:c0f=t` (tira os
   "degraus" do fundo liso desfocado).
4. **Exportar como vídeo NORMAL (SDR bt709), nunca marcado como HDR:**
   `-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`, `-crf 15 -preset slow`.

- **Luz quente (escritório com estante/parede cinza, 26/11/2026):** a receita padrão deixou a pele dela
  **vermelha demais**. A cor "C" (vermelho `r='0/0 0.5/0.455 1/0.97'`, saturação 0,9) ainda deixou vermelho;
  ela aprovou a **"E"**: `r='0/0 0.5/0.42 1/0.95'`, `g='0/0 0.5/0.51 1/1'`, `b='0/0 0.5/0.515 1/1'` e
  saturação 0,82 (`ACAB_E` em `exemplos/lote-neface.py`). Mostre a pessoa de corpo inteiro na comparação.
  Se ainda achar vermelho, tire saturação **só dos vermelhos/magentas** (`huesaturation=colors=r+m:saturation=-0.35:hue=6`,
  cor "G"; no preenchimento testamos também a "K" (vermelhos/magentas -40%, amarelos -45% e `colorbalance=rm=-0.02:bm=0.03:rh=-0.01:bh=0.02`), mas no fim ela preferiu a **G**). Os números da pele podem "bater" e ela continuar vendo
  vermelho nas bochechas e no nariz: o que vale é o olho dela, então mostre a comparação. Sempre confira a pele
  num quadro ampliado do rosto antes de renderizar: se a razão R/G da pele passar de ~1,4, ela está vermelha.
- **"Linha" ao lado da cabeça:** se aparecer uma linha fina e nítida junto do cabelo, quase sempre é algo
  do cenário (cordão, corrente, friso) que encosta nela e o recorte trata como contorno do cabelo. Use a opção
  `cordao=X0:X1` do `desfoque.py` (colunas onde o objeto está) e confira quadros ampliados da cabeça.
- Vídeo que **não** for HDR (sem `color_transfer=arib-std-b67` no ffprobe): pule o passo 1.
- Se ela achar claro/escuro demais: o `npl` do passo 1 controla a exposição (200 = aprovado; maior =
  mais escuro, ex.: 260). Mostre opções em imagem antes de renderizar tudo.

- **Não remova** o `format=rgb24` antes do `format=yuv420p` no fim: sem ele, o ffmpeg 6.1 deixa a
  imagem rosa/magenta.
- Trechos em **preto e branco** (momentos emocionais, como agradecimento ou história pessoal):
  depois do filtro, acrescente `,hue=s=0,curves=master='0/0.04 0.5/0.5 1/0.95'`.
- **Fundo desfocado SEMPRE (pedido dela, 17/11/2026):** como na referência, ela nítida e o fundo em
  desfoque. Recorte a pessoa (`recorte.py`) e desfoque o fundo com `desfoque.py`. **Intensidade 10** (ela pediu
  "razoável, não muito intenso"; 22 ficou forte demais).
  Não use `gblur` direto no ffmpeg: cria uma sombra escura em volta do cabelo.

## 3. Legendas

> **Grafia do método: sempre "N.E. Face"** (com pontos), em legenda, destaque e texto na tela.

**Decisão dela (17/11/2026, depois do teste 1): elegante e minimalista. Só DOIS estilos, ambos BRANCOS.**
Ela é harmonizadora e achou "poluído" ter 4 fontes e cores diferentes. **Não use** título creme,
letra cursiva, serifa, lista ou qualquer outra cor de texto. Nada de título no topo: os ganchos e
as viradas de assunto ("Primeiro", "Segundo") entram como fala normal ou como ênfase.

Modelo: `instagram/legendas-modelo.ass`. Fontes em `instagram/fontes/`. Renderize com
`ass=legendas.ass:fontsdir=instagram/fontes`.

| Estilo | Uso | Fonte |
|---|---|---|
| `Fala` | legenda padrão, branca, no meio da tela (y ≈ 1180) | Montserrat SemiBold 64 |
| `Destaque` + `DestaqueBrilho` | **ênfase**: a palavra forte, enorme, branca com brilho | **Cormorant Bold Italic 220** (estreitada a 90%). Ela achou feio o N enrolado da Playfair Italic (23/11/2026) |
| ~~`Apoio`~~ | **não usar** (ela não quer palavrinha em cima da ênfase) | — |

Regras:
1. **1 a 3 palavras por vez**, trocando no ritmo da fala (tempo de cada palavra com `transcrever.py`).
   Nunca duas linhas de legenda corrida.
2. Entrada com fade curto (`\fad(60,0)`). **Uma legenda NUNCA fica em cima da outra** (pedido dela):
   cada uma termina exatamente quando a próxima começa, inclusive a ênfase. Confira com um script antes de exportar.
3. **Ênfase (pedido dela, 18/11/2026): primeiro a frase, depois a palavra de destaque, nunca juntas.**
   A parte da frase antes da palavra forte entra como legenda `Fala` normal, na posição de sempre
   (ex.: "com o"). Quando ela fala a palavra forte, a frase sai e a palavra de destaque entra **sozinha**,
   no mesmo lugar, grande e com brilho (entra desfocada e fica nítida em ~0,3 s). Nada fica em cima e
   nada muda de posição. No máximo 1 ênfase a cada 5–8 s. Palavras longas: reduza o `\fs` para caber.
4. Revise a transcrição: corrija nomes, termos técnicos e acentos. Tire "né", "tipo", "é…".
5. **Fundo claro (os vídeos dela):** coloque um halo escuro suave na Fala
   (`\3c&H1A2430&\3a&H70&\bord4\blur8`). Não aparece como cor, só dá leitura.
6. **Legenda que ela grava no vídeo** (para eu ler): use para corrigir a transcrição e tire do vídeo
   final cortando a faixa de baixo (no teste 1: recorte de 1080×1820 a partir do topo e depois
   enquadramento 9:16 ampliado).
7. **NUNCA em cima do rosto (ela reclamou nos vídeos NE Face).** A altura padrão (y ≈ 1180) só serve
   quando ela está enquadrada como no teste 1. Confira um quadro de cada vídeo: se ela aparece mais
   baixa na tela (sentada, plano mais aberto), desça a legenda para a altura do colo (NE Face: y = 1430).
8. Nada abaixo de y ≈ 1500 (legenda do post e botões do Instagram) nem colado na direita.
   Mova a legenda se ela cair em cima do rosto.

## 4. Áudio

1. **Voz** (sempre primeiro):
   `highpass=f=80,afftdn=nf=-25,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,loudnorm=I=-14:TP=-1.5:LRA=7`
2. **Cortar pausas e respirações longas** (jump cuts): o ritmo da referência não tem silêncio.
   Use os tempos das palavras para cortar pausas acima de ~0,35 s e erros/repetições.
3. **Música de fundo — bem baixinha (decisão dela, 24/11/2026).** Mantenha o nível original:
   `volume=0.22` e `sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400`. Testei a música
   mais alta (12 dB abaixo da voz) e ela **não gostou**: não aumente. Instrumental calma (piano, lo-fi suave, cordas), **sem letra** quando ela
   estiver falando, uns 20 dB abaixo da voz, com abaixamento automático enquanto ela fala
   (`sidechaincompress`). Fade-in de 0,5 s e fade-out de 1 s.
   - Fonte que funciona daqui: **incompetech.com** (Kevin MacLeod, licença CC BY 4.0). Exige crédito
     na **legenda do post**: "Música: <nome> — Kevin MacLeod (incompetech.com), CC BY 4.0". Sempre
     entregue esse texto para ela. Pixabay bloqueia o acesso automático.
   - **Decisão dela (17/11/2026): o Claude faz tudo, inclusive escolher e colocar a música.**
     Use trilhas instrumentais livres de direitos para redes sociais, que combinem com o clima
     elegante (piano, cordas, lo-fi suave). Se ela mandar uma música específica, use a dela.
   - **Mixagem sem cortar o fim (bug do teste 1):** a voz passa por `loudnorm`, que muda a taxa de
     amostragem, e o `sidechaincompress` terminava o som 3 s antes do vídeo, cortando a última frase.
     Sempre use `aresample=48000,apad=whole_dur=<duração>` na voz, `aresample=48000` na música e
     `amix=...:duration=first`. **Confira que o áudio final tem a mesma duração do vídeo.**
4. Vídeos sem fala (só imagens): música mais presente, cortes no ritmo da batida.

## 5. Cortes, transições e movimento

- **Repetições (ela reclamou):** quando ela erra e repete a frase no mesmo arquivo, fica só a última
  tentativa completa. A transcrição do arquivo bruto erra os tempos e esconde repetições, então
  **depois de cortar, transcreva de novo o vídeo já cortado** e leia procurando frases repetidas antes de
  seguir. As legendas saem dessa 2ª transcrição (tempos exatos). Ferramenta: `exemplos/lote-neface.py --corte`.
  **A transcrição do vídeo inteiro NÃO pega começos interrompidos** ("E com... E com o meu método"):
  ela "limpa" a repetição. Ela reclamou disso na Juliana. **Sempre** rode
  `exemplos/ouvir-trechos.py <vídeo>`, que transcreve cada trecho entre silêncios separado, e leia
  procurando frase cortada no meio ("...", palavra solta) seguida da frase inteira. Trechos de
  menos de ~0,5 s que saem como "Método N.E. Face" são respiração/ruído (o Whisper repete a dica): corte também.
  **Nunca corte o fim de uma fala porque a transcrição saiu sem sentido** ("Método, Michelle, me vamos
  conversar" era "Me chama e vamos conversar", o convite final da Monique: ela reclamou do "corte
  bruto"). Na dúvida, transcreva o trecho com o modelo `medium` antes de decidir. Confira sempre o
  **final de cada vídeo** (o último trecho ganha 0,4 s de folga: a última palavra morre baixinho): ele tem que terminar numa frase de fechamento, nunca no meio.
  Para achar a tentativa certa, transcreva **cada trecho de fala separado** (entre silêncios): mostra
  exatamente onde começa a última tentativa completa. Ao mudar as janelas de um vídeo, **apague os
  pedaços já renderizados** (`trechos/`, `corte.mkv`, `cortado.*`), senão os antigos são reaproveitados.
- **Ritmo:** cortar todas as pausas (silêncio > ~0,3 s). Gancho forte nos 2 primeiros segundos.
- **Toda emenda de corte tem transição, alternando os dois tipos da referência** (aprovado no teste 1):
  - **Aproximação:** o trecho novo começa e "empurra" 7% para dentro em 0,45 s, suave no fim
    (`scale=...:eval=frame` com `k=1+0.07*p*(2-p)`, `p=min(t/0.45,1)`, depois `crop` 1080×1920).
  - **Brilho:** clarão suave que se apaga em 0,3 s (cópia desfocada somada só no brilho/luma, força 0,4;
    0,85 ficou estourado no fundo claro dela).
  - Além disso, alterne o enquadramento entre trechos (100% e 112%) para esconder o corte.
- **Flash branco** curto nas viradas de assunto ("Primeiro", "Segundo").
- **Cenas de apoio (B-roll)** e **telas divididas** quando ela mandar imagens.
- Implementação completa: `instagram/exemplos/teste1-bone-smashing.py`.

## 5a. Fotos de antes e depois — FORMATO APROVADO (23/11/2026, pelos prints da @dra.luiseferrao)

**Use este formato para as fotos dela.** Ele substitui o "cartão" da seção 5b quando a foto é um antes e depois.

1. Ela em **tela cheia**.
2. Entra a foto ocupando **TODA A LARGURA** da tela (nada de cartão pequeno ou de margem), na parte de
   cima, até a altura da cabeça dela (máx. ~1150 px). A parte de baixo da foto **se funde suavemente**
   no vídeo numa emenda BEM FININHA (~70 px). Ela reclamou da de 300 px: o desfoque invadia a foto.
3. **A cabeça dela fica NA FRENTE** da parte de baixo da foto (recorte com `recorte.py`). Ela desce
   só ~60 px.
4. **Zoom suave** na foto enquanto está na tela (até 8%), puxando para o antes ou para o depois conforme a fala.
5. Na saída, **animação de zoom** (10% → 0 em 0,5 s) e volta para ela em tela cheia.
- **Sem nome nenhum nas fotos.** Só os textos do roteiro: "Resultado imediato" (canto) e, na Monique,
  "Dia 1 → 3 anos depois".
- **Qualidade das fotos:** use sempre o arquivo original de maior resolução, sem bordas (se vier com
  faixa desfocada nas laterais, peça a foto limpa ou corte), redimensione com lanczos.
- Legendas continuam na altura do colo (não ficam em cima da foto nem do rosto).
- Ferramentas: `exemplos/fotos-largura-total.py` (montagem) e `exemplos/neface-plano-fotos.py`
  (em que frase cada foto entra e sai, com foco no antes/depois). Mostre **um exemplo** antes de aplicar em todos.

## 5b. Tela dividida (muito usada na referência, sempre que possível)

Use quando ela comenta um caso, uma foto, um produto ou um ambiente: a imagem fica em cima e ela
continua falando embaixo. Script: `instagram/tela-dividida.sh` (aplica o filtro de cor em tudo).
As máscaras saem de `instagram/mascaras.py`.

| Formato | Como fica | Quando usar | Comando |
|---|---|---|---|
| **Cartão** | foto/vídeo num cartão de cantos arredondados (860×640) no alto, com sombra suave, por cima da fala | mostrar uma foto, um print, um vídeo curto | `DESCER=420 ./tela-dividida.sh cartao fala.mp4 foto.jpg saida.mp4` |
| **Comparação** | cartão largo (1000×620) com **duas imagens lado a lado** | antes e depois, dois ângulos, duas opções | `DESCER=420 ./tela-dividida.sh comparacao fala.mp4 a.jpg b.jpg saida.mp4` |
| **Metade** | imagem ocupando o terço de cima (1080×860), **emenda esfumada** com a fala embaixo e a legenda `Fala` na emenda (y≈830) | explicar algo na imagem, com riscos desenhados | `./tela-dividida.sh metade fala.mp4 foto.jpg saida.mp4` |

- **Fotos de antes e depois dela (23/11/2026): cada foto JÁ É uma montagem antes × depois.** Não
  junte duas imagens (o formato "comparação" é só para quando vierem imagens separadas). Use o
  **cartão** com a foto **inteira, exatamente como está**: sem cortar, o cartão se ajusta à proporção
  da foto (encaixar, não preencher). Cabeça dela na frente ou cartão inteiro acima, pelo contexto,
  e zoom suave na foto para guiar o olhar.
- **Quem escolhe o formato é o Claude, pelo contexto (decisão dela, 17/11/2026).** Não pergunte. Critério:
  - **Cartão, cabeça na frente:** ela fala de uma foto, um print, um vídeo curto ou um produto e
    continua sendo o centro da cena. É o formato mais usado.
  - **Cartão inteiro acima da cabeça:** a imagem é o principal e precisa aparecer sem nada na frente
    (detalhe pequeno, texto num print), ou o recorte da pessoa não ficou bom.
  - **Comparação:** sempre que houver duas imagens para comparar (antes e depois, dois ângulos, duas opções).
  - **Metade:** quando ela explica algo **dentro** da imagem (regiões do rosto, contorno, linhas)
    e vai ter risco desenhado. A imagem precisa de espaço e a fala fica embaixo.
  - **Sem tela dividida:** fala pessoal, emocional ou de opinião. Aí vale o rosto dela em tela cheia.
- **Regra de ouro (pedido dela): a imagem NUNCA corta a cabeça dela.** Na referência, ou a cabeça
  fica **na frente** do cartão (o cabelo passa por cima da borda), ou o cartão fica **inteiro acima**
  da cabeça. No cartão e na comparação o script já recorta a pessoa quadro a quadro (`recorte.py`,
  modelo Robust Video Matting) e põe a cabeça na frente (`FRENTE=1`, padrão). Confira sempre
  um quadro: se o recorte falhar (cabelo "comido", borda estranha), use `FRENTE=0` e suba o cartão
  (`CARTAO_Y=`) ou desça a pessoa (`DESCER=`) até a cabeça ficar inteira abaixo do cartão.
  No modo metade, ela já fica toda abaixo da imagem.
- Cartão de texto feito por mim (ex.: números de um estudo): só as mesmas duas fontes, texto escuro
  sobre fundo claro ou branco sobre escuro, sem enfeites. No teste 1 ela achou o resto poluído; mantenha mínimo.
- `DESCER=` empurra a pessoa para baixo para o rosto não ficar atrás do cartão. O espaço de cima
  vira a própria imagem desfocada e escura, com emenda suave. Ajuste o valor pelo enquadramento (0 a ~500).
- **Riscos desenhados** (setas, contornos, linhas brancas que "se desenham" sobre a foto de cima):
  estilo `Risco` no `.ass`, um desenho vetorial revelado por `\clip` animado (Exemplo 4 do modelo).
  Desenhe o traço seguindo a área de que ela está falando, sincronizado com a palavra.
- Entrada da tela dividida: corte seco ou dissolve de 0,2 s. Fica na tela enquanto ela fala daquilo
  (3 a 10 s) e sai com corte seco.
- A legenda corrida da fala continua, mas posicionada **abaixo do cartão** (ou na emenda), nunca por cima da imagem.

## 6. Exportação

- 1080×1920, 30 fps, H.264 (`-c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart`),
  áudio AAC 192 kbps, 48 kHz.
- Duração ideal: 30 a 60 s.
- Entregue também **uma capa** (quadro forte com a palavra principal no estilo `Destaque`, branca).

## 7. Dicas de gravação para passar para ela (quando fizer sentido)

- Gravar com a câmera traseira do celular, em 4K e 30 fps, de frente para uma janela (luz natural de lado).
- Usar o **modo Cinema/Retrato** do iPhone para ter o fundo desfocado da referência.
- Microfone de lapela, se tiver. A voz limpa faz tanta diferença quanto a imagem.
- Fundo neutro (bege, branco, madeira) combina com o filtro.

## 8. Conteúdo

**Decisão dela (17/11/2026):** os vídeos são para o **Instagram**, não para o Google Ads. As regras
do `COMPLIANCE.md` (sem antes e depois, sem nomes de produtos etc.) valem para o site e os anúncios,
**não para estes vídeos**. Pode replicar a referência por completo, inclusive comparações e nomes,
sem ficar avisando. Só não reaproveite nada destes vídeos no site ou nos anúncios do Google.

## 9. Roteiro de trabalho quando chegarem os arquivos

Modelo completo de edição (cortes, zoom alternado, cartão com a cabeça na frente, legendas, música):
`instagram/exemplos/teste1-bone-smashing.py`. Copie para a pasta do vídeo novo e adapte.


1. Baixar (Google Drive com link "qualquer pessoa com o link"):
   `curl -L -o bruto.mp4 "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`
   Guarde os brutos no scratchpad, **nunca no git** (são grandes).
2. Assistir: tirar quadros (`fps=1/4`) e transcrever (`transcrever.py`).
3. Montar o corte: pausas fora, melhor ordem, gancho no início.
4. Cor "foto profissional" (seção 2) → fundo desfocado → transições → legendas → áudio → exportar como SDR bt709.
5. Mostrar para ela 3–4 quadros do resultado e enviar o vídeo final. Ajustar o que ela pedir.
6. O que ela aprovar ou rejeitar no estilo, **anote neste arquivo** para as próximas edições.
