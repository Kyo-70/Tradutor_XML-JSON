# ============================================================================
#                 GAME TRANSLATOR - VERIFICACAO DO SISTEMA v3.0.0
#                     Visual Ultra Moderno com Animacoes
# ============================================================================
# Requer PowerShell 5.1 ou superior

$Host.UI.RawUI.WindowTitle = "Game Translator - Verificacao do Sistema"
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
Set-UITheme -ThemeName "Ocean" | Out-Null

# ============================================================================
# HEADER ANIMADO - LUPA/SCANNER
# ============================================================================

function Show-ScannerHeader {
    Clear-Host
    Write-Host ""
    Write-GradientLine -Char "═" -Length 76 -Animated

    Write-Host ""

    $scanner = @(
        "               ╔═══════════════════════════╗               ",
        "               ║    ◉ SYSTEM SCANNER ◉    ║               ",
        "               ╚═══════════════════════════╝               ",
        "                                                           ",
        "                    ╭─────────────────╮                    ",
        "                   ╱                   ╲                   ",
        "                  │    ┌─────────┐     │                  ",
        "                  │    │  ◎  ◎  │     │                  ",
        "                  │    │ ═══════ │     │                  ",
        "                  │    │  ▓▓▓▓▓  │     │                  ",
        "                  │    └─────────┘     │                  ",
        "                   ╲                   ╱                   ",
        "                    ╰─────────────────╯                    "
    )

    $scannerColors = @("Cyan", "White", "Cyan", "Blue", "DarkCyan", "Cyan", "Cyan", "Yellow", "White", "Green", "Cyan", "Cyan", "DarkCyan")

    for ($i = 0; $i -lt $scanner.Count; $i++) {
        Write-CenteredText $scanner[$i] $scannerColors[$i] 76
        Start-Sleep -Milliseconds 50
    }

    Write-Host ""
    Write-GradientLine -Char "─" -Length 76
    Write-Host ""
    Write-CenteredText "GAME TRANSLATOR" $Colors.Primary 76
    Write-CenteredText "Verificacao do Sistema v3.0.0" "DarkGray" 76
    Write-Host ""
    Write-GradientLine -Char "═" -Length 76
    Write-Host ""
}

# ============================================================================
# ANIMACAO DE SCAN
# ============================================================================

function Show-ScanningAnimation {
    param([int]$Duration = 2)

    $width = 50
    $scanChar = "▓"
    $emptyChar = "░"

    Write-Host ""
    Write-Host "  ╔$("═" * ($width + 2))╗" -ForegroundColor $Colors.Primary
    Write-Host "  ║ " -NoNewline -ForegroundColor $Colors.Primary

    for ($pos = 0; $pos -lt $width; $pos++) {
        # Desenha a barra com a posição do scanner
        Write-Host "`r  ║ " -NoNewline -ForegroundColor $Colors.Primary

        for ($i = 0; $i -lt $width; $i++) {
            if ($i -eq $pos -or $i -eq $pos - 1 -or $i -eq $pos + 1) {
                Write-Host $scanChar -NoNewline -ForegroundColor $Colors.Secondary
            } elseif ($i -lt $pos - 1) {
                Write-Host $scanChar -NoNewline -ForegroundColor $Colors.Success
            } else {
                Write-Host $emptyChar -NoNewline -ForegroundColor $Colors.Dim
            }
        }

        Write-Host " ║" -NoNewline -ForegroundColor $Colors.Primary
        $percent = [math]::Floor(($pos / $width) * 100)
        Write-Host " $percent%" -NoNewline -ForegroundColor $Colors.Info

        Start-Sleep -Milliseconds ([math]::Floor($Duration * 1000 / $width))
    }

    # Finaliza a barra completa
    Write-Host "`r  ║ " -NoNewline -ForegroundColor $Colors.Primary
    Write-Host ($scanChar * $width) -NoNewline -ForegroundColor $Colors.Success
    Write-Host " ║" -NoNewline -ForegroundColor $Colors.Primary
    Write-Host " 100% ✓" -ForegroundColor $Colors.Success

    Write-Host "  ╚$("═" * ($width + 2))╝" -ForegroundColor $Colors.Primary
    Write-Host ""
}

# ============================================================================
# RESULTADO DETALHADO
# ============================================================================

function Show-CheckResult {
    param(
        [string]$Component,
        [bool]$Found,
        [string]$Version = "",
        [string]$Details = ""
    )

    $status = if ($Found) { "[✓]" } else { "[✗]" }
    $statusColor = if ($Found) { $Colors.Success } else { $Colors.Error }
    $statusText = if ($Found) { "OK" } else { "NAO ENCONTRADO" }

    Write-Host "  ║ $status " -NoNewline -ForegroundColor $statusColor
    Write-Host $Component.PadRight(20) -NoNewline -ForegroundColor $Colors.Info

    if ($Version) {
        Write-Host "│ " -NoNewline -ForegroundColor $Colors.Dim
        Write-Host $Version.PadRight(18) -NoNewline -ForegroundColor $Colors.Secondary
    } else {
        Write-Host "│ " -NoNewline -ForegroundColor $Colors.Dim
        Write-Host $statusText.PadRight(18) -NoNewline -ForegroundColor $statusColor
    }

    Write-Host "│ " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host $Details.PadRight(20) -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "║" -ForegroundColor $Colors.Primary
}

# ============================================================================
# TABELA DE RESULTADOS
# ============================================================================

