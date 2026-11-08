import type { NextConfig } from "next";

// Exportação 100% estática (pasta out/). Funciona na Vercel, Cloudflare Pages ou Netlify.
const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  // Sem servidor de otimização: as fotos em /public/images já devem ir no tamanho recomendado.
  images: { unoptimized: true },
  // Esconde o ícone "N" do Next.js que aparece no canto da tela durante o desenvolvimento (não vai para o site publicado).
  devIndicators: false,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;
