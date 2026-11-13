#!/usr/bin/env python3
"""Classifica resultados Gitleaks sem exibir valores. Nao suprime alertas novos."""
from __future__ import annotations

import collections
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
RULE = "generic-api-key"
WORKFLOW = ".github/workflows/build-zypherdesk.yml"
SAFE_LINE = "$flutterRoot = Split-Path -Parent (Split-Path -Parent $flutterCmd)"
BASELINE = json.loads((ROOT / "scripts" / "upstream_rustdesk_1_5_3_blobs.json").read_text(encoding="utf-8"))["file_blob_sha"]

def git(*args: str) -> str | None:
    p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False)
    return p.stdout.strip() if p.returncode == 0 else None

def categorize(finding: dict) -> str:
    path = str(finding.get("File", ""))
    commit = str(finding.get("Commit", ""))
    rule = finding.get("RuleID", "")
    if rule != RULE or not commit:
        return "novo_ou_inconclusivo"
    if path in BASELINE:
        if git("rev-parse", f"{commit}:{path}") == BASELINE[path]:
            return "arquivo_identico_ao_upstream"
        return "arquivo_modificado_no_historico"
    if path == WORKFLOW:
        try:
            line_number = int(finding["StartLine"])
        except (KeyError, ValueError, TypeError):
            return "linha_desconhecida"
        content = git("show", f"{commit}:{path}")
        if content is None:
            return "commit_inacessivel"
        lines = content.splitlines()
        if 1 <= line_number <= len(lines) and lines[line_number - 1].strip() == SAFE_LINE:
            return "comando_flutter_sem_credencial"
    return "novo_ou_inconclusivo"

def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv)>1 else Path(".gitleaks-audit-tmp.json")
    findings = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else []
    if not isinstance(findings, list):
        print("Erro: relatorio do detector de segredos invalido.")
        return 1

    checked = [(f, categorize(f)) for f in findings]
    counts = collections.Counter(category for _f, category in checked)
    bad = [(f, c) for f, c in checked if c not in {"arquivo_identico_ao_upstream", "comando_flutter_sem_credencial"}]

    print(f"Potenciais achados: {len(findings)}.")
    print(f"Codigo ORIGINAL identico ao RustDesk 1.5.3: {counts['arquivo_identico_ao_upstream']}.")
    print(f"Comando local de caminho do Flutter sem credencial: {counts['comando_flutter_sem_credencial']}.")
    print(f"Alertas NOVOS ou nao classificados: {len(bad)}.")
    if bad:
        for finding, category in bad[:25]:
            # Nunca exibir o valor sinalizado: somente caminho, linha, regra e commit.
            print(f"PENDENTE: {finding.get('File','?')}:{finding.get('StartLine','?')} | {finding.get('RuleID','?')} | {category} | commit {finding.get('Commit','?')}")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("### Auditoria de segredos — criterio estrito\\n")
            f.write(f"Alertas: **{len(findings)}**. Idênticos ao upstream RustDesk 1.5.3: **{counts['arquivo_identico_ao_upstream']}**. Linha Flutter classificada sem segredo: **{counts['comando_flutter_sem_credencial']}**. Pendentes: **{len(bad)}**.\\n")
            f.write("A validacao compara o SHA de cada blob no commit exato que disparou o alerta. Mudancas em qualquer arquivo/commit ou novas regras **nao serao ignoradas**. Ainda e necessaria revisao humana de historico, logs e privacidade antes de tornar o repositorio publico.\\n")
    if bad:
        print("Reprovado: revisar os alertas novos sem publicar valores de credenciais.")
        return 1
    print("Triagem automatica sem achados nao classificados. Revisao manual de publicacao ainda necessaria.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
