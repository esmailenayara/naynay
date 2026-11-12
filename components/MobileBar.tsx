import { linkWhatsApp } from "@/lib/site";
import { MENSAGEM_WHATSAPP_PADRAO } from "@/lib/terms";
import { IconWhatsApp } from "./Icons";

/** Barra fixa no rodapé, só no celular. O contato é só pelo WhatsApp; o texto combina com a mensagem pronta ("tirar dúvidas"). */
export function MobileBar() {
  return (
    <nav
      aria-label="Agendamento"
      className="fixed inset-x-0 bottom-0 z-30 border-t border-line bg-surface/95 p-2.5 pb-[max(0.625rem,env(safe-area-inset-bottom))] backdrop-blur md:hidden"
    >
      <a
        href={linkWhatsApp(MENSAGEM_WHATSAPP_PADRAO)}
        target="_blank"
        rel="noopener noreferrer"
        data-conv="whatsapp"
        className="flex min-h-12 items-center justify-center gap-2 rounded-full bg-botao font-medium text-white"
      >
        <IconWhatsApp /> Tirar dúvidas pelo WhatsApp
      </a>
    </nav>
  );
}
