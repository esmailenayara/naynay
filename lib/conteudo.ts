/**
 * TEXTOS DAS SEÇÕES.
 *
 * Itens com `confirmado: false` aparecem no `npm run dev` com a etiqueta "CONFIRMAR"
 * e NÃO aparecem no site publicado (`npm run build`) até ela trocar para `true`.
 * Assim nenhuma afirmação vai ao ar sem a profissional conferir que é verdade.
 */

// NEXT_PUBLIC_MOSTRAR_RASCUNHO=1 mostra tudo também no build (útil para um link de revisão, nunca no site oficial).
export const MOSTRAR_NAO_CONFIRMADOS =
  process.env.NODE_ENV !== "production" || process.env.NEXT_PUBLIC_MOSTRAR_RASCUNHO === "1";

export type ItemConfirmavel = { titulo: string; texto: string; confirmado: boolean };

export const visiveis = <T extends { confirmado: boolean }>(itens: T[]) =>
  itens.filter((i) => i.confirmado || MOSTRAR_NAO_CONFIRMADOS);

// Faixa abaixo do hero: só fatos verificáveis, sem números ou superlativos.
export const FAIXA = [
  "Tijuca e Barra da Tijuca",
  "Atendimento com hora marcada",
  "Consulta antes de qualquer indicação",
  "Formada pela UFRJ",
  "Pós-graduada em Saúde Estética",
];

export const PASSOS = [
  {
    titulo: "Você chama no WhatsApp",
    texto:
      "Nossa equipe faz um atendimento humanizado, tira todas as suas dúvidas e agenda a consulta no local de sua preferência.",
  },
  {
    titulo: "Conversa e consulta avaliativa",
    texto:
      "Você conta o que gostaria de cuidar no rosto. A Dra. Nayara Esmaile examina com calma e responde às suas dúvidas.",
  },
  {
    titulo: "Opções explicadas",
    texto:
      "Ela explica as opções adequadas ao seu caso, com os cuidados de cada uma, e apresenta o plano indicado para você.",
  },
];

export const SOBRE = {
  // Textos enviados pela própria Dra. (já confirmados).
  paragrafos: [
    {
      texto:
        "O lema da Dra. Nayara Esmaile é naturalidade e elegância: realçar o que já é seu e cuidar, com delicadeza, dos sinais que o tempo deixou.",
      confirmado: true,
    },
  ],
};

export const EXPECTATIVAS: ItemConfirmavel[] = [
  {
    titulo: "Ambiente reservado",
    texto: "Atendimento individual, com hora marcada, em sala reservada.",
    confirmado: true,
  },
  {
    titulo: "Biossegurança",
    texto:
      "Materiais descartáveis de uso único e higienização do ambiente entre um atendimento e outro, conforme as normas da vigilância sanitária.",
    confirmado: true,
  },
  {
    titulo: "Produtos regularizados",
    texto:
      "Uso apenas de produtos com registro na Anvisa, com lote e validade anotados no seu prontuário para rastreabilidade.",
    confirmado: true,
  },
  {
    titulo: "Consulta antes de qualquer indicação",
    texto: "Nenhum procedimento é indicado sem consulta individual e sem explicação dos cuidados envolvidos.",
    confirmado: true,
  },
  {
    titulo: "Consentimento informado",
    texto: "Antes de qualquer procedimento, você lê e assina um termo com as informações do que será feito.",
    confirmado: true,
  },
];

export const FAQ = [
  {
    pergunta: "Como funciona a primeira consulta?",
    resposta:
      "Você conversa com a Dra. Nayara Esmaile sobre o que gostaria de cuidar no rosto. Em seguida, ela examina e explica as opções adequadas ao seu caso, com os cuidados de cada uma.",
  },
  {
    pergunta: "Como faço para agendar?",
    resposta:
      "Pelo WhatsApp. Nossa equipe faz um atendimento humanizado, tira todas as suas dúvidas e encontra um horário no local de sua preferência.",
  },
  {
    pergunta: "Quanto tempo dura a consulta avaliativa?",
    resposta: "Em média 45 minutos. Recomendamos chegar alguns minutos antes do horário marcado.",
  },
  {
    pergunta: "A consulta avaliativa tem custo?",
    resposta: "Sim, é uma consulta paga. O valor é informado pelo WhatsApp, antes de você confirmar o horário.",
  },
  {
    pergunta: "Posso remarcar ou cancelar?",
    resposta:
      "Sim. Basta avisar pelo WhatsApp com pelo menos 24 horas de antecedência para liberarmos o horário.",
  },
  {
    pergunta: "Em qual local devo agendar?",
    resposta:
      "No que for mais prático para você. O atendimento segue o mesmo cuidado na Tijuca e na Barra da Tijuca.",
  },
  {
    pergunta: "Como meus dados são tratados?",
    resposta:
      "Este site não pede seus dados pessoais. O contato acontece pelo WhatsApp, e o que você nos enviar lá é usado só para o seu atendimento, conforme a Política de Privacidade.",
  },
  {
    pergunta: "Preciso fazer algum procedimento depois da consulta?",
    resposta:
      "Não. Na consulta avaliativa, a Dra. Nayara Esmaile explica o que é indicado para o seu caso. Você pode levar as informações para casa e decidir depois.",
  },
];
