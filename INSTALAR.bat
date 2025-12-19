@echo off
chcp 65001 >nul 2>&1
title Game Translator - Instalador v1.0.6

echo.
echo ========================================================================
echo.
echo     GAME TRANSLATOR - INSTALADOR v1.0.6
echo.
echo     Sistema Profissional de Traducao para Jogos e Mods
echo.
echo ========================================================================
echo.

:MENU
echo.
echo   [1] Instalacao Completa (Recomendado)
echo   [2] Verificar Requisitos
echo   [3] Instalar Dependencias
echo   [4] Criar Executavel (.exe)
echo   [5] Executar Programa (modo desenvolvedor)
echo   [0] Sair
echo.
set /p OPCAO="Digite sua opcao: "

if "%OPCAO%"=="1" goto INSTALACAO_COMPLETA
if "%OPCAO%"=="2" goto VERIFICAR
if "%OPCAO%"=="3" goto INSTALAR_DEPS
if "%OPCAO%"=="4" goto CRIAR_EXE
if "%OPCAO%"=="5" goto EXECUTAR
if "%OPCAO%"=="0" goto SAIR

echo.
echo [ERRO] Opcao invalida! Tente novamente.
echo.
pause
cls
goto MENU

:INSTALACAO_COMPLETA
cls
echo.
echo ========================================================================
echo   INSTALACAO COMPLETA
echo ========================================================================
echo.

echo [1/4] Verificando Python...
echo.

py --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Instale Python de: https://www.python.org/downloads/
    echo Durante a instalacao, marque "Add Python to PATH"
    echo.
    pause
    goto MENU
)

for /f "tokens=*" %%i in ('py --version') do echo [OK] %%i encontrado

echo.
echo [2/4] Instalando dependencias...
echo.

echo    Atualizando pip...
py -m pip install --upgrade pip --quiet

echo    Instalando PySide6...
py -m pip install PySide6 --quiet

echo    Instalando requests...
py -m pip install requests --quiet

echo    Instalando psutil...
py -m pip install psutil --quiet

echo    Instalando colorama...
py -m pip install colorama --quiet

echo    Instalando PyInstaller...
py -m pip install pyinstaller --quiet

echo.
echo [OK] Dependencias instaladas!
echo.

echo [3/4] Criando executavel...
echo.
echo    Isso pode levar alguns minutos, aguarde...
echo.

cd /d "%~dp0"

if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist" rmdir /s /q "dist" >nul 2>&1

py -m PyInstaller --name="GameTranslator" --onefile --windowed --noconfirm --clean --paths="%~dp0src" --hidden-import=PySide6.QtCore --hidden-import=PySide6.QtGui --hidden-import=PySide6.QtWidgets --hidden-import=sqlite3 --hidden-import=psutil --add-data "src;src" "%~dp0src\main.py"

echo.
echo [4/4] Verificando resultado...
echo.

if exist "%~dp0dist\GameTranslator.exe" (
    echo ========================================================================
    echo.
    echo   [OK] INSTALACAO CONCLUIDA COM SUCESSO!
    echo.
    echo   Executavel criado em:
    echo   %~dp0dist\GameTranslator.exe
    echo.
    echo ========================================================================
    echo.
    set /p ABRIR="Deseja abrir o programa agora? (S/N): "
    if /i "%ABRIR%"=="S" start "" "%~dp0dist\GameTranslator.exe"
) else (
    echo [ERRO] Falha ao criar executavel!
    echo Verifique os erros acima.
)

echo.
pause
cls
goto MENU

:VERIFICAR
cls
echo.
echo ========================================================================
echo   VERIFICACAO DE REQUISITOS
echo ========================================================================
echo.

:: Verifica se Python esta disponivel primeiro
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Instale Python de: https://www.python.org/downloads/
    echo Durante a instalacao, marque "Add Python to PATH"
    echo.
    pause
    goto MENU
)

:: Usa o script Python com cores para verificacao
cd /d "%~dp0src"
py verificar_sistema.py
cd /d "%~dp0"

echo.
pause
cls
goto MENU

:INSTALAR_DEPS
cls
echo.
echo ========================================================================
echo   INSTALACAO DE DEPENDENCIAS
echo ========================================================================
echo.

echo Verificando Python...
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Instale Python de: https://www.python.org/downloads/
    pause
    goto MENU
)

echo.
echo Instalando dependencias...
echo.

echo [1/5] Atualizando pip...
py -m pip install --upgrade pip

echo.
echo [2/5] Instalando PySide6...
py -m pip install PySide6

echo.
echo [3/5] Instalando requests...
py -m pip install requests

echo.
echo [4/5] Instalando psutil e colorama...
py -m pip install psutil colorama

echo.
echo [5/5] Instalando PyInstaller...
py -m pip install pyinstaller

echo.
echo ========================================================================
echo   [OK] Todas as dependencias foram instaladas!
echo ========================================================================
echo.
pause
cls
goto MENU

:CRIAR_EXE
cls
echo.
echo ========================================================================
echo   CRIACAO DO EXECUTAVEL
echo ========================================================================
echo.

echo Verificando Python...
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    pause
    goto MENU
)

echo.
echo Criando executavel (isso pode levar alguns minutos)...
echo.

cd /d "%~dp0"

if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist" rmdir /s /q "dist" >nul 2>&1

py -m PyInstaller --name="GameTranslator" --onefile --windowed --noconfirm --clean --paths="%~dp0src" --hidden-import=PySide6.QtCore --hidden-import=PySide6.QtGui --hidden-import=PySide6.QtWidgets --hidden-import=sqlite3 --hidden-import=psutil --add-data "src;src" "%~dp0src\main.py"

echo.

if exist "%~dp0dist\GameTranslator.exe" (
    echo [OK] Executavel criado com sucesso!
    echo Local: %~dp0dist\GameTranslator.exe
    echo.
    set /p ABRIR="Abrir pasta? (S/N): "
    if /i "%ABRIR%"=="S" explorer "%~dp0dist"
) else (
    echo [ERRO] Falha ao criar executavel!
)

echo.
pause
cls
goto MENU

:EXECUTAR
cls
echo.
echo ========================================================================
echo   EXECUTAR PROGRAMA
echo ========================================================================
echo.

echo Verificando Python...
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    pause
    goto MENU
)

echo.
echo Iniciando Game Translator...
echo.

cd /d "%~dp0src"
py main.py

echo.
pause
cls
goto MENU

:SAIR
echo.
echo Obrigado por usar o Game Translator!
echo.
exit /b 0
