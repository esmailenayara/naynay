@AGENTS.md

# Site da Dra. Nayara Esmaile — contexto para o Claude Code

Quem usa este projeto é a própria **Dra. Nayara Esmaile** (não é programadora). Fale com ela em português, sem jargão técnico, em frases curtas. Ela decide o conteúdo; você cuida da parte técnica, confere o resultado e publica quando ela pedir.

## O que é

Landing page de uma página só, no ar em **https://dranayaraesmaile.com.br** (e `www.`). Ela recebe tráfego de **Google Ads (rede de Pesquisa)**. O objetivo é a pessoa chamar no **WhatsApp** para agendar a consulta.

Prioridades, nesta ordem:
1. **Ser aprovada pelo Google Ads.** Campanhas anteriores foram reprovadas por "antes e depois" e por "medicamentos restritos". Qualquer texto novo passa pelas regras abaixo.
2. Converter visita em conversa no WhatsApp.

## Stack e comandos

- Next.js 16 (App Router, Turbopack) + TypeScript + Tailwind 4, com **export estático** (`output: "export"`, pasta `out/`). Fonte Jost.
- Hospedagem: **Cloudflare Workers com arquivos estáticos** (NÃO é Pages nem OpenNext). A configuração está em `wrangler.jsonc`. Conta Cloudflare: esmaile.nayara@gmail.com. Domínio no registro.br, pago até 08/11/2030, com DNS na Cloudflare.

```bash
npm install          # primeira vez
npm run dev          # http://localhost:3000 para ver as alterações
npm run publicar     # build + deploy na Cloudflare (~1 min); coloca no ar
npx wrangler login   # se o publicar pedir login (clicar em Allow, conta esmaile.nayara@gmail.com)
```

- Se o `wrangler deploy` oferecer migrar para OpenNext ou "configurar automaticamente", **recuse**. Já aconteceu e quebrou o build. O `wrangler.jsonc` atual está correto.
- O `.env.local` não vai para o git e é lido no build. Depois de mudar qualquer variável, rode `npm run publicar` de novo.
  - `NEXT_PUBLIC_SITE_URL=https://dranayaraesmaile.com.br`
  - `NEXT_PUBLIC_GADS_ID`: ID `AW-…` do Google Ads. **Ainda vazio.**
  - `NEXT_PUBLIC_GADS_CONV_WHATSAPP`: `AW-…/rótulo` da conversão "Clique no WhatsApp". **Ainda vazio.**
  - `NEXT_PUBLIC_MOSTRAR_RASCUNHO`: deixar vazio no site oficial.
- O `devIndicators: false` no next.config é de propósito: o "N" do Next no canto da tela já foi confundido com o logo.
- Às vezes o `npm run dev` não recarrega sozinho depois de uma edição. Se a mudança não aparecer, reinicie o servidor antes de concluir que não funcionou.

## Onde fica cada coisa

| O quê | Arquivo |
|---|---|
| Nome, e-mail, formação, WhatsApp, Instagram, endereços, link do perfil do Google | `lib/site.ts` |
| Título e subtítulo do topo, aviso de resultados, SEO, **mensagem do WhatsApp** | `lib/terms.ts` |
| Faixa de fatos, passos, "Sobre a Dra.", "O que esperar", FAQ | `lib/conteudo.ts` |
| Procedimentos (perguntas e respostas) e depoimentos | `lib/procedimentos.ts` |
| Seções da página (topo, faixa, compromisso, sobre…) | `components/Secoes.tsx` e demais `components/` |
| Cores e tokens | `app/globals.css` |
| Fotos e logos | `public/images/` (ver tabela no README) |
| Política de Privacidade / Termos | `app/politica-de-privacidade/`, `app/termos-de-uso/` (ao mudar, atualize `ATUALIZACAO_LEGAL` em `lib/site.ts`) |

Os itens de conteúdo têm `confirmado: true/false`. Os que estão como `false` só aparecem no `npm run dev`, nunca no site publicado.

## Regras de compliance (Google Ads + CFM/saúde): não quebrar

