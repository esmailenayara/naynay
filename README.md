# Landing page — Dra. Nayara Esmaile (consulta avaliativa)

Página única para receber tráfego de Google Ads (rede de Pesquisa). Objetivo: levar a pessoa a agendar a consulta **pelo WhatsApp**, único canal de contato (sem formulário e sem ligação).

- Next.js 16 (App Router) + TypeScript + Tailwind 4, **exportação 100% estática** (pasta `out/`, sem servidor).
- Contato só pelo WhatsApp: todos os botões abrem a conversa com a mensagem "Olá, vim do Google e gostaria de tirar algumas dúvidas". Atendimento humanizado feito pela equipe.
- Antes de mexer em qualquer texto, leia [COMPLIANCE.md](COMPLIANCE.md). O que falta preencher está em [PLACEHOLDERS.md](PLACEHOLDERS.md).

## Rodar no computador

```bash
npm install
cp .env.example .env.local   # e preencha as variáveis
npm run dev                  # http://localhost:3000
npm run build                # gera a pasta out/ (site estático)
npx serve out                # testa o build final localmente
```

No `npm run dev`, textos ainda não confirmados aparecem com a etiqueta amarela **CONFIRMAR**. No `npm run build` eles **somem** do site até virarem `confirmado: true` em `lib/conteudo.ts` / `lib/procedimentos.ts`.

Para gerar um link de **revisão** com tudo visível (para ela ler os textos no celular), faça um deploy de teste com `NEXT_PUBLIC_MOSTRAR_RASCUNHO=1`. Nunca use essa variável no site oficial nem aponte o anúncio para esse link.

## Onde editar cada coisa

| O quê | Arquivo |
|---|---|
| Nome, e-mail, formação, endereços, WhatsApp, Instagram, perfil do Google | `lib/site.ts` |
| Termos neutros, título, subtítulo, aviso de resultados, mensagem do WhatsApp, SEO | `lib/terms.ts` |
| Faixa de fatos, passos, "Sobre a Dra.", "O que esperar", FAQ | `lib/conteudo.ts` |
| Procedimentos (perguntas e respostas) e avaliações do Google | `lib/procedimentos.ts` |
| Cores (marrom e bege; paleta alternativa comentada) e fonte | `app/globals.css`, `app/layout.tsx` (Jost) |
| Política de Privacidade / Termos de Uso | `app/politica-de-privacidade/page.tsx`, `app/termos-de-uso/page.tsx` |

Busque por `[PREENCHER` e `[CONFIRMAR` no projeto para achar tudo que falta.

## Como trocar as fotos

Cada lugar de foto é um `<PhotoSlot>`. Enquanto o arquivo não existir, aparece uma caixa tracejada com a descrição da foto ideal. **Para trocar, basta salvar o arquivo com o nome exato em `public/images/` e rodar o build de novo.** A caixa tem proporção fixa, então a página não "pula".

| Arquivo | Proporção | Tamanho | O que mostrar |
|---|---|---|---|
| `hero.jpg` | retrato | 847 × 1280 ou maior | **Foto do topo.** Retrato da Dra. em fundo escuro. No computador ocupa a direita da tela; no celular fica em cima do texto. Hoje tem uma seringa na mão (ver COMPLIANCE.md). |
| `faixa-ambiente.jpg` | paisagem | 2000 × 1200 | Foto de fundo da faixa "Primeiro, a conversa": detalhe do ambiente sem pessoas |
| `profissional-nayara.jpg` | 4:5 | 1000 × 1250 | Retrato profissional, fundo neutro |
| `local-tijuca.jpg` | 16:9 | 1200 × 675 | Fachada, entrada do prédio ou recepção |
| `local-barra.jpg` | 16:9 | 1200 × 675 | Fachada, entrada do prédio ou recepção |
| `og.jpg` | 1200 × 630 | — | Imagem que aparece ao compartilhar o link (WhatsApp/redes). Hoje é o logo completo em fundo marrom. |
| `logo-horizontal-bege.png` | — | 820 × 96 | Logo horizontal da Dra. (nome com o ponto + "Harmonização Facial e Estética Avançada"), sem o monograma, fundo transparente. Aparece no rodapé, só no computador. |
| `monograma-bege.png` | — | 500 × 540 | Monograma "NE" com fundo transparente. Base do ícone da aba; não aparece na página. |
| `app/icon.png` / `app/apple-icon.png` | quadrado | 512 × 512 | Ícone da aba do navegador e do atalho no celular: monograma bege em fundo marrom. |

