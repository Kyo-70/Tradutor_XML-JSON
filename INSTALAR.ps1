# Game Translator - Instalador v1.0.8
# Requer PowerShell 5.1 ou superior

$Host.UI.RawUI.WindowTitle = "Game Translator - Instalador v1.0.8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Cores personalizadas
$ColorTitulo = "Magenta"
$ColorSucesso = "Green"
$ColorErro = "Red"
$ColorAviso = "Yellow"
$ColorInfo = "Cyan"
$ColorDestaque = "White"
$ColorSecao = "Blue"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

function Show-Menu {
    Clear-Host
    Write-Host ""
    Write-Host "========================================================================" -ForegroundColor $ColorTitulo
    Write-Host "                                                                        " -ForegroundColor $ColorTitulo
    Write-Host "     GAME TRANSLATOR - INSTALADOR v1.0.8                               " -ForegroundColor $ColorTitulo
    Write-Host "                                                                        " -ForegroundColor $ColorTitulo
    Write-Host "     Sistema Profissional de Traducao para Jogos e Mods                " -ForegroundColor $ColorTitulo
    Write-Host "                                                                        " -ForegroundColor $ColorTitulo
    Write-Host "========================================================================" -ForegroundColor $ColorTitulo
    Write-Host ""
    Write-Host "  [1] " -ForegroundColor $ColorInfo -NoNewline
    Write-Host "Instalacao Completa" -ForegroundColor $ColorDestaque -NoNewline
    Write-Host " (Recomendado)"
    Write-Host "  [2] " -ForegroundColor $ColorInfo -NoNewline
    Write-Host "Verificar Requisitos"
    Write-Host "  [3] " -ForegroundColor $ColorInfo -NoNewline
    Write-Host "Instalar Dependencias"
    Write-Host "  [4] " -ForegroundColor $ColorInfo -NoNewline
    Write-Host "Criar Executavel (.exe)"
    Write-Host "  [5] " -ForegroundColor $ColorInfo -NoNewline
    Write-Host "Executar Programa (modo desenvolvedor)"
    Write-Host "  [6] " -ForegroundColor $ColorInfo -NoNewline
    Write-Host "Limpar Arquivos Temporarios"
    Write-Host "  [0] " -ForegroundColor $ColorInfo -NoNewline
    Write-Host "Sair"
    Write-Host ""
}

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
    param(
        [bool]$Silent = $false
    )
    
    if (-not $Silent) {
        Write-Host ""
        Write-Host "Limpando arquivos temporarios..." -ForegroundColor $ColorInfo
        Write-Host ""
    }
    
    $totalRemoved = 0
    
    # Lista de pastas a serem removidas
    $foldersToRemove = @(
        "build",
        "dist",
        "__pycache__",
        "src\__pycache__",
        "src\gui\__pycache__"
    )
    
    # Remove pastas principais
    foreach ($folder in $foldersToRemove) {
        $folderPath = Join-Path $ScriptDir $folder
        if (Test-Path $folderPath) {
            try {
                Remove-Item -Path $folderPath -Recurse -Force -ErrorAction Stop
                if (-not $Silent) {
                    Write-Host "  [OK] Removido: $folder" -ForegroundColor $ColorSucesso
                }
                $totalRemoved++
            }
            catch {
                if (-not $Silent) {
                    Write-Host "  [ERRO] Falha ao remover: $folder" -ForegroundColor $ColorErro
                }
            }
        }
    }
    
    # Remove arquivos .spec
    $specFiles = Get-ChildItem -Path $ScriptDir -Filter "*.spec" -ErrorAction SilentlyContinue
    foreach ($file in $specFiles) {
        try {
            Remove-Item -Path $file.FullName -Force
            if (-not $Silent) {
                Write-Host "  [OK] Removido: $($file.Name)" -ForegroundColor $ColorSucesso
            }
            $totalRemoved++
        }
        catch {
            if (-not $Silent) {
                Write-Host "  [ERRO] Falha ao remover: $($file.Name)" -ForegroundColor $ColorErro
            }
        }
    }
    
    # Busca e remove __pycache__ em subpastas recursivamente
    $pycacheFolders = Get-ChildItem -Path $ScriptDir -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue
    foreach ($pycache in $pycacheFolders) {
        try {
            Remove-Item -Path $pycache.FullName -Recurse -Force
            if (-not $Silent) {
                Write-Host "  [OK] Removido: $($pycache.FullName.Replace($ScriptDir, '.'))" -ForegroundColor $ColorSucesso
            }
            $totalRemoved++
        }
        catch {
            if (-not $Silent) {
                Write-Host "  [ERRO] Falha ao remover: $($pycache.FullName)" -ForegroundColor $ColorErro
            }
        }
    }
    
    # Remove arquivos .pyc soltos
    $pycFiles = Get-ChildItem -Path $ScriptDir -Filter "*.pyc" -Recurse -ErrorAction SilentlyContinue
    foreach ($pyc in $pycFiles) {
        try {
            Remove-Item -Path $pyc.FullName -Force
            if (-not $Silent) {
                Write-Host "  [OK] Removido: $($pyc.FullName.Replace($ScriptDir, '.'))" -ForegroundColor $ColorSucesso
            }
            $totalRemoved++
        }
        catch {
            if (-not $Silent) {
                Write-Host "  [ERRO] Falha ao remover: $($pyc.Name)" -ForegroundColor $ColorErro
            }
        }
    }
    
    # Remove arquivos .pyo soltos
    $pyoFiles = Get-ChildItem -Path $ScriptDir -Filter "*.pyo" -Recurse -ErrorAction SilentlyContinue
    foreach ($pyo in $pyoFiles) {
        try {
            Remove-Item -Path $pyo.FullName -Force
            if (-not $Silent) {
                Write-Host "  [OK] Removido: $($pyo.FullName.Replace($ScriptDir, '.'))" -ForegroundColor $ColorSucesso
            }
            $totalRemoved++
        }
        catch {
            if (-not $Silent) {
                Write-Host "  [ERRO] Falha ao remover: $($pyo.Name)" -ForegroundColor $ColorErro
            }
        }
    }
    
    if (-not $Silent) {
        Write-Host ""
        Write-Host "  Total de itens removidos: $totalRemoved" -ForegroundColor $ColorInfo
    }
    
    return $totalRemoved
}

