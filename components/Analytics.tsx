"use client";

import Script from "next/script";
import { useEffect } from "react";
import { GADS_ID, aplicarConsentimento, lerConsentimento, registrarConversao } from "@/lib/gtag";

/**
 * Carrega o gtag.js só se NEXT_PUBLIC_GADS_ID estiver definido.
 * Consent Mode v2 começa tudo negado; o banner de cookies libera ad_storage.
 * Cliques em links com data-conv="whatsapp" viram conversão (único canal de contato do site).
 */
export function Analytics() {
  useEffect(() => {
    if (!GADS_ID) return;
    const salvo = lerConsentimento();
    if (salvo) aplicarConsentimento(salvo);

    const onClick = (e: MouseEvent) => {
      const alvo = (e.target as HTMLElement | null)?.closest<HTMLElement>("[data-conv]");
      const tipo = alvo?.dataset.conv;
      if (tipo === "whatsapp") registrarConversao(tipo);
    };
    document.addEventListener("click", onClick);
    return () => document.removeEventListener("click", onClick);
  }, []);

  if (!GADS_ID) return null;

  return (
    <>
      <Script id="gtag-consent" strategy="afterInteractive">
        {`window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',wait_for_update:500});
gtag('set','ads_data_redaction',true);
gtag('js',new Date());
gtag('config','${GADS_ID}',{allow_ad_personalization_signals:false,allow_google_signals:false});`}
      </Script>
      <Script src={`https://www.googletagmanager.com/gtag/js?id=${GADS_ID}`} strategy="afterInteractive" />
    </>
  );
}
