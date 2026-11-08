/**
 * TERMOS E TEXTOS SENSÍVEIS — centralizados aqui para ajuste sem mexer nos componentes.
 *
 * Regra: nenhum nome de medicamento, marca ou princípio ativo. Nada de promessa,
 * superlativo, preço ou urgência. Antes de trocar qualquer texto, confira COMPLIANCE.md.
 * O site usa "consulta" / "consulta avaliativa" (não usar a palavra "avaliação" no site).
 */

export const TERMOS = {
  foco: "consulta avaliativa",
  areas: [
    "Harmonização facial",
    "Rejuvenescimento facial",
    "Bioestimulação",
    "Cuidados com a pele do rosto",
  ],
};

export const AVISO_RESULTADOS =
  "Todo procedimento é indicado após consulta individual com a profissional. Os resultados variam de pessoa para pessoa.";

export const HERO = {
  // O título aparece em duas linhas: `titulo` (branco) e `destaque` (caramelo).
  titulo: "Consulta avaliativa individualizada",
  destaque: "na Tijuca e na Barra da Tijuca.",
  subtitulo:
    "Harmonização facial e estética avançada com a Dra. Nayara Esmaile. Uma consulta dedicada a entender o seu rosto e indicar o tratamento adequado para você.",
};

export const SEO = {
  titulo: "Consulta avaliativa facial na Tijuca e na Barra da Tijuca | Dra. Nayara Esmaile",
  descricao:
    "Agende pelo WhatsApp sua consulta avaliativa com a Dra. Nayara Esmaile, com atendimento na Tijuca e na Barra da Tijuca, no Rio de Janeiro. Harmonização facial com naturalidade e elegância.",
};

export const MENSAGEM_WHATSAPP_PADRAO = "Olá! Gostaria de agendar uma consulta.";

// `prep` = bairro com preposição, ex.: "na Tijuca".
export const mensagemWhatsAppLocal = (prep: string) => `Olá! Gostaria de agendar uma consulta ${prep}.`;
