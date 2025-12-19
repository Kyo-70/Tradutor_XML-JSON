@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
:: GAME TRANSLATOR - EXECUCAO RAPIDA v1.0.5
:: ============================================================================

:: Habilita cores ANSI
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
chcp 65001 >nul 2>&1

:: Define cores
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

set "RESET=%ESC%[0m"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "CYAN=%ESC%[96m"
set "RED=%ESC%[91m"
set "WHITE=%ESC%[97m"

set "CHECK=[OK]"
set "CROSS=[X]"
set "ARROW=[>]"

title Game Translator

set "SCRIPT_DIR=%~dp0"
set "EXE_PATH=%SCRIPT_DIR%dist\GameTranslator.exe"

:: Verifica se o executavel existe
if exist "%EXE_PATH%" (
    echo.
    echo %GREEN%%ARROW%%RESET% Iniciando Game Translator...
    start "" "%EXE_PATH%"
    exit /b 0
)

:: Se nao existe, tenta via Python
echo.
echo %YELLOW%%ARROW%%RESET% Executavel nao encontrado. Iniciando via Python...
echo.

:: Detecta Python
set "PY_CMD="

py --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py"
    echo %GREEN%%CHECK%%RESET% Usando Python Launcher %WHITE%[py]%RESET%
    goto :RUN
)

python --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=python"
    echo %GREEN%%CHECK%%RESET% Usando Python %WHITE%[python]%RESET%
    goto :RUN
)

echo %RED%%CROSS%%RESET% Python nao encontrado!
echo %WHITE%Execute%RESET% %CYAN%INSTALAR.bat%RESET% %WHITE%primeiro.%RESET%
pause
exit /b 1

:RUN
echo.
echo %YELLOW%%ARROW%%RESET% Verificando dependencias...

!PY_CMD! -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo   %YELLOW%%ARROW%%RESET% Instalando PySide6...
    !PY_CMD! -m pip install PySide6 >nul 2>&1
)

!PY_CMD! -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo   %YELLOW%%ARROW%%RESET% Instalando requests...
    !PY_CMD! -m pip install requests >nul 2>&1
)

!PY_CMD! -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo   %YELLOW%%ARROW%%RESET% Instalando psutil...
    !PY_CMD! -m pip install psutil >nul 2>&1
)

echo %GREEN%%CHECK%%RESET% Dependencias OK!
echo.
echo %GREEN%%ARROW%%RESET% Iniciando Game Translator...
echo.

cd /d "%SCRIPT_DIR%src"
!PY_CMD! main.py

pause