function Show-CleanMenu {
    Clear-Host
    Write-Host ""
    Write-Host "========================================================================" -ForegroundColor $ColorSecao
    Write-Host "  LIMPEZA DE ARQUIVOS TEMPORARIOS" -ForegroundColor $ColorSecao
    Write-Host "========================================================================" -ForegroundColor $ColorSecao
    Write-Host ""
    Write-Host "Esta funcao remove os seguintes arquivos/pastas:" -ForegroundColor $ColorInfo
    Write-Host ""
    Write-Host "  - build/          (pasta de compilacao do PyInstaller)" -ForegroundColor $ColorDestaque
    Write-Host "  - dist/           (pasta do executavel gerado)" -ForegroundColor $ColorDestaque
    Write-Host "  - __pycache__/    (cache do Python em todas as pastas)" -ForegroundColor $ColorDestaque
    Write-Host "  - *.spec          (arquivos de especificacao do PyInstaller)" -ForegroundColor $ColorDestaque
    Write-Host "  - *.pyc           (arquivos compilados do Python)" -ForegroundColor $ColorDestaque
    Write-Host "  - *.pyo           (arquivos otimizados do Python)" -ForegroundColor $ColorDestaque
    Write-Host ""
    
    $response = Read-Host "Deseja continuar com a limpeza? (S/N)"
    if ($response -eq "S" -or $response -eq "s" -or $response -eq "Y" -or $response -eq "y") {
        Clear-TempFiles -Silent $false
        Write-Host ""
        Write-Host "========================================================================" -ForegroundColor $ColorSucesso
        Write-Host "  [OK] Limpeza concluida!" -ForegroundColor $ColorSucesso
        Write-Host "========================================================================" -ForegroundColor $ColorSucesso
    } else {
        Write-Host ""
        Write-Host "Limpeza cancelada." -ForegroundColor $ColorAviso
    }
    
    Write-Host ""
    Read-Host "Pressione Enter para continuar"
}

