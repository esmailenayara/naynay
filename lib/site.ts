/**
 * DADOS DO NEGÓCIO — único lugar para preencher informações do atendimento.
 * A Dra. atende em dois locais que não são dela: no site, falar "locais de atendimento", nunca "unidades" ou "clínica própria".
 * Decisão da Dra.: ela é profissional autônoma (sem CNPJ). O site mostra o endereço do prédio,
 * sem sala nem bloco; sala, bloco e horários são passados pelo WhatsApp. Ver COMPLIANCE.md.
 */

export const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000").replace(/\/$/, "");

export const CLINICA = {
  nome: "Dra. Nayara Esmaile",
  descritor: "Harmonização Facial e Estética Avançada",
  // Identificação usada nas páginas legais (controladora dos dados, LGPD).
  // Sem "responsável técnica" nem "profissional autônoma" no site (pedido da Dra.).
  responsavelLegal: "Nayara Esmaile",
  email: "esmaile.nayara@gmail.com",
};

// Data exibida em "Última atualização" das páginas legais. Atualize ao mudar o texto delas.
export const ATUALIZACAO_LEGAL = "8 de novembro de 2026";

export const PROFISSIONAL = {
  // Decisão da Dra.: usar "Dra." sempre antes do nome (ver COMPLIANCE.md, "Título profissional").
  tratamento: "Dra.",
  nome: "Nayara Esmaile",
  // Registro no conselho guardado aqui, mas NÃO exibido no site por decisão da Dra.
  conselho: "CRBio-02",
  registro: "[PREENCHER: nº do registro]",
  mostrarRegistro: false,
  formacao: [
    "Formada pela Universidade Federal do Rio de Janeiro (UFRJ)",
    "Pós-graduada em Saúde Estética e Procedimentos Injetáveis",
  ],
};

export const nomeProfissional = () =>
  [PROFISSIONAL.tratamento, PROFISSIONAL.nome].filter(Boolean).join(" ");

// Um único WhatsApp para os dois locais de atendimento. O contato é feito só por ele (sem formulário e sem ligação).
export const CONTATO = {
  whatsapp: "5521990645009",
  whatsappExibicao: "(21) 99064-5009",
  // Só no rodapé, discreto: o foco da página é o agendamento pelo WhatsApp.
  instagram: "https://www.instagram.com/nayaraesmaile/",
  instagramExibicao: "@nayaraesmaile",
};

export type LocalId = "tijuca" | "barra";

export type LocalAtendimento = {
  id: LocalId;
  bairro: string;
  // Bairro com preposição, para frases como "Agendar na Tijuca".
  prep: string;
  // Endereço do prédio, sem sala nem bloco.
  endereco: string;
  predio: string;
  // Link público do perfil no Google (depoimentos e fotos). Sem nota ou contagem na página.
  perfilGoogle: string;
};

// Perfil do Google com mais avaliações (89): destino dos botões de depoimentos e fotos.
// Link direto do Google Maps pelo ID do lugar (cid). O link curto share.google abria só uma pesquisa em alguns aparelhos.
export const PERFIL_GOOGLE = "https://maps.google.com/?cid=11602936485510843382";

export const LOCAIS: LocalAtendimento[] = [
  {
    id: "tijuca",
    bairro: "Tijuca",
    prep: "na Tijuca",
    endereco: "Rua Conde de Bonfim, 497",
    predio: "Tijuca Blue Offices",
    perfilGoogle: "https://share.google/EGu5jMONU8ltQHMoQ",
  },
  {
    id: "barra",
    bairro: "Barra da Tijuca",
    prep: "na Barra da Tijuca",
    endereco: "Av. João Cabral de Mello Neto, 850",
    predio: "CEO Corporate Executive Offices",
    perfilGoogle: "https://share.google/gv2PRy78WjbhDRmYA",
  },
];

export const enderecoCompleto = (u: LocalAtendimento) =>
  `${u.endereco} — ${u.predio} · ${u.bairro}, Rio de Janeiro — RJ`;

export const enderecoMapa = (u: LocalAtendimento) => `${u.endereco}, ${u.bairro}, Rio de Janeiro - RJ`;

export const linkComoChegar = (u: LocalAtendimento) =>
  `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(enderecoMapa(u))}`;

export function linkWhatsApp(mensagem: string) {
  return `https://wa.me/${CONTATO.whatsapp}?text=${encodeURIComponent(mensagem)}`;
}
