import type { ReactNode } from "react";

/** Título em duas cores: primeira linha escura, segunda em caramelo. */
export function Titulo({
  id,
  kicker,
  titulo,
  destaque,
  as: Tag = "h2",
  claro = false,
}: {
  id?: string;
  kicker?: string;
  titulo: string;
  destaque?: string;
  as?: "h1" | "h2";
  claro?: boolean;
}) {
  return (
    <>
      {kicker && (
        <p className={`text-xs font-medium uppercase tracking-[0.22em] ${claro ? "text-white/85" : "text-brand"}`}>{kicker}</p>
      )}
      <Tag
        id={id}
        className={`mt-4 max-w-3xl text-[2.1rem] sm:text-5xl ${claro ? "text-white" : "text-ink"}`}
      >
        {titulo}
        {destaque && (
          <>
            {" "}
            <span className={`block italic ${claro ? "text-[#ead9c6]" : "text-accent"}`}>{destaque}</span>
          </>
        )}
      </Tag>
    </>
  );
}

export function Section({
  id,
  kicker,
  titulo,
  destaque,
  intro,
  children,
  fundo = false,
}: {
  id: string;
  kicker?: string;
  titulo: string;
  destaque?: string;
  intro?: string;
  children: ReactNode;
  fundo?: boolean;
}) {
  return (
    <section id={id} aria-labelledby={`${id}-titulo`} className={fundo ? "bg-bg-soft" : ""}>
      <div className="mx-auto max-w-6xl px-4 py-20 sm:px-6 md:py-28">
        <Titulo id={`${id}-titulo`} kicker={kicker} titulo={titulo} destaque={destaque} />
        {intro && <p className="mt-5 max-w-2xl text-lg text-ink-soft">{intro}</p>}
        <div className="mt-12">{children}</div>
      </div>
    </section>
  );
}
