# Game Translator - Execução Rápida
# Requer PowerShell 5.1 ou superior

$Host.UI.RawUI.WindowTitle = "Game Translator"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Cores personalizadas
$ColorTitulo = "Magenta"
$ColorSucesso = "Green"
$ColorErro = "Red"
$ColorAviso = "Yellow"
$ColorInfo = "Cyan"

Clear-Host
Write-Host ""
Write-Host "========================================================================" -ForegroundColor $ColorTitulo
Write-Host "  GAME TRANSLATOR - EXECUCAO RAPIDA" -ForegroundColor $ColorTitulo
Write-Host "========================================================================" -ForegroundColor $ColorTitulo
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ExePath = Join-Path $ScriptDir "dist\GameTranslator.exe"

# Verifica se o executável existe
if (Test-Path $ExePath) {
    Write-Host "Iniciando Game Translator..." -ForegroundColor $ColorInfo
    Start-Process $ExePath
    exit 0
}

# Se não existe, tenta via Python
Write-Host "Executavel nao encontrado. Iniciando via Python..." -ForegroundColor $ColorAviso
Write-Host ""

# Verifica Python
try {
    $pythonVersion = py --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python não encontrado" }
} catch {
    Write-Host "[ERRO] Python nao encontrado!" -ForegroundColor $ColorErro
    Write-Host "Execute INSTALAR.ps1 primeiro." -ForegroundColor $ColorInfo
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "Verificando dependencias..." -ForegroundColor $ColorInfo
Write-Host ""

# Verifica e instala dependências se necessário
$dependencies = @("PySide6", "requests", "psutil", "colorama")

foreach ($dep in $dependencies) {
    $checkCmd = "import $dep"
    $result = py -c $checkCmd 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   Instalando $dep..." -ForegroundColor $ColorInfo
        py -m pip install $dep --quiet
    }
}

Write-Host "[OK] Dependencias verificadas!" -ForegroundColor $ColorSucesso
Write-Host ""
Write-Host "Iniciando Game Translator..." -ForegroundColor $ColorInfo
Write-Host ""

Set-Location (Join-Path $ScriptDir "src")
py main.py

Write-Host ""
Write-Host "Programa encerrado." -ForegroundColor $ColorInfo
Read-Host "Pressione Enter para sair"
