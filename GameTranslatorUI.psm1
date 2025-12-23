# ============================================================================
#                    GAME TRANSLATOR - UI MODULE v3.0.0
#                     Modulo Visual Avancado com Animacoes
# ============================================================================
# Este modulo contem funcoes visuais compartilhadas para todos os scripts PS1
# Requer PowerShell 5.1 ou superior

# ============================================================================
# TEMAS DE CORES - Escolha seu estilo!
# ============================================================================

$script:Themes = @{
    "Neon" = @{
        Primary    = "Magenta"
        Secondary  = "Cyan"
        Tertiary   = "Yellow"
        Success    = "Green"
        Error      = "Red"
        Warning    = "Yellow"
        Info       = "White"
        Accent     = "Blue"
        Highlight  = "DarkMagenta"
        Dim        = "DarkGray"
        Gradient   = @("DarkMagenta", "Magenta", "Cyan", "DarkCyan", "Cyan", "Magenta", "DarkMagenta")
    }
    "Ocean" = @{
        Primary    = "Cyan"
        Secondary  = "Blue"
        Tertiary   = "DarkCyan"
        Success    = "Green"
        Error      = "Red"
        Warning    = "Yellow"
        Info       = "White"
        Accent     = "DarkBlue"
        Highlight  = "DarkCyan"
        Dim        = "DarkGray"
        Gradient   = @("DarkBlue", "Blue", "DarkCyan", "Cyan", "DarkCyan", "Blue", "DarkBlue")
    }
    "Sunset" = @{
        Primary    = "Yellow"
        Secondary  = "Red"
        Tertiary   = "Magenta"
        Success    = "Green"
        Error      = "Red"
        Warning    = "Yellow"
        Info       = "White"
        Accent     = "DarkRed"
        Highlight  = "DarkYellow"
        Dim        = "DarkGray"
        Gradient   = @("DarkRed", "Red", "Yellow", "White", "Yellow", "Red", "DarkRed")
    }
    "Matrix" = @{
        Primary    = "Green"
        Secondary  = "DarkGreen"
        Tertiary   = "White"
        Success    = "Green"
        Error      = "Red"
        Warning    = "Yellow"
        Info       = "Green"
        Accent     = "DarkGreen"
        Highlight  = "Green"
        Dim        = "DarkGray"
        Gradient   = @("Black", "DarkGreen", "Green", "White", "Green", "DarkGreen", "Black")
    }
    "Cyberpunk" = @{
        Primary    = "Magenta"
        Secondary  = "Yellow"
        Tertiary   = "Cyan"
        Success    = "Green"
        Error      = "Red"
        Warning    = "Yellow"
        Info       = "White"
        Accent     = "DarkMagenta"
        Highlight  = "Cyan"
        Dim        = "DarkGray"
        Gradient   = @("DarkMagenta", "Magenta", "Yellow", "Cyan", "Yellow", "Magenta", "DarkMagenta")
    }
    "Arctic" = @{
        Primary    = "White"
        Secondary  = "Cyan"
        Tertiary   = "Blue"
        Success    = "Green"
        Error      = "Red"
        Warning    = "Yellow"
        Info       = "White"
        Accent     = "DarkCyan"
        Highlight  = "Cyan"
        Dim        = "DarkGray"
        Gradient   = @("DarkBlue", "Blue", "Cyan", "White", "Cyan", "Blue", "DarkBlue")
    }
}

# Tema ativo (pode ser alterado)
$script:ActiveTheme = "Neon"
$script:Colors = $script:Themes[$script:ActiveTheme]

# ============================================================================
# FUNCAO PARA TROCAR TEMA
# ============================================================================

function Set-UITheme {
    param([string]$ThemeName)
    if ($script:Themes.ContainsKey($ThemeName)) {
        $script:ActiveTheme = $ThemeName
        $script:Colors = $script:Themes[$ThemeName]
        return $true
    }
    return $false
}

function Get-UITheme {
    return $script:ActiveTheme
}

function Get-AvailableThemes {
    return $script:Themes.Keys
}

