# ============================================================================
#                 GAME TRANSLATOR - VERIFICACAO DO SISTEMA v2.0.1
#                     Visual Moderno com Animacoes
# ============================================================================
# Requer PowerShell 5.1 ou superior

$Host.UI.RawUI.WindowTitle = "Game Translator - Verificacao do Sistema"
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

function Show-ScanAnimation {
    param([int]$Duration = 2)
    $frames = @(
        "  [#         ] 10%  ",
        "  [##        ] 20%  ",
        "  [###       ] 30%  ",
        "  [####      ] 40%  ",
        "  [#####     ] 50%  ",
        "  [######    ] 60%  ",
        "  [#######   ] 70%  ",
        "  [########  ] 80%  ",
        "  [######### ] 90%  ",
        "  [##########] 100% "
    )
    
    foreach ($frame in $frames) {
        Write-Host "`r$frame" -NoNewline -ForegroundColor $Colors.Primary
        Start-Sleep -Milliseconds ($Duration * 100)
    }
    Write-Host ""
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
    Write-Host "`r  [+] $Message                              " -ForegroundColor $Colors.Success
}

function Show-Header {
    Clear-Host
    Write-Host ""
    Write-GradientLine "=" 76
    Write-Host ""
    
    $magnifier = @(
        "         (?) ",
        "        /    ",
        "       O     ",
        "      /|\    ",
        "      / \    "
    )
    
    foreach ($line in $magnifier) {
        Write-CenteredText $line "Cyan" 76
        Start-Sleep -Milliseconds 80
    }
    
    Write-Host ""
    Write-CenteredText "============================================================" "DarkGray" 76
    Write-Host ""
    Write-CenteredText "GAME TRANSLATOR" "Cyan" 76
    Write-CenteredText "Verificacao do Sistema" "DarkCyan" 76
    Write-Host ""
    Write-CenteredText "============================================================" "DarkGray" 76
    Write-Host ""
}

function Show-ErrorBox {
    param([string]$Message, [string]$SubMessage = "", [string]$Link = "")
    Write-Host ""
    Write-Host "  +===================================================================+" -ForegroundColor $Colors.Error
    Write-Host "  |                                                                   |" -ForegroundColor $Colors.Error
    Write-Host "  |  [X] " -NoNewline -ForegroundColor $Colors.Error
    Write-Host $Message.PadRight(59) -NoNewline -ForegroundColor "White"
    Write-Host "|" -ForegroundColor $Colors.Error
    if ($SubMessage) {
        Write-Host "  |                                                                   |" -ForegroundColor $Colors.Error
        Write-Host "  |      " -NoNewline -ForegroundColor $Colors.Error
        Write-Host $SubMessage.PadRight(59) -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "|" -ForegroundColor $Colors.Error
    }
    if ($Link) {
        Write-Host "  |                                                                   |" -ForegroundColor $Colors.Error
        Write-Host "  |  [>] " -NoNewline -ForegroundColor $Colors.Error
        Write-Host $Link.PadRight(59) -NoNewline -ForegroundColor $Colors.Primary
        Write-Host "|" -ForegroundColor $Colors.Error
    }
    Write-Host "  |                                                                   |" -ForegroundColor $Colors.Error
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

# ============================================================================
# LOGICA PRINCIPAL
# ============================================================================

Show-Header

Write-Host "  [?] Iniciando verificacao do sistema..." -ForegroundColor $Colors.Info
Write-Host ""

Show-ScanAnimation 1

Write-Host ""
Show-Spinner "Verificando instalacao do Python" 1

# Verifica se Python esta disponivel
try {
    $result = py --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Python nao encontrado" }
    
    $pythonVersion = $result
    Write-Host ""
    Write-Host "  +-------------------------------------------------------------------+" -ForegroundColor $Colors.Success
    Write-Host "  |  [*] Python encontrado: " -NoNewline -ForegroundColor $Colors.Success
    Write-Host "$pythonVersion".PadRight(40) -NoNewline -ForegroundColor $Colors.Info
    Write-Host "|" -ForegroundColor $Colors.Success
    Write-Host "  +-------------------------------------------------------------------+" -ForegroundColor $Colors.Success
    Write-Host ""
    
} catch {
    Show-ErrorBox "Python nao encontrado!" "O Python e necessario para executar este programa." "https://www.python.org/downloads/"
    Show-InfoBox "Durante a instalacao, marque 'Add Python to PATH'"
    
    Write-Host ""
    Write-GradientLine "=" 76
    Write-Host ""
    Read-Host "  Pressione Enter para sair"
    exit 1
}

Write-Host "  [*] Executando verificacao detalhada..." -ForegroundColor $Colors.Info
Write-Host ""
Write-GradientLine "-" 76
Write-Host ""

# Executa o script Python com cores
Set-Location (Join-Path $ScriptDir "src")
py verificar_sistema.py --auto-instalar

$exitCode = $LASTEXITCODE

Write-Host ""
Write-GradientLine "-" 76

if ($exitCode -eq 0) {
    Show-SuccessBox "Verificacao concluida com sucesso!"
} else {
    Show-ErrorBox "Verificacao encontrou problemas." "Codigo de saida: $exitCode"
}

Write-Host ""
Write-GradientLine "=" 76
Write-Host ""
Read-Host "  Pressione Enter para sair"

# Retorna o codigo de saida do script Python
exit $exitCode
