#!/usr/bin/env python3
"""Verifica marca e metadados do ZypherDesk antes da compilacao longa."""
from pathlib import Path
import sys
from PIL import Image

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
        'Color(0xFFDDE4E8)',
        'if (preference.isEmpty || preference == \'system\') return ThemeMode.light;',
        'https://desk.zyphersecurity.com.br',
    ],
    "flutter/lib/desktop/pages/desktop_setting_page.dart": [
        'Sobre o ZypherDesk',
        'Declaração de privacidade',
        'https://desk.zyphersecurity.com.br/privacidade',
        'Licenciamento GNU AGPL-3.0',
        'contato@zyphersecurity.com.br',
    ],
    "LICENCAS_E_AVISOS.txt": [
        "AGPL-3.0",
        "RustDesk",
    ],
    "flutter/lib/desktop/pages/desktop_home_page.dart": [
        'zypher_security_watermark.png',
        'width: isIncomingOnly ? 280.0 : 300.0,',
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
    "assets/zypher_icon_master.png",
    "assets/zypher_logo_master.png",
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
# Nao aceitar silenciosamente o logotipo antigo.
try:
    with Image.open(ROOT / 'assets/zypher_logo_master.png') as master:
        with Image.open(ROOT / 'flutter/assets/logo.png') as applied:
            if master.convert('RGBA').tobytes() != applied.convert('RGBA').tobytes():
                errors.append('Logomarca Flutter difere do segundo arquivo fornecido.')
    with Image.open(ROOT / 'assets/zypher_icon_master.png') as symbol:
        if min(symbol.size) < 128:
            errors.append('Icone Zypher de resolucao insuficiente.')
except Exception as e:
    errors.append(f'Erro ao validar as imagens oficiais: {e}')

if errors:
    for error in errors:
        print(f"[ERRO] {error}")
    sys.exit(1)
print("[OK] ZypherDesk: logos, iconografia, propriedades e Sobre conferidos.")
