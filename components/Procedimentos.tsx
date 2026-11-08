import { MOSTRAR_NAO_CONFIRMADOS, visiveis } from "@/lib/conteudo";
import { COMENTARIOS, PROCEDIMENTOS } from "@/lib/procedimentos";
import { PERFIL_GOOGLE, nomeProfissional } from "@/lib/site";
import { ButtonLink } from "./Button";
import { Confirmar } from "./Confirmar";
import { IconExternal } from "./Icons";
import { ProcedimentosTabs } from "./ProcedimentosTabs";
import { Section } from "./Section";

export function Procedimentos() {
  const itens = visiveis(PROCEDIMENTOS);
  if (itens.length === 0) return null;
  return (
    <Section
      id="procedimentos"
      kicker="Procedimentos"
      titulo="Dúvidas sobre"
      destaque="cada procedimento."
      intro="Informações gerais para você chegar à consulta com mais clareza. A indicação é sempre individual."
      fundo
    >
      <ProcedimentosTabs itens={itens} mostrarConfirmar={MOSTRAR_NAO_CONFIRMADOS} />
    </Section>
  );
}

/**
 * Comentários reais do Google, só sobre atendimento. Sem estrelas, nota ou contagem.
 * Os dois botões levam ao mesmo perfil do Google (o de mais avaliações), onde estão depoimentos e fotos.
 * "Ver fotos" no lugar de "Ver resultados": a palavra soa como promessa de resultado (ver COMPLIANCE.md).
 */
export function Comentarios() {
  const itens = visiveis(COMENTARIOS);
  return (
    <Section
      id="comentarios"
      kicker="Depoimentos no Google"
      titulo="O que dizem"
      destaque="sobre o atendimento."
      intro="Veja os depoimentos e as fotos publicados no Google."
    >
      {/* Nota real do perfil no Google (5,0 em 08/11/2026). Se a nota mudar, atualizar ou tirar as estrelas. */}
      <div className="-mt-8 mb-10 flex flex-wrap items-center gap-x-3 gap-y-2">
        {/* Estrelas finas em dourado champanhe, discretas (a Dra. achou as anteriores infantis). */}
        <span className="flex items-center gap-1.5" aria-hidden="true">
          <svg width="0" height="0" className="absolute">
            <defs>
              <linearGradient id="dourado-estrela" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stopColor="#f3dc9a" />
                <stop offset="50%" stopColor="#d2a64a" />
                <stop offset="100%" stopColor="#a87a2a" />
              </linearGradient>
            </defs>
          </svg>
          <Estrelas />
        </span>
        <span className="text-sm text-ink-soft">A {nomeProfissional()} é 5 estrelas na plataforma.</span>
      </div>
      {itens.length > 0 && (
        <ul className="grid gap-5 md:grid-cols-3">
          {itens.map((a) => (
            <li key={a.texto}>
              <figure className="flex h-full flex-col rounded-[1.75rem] bg-surface p-8 ring-1 ring-line">
                <span className="flex items-center gap-1" role="img" aria-label="5 de 5 estrelas">
                  <Estrelas />
                </span>
                <blockquote className="mt-5 flex-1 text-lg text-ink">“{a.texto}”</blockquote>
                <figcaption className="mt-6 text-sm font-medium text-ink">
                  {a.autor}
                  <Confirmar ok={a.confirmado} />
                </figcaption>
              </figure>
            </li>
          ))}
        </ul>
      )}
      <div className={`flex flex-col gap-3 sm:flex-row ${itens.length > 0 ? "mt-10" : ""}`}>
        <ButtonLink href={PERFIL_GOOGLE} externo aria-label="Ver depoimentos no Google (abre em nova aba)">
          <IconExternal /> Ver depoimentos
        </ButtonLink>
        <ButtonLink href={PERFIL_GOOGLE} externo aria-label="Ver fotos no Google (abre em nova aba)">
          <IconExternal /> Ver fotos
        </ButtonLink>
      </div>
    </Section>
  );
}

/** Cinco estrelas finas em dourado champanhe (o degradê #dourado-estrela é definido uma vez na seção). */
function Estrelas() {
  return (
    <>
      {[0, 1, 2, 3, 4].map((i) => (
        <svg key={i} viewBox="0 0 24 24" className="size-[1.1rem]" aria-hidden="true">
          <path d="M12.00 2.10 L14.47 9.20 L21.99 9.36 L15.99 13.90 L18.17 21.09 L12.00 16.80 L5.83 21.09 L8.01 13.90 L2.01 9.36 L9.53 9.20Z" fill="url(#dourado-estrela)" />
        </svg>
      ))}
    </>
  );
}
