@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
:: GAME TRANSLATOR - INSTALADOR v1.0.5
:: Com cores ANSI funcionais no Windows 10/11
:: ============================================================================

:: Habilita suporte a cores ANSI no Windows 10/11
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1

:: Configura codepage UTF-8
chcp 65001 >nul 2>&1

:: Define cores usando escape sequences
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

:: Cores
set "RESET=%ESC%[0m"
set "BOLD=%ESC%[1m"
set "RED=%ESC%[91m"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "BLUE=%ESC%[94m"
set "MAGENTA=%ESC%[95m"
set "CYAN=%ESC%[96m"
set "WHITE=%ESC%[97m"
set "BG_BLUE=%ESC%[44m"
set "BG_GREEN=%ESC%[42m"
set "BG_RED=%ESC%[41m"

:: Icones (caracteres Unicode)
set "CHECK=[OK]"
set "CROSS=[X]"
set "ARROW=[>]"
set "STAR=[*]"
set "INFO=[i]"
set "WARN=[!]"

:: Variaveis
set "SCRIPT_DIR=%~dp0"
set "DIST_DIR=%SCRIPT_DIR%dist"
set "BUILD_DIR=%SCRIPT_DIR%build"
set "PY_CMD="

title Game Translator - Instalador v1.0.5

