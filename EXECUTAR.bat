@echo off
chcp 65001 >nul 2>&1
title Game Translator

echo.
echo ========================================================================
echo   GAME TRANSLATOR - EXECUCAO RAPIDA
echo ========================================================================
echo.

:: Verifica se o executavel existe
if exist "%~dp0dist\GameTranslator.exe" (
    echo Iniciando Game Translator...
    start "" "%~dp0dist\GameTranslator.exe"
    exit /b 0
)

:: Se nao existe, tenta via Python
echo Executavel nao encontrado. Iniciando via Python...
echo.

:: Verifica Python
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Execute INSTALAR.bat primeiro.
    echo.
    pause
    exit /b 1
)

echo Verificando dependencias...
echo.

:: Verifica e instala dependencias se necessario
py -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo    Instalando PySide6...
    py -m pip install PySide6 --quiet
)

py -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo    Instalando requests...
    py -m pip install requests --quiet
)

py -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo    Instalando psutil...
    py -m pip install psutil --quiet
)

py -c "import colorama" >nul 2>&1
if errorlevel 1 (
    echo    Instalando colorama...
    py -m pip install colorama --quiet
)

echo [OK] Dependencias verificadas!
echo.
echo Iniciando Game Translator...
echo.

cd /d "%~dp0src"
py main.py

echo.
echo Programa encerrado.
pause
