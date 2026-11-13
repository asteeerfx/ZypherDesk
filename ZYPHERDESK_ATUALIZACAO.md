# ZypherDesk — revisão de identidade visual (13/11/2026)

## O que foi alterado

- Ícone oficial Zypher Security no executável portátil, no app Flutter, no binário Rust e na bandeja Windows.
- Metadados do aplicativo e do empacotador: Produto **ZypherDesk**, Empresa **Zypher Security**, descrição **ZypherDesk - Suporte Remoto**.
- Tema azul-petróleo e azul-escuro como preferência visual inicial. O usuário ainda pode selecionar o tema claro nas configurações.
- Marca d'água Zypher Security mantida no painel central, sem bloquear a interação com a interface.
- Texto do topo **Desenvolvido por ZypherSecurity**, com link para `https://desk.zyphersecurity.com.br`.
- Aba **Sobre o ZypherDesk** com versão e data real da compilação, ID/fingerprint, declaração de privacidade, website e contato.
- **Declaração de privacidade:** `https://desk.zyphersecurity.com.br` (redireciona à página indicada pelo titular; é necessário publicar lá o conteúdo da política).
- **Website:** `https://desk.zyphersecurity.com.br`.
- **Contato:** `contato@zyphersecurity.com.br`.
- Mantido o modo de conexão assistida por aprovação do cliente. Não foi implementado acesso sem consentimento.
- Incluída validação de branding antes de compilar e verificação de propriedades após o empacotamento.

## Build

No repositório, abra **Actions > ZypherDesk Portable Windows x64 > Run workflow** (branch `main`). Quando o job finalizar verde, baixe **Artifacts > ZypherDesk-Portable-1.5.3-Windows-x64**.

O executável final só pode ser validado após abrir em um Windows de teste, verificar a aba Sobre, conectar entre dois computadores autorizados e conferir o ícone e as propriedades pelo Explorador do Windows.

## Assinatura e segurança

**O código NÃO incorpora certificado nem remove avisos do Windows SmartScreen.** A assinatura digital legítima deve ser feita após a emissão de um certificado de assinatura de código confiável à Zypher Security. Não coloque senha de certificado, PFX ou tokens em commits públicos. Quando houver certificado, configurar a assinatura via secrets de CI apropriados ou serviço seguro de assinatura e retestar no Windows.

A assinatura, por si só, não garante ausência de alertas do SmartScreen, que também utiliza reputação.

## Direitos autorais

ZypherDesk é uma personalização baseada no RustDesk 1.5.3, licenciado sob **AGPL-3.0**. Os avisos e os direitos autorais do projeto original permanecem aplicáveis. Ao distribuir executáveis a clientes, disponibilize o código-fonte correspondente e as modificações de acordo com a licença.

## Observação sobre funcionalidades

Esta revisão preserva os recursos atuais de conexão, transferência de arquivos e autenticação da base RustDesk 1.5.3. Não atualiza automaticamente o programa para versões posteriores do RustDesk nem substitui testes de segurança e estabilidade.
