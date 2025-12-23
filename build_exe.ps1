# ============================================================================
#                    GAME TRANSLATOR - BUILD SCRIPT v3.0.0
#                     Visual Ultra Moderno com Animacoes
# ============================================================================
# Requer PowerShell 5.1 ou superior

$Host.UI.RawUI.WindowTitle = "Game Translator - Build Script"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# ============================================================================
# IMPORTAR MODULO DE UI
# ============================================================================

$ModulePath = Join-Path $ScriptDir "GameTranslatorUI.psm1"
if (Test-Path $ModulePath) {
    Import-Module $ModulePath -Force -DisableNameChecking
} else {
    Write-Host "ERRO: Modulo UI nao encontrado!" -ForegroundColor Red
    exit 1
}

# Definir tema - Opcoes: Neon, Ocean, Sunset, Matrix, Cyberpunk, Arctic
Set-UITheme -ThemeName "Matrix" | Out-Null

# ============================================================================
# HEADER ANIMADO - ENGRENAGENS
# ============================================================================

function Show-BuildHeader {
    Clear-Host
    Write-Host ""
    Write-GradientLine -Char "═" -Length 76 -Animated

    Write-Host ""

    $gears = @(
        "              ╔═══════════════════════════════════╗              ",
        "              ║    ╔═══╗       ╔═══╗     ╔═══╗   ║              ",
        "              ║   ╔╝██ ╚╗     ╔╝██ ╚╗   ╔╝██ ╚╗  ║              ",
        "              ║   ║ ██  ║─────║ ██  ║───║ ██  ║  ║              ",
        "              ║   ╚╗██ ╔╝     ╚╗██ ╔╝   ╚╗██ ╔╝  ║              ",
        "              ║    ╚═══╝       ╚═══╝     ╚═══╝   ║              ",
        "              ║         B U I L D   S Y S T E M  ║              ",
        "              ╚═══════════════════════════════════╝              "
    )

    $gearColors = @("Green", "DarkGreen", "Green", "White", "Green", "DarkGreen", "White", "Green")

    for ($i = 0; $i -lt $gears.Count; $i++) {
        Write-CenteredText $gears[$i] $gearColors[$i] 76
        Start-Sleep -Milliseconds 60
    }

    Write-Host ""
    Write-GradientLine -Char "─" -Length 76
    Write-Host ""
    Write-CenteredText "GAME TRANSLATOR" $Colors.Primary 76
    Write-CenteredText "Build Script - Criacao do Executavel v3.0.0" "DarkGray" 76
    Write-Host ""
    Write-GradientLine -Char "═" -Length 76
    Write-Host ""
}

# ============================================================================
# ANIMACAO DE COMPILACAO
# ============================================================================

function Show-CompileAnimation {
    param([int]$Iterations = 3)

    $frames = @(
        @("▓░░░░", "░░░░░", "░░░░░"),
        @("█▓░░░", "▓░░░░", "░░░░░"),
        @("██▓░░", "█▓░░░", "▓░░░░"),
        @("███▓░", "██▓░░", "█▓░░░"),
        @("████▓", "███▓░", "██▓░░"),
        @("█████", "████▓", "███▓░"),
        @("█████", "█████", "████▓"),
        @("█████", "█████", "█████")
    )

    Write-Host ""
    Write-Host "  ╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor $Colors.Primary
    Write-Host "  ║                                                               ║" -ForegroundColor $Colors.Primary

    for ($iter = 0; $iter -lt $Iterations; $iter++) {
        foreach ($frame in $frames) {
            Write-Host "`r  ║  COMPILANDO  [" -NoNewline -ForegroundColor $Colors.Primary
            Write-Host $frame[0] -NoNewline -ForegroundColor $Colors.Success
            Write-Host "] [" -NoNewline -ForegroundColor $Colors.Dim
            Write-Host $frame[1] -NoNewline -ForegroundColor $Colors.Secondary
            Write-Host "] [" -NoNewline -ForegroundColor $Colors.Dim
            Write-Host $frame[2] -NoNewline -ForegroundColor $Colors.Primary
            Write-Host "]                    ║" -NoNewline -ForegroundColor $Colors.Primary
            Start-Sleep -Milliseconds 100
        }
    }

    Write-Host "`r  ║  COMPILANDO  [█████] [█████] [█████]  ✓ COMPLETO!      ║" -ForegroundColor $Colors.Success
    Write-Host "  ║                                                               ║" -ForegroundColor $Colors.Primary
    Write-Host "  ╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor $Colors.Primary
    Write-Host ""
}

# ============================================================================
# BARRA DE PROGRESSO DO BUILD
# ============================================================================

