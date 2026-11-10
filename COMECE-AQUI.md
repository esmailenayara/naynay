# Como cuidar do seu site com o Claude Code

Esta pasta é o seu site: **dranayaraesmaile.com.br**. O Claude Code lê o arquivo `CLAUDE.md` daqui e já sabe todas as decisões que você tomou (cores, palavras, regras do Google Ads). Basta pedir em português.

## 1. Preparar o computador (só na primeira vez)

1. **Node.js**: baixe em https://nodejs.org (botão "LTS") e instale normalmente.
2. **Claude**: baixe o app em https://claude.ai/download e entre com a sua conta. O Claude Code precisa do plano Pro ou Max.
3. **A pasta do site**: descompacte o arquivo `.zip` que você recebeu e guarde a pasta `nayara-esmaile-lp` num lugar fixo, por exemplo **Documentos**. Não apague nem mude de lugar depois.

## 2. Abrir o projeto

1. No app do Claude, abra a aba **Code**.
2. Escolha a pasta `nayara-esmaile-lp` como pasta de trabalho.
3. Na primeira conversa, mande:

   > Leia o CLAUDE.md, instale o que for preciso e me mostre o site rodando no computador.

O Claude vai pedir permissão para rodar alguns comandos. Pode aceitar.

## 3. Pedir mudanças

Fale normalmente, como se fosse com uma pessoa. Exemplos:

- "Troca o texto do Sobre a Dra. por este: …"
- "Adiciona uma pergunta no FAQ: …"
- "Coloca este novo depoimento do Google: …"
- "Troca a foto do topo por esta." (arraste a foto para a conversa)
- "Me mostra como fica no celular."

O Claude mostra como ficou **antes** de colocar no ar. Quando estiver do seu jeito, diga:

> Pode publicar.

Em cerca de um minuto a mudança está no site oficial. Se o celular continuar mostrando a versão antiga, basta atualizar a página.

## 4. Primeira publicação: login na Cloudflare

Na primeira vez que publicar, vai abrir uma página da **Cloudflare** no navegador. Entre com **esmaile.nayara@gmail.com** (a conta onde o site está) e clique em **Allow**. Depois disso não precisa mais.

## 5. Bom saber

- **O Claude avisa se algo pode fazer o Google reprovar o anúncio**: nomes de produtos ou marcas, antes e depois, promessas de resultado, preços. Se ele sugerir outra palavra, é por isso.
- **Não precisa entender de código.** Se algo der errado, peça: "deu este erro, resolve" ou "volta como estava antes". O Claude guarda cada versão publicada.
- **Ainda falta fazer:**
  - Colocar o código de conversão do Google Ads. Peça ao Claude: "me guia para criar a conversão do WhatsApp no Google Ads".
  - Ligar o "Always Use HTTPS" na Cloudflare. Peça: "me guia para ligar o Always Use HTTPS".
