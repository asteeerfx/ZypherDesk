@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================
echo ZYPHER SECURITY - PUBLICAR ZYPHERDESK NO GITHUB
 echo ============================================================
echo.
echo 1. Crie um repositorio VAZIO chamado ZypherDesk no GitHub.
echo 2. Copie a URL HTTPS desse repositorio.
echo    Exemplo: https://github.com/SEU_USUARIO/ZypherDesk.git
echo.
set /p "GITHUB_REPO=Cole a URL HTTPS do seu repositorio: "
if "%GITHUB_REPO%"=="" (
    echo Erro: URL vazia.
    pause
    exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\publicar.ps1" -GitHubRepo "%GITHUB_REPO%"
if errorlevel 1 (
    echo.
    echo [ERRO] Nao foi possivel publicar. Confira a mensagem acima.
) else (
    echo.
    echo [OK] Entre em Actions no seu repositorio e execute ZypherDesk Portable Windows x64.
)
pause
