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

## 2. Cor (o "filtro")

O filtro está pronto em `instagram/filtro-cor.txt` (cadeia do ffmpeg). Medidas que ele reproduz,
tiradas dos quadros da referência:

| Característica | Referência | Como o filtro faz |
|---|---|---|
| Pretos | nunca chegam a 0; ficam em ~6% (preto "leitoso") | curva levanta o ponto preto para 0,055 |
| Brancos | topo em ~80–93%, sem estourar | curva limita o branco em 0,93 |
| Sombras | quentes, R bem acima de B | colorbalance: sombras +vermelho, −azul |
| Saturação | média 0,27–0,34 (contida) | −8% geral, −35% em verdes, cianos e azuis |
| Brilho nas luzes | halo suave (efeito filtro "pro-mist") | cópia só das luzes, desfocada, em "screen" a 22% |
| Bordas | escurecem de leve | vinheta suave |

Como aplicar (sempre em vídeo vertical 1080×1920):

```bash
F=$(tr -d '\n' < instagram/filtro-cor.txt)
ffmpeg -i entrada.mp4 -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,$F" saida.mp4
```

- **Ajuste fino por vídeo:** o filtro foi calibrado na referência e testado nas fotos do site. Na
  primeira leva de vídeos dela, compare um quadro antes/depois e meça com o script de cor (pretos em
  ~0,05–0,07, brancos ≤0,93, sombras quentes). Celular gravando no sol ou em luz fria pode pedir mais
  calor (`rm`/`bm`) ou menos brilho. Depois de ajustar, **atualize este arquivo e o filtro**.
- **Não remova** o `format=rgb24` antes do `format=yuv420p` no fim: sem ele, o ffmpeg 6.1 deixa a
  imagem rosa/magenta.
- Trechos em **preto e branco** (momentos emocionais, como agradecimento ou história pessoal):
  depois do filtro, acrescente `,hue=s=0,curves=master='0/0.04 0.5/0.5 1/0.95'`.
- O fundo desfocado da referência vem da câmera (lente). Dá para orientar a gravação (seção 7),
  mas não dá para criar isso de forma convincente na edição. Não tente.

## 3. Legendas

Modelo pronto: `instagram/legendas-modelo.ass` (estilos já configurados). Fontes em
`instagram/fontes/` (todas gratuitas, do Google Fonts). Sempre renderize com
`ass=legendas.ass:fontsdir=instagram/fontes`.

| Estilo | Uso | Fonte |
|---|---|---|
| `Fala` | legenda corrida da fala, branca, no meio da tela (y ≈ 1180) | Montserrat SemiBold 64 |
| `FalaSerifa` | alternativa mais delicada para vídeos calmos | Cormorant Medium Italic 74 |
| `Destaque` + `DestaqueBrilho` | **a palavra forte** da frase, enorme, com brilho | Playfair ExtraBold Italic 200, estreitada a 80% |
| `Apoio` | palavrinha pequena acima e à esquerda do destaque ("é ver a", "quem") | Montserrat SemiBold 46 |
| `Titulo` | gancho/título no topo, cor creme `#F2E4C9` | Cormorant SemiBold 118 |
| `Lista` | itens que vão aparecendo um embaixo do outro | Allura 108 |

Regras:
1. **1 a 3 palavras por vez**, trocando no ritmo da fala (tempo de cada palavra com
   `instagram/transcrever.py`). Nunca duas linhas de legenda corrida.
2. Entrada com fade curto (`\fad(60,0)`). Sem saída animada: a próxima legenda substitui a anterior.
3. **Destaque:** no máximo 1 a cada 5–8 segundos, só na palavra que carrega a emoção ou o tema
   ("naturalidade", "elegância", "ajudou", "segurança"). Entra desfocada e fica nítida em ~0,3 s
   (`\blur10\t(0,280,\blur0.6)`), com a camada de brilho atrás. Enquanto o destaque está na tela,
   a legenda corrida some.
4. **Título** nos primeiros 2 segundos (o gancho), e lista em cursiva quando ela enumerar coisas.
5. Revise a transcrição: corrija nomes, termos técnicos e acentos. Tire "né", "tipo", "é…".
6. Mantenha tudo fora das áreas da interface do Instagram: nada abaixo de y ≈ 1500 (legenda do post
   e botões) nem colado na direita (curtir/comentar). Mova a legenda se ela cair em cima do rosto
   ou de uma roupa branca (ilegível).

