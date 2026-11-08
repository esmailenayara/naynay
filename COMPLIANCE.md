# Compliance — Google Ads (saúde/estética) e LGPD

Prioridade 1: aprovação na revisão do Google. Prioridade 2: conversão. Na dúvida, foi escolhida a opção mais conservadora.

---

## ⚠️ Bloqueadores fora da página (resolver ANTES de reenviar a campanha)

Ao montar a página, consultei os dois perfis públicos do Google enviados. Eles têm problemas que **sozinhos** explicam reprovações repetidas, mesmo com uma landing page limpa. Isso pesa ainda mais se a campanha usa **recursos de local** (endereço/perfil vinculado), porque aí o nome do perfil aparece no próprio anúncio.

| # | Onde | Problema | O que fazer |
|---|---|---|---|
| 1 | Perfil Google da unidade Vila Isabel | O **nome do perfil** contém uma marca de medicamento e nomes de procedimento ("Dra. Nayara Esmaile: [marca] - Preenchimento - Bioestimulador de Colágeno : Barra da Tijuca e Vila Isabel, RJ"). Isso fere a política de medicamentos com receita do Ads **e** a regra de nomes do Perfil da Empresa (proibido incluir palavras-chave no nome). | Renomear para o nome real do negócio, igual à fachada/CNPJ, ex.: "Nayara Esmaile — Harmonização Facial e Estética Avançada". |
| 2 | Perfil Google da unidade Vila Isabel | A **descrição** cita o princípio ativo pelo nome, e há **postagens** com volume de produto e relato de insegurança de paciente. | Reescrever a descrição com os termos neutros de `lib/terms.ts`; arquivar as postagens com produto, antes e depois ou insegurança. |
| 3 | Os dois perfis | Categoria **"Médico" / "Consultório médico"**, mas a responsável técnica é **bióloga**. O Google pode tratar isso como deturpação de credenciais. | Trocar a categoria principal para "Clínica de estética" (ou equivalente não médico). |
| 4 | Perfil da Barra | O nome inclui palavras-chave ("- Harmonização Facial : Barra da Tijuca, RJ"). | Usar o mesmo nome real nos dois perfis (o de Vila Isabel, hoje ligado à unidade Tijuca, e o da Barra). |
| 5 | Os dois perfis | O botão "Site" aponta para uma página de terceiros. | Depois do deploy, trocar para o domínio próprio. |
| 6 | Instagram @nayaraesmaile | O perfil tem posts com nomes de marca e fotos de resultado. | **Não** linkar o Instagram na landing page nem usar como sitelink/recurso do anúncio (por isso ele não aparece no site). |
| 7 | Conta do Ads | As reprovações podem vir das **palavras-chave e dos textos do anúncio**, não só da página. | Ver a lista "Antes de publicar". |

> Os botões "Ver avaliações no Google" apontam para esses perfis. **Só publique depois dos itens 1 a 4**, ou remova os links de `lib/site.ts` (`perfilGoogle`) até lá.

### Título profissional, registro e atuação (decisões da Dra. em 07/11/2026)
- O site usa **"Dra. Nayara Esmaile"** sempre que o nome aparece, por decisão dela. Com a categoria "Médico" ainda nos perfis do Google, o título pode sugerir formação médica: trocar a categoria (bloqueador 3) fica ainda mais importante.
- **Não há menção à profissão nem ao registro no conselho no site**, por decisão dela. O número fica guardado em `lib/site.ts` (`mostrarRegistro: false`). Risco: o pedido original exigia o registro na página para dar credibilidade à revisão do Google, e conselhos profissionais costumam exigir nome e número de registro em toda publicidade. **Confirmar com o CRBio-02** se o número precisa aparecer; se precisar, basta exibir de novo.
- Formação exibida: formada pela UFRJ e pós-graduada em Saúde Estética e Procedimentos Injetáveis (texto dela).
- A atuação de biólogos em procedimentos injetáveis estéticos é tema de disputa regulatória entre conselhos. Confirme com o CRBio-02 o que a regulamentação vigente permite anunciar.

