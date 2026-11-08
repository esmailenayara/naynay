import type { AnchorHTMLAttributes, ReactNode } from "react";

type Variante = "primario" | "claro" | "vidro";

const estilos: Record<Variante, string> = {
  primario: "bg-botao text-white hover:bg-botao-hover",
  // Para usar sobre o fundo escuro do topo (hero). Fora do topo, todos os botões são "primario".
  claro: "bg-surface text-brand hover:bg-brand-tint",
  vidro: "border border-white/60 bg-white/10 text-white backdrop-blur hover:bg-white/20",
};

type Props = AnchorHTMLAttributes<HTMLAnchorElement> & {
  variante?: Variante;
  children: ReactNode;
  externo?: boolean;
};

/** Link com cara de botão em pílula (alvo de toque ≥ 48px). */
export function ButtonLink({ variante = "primario", className = "", externo, children, ...rest }: Props) {
  return (
    <a
      {...rest}
      {...(externo && { target: "_blank", rel: "noopener noreferrer" })}
      className={`inline-flex min-h-12 items-center justify-center gap-2 rounded-full px-7 text-[0.9375rem] font-medium tracking-wide transition-colors ${estilos[variante]} ${className}`}
    >
      {children}
    </a>
  );
}
