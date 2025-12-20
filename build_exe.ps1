# Game Translator - Build Script
# Requer PowerShell 5.1 ou superior

$Host.UI.RawUI.WindowTitle = "Game Translator - Build Script"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "========================================"
Write-Host " Game Translator - Build Script"
Write-Host "========================================"
Write-Host ""

Write-Host "Instalando PyInstaller..."
pip install pyinstaller

Write-Host ""
Write-Host "Gerando executavel..."

Set-Location $ScriptDir

# Verifica se a pasta profiles existe
$profilesPath = Join-Path $ScriptDir "profiles"
$addDataArg = if (Test-Path $profilesPath) { "--add-data `"profiles;profiles`"" } else { "" }

$mainPath = Join-Path $ScriptDir "src\main.py"

if ($addDataArg) {
    pyinstaller --name="GameTranslator" --onefile --windowed --add-data "profiles;profiles" $mainPath
} else {
    pyinstaller --name="GameTranslator" --onefile --windowed $mainPath
}

Write-Host ""
Write-Host "========================================"
Write-Host "Build concluido!"
Write-Host "Executavel criado em: dist\GameTranslator.exe"
Write-Host "========================================"
Read-Host "Pressione Enter para sair"