### Outras decisões da Dra. (07/11/2026)
| Decisão | O que mudou | Atenção |
|---|---|---|
| Não usar a palavra "avaliação" | Trocada por "consulta" ou "consulta avaliativa" em todo o site, inclusive título, metatags e páginas legais. Os comentários do Google viraram "comentários". | **O anúncio e as palavras-chave precisam acompanhar**: se o anúncio disser "avaliação facial" e a página "consulta avaliativa", o Google pode ver incoerência entre anúncio e página. |
| Unidades Tijuca e Barra da Tijuca | "Vila Isabel" virou "Tijuca" | O endereço da Tijuca está como `[PREENCHER]`. O perfil do Google ligado a essa unidade ainda se chama Vila Isabel. |
| Contato só pelo WhatsApp | Formulário, página `/obrigado`, ligação e Web3Forms removidos. Uma única conversão (clique no WhatsApp) | O site não coleta dados pessoais. Os dados passam a ser tratados na conversa do WhatsApp (Política de Privacidade atualizada). |
| Sem frisar "decidir depois" | Saíram a faixa "levar as informações para casa", o item "Tempo para decidir", "sem compromisso" da faixa e da descrição do Google, e o "você decide" das etapas | A informação ficou só na última pergunta do FAQ, como pedido. Continua sem urgência, desconto ou pressão: a venda segue ética. |
| Sem galeria "Conheça a clínica" (07/11) | Seção removida. As outras fotos (topo, retrato, locais) continuam | — |
| Os locais não são dela (07/11) | "Unidades" virou "locais de atendimento" em todo o site; botões "Agendar na Tijuca" / "Agendar na Barra da Tijuca"; saiu o selo "Unidade nova" e a palavra "clínica" | Nos perfis do Google, conferir se o nome e a descrição não sugerem clínica própria. |
| Foto do topo com seringa (07/11) | `hero.jpg` = retrato da Dra. segurando uma seringa, a pedido dela ("o site aprovado antes usava essa foto") | **Risco alto.** Contraria a regra "sem agulhas, seringas ou frascos" deste projeto, e seringa em destaque é um sinal típico de "medicamentos restritos", um dos motivos das reprovações. Uma aprovação antiga não garante a próxima. Se o anúncio for reprovado de novo, **trocar esta foto é a primeira coisa a fazer**: o retrato `profissional-nayara.jpg` ou uma versão recortada sem a seringa. |
| Profissional autônoma, sem CNPJ (08/11) | Saíram razão social e CNPJ. Identificação: "Dra. Nayara Esmaile, profissional autônoma" + e-mail esmaile.nayara@gmail.com + WhatsApp | Menos dados de identificação do que o pedido original previa. Nome, contato e endereço do prédio continuam visíveis. |
| Endereço só do prédio, sem horários (08/11) | Mostra rua, número e nome do prédio; sala, bloco e horários vão pelo WhatsApp | — |
| Perfis do Google sem mudanças (08/11) | A Dra. decidiu não alterar nome, categoria e postagens dos perfis: o anúncio não está vinculado a eles e a revisão olha a página de destino | Correto se a campanha **não usar recursos de local** (endereço/perfil vinculado). A página tem botões que levam aos perfis; o revisor pode seguir links, então o risco é menor, mas existe. |
| Botões para o Google nos depoimentos (08/11) | Dois botões para o mesmo perfil (o de mais avaliações): "Ver depoimentos" e "Ver fotos" | A Dra. sugeriu um botão "resultados". Usamos "depoimentos e fotos": a palavra "resultados" na página de destino soa como alegação de eficácia, que é o que o Google mais reprova em saúde. |
| Mapa já aberto (08/11) | O mapa do Google aparece direto (carrega ao rolar até ele), sem o botão "Mostrar no mapa" | Deixa o site um pouco mais pesado e o Google pode gravar cookies sem a pessoa pedir; isso foi incluído na Política de Privacidade. |
| 5 estrelas nos depoimentos (08/11) | Cinco estrelas abaixo de "Veja os depoimentos e as fotos publicados no Google", sem contagem | É a nota real do perfil (5,0 com 89 avaliações em 08/11/2026). **Se a nota cair, atualizar ou remover**, senão vira informação falsa. Não foi colocada nota nos dados estruturados (o Google proíbe nota do próprio site ali). |
| Depoimentos escolhidos pela Dra. (08/11) | Karla Luiza Pascual, Juscelia Silva e Ana Lívia Carvalho, com 5 estrelas e o nome | No da Juscelia, o trecho que citava a marca foi trocado por "(…)". |
| Instagram no rodapé (08/11) | Link discreto para @nayaraesmaile na coluna Contato | O perfil tem posts com marca e antes e depois; fica no rodapé, longe dos botões principais. |
| "Mais de 500 pacientes" (08/11) | Número informado pela Dra., no texto "Sobre a Dra." | Usado "atendidas/atendeu" em vez de "satisfeitas": número de atendimentos é comprovável; satisfação não. Precisa ser verdadeiro e atualizado. |
| "apenas" fora do aviso | Aviso agora: "Todo procedimento é indicado após consulta individual com a profissional. Os resultados variam de pessoa para pessoa." | — |

