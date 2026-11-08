/**
 * PROCEDIMENTOS — perguntas e respostas.
 *
 * Regras (ver COMPLIANCE.md): nenhum nome de marca, medicamento ou princípio ativo;
 * nenhuma promessa de resultado ou de duração, nem frase sobre ausência de dor; nenhuma alegação de
 * tratar doença. Toda resposta remete à consulta individual. Não usar a palavra "avaliação".
 *
 * `confirmado: false` = some do site publicado até ela confirmar que oferece o
 * procedimento e que o texto está correto.
 */

export type Procedimento = {
  id: string;
  nome: string;
  resumo: string;
  perguntas: { pergunta: string; resposta: string }[];
  confirmado: boolean;
};

const DURACAO =
  "Varia de pessoa para pessoa, conforme o organismo, a técnica usada e os cuidados depois do procedimento. A profissional explica o que esperar no seu caso durante a consulta.";
const SENSACAO =
  "A sensação varia de pessoa para pessoa. Na consulta, a profissional explica como o procedimento é feito e quais recursos de conforto podem ser usados.";
const QUEM_NAO_PODE =
  "Existem situações em que o procedimento não é indicado. Por isso a consulta individual vem sempre antes de qualquer indicação.";

export const PROCEDIMENTOS: Procedimento[] = [
  {
    id: "harmonizacao",
    nome: "Harmonização facial",
    resumo:
      "Conjunto de técnicas planejadas para equilibrar as proporções do rosto, respeitando as características de cada pessoa. O plano é montado depois da consulta e pode envolver uma ou mais etapas.",
    perguntas: [
      {
        pergunta: "A harmonização muda a minha aparência?",
        resposta:
          "O objetivo é trabalhar proporções e equilíbrio, respeitando os traços de cada pessoa. O que é possível e o que não é indicado no seu caso é conversado na consulta.",
      },
      { pergunta: "É feita em uma sessão só?", resposta: "Depende do plano definido na consulta. Algumas pessoas fazem em etapas, com intervalos entre elas." },
      { pergunta: "Quem não pode fazer?", resposta: QUEM_NAO_PODE },
    ],
    confirmado: true,
  },
  {
    id: "linhas",
    nome: "Linhas de expressão",
    resumo:
      "Procedimento injetável para suavizar linhas formadas pelo movimento do rosto, como as da testa e ao redor dos olhos. A indicação, as áreas e a quantidade são definidas na consulta.",
    perguntas: [
      { pergunta: "Quanto tempo dura?", resposta: DURACAO },
      { pergunta: "Dói?", resposta: SENSACAO },
      {
        pergunta: "Posso voltar à rotina no mesmo dia?",
        resposta: "Em geral, sim, com alguns cuidados nas primeiras horas. As orientações completas são passadas no dia do atendimento.",
      },
      { pergunta: "Quem não pode fazer?", resposta: QUEM_NAO_PODE },
    ],
    confirmado: true,
  },
  {
    id: "preenchimento",
    nome: "Preenchimento facial",
    resumo:
      "Reposição de volume ou definição de contornos em áreas específicas do rosto, como lábios, olheiras, malar e mandíbula. Produto, área e quantidade são indicados após a consulta.",
    perguntas: [
      { pergunta: "Quanto tempo dura?", resposta: DURACAO },
      { pergunta: "Fica com aspecto artificial?", resposta: "O planejamento busca respeitar as proporções do seu rosto. Expectativas e limites são conversados com franqueza na consulta." },
      {
        pergunta: "Fica roxo ou inchado?",
        resposta: "Pode haver inchaço ou pequenas manchas roxas nos primeiros dias, que variam de pessoa para pessoa. Os cuidados são explicados no atendimento.",
      },
      { pergunta: "Quem não pode fazer?", resposta: QUEM_NAO_PODE },
    ],
    confirmado: true,
  },
  {
    id: "bioestimulacao",
    nome: "Bioestimulação de colágeno",
    resumo:
      "Técnicas que estimulam a pele a produzir o próprio colágeno ao longo das semanas seguintes. O número de sessões e o intervalo entre elas são definidos na consulta.",
    perguntas: [
      { pergunta: "Quando dá para perceber diferença?", resposta: "A resposta é gradual e varia de pessoa para pessoa. A profissional explica o que esperar no seu caso." },
      { pergunta: "Quantas sessões são necessárias?", resposta: "Depende do estado da sua pele e dos seus objetivos. Não existe um número fixo para todo mundo." },
      { pergunta: "Quem não pode fazer?", resposta: QUEM_NAO_PODE },
    ],
    confirmado: true,
  },
  {
    id: "pele",
    nome: "Qualidade da pele",
    resumo:
      "Procedimentos voltados à hidratação, ao viço e à textura da pele do rosto, combinados ou não com cuidados em casa. A escolha depende do que for observado na consulta.",
    perguntas: [
      { pergunta: "Precisa de manutenção?", resposta: "Geralmente sim. A frequência é combinada de acordo com a consulta e com a resposta da sua pele." },
      { pergunta: "Posso fazer junto com outros procedimentos?", resposta: "Em alguns casos, sim. A combinação e a ordem são definidas pela profissional na consulta." },
    ],
    confirmado: true,
  },
];

/**
 * COMENTÁRIOS DO GOOGLE — copiadas literalmente dos perfis públicos.
 *
 * Critério: só entram comentários sobre ATENDIMENTO (cuidado, ambiente, atenção).
 * Ficam de fora os que falam de resultado ("ficou natural", "reduziu") ou citam
 * marca de produto — isso é o que a revisão do Google reprova em saúde.
 * Nada de estrelas, nota média ou número de comentários.
 * Preencha o nome exatamente como aparece no Google e troque `confirmado` para true.
 */
export const COMENTARIOS = [
  // Avaliações escolhidas e enviadas pela Dra. em 08/11/2026. "(…)" marca trecho omitido.
  {
    // Enviada pela Dra. (texto completo, sem os emojis).
    texto:
      "É tão bom encontrar uma profissional que entende que cuidar da gente não significa mudar quem somos. A Dra. Nayara tem esse olhar especial: competência, precisão e, acima de tudo, respeito pela nossa naturalidade. Cada procedimento é feito com muito bom senso, sem exageros e sempre valorizando o que já temos de melhor. Obrigada, Dra. Nayara, por cuidar de mim com tanto profissionalismo e delicadeza.",
    autor: "Karla Luiza Pascual",
    local: "",
    confirmado: true,
  },
  {
    // Enviada pela Dra. O trecho com nomes de procedimentos/marca foi trocado por "(…)" (regra do Google Ads).
    texto:
      "Procurei muito uma profissional confiável que eu pudesse fazer meus procedimentos na Barra. (…) Fiquei muito satisfeita com o atendimento. Ela foi cuidadosa em cada detalhe, especialmente no pós, me acompanhou e tirou todas as dúvidas. Deixo a minha recomendação e voltarei em breve para dar continuidade ao tratamento.",
    autor: "Juscelia Silva",
    local: "Barra da Tijuca",
    confirmado: true,
  },
  {
    // Enviada pela Dra. (texto completo).
    texto:
      "Eu buscava uma profissional ética, segura, competente pra criar um vínculo de cuidado. Me surpreendi com o olhar atento, a escuta ativa e o manejo sensível no tratamento. Encontrei tudo isso na Dra Nayara. Eu a recomendo com satisfação.",
    autor: "Ana Lívia Carvalho",
    local: "",
    confirmado: true,
  },
];