function Install-Complete {
    Clear-Host
    Write-Host ""
    Write-Host "========================================================================" -ForegroundColor $ColorSecao
    Write-Host "  INSTALACAO COMPLETA" -ForegroundColor $ColorSecao
    Write-Host "========================================================================" -ForegroundColor $ColorSecao
    Write-Host ""
    
    Write-Host "[1/5] Verificando Python..." -ForegroundColor $ColorInfo
    Write-Host ""
    
    if (-not (Test-Python)) {
        Write-Host "[ERRO] Python nao encontrado!" -ForegroundColor $ColorErro
        Write-Host ""
        Write-Host "Instale Python de: https://www.python.org/downloads/" -ForegroundColor $ColorInfo
        Write-Host "Durante a instalacao, marque 'Add Python to PATH'" -ForegroundColor $ColorInfo
        Write-Host ""
        Read-Host "Pressione Enter para continuar"
        return
    }
    
    $pythonVersion = py --version 2>&1
    Write-Host "[OK] $pythonVersion encontrado" -ForegroundColor $ColorSucesso
    
    Write-Host ""
    Write-Host "[2/5] Limpando arquivos temporarios anteriores..." -ForegroundColor $ColorInfo
    Clear-TempFiles -Silent $true
    Write-Host "[OK] Arquivos temporarios removidos" -ForegroundColor $ColorSucesso
    
    Write-Host ""
    Write-Host "[3/5] Instalando dependencias..." -ForegroundColor $ColorInfo
    Write-Host ""
    
    Write-Host "   Atualizando pip..." -ForegroundColor $ColorInfo
    py -m pip install --upgrade pip --quiet
    
    $deps = @("PySide6", "requests", "psutil", "colorama", "pyinstaller")
    foreach ($dep in $deps) {
        Write-Host "   Instalando $dep..." -ForegroundColor $ColorInfo
        py -m pip install $dep --quiet
    }
    
    Write-Host ""
    Write-Host "[OK] Dependencias instaladas!" -ForegroundColor $ColorSucesso
    Write-Host ""
    
    Write-Host "[4/5] Criando executavel..." -ForegroundColor $ColorInfo
    Write-Host ""
    Write-Host "   Isso pode levar alguns minutos, aguarde..." -ForegroundColor $ColorAviso
    Write-Host ""
    
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
        "$mainPath"
    
    Write-Host ""
    Write-Host "[5/5] Verificando resultado e limpando temporarios..." -ForegroundColor $ColorInfo
    Write-Host ""
    
    $exePath = Join-Path $ScriptDir "dist\GameTranslator.exe"
    
    if (Test-Path $exePath) {
        # Limpa arquivos temporarios apos build bem-sucedido (mantem dist/)
        if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
        $specFiles = Get-ChildItem -Path $ScriptDir -Filter "*.spec" -ErrorAction SilentlyContinue
        foreach ($file in $specFiles) {
            Remove-Item -Path $file.FullName -Force -ErrorAction SilentlyContinue
        }
        # Limpa __pycache__ recursivamente
        Get-ChildItem -Path $ScriptDir -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue | ForEach-Object {
            Remove-Item -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
        }
        
        Write-Host "========================================================================" -ForegroundColor $ColorSucesso
        Write-Host "                                                                        " -ForegroundColor $ColorSucesso
        Write-Host "  [OK] INSTALACAO CONCLUIDA COM SUCESSO!                              " -ForegroundColor $ColorSucesso
        Write-Host "                                                                        " -ForegroundColor $ColorSucesso
        Write-Host "  Executavel criado em:                                               " -ForegroundColor $ColorSucesso
        Write-Host "  $exePath" -ForegroundColor $ColorSucesso
        Write-Host "                                                                        " -ForegroundColor $ColorSucesso
        Write-Host "  Arquivos temporarios foram limpos automaticamente.                  " -ForegroundColor $ColorSucesso
        Write-Host "                                                                        " -ForegroundColor $ColorSucesso
        Write-Host "========================================================================" -ForegroundColor $ColorSucesso
        Write-Host ""
        
        $response = Read-Host "Deseja abrir o programa agora? (S/N)"
        if ($response -eq "S" -or $response -eq "s" -or $response -eq "Y" -or $response -eq "y") {
            Start-Process $exePath
        }
    } else {
        Write-Host "[ERRO] Falha ao criar executavel!" -ForegroundColor $ColorErro
        Write-Host "Verifique os erros acima." -ForegroundColor $ColorAviso
    }
    
    Write-Host ""
    Read-Host "Pressione Enter para continuar"
}

