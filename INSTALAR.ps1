# ============================================================================
#                    GAME TRANSLATOR - INSTALADOR v2.0.1
#                     Visual Moderno com Animacoes
# ============================================================================
# Requer PowerShell 5.1 ou superior

$Host.UI.RawUI.WindowTitle = "Game Translator - Instalador v2.0.1"
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
    Highlight  = "DarkCyan"
    Dim        = "DarkGray"
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# ============================================================================
# FUNCOES DE ANIMACAO E VISUAL
# ============================================================================

function Write-AnimatedText {
    param(
        [string]$Text,
        [string]$Color = "White",
        [int]$Delay = 5
    )
    foreach ($char in $Text.ToCharArray()) {
        Write-Host $char -NoNewline -ForegroundColor $Color
        Start-Sleep -Milliseconds $Delay
    }
    Write-Host ""
}

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
    param(
        [string]$Text,
        [string]$Color = "White",
        [int]$Width = 76
    )
    $padding = [math]::Max(0, ($Width - $Text.Length) / 2)
    Write-Host (" " * $padding) -NoNewline
    Write-Host $Text -ForegroundColor $Color
}

function Show-Spinner {
    param(
        [string]$Message,
        [int]$Duration = 3
    )
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

function Show-ProgressAnimation {
    param(
        [string]$Task,
        [int]$Steps = 20
    )
    Write-Host ""
    Write-Host "  $Task" -ForegroundColor $Colors.Info
    Write-Host "  [" -NoNewline -ForegroundColor $Colors.Dim
    
    for ($i = 0; $i -lt $Steps; $i++) {
        Write-Host "#" -NoNewline -ForegroundColor $Colors.Primary
        Start-Sleep -Milliseconds 50
    }
    
    Write-Host "] " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "100%" -ForegroundColor $Colors.Success
}

function Show-Logo {
    Clear-Host
    Write-Host ""
    Write-GradientLine "=" 76
    Write-Host ""
    
    $logo = @(
        "   ####    ###   ##   ## #######",
        "  ##      ## ##  ### ### ##     ",
        "  ## ### ##   ## ## # ## #####  ",
        "  ##  ## ####### ##   ## ##     ",
        "   ####  ##   ## ##   ## #######",
        "",
        "  ####### ####    ###   ##   ##  #### ##       ###   ####### #####  ####  ",
        "     ##   ##  ## ## ##  ###  ## ##    ##      ## ##     ##  ##   ## ##  ## ",
        "     ##   ####   #####  ## # ##  ###  ##      #####     ##  ##   ## ####   ",
        "     ##   ## ##  ##  ## ##  ###    ## ##      ##  ##    ##  ##   ## ## ##  ",
        "     ##   ##  ## ##  ## ##   ## ####  ####### ##  ##    ##   #####  ##  ## "
    )
    
    $logoColors = @("Cyan", "Cyan", "DarkCyan", "Blue", "DarkBlue", 
                    "Magenta", "Magenta", "Magenta", "DarkMagenta", "DarkMagenta", "DarkMagenta")
    
    for ($i = 0; $i -lt $logo.Count; $i++) {
        Write-CenteredText $logo[$i] $logoColors[$i] 90
        Start-Sleep -Milliseconds 30
    }
    
    Write-Host ""
    Write-CenteredText "============================================================" "DarkGray" 90
    Write-CenteredText "Sistema Profissional de Traducao para Jogos e Mods" "White" 90
    Write-CenteredText "Versao 2.0.1 | PowerShell Edition" "DarkGray" 90
    Write-CenteredText "============================================================" "DarkGray" 90
    Write-Host ""
}

function Show-Menu {
    Show-Logo
    
    Write-Host ""
    Write-Host "  +---------------------------------------------------------------------+" -ForegroundColor $Colors.Accent
    Write-Host "  |                         " -NoNewline -ForegroundColor $Colors.Accent
    Write-Host "MENU PRINCIPAL" -NoNewline -ForegroundColor $Colors.Primary
    Write-Host "                            |" -ForegroundColor $Colors.Accent
    Write-Host "  +---------------------------------------------------------------------+" -ForegroundColor $Colors.Accent
    Write-Host "  |                                                                     |" -ForegroundColor $Colors.Accent
    
    # Opcoes do menu
    $menuItems = @(
        @{ Key = "1"; Icon = ">>"; Text = "Instalacao Completa"; Extra = "(Recomendado)" },
        @{ Key = "2"; Icon = "??"; Text = "Verificar Requisitos"; Extra = "" },
        @{ Key = "3"; Icon = "[]"; Text = "Instalar Dependencias"; Extra = "" },
        @{ Key = "4"; Icon = "##"; Text = "Criar Executavel (.exe)"; Extra = "" },
        @{ Key = "5"; Icon = "> "; Text = "Executar Programa"; Extra = "(Dev Mode)" },
        @{ Key = "6"; Icon = "~~"; Text = "Limpar Arquivos Temporarios"; Extra = "" },
        @{ Key = "7"; Icon = "<>"; Text = "Gerenciar Backups"; Extra = "" },
        @{ Key = "8"; Icon = "[="; Text = "Informacoes do Sistema"; Extra = "" },
        @{ Key = "9"; Icon = "[]"; Text = "Limpar Tela do Terminal"; Extra = "" },
        @{ Key = "0"; Icon = "<-"; Text = "Sair"; Extra = "" }
    )
    
    foreach ($item in $menuItems) {
        Write-Host "  |    [" -NoNewline -ForegroundColor $Colors.Accent
        Write-Host $item.Key -NoNewline -ForegroundColor $Colors.Primary
        Write-Host "] " -NoNewline -ForegroundColor $Colors.Accent
        Write-Host "$($item.Icon) " -NoNewline -ForegroundColor $Colors.Secondary
        Write-Host $item.Text -NoNewline -ForegroundColor $Colors.Info
        if ($item.Extra) {
            Write-Host " $($item.Extra)" -NoNewline -ForegroundColor $Colors.Dim
        }
        $padding = 53 - $item.Text.Length - $item.Extra.Length
        Write-Host (" " * [math]::Max(1, $padding)) -NoNewline
        Write-Host "|" -ForegroundColor $Colors.Accent
    }
    
    Write-Host "  |                                                                     |" -ForegroundColor $Colors.Accent
    Write-Host "  +---------------------------------------------------------------------+" -ForegroundColor $Colors.Accent
    Write-Host ""
}

function Show-SectionHeader {
    param([string]$Title, [string]$Icon = "*")
    
    Clear-Host
    Write-Host ""
    Write-GradientLine "=" 76
    Write-Host ""
    Write-Host "  [$Icon] " -NoNewline -ForegroundColor $Colors.Primary
    Write-Host $Title.ToUpper() -ForegroundColor $Colors.Info
    Write-Host ""
    Write-GradientLine "-" 76
    Write-Host ""
}

function Show-SuccessBox {
    param([string]$Message, [string]$SubMessage = "")
    
    Write-Host ""
    Write-Host "  +===================================================================+" -ForegroundColor $Colors.Success
    Write-Host "  |                                                                   |" -ForegroundColor $Colors.Success
    Write-Host "  |  [OK] " -NoNewline -ForegroundColor $Colors.Success
    Write-Host $Message.PadRight(58) -NoNewline -ForegroundColor "White"
    Write-Host "|" -ForegroundColor $Colors.Success
    if ($SubMessage) {
        Write-Host "  |       " -NoNewline -ForegroundColor $Colors.Success
        Write-Host $SubMessage.PadRight(58) -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "|" -ForegroundColor $Colors.Success
    }
    Write-Host "  |                                                                   |" -ForegroundColor $Colors.Success
    Write-Host "  +===================================================================+" -ForegroundColor $Colors.Success
    Write-Host ""
}

function Show-ErrorBox {
    param([string]$Message, [string]$SubMessage = "")
    
    Write-Host ""
    Write-Host "  +===================================================================+" -ForegroundColor $Colors.Error
    Write-Host "  |                                                                   |" -ForegroundColor $Colors.Error
    Write-Host "  |  [X] " -NoNewline -ForegroundColor $Colors.Error
    Write-Host $Message.PadRight(59) -NoNewline -ForegroundColor "White"
    Write-Host "|" -ForegroundColor $Colors.Error
    if ($SubMessage) {
        Write-Host "  |      " -NoNewline -ForegroundColor $Colors.Error
        Write-Host $SubMessage.PadRight(59) -NoNewline -ForegroundColor $Colors.Dim
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

function Write-Step {
    param(
        [int]$Current,
        [int]$Total,
        [string]$Message
    )
    Write-Host ""
    Write-Host "  [$Current/$Total] " -NoNewline -ForegroundColor $Colors.Primary
    Write-Host $Message -ForegroundColor $Colors.Info
}

function Write-SubStep {
    param([string]$Message, [string]$Status = "...")
    Write-Host "       -> " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host $Message -NoNewline -ForegroundColor $Colors.Info
    Write-Host " $Status" -ForegroundColor $Colors.Dim
}

function Write-SubStepSuccess {
    param([string]$Message)
    Write-Host "       [+] " -NoNewline -ForegroundColor $Colors.Success
    Write-Host $Message -ForegroundColor $Colors.Info
}

function Write-SubStepError {
    param([string]$Message)
    Write-Host "       [X] " -NoNewline -ForegroundColor $Colors.Error
    Write-Host $Message -ForegroundColor $Colors.Info
}

# ============================================================================
# FUNCOES DE LOG E SISTEMA
# ============================================================================

$script:LogFile = Join-Path $ScriptDir "game_translator.log"

function Write-Log {
    param(
        [string]$Message,
        [ValidateSet("INFO", "SUCCESS", "WARNING", "ERROR")]
        [string]$Level = "INFO"
    )

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"

    try {
        Add-Content -Path $script:LogFile -Value $logEntry -ErrorAction SilentlyContinue
    } catch {}
}

function Test-PowerShellVersion {
    $minVersion = [Version]"5.1"
    $currentVersion = $PSVersionTable.PSVersion

    if ($currentVersion -lt $minVersion) {
        Write-Host ""
        Write-Host "  [!] " -NoNewline -ForegroundColor $Colors.Warning
        Write-Host "PowerShell $currentVersion detectado. Recomendado: 5.1+" -ForegroundColor $Colors.Warning
        Write-Log "PowerShell versao $currentVersion (minimo recomendado: 5.1)" "WARNING"
        return $false
    }
    return $true
}

function Show-Notification {
    param(
        [string]$Title = "Game Translator",
        [string]$Message,
        [ValidateSet("Success", "Error", "Warning", "Info")]
        [string]$Type = "Info"
    )

    # Som de notificacao
    switch ($Type) {
        "Success" { [System.Media.SystemSounds]::Asterisk.Play() }
        "Error"   { [System.Media.SystemSounds]::Hand.Play() }
        "Warning" { [System.Media.SystemSounds]::Exclamation.Play() }
        default   { [System.Media.SystemSounds]::Beep.Play() }
    }

    # Notificacao Toast do Windows (se disponivel)
    try {
        $null = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]
        $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
        $textNodes = $template.GetElementsByTagName("text")
        $textNodes.Item(0).AppendChild($template.CreateTextNode($Title)) | Out-Null
        $textNodes.Item(1).AppendChild($template.CreateTextNode($Message)) | Out-Null
        $toast = [Windows.UI.Notifications.ToastNotification]::new($template)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Game Translator").Show($toast)
    } catch {
        # Notificacao nao suportada, apenas usa o som
    }
}

function Get-DiskSpaceInfo {
    param([string]$Path = $ScriptDir)

    try {
        $drive = (Get-Item $Path).PSDrive
        $freeSpace = [math]::Round($drive.Free / 1GB, 2)
        $totalSpace = [math]::Round(($drive.Used + $drive.Free) / 1GB, 2)
        $usedPercent = [math]::Round(($drive.Used / ($drive.Used + $drive.Free)) * 100, 1)

        return @{
            Drive = $drive.Name
            FreeGB = $freeSpace
            TotalGB = $totalSpace
            UsedPercent = $usedPercent
        }
    } catch {
        return $null
    }
}

function Test-DiskSpace {
    param([int]$RequiredMB = 500)

    $diskInfo = Get-DiskSpaceInfo
    if ($diskInfo) {
        $freeSpaceMB = $diskInfo.FreeGB * 1024
        if ($freeSpaceMB -lt $RequiredMB) {
            Write-Host ""
            Write-Host "  [!] " -NoNewline -ForegroundColor $Colors.Warning
            Write-Host "Espaco em disco baixo: $($diskInfo.FreeGB) GB livres" -ForegroundColor $Colors.Warning
            Write-Log "Espaco em disco baixo: $($diskInfo.FreeGB) GB" "WARNING"
            return $false
        }
    }
    return $true
}

function Show-DiskSpaceBar {
    $diskInfo = Get-DiskSpaceInfo
    if ($diskInfo) {
        Write-Host ""
        Write-Host "  [*] Espaco em disco ($($diskInfo.Drive):):" -ForegroundColor $Colors.Info

        $barLength = 30
        $usedBlocks = [math]::Floor($diskInfo.UsedPercent / 100 * $barLength)
        $freeBlocks = $barLength - $usedBlocks

        $usedColor = if ($diskInfo.UsedPercent -gt 90) { "Red" }
                     elseif ($diskInfo.UsedPercent -gt 70) { "Yellow" }
                     else { "Cyan" }

        Write-Host "      [" -NoNewline -ForegroundColor $Colors.Dim
        Write-Host ("#" * $usedBlocks) -NoNewline -ForegroundColor $usedColor
        Write-Host ("." * $freeBlocks) -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "] " -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "$($diskInfo.UsedPercent)% usado" -NoNewline -ForegroundColor $Colors.Info
        Write-Host " | $($diskInfo.FreeGB) GB livres" -ForegroundColor $Colors.Success
    }
}

function New-DesktopShortcut {
    param(
        [string]$TargetPath,
        [string]$ShortcutName = "Game Translator"
    )

    try {
        $desktopPath = [Environment]::GetFolderPath("Desktop")
        $shortcutPath = Join-Path $desktopPath "$ShortcutName.lnk"

        $shell = New-Object -ComObject WScript.Shell
        $shortcut = $shell.CreateShortcut($shortcutPath)
        $shortcut.TargetPath = $TargetPath
        $shortcut.WorkingDirectory = Split-Path $TargetPath
        $shortcut.Description = "Game Translator - Sistema de Traducao"
        $shortcut.Save()

        Write-Log "Atalho criado na area de trabalho: $shortcutPath" "SUCCESS"
        return $true
    } catch {
        Write-Log "Falha ao criar atalho: $_" "ERROR"
        return $false
    }
}

function Backup-Configurations {
    $backupDir = Join-Path $ScriptDir "backups"
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupPath = Join-Path $backupDir "backup_$timestamp"

    try {
        if (-not (Test-Path $backupDir)) {
            New-Item -Path $backupDir -ItemType Directory -Force | Out-Null
        }

        New-Item -Path $backupPath -ItemType Directory -Force | Out-Null

        # Backup de perfis
        $profilesDir = Join-Path $ScriptDir "profiles"
        if (Test-Path $profilesDir) {
            Copy-Item -Path $profilesDir -Destination $backupPath -Recurse -Force
        }

        # Backup de configuracoes src (apenas .json e .ini)
        $configFiles = Get-ChildItem -Path $ScriptDir -Include "*.json", "*.ini" -Recurse -ErrorAction SilentlyContinue
        foreach ($file in $configFiles) {
            $destPath = Join-Path $backupPath $file.Name
            Copy-Item -Path $file.FullName -Destination $destPath -Force
        }

        Write-Log "Backup criado: $backupPath" "SUCCESS"
        return $backupPath
    } catch {
        Write-Log "Falha no backup: $_" "ERROR"
        return $null
    }
}

function Restore-LatestBackup {
    $backupDir = Join-Path $ScriptDir "backups"

    if (-not (Test-Path $backupDir)) {
        return $null
    }

    $latestBackup = Get-ChildItem -Path $backupDir -Directory |
                    Sort-Object CreationTime -Descending |
                    Select-Object -First 1

    if ($latestBackup) {
        return $latestBackup.FullName
    }
    return $null
}

function Show-BackupMenu {
    Show-SectionHeader "Gerenciamento de Backups" "[]"

    $backupDir = Join-Path $ScriptDir "backups"

    Write-Host "  [1] Criar novo backup" -ForegroundColor $Colors.Info
    Write-Host "  [2] Listar backups existentes" -ForegroundColor $Colors.Info
    Write-Host "  [3] Restaurar ultimo backup" -ForegroundColor $Colors.Info
    Write-Host "  [0] Voltar" -ForegroundColor $Colors.Dim
    Write-Host ""
    Write-Host "  Escolha uma opcao: " -NoNewline -ForegroundColor $Colors.Info
    $choice = Read-Host

    switch ($choice) {
        "1" {
            Write-Host ""
            Show-Spinner "Criando backup" 2
            $result = Backup-Configurations
            if ($result) {
                Show-SuccessBox "Backup criado com sucesso!" $result
                Show-Notification -Message "Backup criado com sucesso!" -Type "Success"
            } else {
                Show-ErrorBox "Falha ao criar backup!"
            }
        }
        "2" {
            Write-Host ""
            if (Test-Path $backupDir) {
                $backups = Get-ChildItem -Path $backupDir -Directory | Sort-Object CreationTime -Descending
                if ($backups.Count -gt 0) {
                    Write-Host "  Backups encontrados:" -ForegroundColor $Colors.Info
                    Write-Host ""
                    foreach ($backup in $backups) {
                        $size = (Get-ChildItem $backup.FullName -Recurse | Measure-Object -Property Length -Sum).Sum / 1KB
                        Write-Host "    [*] " -NoNewline -ForegroundColor $Colors.Primary
                        Write-Host "$($backup.Name)" -NoNewline -ForegroundColor $Colors.Info
                        Write-Host " ($([math]::Round($size, 2)) KB)" -ForegroundColor $Colors.Dim
                    }
                } else {
                    Show-InfoBox "Nenhum backup encontrado."
                }
            } else {
                Show-InfoBox "Pasta de backups nao existe."
            }
        }
        "3" {
            $latestBackup = Restore-LatestBackup
            if ($latestBackup) {
                Write-Host ""
                Write-Host "  Restaurar backup: " -NoNewline -ForegroundColor $Colors.Info
                Write-Host (Split-Path $latestBackup -Leaf) -ForegroundColor $Colors.Primary
                Write-Host "  Confirmar? (S/N): " -NoNewline -ForegroundColor $Colors.Warning
                $confirm = Read-Host
                if ($confirm -match "^[SsYy]$") {
                    # Restaurar profiles
                    $profilesBackup = Join-Path $latestBackup "profiles"
                    if (Test-Path $profilesBackup) {
                        Copy-Item -Path $profilesBackup -Destination $ScriptDir -Recurse -Force
                        Show-SuccessBox "Backup restaurado!"
                        Write-Log "Backup restaurado de: $latestBackup" "SUCCESS"
                    }
                }
            } else {
                Show-InfoBox "Nenhum backup disponivel para restaurar."
            }
        }
    }

    Write-Host ""
    Read-Host "  Pressione Enter para continuar"
}

function Show-SystemInfo {
    Show-SectionHeader "Informacoes do Sistema" "[="

    # Informacoes do PowerShell
    Write-Host "  [*] PowerShell:" -ForegroundColor $Colors.Info
    Write-Host "      Versao: " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "$($PSVersionTable.PSVersion)" -ForegroundColor $Colors.Primary
    Write-Host "      Edicao: " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "$($PSVersionTable.PSEdition)" -ForegroundColor $Colors.Primary
    Write-Host ""

    # Informacoes do Sistema Operacional
    Write-Host "  [*] Sistema Operacional:" -ForegroundColor $Colors.Info
    try {
        $os = Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction SilentlyContinue
        if ($os) {
            Write-Host "      Nome: " -NoNewline -ForegroundColor $Colors.Dim
            Write-Host "$($os.Caption)" -ForegroundColor $Colors.Primary
            Write-Host "      Versao: " -NoNewline -ForegroundColor $Colors.Dim
            Write-Host "$($os.Version)" -ForegroundColor $Colors.Primary
            Write-Host "      Arquitetura: " -NoNewline -ForegroundColor $Colors.Dim
            Write-Host "$($os.OSArchitecture)" -ForegroundColor $Colors.Primary
        }
    } catch {
        Write-Host "      Nao foi possivel obter informacoes do SO" -ForegroundColor $Colors.Dim
    }
    Write-Host ""

    # Informacoes de Memoria
    Write-Host "  [*] Memoria:" -ForegroundColor $Colors.Info
    try {
        $mem = Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction SilentlyContinue
        if ($mem) {
            $totalMem = [math]::Round($mem.TotalVisibleMemorySize / 1MB, 2)
            $freeMem = [math]::Round($mem.FreePhysicalMemory / 1MB, 2)
            $usedMem = $totalMem - $freeMem
            $usedPercent = [math]::Round(($usedMem / $totalMem) * 100, 1)

            $memColor = if ($usedPercent -gt 90) { "Red" }
                        elseif ($usedPercent -gt 70) { "Yellow" }
                        else { "Green" }

            Write-Host "      Total: " -NoNewline -ForegroundColor $Colors.Dim
            Write-Host "$totalMem GB" -ForegroundColor $Colors.Primary
            Write-Host "      Em uso: " -NoNewline -ForegroundColor $Colors.Dim
            Write-Host "$usedMem GB ($usedPercent%)" -ForegroundColor $memColor
            Write-Host "      Livre: " -NoNewline -ForegroundColor $Colors.Dim
            Write-Host "$freeMem GB" -ForegroundColor $Colors.Success
        }
    } catch {
        Write-Host "      Nao foi possivel obter informacoes de memoria" -ForegroundColor $Colors.Dim
    }
    Write-Host ""

    # Espaco em Disco
    Show-DiskSpaceBar
    Write-Host ""

    # Python
    Write-Host "  [*] Python:" -ForegroundColor $Colors.Info
    if (Test-Python) {
        $pythonVersion = py --version 2>&1
        Write-Host "      Versao: " -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "$pythonVersion" -ForegroundColor $Colors.Success

        # Verificar pip
        try {
            $pipVersion = py -m pip --version 2>&1
            Write-Host "      Pip: " -NoNewline -ForegroundColor $Colors.Dim
            Write-Host "$($pipVersion -replace 'pip ', '' -replace ' from.*', '')" -ForegroundColor $Colors.Primary
        } catch {}
    } else {
        Write-Host "      Status: " -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "Nao instalado" -ForegroundColor $Colors.Error
    }
    Write-Host ""

    # Projeto
    Write-Host "  [*] Projeto Game Translator:" -ForegroundColor $Colors.Info
    Write-Host "      Diretorio: " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "$ScriptDir" -ForegroundColor $Colors.Primary

    $exePath = Join-Path $ScriptDir "dist\GameTranslator.exe"
    if (Test-Path $exePath) {
        $exeInfo = Get-Item $exePath
        Write-Host "      Executavel: " -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "Encontrado ($([math]::Round($exeInfo.Length / 1MB, 2)) MB)" -ForegroundColor $Colors.Success
    } else {
        Write-Host "      Executavel: " -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "Nao compilado" -ForegroundColor $Colors.Warning
    }

    # Backups
    $backupDir = Join-Path $ScriptDir "backups"
    if (Test-Path $backupDir) {
        $backupCount = (Get-ChildItem -Path $backupDir -Directory).Count
        Write-Host "      Backups: " -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "$backupCount backup(s) disponivel(is)" -ForegroundColor $Colors.Primary
    }

    # Log
    if (Test-Path $script:LogFile) {
        $logInfo = Get-Item $script:LogFile
        Write-Host "      Log: " -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "$([math]::Round($logInfo.Length / 1KB, 2)) KB" -ForegroundColor $Colors.Primary
    }

    Write-Host ""
    Write-GradientLine "-" 76
    Write-Host ""
    Read-Host "  Pressione Enter para continuar"
}

# ============================================================================
# FUNCOES UTILITARIAS
# ============================================================================

function Test-Python {
    try {
        $result = py --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
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
# FUNCOES PRINCIPAIS DO MENU
# ============================================================================

function Install-Complete {
    Show-SectionHeader "Instalacao Completa" ">>"

    Write-Log "Iniciando instalacao completa" "INFO"

    # Verificar versao do PowerShell
    Test-PowerShellVersion | Out-Null

    # Verificar espaco em disco
    Write-Host "  [*] Verificando espaco em disco..." -ForegroundColor $Colors.Info
    Show-DiskSpaceBar
    if (-not (Test-DiskSpace -RequiredMB 500)) {
        Write-Host ""
        Write-Host "  [!] " -NoNewline -ForegroundColor $Colors.Warning
        Write-Host "Espaco em disco pode ser insuficiente." -ForegroundColor $Colors.Warning
        Write-Host "  Continuar mesmo assim? " -NoNewline -ForegroundColor $Colors.Info
        Write-Host "(S/N) " -NoNewline -ForegroundColor $Colors.Primary
        $continue = Read-Host
        if ($continue -notmatch "^[SsYy]$") {
            Write-Log "Instalacao cancelada - espaco em disco insuficiente" "WARNING"
            return
        }
    }
    Write-Host ""

    Write-Step 1 6 "Verificando Python..."
    Start-Sleep -Milliseconds 500

    if (-not (Test-Python)) {
        Show-ErrorBox "Python nao encontrado!" "Instale em: https://www.python.org/downloads/"
        Show-InfoBox "Durante a instalacao, marque 'Add Python to PATH'"
        Write-Log "Python nao encontrado" "ERROR"
        Read-Host "  Pressione Enter para continuar"
        return
    }

    $pythonVersion = py --version 2>&1
    Write-SubStepSuccess "$pythonVersion encontrado"
    Write-Log "Python encontrado: $pythonVersion" "SUCCESS"

    Write-Step 2 6 "Limpando arquivos temporarios anteriores..."
    $removed = Clear-TempFiles -Silent $true
    Write-SubStepSuccess "Removidos $removed itens temporarios"

    Write-Step 3 6 "Instalando dependencias..."
    Write-Host ""

    Write-SubStep "Atualizando pip"
    py -m pip install --upgrade pip --quiet 2>$null
    Write-SubStepSuccess "pip atualizado"

    $deps = @("PySide6", "requests", "psutil", "colorama", "pyinstaller")
    foreach ($dep in $deps) {
        Write-SubStep "Instalando $dep"
        py -m pip install $dep --quiet 2>$null
        Write-SubStepSuccess "$dep instalado"
        Write-Log "Dependencia instalada: $dep" "INFO"
    }

    Write-Step 4 6 "Criando executavel..."
    Show-InfoBox "Isso pode levar alguns minutos, aguarde..."

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

    Write-Step 5 6 "Verificando resultado e limpando temporarios..."

    $exePath = Join-Path $ScriptDir "dist\GameTranslator.exe"

    if (Test-Path $exePath) {
        # Limpa temporarios mantendo dist/
        if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
        Get-ChildItem -Path $ScriptDir -Filter "*.spec" -ErrorAction SilentlyContinue | Remove-Item -Force
        Get-ChildItem -Path $ScriptDir -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force

        $exeInfo = Get-Item $exePath
        Write-Log "Executavel criado: $exePath ($([math]::Round($exeInfo.Length / 1MB, 2)) MB)" "SUCCESS"

        Show-SuccessBox "INSTALACAO CONCLUIDA COM SUCESSO!" $exePath
        Show-Notification -Message "Instalacao concluida com sucesso!" -Type "Success"

        Write-Step 6 6 "Opcoes pos-instalacao..."
        Write-Host ""

        # Opcao de criar atalho
        Write-Host "  Criar atalho na area de trabalho? " -NoNewline -ForegroundColor $Colors.Info
        Write-Host "(S/N) " -NoNewline -ForegroundColor $Colors.Primary
        $createShortcut = Read-Host
        if ($createShortcut -match "^[SsYy]$") {
            if (New-DesktopShortcut -TargetPath $exePath) {
                Write-SubStepSuccess "Atalho criado na area de trabalho!"
            } else {
                Write-SubStepError "Falha ao criar atalho"
            }
        }

        Write-Host ""
        Write-Host "  Deseja abrir o programa agora? " -NoNewline -ForegroundColor $Colors.Info
        Write-Host "(S/N) " -NoNewline -ForegroundColor $Colors.Primary
        $response = Read-Host
        if ($response -match "^[SsYy]$") {
            Start-Process $exePath
            Write-Log "Programa iniciado pelo usuario" "INFO"
        }
    } else {
        Show-ErrorBox "Falha ao criar executavel!" "Verifique os erros acima."
        Show-Notification -Message "Falha na instalacao!" -Type "Error"
        Write-Log "Falha ao criar executavel" "ERROR"
    }

    Write-Host ""
    Read-Host "  Pressione Enter para continuar"
}

function Test-Requirements {
    Show-SectionHeader "Verificacao de Requisitos" "??"
    
    if (-not (Test-Python)) {
        Show-ErrorBox "Python nao encontrado!" "Instale em: https://www.python.org/downloads/"
        Read-Host "  Pressione Enter para continuar"
        return
    }
    
    Set-Location (Join-Path $ScriptDir "src")
    py verificar_sistema.py
    Set-Location $ScriptDir
    
    Write-Host ""
    Read-Host "  Pressione Enter para continuar"
}

function Install-Dependencies {
    Show-SectionHeader "Instalacao de Dependencias" "[]"
    
    if (-not (Test-Python)) {
        Show-ErrorBox "Python nao encontrado!"
        Read-Host "  Pressione Enter para continuar"
        return
    }
    
    $steps = @(
        @{ Name = "pip"; Cmd = "py -m pip install --upgrade pip" },
        @{ Name = "PySide6"; Cmd = "py -m pip install PySide6" },
        @{ Name = "requests"; Cmd = "py -m pip install requests" },
        @{ Name = "psutil e colorama"; Cmd = "py -m pip install psutil colorama" },
        @{ Name = "PyInstaller"; Cmd = "py -m pip install pyinstaller" }
    )
    
    for ($i = 0; $i -lt $steps.Count; $i++) {
        Write-Step ($i + 1) $steps.Count "Instalando $($steps[$i].Name)..."
        Invoke-Expression $steps[$i].Cmd 2>$null
        Write-SubStepSuccess "$($steps[$i].Name) instalado com sucesso"
    }
    
    Show-SuccessBox "Todas as dependencias foram instaladas!"
    Read-Host "  Pressione Enter para continuar"
}

function Build-Executable {
    Show-SectionHeader "Criacao do Executavel" "##"
    
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
        
        Show-SuccessBox "Executavel criado com sucesso!" $exePath
        
        Write-Host "  Abrir pasta do executavel? " -NoNewline -ForegroundColor $Colors.Info
        Write-Host "(S/N) " -NoNewline -ForegroundColor $Colors.Primary
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
    Show-SectionHeader "Executar Programa" "> "
    
    if (-not (Test-Python)) {
        Show-ErrorBox "Python nao encontrado!"
        Read-Host "  Pressione Enter para continuar"
        return
    }
    
    Write-Host "  [*] Iniciando Game Translator..." -ForegroundColor $Colors.Primary
    Write-Host ""
    
    Set-Location (Join-Path $ScriptDir "src")
    py main.py
    
    Write-Host ""
    Read-Host "  Pressione Enter para continuar"
}

function Show-CleanMenu {
    Show-SectionHeader "Limpeza de Arquivos Temporarios" "~~"
    
    Write-Host "  Esta funcao remove os seguintes arquivos/pastas:" -ForegroundColor $Colors.Info
    Write-Host ""
    Write-Host "    [DIR] build/          " -NoNewline -ForegroundColor $Colors.Warning
    Write-Host "(pasta de compilacao do PyInstaller)" -ForegroundColor $Colors.Dim
    Write-Host "    [DIR] dist/           " -NoNewline -ForegroundColor $Colors.Warning
    Write-Host "(pasta do executavel gerado)" -ForegroundColor $Colors.Dim
    Write-Host "    [DIR] __pycache__/    " -NoNewline -ForegroundColor $Colors.Warning
    Write-Host "(cache do Python)" -ForegroundColor $Colors.Dim
    Write-Host "    [FILE] *.spec         " -NoNewline -ForegroundColor $Colors.Warning
    Write-Host "(arquivos de especificacao)" -ForegroundColor $Colors.Dim
    Write-Host "    [FILE] *.pyc / *.pyo  " -NoNewline -ForegroundColor $Colors.Warning
    Write-Host "(arquivos compilados)" -ForegroundColor $Colors.Dim
    Write-Host ""
    
    Write-Host "  Deseja continuar? " -NoNewline -ForegroundColor $Colors.Info
    Write-Host "(S/N) " -NoNewline -ForegroundColor $Colors.Primary
    $response = Read-Host
    
    if ($response -match "^[SsYy]$") {
        Write-Host ""
        $removed = Clear-TempFiles -Silent $false
        Show-SuccessBox "Limpeza concluida!" "Total de $removed itens removidos"
    } else {
        Show-InfoBox "Limpeza cancelada pelo usuario."
    }
    
    Read-Host "  Pressione Enter para continuar"
}

function Show-ExitAnimation {
    Clear-Host
    Write-Host ""
    Write-Host ""
    Write-CenteredText "+=========================================================+" "Cyan" 76
    Write-CenteredText "|                                                         |" "Cyan" 76
    Write-CenteredText "|      Obrigado por usar o Game Translator!               |" "Cyan" 76
    Write-CenteredText "|                                                         |" "Cyan" 76
    Write-CenteredText "|              Ate a proxima!                             |" "Cyan" 76
    Write-CenteredText "|                                                         |" "Cyan" 76
    Write-CenteredText "+=========================================================+" "Cyan" 76
    Write-Host ""
    
    # Animacao de saida
    $dots = @(".", "..", "...", "....", ".....")
    foreach ($dot in $dots) {
        Write-Host "`r                    Encerrando$dot" -NoNewline -ForegroundColor $Colors.Dim
        Start-Sleep -Milliseconds 300
    }
    Write-Host ""
}

# ============================================================================
# LOOP PRINCIPAL
# ============================================================================

do {
    Show-Menu
    Write-Host "  Digite sua opcao: " -NoNewline -ForegroundColor $Colors.Info
    $option = Read-Host
    
    switch ($option) {
        "1" { Install-Complete }
        "2" { Test-Requirements }
        "3" { Install-Dependencies }
        "4" { Build-Executable }
        "5" { Start-Program }
        "6" { Show-CleanMenu }
        "7" { Show-BackupMenu }
        "8" { Show-SystemInfo }
        "9" { Clear-Host }
        "0" {
            Show-ExitAnimation
            exit 0
        }
        default {
            Show-ErrorBox "Opcao invalida!" "Por favor, escolha uma opcao de 0 a 9."
            Start-Sleep -Seconds 2
        }
    }
} while ($true)
