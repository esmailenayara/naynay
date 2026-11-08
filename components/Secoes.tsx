import { CLINICA, PROFISSIONAL, linkWhatsApp, nomeProfissional } from "@/lib/site";
import { AVISO_RESULTADOS, HERO, MENSAGEM_WHATSAPP_PADRAO } from "@/lib/terms";
import { EXPECTATIVAS, FAIXA, PASSOS, SOBRE, visiveis } from "@/lib/conteudo";
import { ButtonLink } from "./Button";
import { Confirmar } from "./Confirmar";
import { IconWhatsApp } from "./Icons";
import { PhotoSlot } from "./PhotoSlot";
import { Section, Titulo } from "./Section";

export function Hero() {
  return (
    <section aria-labelledby="hero-titulo" className="relative isolate flex min-h-[92svh] items-end overflow-hidden bg-[#1c0908]">
      {/* Celular: foto em cima e texto embaixo. Computador: foto à direita e texto à esquerda, sobre o fundo da própria foto (#1c0908). */}
      <div className="absolute inset-x-0 top-0 h-[60svh] md:inset-y-0 md:left-[46%] md:right-0 md:h-auto">
        <PhotoSlot
          src="/images/hero.jpg"
          alt={`Retrato da ${CLINICA.nome}`}
          fundo
          posicao="object-[55%_35%] md:object-[50%_50%]"
          descricao="Foto de fundo: retrato dela em fundo escuro"
          tamanho="retrato, 1200 × 1800 px"
          sizes="(min-width: 768px) 54vw, 100vw"
          priority
        />
        <div aria-hidden="true" className="absolute inset-y-0 left-0 hidden w-2/5 bg-gradient-to-r from-[#1c0908] to-transparent md:block" />
        <div aria-hidden="true" className="absolute inset-x-0 bottom-0 h-2/5 bg-gradient-to-t from-[#1c0908] to-transparent md:hidden" />
      </div>
      <div className="relative mx-auto w-full max-w-6xl px-4 pb-28 pt-[54svh] sm:px-6 md:pb-24 md:pt-36">
        {/* Em telas médias, o texto quebra antes para não ficar em cima do braço na foto. */}
        <div className="md:max-w-[42vw] xl:max-w-none">
        <Titulo
          as="h1"
          id="hero-titulo"
          claro
          kicker={CLINICA.descritor}
          titulo={HERO.titulo}
          destaque={HERO.destaque}
        />
        <p className="mt-6 max-w-xl text-lg text-white/85">{HERO.subtitulo}</p>
        <div className="mt-9 flex flex-col gap-3 sm:flex-row md:flex-col md:items-start xl:flex-row">
          <ButtonLink
            href={linkWhatsApp(MENSAGEM_WHATSAPP_PADRAO)}
            externo
            data-conv="whatsapp"
            variante="claro"
            aria-label="Agendar minha consulta pelo WhatsApp (abre em nova aba)"
          >
            <IconWhatsApp /> Agendar minha consulta
          </ButtonLink>
          <ButtonLink href="#locais" variante="vidro">
            Locais de atendimento
          </ButtonLink>
        </div>
        <p className="mt-8 max-w-xl text-sm text-white/70">{AVISO_RESULTADOS}</p>
        </div>
      </div>
    </section>
  );
}

