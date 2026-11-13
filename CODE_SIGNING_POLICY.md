# Code signing policy — ZypherDesk

**Estado em 13/11/2026: NÃO ASSINADO.** A assinatura digital gratuita da SignPath Foundation ainda **não foi solicitada nem aprovada**. O executável atual não deve ser divulgado como assinado ou confiável por certificação.

## Projeto
- Nome: ZypherDesk
- Mantenedora das modificações: Zypher Security
- Repositório: https://github.com/asteeerfx/ZypherDesk
- Site: https://desk.zyphersecurity.com.br
- Política de privacidade pretendida: https://desk.zyphersecurity.com.br/privacidade
- Contato: contato@zyphersecurity.com.br
- Origem: personalização do RustDesk 1.5.3, software licenciado sob GNU AGPL-3.0; os créditos e obrigações do projeto original são mantidos.

## Código, builds e publicação
O código é compilado no GitHub Actions a partir deste repositório, especialmente pelo workflow
`.github/workflows/build-zypherdesk.yml`.
O programa oferece acesso remoto por ID e mecanismos de consentimento, com aprovação por clique como configuração padrão de novas instalações (configurações preexistentes podem diferir).

A assinatura deve ser feita **somente após uma aprovação formal da SignPath Foundation** e aplicada exclusivamente aos artefatos produzidos por uma execução verificável do workflow em uma versão marcada com tag. O projeto não deve assinar binários de terceiros com um eventual certificado SignPath.

Quando aprovado: **Free code signing provided by SignPath.io, certificate by SignPath Foundation**. Até lá, nenhuma assinatura pela SignPath Foundation é fornecida ou alegada.

Cada versão terá que ser revisada e aprovada manualmente antes da assinatura. O projeto deve publicar checksum SHA-256, alterações e instruções de verificação das assinaturas junto ao download.

## Papéis e segurança
- Responsável por preparar o projeto / committer atual: proprietário do repositório `@asteeerfx`.
- Revisores independentes: **A DESIGNAR**; não declarar aprovação ou revisão ainda inexistente.
- Aprovadores de assinatura: **A DESIGNAR**; responsável legal pelo projeto deverá confirmar os nomes.
- Todos os participantes precisam usar autenticação multifator (MFA) no GitHub e no SignPath.
- Todas as mudanças relevantes, especialmente nos workflows de build e assinatura, devem passar por revisão apropriada.

## Privacidade e permissões
O ZypherDesk é uma ferramenta de acesso remoto. Ao usá-lo, podem ser enviados IDs de conexão, metadados, dados da sessão e, quando permitido, conteúdo da tela, arquivos ou área de transferência. O aplicativo pode usar servidores públicos do projeto base até que um servidor próprio seja configurado.

A política em https://desk.zyphersecurity.com.br/privacidade deve descrever corretamente os dados tratados, provedores de infraestrutura e controles de consentimento antes da publicação pública. Não afirmar que a conexão é exclusivamente local ou que não transmite dados.

## Verificação de assinaturas (quando houver certificado válido)
No PowerShell:
```powershell
Get-AuthenticodeSignature .\ZypherDesk-Portable-1.5.3-x64.exe | Format-List Status,SignerCertificate
Get-FileHash .\ZypherDesk-Portable-1.5.3-x64.exe -Algorithm SHA256
```
Uma assinatura válida **não garante** ausência de avisos do Microsoft Defender SmartScreen, que também utiliza reputação.

## Referências
- Condições SignPath Foundation: https://signpath.org/terms
- Solicitação: https://signpath.org/apply
- Código-base: https://github.com/rustdesk/rustdesk
- Licença: `LICENCE` e `LICENCAS_E_AVISOS.txt`
