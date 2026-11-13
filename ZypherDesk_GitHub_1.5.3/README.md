# ZypherDesk 1.5.3 — Zypher Security

Kit de código-fonte modificado, logos da Zypher Security e workflow GitHub Actions que gera um **EXE portátil autoextraível** baseado no RustDesk 1.5.3.

> **Este pacote NÃO contém um EXE já compilado.** A compilação foi preparada para GitHub Actions Windows e só pode ser considerada pronta quando o workflow ficar verde e o executável for testado no Windows.

## O que foi personalizado

- Ícone do programa: símbolo oficial Zypher Security.
- Logos da interface: identidade Zypher Security fornecida pelo titular.
- Marca d’água: logo completa sobreposta com opacidade reduzida no painel de conexão, ignorando cliques.
- Identificação `ZypherDesk` em metadados do Windows e nome interno do processo principal.
- Azul-petróleo como cor de borda da tela inicial. A prévia em `assets/PREVIA_ZYPHERDESK.png` é um **conceito visual**, e não uma captura de tela do programa compilado.
- Padrão de acesso assistido: `approve-mode=click` para novas instalações sem configuração anterior. O usuário precisa aceitar a solicitação; configurações existentes não são sobrescritas automaticamente.
- Workflow com Rust 1.75, Flutter 3.24.5, LLVM 15.0.6, vcpkg, bridge e empacotador oficial do RustDesk.

## Como fazer — sem instalar Rust ou Flutter no seu PC

1. Entre em <https://github.com/new> e crie um repositório **vazio**, por exemplo `ZypherDesk` (sem README, .gitignore ou licença inicial; o histórico oficial já será enviado). Prefira **público** para facilitar a disponibilização do código-fonte AGPL.
2. Extraia este ZIP e execute `ENVIAR_PARA_GITHUB.bat` no seu Windows (você já tem Git e Python instalados).
3. Cole a URL HTTPS do repositório recém-criado quando o script pedir, por exemplo `https://github.com/SEU_USUARIO/ZypherDesk.git`.
4. O Git pode pedir login no GitHub no navegador para autorizar o `push`. Autorize sua própria conta.
5. No GitHub, abra o repositório → **Actions** → **ZypherDesk Portable Windows x64** → **Run workflow**.
6. Após o workflow ficar verde, entre no job e baixe **Artifacts → ZypherDesk-Portable-1.5.3-Windows-x64**. Extraia o ZIP para obter `ZypherDesk-Portable-1.5.3-x64.exe`.

Se o GitHub mostrar erro, baixe ou copie o log da etapa em vermelho. O RustDesk 1.5.3 usa diversas dependências e o workflow não foi executado neste ambiente.

### Avisos

- O EXE gerado será **não assinado digitalmente**; não ignore avisos de segurança sem conferir a origem.
- A aprovação por clique exige que o cliente esteja presente e **autorize cada conexão**. Para telas de bloqueio/logon, elevação e acesso não assistido, testes e políticas adicionais são necessários.
- Não foi integrado servidor próprio. O servidor RustDesk OSS (`hbbs`/`hbbr`) deve ser configurado separadamente se desejar infraestrutura Zypher.
- O aplicativo inclui bibliotecas e componentes do RustDesk. Mantenha avisos/licença AGPL-3.0 e publique o código-fonte correspondente com as alterações; o fork não é oficial do RustDesk.
- Não distribua a clientes antes de testar porta, tela/controle, segurança, consentimento, instalação/remoção e uso multi-monitor.

Fonte de referência do pipeline oficial: <https://github.com/rustdesk/rustdesk/blob/1.5.3/.github/workflows/flutter-build.yml>