# ============================================================================
# ANIMACOES AVANCADAS
# ============================================================================

function Write-RainbowText {
    param(
        [string]$Text,
        [int]$Delay = 30,
        [switch]$NoNewline,
        [switch]$Animated
    )
    $rainbowColors = @("Red", "Yellow", "Green", "Cyan", "Blue", "Magenta")

    if ($Animated) {
        for ($wave = 0; $wave -lt 2; $wave++) {
            Write-Host "`r" -NoNewline
            for ($i = 0; $i -lt $Text.Length; $i++) {
                $colorIndex = ($i + $wave) % $rainbowColors.Count
                Write-Host $Text[$i] -NoNewline -ForegroundColor $rainbowColors[$colorIndex]
            }
            Start-Sleep -Milliseconds 150
        }
    }

    for ($i = 0; $i -lt $Text.Length; $i++) {
        $colorIndex = $i % $rainbowColors.Count
        Write-Host $Text[$i] -NoNewline -ForegroundColor $rainbowColors[$colorIndex]
        if ($Delay -gt 0) { Start-Sleep -Milliseconds $Delay }
    }

    if (-not $NoNewline) { Write-Host "" }
}

function Write-PulseText {
    param(
        [string]$Text,
        [int]$Pulses = 3,
        [int]$Duration = 100
    )
    $pulseColors = @($Colors.Primary, $Colors.Secondary, "White", $Colors.Secondary)

    for ($p = 0; $p -lt $Pulses; $p++) {
        foreach ($color in $pulseColors) {
            Write-Host "`r  $Text" -NoNewline -ForegroundColor $color
            Start-Sleep -Milliseconds $Duration
        }
    }
    Write-Host "`r  $Text" -ForegroundColor $Colors.Primary
}

function Write-WaveText {
    param(
        [string]$Text,
        [int]$Waves = 2
    )
    $colors = @($Colors.Dim, $Colors.Secondary, $Colors.Primary, "White", $Colors.Primary, $Colors.Secondary)

    for ($wave = 0; $wave -lt $Waves * $Text.Length; $wave++) {
        Write-Host "`r  " -NoNewline
        for ($i = 0; $i -lt $Text.Length; $i++) {
            $colorIndex = [math]::Abs(($wave - $i) % $colors.Count)
            Write-Host $Text[$i] -NoNewline -ForegroundColor $colors[$colorIndex]
        }
        Start-Sleep -Milliseconds 50
    }
    Write-Host ""
}

function Write-TypewriterText {
    param(
        [string]$Text,
        [string]$Color = "White",
        [int]$CharDelay = 20,
        [int]$CursorBlinks = 2
    )

    # Cursor piscando antes
    for ($b = 0; $b -lt $CursorBlinks; $b++) {
        Write-Host "_" -NoNewline -ForegroundColor $Color
        Start-Sleep -Milliseconds 200
        Write-Host "`b " -NoNewline
        Start-Sleep -Milliseconds 200
    }

    # Digita o texto
    foreach ($char in $Text.ToCharArray()) {
        Write-Host $char -NoNewline -ForegroundColor $Color
        $delay = if ($char -match '[.,!?]') { $CharDelay * 5 } else { $CharDelay }
        Start-Sleep -Milliseconds $delay
    }
    Write-Host ""
}

function Show-ParticleExplosion {
    param(
        [int]$Duration = 500,
        [int]$Width = 40
    )
    $particles = @("*", ".", "+", "o", ".", "*", "+", ".")
    $colors = @($Colors.Primary, $Colors.Secondary, $Colors.Tertiary, "White")

    $endTime = (Get-Date).AddMilliseconds($Duration)
    while ((Get-Date) -lt $endTime) {
        Write-Host "`r  " -NoNewline
        for ($i = 0; $i -lt $Width; $i++) {
            $particle = $particles[(Get-Random -Maximum $particles.Count)]
            $color = $colors[(Get-Random -Maximum $colors.Count)]
            Write-Host $particle -NoNewline -ForegroundColor $color
        }
        Start-Sleep -Milliseconds 50
    }
    Write-Host "`r$(' ' * ($Width + 4))" -NoNewline
    Write-Host ""
}

