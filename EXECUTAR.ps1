# ============================================================================
#                    GAME TRANSLATOR - EXECUCAO RAPIDA v2.0.1
#                     Visual Moderno com Animacoes
# ============================================================================
# Requer PowerShell 5.1 ou superior

$Host.UI.RawUI.WindowTitle = "Game Translator - Execucao Rapida"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# ============================================================================
# CONFIGURACAO DE CORES MODERNAS
# ============================================================================
$script:Colors = @{
    Primary    = "Cyan"
    Secondary  = "Magenta"
    Success    = "Green"
    Error      = "Red"
    Warning    = "Yellow"
    Info       = "White"
    Accent     = "Blue"
    Dim        = "DarkGray"
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# ============================================================================
# FUNCOES DE ANIMACAO E VISUAL
# ============================================================================

function Write-GradientLine {
    param([string]$Char = "=", [int]$Length = 76)
    $colors = @("DarkBlue", "Blue", "Cyan", "DarkCyan", "Cyan", "Blue", "DarkBlue")
    $segmentLength = [math]::Ceiling($Length / $colors.Count)
    
    for ($i = 0; $i -lt $colors.Count; $i++) {
        $remaining = $Length - ($i * $segmentLength)
        $currentLength = [math]::Min($segmentLength, $remaining)
        if ($currentLength -gt 0) {
            Write-Host ($Char * $currentLength) -NoNewline -ForegroundColor $colors[$i]
        }
    }
    Write-Host ""
}

function Write-CenteredText {
    param([string]$Text, [string]$Color = "White", [int]$Width = 76)
    $padding = [math]::Max(0, ($Width - $Text.Length) / 2)
    Write-Host (" " * $padding) -NoNewline
    Write-Host $Text -ForegroundColor $Color
}

function Show-Spinner {
    param([string]$Message, [int]$Duration = 2)
    $spinChars = @("|", "/", "-", "\")
    $endTime = (Get-Date).AddSeconds($Duration)
    $i = 0
    
    while ((Get-Date) -lt $endTime) {
        Write-Host "`r  [$($spinChars[$i % $spinChars.Count])] $Message" -NoNewline -ForegroundColor $Colors.Primary
        Start-Sleep -Milliseconds 100
        $i++
    }
    Write-Host "`r  [+] $Message                    " -ForegroundColor $Colors.Success
}

function Show-LoadingBar {
    param([string]$Message, [int]$Steps = 30)
    Write-Host ""
    Write-Host "  $Message" -ForegroundColor $Colors.Info
    Write-Host "  [" -NoNewline -ForegroundColor $Colors.Dim
    
    for ($i = 0; $i -lt $Steps; $i++) {
        $color = if ($i -lt $Steps/3) { "DarkCyan" } elseif ($i -lt $Steps*2/3) { "Cyan" } else { "White" }
        Write-Host "#" -NoNewline -ForegroundColor $color
        Start-Sleep -Milliseconds 30
    }
    
    Write-Host "] " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "OK!" -ForegroundColor $Colors.Success
}

function Show-Header {
    Clear-Host
    Write-Host ""
    Write-GradientLine "=" 76
    Write-Host ""
    
    $rocket = @(
        "                    /\  ",
        "                   /  \ ",
        "                  / || \ ",
        "                 /  ||  \ ",
        "                /_______\ ",
        "                   || ",
        "                  /||\ ",
        "                 * ** *"
    )
    
    foreach ($line in $rocket) {
        Write-CenteredText $line "Cyan" 76
        Start-Sleep -Milliseconds 50
    }
    
    Write-Host ""
    Write-CenteredText "============================================================" "DarkGray" 76
    Write-Host ""
    Write-CenteredText "GAME TRANSLATOR" "Cyan" 76
    Write-CenteredText "Execucao Rapida" "DarkCyan" 76
    Write-Host ""
    Write-CenteredText "============================================================" "DarkGray" 76
    Write-Host ""
}

function Show-SuccessBox {
    param([string]$Message)
    Write-Host ""
    Write-Host "  +===================================================================+" -ForegroundColor $Colors.Success
    Write-Host "  |  [OK] " -NoNewline -ForegroundColor $Colors.Success
    Write-Host $Message.PadRight(58) -NoNewline -ForegroundColor "White"
    Write-Host "|" -ForegroundColor $Colors.Success
    Write-Host "  +===================================================================+" -ForegroundColor $Colors.Success
    Write-Host ""
}

function Show-ErrorBox {
    param([string]$Message, [string]$SubMessage = "")
    Write-Host ""
    Write-Host "  +===================================================================+" -ForegroundColor $Colors.Error
    Write-Host "  |  [X] " -NoNewline -ForegroundColor $Colors.Error
    Write-Host $Message.PadRight(59) -NoNewline -ForegroundColor "White"
    Write-Host "|" -ForegroundColor $Colors.Error
    if ($SubMessage) {
        Write-Host "  |      " -NoNewline -ForegroundColor $Colors.Error
        Write-Host $SubMessage.PadRight(59) -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "|" -ForegroundColor $Colors.Error
    }
    Write-Host "  +===================================================================+" -ForegroundColor $Colors.Error
    Write-Host ""
}

function Show-InfoBox {
    param([string]$Message)
    Write-Host ""
    Write-Host "  +-------------------------------------------------------------------+" -ForegroundColor $Colors.Primary
    Write-Host "  |  [i] " -NoNewline -ForegroundColor $Colors.Primary
    Write-Host $Message.PadRight(59) -NoNewline -ForegroundColor $Colors.Info
    Write-Host "|" -ForegroundColor $Colors.Primary
    Write-Host "  +-------------------------------------------------------------------+" -ForegroundColor $Colors.Primary
    Write-Host ""
}

function Write-SubStep {
    param([string]$Message, [string]$Status = "")
    Write-Host "     -> " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host $Message -NoNewline -ForegroundColor $Colors.Info
    if ($Status) { Write-Host " $Status" -ForegroundColor $Colors.Dim }
    else { Write-Host "" }
}

function Write-SubStepSuccess {
    param([string]$Message)
    Write-Host "     [+] " -NoNewline -ForegroundColor $Colors.Success
    Write-Host $Message -ForegroundColor $Colors.Info
}

# ============================================================================
# LOGICA PRINCIPAL
# ============================================================================

Show-Header

$ExePath = Join-Path $ScriptDir "dist\GameTranslator.exe"

# Verifica se o executavel existe
if (Test-Path $ExePath) {
    Show-Spinner "Localizando executavel" 1
    Write-SubStepSuccess "Executavel encontrado!"
    Write-Host ""
    
    Show-LoadingBar "Iniciando Game Translator..." 25
    
    Write-Host ""
    Write-Host "  [*] " -NoNewline -ForegroundColor $Colors.Primary
    Write-Host "Abrindo aplicacao..." -ForegroundColor $Colors.Info
    
    Start-Process $ExePath
    
    Show-SuccessBox "Game Translator iniciado com sucesso!"
    
    # Animacao de saida
    Write-Host "  Fechando em " -NoNewline -ForegroundColor $Colors.Dim
    for ($i = 3; $i -ge 1; $i--) {
        Write-Host "$i " -NoNewline -ForegroundColor $Colors.Primary
        Start-Sleep -Seconds 1
    }
    Write-Host ""
    exit 0
}

# Se nao existe, tenta via Python
Write-Host "  [!] " -NoNewline -ForegroundColor $Colors.Warning
Write-Host "Executavel nao encontrado. Iniciando via Python..." -ForegroundColor $Colors.Warning
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
Write-Host "  [*] Verificando dependencias..." -ForegroundColor $Colors.Info
Write-Host ""

# Verifica e instala dependencias se necessario
$dependencies = @("PySide6", "requests", "psutil", "colorama")

foreach ($dep in $dependencies) {
    Write-SubStep "Verificando $dep..."
    $checkCmd = "import $dep"
    $result = py -c $checkCmd 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`r     -> Instalando $dep...          " -NoNewline -ForegroundColor $Colors.Warning
        py -m pip install $dep --quiet 2>$null
        Write-Host "`r     [+] $dep instalado              " -ForegroundColor $Colors.Success
    } else {
        Write-Host "`r     [+] $dep OK                     " -ForegroundColor $Colors.Success
    }
}

Write-Host ""
Show-SuccessBox "Dependencias verificadas!"

Show-LoadingBar "Iniciando Game Translator..." 25

Write-Host ""
Write-Host "  [*] " -NoNewline -ForegroundColor $Colors.Primary
Write-Host "Executando aplicacao..." -ForegroundColor $Colors.Info
Write-Host ""
Write-GradientLine "-" 76
Write-Host ""

Set-Location (Join-Path $ScriptDir "src")
py main.py

Write-Host ""
Write-GradientLine "-" 76
Write-Host ""
Write-Host "  [*] " -NoNewline -ForegroundColor $Colors.Primary
Write-Host "Programa encerrado." -ForegroundColor $Colors.Info
Write-Host ""
Read-Host "  Pressione Enter para sair"
