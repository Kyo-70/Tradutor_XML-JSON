# ============================================================================
#                    GAME TRANSLATOR - EXECUCAO RAPIDA v3.0.0
#                     Visual Ultra Moderno com Animacoes
# ============================================================================
# Requer PowerShell 5.1 ou superior

$Host.UI.RawUI.WindowTitle = "Game Translator - Execucao Rapida"
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
Set-UITheme -ThemeName "Neon" | Out-Null

# ============================================================================
# HEADER ANIMADO - FOGUETE
# ============================================================================

function Show-LaunchHeader {
    Clear-Host
    Write-Host ""
    Write-GradientLine -Char "═" -Length 76 -Animated

    Write-Host ""

    $rocket = @(
        "                      ▄▄████▄▄                      ",
        "                    ▄██████████▄                    ",
        "                   ████████████████                 ",
        "                   ████████████████                 ",
        "                   ████████████████                 ",
        "                   ██████▀▀██████▀▀                 ",
        "                  ▐█████    █████▌                  ",
        "                  ▐█████    █████▌                  ",
        "                 ▄█████▌    ▐█████▄                 ",
        "                ████████    ████████                ",
        "               ▀▀▀▀▀▀██▌    ▐██▀▀▀▀▀▀               ",
        "                     ▐█▌    ▐█▌                     ",
        "                    ▄███    ███▄                    ",
        "                   █████    █████                   ",
        "                  ▀▀ ▀▀      ▀▀ ▀▀                  "
    )

    $rocketColors = @("Magenta", "Magenta", "Cyan", "Cyan", "Cyan", "Yellow", "Yellow", "Yellow", "Cyan", "Cyan", "Yellow", "Red", "Red", "Yellow", "Yellow")

    for ($i = 0; $i -lt $rocket.Count; $i++) {
        Write-CenteredText $rocket[$i] $rocketColors[$i] 76
        Start-Sleep -Milliseconds 40
    }

    Write-Host ""
    Write-GradientLine -Char "─" -Length 76
    Write-Host ""
    Write-CenteredRainbow "GAME TRANSLATOR" 76
    Write-CenteredText "Execucao Rapida v3.0.0" "DarkGray" 76
    Write-Host ""
    Write-GradientLine -Char "═" -Length 76
    Write-Host ""
}

# ============================================================================
# ANIMACAO DE LANCAMENTO
# ============================================================================

function Show-LaunchSequence {
    param([string]$Message)

    Write-Host ""
    Write-Host "  ╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor $Colors.Primary
    Write-Host "  ║                                                               ║" -ForegroundColor $Colors.Primary
    Write-Host "  ║  " -NoNewline -ForegroundColor $Colors.Primary

    $frames = @("▸    ", "▸▸   ", "▸▸▸  ", "▸▸▸▸ ", "▸▸▸▸▸")

    for ($i = 0; $i -lt 3; $i++) {
        foreach ($frame in $frames) {
            Write-Host "`r  ║  $frame " -NoNewline -ForegroundColor $Colors.Secondary
            Write-Host $Message -NoNewline -ForegroundColor White
            Write-Host " $frame" -NoNewline -ForegroundColor $Colors.Secondary
            $padding = 59 - $Message.Length - 12
            Write-Host (" " * [math]::Max(0, $padding)) -NoNewline
            Write-Host "║" -NoNewline -ForegroundColor $Colors.Primary
            Start-Sleep -Milliseconds 80
        }
    }

    Write-Host ""
    Write-Host "  ║                                                               ║" -ForegroundColor $Colors.Primary
    Write-Host "  ╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor $Colors.Primary
    Write-Host ""
}

# ============================================================================
# COUNTDOWN ANIMADO
# ============================================================================

function Show-CountdownExit {
    param([int]$Seconds = 3)

    Write-Host ""
    Write-Host "  Fechando em " -NoNewline -ForegroundColor $Colors.Dim

    for ($i = $Seconds; $i -ge 1; $i--) {
        Write-Host "$i " -NoNewline -ForegroundColor $Colors.Primary
        Start-Sleep -Milliseconds 300

        # Efeito de pulse
        Write-Host "`b`b" -NoNewline
        Write-Host "$i " -NoNewline -ForegroundColor $Colors.Secondary
        Start-Sleep -Milliseconds 300

        Write-Host "`b`b" -NoNewline
        Write-Host "$i " -NoNewline -ForegroundColor $Colors.Primary
        Start-Sleep -Milliseconds 400
    }

    Write-Host ""
    Write-Host ""
    Write-CenteredText "Ate a proxima!" $Colors.Success 76
    Write-Host ""
}

