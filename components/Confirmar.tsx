/** Etiqueta visível só no `npm run dev`, marcando texto que a profissional precisa confirmar. */
export function Confirmar({ ok }: { ok: boolean }) {
  if (ok) return null;
  return (
    <span className="ml-2 inline-block rounded bg-amber-100 px-1.5 py-0.5 align-middle font-sans text-xs font-semibold tracking-wide text-amber-900">
      CONFIRMAR
    </span>
  );
}
