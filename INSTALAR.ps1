# ============================================================================
#                    GAME TRANSLATOR - INSTALADOR v3.0.0
#                     Visual Ultra Moderno com Animacoes
# ============================================================================
# Requer PowerShell 5.1 ou superior

$Host.UI.RawUI.WindowTitle = "Game Translator - Instalador v3.0.0"
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
Set-UITheme -ThemeName "Cyberpunk" | Out-Null

# ============================================================================
# CONFIGURACAO DE CORES LOCAIS (fallback do modulo)
# ============================================================================

$script:LocalColors = $Colors

# ============================================================================
# FUNCOES UTILITARIAS
# ============================================================================

function Test-Python {
    try {
        $result = py --version 2>&1
        if ($LASTEXITCODE -eq 0) { return $true }
    } catch {}
    return $false
}

function Clear-TempFiles {
    param([bool]$Silent = $false)

    $totalRemoved = 0
    $foldersToRemove = @("build", "dist", "__pycache__", "src\__pycache__", "src\gui\__pycache__")

    foreach ($folder in $foldersToRemove) {
        $folderPath = Join-Path $ScriptDir $folder
        if (Test-Path $folderPath) {
            try {
                Remove-Item -Path $folderPath -Recurse -Force -ErrorAction Stop
                if (-not $Silent) { Write-SubStepSuccess "Removido: $folder" }
                $totalRemoved++
            } catch {
                if (-not $Silent) { Write-SubStepError "Falha: $folder" }
            }
        }
    }

    # Remove arquivos .spec
    Get-ChildItem -Path $ScriptDir -Filter "*.spec" -ErrorAction SilentlyContinue | ForEach-Object {
        try {
            Remove-Item -Path $_.FullName -Force
            if (-not $Silent) { Write-SubStepSuccess "Removido: $($_.Name)" }
            $totalRemoved++
        } catch {}
    }

    # Remove __pycache__ recursivamente
    Get-ChildItem -Path $ScriptDir -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue | ForEach-Object {
        try {
            Remove-Item -Path $_.FullName -Recurse -Force
            $totalRemoved++
        } catch {}
    }

    # Remove .pyc e .pyo
    Get-ChildItem -Path $ScriptDir -Include "*.pyc", "*.pyo" -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
        try {
            Remove-Item -Path $_.FullName -Force
            $totalRemoved++
        } catch {}
    }

    return $totalRemoved
}

# ============================================================================
# LOGO ANIMADO ESPECIAL
# ============================================================================

function Show-InstallerLogo {
    Clear-Host
    Write-Host ""
    Write-GradientLine -Char "═" -Length 80 -Animated

    Write-Host ""
    Write-WelcomeAnimation -Duration 800

    $logo = @(
        "   ██████╗  █████╗ ███╗   ███╗███████╗",
        "  ██╔════╝ ██╔══██╗████╗ ████║██╔════╝",
        "  ██║  ███╗███████║██╔████╔██║█████╗  ",
        "  ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  ",
        "  ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗",
        "   ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝"
    )

    $translator = @(
        " ████████╗██████╗  █████╗ ███╗   ██╗███████╗██╗      █████╗ ████████╗ ██████╗ ██████╗ ",
        " ╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗",
        "    ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     ███████║   ██║   ██║   ██║██████╔╝",
        "    ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗",
        "    ██║   ██║  ██║██║  ██║██║ ╚████║███████║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║",
        "    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝"
    )

    $logoColors = @("Magenta", "Yellow", "Cyan", "Yellow", "Magenta", "Cyan")

    for ($i = 0; $i -lt $logo.Count; $i++) {
        Write-CenteredText $logo[$i] $logoColors[$i] 80
        Start-Sleep -Milliseconds 40
    }

    Write-Host ""

    for ($i = 0; $i -lt $translator.Count; $i++) {
        Write-CenteredText $translator[$i] $logoColors[$i] 95
        Start-Sleep -Milliseconds 40
    }

    Write-Host ""
    Write-GradientLine -Char "─" -Length 80
    Write-CenteredText "Sistema Profissional de Traducao para Jogos e Mods" "White" 80
    Write-CenteredText "Versao 3.0.0 | PowerShell Ultra Edition" "DarkGray" 80
    Write-GradientLine -Char "═" -Length 80
    Write-Host ""
}

