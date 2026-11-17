# Estilo de edição dos vídeos do Instagram (Reels)

> **Para o Claude:** quando a Dra. Nayara Esmaile enviar vídeos para editar, siga este guia
> do começo ao fim, sem perguntar de novo o que já está decidido aqui. Ela não é programadora:
> fale em português simples e mostre o resultado (prints e o vídeo final) antes de considerar pronto.

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

## 2. Cor — SEMPRE por referência (comando obrigatório)

> **Regra dela (17/11/2026):** a cor tem que ficar **sempre igual à 1ª edição do teste 1**, que ela
> aprovou. **Não aplique um filtro fixo por cima.** Cada gravação tem luz e sombra diferentes, então a
> cor é **calculada a partir do arquivo original** de cada vídeo.

**Passo 1, para cada arquivo bruto, ANTES de editar:**

```bash
python3 -I instagram/cor.py ajustar <bruto.mov> <pasta>/cor --recorte "<mesmo enquadramento da edição>"
```

- O script lê 24 quadros do **original**, mede preto, meio-tom, branco, cor de cada canal (R, G, B) e
  saturação, e calcula a curva que leva **aquele** vídeo até a cor aprovada (casamento de histograma
  por canal + ajuste de saturação). O alvo medido da edição aprovada está em `instagram/cor-alvo.json`.
- Ele imprime **ANTES / DEPOIS / ALVO**. O DEPOIS tem que bater com o ALVO: preto ~0,09–0,10,
  meio ~0,63, branco ~0,82, saturação ~0,21. Se não bater, não siga: investigue.
- Testado: um vídeo dela escurecido e esfriado de propósito chegou no mesmo alvo.
- Se a luz mudar muito **dentro** do mesmo arquivo (ex.: saiu do sol), rode por trecho com
  `--inicio S --fim S` e use a cor de cada trecho.

**Passo 2, na edição:** a cor entra logo depois do enquadramento, e é a única coisa de cor da cadeia:

```bash
... -filter_complex "<recorte>,$(cat <pasta>/cor/cor-filtro.txt)" ...
```

- `cor-filtro.txt` já inclui a textura do visual aprovado (vinheta suave e brilho leve nas luzes).
- **Não use mais** `filtro-cor.txt` nem a "pré-correção" de forma direta: elas ficam só como receita
  da edição aprovada, e o `cor.py` usa essa receita para medir o alvo.
- Só recrie o alvo (`cor.py alvo ...`) se ela aprovar **outra** cor como nova referência.

**Passo 3, conferência antes de entregar:** meça um quadro do vídeo final ao lado do alvo. Se ela
disser que a cor mudou, meça antes de mexer: no teste 1, a versão 3 tinha a mesma cor da 1ª (diferença
< 2%). O que muda a percepção é a **marcação HDR** (abaixo) e o **fundo desfocado**, que deixa o
ambiente mais liso.

- **HDR do iPhone (importante):** os vídeos dela chegam marcados como HDR (HLG, bt2020). Ela aprovou
  a cor do vídeo que saiu **com essa marcação**. Sem ela, o celular mostra a mesma imagem mais apagada
  e ela acha que "a cor mudou". Na exportação final, sempre acrescente:
  `-color_primaries bt2020 -color_trc arib-std-b67 -color_range tv`
  (confira com ffprobe que o final tem `color_transfer=arib-std-b67`).
- **Não remova** o `format=rgb24` antes do `format=yuv420p` no fim: sem ele, o ffmpeg 6.1 deixa a
  imagem rosa/magenta.
- Trechos em **preto e branco** (momentos emocionais, como agradecimento ou história pessoal):
  depois do filtro, acrescente `,hue=s=0,curves=master='0/0.04 0.5/0.5 1/0.95'`.
- **Fundo desfocado SEMPRE (pedido dela, 17/11/2026):** como na referência, ela nítida e o fundo em
  desfoque. Recorte a pessoa (`recorte.py`) e desfoque o fundo com `desfoque.py`. **Intensidade 10** (ela pediu
  "razoável, não muito intenso"; 22 ficou forte demais).
  Não use `gblur` direto no ffmpeg: cria uma sombra escura em volta do cabelo.

## 3. Legendas

**Decisão dela (17/11/2026, depois do teste 1): elegante e minimalista. Só DOIS estilos, ambos BRANCOS.**
Ela é harmonizadora e achou "poluído" ter 4 fontes e cores diferentes. **Não use** título creme,
letra cursiva, serifa, lista ou qualquer outra cor de texto. Nada de título no topo: os ganchos e
as viradas de assunto ("Primeiro", "Segundo") entram como fala normal ou como ênfase.

Modelo: `instagram/legendas-modelo.ass`. Fontes em `instagram/fontes/`. Renderize com
`ass=legendas.ass:fontsdir=instagram/fontes`.

