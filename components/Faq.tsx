import { FAQ } from "@/lib/conteudo";
import { IconChevron } from "./Icons";
import { Section } from "./Section";

export function Faq() {
  return (
    <Section id="duvidas" kicker="Perguntas frequentes" titulo="Sobre a consulta" destaque="e o agendamento.">
      <div className="max-w-3xl divide-y divide-line rounded-[1.75rem] bg-surface ring-1 ring-line">
        {FAQ.map((f) => (
          <details key={f.pergunta} className="group px-5 sm:px-6">
            <summary className="flex min-h-14 cursor-pointer list-none items-center justify-between gap-4 py-4 font-medium text-ink">
              <h3 className="text-lg font-normal">{f.pergunta}</h3>
              <IconChevron className="size-5 text-accent transition-transform group-open:rotate-180" />
            </summary>
            <p className="pb-5 text-ink-soft">{f.resposta}</p>
          </details>
        ))}
      </div>
    </Section>
  );
}
