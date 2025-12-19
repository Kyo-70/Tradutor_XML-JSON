@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
:: GAME TRANSLATOR - VERIFICACAO DO SISTEMA v1.0.5
:: Com cores ANSI funcionais no Windows 10/11
:: ============================================================================

:: Habilita suporte a cores ANSI
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1

chcp 65001 >nul 2>&1

:: Define cores
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

set "RESET=%ESC%[0m"
set "BOLD=%ESC%[1m"
set "RED=%ESC%[91m"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "BLUE=%ESC%[94m"
set "MAGENTA=%ESC%[95m"
set "CYAN=%ESC%[96m"
set "WHITE=%ESC%[97m"

set "CHECK=[OK]"
set "CROSS=[X]"
set "ARROW=[>]"
set "INFO=[i]"
set "WARN=[!]"

title Game Translator - Verificacao do Sistema

cls
echo.
echo %CYAN%========================================================================%RESET%
echo   %BOLD%%WHITE%GAME TRANSLATOR - VERIFICACAO DO SISTEMA%RESET%
echo %CYAN%========================================================================%RESET%
echo.

set "ERROS=0"
set "AVISOS=0"
set "SCRIPT_DIR=%~dp0"
set "PY_CMD="

:: ============================================================================
:: DETECTAR PYTHON
:: ============================================================================
echo %YELLOW%%INFO% [1/4] Verificando Python...%RESET%
echo.

py --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py"
    for /f "tokens=2" %%v in ('py --version 2^>nul') do (
        echo   %GREEN%%CHECK%%RESET% Python %CYAN%%%v%RESET% encontrado %WHITE%[comando: py]%RESET%
    )
    goto :CHECK_PIP
)

python --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=python"
    for /f "tokens=2" %%v in ('python --version 2^>nul') do (
        echo   %GREEN%%CHECK%%RESET% Python %CYAN%%%v%RESET% encontrado %WHITE%[comando: python]%RESET%
    )
    goto :CHECK_PIP
)

echo   %RED%%CROSS%%RESET% Python %RED%NAO ENCONTRADO%RESET%
echo   %WHITE%Baixe em:%RESET% %CYAN%https://www.python.org/downloads/%RESET%
set /a ERROS+=1
goto :CHECK_FILES

:: ============================================================================
:: VERIFICAR PIP
:: ============================================================================
:CHECK_PIP
echo.
echo %YELLOW%%INFO% [2/4] Verificando pip...%RESET%
echo.

!PY_CMD! -m pip --version >nul 2>&1
if errorlevel 1 (
    echo   %RED%%CROSS%%RESET% pip %RED%NAO ENCONTRADO%RESET%
    set /a ERROS+=1
) else (
    echo   %GREEN%%CHECK%%RESET% pip %GREEN%instalado%RESET%
)

:: ============================================================================
:: VERIFICAR BIBLIOTECAS
:: ============================================================================
echo.
echo %YELLOW%%INFO% [3/4] Verificando bibliotecas...%RESET%
echo.

!PY_CMD! -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo   %YELLOW%%WARN%%RESET% PySide6: %YELLOW%Nao instalado%RESET%
    set /a AVISOS+=1
    set "NEED_PYSIDE=1"
) else (
    echo   %GREEN%%CHECK%%RESET% PySide6: %GREEN%OK%RESET%
)

!PY_CMD! -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo   %YELLOW%%WARN%%RESET% requests: %YELLOW%Nao instalado%RESET%
    set /a AVISOS+=1
    set "NEED_REQUESTS=1"
) else (
    echo   %GREEN%%CHECK%%RESET% requests: %GREEN%OK%RESET%
)

!PY_CMD! -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo   %YELLOW%%WARN%%RESET% psutil: %YELLOW%Nao instalado%RESET%
    set /a AVISOS+=1
    set "NEED_PSUTIL=1"
) else (
    echo   %GREEN%%CHECK%%RESET% psutil: %GREEN%OK%RESET%
)

