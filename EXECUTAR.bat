@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
:: GAME TRANSLATOR - EXECUCAO RAPIDA
:: Versao: 1.0.3 - Compativel com Windows 11 e Python Launcher (py)
:: ============================================================================

chcp 65001 >nul 2>&1
title Game Translator

:: Variaveis
set "SCRIPT_DIR=%~dp0"
set "EXE_PATH=%SCRIPT_DIR%dist\GameTranslator.exe"

:: Verifica se o executavel existe
if exist "%EXE_PATH%" (
    echo.
    echo [INFO] Iniciando Game Translator...
    start "" "%EXE_PATH%"
    exit /b 0
)

:: Se nao existe executavel, tenta executar via Python
echo.
echo [AVISO] Executavel nao encontrado. Tentando modo desenvolvimento...
echo.

:: Detecta comando Python (py ou python)
set "PY_CMD="

py --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py"
    echo [OK] Usando Python Launcher (py)
    goto :RUN
)

python --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=python"
    echo [OK] Usando Python (python)
    goto :RUN
)

:: Nenhum Python encontrado
echo [ERRO] Python nao encontrado!
echo.
echo Instale Python de: https://www.python.org/downloads/
echo Ou execute INSTALAR.bat para mais opcoes.
echo.
pause
exit /b 1

:RUN
:: Verifica e instala dependencias
echo [INFO] Verificando dependencias...

%PY_CMD% -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando PySide6...
    %PY_CMD% -m pip install PySide6 >nul 2>&1
)

%PY_CMD% -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando requests...
    %PY_CMD% -m pip install requests >nul 2>&1
)

%PY_CMD% -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando psutil...
    %PY_CMD% -m pip install psutil >nul 2>&1
)

echo [OK] Dependencias verificadas!
echo.
echo [INFO] Iniciando Game Translator...
echo.

cd /d "%SCRIPT_DIR%src"
%PY_CMD% main.py

pause