Regras das fotos (ver COMPLIANCE.md): **sem** antes e depois, sem procedimento acontecendo, sem agulha, seringa, frasco ou caixa de produto, sem rosto de paciente, sem banco de imagens que pareça paciente, sem corpo exposto.

Como o site é estático, as fotos não são otimizadas automaticamente. Antes de salvar: exporte em JPG no tamanho da tabela, qualidade ~75, e passe no [Squoosh](https://squoosh.app). Alvo: **até 250 KB** cada; as duas fotos de fundo, **até 300 KB** (a do topo pesa no LCP).

## Variáveis de ambiente

| Variável | Para quê |
|---|---|
| `NEXT_PUBLIC_SITE_URL` | URL final, `https://dranayaraesmaile.com.br` (canonical, sitemap, og). **Obrigatória antes do build de produção.** |
| `NEXT_PUBLIC_GADS_ID` | ID do Google Ads (`AW-XXXXXXXXXX`). Vazio = nenhum script do Google carrega. |
| `NEXT_PUBLIC_GADS_CONV_WHATSAPP` | Rótulo da conversão "Clique no WhatsApp". |
| `NEXT_PUBLIC_MOSTRAR_RASCUNHO` | `1` só em deploy de revisão: mostra textos ainda não confirmados. **Vazio no site oficial.** |

Como as variáveis são lidas no build, **depois de mudar qualquer uma é preciso fazer um novo deploy**.

### Criar as conversões no Google Ads
Metas → Conversões → Nova ação → Site → configurar manualmente. Crie uma ação "Clique no WhatsApp", categoria "Contato", contagem "Uma". Copie o `send_to` para `NEXT_PUBLIC_GADS_CONV_WHATSAPP`.

### Remarketing: desligado de propósito
Saúde é categoria sensível nas políticas de publicidade personalizada do Google. O código envia `allow_ad_personalization_signals: false`, `ad_personalization: denied` e `allow_google_signals: false`. **Não** crie públicos de remarketing nem "segmentos de dados" a partir deste site na conta do Google Ads.

## Publicar alterações (dia a dia)

O site está na Cloudflare (Workers, só arquivos estáticos), no domínio **dranayaraesmaile.com.br**. Depois de alterar e conferir no `npm run dev`:

```bash
npm run publicar
```

Isso gera a versão final e envia para a Cloudflare em cerca de um minuto. Se pedir login, rode `npx wrangler login` e clique em **Allow** no navegador (conta esmaile.nayara@gmail.com).

## Hospedagem (configuração já feita)

- Cloudflare Workers com arquivos estáticos (`wrangler.jsonc`), conta esmaile.nayara@gmail.com. Domínios próprios: `dranayaraesmaile.com.br` e `www.dranayaraesmaile.com.br` (registro.br, pago até 08/11/2030, DNS na Cloudflare).
- Não use OpenNext nem Cloudflare Pages: se o wrangler oferecer migrar ou configurar automaticamente, recuse.
- Falta ligar **Always Use HTTPS** no painel (SSL/TLS → Edge Certificates).

## Checklist técnico depois do deploy
- [ ] Abrir no celular e tocar em cada botão de agendar: o WhatsApp abre com a mensagem certa.
- [ ] Google Ads → Conversões: a ação "Clique no WhatsApp" sai de "Não verificado" depois dos primeiros testes.
- [ ] PageSpeed Insights (pagespeed.web.dev), versão mobile: ≥ 90 em Desempenho, Acessibilidade e SEO.
- [ ] `https://dranayaraesmaile.com.br/sitemap.xml` e `/robots.txt` abrindo.
