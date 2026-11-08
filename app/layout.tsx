import type { Metadata, Viewport } from "next";
import { Jost } from "next/font/google";
import fs from "node:fs";
import path from "node:path";
import "./globals.css";
import { Analytics } from "@/components/Analytics";
import { CookieBanner } from "@/components/CookieBanner";
import { SITE_URL, CLINICA } from "@/lib/site";
import { SEO } from "@/lib/terms";

const jost = Jost({
  subsets: ["latin"],
  variable: "--font-jost",
  display: "swap",
  weight: ["300", "400", "500"],
  // Itálico usado na 2ª linha dos títulos (destaque).
  style: ["normal", "italic"],
});

const temOg = fs.existsSync(path.join(process.cwd(), "public/images/og.jpg"));

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: { default: SEO.titulo, template: `%s | ${CLINICA.nome}` },
  description: SEO.descricao,
  applicationName: `${CLINICA.nome} — ${CLINICA.descritor}`,
  robots: { index: true, follow: true },
  openGraph: {
    type: "website",
    locale: "pt_BR",
    siteName: `${CLINICA.nome} — ${CLINICA.descritor}`,
    title: SEO.titulo,
    description: SEO.descricao,
    url: "/",
    ...(temOg && {
      images: [{ url: "/images/og.jpg", width: 1200, height: 630, alt: "Dra. Nayara Esmaile" }],
    }),
  },
  formatDetection: { telephone: false },
};

export const viewport: Viewport = {
  themeColor: "#f7f2eb",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="pt-BR" className={`${jost.variable} antialiased`}>
      <body className="min-h-screen font-sans">
        <a
          href="#conteudo"
          className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[60] focus:rounded-lg focus:bg-surface focus:px-4 focus:py-3 focus:text-ink focus:shadow"
        >
          Pular para o conteúdo
        </a>
        {children}
        <CookieBanner />
        <Analytics />
      </body>
    </html>
  );
}
