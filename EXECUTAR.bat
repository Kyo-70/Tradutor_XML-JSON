@echo off
chcp 65001 >nul 2>&1
title Game Translator

:: Define cores customizadas usando ANSI escape codes
:: Habilita suporte a cores ANSI no Windows 10+
for /F %%A in ('prompt $E ^| cmd') do set "ESC=%%A"

:: Cores personalizadas
set "COLOR_RESET=%ESC%[0m"
set "COLOR_TITULO=%ESC%[95m%ESC%[1m"
set "COLOR_SUCESSO=%ESC%[92m%ESC%[1m"
set "COLOR_ERRO=%ESC%[91m%ESC%[1m"
set "COLOR_AVISO=%ESC%[93m%ESC%[1m"
set "COLOR_INFO=%ESC%[96m%ESC%[1m"

cls
echo.
echo %COLOR_TITULO%========================================================================%COLOR_RESET%
echo %COLOR_TITULO%  GAME TRANSLATOR - EXECUCAO RAPIDA%COLOR_RESET%
echo %COLOR_TITULO%========================================================================%COLOR_RESET%
echo.

:: Verifica se o executavel existe
if exist "%~dp0dist\GameTranslator.exe" (
    echo %COLOR_INFO%Iniciando Game Translator...%COLOR_RESET%
    start "" "%~dp0dist\GameTranslator.exe"
    exit /b 0
)

:: Se nao existe, tenta via Python
echo %COLOR_AVISO%Executavel nao encontrado. Iniciando via Python...%COLOR_RESET%
echo.

:: Verifica Python
py --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_ERRO%[ERRO] Python nao encontrado!%COLOR_RESET%
    echo %COLOR_INFO%Execute INSTALAR.bat primeiro.%COLOR_RESET%
    echo.
    pause
    exit /b 1
)

echo %COLOR_INFO%Verificando dependencias...%COLOR_RESET%
echo.

:: Verifica e instala dependencias se necessario
py -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo %COLOR_INFO%   Instalando PySide6...%COLOR_RESET%
    py -m pip install PySide6 --quiet
)

py -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo %COLOR_INFO%   Instalando requests...%COLOR_RESET%
    py -m pip install requests --quiet
)

py -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo %COLOR_INFO%   Instalando psutil...%COLOR_RESET%
    py -m pip install psutil --quiet
)

py -c "import colorama" >nul 2>&1
if errorlevel 1 (
    echo %COLOR_INFO%   Instalando colorama...%COLOR_RESET%
    py -m pip install colorama --quiet
)

echo %COLOR_SUCESSO%[OK] Dependencias verificadas!%COLOR_RESET%
echo.
echo %COLOR_INFO%Iniciando Game Translator...%COLOR_RESET%
echo.

cd /d "%~dp0src"
py main.py

echo.
echo %COLOR_INFO%Programa encerrado.%COLOR_RESET%
pause