function Show-BuildProgress {
    param(
        [string]$Stage,
        [int]$Current,
        [int]$Total
    )

    $percent = [math]::Floor(($Current / $Total) * 100)
    $barWidth = 40
    $filled = [math]::Floor(($percent / 100) * $barWidth)
    $empty = $barWidth - $filled

    $filledBar = "█" * $filled
    $emptyBar = "░" * $empty

    Write-Host "`r  [$Stage] [" -NoNewline -ForegroundColor $Colors.Primary
    Write-Host $filledBar -NoNewline -ForegroundColor $Colors.Success
    Write-Host $emptyBar -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "] $percent%" -NoNewline -ForegroundColor $Colors.Info
}

# ============================================================================
# INFORMACOES DO EXECUTAVEL
# ============================================================================

function Show-ExecutableInfo {
    param([string]$Path)

    $fileInfo = Get-Item $Path
    $fileSize = [math]::Round($fileInfo.Length / 1MB, 2)

    Write-Host ""
    Write-Host "  ╔═══════════════════════════════════════════════════════════╗" -ForegroundColor $Colors.Success
    Write-Host "  ║                                                           ║" -ForegroundColor $Colors.Success
    Write-Host "  ║  " -NoNewline -ForegroundColor $Colors.Success
    Write-Host "★ EXECUTAVEL CRIADO COM SUCESSO! ★" -NoNewline -ForegroundColor White
    Write-Host "                  ║" -ForegroundColor $Colors.Success
    Write-Host "  ║                                                           ║" -ForegroundColor $Colors.Success
    Write-Host "  ╠═══════════════════════════════════════════════════════════╣" -ForegroundColor $Colors.Success
    Write-Host "  ║                                                           ║" -ForegroundColor $Colors.Success
    Write-Host "  ║  " -NoNewline -ForegroundColor $Colors.Success
    Write-Host "Arquivo:  " -NoNewline -ForegroundColor $Colors.Info
    Write-Host "GameTranslator.exe".PadRight(37) -NoNewline -ForegroundColor White
    Write-Host "║" -ForegroundColor $Colors.Success
    Write-Host "  ║  " -NoNewline -ForegroundColor $Colors.Success
    Write-Host "Local:    " -NoNewline -ForegroundColor $Colors.Info
    Write-Host "dist\".PadRight(37) -NoNewline -ForegroundColor $Colors.Secondary
    Write-Host "║" -ForegroundColor $Colors.Success
    Write-Host "  ║  " -NoNewline -ForegroundColor $Colors.Success
    Write-Host "Tamanho:  " -NoNewline -ForegroundColor $Colors.Info
    Write-Host "$fileSize MB".PadRight(37) -NoNewline -ForegroundColor $Colors.Primary
    Write-Host "║" -ForegroundColor $Colors.Success
    Write-Host "  ║  " -NoNewline -ForegroundColor $Colors.Success
    Write-Host "Criado:   " -NoNewline -ForegroundColor $Colors.Info
    Write-Host "$($fileInfo.CreationTime.ToString('dd/MM/yyyy HH:mm:ss'))".PadRight(37) -NoNewline -ForegroundColor $Colors.Primary
    Write-Host "║" -ForegroundColor $Colors.Success
    Write-Host "  ║                                                           ║" -ForegroundColor $Colors.Success
    Write-Host "  ╚═══════════════════════════════════════════════════════════╝" -ForegroundColor $Colors.Success
    Write-Host ""
}

# ============================================================================
# LOG DE BUILD
# ============================================================================

function Write-BuildLog {
    param(
        [string]$Message,
        [string]$Type = "INFO" # INFO, SUCCESS, WARNING, ERROR
    )

    $timestamp = Get-Date -Format "HH:mm:ss"
    $icon = switch ($Type) {
        "INFO"    { "[i]"; $Colors.Info }
        "SUCCESS" { "[✓]"; $Colors.Success }
        "WARNING" { "[!]"; $Colors.Warning }
        "ERROR"   { "[✗]"; $Colors.Error }
        default   { "[*]"; $Colors.Primary }
    }

    Write-Host "  $timestamp " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host $icon[0] -NoNewline -ForegroundColor $icon[1]
    Write-Host " $Message" -ForegroundColor $Colors.Info
}

# ============================================================================
# LOGICA PRINCIPAL
# ============================================================================

Show-BuildHeader

Write-Host "  [*] " -NoNewline -ForegroundColor $Colors.Primary
Write-Host "Iniciando processo de build..." -ForegroundColor $Colors.Info
Write-Host ""

# ETAPA 1: Verificar Python
Write-Step 1 4 "Verificando Python..."
Show-AdvancedSpinner -Message "Procurando Python" -Duration 1 -Style "Braille"

