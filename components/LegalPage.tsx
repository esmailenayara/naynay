import type { ReactNode } from "react";
import { Footer } from "./Footer";
import { Header } from "./Header";

export function LegalPage({ titulo, atualizado, children }: { titulo: string; atualizado: string; children: ReactNode }) {
  return (
    <>
      <Header simples />
      <main id="conteudo" className="mx-auto max-w-3xl px-4 pb-16 pt-32 sm:px-6 md:pb-24 md:pt-36">
        <h1 className="text-3xl text-ink md:text-4xl">{titulo}</h1>
        <p className="mt-2 text-sm text-ink-soft">Última atualização: {atualizado}</p>
        <div className="mt-10 space-y-4 text-ink-soft [&_a]:text-brand-strong [&_a]:underline [&_h2]:mt-10 [&_h2]:text-2xl [&_h2]:text-ink [&_li]:ml-5 [&_li]:list-disc [&_strong]:text-ink">
          {children}
        </div>
      </main>
      <Footer />
    </>
  );
}