function Show-LoadingDots {
    param(
        [string]$Message,
        [int]$Duration = 2
    )
    $endTime = (Get-Date).AddSeconds($Duration)
    $dots = 0

    while ((Get-Date) -lt $endTime) {
        $dotString = "." * ($dots % 4)
        Write-Host "`r  $Message$($dotString.PadRight(4))" -NoNewline -ForegroundColor $Colors.Primary
        Start-Sleep -Milliseconds 300
        $dots++
    }
    Write-Host "`r  $Message... " -NoNewline -ForegroundColor $Colors.Success
    Write-Host "OK!" -ForegroundColor $Colors.Success
}

# ============================================================================
# SPINNERS AVANCADOS
# ============================================================================

function Show-AdvancedSpinner {
    param(
        [string]$Message,
        [int]$Duration = 2,
        [ValidateSet("Classic", "Dots", "Braille", "Arrow", "Bounce", "Blocks")]
        [string]$Style = "Braille"
    )

    $spinners = @{
        "Classic" = @("|", "/", "-", "\")
        "Dots"    = @("   ", ".  ", ".. ", "...", " ..", "  .", "   ")
        "Braille" = @("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")
        "Arrow"   = @("←", "↖", "↑", "↗", "→", "↘", "↓", "↙")
        "Bounce"  = @("[    ]", "[=   ]", "[==  ]", "[=== ]", "[ ===]", "[  ==]", "[   =]", "[    ]")
        "Blocks"  = @("▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▂")
    }

    $chars = $spinners[$Style]
    $endTime = (Get-Date).AddSeconds($Duration)
    $i = 0

    while ((Get-Date) -lt $endTime) {
        $spinner = $chars[$i % $chars.Count]
        Write-Host "`r  [$spinner] " -NoNewline -ForegroundColor $Colors.Primary
        Write-Host $Message -NoNewline -ForegroundColor $Colors.Info
        Write-Host "     " -NoNewline
        Start-Sleep -Milliseconds 80
        $i++
    }
    Write-Host "`r  [+] $Message                              " -ForegroundColor $Colors.Success
}

# ============================================================================
# BARRAS DE PROGRESSO AVANCADAS
# ============================================================================

function Show-GradientProgressBar {
    param(
        [string]$Message,
        [int]$Steps = 30,
        [int]$Delay = 40
    )

    $gradient = $Colors.Gradient
    Write-Host ""
    Write-Host "  $Message" -ForegroundColor $Colors.Info
    Write-Host "  [" -NoNewline -ForegroundColor $Colors.Dim

    for ($i = 0; $i -lt $Steps; $i++) {
        $colorIndex = [math]::Floor(($i / $Steps) * ($gradient.Count - 1))
        $color = $gradient[$colorIndex]
        Write-Host "█" -NoNewline -ForegroundColor $color
        Start-Sleep -Milliseconds $Delay
    }

    Write-Host "] " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "100%" -ForegroundColor $Colors.Success
}

function Show-AnimatedProgressBar {
    param(
        [string]$Task,
        [int]$TargetPercent = 100,
        [int]$BarWidth = 25
    )

    for ($percent = 0; $percent -le $TargetPercent; $percent += 2) {
        $filled = [math]::Floor(($percent / 100) * $BarWidth)
        $empty = $BarWidth - $filled

        $filledBar = "█" * $filled
        $emptyBar = "░" * $empty

        Write-Host "`r  $Task [" -NoNewline -ForegroundColor $Colors.Info
        Write-Host $filledBar -NoNewline -ForegroundColor $Colors.Primary
        Write-Host $emptyBar -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "] $($percent.ToString().PadLeft(3))%" -NoNewline -ForegroundColor $Colors.Info

        Start-Sleep -Milliseconds 30
    }
    Write-Host ""
}

function Show-MultiColorProgressBar {
    param(
        [string]$Message,
        [int]$Steps = 30
    )

    $colors = @("DarkRed", "Red", "Yellow", "Green", "Cyan")

    Write-Host ""
    Write-Host "  $Message" -ForegroundColor $Colors.Info
    Write-Host "  ╔" -NoNewline -ForegroundColor $Colors.Dim
    Write-Host ("═" * $Steps) -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "╗" -ForegroundColor $Colors.Dim
    Write-Host "  ║" -NoNewline -ForegroundColor $Colors.Dim

    for ($i = 0; $i -lt $Steps; $i++) {
        $colorIndex = [math]::Floor(($i / $Steps) * ($colors.Count - 1))
        Write-Host "▓" -NoNewline -ForegroundColor $colors[$colorIndex]
        Start-Sleep -Milliseconds 40
    }

    Write-Host "║" -ForegroundColor $Colors.Dim
    Write-Host "  ╚" -NoNewline -ForegroundColor $Colors.Dim
    Write-Host ("═" * $Steps) -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "╝ " -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "COMPLETO!" -ForegroundColor $Colors.Success
}

# ============================================================================
# LINHAS DECORATIVAS
# ============================================================================

function Write-GradientLine {
    param(
        [string]$Char = "═",
        [int]$Length = 76,
        [switch]$Animated
    )

    $gradient = $Colors.Gradient
    $segmentLength = [math]::Ceiling($Length / $gradient.Count)

    for ($i = 0; $i -lt $gradient.Count; $i++) {
        $remaining = $Length - ($i * $segmentLength)
        $currentLength = [math]::Min($segmentLength, $remaining)
        if ($currentLength -gt 0) {
            Write-Host ($Char * $currentLength) -NoNewline -ForegroundColor $gradient[$i]
            if ($Animated) { Start-Sleep -Milliseconds 20 }
        }
    }
    Write-Host ""
}

function Write-DoubleLine {
    param([int]$Length = 76)
    Write-Host ("═" * $Length) -ForegroundColor $Colors.Primary
}

function Write-DashedLine {
    param([int]$Length = 76)
    $pattern = "─ "
    $result = ""
    while ($result.Length -lt $Length) { $result += $pattern }
    Write-Host $result.Substring(0, $Length) -ForegroundColor $Colors.Dim
}

function Write-FancyBorder {
    param(
        [string]$Position = "top", # top, bottom
        [int]$Width = 70
    )

    switch ($Position) {
        "top" {
            Write-Host "  ╔" -NoNewline -ForegroundColor $Colors.Primary
            Write-Host ("═" * $Width) -NoNewline -ForegroundColor $Colors.Primary
            Write-Host "╗" -ForegroundColor $Colors.Primary
        }
        "bottom" {
            Write-Host "  ╚" -NoNewline -ForegroundColor $Colors.Primary
            Write-Host ("═" * $Width) -NoNewline -ForegroundColor $Colors.Primary
            Write-Host "╝" -ForegroundColor $Colors.Primary
        }
        "middle" {
            Write-Host "  ╠" -NoNewline -ForegroundColor $Colors.Primary
            Write-Host ("═" * $Width) -NoNewline -ForegroundColor $Colors.Primary
            Write-Host "╣" -ForegroundColor $Colors.Primary
        }
    }
}

# ============================================================================
# TEXTO CENTRALIZADO E FORMATADO
# ============================================================================

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

function Write-CenteredRainbow {
    param(
        [string]$Text,
        [int]$Width = 76
    )
    $padding = [math]::Max(0, ($Width - $Text.Length) / 2)
    Write-Host (" " * $padding) -NoNewline
    Write-RainbowText -Text $Text -Delay 0
}

function Write-BoxedText {
    param(
        [string]$Text,
        [string]$BorderColor = "Cyan",
        [string]$TextColor = "White",
        [int]$Width = 60
    )

    $innerWidth = $Width - 4
    $paddedText = $Text.PadRight($innerWidth).Substring(0, $innerWidth)

    Write-Host "  ╔$("═" * $innerWidth)╗" -ForegroundColor $BorderColor
    Write-Host "  ║ " -NoNewline -ForegroundColor $BorderColor
    Write-Host $paddedText -NoNewline -ForegroundColor $TextColor
    Write-Host " ║" -ForegroundColor $BorderColor
    Write-Host "  ╚$("═" * $innerWidth)╝" -ForegroundColor $BorderColor
}

# ============================================================================
# CAIXAS DE STATUS
# ============================================================================

function Show-SuccessBox {
    param(
        [string]$Message,
        [string]$SubMessage = "",
        [switch]$Animated
    )

    if ($Animated) { Show-ParticleExplosion -Duration 300 -Width 50 }

    Write-Host ""
    Write-Host "  ╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor $Colors.Success
    Write-Host "  ║                                                                   ║" -ForegroundColor $Colors.Success
    Write-Host "  ║  " -NoNewline -ForegroundColor $Colors.Success
    Write-Host "[✓] " -NoNewline -ForegroundColor "White"
    Write-Host $Message.PadRight(58) -NoNewline -ForegroundColor "White"
    Write-Host "║" -ForegroundColor $Colors.Success
    if ($SubMessage) {
        Write-Host "  ║      " -NoNewline -ForegroundColor $Colors.Success
        Write-Host $SubMessage.PadRight(59) -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "║" -ForegroundColor $Colors.Success
    }
    Write-Host "  ║                                                                   ║" -ForegroundColor $Colors.Success
    Write-Host "  ╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor $Colors.Success
    Write-Host ""
}

function Show-ErrorBox {
    param(
        [string]$Message,
        [string]$SubMessage = "",
        [string]$Link = ""
    )
    Write-Host ""
    Write-Host "  ╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor $Colors.Error
    Write-Host "  ║                                                                   ║" -ForegroundColor $Colors.Error
    Write-Host "  ║  " -NoNewline -ForegroundColor $Colors.Error
    Write-Host "[✗] " -NoNewline -ForegroundColor "White"
    Write-Host $Message.PadRight(58) -NoNewline -ForegroundColor "White"
    Write-Host "║" -ForegroundColor $Colors.Error
    if ($SubMessage) {
        Write-Host "  ║                                                                   ║" -ForegroundColor $Colors.Error
        Write-Host "  ║      " -NoNewline -ForegroundColor $Colors.Error
        Write-Host $SubMessage.PadRight(59) -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "║" -ForegroundColor $Colors.Error
    }
    if ($Link) {
        Write-Host "  ║                                                                   ║" -ForegroundColor $Colors.Error
        Write-Host "  ║  [→] " -NoNewline -ForegroundColor $Colors.Error
        Write-Host $Link.PadRight(59) -NoNewline -ForegroundColor $Colors.Primary
        Write-Host "║" -ForegroundColor $Colors.Error
    }
    Write-Host "  ║                                                                   ║" -ForegroundColor $Colors.Error
    Write-Host "  ╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor $Colors.Error
    Write-Host ""
}

function Show-WarningBox {
    param(
        [string]$Message,
        [string]$SubMessage = ""
    )
    Write-Host ""
    Write-Host "  ╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor $Colors.Warning
    Write-Host "  ║  " -NoNewline -ForegroundColor $Colors.Warning
    Write-Host "[!] " -NoNewline -ForegroundColor "White"
    Write-Host $Message.PadRight(58) -NoNewline -ForegroundColor "White"
    Write-Host "║" -ForegroundColor $Colors.Warning
    if ($SubMessage) {
        Write-Host "  ║      " -NoNewline -ForegroundColor $Colors.Warning
        Write-Host $SubMessage.PadRight(59) -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "║" -ForegroundColor $Colors.Warning
    }
    Write-Host "  ╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor $Colors.Warning
    Write-Host ""
}

function Show-InfoBox {
    param([string]$Message)
    Write-Host ""
    Write-Host "  ┌───────────────────────────────────────────────────────────────────┐" -ForegroundColor $Colors.Primary
    Write-Host "  │  " -NoNewline -ForegroundColor $Colors.Primary
    Write-Host "[i] " -NoNewline -ForegroundColor $Colors.Secondary
    Write-Host $Message.PadRight(58) -NoNewline -ForegroundColor $Colors.Info
    Write-Host "│" -ForegroundColor $Colors.Primary
    Write-Host "  └───────────────────────────────────────────────────────────────────┘" -ForegroundColor $Colors.Primary
    Write-Host ""
}

# ============================================================================
# STEPS E SUB-STEPS
# ============================================================================

function Write-Step {
    param(
        [int]$Current,
        [int]$Total,
        [string]$Message
    )
    Write-Host ""
    Write-Host "  [$Current" -NoNewline -ForegroundColor $Colors.Primary
    Write-Host "/" -NoNewline -ForegroundColor $Colors.Dim
    Write-Host "$Total] " -NoNewline -ForegroundColor $Colors.Primary
    Write-Host $Message -ForegroundColor $Colors.Info
}

function Write-SubStep {
    param(
        [string]$Message,
        [string]$Status = "..."
    )
    Write-Host "       → " -NoNewline -ForegroundColor $Colors.Secondary
    Write-Host $Message -NoNewline -ForegroundColor $Colors.Info
    Write-Host " $Status" -ForegroundColor $Colors.Dim
}

function Write-SubStepSuccess {
    param([string]$Message)
    Write-Host "       [✓] " -NoNewline -ForegroundColor $Colors.Success
    Write-Host $Message -ForegroundColor $Colors.Info
}

function Write-SubStepError {
    param([string]$Message)
    Write-Host "       [✗] " -NoNewline -ForegroundColor $Colors.Error
    Write-Host $Message -ForegroundColor $Colors.Info
}

function Write-SubStepWarning {
    param([string]$Message)
    Write-Host "       [!] " -NoNewline -ForegroundColor $Colors.Warning
    Write-Host $Message -ForegroundColor $Colors.Info
}

# ============================================================================
# ASCII ARTS
# ============================================================================

$script:AsciiArts = @{
    "Rocket" = @(
        "            ▄▄████▄▄            ",
        "          ▄██████████▄          ",
        "         ███████████████        ",
        "        ████████████████        ",
        "        ████████████████        ",
        "        ██████▀▀██████▀▀        ",
        "       ▐█████    █████▌         ",
        "       ▐█████    █████▌         ",
        "      ▄█████▌    ▐█████▄        ",
        "     ████████    ████████       ",
        "    ▀▀▀▀▀▀██▌    ▐██▀▀▀▀▀▀      ",
        "          ▐█▌    ▐█▌            ",
        "         ▄███    ███▄           ",
        "        █████    █████          ",
        "       ▀▀ ▀▀      ▀▀ ▀▀         "
    )
    "Gear" = @(
        "       ╔═══╗       ",
        "    ╔══╝   ╚══╗    ",
        "  ╔═╝  ╔═══╗  ╚═╗  ",
        " ═╝   ╔╝   ╚╗   ╚═ ",
        "      ║     ║      ",
        " ═╗   ╚╗   ╔╝   ╔═ ",
        "  ╚═╗  ╚═══╝  ╔═╝  ",
        "    ╚══╗   ╔══╝    ",
        "       ╚═══╝       "
    )
    "Check" = @(
        "    ╔══════════╗    ",
        "   ╔╝          ╚╗   ",
        "  ╔╝      ╔═╗   ╚╗  ",
        " ╔╝     ╔═╝ ╚╗   ╚╗ ",
        " ║   ╔═╝    ╚═╗  ║ ",
        " ╚╗ ╔╝        ╚╗╔╝ ",
        "  ╚╝          ╚╝  "
    )
    "Game" = @(
        "    ██████╗  █████╗ ███╗   ███╗███████╗",
        "   ██╔════╝ ██╔══██╗████╗ ████║██╔════╝",
        "   ██║  ███╗███████║██╔████╔██║█████╗  ",
        "   ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  ",
        "   ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗",
        "    ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝"
    )
    "Translator" = @(
        "████████╗██████╗  █████╗ ███╗   ██╗███████╗██╗      █████╗ ████████╗ ██████╗ ██████╗",
        "╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗",
        "   ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     ███████║   ██║   ██║   ██║██████╔╝",
        "   ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗",
        "   ██║   ██║  ██║██║  ██║██║ ╚████║███████║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║",
        "   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝"
    )
    "Controller" = @(
        "      ╔══════════════════╗      ",
        "   ╔══╝   ╔══╗   ╔══╗    ╚══╗   ",
        "  ╔╝  ╔═╗ ║  ║   ║  ║ ●  ●  ╚╗  ",
        " ╔╝ ══╬══ ╚══╝   ╚══╝  ●  ●  ╚╗ ",
        " ║   ╔═╗                      ║ ",
        " ╚╗  ▀▀▀     ▄▄  ▄▄          ╔╝ ",
        "  ╚╗        ▀▀▀  ▀▀▀        ╔╝  ",
        "   ╚══╗                  ╔══╝   ",
        "      ╚══════════════════╝      "
    )
    "Build" = @(
        "  ╔══════════════════════════╗  ",
        "  ║  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ║  ",
        "  ║  ▓  ╔════════════╗  ▓  ║  ",
        "  ║  ▓  ║   BUILD    ║  ▓  ║  ",
        "  ║  ▓  ╚════════════╝  ▓  ║  ",
        "  ║  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ║  ",
        "  ╚══════════════════════════╝  "
    )
}

function Show-AsciiArt {
    param(
        [string]$Name,
        [string]$Color = "",
        [switch]$Animated,
        [switch]$Rainbow,
        [int]$CenterWidth = 80
    )

    if (-not $script:AsciiArts.ContainsKey($Name)) {
        Write-Host "ASCII Art '$Name' not found" -ForegroundColor $Colors.Error
        return
    }

    $art = $script:AsciiArts[$Name]
    $useColor = if ($Color) { $Color } else { $Colors.Primary }

    foreach ($line in $art) {
        $padding = [math]::Max(0, ($CenterWidth - $line.Length) / 2)
        Write-Host (" " * $padding) -NoNewline

        if ($Rainbow) {
            Write-RainbowText -Text $line -Delay 0
        } else {
            Write-Host $line -ForegroundColor $useColor
        }

        if ($Animated) { Start-Sleep -Milliseconds 50 }
    }
}

# ============================================================================
# HEADERS ESPECIAIS
# ============================================================================

function Show-MainHeader {
    param(
        [string]$Title,
        [string]$Subtitle = "",
        [string]$Version = "v3.0.0",
        [switch]$Animated
    )

    Clear-Host
    Write-Host ""
    Write-GradientLine -Char "═" -Length 76 -Animated:$Animated
    Write-Host ""

    # Logo animado
    Show-AsciiArt -Name "Game" -Animated:$Animated -Color $Colors.Primary -CenterWidth 76
    Show-AsciiArt -Name "Translator" -Animated:$Animated -Color $Colors.Secondary -CenterWidth 90

    Write-Host ""
    Write-GradientLine -Char "─" -Length 76
    Write-Host ""
    Write-CenteredText $Title $Colors.Primary 76
    if ($Subtitle) { Write-CenteredText $Subtitle $Colors.Dim 76 }
    Write-CenteredText $Version $Colors.Secondary 76
    Write-Host ""
    Write-GradientLine -Char "═" -Length 76 -Animated:$Animated
    Write-Host ""
}

function Show-SectionHeader {
    param(
        [string]$Title,
        [string]$Icon = "★"
    )

    Clear-Host
    Write-Host ""
    Write-GradientLine -Char "═" -Length 76
    Write-Host ""
    Write-Host "  [$Icon] " -NoNewline -ForegroundColor $Colors.Secondary
    Write-Host $Title.ToUpper() -ForegroundColor $Colors.Primary
    Write-Host ""
    Write-GradientLine -Char "─" -Length 76
    Write-Host ""
}

# ============================================================================
# MENUS ESTILIZADOS
# ============================================================================

function Show-StylizedMenu {
    param(
        [array]$MenuItems,
        [string]$Title = "MENU",
        [int]$Width = 65
    )

    $innerWidth = $Width - 4

    Write-Host ""
    Write-Host "  ╔$("═" * $innerWidth)╗" -ForegroundColor $Colors.Primary

    # Titulo centralizado
    $titlePadding = [math]::Floor(($innerWidth - $Title.Length) / 2)
    Write-Host "  ║" -NoNewline -ForegroundColor $Colors.Primary
    Write-Host (" " * $titlePadding) -NoNewline
    Write-Host $Title -NoNewline -ForegroundColor $Colors.Secondary
    Write-Host (" " * ($innerWidth - $titlePadding - $Title.Length)) -NoNewline
    Write-Host "║" -ForegroundColor $Colors.Primary

    Write-Host "  ╠$("═" * $innerWidth)╣" -ForegroundColor $Colors.Primary
    Write-Host "  ║$(" " * $innerWidth)║" -ForegroundColor $Colors.Primary

    foreach ($item in $MenuItems) {
        $key = $item.Key
        $icon = $item.Icon
        $text = $item.Text
        $extra = if ($item.Extra) { " $($item.Extra)" } else { "" }

        $content = "   [$key] $icon $text$extra"
        $padding = $innerWidth - $content.Length

        Write-Host "  ║" -NoNewline -ForegroundColor $Colors.Primary
        Write-Host "   [" -NoNewline -ForegroundColor $Colors.Dim
        Write-Host $key -NoNewline -ForegroundColor $Colors.Secondary
        Write-Host "] " -NoNewline -ForegroundColor $Colors.Dim
        Write-Host "$icon " -NoNewline -ForegroundColor $Colors.Primary
        Write-Host $text -NoNewline -ForegroundColor $Colors.Info
        if ($extra) { Write-Host $extra -NoNewline -ForegroundColor $Colors.Dim }
        Write-Host (" " * [math]::Max(1, $padding)) -NoNewline
        Write-Host "║" -ForegroundColor $Colors.Primary
    }

    Write-Host "  ║$(" " * $innerWidth)║" -ForegroundColor $Colors.Primary
    Write-Host "  ╚$("═" * $innerWidth)╝" -ForegroundColor $Colors.Primary
    Write-Host ""
}

# ============================================================================
# ANIMACOES DE TRANSICAO
# ============================================================================

function Show-TransitionWipe {
    param([int]$Width = 76)

    for ($i = 0; $i -lt $Width; $i += 2) {
        Write-Host "`r$(" " * $i)██" -NoNewline -ForegroundColor $Colors.Primary
        Start-Sleep -Milliseconds 5
    }
    Write-Host ""
}

function Show-ExitAnimation {
    Clear-Host
    Write-Host ""
    Write-Host ""

    $message = "Obrigado por usar o Game Translator!"
    Write-CenteredRainbow $message 76

    Write-Host ""
    Write-Host ""
    Write-CenteredText "Ate a proxima!" $Colors.Primary 76
    Write-Host ""

    # Animacao de saida
    $frames = @(".", "..", "...", "....", ".....", "....", "...", "..", ".")
    foreach ($frame in $frames) {
        Write-Host "`r" -NoNewline
        Write-CenteredText "Encerrando$frame" $Colors.Dim 76
        Start-Sleep -Milliseconds 150
    }
    Write-Host ""
}

function Show-WelcomeAnimation {
    param([int]$Duration = 2000)

    $endTime = (Get-Date).AddMilliseconds($Duration)
    $chars = @("★", "☆", "◆", "◇", "●", "○", "■", "□")

    while ((Get-Date) -lt $endTime) {
        Write-Host "`r  " -NoNewline
        for ($i = 0; $i -lt 30; $i++) {
            $char = $chars[(Get-Random -Maximum $chars.Count)]
            $color = @($Colors.Primary, $Colors.Secondary, $Colors.Tertiary)[(Get-Random -Maximum 3)]
            Write-Host $char -NoNewline -ForegroundColor $color
        }
        Start-Sleep -Milliseconds 100
    }
    Write-Host ""
}

# ============================================================================
# EXPORTAR FUNCOES
# ============================================================================

Export-ModuleMember -Function * -Variable Colors, Themes, ActiveTheme, AsciiArts