---

## Pedidos da clínica: o que entrou e o que ficou de fora

| Pedido | Decisão | Por quê |
|---|---|---|
| Visual inspirado no BHR Center | **Entrou**: hero com foto de fundo, cabeçalho em pílula, títulos em duas cores, faixa de fatos, etapas 01/02/03, faixa "nosso compromisso" | Do site de referência ficaram **de fora** o pop-up de desconto, a lista de marcas de produtos, o vídeo em autoplay e os preços. Os quatro reprovariam aqui. |
| Marrom e bege | **Entrou** | Paleta em `app/globals.css`, com contraste AA conferido. |
| Perguntas e respostas sobre procedimentos | **Entrou** (seção "Dúvidas sobre cada procedimento") | Nomes genéricos ("linhas de expressão", "preenchimento facial", "bioestimulação de colágeno"), sem marca nem princípio ativo, sem prazo de duração nem "não dói". Toda resposta remete à avaliação. Fica oculto até ela confirmar cada procedimento. |
| Mapa | **Entrou** | O mapa do Google só carrega no clique: não pesa no carregamento e não grava cookie do Google antes de a pessoa pedir. |
| Avaliações do Google | **Entrou, com filtro** | Comentários reais, copiados ao pé da letra, **só sobre atendimento**. Sem estrelas, nota média ou contagem. Ficaram de fora os que falam de resultado ("bem reduzida", "amei meus resultados") e o que cita marca. |
| Depoimentos de pacientes | **Atendido pela seção de avaliações do Google** | Depoimento sobre resultado conta como alegação de eficácia em saúde e é motivo frequente de reprovação. Se houver depoimentos fora do Google, o mesmo filtro vale, com autorização escrita da paciente. |
| Fotos de antes e depois | **Não entrou** | Foi um dos motivos das reprovações. Também tende a ser restrito pelos conselhos profissionais. Recomendação: deixar no Instagram, que **não** é linkado nesta página nem nos anúncios. |

---

## Regras atendidas na página