try {
    $pythonVersion = py --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python nao encontrado" }
    Write-SubStepSuccess "Python encontrado: $pythonVersion"
} catch {
    Show-ErrorBox "Python nao encontrado! Instale primeiro."
    Read-Host "  Pressione Enter para sair"
    exit 1
}

# ETAPA 2: Instalar PyInstaller
Write-Step 2 4 "Instalando/Atualizando PyInstaller..."
Show-AdvancedSpinner -Message "Verificando PyInstaller" -Duration 1 -Style "Dots"
py -m pip install pyinstaller --quiet 2>$null
Write-SubStepSuccess "PyInstaller pronto"

# ETAPA 3: Limpar e preparar
Write-Step 3 4 "Preparando ambiente de build..."
Set-Location $ScriptDir

Write-BuildLog "Limpando arquivos de builds anteriores..." "INFO"

if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-BuildLog "Pasta build/ removida" "SUCCESS"
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-BuildLog "Pasta dist/ removida" "SUCCESS"
}
Get-ChildItem -Path $ScriptDir -Filter "*.spec" -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-Item -Force $_.FullName
    Write-BuildLog "Arquivo $($_.Name) removido" "SUCCESS"
}

# ETAPA 4: Compilar
Write-Step 4 4 "Compilando executavel..."
Show-InfoBox "Este processo pode levar alguns minutos..."
Write-Host ""

Write-BuildLog "Iniciando PyInstaller..." "INFO"
Write-BuildLog "Configurando dependencias ocultas..." "INFO"
Write-BuildLog "Incluindo recursos do projeto..." "INFO"

Show-CompileAnimation 2

$profilesPath = Join-Path $ScriptDir "profiles"
$mainPath = Join-Path $ScriptDir "src\main.py"
$srcPath = Join-Path $ScriptDir "src"

Write-BuildLog "Executando compilacao principal..." "INFO"

# Simula progresso
$stages = @("Analisando", "Coletando", "Empacotando", "Finalizando")
for ($i = 0; $i -lt $stages.Count; $i++) {
    Show-BuildProgress -Stage $stages[$i] -Current ($i + 1) -Total $stages.Count
    Start-Sleep -Milliseconds 500
}
Write-Host ""

# Executa PyInstaller
if (Test-Path $profilesPath) {
    py -m PyInstaller --name="GameTranslator" --onefile --windowed --noconfirm --clean `
        --paths="$srcPath" `
        --hidden-import=PySide6.QtCore `
        --hidden-import=PySide6.QtGui `
        --hidden-import=PySide6.QtWidgets `
        --hidden-import=sqlite3 `
        --hidden-import=psutil `
        --add-data "profiles;profiles" `
        --add-data "src;src" `
        "$mainPath" 2>$null
} else {
    py -m PyInstaller --name="GameTranslator" --onefile --windowed --noconfirm --clean `
        --paths="$srcPath" `
        --hidden-import=PySide6.QtCore `
        --hidden-import=PySide6.QtGui `
        --hidden-import=PySide6.QtWidgets `
        --hidden-import=sqlite3 `
        --hidden-import=psutil `
        --add-data "src;src" `
        "$mainPath" 2>$null
}

Write-Host ""

# Verificar resultado
$exePath = Join-Path $ScriptDir "dist\GameTranslator.exe"

if (Test-Path $exePath) {
    Write-BuildLog "Compilacao bem-sucedida!" "SUCCESS"

    # Limpar arquivos temporarios
    Write-BuildLog "Limpando arquivos temporarios..." "INFO"
    if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
    Get-ChildItem -Path $ScriptDir -Filter "*.spec" -ErrorAction SilentlyContinue | Remove-Item -Force
    Get-ChildItem -Path $ScriptDir -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
    Write-BuildLog "Arquivos temporarios removidos" "SUCCESS"

    Write-Host ""
    Write-GradientLine -Char "═" -Length 76

    Show-ExecutableInfo -Path $exePath

    Show-ParticleExplosion -Duration 400 -Width 60

    Write-Host ""
    Write-Host "  Abrir pasta do executavel? " -NoNewline -ForegroundColor $Colors.Info
    Write-Host "(S/N) " -NoNewline -ForegroundColor $Colors.Secondary
    $response = Read-Host
    if ($response -match "^[SsYy]$") {
        explorer (Join-Path $ScriptDir "dist")
    }
} else {
    Write-BuildLog "Falha na compilacao!" "ERROR"
    Show-ErrorBox "Falha ao criar executavel!" "Verifique os erros acima."
}

Write-Host ""
Write-GradientLine -Char "═" -Length 76
Write-Host ""
Read-Host "  Pressione Enter para sair"