:MENU_PRINCIPAL
cls
echo.
echo %CYAN%========================================================================%RESET%
echo.
echo   %BOLD%%WHITE%   ____                        _____                    _       _             %RESET%
echo   %BOLD%%WHITE%  / ___^|  __ _  _ __ ___    __|_   _^| _ __  __ _  _ __  ^| ^| __ _^| ^|_  ___   _ ^|%RESET%
echo   %BOLD%%WHITE% ^| ^|  _  / _` ^|^| '_ ` _ \  / _ \^| ^|  ^| '__^|/ _` ^|^| '_ \ ^| ^|/ _` ^| __^|/ _ \ ^| '_^|%RESET%
echo   %BOLD%%WHITE% ^| ^|_^| ^|^| (_^| ^|^| ^| ^| ^| ^| ^|^|  __/^| ^|  ^| ^|  ^| (_^| ^|^| ^| ^| ^|^| ^| (_^| ^| ^|_^| (_) ^|^| ^|  %RESET%
echo   %BOLD%%WHITE%  \____^| \__,_^|^|_^| ^|_^| ^|_^| \___^|^|_^|  ^|_^|   \__,_^|^|_^| ^|_^|^|_^|\__,_^|\__^|\___/ ^|_^|  %RESET%
echo.
echo %CYAN%========================================================================%RESET%
echo.
echo   %BOLD%%MAGENTA%Sistema Profissional de Traducao para Jogos e Mods%RESET%
echo   %WHITE%Versao 1.0.5%RESET%
echo.
echo %CYAN%========================================================================%RESET%
echo.
echo   %GREEN%%ARROW%%RESET% %BOLD%[1]%RESET% %WHITE%Instalacao Completa%RESET% %YELLOW%(Recomendado)%RESET%
echo.
echo   %BLUE%%ARROW%%RESET% %BOLD%[2]%RESET% %WHITE%Verificar Requisitos do Sistema%RESET%
echo.
echo   %BLUE%%ARROW%%RESET% %BOLD%[3]%RESET% %WHITE%Instalar Dependencias%RESET%
echo.
echo   %BLUE%%ARROW%%RESET% %BOLD%[4]%RESET% %WHITE%Criar Executavel (.exe)%RESET%
echo.
echo   %BLUE%%ARROW%%RESET% %BOLD%[5]%RESET% %WHITE%Executar Programa (dev)%RESET%
echo.
echo   %RED%%ARROW%%RESET% %BOLD%[0]%RESET% %WHITE%Sair%RESET%
echo.
echo %CYAN%========================================================================%RESET%
echo.

set /p "OPCAO=%YELLOW%Digite sua opcao:%RESET% "

if "%OPCAO%"=="1" goto INSTALACAO_COMPLETA
if "%OPCAO%"=="2" goto VERIFICAR_REQUISITOS
if "%OPCAO%"=="3" goto INSTALAR_DEPENDENCIAS
if "%OPCAO%"=="4" goto CRIAR_EXECUTAVEL
if "%OPCAO%"=="5" goto EXECUTAR_PROGRAMA
if "%OPCAO%"=="0" goto SAIR

echo.
echo %RED%%CROSS% Opcao invalida!%RESET%
timeout /t 2 >nul
goto MENU_PRINCIPAL

:: ============================================================================
:: INSTALACAO COMPLETA
:: ============================================================================
:INSTALACAO_COMPLETA
cls
echo.
echo %CYAN%========================================================================%RESET%
echo   %BOLD%%WHITE%INSTALACAO COMPLETA%RESET%
echo %CYAN%========================================================================%RESET%
echo.

call :DETECTAR_PYTHON
if "!PY_CMD!"=="" goto MENU_PRINCIPAL

echo.
echo %YELLOW%%STAR% ETAPA 1/3:%RESET% %WHITE%Instalando dependencias...%RESET%
echo.
call :INSTALAR_DEPS

echo.
echo %YELLOW%%STAR% ETAPA 2/3:%RESET% %WHITE%Criando executavel...%RESET%
echo.
call :CRIAR_EXE

echo.
echo %YELLOW%%STAR% ETAPA 3/3:%RESET% %WHITE%Finalizando...%RESET%
echo.

if exist "%DIST_DIR%\GameTranslator.exe" (
    echo %CYAN%========================================================================%RESET%
    echo.
    echo   %GREEN%%CHECK% INSTALACAO CONCLUIDA COM SUCESSO!%RESET%
    echo.
    echo   %WHITE%Executavel criado em:%RESET%
    echo   %CYAN%%DIST_DIR%\GameTranslator.exe%RESET%
    echo.
    echo %CYAN%========================================================================%RESET%
    echo.
    set /p "ABRIR=%YELLOW%Deseja abrir o programa agora? (S/N):%RESET% "
    if /i "!ABRIR!"=="S" start "" "%DIST_DIR%\GameTranslator.exe"
) else (
    echo %RED%%CROSS% ERRO: Falha ao criar executavel!%RESET%
    echo %WHITE%Verifique os erros acima.%RESET%
)

echo.
pause
goto MENU_PRINCIPAL

:: ============================================================================
:: VERIFICAR REQUISITOS
:: ============================================================================
:VERIFICAR_REQUISITOS
cls
echo.
echo %CYAN%========================================================================%RESET%
echo   %BOLD%%WHITE%VERIFICACAO DE REQUISITOS%RESET%
echo %CYAN%========================================================================%RESET%
echo.

call :DETECTAR_PYTHON
if "!PY_CMD!"=="" (
    echo.
    pause
    goto MENU_PRINCIPAL
)

echo.
echo %YELLOW%%INFO% Verificando bibliotecas...%RESET%
echo.

!PY_CMD! -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo   %RED%%CROSS%%RESET% PySide6: %RED%NAO INSTALADO%RESET%
) else (
    echo   %GREEN%%CHECK%%RESET% PySide6: %GREEN%OK%RESET%
)

!PY_CMD! -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo   %RED%%CROSS%%RESET% requests: %RED%NAO INSTALADO%RESET%
) else (
    echo   %GREEN%%CHECK%%RESET% requests: %GREEN%OK%RESET%
)

!PY_CMD! -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo   %RED%%CROSS%%RESET% psutil: %RED%NAO INSTALADO%RESET%
) else (
    echo   %GREEN%%CHECK%%RESET% psutil: %GREEN%OK%RESET%
)

!PY_CMD! -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo   %RED%%CROSS%%RESET% PyInstaller: %RED%NAO INSTALADO%RESET%
) else (
    echo   %GREEN%%CHECK%%RESET% PyInstaller: %GREEN%OK%RESET%
)

echo.
echo %YELLOW%%INFO% Verificando arquivos...%RESET%
echo.

if exist "%SCRIPT_DIR%src\main.py" (
    echo   %GREEN%%CHECK%%RESET% src\main.py: %GREEN%OK%RESET%
) else (
    echo   %RED%%CROSS%%RESET% src\main.py: %RED%NAO ENCONTRADO%RESET%
)

if exist "%SCRIPT_DIR%src\gui\main_window.py" (
    echo   %GREEN%%CHECK%%RESET% src\gui\main_window.py: %GREEN%OK%RESET%
) else (
    echo   %RED%%CROSS%%RESET% src\gui\main_window.py: %RED%NAO ENCONTRADO%RESET%
)

if exist "%SCRIPT_DIR%dist\GameTranslator.exe" (
    echo   %GREEN%%CHECK%%RESET% Executavel: %GREEN%JA CRIADO%RESET%
) else (
    echo   %YELLOW%%INFO%%RESET% Executavel: %YELLOW%Ainda nao criado%RESET%
)

echo.
pause
goto MENU_PRINCIPAL

:: ============================================================================
:: INSTALAR DEPENDENCIAS
:: ============================================================================
:INSTALAR_DEPENDENCIAS
cls
echo.
echo %CYAN%========================================================================%RESET%
echo   %BOLD%%WHITE%INSTALACAO DE DEPENDENCIAS%RESET%
echo %CYAN%========================================================================%RESET%
echo.

call :DETECTAR_PYTHON
if "!PY_CMD!"=="" goto MENU_PRINCIPAL

call :INSTALAR_DEPS

echo.
echo %GREEN%%CHECK% Dependencias instaladas com sucesso!%RESET%
echo.
pause
goto MENU_PRINCIPAL

:INSTALAR_DEPS
echo %BLUE%%ARROW%%RESET% Atualizando pip...
!PY_CMD! -m pip install --upgrade pip >nul 2>&1

echo %BLUE%%ARROW%%RESET% Instalando PySide6...
!PY_CMD! -m pip install PySide6>=6.6.0

echo %BLUE%%ARROW%%RESET% Instalando requests...
!PY_CMD! -m pip install requests>=2.31.0

echo %BLUE%%ARROW%%RESET% Instalando psutil...
!PY_CMD! -m pip install psutil>=5.9.0

echo %BLUE%%ARROW%%RESET% Instalando PyInstaller...
!PY_CMD! -m pip install pyinstaller

exit /b 0

:: ============================================================================
:: CRIAR EXECUTAVEL
:: ============================================================================
:CRIAR_EXECUTAVEL
cls
echo.
echo %CYAN%========================================================================%RESET%
echo   %BOLD%%WHITE%CRIACAO DO EXECUTAVEL%RESET%
echo %CYAN%========================================================================%RESET%
echo.

call :DETECTAR_PYTHON
if "!PY_CMD!"=="" goto MENU_PRINCIPAL

call :CRIAR_EXE

echo.
if exist "%DIST_DIR%\GameTranslator.exe" (
    echo %GREEN%%CHECK% Executavel criado com sucesso!%RESET%
    echo %WHITE%Local:%RESET% %CYAN%%DIST_DIR%\GameTranslator.exe%RESET%
    echo.
    set /p "ABRIR=%YELLOW%Abrir pasta? (S/N):%RESET% "
    if /i "!ABRIR!"=="S" explorer "%DIST_DIR%"
) else (
    echo %RED%%CROSS% ERRO ao criar executavel!%RESET%
)

echo.
pause
goto MENU_PRINCIPAL

:CRIAR_EXE
cd /d "%SCRIPT_DIR%"

:: Limpa builds anteriores
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%" >nul 2>&1
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%" >nul 2>&1
if not exist "profiles" mkdir profiles

echo %YELLOW%%INFO% Criando executavel (isso pode levar alguns minutos)...%RESET%
echo.

:: Usa o arquivo .spec se existir
if exist "%SCRIPT_DIR%GameTranslator.spec" (
    !PY_CMD! -m PyInstaller --noconfirm --clean "%SCRIPT_DIR%GameTranslator.spec"
) else (
    !PY_CMD! -m PyInstaller --name="GameTranslator" --onefile --windowed --noconfirm --clean ^
        --paths="%SCRIPT_DIR%src" ^
        --hidden-import=PySide6.QtCore ^
        --hidden-import=PySide6.QtGui ^
        --hidden-import=PySide6.QtWidgets ^
        --hidden-import=sqlite3 ^
        --hidden-import=psutil ^
        --hidden-import=database ^
        --hidden-import=regex_profiles ^
        --hidden-import=file_processor ^
        --hidden-import=smart_translator ^
        --hidden-import=translation_api ^
        --hidden-import=logger ^
        --hidden-import=security ^
        --add-data "src;src" ^
        "%SCRIPT_DIR%src\main.py"
)

:: Copia pasta profiles
if not exist "%DIST_DIR%\profiles" mkdir "%DIST_DIR%\profiles" >nul 2>&1

exit /b 0

:: ============================================================================
:: EXECUTAR PROGRAMA
:: ============================================================================
:EXECUTAR_PROGRAMA
cls
echo.
echo %CYAN%========================================================================%RESET%
echo   %BOLD%%WHITE%EXECUTAR PROGRAMA%RESET%
echo %CYAN%========================================================================%RESET%
echo.

call :DETECTAR_PYTHON
if "!PY_CMD!"=="" goto MENU_PRINCIPAL

echo %GREEN%%ARROW% Iniciando Game Translator...%RESET%
echo.

cd /d "%SCRIPT_DIR%src"
!PY_CMD! main.py

echo.
pause
goto MENU_PRINCIPAL

:: ============================================================================
:: DETECTAR PYTHON
:: ============================================================================
:DETECTAR_PYTHON
set "PY_CMD="

:: Tenta py primeiro
py --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py"
    for /f "tokens=2" %%v in ('py --version 2^>nul') do (
        echo %GREEN%%CHECK%%RESET% Python encontrado: %CYAN%%%v%RESET% %WHITE%[comando: py]%RESET%
    )
    exit /b 0
)

:: Tenta python
python --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=python"
    for /f "tokens=2" %%v in ('python --version 2^>nul') do (
        echo %GREEN%%CHECK%%RESET% Python encontrado: %CYAN%%%v%RESET% %WHITE%[comando: python]%RESET%
    )
    exit /b 0
)

:: Nao encontrado
echo.
echo %RED%%CROSS% ERRO: Python nao encontrado!%RESET%
echo.
echo %WHITE%Instale Python de:%RESET% %CYAN%https://www.python.org/downloads/%RESET%
echo %WHITE%Durante a instalacao, marque%RESET% %YELLOW%"Add Python to PATH"%RESET%
echo.
set /p "ABRIR=%YELLOW%Abrir site de download? (S/N):%RESET% "
if /i "!ABRIR!"=="S" start https://www.python.org/downloads/

exit /b 1

:: ============================================================================
:: SAIR
:: ============================================================================
:SAIR
cls
echo.
echo %CYAN%========================================================================%RESET%
echo.
echo   %GREEN%Obrigado por usar o Game Translator!%RESET%
echo.
echo   %WHITE%Desenvolvido com%RESET% %RED%<3%RESET% %WHITE%por Manus AI%RESET%
echo.
echo %CYAN%========================================================================%RESET%
echo.
timeout /t 2 >nul
exit /b 0
