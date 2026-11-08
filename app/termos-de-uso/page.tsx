import type { Metadata } from "next";
import Link from "next/link";
import { LegalPage } from "@/components/LegalPage";
import { ATUALIZACAO_LEGAL, CLINICA, nomeProfissional } from "@/lib/site";
import { AVISO_RESULTADOS } from "@/lib/terms";

export const metadata: Metadata = {
  title: "Termos de Uso",
  description: `Condições de uso do site de ${CLINICA.nome}.`,
  alternates: { canonical: "/termos-de-uso/" },
};

// TEXTO-BASE: revise com assessoria jurídica.
export default function Termos() {
  return (
    <LegalPage titulo="Termos de Uso" atualizado={ATUALIZACAO_LEGAL}>
      <p>
        Estes termos regulam o uso deste site, mantido por {CLINICA.responsavelLegal}. Ao usar o site,
        você concorda com as condições abaixo.
      </p>

      <h2>1. Finalidade do site</h2>
      <p>
        O site apresenta informações sobre o atendimento da profissional responsável e os locais onde ela atende, e indica o WhatsApp para
        agendar uma consulta. O conteúdo tem caráter informativo.
      </p>

      <h2>2. Consulta individual</h2>
      <p>{AVISO_RESULTADOS}</p>
      <p>
        As informações do site não constituem indicação, diagnóstico ou recomendação para nenhum caso específico e não
        substituem a consulta presencial com a profissional responsável, {nomeProfissional()}.
      </p>

      <h2>3. Agendamento</h2>
      <p>
        O agendamento é feito somente pelo WhatsApp e só vale depois de confirmado pela equipe. A consulta avaliativa é
        paga, com valor informado antes da confirmação. Remarcações e
        cancelamentos devem ser avisados com antecedência mínima de 24 horas.
      </p>

      <h2>4. Responsabilidades de quem usa o site</h2>
      <ul>
        <li>Informar dados verdadeiros e próprios no atendimento pelo WhatsApp;</li>
        <li>Não usar o site para fins ilícitos ou que prejudiquem seu funcionamento.</li>
      </ul>

      <h2>5. Links externos</h2>
      <p>
        O site contém links para serviços de terceiros, como WhatsApp e Google Maps. Esses serviços têm termos e
        políticas próprios, pelos quais não respondemos.
      </p>

      <h2>6. Propriedade intelectual</h2>
      <p>
        Textos, fotos e marca deste site pertencem a {CLINICA.responsavelLegal} ou são usados com autorização. A reprodução
        sem permissão não é autorizada.
      </p>

      <h2>7. Privacidade</h2>
      <p>
        O tratamento de dados pessoais segue a <Link href="/politica-de-privacidade/">Política de Privacidade</Link>.
      </p>

      <h2>8. Alterações e foro</h2>
      <p>
        Estes termos podem ser atualizados a qualquer momento. Fica eleito o foro da Comarca do Rio de Janeiro — RJ,
        observados os direitos do consumidor previstos em lei.
      </p>
    </LegalPage>
  );
}
