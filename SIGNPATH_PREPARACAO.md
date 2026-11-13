# Preparação para assinatura gratuita — ZypherDesk

**Situação:** candidatura ainda NÃO enviada; programa ainda NÃO assinado.

## Critérios a conferir antes da solicitação
1. [ ] Auditoria de segredos no **repositório inteiro, inclusive commits antigos** e logs do GitHub Actions. Uma verificação de nomes de arquivos não substitui essa auditoria.
2. [ ] Confirmar que não há acesso, domínios privados, contas de clientes, PFX, tokens ou configurações confidenciais no histórico.
3. [ ] Verificar permissão para usar as imagens de marca da Zypher Security no projeto público.
4. [ ] Tornar o repositório público pelo proprietário **somente após** a auditoria. Todos os commits, arquivos, logs e Actions existentes poderão se tornar visíveis.
5. [ ] Adequar o vínculo com o projeto original à condição de **fork visível** exigida pela SignPath Foundation para modificações de upstream. O repositório atual foi criado como cópia do código; **não presumir** que a SignPath aceitará isso como um fork reconhecido. Pode ser necessário migrar as alterações para um fork formal do RustDesk ou obter orientação direta da SignPath.
6. [ ] Comprovar que o software base publica builds assinados, e que o desenvolvimento/release segue ramificações assinadas quando exigido pela SignPath.
7. [ ] Apresentar uma versão publicada e documentada no GitHub Releases, com executável, hash e fonte correspondente (AGPL-3.0).
8. [ ] Publicar uma política de privacidade **verdadeira e completa** em https://desk.zyphersecurity.com.br/privacidade. Não inventar afirmações sobre telemetria, provedores ou coleta.
9. [ ] Publicar no site/README um link intitulado **Code signing policy** apontando para `CODE_SIGNING_POLICY.md`.
10. [ ] Definir autores, revisores e aprovadores de assinatura, habilitar MFA e instituir revisão de mudanças no código e no build.
11. [ ] Testar em Windows limpo, inclusive aprovação do cliente, acesso UAC, remoção/instalação, conexão com infraestrutura e aviso legal.
12. [ ] Conferir os requisitos atuais em https://signpath.org/terms e preencher a candidatura em https://signpath.org/apply.

## Solicitação — rascunho em inglês (NÃO ENVIADA)

**Project name:** ZypherDesk

**Repository:** https://github.com/asteeerfx/ZypherDesk

**Website:** https://desk.zyphersecurity.com.br

**License:** GNU AGPL-3.0, based on RustDesk 1.5.3. The corresponding source, license and upstream attribution will be published according to applicable terms.

**Project description:** ZypherDesk is a branded remote desktop support application for Windows, distributed as a portable executable and built from source using GitHub Actions. New installations use a click-approval mode by default for user-assisted remote support. Existing settings may affect authentication behavior. The maintainers request review for eligibility for the free SignPath Foundation code signing program, including clarification of the requirements applying to modified upstream software and visible GitHub forks.

**Status:** Signing policy prepared; project security audit, public release, role assignments and upstream-fork eligibility confirmation pending.

**Publisher name if accepted:** SignPath Foundation (not Zypher Security).

Não declarar que a inscrição foi aceita, que o executável está assinado ou que o SmartScreen deixará de avisar.

## Mudança de visibilidade — etapa exclusiva do proprietário
Acesse https://github.com/asteeerfx/ZypherDesk/settings → **General** → **Danger Zone** → **Change repository visibility** → **Make public**. Essa ação requer permissões administrativas e implica publicação do histórico. **Não executar antes das etapas 1–3 acima.**

## Se não houver aprovação
Alternativas legítimas: obter um certificado comercial de assinatura de código (OV) para a empresa; ou criar um pacote MSIX e tentar a Microsoft Store, com requisitos específicos de certificação. Nenhuma delas deve ser confundida com um desbloqueio de antivírus.