# ============================================================================
# MENU PRINCIPAL ESTILIZADO
# ============================================================================

function Show-MainMenu {
    Show-InstallerLogo

    $menuItems = @(
        @{ Key = "1"; Icon = "▶▶"; Text = "Instalacao Completa"; Extra = "(Recomendado)" },
        @{ Key = "2"; Icon = "??"; Text = "Verificar Requisitos"; Extra = "" },
        @{ Key = "3"; Icon = "◆◆"; Text = "Instalar Dependencias"; Extra = "" },
        @{ Key = "4"; Icon = "██"; Text = "Criar Executavel (.exe)"; Extra = "" },
        @{ Key = "5"; Icon = "▷ "; Text = "Executar Programa"; Extra = "(Dev Mode)" },
        @{ Key = "6"; Icon = "~~"; Text = "Limpar Arquivos Temporarios"; Extra = "" },
        @{ Key = "7"; Icon = "◇◇"; Text = "Trocar Tema de Cores"; Extra = "" },
        @{ Key = "8"; Icon = "[]"; Text = "Limpar Tela"; Extra = "" },
        @{ Key = "0"; Icon = "←←"; Text = "Sair"; Extra = "" }
    )

    Show-StylizedMenu -MenuItems $menuItems -Title "★ MENU PRINCIPAL ★" -Width 70
}

# ============================================================================
# FUNCOES DO MENU
# ============================================================================