!PY_CMD! -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo   %YELLOW%%WARN%%RESET% PyInstaller: %YELLOW%Nao instalado%RESET%
    set /a AVISOS+=1
    set "NEED_PYINSTALLER=1"
) else (
    echo   %GREEN%%CHECK%%RESET% PyInstaller: %GREEN%OK%RESET%
)

:: ============================================================================
:: VERIFICAR ARQUIVOS
:: ============================================================================
:CHECK_FILES
echo.
echo %YELLOW%%INFO% [4/4] Verificando arquivos do projeto...%RESET%
echo.

if exist "%SCRIPT_DIR%src\main.py" (
    echo   %GREEN%%CHECK%%RESET% src\main.py
) else (
    echo   %RED%%CROSS%%RESET% src\main.py %RED%NAO ENCONTRADO%RESET%
    set /a ERROS+=1
)

if exist "%SCRIPT_DIR%src\gui\main_window.py" (
    echo   %GREEN%%CHECK%%RESET% src\gui\main_window.py
) else (
    echo   %RED%%CROSS%%RESET% src\gui\main_window.py %RED%NAO ENCONTRADO%RESET%
    set /a ERROS+=1
)

if exist "%SCRIPT_DIR%src\database.py" (
    echo   %GREEN%%CHECK%%RESET% src\database.py
) else (
    echo   %RED%%CROSS%%RESET% src\database.py %RED%NAO ENCONTRADO%RESET%
    set /a ERROS+=1
)

if exist "%SCRIPT_DIR%dist\GameTranslator.exe" (
    echo   %GREEN%%CHECK%%RESET% Executavel %GREEN%ja criado%RESET%
) else (
    echo   %BLUE%%INFO%%RESET% Executavel %BLUE%ainda nao criado%RESET%
)

:: ============================================================================
:: RESUMO
:: ============================================================================
echo.
echo %CYAN%========================================================================%RESET%
echo   %BOLD%%WHITE%RESUMO%RESET%
echo %CYAN%========================================================================%RESET%
echo.

if !ERROS! EQU 0 (
    if !AVISOS! EQU 0 (
        echo   %GREEN%%CHECK% SISTEMA PRONTO!%RESET%
        echo   %WHITE%Execute%RESET% %CYAN%INSTALAR.bat%RESET% %WHITE%para criar o executavel.%RESET%
    ) else (
        echo   %YELLOW%%WARN% Sistema OK, mas faltam !AVISOS! dependencia(s).%RESET%
        echo.
        set /p "INSTALAR=%YELLOW%Instalar dependencias agora? (S/N):%RESET% "
        if /i "!INSTALAR!"=="S" (
            echo.
            echo %BLUE%%ARROW%%RESET% Instalando dependencias...
            echo.
            
            if defined NEED_PYSIDE (
                echo   %BLUE%%ARROW%%RESET% Instalando PySide6...
                !PY_CMD! -m pip install PySide6>=6.6.0
            )
            
            if defined NEED_REQUESTS (
                echo   %BLUE%%ARROW%%RESET% Instalando requests...
                !PY_CMD! -m pip install requests>=2.31.0
            )
            
            if defined NEED_PSUTIL (
                echo   %BLUE%%ARROW%%RESET% Instalando psutil...
                !PY_CMD! -m pip install psutil>=5.9.0
            )
            
            if defined NEED_PYINSTALLER (
                echo   %BLUE%%ARROW%%RESET% Instalando PyInstaller...
                !PY_CMD! -m pip install pyinstaller
            )
            
            echo.
            echo %GREEN%%CHECK% Pronto! Execute%RESET% %CYAN%INSTALAR.bat%RESET% %GREEN%para criar o executavel.%RESET%
        )
    )
) else (
    echo   %RED%%CROSS% PROBLEMAS ENCONTRADOS: !ERROS! erro(s), !AVISOS! aviso(s)%RESET%
    echo   %WHITE%Corrija os erros antes de continuar.%RESET%
)

echo.
echo %CYAN%========================================================================%RESET%
echo.
pause