| Estilo | Uso | Fonte |
|---|---|---|
| `Fala` | legenda padrão, branca, no meio da tela (y ≈ 1180) | Montserrat SemiBold 64 |
| `Destaque` + `DestaqueBrilho` | **ênfase**: a palavra forte, enorme, branca com brilho | Playfair ExtraBold Italic 200 (estreitada a 80%) |
| `Apoio` | palavrinha pequena acima e à esquerda da ênfase ("com o", "é") — mesma fonte da Fala | Montserrat SemiBold 46 |

Regras:
1. **1 a 3 palavras por vez**, trocando no ritmo da fala (tempo de cada palavra com `transcrever.py`).
   Nunca duas linhas de legenda corrida.
2. Entrada com fade curto (`\fad(60,0)`). **Uma legenda NUNCA fica em cima da outra** (pedido dela):
   cada uma termina exatamente quando a próxima começa, inclusive a ênfase. Confira com um script antes de exportar.
3. **Ênfase:** no máximo 1 a cada 5–8 segundos, só na palavra que carrega a emoção ou o tema.
   Entra desfocada e fica nítida em ~0,3 s, com a camada de brilho atrás. Palavras longas: reduza
   o tamanho (`\fs`) para caber. Enquanto a ênfase está na tela, a legenda padrão some.
4. Revise a transcrição: corrija nomes, termos técnicos e acentos. Tire "né", "tipo", "é…".
5. **Fundo claro (os vídeos dela):** coloque um halo escuro suave na Fala e no Apoio
   (`\3c&H1A2430&\3a&H70&\bord4\blur8`). Não aparece como cor, só dá leitura.
6. **Legenda que ela grava no vídeo** (para eu ler): use para corrigir a transcrição e tire do vídeo
   final cortando a faixa de baixo (no teste 1: recorte de 1080×1820 a partir do topo e depois
   enquadramento 9:16 ampliado).
7. Nada abaixo de y ≈ 1500 (legenda do post e botões do Instagram) nem colado na direita.
   Mova a legenda se ela cair em cima do rosto.

## 4. Áudio

1. **Voz** (sempre primeiro):
   `highpass=f=80,afftdn=nf=-25,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,loudnorm=I=-14:TP=-1.5:LRA=7`
2. **Cortar pausas e respirações longas** (jump cuts): o ritmo da referência não tem silêncio.
   Use os tempos das palavras para cortar pausas acima de ~0,35 s e erros/repetições.
3. **Música de fundo**: instrumental calma (piano, lo-fi suave, cordas), **sem letra** quando ela
   estiver falando, uns 20 dB abaixo da voz, com abaixamento automático enquanto ela fala
   (`sidechaincompress`). Fade-in de 0,5 s e fade-out de 1 s.
   - Fonte que funciona daqui: **incompetech.com** (Kevin MacLeod, licença CC BY 4.0). Exige crédito
     na **legenda do post**: "Música: <nome> — Kevin MacLeod (incompetech.com), CC BY 4.0". Sempre
     entregue esse texto para ela. Pixabay bloqueia o acesso automático.
   - **Decisão dela (17/11/2026): o Claude faz tudo, inclusive escolher e colocar a música.**
     Use trilhas instrumentais livres de direitos para redes sociais, que combinem com o clima
     elegante (piano, cordas, lo-fi suave). Se ela mandar uma música específica, use a dela.
4. Vídeos sem fala (só imagens): música mais presente, cortes no ritmo da batida.

## 5. Cortes, transições e movimento

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

## 5b. Tela dividida (muito usada na referência, sempre que possível)

Use quando ela comenta um caso, uma foto, um produto ou um ambiente: a imagem fica em cima e ela
continua falando embaixo. Script: `instagram/tela-dividida.sh` (aplica o filtro de cor em tudo).
As máscaras saem de `instagram/mascaras.py`.

| Formato | Como fica | Quando usar | Comando |
|---|---|---|---|
| **Cartão** | foto/vídeo num cartão de cantos arredondados (860×640) no alto, com sombra suave, por cima da fala | mostrar uma foto, um print, um vídeo curto | `DESCER=420 ./tela-dividida.sh cartao fala.mp4 foto.jpg saida.mp4` |
| **Comparação** | cartão largo (1000×620) com **duas imagens lado a lado** | antes e depois, dois ângulos, duas opções | `DESCER=420 ./tela-dividida.sh comparacao fala.mp4 a.jpg b.jpg saida.mp4` |
| **Metade** | imagem ocupando o terço de cima (1080×860), **emenda esfumada** com a fala embaixo e a legenda `Fala` na emenda (y≈830) | explicar algo na imagem, com riscos desenhados | `./tela-dividida.sh metade fala.mp4 foto.jpg saida.mp4` |

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
4. Cor por referência (`cor.py ajustar`, seção 2) → fundo desfocado → transições → legendas → áudio → exportar com a marcação HDR.
5. Mostrar para ela 3–4 quadros do resultado e enviar o vídeo final. Ajustar o que ela pedir.
6. O que ela aprovar ou rejeitar no estilo, **anote neste arquivo** para as próximas edições.
