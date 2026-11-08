import Image from "next/image";

/** Divisor entre seções: linha fina com o monograma NE no centro (escolha da Dra.). */
export function Divisor() {
  return (
    <div aria-hidden="true" className="mx-auto flex max-w-6xl items-center gap-6 px-4 sm:px-6">
      <span className="h-px flex-1 bg-brand/20" />
      <Image src="/images/monograma-cafe.png" alt="" width={500} height={540} className="h-9 w-auto opacity-80" loading="lazy" />
      <span className="h-px flex-1 bg-brand/20" />
    </div>
  );
}
