@echo off
chcp 65001 >nul 2>&1
title Game Translator - Verificacao do Sistema

:: Define cores customizadas usando ANSI escape codes
:: Habilita suporte a cores ANSI no Windows 10+
for /F %%A in ('echo prompt $E ^| cmd') do set "ESC=%%A"

:: Cores personalizadas
set "COLOR_RESET=%ESC%[0m"
set "COLOR_TITULO=%ESC%[95m%ESC%[1m"
set "COLOR_SUCESSO=%ESC%[92m%ESC%[1m"
set "COLOR_ERRO=%ESC%[91m%ESC%[1m"
set "COLOR_AVISO=%ESC%[93m%ESC%[1m"
set "COLOR_INFO=%ESC%[96m%ESC%[1m"

:: Verifica se Python esta disponivel
py --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo %COLOR_TITULO%========================================================================%COLOR_RESET%
    echo %COLOR_ERRO%  ERRO: Python nao encontrado!%COLOR_RESET%
    echo %COLOR_TITULO%========================================================================%COLOR_RESET%
    echo.
    echo %COLOR_INFO%  Baixe Python em: https://www.python.org/downloads/%COLOR_RESET%
    echo %COLOR_INFO%  Durante a instalacao, marque "Add Python to PATH"%COLOR_RESET%
    echo.
    echo %COLOR_TITULO%========================================================================%COLOR_RESET%
    echo.
    pause
    exit /b 1
)

:: Executa o script Python com cores
cd /d "%~dp0src"
py verificar_sistema.py --auto-instalar

:: Retorna o codigo de saida do script Python
exit /b %ERRORLEVEL%
