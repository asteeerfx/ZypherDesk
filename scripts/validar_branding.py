#!/usr/bin/env python3
"""Verifica marca e metadados do ZypherDesk antes da compilacao longa."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECKS = {
    "libs/portable/build.rs": ['set_icon("../../assets/app_icon.ico")'],
    "libs/portable/Cargo.toml": [
        'ProductName = "ZypherDesk"',
        'CompanyName = "Zypher Security"',
        'FileDescription = "ZypherDesk - Suporte Remoto"',
    ],
    "flutter/windows/runner/Runner.rc": [
        'VALUE "CompanyName", "Zypher Security"',
        'VALUE "FileDescription", "ZypherDesk - Suporte Remoto"',
    ],
    "flutter/lib/common.dart": [
        'Desenvolvido por ZypherSecurity',
        '0xFF09283D',
        'https://desk.zyphersecurity.com.br',
    ],
    "flutter/lib/desktop/pages/desktop_setting_page.dart": [
        'Sobre o ZypherDesk',
        'Declaração de privacidade',
        'https://desk.zyphersecurity.com.br',
        'contato@zyphersecurity.com.br',
    ],
    "flutter/lib/desktop/pages/desktop_home_page.dart": [
        'zypher_security_watermark.png',
        'width: isIncomingOnly ? 280.0 : 260.0,',
    ],
    "src/flutter_ffi.rs": [
        'pub fn is_disable_account() -> SyncReturn<bool> {',
        'SyncReturn(true)',
    ],
    "flutter/lib/common/widgets/login.dart": [
        'if (bind.isDisableAccount()) return Future<bool?>.value(false);',
    ],
    "flutter/lib/desktop/pages/connection_page.dart": [
        'const url = "https://desk.zyphersecurity.com.br";',
    ],
}
IMAGES = [
    "assets/app_icon.ico",
    "assets/icon.png",
    "assets/icon.svg",
    "assets/logo.png",
    "assets/logo_light.png",
    "assets/logo_dark.png",
    "assets/zypher_security_watermark.png",
]
errors = []
for rel in IMAGES:
    p = ROOT / rel
    if not p.is_file() or p.stat().st_size < 100:
        errors.append(f"Imagem ausente ou vazia: {rel}")
for rel, snippets in CHECKS.items():
    p = ROOT / rel
    if not p.is_file():
        errors.append(f"Arquivo ausente: {rel}")
        continue
    data = p.read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet not in data:
            errors.append(f"Marca ausente em {rel}: {snippet}")
if errors:
    for error in errors:
        print(f"[ERRO] {error}")
    sys.exit(1)
print("[OK] ZypherDesk: logos, iconografia, propriedades e Sobre conferidos.")
