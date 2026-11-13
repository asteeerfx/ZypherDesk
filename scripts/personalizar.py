#!/usr/bin/env python3
"""Branding ZypherDesk on the upstream RustDesk 1.5.3 checkout.
Preserves AGPL notices and network/auth protocol; requires customer click approval.
"""
from pathlib import Path
import argparse, shutil

ROOT_PACKAGE = Path(__file__).resolve().parents[1]
ASSETS = ROOT_PACKAGE / 'assets'

def replace_once(path, old, new, name):
    if not path.is_file():
        raise RuntimeError(f'{name}: arquivo ausente: {path}')
    content = path.read_text(encoding='utf-8')
    if new in content:
        print(f'[OK] {name} (ja aplicado)')
        return
    count=content.count(old)
    if count != 1:
        raise RuntimeError(f'{name}: esperado 1 ponto em {path}, encontrado {count}. O RustDesk alterou esse trecho?')
    path.write_text(content.replace(old,new,1),encoding='utf-8', newline='')
    print(f'[OK] {name}')

def replace_if_present(path, old, new, name):
    if not path.is_file():
        return
    content = path.read_text(encoding='utf-8')
    if new in content:
        return
    if old in content:
        path.write_text(content.replace(old,new),encoding='utf-8',newline='')
        print(f'[OK] {name}')

def apply(repo):
    repo=repo.resolve()
    required=(repo/'Cargo.toml',repo/'flutter/pubspec.yaml',repo/'src/common.rs')
    if not all(p.is_file() for p in required):
        raise RuntimeError(f'Pasta informada nao parece checkout RustDesk: {repo}')
    if 'version: 1.5.3+' not in (repo/'flutter/pubspec.yaml').read_text(encoding='utf-8'):
        raise RuntimeError('Base incompativel: precisa do tag 1.5.3 do RustDesk.')

    replace_once(repo/'src/common.rs',
       'pub fn global_init() -> bool {\n',
       'pub fn global_init() -> bool {\n'
       '    // ZypherDesk: identifica fork e define modo de aprovacao manual para novas instalacoes.\n'
       '    *hbb_common::config::APP_NAME.write().unwrap() = "ZypherDesk".to_owned();\n'
       '    if hbb_common::config::Config::get_option("approve-mode").is_empty() {\n'
       '        hbb_common::config::Config::set_option("approve-mode".to_owned(), "click".to_owned());\n'
       '    }\n',
       'Nome e aprovacao manual')

    rc=repo/'flutter/windows/runner/Runner.rc'
    for old,new,n in [
      ('VALUE "CompanyName", "Purslane Tech Pte. Ltd."','VALUE "CompanyName", "Zypher Security"','Empresa'),
      ('VALUE "FileDescription", "RustDesk Remote Desktop"','VALUE "FileDescription", "ZypherDesk - Suporte Remoto"','Descricao'),
      ('VALUE "InternalName", "rustdesk"','VALUE "InternalName", "ZypherDesk"','Nome interno Windows'),
      ('VALUE "OriginalFilename", "rustdesk.exe"','VALUE "OriginalFilename", "ZypherDesk.exe"','Nome original Windows'),
      ('VALUE "ProductName", "RustDesk"','VALUE "ProductName", "ZypherDesk"','Produto Windows'),
    ]:
        replace_once(rc,old,new,n)
    replace_once(rc,
       'VALUE "ProductName", "ZypherDesk" "\\0"',
       'VALUE "ProductName", "ZypherDesk" "\\0"\n'
       '            VALUE "Comments", "ZypherDesk e um fork AGPL-3.0 do RustDesk: github.com/rustdesk/rustdesk" "\\0"',
       'Credito do upstream')
    replace_once(repo/'flutter/lib/desktop/pages/desktop_home_page.dart',
       'const borderColor = Color(0xFF2F65BA);',
       'const borderColor = Color(0xFF0B7082);',
       'Paleta azul-petroleo Zypher')
    home = repo/'flutter/lib/desktop/pages/desktop_home_page.dart'
    replace_if_present(home, 'Color.fromARGB(255, 226, 66, 188)',
       'Color.fromARGB(255, 9, 55, 77)', 'Gradiente azul-profundo')
    replace_if_present(home, 'Color.fromARGB(255, 244, 114, 124)',
       'Color.fromARGB(255, 0, 138, 154)', 'Gradiente ciano')

    # Watermark is overlaid with a very low alpha, ignores pointer events, and never blocks controls.
    replace_once(repo/'flutter/lib/desktop/pages/desktop_home_page.dart',
       '''  buildRightPane(BuildContext context) {
    return Container(
      color: Theme.of(context).scaffoldBackgroundColor,
      child: ConnectionPage(),
    );
  }''',
       '''  buildRightPane(BuildContext context) {
    return Container(
      color: Theme.of(context).scaffoldBackgroundColor,
      child: Stack(
        fit: StackFit.expand,
        children: [
          ConnectionPage(),
          // Marca d'agua transparente; nao interfere em clicks e campos.
          IgnorePointer(
            child: Center(
              child: Opacity(
                opacity: 0.075,
                child: Image.asset(
                  'assets/zypher_security_watermark.png',
                  width: 340,
                  fit: BoxFit.contain,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }''',
       'Marca d agua no painel central')

    copied={
        'icon.png': 'flutter/assets/icon.png',
        'logo.png': 'flutter/assets/logo.png',
        'logo_light.png': 'flutter/assets/logo_light.png',
        'logo_dark.png': 'flutter/assets/logo_dark.png',
        'zypher_security_watermark.png': 'flutter/assets/zypher_security_watermark.png',
        'app_icon.ico': 'flutter/windows/runner/resources/app_icon.ico',
        'icon.svg': 'flutter/assets/icon.svg',
    }
    for source,target in copied.items():
        dest=repo/target
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ASSETS/source,dest)
        print('[OK] Identidade:',target)
    (repo/'res').mkdir(parents=True, exist_ok=True)
    shutil.copy2(ASSETS/'icon.png',repo/'res/icon.png')
    print('[OK] Icone res/icon.png')
    # Tambem substitui o icone nativo (Rust/Windows) e o icone da bandeja.
    shutil.copy2(ASSETS/'app_icon.ico',repo/'res/icon.ico')
    shutil.copy2(ASSETS/'app_icon.ico',repo/'res/tray-icon.ico')
    print('[OK] Icones nativos ZypherDesk no executavel e na bandeja')
    print('Personalizacao aplicada ao codigo RustDesk 1.5.3. Compilacao ainda necessaria.')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('repo',type=Path)
    args=parser.parse_args()
    apply(args.repo)
