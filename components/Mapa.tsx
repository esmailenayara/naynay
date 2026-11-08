/**
 * Mapa do Google já aberto (pedido da Dra.: o botão "Mostrar no mapa" parecia erro).
 * `loading="lazy"` faz o mapa carregar só quando a pessoa rola até ele.
 * O mapa pode gravar cookies do Google: isso está na Política de Privacidade.
 */
export function Mapa({ endereco, titulo }: { endereco: string; titulo: string }) {
  const src = `https://www.google.com/maps?q=${encodeURIComponent(endereco)}&output=embed`;
  return (
    <div className="relative aspect-[16/10] overflow-hidden rounded-[1.4rem] bg-bg-soft">
      <iframe
        title={titulo}
        src={src}
        className="absolute inset-0 size-full border-0"
        loading="lazy"
        referrerPolicy="no-referrer-when-downgrade"
      />
    </div>
  );
}
