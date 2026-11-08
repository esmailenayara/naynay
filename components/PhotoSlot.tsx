import Image from "next/image";
import fs from "node:fs";
import path from "node:path";

type Props = {
  /** Caminho em /public, ex.: "/images/hero-clinica.jpg". Para trocar a foto, substitua só o arquivo. */
  src: string;
  alt: string;
  /** Proporção fixa (largura/altura) para não haver salto de layout. */
  proporcao?: "4/5" | "3/2" | "1/1" | "16/9" | "4/3";
  /** Foto de fundo que ocupa todo o elemento pai (o pai precisa ser `relative`). */
  fundo?: boolean;
  /** Classes de enquadramento da foto de fundo (object-position), ex.: "object-[60%_20%]". */
  posicao?: string;
  /** O que deve aparecer na foto ideal (mostrado enquanto o arquivo não existir). */
  descricao: string;
  /** Tamanho recomendado em pixels, ex.: "1600 × 2000 px". */
  tamanho: string;
  priority?: boolean;
  sizes?: string;
  className?: string;
};

const classeProporcao = {
  "4/5": "aspect-[4/5]",
  "3/2": "aspect-[3/2]",
  "1/1": "aspect-square",
  "16/9": "aspect-video",
  "4/3": "aspect-[4/3]",
};

/**
 * Se o arquivo existir em /public na hora do build, mostra a foto.
 * Se não existir, mostra uma caixa com a descrição da foto ideal.
 */
export function PhotoSlot({
  src,
  alt,
  proporcao = "4/5",
  fundo = false,
  posicao = "object-center",
  descricao,
  tamanho,
  priority = false,
  sizes = "(min-width: 768px) 50vw, 100vw",
  className = "",
}: Props) {
  const existe = fs.existsSync(path.join(process.cwd(), "public", src));

  if (fundo) {
    return existe ? (
      <Image src={src} alt={alt} fill sizes={sizes} loading={priority ? "eager" : "lazy"} fetchPriority={priority ? "high" : undefined} className={`object-cover ${posicao}`} />
    ) : (
      <div role="img" aria-label={alt} className="absolute inset-0 bg-[radial-gradient(ellipse_at_70%_30%,#8a6a55_0%,#5a4234_45%,#2f241e)]">
        <span className="absolute right-4 top-24 max-w-56 text-right text-[0.6875rem] leading-snug text-white/55">
          {descricao} · {tamanho} · <code>{src.replace("/images/", "")}</code>
        </span>
      </div>
    );
  }

  return (
    <figure className={`relative overflow-hidden rounded-[1.75rem] bg-bg-soft ${classeProporcao[proporcao]} ${className}`}>
      {existe ? (
        <Image
          src={src}
          alt={alt}
          fill
          sizes={sizes}
          preload={priority}
          fetchPriority={priority ? "high" : undefined}
          loading={priority ? undefined : "lazy"}
          className="object-cover"
        />
      ) : (
        <div
          role="img"
          aria-label={alt}
          className="absolute inset-0 flex flex-col items-center justify-center gap-2 m-2 rounded-[1.4rem] border border-dashed border-[#cdbba6] p-5 text-center"
        >
          <span className="text-sm font-medium text-ink-soft">{descricao}</span>
          <span className="text-xs text-ink-soft">
            {tamanho} · arquivo: <code>{src.replace("/images/", "")}</code>
          </span>
        </div>
      )}
    </figure>
  );
}