function Test-Requirements {
    Clear-Host
    Write-Host ""
    Write-Host "========================================================================" -ForegroundColor $ColorSecao
    Write-Host "  VERIFICACAO DE REQUISITOS" -ForegroundColor $ColorSecao
    Write-Host "========================================================================" -ForegroundColor $ColorSecao
    Write-Host ""
    
    if (-not (Test-Python)) {
        Write-Host "[ERRO] Python nao encontrado!" -ForegroundColor $ColorErro
        Write-Host ""
        Write-Host "Instale Python de: https://www.python.org/downloads/" -ForegroundColor $ColorInfo
        Write-Host "Durante a instalacao, marque 'Add Python to PATH'" -ForegroundColor $ColorInfo
        Write-Host ""
        Read-Host "Pressione Enter para continuar"
        return
    }
    
    Set-Location (Join-Path $ScriptDir "src")
    py verificar_sistema.py
    Set-Location $ScriptDir
    
    Write-Host ""
    Read-Host "Pressione Enter para continuar"
}

function Install-Dependencies {
    Clear-Host
    Write-Host ""
    Write-Host "========================================================================" -ForegroundColor $ColorSecao
    Write-Host "  INSTALACAO DE DEPENDENCIAS" -ForegroundColor $ColorSecao
    Write-Host "========================================================================" -ForegroundColor $ColorSecao
    Write-Host ""
    
    Write-Host "Verificando Python..." -ForegroundColor $ColorInfo
    
    if (-not (Test-Python)) {
        Write-Host "[ERRO] Python nao encontrado!" -ForegroundColor $ColorErro
        Write-Host "Instale Python de: https://www.python.org/downloads/" -ForegroundColor $ColorInfo
        Read-Host "Pressione Enter para continuar"
        return
    }
    
    Write-Host ""
    Write-Host "Instalando dependencias..." -ForegroundColor $ColorInfo
    Write-Host ""
    
    Write-Host "[1/5] Atualizando pip..." -ForegroundColor $ColorInfo
    py -m pip install --upgrade pip
    
    Write-Host ""
    Write-Host "[2/5] Instalando PySide6..." -ForegroundColor $ColorInfo
    py -m pip install PySide6
    
    Write-Host ""
    Write-Host "[3/5] Instalando requests..." -ForegroundColor $ColorInfo
    py -m pip install requests
    
    Write-Host ""
    Write-Host "[4/5] Instalando psutil e colorama..." -ForegroundColor $ColorInfo
    py -m pip install psutil colorama
    
    Write-Host ""
    Write-Host "[5/5] Instalando PyInstaller..." -ForegroundColor $ColorInfo
    py -m pip install pyinstaller
    
    Write-Host ""
    Write-Host "========================================================================" -ForegroundColor $ColorSucesso
    Write-Host "  [OK] Todas as dependencias foram instaladas!" -ForegroundColor $ColorSucesso
    Write-Host "========================================================================" -ForegroundColor $ColorSucesso
    Write-Host ""
    Read-Host "Pressione Enter para continuar"
}

