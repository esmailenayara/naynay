"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { lerConsentimento, salvarConsentimento, type Consentimento } from "@/lib/gtag";

export const EVENTO_ABRIR_COOKIES = "abrir-preferencias-cookies";

/** Faixa discreta, não bloqueia a página. Some depois da escolha. */
export function CookieBanner() {
  const [aberto, setAberto] = useState(false);

  useEffect(() => {
    if (!lerConsentimento()) setAberto(true);
    const abrir = () => setAberto(true);
    window.addEventListener(EVENTO_ABRIR_COOKIES, abrir);
    return () => window.removeEventListener(EVENTO_ABRIR_COOKIES, abrir);
  }, []);

  if (!aberto) return null;

  const escolher = (v: Consentimento) => {
    salvarConsentimento(v);
    setAberto(false);
  };

  return (
    <div
      role="region"
      aria-label="Aviso de cookies"
      className="fixed inset-x-3 bottom-[5.25rem] z-40 mx-auto max-w-lg rounded-2xl border border-line bg-surface px-4 py-3 text-sm shadow-lg md:bottom-4"
    >
      <p className="text-ink-soft">
        Usamos cookies necessários e, se você permitir, um do Google para medir agendamentos. Sem remarketing.{" "}
        <Link href="/politica-de-privacidade/#cookies" className="font-medium text-brand-strong underline underline-offset-2">
          Saiba mais
        </Link>
      </p>
      <div className="mt-2 flex gap-2">
        <button
          type="button"
          onClick={() => escolher("recusado")}
          className="min-h-12 flex-1 rounded-full border border-line px-4 font-medium text-ink hover:bg-bg-soft"
        >
          Recusar
        </button>
        <button
          type="button"
          onClick={() => escolher("aceito")}
          className="min-h-12 flex-1 rounded-full bg-botao px-4 font-medium text-white hover:bg-botao-hover"
        >
          Aceitar
        </button>
      </div>
    </div>
  );
}
