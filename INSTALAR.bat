@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
:: GAME TRANSLATOR - INSTALADOR E CONSTRUTOR DE EXECUTAVEL
:: Versao: 1.0.4 - Compativel com Windows 11
:: ============================================================================

chcp 65001 >nul 2>&1

set "SCRIPT_DIR=%~dp0"
set "DIST_DIR=%SCRIPT_DIR%dist"
set "BUILD_DIR=%SCRIPT_DIR%build"
set "PY_CMD="

title Game Translator - Instalador v1.0.4

:MENU_PRINCIPAL
cls
echo.
echo ========================================================================
echo.
echo   GAME TRANSLATOR - Sistema de Traducao para Jogos e Mods
echo   Versao 1.0.4
echo.
echo ========================================================================
echo.
echo   [1] Instalacao Completa (Recomendado)
echo   [2] Verificar Requisitos do Sistema
echo   [3] Instalar Dependencias
echo   [4] Criar Executavel (.exe)
echo   [5] Executar Programa (modo desenvolvimento)
echo   [0] Sair
echo.
echo ========================================================================
echo.

set /p "OPCAO=Digite sua opcao: "

if "%OPCAO%"=="1" goto INSTALACAO_COMPLETA
if "%OPCAO%"=="2" goto VERIFICAR_REQUISITOS
if "%OPCAO%"=="3" goto INSTALAR_DEPENDENCIAS
if "%OPCAO%"=="4" goto CRIAR_EXECUTAVEL
if "%OPCAO%"=="5" goto EXECUTAR_PROGRAMA
if "%OPCAO%"=="0" goto SAIR

echo.
echo Opcao invalida!
pause
goto MENU_PRINCIPAL

:: ============================================================================
:: INSTALACAO COMPLETA
:: ============================================================================
:INSTALACAO_COMPLETA
cls
echo.
echo ========================================================================
echo  INSTALACAO COMPLETA
echo ========================================================================
echo.

call :DETECTAR_PYTHON
if "!PY_CMD!"=="" goto MENU_PRINCIPAL

echo.
echo [ETAPA 1/3] Instalando dependencias...
echo.
call :INSTALAR_DEPS

echo.
echo [ETAPA 2/3] Criando executavel...
echo.
call :CRIAR_EXE

echo.
echo [ETAPA 3/3] Finalizando...
echo.

if exist "%DIST_DIR%\GameTranslator.exe" (
    echo ========================================================================
    echo.
    echo   INSTALACAO CONCLUIDA COM SUCESSO!
    echo.
    echo   Executavel criado em:
    echo   %DIST_DIR%\GameTranslator.exe
    echo.
    echo ========================================================================
    echo.
    set /p "ABRIR=Deseja abrir o programa agora? (S/N): "
    if /i "!ABRIR!"=="S" start "" "%DIST_DIR%\GameTranslator.exe"
) else (
    echo ERRO: Falha ao criar executavel!
    echo Verifique os erros acima.
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
echo ========================================================================
echo  VERIFICACAO DE REQUISITOS
echo ========================================================================
echo.

call :DETECTAR_PYTHON
if "!PY_CMD!"=="" (
    echo.
    pause
    goto MENU_PRINCIPAL
)

echo.
echo Verificando bibliotecas...
echo.

!PY_CMD! -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo   PySide6: NAO INSTALADO
) else (
    echo   PySide6: OK
)

!PY_CMD! -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo   requests: NAO INSTALADO
) else (
    echo   requests: OK
)

!PY_CMD! -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo   psutil: NAO INSTALADO
) else (
    echo   psutil: OK
)

!PY_CMD! -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo   PyInstaller: NAO INSTALADO
) else (
    echo   PyInstaller: OK
)

echo.
echo Verificando arquivos...
echo.

if exist "%SCRIPT_DIR%src\main.py" (
    echo   src\main.py: OK
) else (
    echo   src\main.py: NAO ENCONTRADO
)

if exist "%SCRIPT_DIR%src\gui\main_window.py" (
    echo   src\gui\main_window.py: OK
) else (
    echo   src\gui\main_window.py: NAO ENCONTRADO
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
echo ========================================================================
echo  INSTALACAO DE DEPENDENCIAS
echo ========================================================================
echo.

call :DETECTAR_PYTHON
if "!PY_CMD!"=="" goto MENU_PRINCIPAL

call :INSTALAR_DEPS

echo.
echo Dependencias instaladas!
echo.
pause
goto MENU_PRINCIPAL

:INSTALAR_DEPS
echo Atualizando pip...
!PY_CMD! -m pip install --upgrade pip >nul 2>&1

echo Instalando PySide6...
!PY_CMD! -m pip install PySide6>=6.6.0

echo Instalando requests...
!PY_CMD! -m pip install requests>=2.31.0

echo Instalando psutil...
!PY_CMD! -m pip install psutil>=5.9.0

echo Instalando PyInstaller...
!PY_CMD! -m pip install pyinstaller

exit /b 0

:: ============================================================================
:: CRIAR EXECUTAVEL
:: ============================================================================
:CRIAR_EXECUTAVEL
cls
echo.
echo ========================================================================
echo  CRIACAO DO EXECUTAVEL
echo ========================================================================
echo.

call :DETECTAR_PYTHON
if "!PY_CMD!"=="" goto MENU_PRINCIPAL

call :CRIAR_EXE

echo.
if exist "%DIST_DIR%\GameTranslator.exe" (
    echo Executavel criado com sucesso!
    echo Local: %DIST_DIR%\GameTranslator.exe
    echo.
    set /p "ABRIR=Abrir pasta? (S/N): "
    if /i "!ABRIR!"=="S" explorer "%DIST_DIR%"
) else (
    echo ERRO ao criar executavel!
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

echo Criando executavel (isso pode levar alguns minutos)...
echo.

:: Usa o arquivo .spec se existir, senao usa comando direto
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
echo ========================================================================
echo  EXECUTAR PROGRAMA
echo ========================================================================
echo.

call :DETECTAR_PYTHON
if "!PY_CMD!"=="" goto MENU_PRINCIPAL

echo Iniciando Game Translator...
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
    for /f "tokens=2" %%v in ('py --version 2^>nul') do echo Python encontrado: %%v [comando: py]
    exit /b 0
)

:: Tenta python
python --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=python"
    for /f "tokens=2" %%v in ('python --version 2^>nul') do echo Python encontrado: %%v [comando: python]
    exit /b 0
)

:: Nao encontrado
echo.
echo ERRO: Python nao encontrado!
echo.
echo Instale Python de: https://www.python.org/downloads/
echo Durante a instalacao, marque "Add Python to PATH"
echo.
set /p "ABRIR=Abrir site de download? (S/N): "
if /i "!ABRIR!"=="S" start https://www.python.org/downloads/

exit /b 1

:: ============================================================================
:: SAIR
:: ============================================================================
:SAIR
echo.
echo Obrigado por usar o Game Translator!
echo.
timeout /t 2 >nul
exit /b 0
