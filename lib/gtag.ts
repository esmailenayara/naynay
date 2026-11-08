/**
 * Google Ads — somente medição de conversão.
 * Remarketing e personalização ficam DESLIGADOS de propósito (saúde é categoria
 * sensível; ver COMPLIANCE.md). Não altere ad_personalization nem
 * allow_ad_personalization_signals.
 */

export const GADS_ID = process.env.NEXT_PUBLIC_GADS_ID || "";

// O contato é só por WhatsApp, então há uma única conversão.
export const CONVERSOES = {
  whatsapp: process.env.NEXT_PUBLIC_GADS_CONV_WHATSAPP || "",
};

export type TipoConversao = keyof typeof CONVERSOES;

const CHAVE_CONSENTIMENTO = "consentimento-cookies";
export type Consentimento = "aceito" | "recusado";

type Gtag = (...args: unknown[]) => void;
const gtag = (): Gtag | undefined =>
  typeof window !== "undefined" ? (window as unknown as { gtag?: Gtag }).gtag : undefined;

export function lerConsentimento(): Consentimento | null {
  try {
    const v = localStorage.getItem(CHAVE_CONSENTIMENTO);
    return v === "aceito" || v === "recusado" ? v : null;
  } catch {
    return null;
  }
}

export function salvarConsentimento(v: Consentimento) {
  try {
    localStorage.setItem(CHAVE_CONSENTIMENTO, v);
  } catch {}
  aplicarConsentimento(v);
}

export function aplicarConsentimento(v: Consentimento) {
  gtag()?.("consent", "update", {
    ad_storage: v === "aceito" ? "granted" : "denied",
    ad_user_data: v === "aceito" ? "granted" : "denied",
    // Sempre negado: sem remarketing/personalização.
    ad_personalization: "denied",
    analytics_storage: "denied",
  });
}

export function registrarConversao(tipo: TipoConversao) {
  const sendTo = CONVERSOES[tipo];
  if (!sendTo) return;
  gtag()?.("event", "conversion", { send_to: sendTo });
}
