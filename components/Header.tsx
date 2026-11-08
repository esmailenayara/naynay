import Link from "next/link";
import { CLINICA, linkWhatsApp } from "@/lib/site";
import { MENSAGEM_WHATSAPP_PADRAO } from "@/lib/terms";
import { IconWhatsApp } from "./Icons";

/**
 * Cabeçalho fixo, sempre na mesma cor escura do topo da página (pedido da Dra.):
 * não fica transparente e não muda de cor ao rolar.
 */
export function Header({ simples = false }: { simples?: boolean }) {
  return (
    <header className="fixed inset-x-0 top-0 z-30 border-b border-white/10 bg-dark text-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-2 sm:px-6">
        <Link href="/" className="flex min-h-12 flex-col justify-center leading-none" aria-label={`${CLINICA.nome}, página inicial`}>
          <span className="whitespace-nowrap text-[0.9375rem] font-light uppercase tracking-[0.2em] sm:text-lg sm:tracking-[0.3em]">
            {CLINICA.nome}
          </span>
          <span className="mt-1.5 hidden text-[0.625rem] uppercase tracking-[0.22em] text-white/70 sm:block">{CLINICA.descritor}</span>
        </Link>
        {!simples && (
          <a
            href={linkWhatsApp(MENSAGEM_WHATSAPP_PADRAO)}
            target="_blank"
            rel="noopener noreferrer"
            data-conv="whatsapp"
            aria-label="Agendar pelo WhatsApp (abre em nova aba)"
            className="flex min-h-12 items-center gap-2 text-sm uppercase tracking-[0.18em]"
          >
            <IconWhatsApp className="size-5" />
            <span className="border-b border-white/60 pb-0.5">Agendar</span>
          </a>
        )}
      </div>
    </header>
  );
}
