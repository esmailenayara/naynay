import { LOCAIS, enderecoMapa, linkComoChegar, linkWhatsApp } from "@/lib/site";
import { mensagemWhatsAppLocal } from "@/lib/terms";
import { ButtonLink } from "./Button";
import { IconPin, IconWhatsApp } from "./Icons";
import { Mapa } from "./Mapa";
import { Section } from "./Section";

/**
 * Locais onde a Dra. atende (não são dela: nunca chamar de "unidades").
 * Mostra só o endereço do prédio; sala, bloco e horários vão pelo WhatsApp (decisão da Dra.).
 */
export function Locais() {
  return (
    <Section
      id="locais"
      kicker="Locais de atendimento"
      titulo="Tijuca e"
      destaque="Barra da Tijuca."
      intro="A sala e os horários disponíveis são enviados pelo WhatsApp, junto com a confirmação da sua consulta."
      fundo
    >
      <div className="grid gap-6 md:grid-cols-2">
        {LOCAIS.map((u) => (
          <article key={u.id} aria-labelledby={`local-${u.id}`} className="flex flex-col rounded-[1.75rem] bg-surface p-4 ring-1 ring-line sm:p-5">
            <div className="px-2 pt-4 sm:px-3">
              <h3 id={`local-${u.id}`} className="text-3xl text-ink">
                {u.bairro}
              </h3>
              <address className="mt-4 flex gap-3 not-italic text-ink-soft">
                <IconPin className="mt-1 size-5 text-accent" />
                <span>
                  {u.endereco}
                  <br />
                  {u.predio}
                  <br />
                  {u.bairro}, Rio de Janeiro — RJ
                </span>
              </address>
            </div>

            <div className="mt-6 px-2 sm:px-3">
              <ButtonLink
                href={linkWhatsApp(mensagemWhatsAppLocal(u.prep))}
                externo
                data-conv="whatsapp"
                className="w-full"
                aria-label={`Agendar ${u.prep} pelo WhatsApp (abre em nova aba)`}
              >
                <IconWhatsApp /> Agendar {u.prep}
              </ButtonLink>
            </div>

            <div className="mt-6">
              <Mapa endereco={enderecoMapa(u)} titulo={`Mapa do local de atendimento ${u.prep}`} />
              <ButtonLink
                href={linkComoChegar(u)}
                externo
                className="mt-3 w-full"
                aria-label={`Como chegar ao local ${u.prep} no Google Maps (abre em nova aba)`}
              >
                <IconPin /> Como chegar
              </ButtonLink>
            </div>
          </article>
        ))}
      </div>
    </Section>
  );
}
