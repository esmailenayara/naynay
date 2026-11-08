import type { Metadata } from "next";
import { LegalPage } from "@/components/LegalPage";
import { ATUALIZACAO_LEGAL, CLINICA, CONTATO, LOCAIS, enderecoCompleto } from "@/lib/site";

export const metadata: Metadata = {
  title: "Política de Privacidade",
  description: `Como ${CLINICA.nome} trata os dados pessoais coletados neste site, conforme a LGPD.`,
  alternates: { canonical: "/politica-de-privacidade/" },
};

// TEXTO-BASE: revise com assessoria jurídica.
export default function Politica() {
  return (
    <LegalPage titulo="Política de Privacidade" atualizado={ATUALIZACAO_LEGAL}>
      <p>
        Esta política explica como {CLINICA.responsavelLegal} (&quot;nós&quot;), trata os dados pessoais
        de quem usa este site, em conformidade com a Lei Geral de Proteção de Dados Pessoais (Lei nº 13.709/2018 —
        LGPD).
      </p>

      <h2>1. Quem é o controlador dos dados</h2>
      <p>
        {CLINICA.responsavelLegal}, e-mail {CLINICA.email}, com atendimento em:
      </p>
      <ul>
        {LOCAIS.map((u) => (
          <li key={u.id}>{enderecoCompleto(u)}</li>
        ))}
      </ul>
      <p>
        Encarregada pelo tratamento de dados: Nayara Esmaile, e-mail {CLINICA.email}.
      </p>

      <h2>2. Quais dados coletamos</h2>
      <p>
        <strong>Neste site:</strong> não há formulário e não pedimos nenhum dado pessoal. O agendamento é feito somente
        pelo WhatsApp.
      </p>
      <p>
        <strong>Ao navegar:</strong> dados técnicos como endereço IP, tipo de navegador e páginas acessadas, coletados
        automaticamente pelo serviço de hospedagem para segurança e funcionamento do site e, somente se você permitir
        no aviso de cookies, pelo Google Ads para medir agendamentos originados de anúncios.
      </p>
      <p>
        <strong>No WhatsApp:</strong> a conversa acontece fora deste site. Usamos o seu nome, o número de telefone e o
        que você nos enviar apenas para o seu atendimento e agendamento. A conversa também segue a política de
        privacidade do WhatsApp.
      </p>

      <h2>3. Para que usamos os dados</h2>
      <ul>
        <li>Atender você e confirmar, remarcar ou cancelar a sua consulta;</li>
        <li>Medir, de forma agregada, quantos agendamentos vieram de anúncios (somente com o seu consentimento);</li>
        <li>Garantir a segurança do site e cumprir obrigações legais.</li>
      </ul>
      <p>
        Não usamos seus dados para remarketing, criação de públicos de publicidade ou personalização de anúncios, e
        não vendemos dados pessoais.
      </p>

      <h2>4. Bases legais</h2>
      <ul>
        <li>Consentimento (art. 7º, I, da LGPD), dado no aviso de cookies e ao iniciar a conversa pelo WhatsApp;</li>
        <li>Procedimentos preliminares relacionados a contrato a pedido do titular (art. 7º, V), para o agendamento;</li>
        <li>Cumprimento de obrigação legal ou regulatória (art. 7º, II) e legítimo interesse para segurança do site (art. 7º, IX).</li>
      </ul>

      <h2>5. Com quem compartilhamos</h2>
      <p>Os dados podem ser tratados por prestadores que nos ajudam a operar o site, sempre limitados ao necessário:</p>
      <ul>
        <li>Hospedagem do site: Cloudflare, Inc. (Cloudflare Pages);</li>
        <li>Atendimento por mensagens: WhatsApp (Meta Platforms, Inc.);</li>
        <li>Medição de conversões: Google LLC (Google Ads), apenas se você aceitar no aviso de cookies;</li>
        <li>Mapas dos locais de atendimento: Google LLC (Google Maps);</li>
        <li>Autoridades públicas, quando houver obrigação legal.</li>
      </ul>
      <p>
        Alguns desses prestadores podem armazenar dados fora do Brasil. Nesses casos, a transferência ocorre nos termos
        do art. 33 da LGPD, com prestadores que adotam padrões de proteção compatíveis.
      </p>

      <h2 id="cookies">6. Cookies</h2>
      <p>
        <strong>Necessários:</strong> guardam a sua escolha no aviso de cookies (armazenamento local do navegador). Não
        podem ser desativados, pois o site depende deles para lembrar a sua preferência.
      </p>
      <p>
        <strong>Medição de anúncios (opcional):</strong> cookie do Google Ads usado só para contar agendamentos vindos
        de anúncios. Fica desativado até você clicar em &quot;Aceitar&quot; no aviso. Não usamos cookies de remarketing
        nem de personalização de anúncios.
      </p>
      <p>
        <strong>Mapa do Google:</strong> a seção &quot;Locais de atendimento&quot; mostra mapas do Google Maps, que carregam
        quando você chega a essa parte da página. O Google pode gravar cookies próprios ao exibir o mapa, conforme a
        política de privacidade do Google.
      </p>
      <p>Você pode mudar a sua escolha a qualquer momento pelo link &quot;Preferências de cookies&quot;, no rodapé.</p>

      <h2>7. Por quanto tempo guardamos</h2>
      <p>
        Dados de agendamento que não resultarem em atendimento são excluídos em até 6 meses. Se houver
        atendimento, os dados passam a seguir as regras de guarda do prontuário, conforme a legislação e as normas do
        conselho profissional.
      </p>

      <h2>8. Seus direitos</h2>
      <p>Conforme o art. 18 da LGPD, você pode, a qualquer momento:</p>
      <ul>
        <li>Confirmar se tratamos seus dados e acessá-los;</li>
        <li>Corrigir dados incompletos, inexatos ou desatualizados;</li>
        <li>Pedir anonimização, bloqueio ou eliminação de dados desnecessários;</li>
        <li>Revogar o consentimento e pedir a eliminação dos dados tratados com base nele;</li>
        <li>Pedir informações sobre compartilhamento e sobre a portabilidade dos dados;</li>
        <li>Apresentar reclamação à Autoridade Nacional de Proteção de Dados (ANPD).</li>
      </ul>
      <p>
        Para exercer esses direitos, escreva para {CLINICA.email} ou fale pelo WhatsApp {CONTATO.whatsappExibicao}.
        Respondemos em até 15 dias.
      </p>

      <h2>9. Segurança</h2>
      <p>
        O site usa conexão criptografada (HTTPS). Adotamos medidas técnicas e administrativas para proteger os dados
        contra acesso não autorizado, perda ou alteração, e o acesso é restrito à equipe responsável pelo agendamento.
      </p>

      <h2>10. Alterações</h2>
      <p>
        Esta política pode ser atualizada. A data da última versão fica sempre no topo da página.
      </p>
    </LegalPage>
  );
}