function Install-Complete {
    Show-SectionHeader "Instalacao Completa" "▶▶"

    Write-PulseText "Iniciando instalacao completa..." 2 80

    Write-Step 1 5 "Verificando Python..."
    Show-AdvancedSpinner -Message "Procurando Python no sistema" -Duration 1 -Style "Braille"

    if (-not (Test-Python)) {
        Show-ErrorBox "Python nao encontrado!" "Instale em: https://www.python.org/downloads/"
        Show-InfoBox "Durante a instalacao, marque 'Add Python to PATH'"
        Read-Host "  Pressione Enter para continuar"
        return
    }

    $pythonVersion = py --version 2>&1
    Write-SubStepSuccess "$pythonVersion encontrado"
    Show-ParticleExplosion -Duration 200 -Width 40

    Write-Step 2 5 "Limpando arquivos temporarios anteriores..."
    $removed = Clear-TempFiles -Silent $true
    Write-SubStepSuccess "Removidos $removed itens temporarios"

    Write-Step 3 5 "Instalando dependencias..."
    Write-Host ""

    Show-AdvancedSpinner -Message "Atualizando pip" -Duration 1 -Style "Dots"
    py -m pip install --upgrade pip --quiet 2>$null
    Write-SubStepSuccess "pip atualizado"

    $deps = @(
        @{ Name = "PySide6"; Desc = "Interface Grafica Qt6" },
        @{ Name = "requests"; Desc = "Requisicoes HTTP" },
        @{ Name = "psutil"; Desc = "Utilitarios do Sistema" },
        @{ Name = "colorama"; Desc = "Cores no Terminal" },
        @{ Name = "pyinstaller"; Desc = "Criador de Executaveis" }
    )

    foreach ($dep in $deps) {
        Write-SubStep "Instalando $($dep.Name)" "($($dep.Desc))"
        py -m pip install $dep.Name --quiet 2>$null
        Write-Host "`r       [✓] $($dep.Name) instalado                              " -ForegroundColor Green
    }

    Show-GradientProgressBar -Message "Preparando ambiente de compilacao..." -Steps 25 -Delay 30

    Write-Step 4 5 "Criando executavel..."
    Show-InfoBox "Isso pode levar alguns minutos, aguarde..."

    Write-WaveText "Compilando Game Translator"

    Set-Location $ScriptDir
    $srcPath = Join-Path $ScriptDir "src"
    $mainPath = Join-Path $srcPath "main.py"

    py -m PyInstaller --name="GameTranslator" --onefile --windowed --noconfirm --clean `
        --paths="$srcPath" `
        --hidden-import=PySide6.QtCore `
        --hidden-import=PySide6.QtGui `
        --hidden-import=PySide6.QtWidgets `
        --hidden-import=sqlite3 `
        --hidden-import=psutil `
        --add-data "src;src" `
        "$mainPath" 2>$null

    Write-Step 5 5 "Verificando resultado e limpando temporarios..."

    $exePath = Join-Path $ScriptDir "dist\GameTranslator.exe"

    if (Test-Path $exePath) {
        # Limpa temporarios mantendo dist/
        if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
        Get-ChildItem -Path $ScriptDir -Filter "*.spec" -ErrorAction SilentlyContinue | Remove-Item -Force
        Get-ChildItem -Path $ScriptDir -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force

        Show-SuccessBox "INSTALACAO CONCLUIDA COM SUCESSO!" $exePath -Animated

        $fileInfo = Get-Item $exePath
        $fileSize = [math]::Round($fileInfo.Length / 1MB, 2)

        Write-Host "  ╔═══════════════════════════════════════════╗" -ForegroundColor $Colors.Primary
        Write-Host "  ║  " -NoNewline -ForegroundColor $Colors.Primary
        Write-Host "Informacoes do Executavel:" -NoNewline -ForegroundColor White
        Write-Host "               ║" -ForegroundColor $Colors.Primary
        Write-Host "  ║  → Tamanho: " -NoNewline -ForegroundColor $Colors.Primary
        Write-Host "$fileSize MB".PadRight(30) -NoNewline -ForegroundColor $Colors.Secondary
        Write-Host "║" -ForegroundColor $Colors.Primary
        Write-Host "  ║  → Criado:  " -NoNewline -ForegroundColor $Colors.Primary
        Write-Host "$($fileInfo.CreationTime.ToString('dd/MM/yyyy HH:mm'))".PadRight(30) -NoNewline -ForegroundColor $Colors.Secondary
        Write-Host "║" -ForegroundColor $Colors.Primary
        Write-Host "  ╚═══════════════════════════════════════════╝" -ForegroundColor $Colors.Primary

        Write-Host ""
        Write-Host "  Deseja abrir o programa agora? " -NoNewline -ForegroundColor $Colors.Info
        Write-Host "(S/N) " -NoNewline -ForegroundColor $Colors.Secondary
        $response = Read-Host
        if ($response -match "^[SsYy]$") {
            Start-Process $exePath
        }
    } else {
        Show-ErrorBox "Falha ao criar executavel!" "Verifique os erros acima."
    }

    Write-Host ""
    Read-Host "  Pressione Enter para continuar"
}

function Test-Requirements {
    Show-SectionHeader "Verificacao de Requisitos" "??"

    Write-PulseText "Iniciando verificacao do sistema..." 2 100

    if (-not (Test-Python)) {
        Show-ErrorBox "Python nao encontrado!" "Instale em: https://www.python.org/downloads/"
        Read-Host "  Pressione Enter para continuar"
        return
    }

    Show-MultiColorProgressBar -Message "Analisando sistema..." -Steps 25

    Set-Location (Join-Path $ScriptDir "src")
    py verificar_sistema.py
    Set-Location $ScriptDir

    Write-Host ""
    Read-Host "  Pressione Enter para continuar"
}