function Show-ResultsTable {
    param([array]$Results)

    Write-Host ""
    Write-Host "  ╔════════════════════════╤════════════════════╤══════════════════════╗" -ForegroundColor $Colors.Primary
    Write-Host "  ║ " -NoNewline -ForegroundColor $Colors.Primary
    Write-Host "COMPONENTE".PadRight(22) -NoNewline -ForegroundColor $Colors.Info
    Write-Host "│ " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "VERSAO/STATUS".PadRight(18) -NoNewline -ForegroundColor $Colors.Info
    Write-Host "│ " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "DETALHES".PadRight(20) -NoNewline -ForegroundColor $Colors.Info
    Write-Host "║" -ForegroundColor $Colors.Primary
    Write-Host "  ╠════════════════════════╪════════════════════╪══════════════════════╣" -ForegroundColor $Colors.Primary

    foreach ($result in $Results) {
        Show-CheckResult -Component $result.Component -Found $result.Found -Version $result.Version -Details $result.Details
    }

    Write-Host "  ╚════════════════════════╧════════════════════╧══════════════════════╝" -ForegroundColor $Colors.Primary
    Write-Host ""
}

# ============================================================================
# LOGICA PRINCIPAL
# ============================================================================

Show-ScannerHeader

Write-Host "  [?] " -NoNewline -ForegroundColor $Colors.Secondary
Write-Host "Iniciando verificacao do sistema..." -ForegroundColor $Colors.Info
Write-Host ""

Show-ScanningAnimation 2

Write-Host ""
Show-AdvancedSpinner -Message "Verificando instalacao do Python" -Duration 1 -Style "Braille"

# Verifica se Python esta disponivel
$results = @()

try {
    $result = py --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python nao encontrado" }

    $pythonVersion = $result
    $results += @{ Component = "Python"; Found = $true; Version = $pythonVersion; Details = "Instalado" }

} catch {
    $results += @{ Component = "Python"; Found = $false; Version = ""; Details = "Necessario" }

    Show-ErrorBox "Python nao encontrado!" "O Python e necessario para executar este programa." "https://www.python.org/downloads/"
    Show-InfoBox "Durante a instalacao, marque 'Add Python to PATH'"

    Write-Host ""
    Write-GradientLine "=" 76
    Write-Host ""
    Read-Host "  Pressione Enter para sair"
    exit 1
}

# Verifica modulos Python
$modules = @(
    @{ Name = "PySide6"; DisplayName = "PySide6 (Qt6)"; Required = $true },
    @{ Name = "requests"; DisplayName = "Requests"; Required = $true },
    @{ Name = "psutil"; DisplayName = "PSUtil"; Required = $true },
    @{ Name = "colorama"; DisplayName = "Colorama"; Required = $true },
    @{ Name = "pyinstaller"; DisplayName = "PyInstaller"; Required = $false }
)

foreach ($module in $modules) {
    Show-AdvancedSpinner -Message "Verificando $($module.DisplayName)" -Duration 0.5 -Style "Dots"

    $checkResult = py -c "import $($module.Name); print($($module.Name).__version__ if hasattr($($module.Name), '__version__') else 'OK')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        $version = $checkResult.Trim()
        $results += @{
            Component = $module.DisplayName
            Found = $true
            Version = $version
            Details = if ($module.Required) { "Requerido" } else { "Opcional" }
        }
    } else {
        $results += @{
            Component = $module.DisplayName
            Found = $false
            Version = ""
            Details = if ($module.Required) { "REQUERIDO!" } else { "Opcional" }
        }
    }
}

# Exibe tabela de resultados
Write-Host ""
Write-GradientLine -Char "═" -Length 76
Write-CenteredText "RESULTADOS DA VERIFICACAO" $Colors.Primary 76
Write-GradientLine -Char "─" -Length 76

Show-ResultsTable -Results $results

# Conta os que faltam
$missing = ($results | Where-Object { -not $_.Found -and $_.Details -eq "REQUERIDO!" }).Count
$total = $results.Count
$found = ($results | Where-Object { $_.Found }).Count

# Barra de status geral
Write-Host "  ┌─────────────────────────────────────────────────────────────────────┐" -ForegroundColor $Colors.Dim
Write-Host "  │  Status: " -NoNewline -ForegroundColor $Colors.Dim
Write-Host "$found/$total componentes verificados" -NoNewline -ForegroundColor $Colors.Info
if ($missing -gt 0) {
    Write-Host " | " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "$missing faltando" -NoNewline -ForegroundColor $Colors.Error
}
$padding = if ($missing -gt 0) { 25 } else { 40 }
Write-Host (" " * $padding) -NoNewline
Write-Host "│" -ForegroundColor $Colors.Dim
Write-Host "  └─────────────────────────────────────────────────────────────────────┘" -ForegroundColor $Colors.Dim

Write-Host ""
Write-Host "  [*] " -NoNewline -ForegroundColor $Colors.Primary
Write-Host "Executando verificacao detalhada via Python..." -ForegroundColor $Colors.Info
Write-Host ""
Write-GradientLine -Char "─" -Length 76
Write-Host ""

# Executa o script Python com cores
Set-Location (Join-Path $ScriptDir "src")
py verificar_sistema.py --auto-instalar

$exitCode = $LASTEXITCODE

Write-Host ""
Write-GradientLine -Char "─" -Length 76

if ($exitCode -eq 0) {
    Show-SuccessBox "Verificacao concluida com sucesso!" -Animated
} else {
    Show-ErrorBox "Verificacao encontrou problemas." "Codigo de saida: $exitCode"
}

Write-Host ""
Write-GradientLine -Char "═" -Length 76
Write-Host ""
Read-Host "  Pressione Enter para sair"

# Retorna o codigo de saida do script Python
exit $exitCode
