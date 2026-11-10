import { CONTATO, LOCAIS, linkWhatsApp } from "@/lib/site";
import { AVISO_RESULTADOS, MENSAGEM_WHATSAPP_PADRAO } from "@/lib/terms";
import { ButtonLink } from "./Button";
import { IconWhatsApp } from "./Icons";
import { Titulo } from "./Section";

/** Agendamento só pelo WhatsApp: sem formulário, sem ligação. */
export function Contato() {
  return (
    <section id="agendar" aria-labelledby="agendar-titulo" className="bg-bg">
      <div className="mx-auto max-w-6xl px-4 py-20 sm:px-6 md:py-28">
        <div className="grid items-center gap-10 rounded-[1.75rem] bg-surface p-6 shadow-[0_20px_50px_rgba(47,36,30,0.08)] ring-1 ring-line sm:p-10 md:grid-cols-[1.2fr_1fr] md:gap-16 md:p-14">
          <div>
            <Titulo id="agendar-titulo" kicker="Agendamento" titulo="Agende sua consulta" destaque="pelo WhatsApp." />
            <p className="mt-5 max-w-xl text-lg text-ink-soft">
              No WhatsApp, nossa equipe faz um atendimento humanizado, tira todas as suas dúvidas e agenda a consulta no
              local de sua preferência.
            </p>
            <p className="mt-8 border-l-2 border-accent pl-4 text-sm text-ink-soft">{AVISO_RESULTADOS}</p>
          </div>
          <div className="grid gap-3">
            <ButtonLink
              href={linkWhatsApp(MENSAGEM_WHATSAPP_PADRAO)}
              externo
              data-conv="whatsapp"
              className="min-h-14 text-base"
              aria-label="Agendar pelo WhatsApp (abre em nova aba)"
            >
              <IconWhatsApp /> Agendar pelo WhatsApp
            </ButtonLink>
            {LOCAIS.map((u) => (
              <ButtonLink
                key={u.id}
                href={linkWhatsApp(MENSAGEM_WHATSAPP_PADRAO)}
                externo
                data-conv="whatsapp"
                aria-label={`Agendar ${u.prep} pelo WhatsApp (abre em nova aba)`}
              >
                Agendar {u.prep}
              </ButtonLink>
            ))}
            <p className="mt-2 text-center text-sm text-ink-soft">WhatsApp {CONTATO.whatsappExibicao}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