function Install-Dependencies {
    Show-SectionHeader "Instalacao de Dependencias" "◆◆"

    if (-not (Test-Python)) {
        Show-ErrorBox "Python nao encontrado!"
        Read-Host "  Pressione Enter para continuar"
        return
    }

    $steps = @(
        @{ Name = "pip"; Cmd = "py -m pip install --upgrade pip"; Icon = "↑" },
        @{ Name = "PySide6"; Cmd = "py -m pip install PySide6"; Icon = "◆" },
        @{ Name = "requests"; Cmd = "py -m pip install requests"; Icon = "◆" },
        @{ Name = "psutil e colorama"; Cmd = "py -m pip install psutil colorama"; Icon = "◆" },
        @{ Name = "PyInstaller"; Cmd = "py -m pip install pyinstaller"; Icon = "◆" }
    )

    for ($i = 0; $i -lt $steps.Count; $i++) {
        Write-Step ($i + 1) $steps.Count "Instalando $($steps[$i].Name)..."
        Show-AdvancedSpinner -Message "Baixando pacotes" -Duration 1 -Style "Bounce"
        Invoke-Expression $steps[$i].Cmd 2>$null
        Write-SubStepSuccess "$($steps[$i].Name) instalado com sucesso"
    }

    Show-SuccessBox "Todas as dependencias foram instaladas!" -Animated
    Read-Host "  Pressione Enter para continuar"
}

function Build-Executable {
    Show-SectionHeader "Criacao do Executavel" "██"

    if (-not (Test-Python)) {
        Show-ErrorBox "Python nao encontrado!"
        Read-Host "  Pressione Enter para continuar"
        return
    }

    Write-Step 1 3 "Limpando arquivos temporarios anteriores..."
    Clear-TempFiles -Silent $true
    Write-SubStepSuccess "Arquivos temporarios removidos"

    Write-Step 2 3 "Criando executavel..."
    Show-InfoBox "Isso pode levar alguns minutos..."

    Show-AnimatedProgressBar -Task "Compilando" -TargetPercent 100 -BarWidth 30

    Set-Location $ScriptDir
    $srcPath = Join-Path $ScriptDir "src"
    $mainPath = Join-Path $srcPath "main.py"

    py -m PyInstaller --name="GameTranslator" --onefile --windowed --noconfirm --clean `
        --paths="$srcPath" `
        --hidden-import=PySide6.QtCore `
        --hidden-import=PySide6.QtGui `
        --hidden-import=PySide6.QtWidgets `
        --hidden-import=sqlite3 `
        --hidden-import=psutil `
        --add-data "src;src" `
        "$mainPath" 2>$null

    Write-Step 3 3 "Finalizando..."

    $exePath = Join-Path $ScriptDir "dist\GameTranslator.exe"

    if (Test-Path $exePath) {
        if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
        Get-ChildItem -Path $ScriptDir -Filter "*.spec" -ErrorAction SilentlyContinue | Remove-Item -Force
        Get-ChildItem -Path $ScriptDir -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force

        Show-SuccessBox "Executavel criado com sucesso!" $exePath -Animated

        Write-Host "  Abrir pasta do executavel? " -NoNewline -ForegroundColor $Colors.Info
        Write-Host "(S/N) " -NoNewline -ForegroundColor $Colors.Secondary
        $response = Read-Host
        if ($response -match "^[SsYy]$") {
            explorer (Join-Path $ScriptDir "dist")
        }
    } else {
        Show-ErrorBox "Falha ao criar executavel!"
    }

    Read-Host "  Pressione Enter para continuar"
}

function Start-Program {
    Show-SectionHeader "Executar Programa" "▷"

    if (-not (Test-Python)) {
        Show-ErrorBox "Python nao encontrado!"
        Read-Host "  Pressione Enter para continuar"
        return
    }

    Write-TypewriterText "Iniciando Game Translator em modo desenvolvimento..." $Colors.Primary 15 1

    Show-GradientProgressBar -Message "Carregando modulos..." -Steps 20 -Delay 25

    Set-Location (Join-Path $ScriptDir "src")
    py main.py

    Write-Host ""
    Read-Host "  Pressione Enter para continuar"
}