function Build-Executable {
    Clear-Host
    Write-Host ""
    Write-Host "========================================================================" -ForegroundColor $ColorSecao
    Write-Host "  CRIACAO DO EXECUTAVEL" -ForegroundColor $ColorSecao
    Write-Host "========================================================================" -ForegroundColor $ColorSecao
    Write-Host ""
    
    Write-Host "Verificando Python..." -ForegroundColor $ColorInfo
    
    if (-not (Test-Python)) {
        Write-Host "[ERRO] Python nao encontrado!" -ForegroundColor $ColorErro
        Read-Host "Pressione Enter para continuar"
        return
    }
    
    Write-Host ""
    Write-Host "Limpando arquivos temporarios anteriores..." -ForegroundColor $ColorInfo
    Clear-TempFiles -Silent $true
    Write-Host "[OK] Arquivos temporarios removidos" -ForegroundColor $ColorSucesso
    
    Write-Host ""
    Write-Host "Criando executavel (isso pode levar alguns minutos)..." -ForegroundColor $ColorInfo
    Write-Host ""
    
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
        "$mainPath"
    
    Write-Host ""
    
    $exePath = Join-Path $ScriptDir "dist\GameTranslator.exe"
    
    if (Test-Path $exePath) {
        # Limpa arquivos temporarios apos build bem-sucedido (mantem dist/)
        if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
        $specFiles = Get-ChildItem -Path $ScriptDir -Filter "*.spec" -ErrorAction SilentlyContinue
        foreach ($file in $specFiles) {
            Remove-Item -Path $file.FullName -Force -ErrorAction SilentlyContinue
        }
        # Limpa __pycache__ recursivamente
        Get-ChildItem -Path $ScriptDir -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue | ForEach-Object {
            Remove-Item -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
        }
        
        Write-Host "[OK] Executavel criado com sucesso!" -ForegroundColor $ColorSucesso
        Write-Host "Local: $exePath" -ForegroundColor $ColorInfo
        Write-Host ""
        Write-Host "[OK] Arquivos temporarios limpos automaticamente." -ForegroundColor $ColorSucesso
        Write-Host ""
        
        $response = Read-Host "Abrir pasta? (S/N)"
        if ($response -eq "S" -or $response -eq "s" -or $response -eq "Y" -or $response -eq "y") {
            explorer (Join-Path $ScriptDir "dist")
        }
    } else {
        Write-Host "[ERRO] Falha ao criar executavel!" -ForegroundColor $ColorErro
    }
    
    Write-Host ""
    Read-Host "Pressione Enter para continuar"
}

function Start-Program {
    Clear-Host
    Write-Host ""
    Write-Host "========================================================================" -ForegroundColor $ColorSecao
    Write-Host "  EXECUTAR PROGRAMA" -ForegroundColor $ColorSecao
    Write-Host "========================================================================" -ForegroundColor $ColorSecao
    Write-Host ""
    
    Write-Host "Verificando Python..." -ForegroundColor $ColorInfo
    
    if (-not (Test-Python)) {
        Write-Host "[ERRO] Python nao encontrado!" -ForegroundColor $ColorErro
        Read-Host "Pressione Enter para continuar"
        return
    }
    
    Write-Host ""
    Write-Host "Iniciando Game Translator..." -ForegroundColor $ColorInfo
    Write-Host ""
    
    Set-Location (Join-Path $ScriptDir "src")
    py main.py
    
    Write-Host ""
    Read-Host "Pressione Enter para continuar"
}

# Loop principal do menu
do {
    Show-Menu
    $option = Read-Host "Digite sua opcao"
    
    switch ($option) {
        "1" { Install-Complete }
        "2" { Test-Requirements }
        "3" { Install-Dependencies }
        "4" { Build-Executable }
        "5" { Start-Program }
        "6" { Show-CleanMenu }
        "0" { 
            Write-Host ""
            Write-Host "Obrigado por usar o Game Translator!" -ForegroundColor $ColorDestaque
            Write-Host ""
            Start-Sleep -Seconds 2
            exit 0
        }
        default {
            Write-Host ""
            Write-Host "[ERRO] Opcao invalida! Tente novamente." -ForegroundColor $ColorErro
            Write-Host ""
            Read-Host "Pressione Enter para continuar"
        }
    }
} while ($true)
