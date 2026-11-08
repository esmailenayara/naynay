import Image from "next/image";
import Link from "next/link";
import { CLINICA, CONTATO, LOCAIS, enderecoCompleto, linkWhatsApp, nomeProfissional } from "@/lib/site";
import { MENSAGEM_WHATSAPP_PADRAO } from "@/lib/terms";
import { AVISO_RESULTADOS } from "@/lib/terms";
import { CookiePrefsButton } from "./CookiePrefsButton";
import { IconInstagram } from "./Icons";

export function Footer() {
  return (
    <footer className="border-t border-line bg-[#2f241e] text-[#e9dccd] pb-24 md:pb-0">
      <div className="mx-auto max-w-6xl px-4 py-12 text-[0.9375rem] text-[#d9c9b6] sm:px-6">
        {/* Logo horizontal da Dra. (só no computador: no celular as letras ficariam pequenas demais). */}
        <Image
          src="/images/logo-horizontal-bege.png"
          alt={`${CLINICA.nome}: ${CLINICA.descritor}`}
          width={820}
          height={96}
          className="mx-auto mb-12 hidden h-auto w-full max-w-2xl md:block"
          loading="lazy"
        />
        <p className="rounded-xl bg-white/10 p-4 text-white">{AVISO_RESULTADOS}</p>

        <div className="mt-10 grid gap-8 md:grid-cols-3">
          <div>
            <p className="text-lg font-light uppercase tracking-[0.22em] text-white">{CLINICA.nome}</p>
            <p className="text-xs uppercase tracking-[0.18em]">{CLINICA.descritor}</p>
            <p className="mt-3">Responsável técnica: {nomeProfissional()}</p>
            <p>Profissional autônoma</p>
          </div>

          <div>
            <p className="font-medium text-white">Locais de atendimento</p>
            {LOCAIS.map((u) => (
              <div key={u.id} className="mt-3">
                <p className="font-medium text-white">{u.bairro}</p>
                <address className="not-italic">{enderecoCompleto(u)}</address>
              </div>
            ))}
          </div>

          <div>
            <p className="font-medium text-white">Contato</p>
            <p className="mt-3">
              Agendamento somente pelo WhatsApp:{" "}
              <a
                href={linkWhatsApp(MENSAGEM_WHATSAPP_PADRAO)}
                target="_blank"
                rel="noopener noreferrer"
                data-conv="whatsapp"
                className="underline underline-offset-2 hover:text-white"
              >
                {CONTATO.whatsappExibicao}
              </a>
            </p>
            <a
              href={CONTATO.instagram}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-3 inline-flex min-h-12 items-center gap-2 underline-offset-2 hover:text-white hover:underline"
              aria-label={`Instagram ${CONTATO.instagramExibicao} (abre em nova aba)`}
            >
              <IconInstagram /> {CONTATO.instagramExibicao}
            </a>
            <ul className="mt-5 space-y-2">
              <li>
                <Link href="/politica-de-privacidade/" className="underline underline-offset-2 hover:text-white">
                  Política de Privacidade
                </Link>
              </li>
              <li>
                <Link href="/termos-de-uso/" className="underline underline-offset-2 hover:text-white">
                  Termos de Uso
                </Link>
              </li>
              <li>
                <CookiePrefsButton />
              </li>
            </ul>
          </div>
        </div>

        <p className="mt-10 text-sm">
          © {new Date().getFullYear()} {CLINICA.nome}. As informações deste site têm caráter informativo e não
          substituem a consulta individual.
        </p>
      </div>
    </footer>
  );
}