| Regra | Como foi atendida | Onde |
|---|---|---|
| Sem nomes de medicamentos/marcas nem princípio ativo como chamariz | Só termos neutros ("consulta avaliativa", "harmonização facial", "rejuvenescimento facial", "bioestimulação", "procedimentos injetáveis, indicados apenas após avaliação individual"), centralizados | `lib/terms.ts` |
| Sem promessas ou garantias | Nenhuma promessa de resultado. O texto fala de conversa, consulta e explicação de opções | `lib/terms.ts`, `lib/conteudo.ts` |
| Sem superlativos ou autopromoção comparativa | Nenhum "melhor", "referência" ou "número 1". Sem formulário no site | todo o site; ver grep abaixo |
| Sem preço, promoção, cupom, urgência ou contagem regressiva | Não há valores. O FAQ diz só que a consulta avaliativa é paga e o valor é informado no agendamento (transparência sem preço) | `lib/conteudo.ts` (FAQ) |
| Sem antes e depois, procedimento, agulhas, frascos ou corpo exposto | **Exceção decidida pela Dra.: a foto do topo mostra uma seringa** (ver "Outras decisões"). As demais fotos são de ambiente e da profissional. Cada `PhotoSlot` descreve a foto permitida | `components/PhotoSlot.tsx`, `lib/conteudo.ts` (GALERIA), README |
| Sem explorar insegurança | Sem perguntas do tipo "incomodada com…?", sem "acabe com", sem foco em defeitos | textos |
| Sem depoimentos de resultado, notas ou números inventados | Sem contagem de pacientes ou anos de experiência. Estrelas só a nota real do Google, por decisão da Dra. (ver "Outras decisões"). As avaliações exibidas são comentários reais do Google, só sobre atendimento, e ficam ocultas até o nome da autora ser preenchido. O JSON-LD não tem `aggregateRating` | `lib/procedimentos.ts`, `components/Procedimentos.tsx`, `components/JsonLd.tsx` |
| Perguntas sobre procedimentos sem promessa | Respostas padronizadas para duração ("varia de pessoa para pessoa"), sensação e contraindicação (remetem à avaliação). Aviso de resultados em cada aba | `lib/procedimentos.ts` |
| Sem alegações de saúde, cura ou diagnóstico | O texto fala de estética e consulta. Os Termos dizem que o conteúdo é informativo | `app/termos-de-uso` |
| Aviso de resultados individuais visível no rodapé e perto do agendamento | Texto exato em `AVISO_RESULTADOS`, exibido no hero, na seção de agendamento, em cada aba de procedimento e no rodapé | `lib/terms.ts` |
| Tom sóbrio, frases curtas | Revisado em todas as seções | — |
| Identificação do negócio | Nome da profissional (autônoma), endereço do prédio de cada local e WhatsApp no rodapé e nos cards; e-mail nas páginas legais. Sem CNPJ e sem horários, por decisão da Dra. | `components/Footer.tsx`, `components/Unidades.tsx` |
| Profissional responsável com formação | "Sobre a Dra." com formação + "Responsável técnica" no rodapé. **Registro no conselho oculto por decisão da Dra.** (ver acima) | `components/Secoes.tsx`, `components/Footer.tsx` |
| Política de Privacidade (LGPD) e Termos de Uso no rodapé | Textos-base completos com trechos `[PREENCHER]` | `app/politica-de-privacidade`, `app/termos-de-uso` |
| Sem pop-ups, redirecionamentos, autoplay, botões enganosos ou rolagem infinita | Nenhum modal, mesmo com o visual da referência (que tem pop-up de desconto). Mapa carrega ao rolar até ele. O aviso de cookies é uma faixa discreta que não bloqueia a página. Não há vídeo/áudio. O WhatsApp abre só no clique | — |
| Cookies só com o necessário | Duas opções (Recusar/Aceitar). Consent Mode v2 começa negado. Link "Preferências de cookies" no rodapé | `components/CookieBanner.tsx`, `lib/gtag.ts` |
| Conteúdo bate com o anúncio | Foco único: consulta avaliativa + agendamento pelo WhatsApp. H1 = "Consulta avaliativa individualizada na Tijuca e na Barra da Tijuca" | `lib/terms.ts` (HERO) |
| Metatags honestas, canonical, robots, sitemap | `title`, `description`, `og`, `canonical` por página. `robots.txt` libera tudo. `sitemap.xml` com as 3 páginas públicas | `app/layout.tsx`, `app/robots.ts`, `app/sitemap.ts` |
| HTTPS | Automático na Vercel/Cloudflare | README |
| Coleta mínima de dados | Não há formulário: o site não pede nenhum dado pessoal. O contato é só pelo WhatsApp | `components/Contato.tsx` |
| gtag com ID por variável e conversão | `NEXT_PUBLIC_GADS_ID`. Uma conversão: clique em qualquer botão do WhatsApp (`data-conv="whatsapp"`) | `components/Analytics.tsx`, `lib/gtag.ts` |
| Sem remarketing ou públicos | `allow_ad_personalization_signals: false`, `ad_personalization: 'denied'` fixo, `allow_google_signals: false`, sem tag de remarketing | `lib/gtag.ts`, `components/Analytics.tsx` |
| WhatsApp com mensagem pré-preenchida neutra | "Olá! Gostaria de agendar uma consulta na unidade [unidade]." | `lib/terms.ts` |
| Só afirmar o que for verdade | Afirmações sobre biossegurança, Anvisa, consentimento etc. ficam com `confirmado: false` e **não vão ao ar** até ela confirmar | `lib/conteudo.ts` |
| Acessibilidade | `lang="pt-BR"`, HTML semântico, skip-link, foco visível, botões ≥ 48 px, corpo de 17 px, contraste AA | todo o site |

