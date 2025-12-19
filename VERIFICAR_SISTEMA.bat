@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
:: GAME TRANSLATOR - VERIFICACAO DO SISTEMA
:: Versao: 1.0.4
:: ============================================================================

chcp 65001 >nul 2>&1
title Game Translator - Verificacao do Sistema

cls
echo.
echo ========================================================================
echo  GAME TRANSLATOR - VERIFICACAO DO SISTEMA
echo ========================================================================
echo.

set "ERROS=0"
set "AVISOS=0"
set "SCRIPT_DIR=%~dp0"
set "PY_CMD="

:: ============================================================================
:: DETECTAR PYTHON
:: ============================================================================
echo [1/4] Verificando Python...
echo.

py --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py"
    for /f "tokens=2" %%v in ('py --version 2^>nul') do (
        echo   OK: Python %%v encontrado [comando: py]
    )
    goto :CHECK_PIP
)

python --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=python"
    for /f "tokens=2" %%v in ('python --version 2^>nul') do (
        echo   OK: Python %%v encontrado [comando: python]
    )
    goto :CHECK_PIP
)

echo   ERRO: Python NAO encontrado!
echo   Baixe em: https://www.python.org/downloads/
set /a ERROS+=1
goto :CHECK_FILES

:: ============================================================================
:: VERIFICAR PIP
:: ============================================================================
:CHECK_PIP
echo.
echo [2/4] Verificando pip...
echo.

!PY_CMD! -m pip --version >nul 2>&1
if errorlevel 1 (
    echo   ERRO: pip nao encontrado
    set /a ERROS+=1
) else (
    echo   OK: pip instalado
)

:: ============================================================================
:: VERIFICAR BIBLIOTECAS
:: ============================================================================
echo.
echo [3/4] Verificando bibliotecas...
echo.

!PY_CMD! -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo   FALTA: PySide6
    set /a AVISOS+=1
    set "NEED_PYSIDE=1"
) else (
    echo   OK: PySide6
)

!PY_CMD! -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo   FALTA: requests
    set /a AVISOS+=1
    set "NEED_REQUESTS=1"
) else (
    echo   OK: requests
)

!PY_CMD! -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo   FALTA: psutil
    set /a AVISOS+=1
    set "NEED_PSUTIL=1"
) else (
    echo   OK: psutil
)

!PY_CMD! -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo   FALTA: PyInstaller
    set /a AVISOS+=1
    set "NEED_PYINSTALLER=1"
) else (
    echo   OK: PyInstaller
)

:: ============================================================================
:: VERIFICAR ARQUIVOS
:: ============================================================================
:CHECK_FILES
echo.
echo [4/4] Verificando arquivos do projeto...
echo.

if exist "%SCRIPT_DIR%src\main.py" (
    echo   OK: src\main.py
) else (
    echo   ERRO: src\main.py NAO encontrado
    set /a ERROS+=1
)

if exist "%SCRIPT_DIR%src\gui\main_window.py" (
    echo   OK: src\gui\main_window.py
) else (
    echo   ERRO: src\gui\main_window.py NAO encontrado
    set /a ERROS+=1
)

if exist "%SCRIPT_DIR%src\database.py" (
    echo   OK: src\database.py
) else (
    echo   ERRO: src\database.py NAO encontrado
    set /a ERROS+=1
)

if exist "%SCRIPT_DIR%dist\GameTranslator.exe" (
    echo   OK: Executavel ja criado
) else (
    echo   INFO: Executavel ainda nao criado
)

:: ============================================================================
:: RESUMO
:: ============================================================================
echo.
echo ========================================================================
echo  RESUMO
echo ========================================================================
echo.

if !ERROS! EQU 0 (
    if !AVISOS! EQU 0 (
        echo   Sistema PRONTO!
        echo   Execute INSTALAR.bat para criar o executavel.
    ) else (
        echo   Sistema OK, mas faltam !AVISOS! dependencia(s).
        echo.
        set /p "INSTALAR=Instalar dependencias agora? (S/N): "
        if /i "!INSTALAR!"=="S" (
            echo.
            echo Instalando...
            echo.
            
            if defined NEED_PYSIDE (
                echo   Instalando PySide6...
                !PY_CMD! -m pip install PySide6>=6.6.0
            )
            
            if defined NEED_REQUESTS (
                echo   Instalando requests...
                !PY_CMD! -m pip install requests>=2.31.0
            )
            
            if defined NEED_PSUTIL (
                echo   Instalando psutil...
                !PY_CMD! -m pip install psutil>=5.9.0
            )
            
            if defined NEED_PYINSTALLER (
                echo   Instalando PyInstaller...
                !PY_CMD! -m pip install pyinstaller
            )
            
            echo.
            echo Pronto! Execute INSTALAR.bat para criar o executavel.
        )
    )
) else (
    echo   PROBLEMAS encontrados: !ERROS! erro(s), !AVISOS! aviso(s)
    echo   Corrija os erros antes de continuar.
)

echo.
echo ========================================================================
echo.
pause