Leia **COMPLIANCE.md** antes de mudar textos ou fotos. Resumo:
- **Nunca** citar nomes de marcas ou de substâncias: botox, toxina, botulínica, dysport, xeomin, radiesse, sculptra, juvederm, restylane etc. Use termos neutros, centralizados em `lib/terms.ts`.
- **Nunca** usar fotos de antes e depois, rosto de paciente, procedimento acontecendo, agulha, frasco ou caixa de produto. Exceção conhecida: a foto do topo (`hero.jpg`) mostra a Dra. com uma seringa. Foi decisão dela, e o risco está registrado no COMPLIANCE.md.
- Sem promessa de resultado ("garantido", "definitivo", "sem dor", "sem risco"), sem superlativo ("melhor", "referência", "número 1"), sem preço, desconto ou promoção.
- Manter o aviso "os resultados variam de pessoa para pessoa" (`AVISO_RESULTADOS`).
- Remarketing desligado de propósito, porque saúde é categoria sensível. O Consent Mode começa negado e `ad_personalization` fica sempre desligado. Não mude isso.
- Depois de **qualquer** edição de texto, rode o grep de termos proibidos (está no fim do COMPLIANCE.md). Resultados já conhecidos e aceitos: `100%` (gradiente das estrelas) e "melhor" no depoimento da Karla.

## Decisões da Dra. (respeitar sem perguntar de novo)

- Escrever **"consulta"** ou **"consulta avaliativa"**, nunca "avaliação". Sempre **"Dra. Nayara Esmaile"**.
- Ela atende em dois **locais de atendimento** que não são dela: **Tijuca** (Rua Conde de Bonfim, 497, Tijuca Blue Offices) e **Barra da Tijuca** (Av. João Cabral de Mello Neto, 850, CEO Corporate Executive Offices). Diga "locais", nunca "unidades" ou "clínica". Não informe sala, bloco nem horários.
- Contato **só pelo WhatsApp** (21) 99064-5009: sem formulário e sem ligação. Todos os botões usam a mesma mensagem, "Olá, vim do Google e gostaria de tirar algumas dúvidas" (`MENSAGEM_WHATSAPP_PADRAO` em `lib/terms.ts`). Os botões têm `data-conv="whatsapp"` para a conversão do Ads; mantenha esse atributo em qualquer botão novo do WhatsApp.
- Não mencionar bióloga nem CRBio. Formação exibida: "Formada pela UFRJ" e "Pós-graduada em Saúde Estética e Procedimentos Injetáveis". É autônoma, sem CNPJ, e o rodapé não tem "responsável técnica" nem "profissional autônoma".
- Lema: **naturalidade e elegância**. A ideia de "pode decidir depois" aparece só na última resposta do FAQ, sem destaque em outros lugares.
- Instagram (@nayaraesmaile) só no rodapé. Os botões "Ver depoimentos" e "Ver fotos" levam ao perfil do Google com 89 avaliações (`PERFIL_GOOGLE`, link `maps.google.com/?cid=…`). Os links `share.google` abrem só uma pesquisa, então não use. O site não mostra nota nem número de avaliações; a frase é "A Dra. Nayara Esmaile é 5 estrelas na plataforma."
- Gosto visual: tons café e bege, botões café sólidos (`--botao: #4a3428`), destaques em itálico, estrelas finas dourado-champanhe, cabeçalho fixo sempre na cor escura (`bg-dark`, nunca transparente). Ela **não gosta** de visual infantil, de muitas cores nem de nada "pesado". Antes de mudar algo visual, mostre como ficou (screenshot no celular e no computador) e pergunte.

## Como trabalhar com ela

1. Ela pede uma mudança. Você edita, roda `npm run dev` e mostra o resultado (no celular e no computador, quando for visual).
2. Se for texto, rode o grep de compliance. Se algo arriscar a aprovação do Google, avise de forma simples e sugira uma alternativa antes de aplicar.
3. Só publique (`npm run publicar`) quando ela aprovar. Depois confira no endereço real (`curl -s https://dranayaraesmaile.com.br/ | grep …`) e confirme para ela que está no ar.
4. Faça commit no git a cada mudança publicada, com uma mensagem curta em português. Assim dá para voltar atrás se ela não gostar.

## Pendências

- [ ] **Conversão do Google Ads:** criar no Ads a ação "Clique no WhatsApp" (Metas → Conversões → Nova → Site → manual; categoria Contato; contagem "Uma"). Preencher `NEXT_PUBLIC_GADS_ID` e `NEXT_PUBLIC_GADS_CONV_WHATSAPP` no `.env.local`, rodar `npm run publicar` e conferir se o gtag aparece no HTML depois de aceitar os cookies.
- [ ] **Always Use HTTPS:** no painel da Cloudflare (dranayaraesmaile.com.br → SSL/TLS → Edge Certificates), ligar a opção, porque `http://` ainda não redireciona. O token do wrangler não tem permissão para isso, então ela precisa clicar no painel.
- [ ] Na campanha: nada de "botox" nem de outras marcas nas palavras-chave e nos anúncios, e não usar a extensão de local.
