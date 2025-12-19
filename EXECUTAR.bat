@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
:: GAME TRANSLATOR - EXECUCAO RAPIDA
:: Versao: 1.0.4
:: ============================================================================

chcp 65001 >nul 2>&1
title Game Translator

set "SCRIPT_DIR=%~dp0"
set "EXE_PATH=%SCRIPT_DIR%dist\GameTranslator.exe"

:: Verifica se o executavel existe
if exist "%EXE_PATH%" (
    echo Iniciando Game Translator...
    start "" "%EXE_PATH%"
    exit /b 0
)

:: Se nao existe, tenta via Python
echo Executavel nao encontrado. Iniciando via Python...
echo.

:: Detecta Python
set "PY_CMD="

py --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py"
    goto :RUN
)

python --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=python"
    goto :RUN
)

echo ERRO: Python nao encontrado!
echo Execute INSTALAR.bat primeiro.
pause
exit /b 1

:RUN
:: Verifica dependencias
!PY_CMD! -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo Instalando PySide6...
    !PY_CMD! -m pip install PySide6 >nul 2>&1
)

!PY_CMD! -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Instalando requests...
    !PY_CMD! -m pip install requests >nul 2>&1
)

!PY_CMD! -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo Instalando psutil...
    !PY_CMD! -m pip install psutil >nul 2>&1
)

echo Iniciando...
echo.

cd /d "%SCRIPT_DIR%src"
!PY_CMD! main.py

pause
