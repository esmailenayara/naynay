import type { Metadata } from "next";
import { Faq } from "@/components/Faq";
import { Footer } from "@/components/Footer";
import { Header } from "@/components/Header";
import { JsonLd } from "@/components/JsonLd";
import { Contato } from "@/components/Contato";
import { Divisor } from "@/components/Divisor";
import { MobileBar } from "@/components/MobileBar";
import { Comentarios, Procedimentos } from "@/components/Procedimentos";
import { ComoFunciona, Compromisso, Expectativas, Faixa, Hero, Sobre } from "@/components/Secoes";
import { Locais } from "@/components/Locais";

export const metadata: Metadata = { alternates: { canonical: "/" } };

export default function Home() {
  return (
    <>
      <Header />
      <main id="conteudo">
        <Hero />
        <Faixa />
        <ComoFunciona />
        <Sobre />
        <Compromisso />
        <Procedimentos />
        <Expectativas />
        <Divisor />
        <Comentarios />
        <Locais />
        <Contato />
        <Divisor />
        <Faq />
      </main>
      <Footer />
      <MobileBar />
      <JsonLd />
    </>
  );
}