function Show-CleanMenu {
    Show-SectionHeader "Limpeza de Arquivos Temporarios" "~~"

    Write-Host "  Esta funcao remove os seguintes arquivos/pastas:" -ForegroundColor $Colors.Info
    Write-Host ""

    $items = @(
        @{ Type = "DIR "; Name = "build/"; Desc = "pasta de compilacao do PyInstaller" },
        @{ Type = "DIR "; Name = "dist/"; Desc = "pasta do executavel gerado" },
        @{ Type = "DIR "; Name = "__pycache__/"; Desc = "cache do Python" },
        @{ Type = "FILE"; Name = "*.spec"; Desc = "arquivos de especificacao" },
        @{ Type = "FILE"; Name = "*.pyc / *.pyo"; Desc = "arquivos compilados" }
    )

    foreach ($item in $items) {
        Write-Host "    [$($item.Type)] " -NoNewline -ForegroundColor $Colors.Warning
        Write-Host $item.Name.PadRight(18) -NoNewline -ForegroundColor $Colors.Secondary
        Write-Host "($($item.Desc))" -ForegroundColor $Colors.Dim
    }

    Write-Host ""
    Write-Host "  Deseja continuar? " -NoNewline -ForegroundColor $Colors.Info
    Write-Host "(S/N) " -NoNewline -ForegroundColor $Colors.Secondary
    $response = Read-Host

    if ($response -match "^[SsYy]$") {
        Write-Host ""
        Show-AdvancedSpinner -Message "Removendo arquivos" -Duration 1 -Style "Blocks"
        $removed = Clear-TempFiles -Silent $false
        Show-SuccessBox "Limpeza concluida!" "Total de $removed itens removidos"
    } else {
        Show-InfoBox "Limpeza cancelada pelo usuario."
    }

    Read-Host "  Pressione Enter para continuar"
}

function Show-ThemeSelector {
    Show-SectionHeader "Selecionar Tema de Cores" "◇◇"

    $themes = Get-AvailableThemes
    $currentTheme = Get-UITheme

    Write-Host "  Tema atual: " -NoNewline -ForegroundColor $Colors.Info
    Write-Host $currentTheme -ForegroundColor $Colors.Secondary
    Write-Host ""
    Write-Host "  Temas disponiveis:" -ForegroundColor $Colors.Info
    Write-Host ""

    $themeDescriptions = @{
        "Neon" = "Magenta e Cyan vibrantes"
        "Ocean" = "Tons de azul e ciano"
        "Sunset" = "Amarelo, vermelho e magenta"
        "Matrix" = "Verde estilo hacker"
        "Cyberpunk" = "Magenta, amarelo e ciano"
        "Arctic" = "Branco e azul gelado"
    }

    $i = 1
    foreach ($theme in $themes) {
        Write-Host "    [$i] " -NoNewline -ForegroundColor $Colors.Dim
        Write-Host $theme.PadRight(12) -NoNewline -ForegroundColor $Colors.Secondary
        Write-Host "- $($themeDescriptions[$theme])" -ForegroundColor $Colors.Dim
        $i++
    }

    Write-Host ""
    Write-Host "  Digite o numero do tema (ou Enter para cancelar): " -NoNewline -ForegroundColor $Colors.Info
    $choice = Read-Host

    if ($choice -match "^\d+$") {
        $index = [int]$choice - 1
        $themeList = @($themes)
        if ($index -ge 0 -and $index -lt $themeList.Count) {
            $selectedTheme = $themeList[$index]
            Set-UITheme -ThemeName $selectedTheme | Out-Null
            Show-SuccessBox "Tema alterado para: $selectedTheme"
        } else {
            Show-ErrorBox "Opcao invalida!"
        }
    }

    Read-Host "  Pressione Enter para continuar"
}

# ============================================================================
# LOOP PRINCIPAL
# ============================================================================

do {
    Show-MainMenu
    Write-Host "  Digite sua opcao: " -NoNewline -ForegroundColor $Colors.Info
    $option = Read-Host

    switch ($option) {
        "1" { Install-Complete }
        "2" { Test-Requirements }
        "3" { Install-Dependencies }
        "4" { Build-Executable }
        "5" { Start-Program }
        "6" { Show-CleanMenu }
        "7" { Show-ThemeSelector }
        "8" { Clear-Host }
        "0" {
            Show-ExitAnimation
            exit 0
        }
        default {
            Show-ErrorBox "Opcao invalida!" "Por favor, escolha uma opcao de 0 a 8."
            Start-Sleep -Seconds 2
        }
    }
} while ($true)