---

## Antes de publicar
- [ ] Resolver os **bloqueadores 1 a 5** dos perfis do Google (nome, descrição, postagens, categoria, site).
- [ ] Revisar textos e título profissional com o **CRBio-02** (o que pode ser anunciado e como).
- [ ] Conferir que **anúncios, palavras-chave, recursos (sitelinks, frases de destaque, snippets), nomes de campanha/grupo e URLs** não usam nomes de medicamentos ou marcas. Incluir essas marcas como **palavras-chave negativas**.
- [ ] Desvincular recursos de local se os perfis ainda não tiverem sido renomeados.
- [ ] Não usar o Instagram como sitelink ou recurso.
- [ ] Texto do anúncio coerente com a página: "consulta avaliativa" (não "avaliação"), unidades Tijuca e Barra da Tijuca, agendamento pelo WhatsApp. Sem preço, promoção ou urgência.
- [ ] Preencher todos os itens de PLACEHOLDERS.md (CNPJ e endereços **precisam** aparecer; placeholder no ar parece site inacabado).
- [ ] Confirmar (ou deixar ocultos) os itens de `lib/conteudo.ts` e os procedimentos/avaliações de `lib/procedimentos.ts`.
- [ ] Conferir que `NEXT_PUBLIC_MOSTRAR_RASCUNHO` está **vazia** no deploy oficial.
- [ ] Revisar a Política de Privacidade e os Termos com advogado(a).
- [ ] Deploy feito, domínio próprio com HTTPS, página abrindo no celular, todos os botões do WhatsApp testados.
- [ ] Rodar o grep de termos proibidos (comando abaixo) depois de qualquer edição de texto.
- [ ] **Só então** enviar a campanha para revisão (a página precisa estar no ar e funcionando).
- [ ] Se reprovar de novo: copiar o **texto exato** da política citada e de qual item (anúncio, palavra-chave, recurso ou destino) para analisar o caso.

### Grep de termos proibidos
```bash
grep -rniE "botox|dysport|xeomin|botulift|radiesse|sculptra|juvederm|restylane|toxina|botul|garantid|melhor|promo[cç][aã]o|antes e depois|R\\$|100%|definitiv|sem dor|sem risco|milagre|desconto|cupom|brinde|últimas vagas|\\breferência\\b|número 1" app components lib public
```
Deve voltar só com dois achados esperados: `100%` em `components/Procedimentos.tsx` (é o degradê das estrelas, não texto) e `melhor` em `lib/procedimentos.ts` (está no depoimento da Karla, "o que já temos de melhor", que são palavras da paciente sobre si mesma, não superlativo sobre a clínica). Os arquivos `.md` ficam de fora porque citam os termos justamente para proibi-los.
