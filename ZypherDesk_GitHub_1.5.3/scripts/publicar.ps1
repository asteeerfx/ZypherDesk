param([Parameter(Mandatory=$true)][string]$GitHubRepo)
$ErrorActionPreference = 'Stop'
$package = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$source = Join-Path $package 'rustdesk'
if ($GitHubRepo -notmatch '^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?$') {
    throw 'URL HTTPS inválida. Exemplo: https://github.com/seuusuario/ZypherDesk.git'
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git não encontrado.' }
if (-not (Test-Path (Join-Path $source 'Cargo.toml'))) {
    Write-Host 'Baixando RustDesk 1.5.3 e submodulos do repositorio oficial...'
    & git clone --depth 1 --branch 1.5.3 --recurse-submodules https://github.com/rustdesk/rustdesk.git $source
    if ($LASTEXITCODE -ne 0) { throw 'Falha no download do RustDesk. Confirme a internet.' }
}
Push-Location $source
try {
    $isGitRepo = (& git rev-parse --is-inside-work-tree 2>$null) -eq 'true'
    if (-not $isGitRepo) { throw 'A pasta rustdesk não tem repositorio Git.' }
    $branch = & git branch --show-current
    if ($branch -ne 'main') {
        & git switch -C main
        if ($LASTEXITCODE -ne 0) { throw 'Não foi possível criar branch main.' }
    }
    $files = @(
        @{Origin='assets'; Target='assets'},
        @{Origin='scripts/personalizar.py'; Target='scripts/personalizar.py'},
        @{Origin='.github/workflows/build-zypherdesk.yml'; Target='.github/workflows/build-zypherdesk.yml'},
        @{Origin='README.md'; Target='README-ZYPHERDESK.md'}
    )
    foreach ($item in $files) {
        $from = Join-Path $package $item.Origin
        $to = Join-Path $source $item.Target
        $parent = Split-Path -Parent $to
        if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
        if (Test-Path $from -PathType Container) {
            if (-not (Test-Path $to)) { New-Item -ItemType Directory -Force -Path $to | Out-Null }
            Copy-Item (Join-Path $from '*') $to -Recurse -Force
        } else {
            Copy-Item $from $to -Force
        }
    }
    & python scripts/personalizar.py .
    if ($LASTEXITCODE -ne 0) { throw 'Patch de marca falhou. Repositório não publicado.' }
    & git add -- scripts/personalizar.py .github/workflows/build-zypherdesk.yml README-ZYPHERDESK.md assets/ flutter/assets/ flutter/windows/runner/resources/app_icon.ico res/icon.png src/common.rs flutter/lib/desktop/pages/desktop_home_page.dart flutter/windows/runner/Runner.rc
    if ($LASTEXITCODE -ne 0) { throw 'Falha em git add.' }
    & git -c user.name='Zypher Security' -c user.email='contato@zyphersecurity.com.br' commit -m 'ZypherDesk 1.5.3: identidade oficial e build Windows portable'
    if ($LASTEXITCODE -ne 0) { Write-Host 'Nenhuma mudança nova. Tentando publicar o estado atual...' }
    $remotes = @(& git remote)
    if ($remotes -contains 'zypher') { & git remote remove zypher }
    & git remote add zypher $GitHubRepo
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao configurar remoto do GitHub.' }
    & git push -u zypher HEAD:main
    if ($LASTEXITCODE -ne 0) { throw 'Falha no git push. O GitHub pode pedir login ou o repositório pode não estar vazio.' }
    Write-Host '[OK] Projeto publicado. Abra seu GitHub -> Repositorio -> Actions.' -ForegroundColor Green
} finally {
    Pop-Location
}
