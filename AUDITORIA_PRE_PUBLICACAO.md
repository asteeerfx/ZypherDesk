# Auditoria de segurança antes de tornar o ZypherDesk público

**Situação: revisão pendente. NÃO alterar a visibilidade para público antes da conclusão.**

## Triagem automática realizada em 13/11/2026
- Workflow: `.github/workflows/auditoria-publicacao.yml`
- Execução mais recente com relatório sanitizado: https://github.com/asteeerfx/ZypherDesk/actions/runs/43523008397
- Ferramenta: Gitleaks 8.24.2, varredura de histórico Git completo com `--log-opts="--all"`
- Resultado: **91 alertas potenciais**, todos com a regra `generic-api-key`. O número de alertas não equivale a 91 segredos reais.
- Localização: concentrados em `src/lang/*.rs` (arquivos de tradução) e `src/custom_server.rs`, além de um alerta em `.github/workflows/build-zypherdesk.yml`.
- Verificação pontual: `src/custom_server.rs`, `src/lang/pt_BR.rs` e `src/lang/en.rs` têm exatamente o mesmo blob SHA que o repositório upstream RustDesk no tag `1.5.3`.
- **Conclusão da auditoria: inconclusiva.** Há sinais de falsos positivos nos trechos herdados, mas não se deve colocar o projeto em público antes de analisar os achados restantes.

## Tarefas obrigatórias
- [ ] Conferir no resumo do job as ocorrências por regra e arquivo **sem exibir valores**.
- [ ] Classificar cada alerta como falso positivo ou segredo real; confirmar os 91, não apenas exemplos.
- [ ] Se encontrar segredo real, revogar e substituir a credencial. Apagar apenas a linha atual é insuficiente; inspecionar e, se necessário, sanear o histórico.
- [ ] Revisar o alerta em `.github/workflows/build-zypherdesk.yml`, especialmente a referência à variável efêmera `ACTIONS_RUNTIME_TOKEN`, que não deve ser fixada em texto.
- [ ] Revisar o histórico de GitHub Actions e os artefatos antes de tornar público: os logs passam a ficar visíveis.
- [ ] Reavaliar requisitos de privacidade, permissões, comunicação de dados e vínculo visível com upstream para a SignPath Foundation.
- [ ] Executar novamente o Gitleaks após corrigir problemas e só então considerar a publicação.

**Observação:** nenhuma assinatura digital foi aplicada ou aprovada. O status final de auditoria não pode ser dado como seguro apenas com esta análise.
