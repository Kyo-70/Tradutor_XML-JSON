# Game Translator - Verificação do Sistema
# Requer PowerShell 5.1 ou superior

$Host.UI.RawUI.WindowTitle = "Game Translator - Verificacao do Sistema"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Cores personalizadas
$ColorTitulo = "Magenta"
$ColorErro = "Red"
$ColorInfo = "Cyan"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Verifica se Python está disponível
try {
    $result = py --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python não encontrado" }
} catch {
    Write-Host ""
    Write-Host "========================================================================" -ForegroundColor $ColorTitulo
    Write-Host "  ERRO: Python nao encontrado!" -ForegroundColor $ColorErro
    Write-Host "========================================================================" -ForegroundColor $ColorTitulo
    Write-Host ""
    Write-Host "  Baixe Python em: https://www.python.org/downloads/" -ForegroundColor $ColorInfo
    Write-Host "  Durante a instalacao, marque 'Add Python to PATH'" -ForegroundColor $ColorInfo
    Write-Host ""
    Write-Host "========================================================================" -ForegroundColor $ColorTitulo
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Executa o script Python com cores
Set-Location (Join-Path $ScriptDir "src")
py verificar_sistema.py --auto-instalar

# Retorna o código de saída do script Python
exit $LASTEXITCODE
