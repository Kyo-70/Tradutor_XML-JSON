@echo off
chcp 65001 >nul 2>&1
title Game Translator - Verificacao do Sistema

:: Verifica se Python esta disponivel
py --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ========================================================================
    echo   ERRO: Python nao encontrado!
    echo ========================================================================
    echo.
    echo   Baixe Python em: https://www.python.org/downloads/
    echo   Durante a instalacao, marque "Add Python to PATH"
    echo.
    echo ========================================================================
    echo.
    pause
    exit /b 1
)

:: Executa o script Python com cores
cd /d "%~dp0src"
py verificar_sistema.py --auto-instalar

:: Retorna o codigo de saida do script Python
exit /b %ERRORLEVEL%