## 4. Áudio

1. **Voz** (sempre primeiro):
   `highpass=f=80,afftdn=nf=-25,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,loudnorm=I=-14:TP=-1.5:LRA=7`
2. **Cortar pausas e respirações longas** (jump cuts): o ritmo da referência não tem silêncio.
   Use os tempos das palavras para cortar pausas acima de ~0,35 s e erros/repetições.
3. **Música de fundo**: instrumental calma (piano, lo-fi suave, cordas), **sem letra** quando ela
   estiver falando, uns 20 dB abaixo da voz, com abaixamento automático enquanto ela fala
   (`sidechaincompress`). Fade-in de 0,5 s e fade-out de 1 s.
   - Use **só música que ela mesma enviar** ou de banco livre de direitos. Melhor ainda: postar o
     vídeo sem música e ela escolher a trilha pelo próprio Instagram (biblioteca licenciada).
     Pergunte qual opção ela prefere na primeira vez e registre aqui.
4. Vídeos sem fala (só imagens): música mais presente, cortes no ritmo da batida.

## 5. Cortes, transições e movimento

- **Ritmo:** um corte a cada 1,5–4 s. Gancho forte nos 2 primeiros segundos.
- **Transição padrão:** corte seco. Entre cenas diferentes, dissolve curto (`xfade=fade:duration=0.25`).
- **Flash branco** (`xfade=fadewhite:duration=0.2`) para abrir um assunto novo ou revelar algo.
- **Zoom de ênfase:** nas frases fortes, aproxime de 100% para 108% em 0,3 s ou corte direto para um
  enquadramento mais fechado. Em tomadas longas, zoom lento contínuo (cerca de 1% por segundo).
- **Cenas de apoio (B-roll):** ambiente, mãos, detalhes, ela de perfil. Entram por cima da fala,
  com a legenda continuando.
- **Preto e branco** em trechos emocionais (ver seção 2).

## 6. Exportação

- 1080×1920, 30 fps, H.264 (`-c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart`),
  áudio AAC 192 kbps, 48 kHz.
- Duração ideal: 30 a 60 s.
- Entregue também **uma capa** (quadro forte com o título em `Titulo`).

## 7. Dicas de gravação para passar para ela (quando fizer sentido)

- Gravar com a câmera traseira do celular, em 4K e 30 fps, de frente para uma janela (luz natural de lado).
- Usar o **modo Cinema/Retrato** do iPhone para ter o fundo desfocado da referência.
- Microfone de lapela, se tiver. A voz limpa faz tanta diferença quanto a imagem.
- Fundo neutro (bege, branco, madeira) combina com o filtro.

## 8. Cuidados de conteúdo (Instagram também conta)

A referência mostra **antes e depois**, rostos de pacientes, agulha e **nomes de produtos**
("Radiesse", "Botox"). **Não reproduza isso nos vídeos dela**, mesmo pedindo "igual à referência".
Isso já reprovou campanhas no Google Ads e também vai contra as regras de publicidade em saúde
(ver `COMPLIANCE.md`). Se o vídeo bruto dela tiver algo assim, avise de forma simples e sugira cortar
ou trocar a palavra na legenda. Rode o grep de termos proibidos do `COMPLIANCE.md` no texto das legendas.

## 9. Roteiro de trabalho quando chegarem os arquivos

1. Baixar (Google Drive com link "qualquer pessoa com o link"):
   `curl -L -o bruto.mp4 "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`
   Guarde os brutos no scratchpad, **nunca no git** (são grandes).
2. Assistir: tirar quadros (`fps=1/4`) e transcrever (`transcrever.py`).
3. Montar o corte: pausas fora, melhor ordem, gancho no início.
4. Aplicar cor → legendas → áudio → transições → exportar.
5. Mostrar para ela 3–4 quadros do resultado e enviar o vídeo final. Ajustar o que ela pedir.
6. O que ela aprovar ou rejeitar no estilo, **anote neste arquivo** para as próximas edições.