# ============================================================================
# LOGICA PRINCIPAL
# ============================================================================

Show-LaunchHeader

$ExePath = Join-Path $ScriptDir "dist\GameTranslator.exe"

# Verifica se o executavel existe
if (Test-Path $ExePath) {
    Show-AdvancedSpinner -Message "Localizando executavel" -Duration 1 -Style "Braille"
    Write-SubStepSuccess "Executavel encontrado!"
    Write-Host ""

    # Informacoes do arquivo
    $fileInfo = Get-Item $ExePath
    $fileSize = [math]::Round($fileInfo.Length / 1MB, 2)

    Write-Host "  ┌─────────────────────────────────────────┐" -ForegroundColor $Colors.Dim
    Write-Host "  │ " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "Arquivo: GameTranslator.exe" -NoNewline -ForegroundColor $Colors.Info
    Write-Host "            │" -ForegroundColor $Colors.Dim
    Write-Host "  │ " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "Tamanho: $fileSize MB".PadRight(37) -NoNewline -ForegroundColor $Colors.Secondary
    Write-Host "│" -ForegroundColor $Colors.Dim
    Write-Host "  └─────────────────────────────────────────┘" -ForegroundColor $Colors.Dim
    Write-Host ""

    Show-GradientProgressBar -Message "Iniciando Game Translator..." -Steps 25 -Delay 35

    Show-LaunchSequence "LANCANDO APLICACAO"

    Start-Process $ExePath

    Show-SuccessBox "Game Translator iniciado com sucesso!" -Animated

    Show-CountdownExit 3
    exit 0
}

# Se nao existe o .exe, tenta via Python
Write-Host ""
Show-WarningBox "Executavel nao encontrado" "Iniciando via Python..."
Write-Host ""

# Verifica Python
try {
    $pythonVersion = py --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python nao encontrado" }
    Write-SubStepSuccess "Python encontrado: $pythonVersion"
} catch {
    Show-ErrorBox "Python nao encontrado!" "Execute INSTALAR.ps1 primeiro."
    Read-Host "  Pressione Enter para sair"
    exit 1
}

Write-Host ""
Show-AdvancedSpinner -Message "Verificando dependencias" -Duration 1 -Style "Dots"
Write-Host ""

# Verifica e instala dependencias se necessario
$dependencies = @(
    @{ Module = "PySide6"; Display = "PySide6 (Interface)" },
    @{ Module = "requests"; Display = "Requests (HTTP)" },
    @{ Module = "psutil"; Display = "PSUtil (Sistema)" },
    @{ Module = "colorama"; Display = "Colorama (Cores)" }
)

foreach ($dep in $dependencies) {
    Write-SubStep "Verificando $($dep.Display)..."
    $checkCmd = "import $($dep.Module)"
    $result = py -c $checkCmd 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`r       [!] Instalando $($dep.Display)...          " -NoNewline -ForegroundColor $Colors.Warning
        py -m pip install $dep.Module --quiet 2>$null
        Write-Host "`r       [✓] $($dep.Display) instalado                " -ForegroundColor $Colors.Success
    } else {
        Write-Host "`r       [✓] $($dep.Display) OK                       " -ForegroundColor $Colors.Success
    }
}

Write-Host ""
Show-SuccessBox "Dependencias verificadas!"

Show-GradientProgressBar -Message "Iniciando Game Translator..." -Steps 25 -Delay 35

Write-Host ""
Write-Host "  [★] " -NoNewline -ForegroundColor $Colors.Secondary
Write-Host "Executando aplicacao..." -ForegroundColor $Colors.Info
Write-Host ""
Write-GradientLine -Char "─" -Length 76
Write-Host ""

Set-Location (Join-Path $ScriptDir "src")
py main.py

Write-Host ""
Write-GradientLine -Char "─" -Length 76
Write-Host ""
Write-Host "  [★] " -NoNewline -ForegroundColor $Colors.Primary
Write-Host "Programa encerrado." -ForegroundColor $Colors.Info
Write-Host ""
Read-Host "  Pressione Enter para sair"