/** Faixa de fatos logo abaixo do hero. Só entram afirmações verificáveis. */
export function Faixa() {
  return (
    <div className="border-b border-line bg-bg-soft">
      <ul className="mx-auto flex max-w-6xl flex-wrap justify-center gap-x-8 gap-y-3 px-4 py-5 text-center text-[0.6875rem] font-medium uppercase tracking-[0.2em] text-ink-soft sm:px-6">
        {FAIXA.map((f) => (
          <li key={f} className="flex items-center gap-8">
            <span>{f}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function ComoFunciona() {
  return (
    <Section id="como-funciona" kicker="Como funciona" titulo="Do primeiro contato" destaque="ao seu plano.">
      <ol className="grid gap-px overflow-hidden rounded-[1.75rem] bg-line md:grid-cols-3">
        {PASSOS.map((p, i) => (
          <li key={p.titulo} className="bg-surface p-8 md:p-10">
            <span aria-hidden="true" className="text-4xl font-light text-accent">
              {String(i + 1).padStart(2, "0")}
            </span>
            <h3 className="mt-6 text-2xl text-ink">
              <span className="sr-only">Etapa {i + 1}: </span>
              {p.titulo}
            </h3>
            <p className="mt-3 text-ink-soft">{p.texto}</p>
          </li>
        ))}
      </ol>
      <div className="mt-10">
        <ButtonLink
          href={linkWhatsApp(MENSAGEM_WHATSAPP_PADRAO)}
          externo
          data-conv="whatsapp"
          aria-label="Agendar pelo WhatsApp (abre em nova aba)"
        >
          <IconWhatsApp /> Agendar pelo WhatsApp
        </ButtonLink>
      </div>
    </Section>
  );
}

/** Faixa com foto de fundo e uma frase, como pausa visual entre seções. */
export function Compromisso() {
  return (
    <section aria-labelledby="compromisso-titulo" className="relative isolate flex min-h-[70svh] items-center overflow-hidden">
      <PhotoSlot
        src="/images/faixa-ambiente.jpg"
        alt="Detalhe do ambiente de atendimento"
        fundo
        descricao="Foto de fundo: detalhe do ambiente (poltrona, plantas, luz), sem pessoas"
        tamanho="2000 × 1200 px"
      />
      <div aria-hidden="true" className="absolute inset-0 bg-gradient-to-r from-[#2f241e]/90 via-[#2f241e]/70 to-[#2f241e]/30" />
      <div className="relative mx-auto w-full max-w-6xl px-4 py-24 sm:px-6">
        <Titulo id="compromisso-titulo" claro kicker="Nosso propósito" titulo="Naturalidade" destaque="e elegância." />
        <p className="mt-6 max-w-lg text-lg text-white/85">
          Realçar o que já é seu e cuidar, com delicadeza, dos sinais que o tempo deixou.
        </p>
      </div>
    </section>
  );
}

export function Sobre() {
  const paragrafos = visiveis(SOBRE.paragrafos);
  return (
    <section id="profissional" aria-labelledby="profissional-titulo" className="bg-bg-soft">
      <div className="mx-auto grid max-w-6xl items-center gap-12 px-4 py-20 sm:px-6 md:grid-cols-[1fr_1.15fr] md:gap-20 md:py-28">
        <div className="relative">
          <PhotoSlot
            src="/images/profissional-nayara.jpg"
            alt={`Retrato da ${nomeProfissional()}`}
            proporcao="4/5"
            descricao="Retrato dela, roupa sóbria, fundo neutro"
            tamanho="1000 × 1250 px"
            sizes="(min-width: 768px) 40vw, 100vw"
          />
        </div>
        <div>
          <Titulo id="profissional-titulo" kicker="Sobre a Dra." titulo={nomeProfissional()} />
          <ul className="mt-8 divide-y divide-line border-y border-line">
            {PROFISSIONAL.formacao.map((f) => (
              <li key={f} className="py-4 text-ink">
                {f}
              </li>
            ))}
          </ul>
          {paragrafos.map((p) => (
            <p key={p.texto} className="mt-6 text-ink-soft">
              {p.texto}
              <Confirmar ok={p.confirmado} />
            </p>
          ))}
        </div>
      </div>
    </section>
  );
}

export function Expectativas() {
  const itens = visiveis(EXPECTATIVAS);
  if (itens.length === 0) return null;
  return (
    <Section id="atendimento" kicker="O atendimento" titulo="O que você pode" destaque="esperar de nós.">
      <ul className="grid gap-x-12 gap-y-10 sm:grid-cols-2 lg:grid-cols-3">
        {itens.map((e) => (
          <li key={e.titulo} className="border-t border-brand/25 pt-6">
            <h3 className="text-xl text-ink">
              {e.titulo}
              <Confirmar ok={e.confirmado} />
            </h3>
            <p className="mt-2 text-ink-soft">{e.texto}</p>
          </li>
        ))}
      </ul>
    </Section>
  );
}
