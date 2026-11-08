import { CLINICA, CONTATO, SITE_URL, LOCAIS } from "@/lib/site";

/** Dados estruturados do atendimento. Sem endereço completo (decisão da Dra.), nota, comentários ou preço. */
export function JsonLd() {
  const dados = {
    "@context": "https://schema.org",
    "@type": "HealthAndBeautyBusiness",
    name: CLINICA.nome,
    description: CLINICA.descritor,
    url: SITE_URL,
    telephone: `+${CONTATO.whatsapp}`,
    areaServed: LOCAIS.map((u) => ({ "@type": "Place", name: `${u.bairro}, Rio de Janeiro - RJ` })),
  };
  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(dados) }} />;
}
