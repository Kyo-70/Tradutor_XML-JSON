@echo off
chcp 65001 >nul 2>&1
title Game Translator - Instalador Simples

:MENU
cls
echo ========================================================================
echo                  GAME TRANSLATOR - INSTALADOR SIMPLES
echo ========================================================================
echo.
echo   [1] Instalacao Completa (Recomendado)
echo   [2] Verificar Requisitos
echo   [3] Instalar Dependencias
echo   [4] Criar Executavel (.exe)
echo   [5] Executar Programa (modo desenvolvedor)
echo   [0] Sair
echo.
set /p OPCAO="Digite sua opcao: "
echo.

if "%OPCAO%"=="1" goto INSTALACAO_COMPLETA
if "%OPCAO%"=="2" goto VERIFICAR
if "%OPCAO%"=="3" goto INSTALAR_DEPS
if "%OPCAO%"=="4" goto CRIAR_EXE
if "%OPCAO%"=="5" goto EXECUTAR
if "%OPCAO%"=="0" goto SAIR

echo ERRO: Opcao invalida! Tente novamente.
pause
goto MENU

:INSTALACAO_COMPLETA
cls
echo ========================================================================
echo                  INSTALACAO COMPLETA
echo ========================================================================
echo.

echo [1/4] Verificando Python...
call :VERIFICAR_PYTHON
if errorlevel 1 goto MENU
echo.

echo [2/4] Instalando dependencias...
echo   Atualizando pip...
py -m pip install --upgrade pip --quiet
echo   Instalando dependencias do requirements.txt...
py -m pip install -r requirements.txt --quiet
echo   Instalando PyInstaller...
py -m pip install pyinstaller --quiet
echo OK: Dependencias instaladas!
echo.

echo [3/4] Criando executavel...
echo   Isso pode levar alguns minutos, aguarde...
echo.

:: Limpa builds anteriores
if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist" rmdir /s /q "dist" >nul 2>&1

:: Comando PyInstaller completo em uma única linha
py -m PyInstaller --name="GameTranslator" --onefile --windowed --noconfirm --clean --paths="%~dp0src" --hidden-import=PySide6.QtCore --hidden-import=PySide6.QtGui --hidden-import=PySide6.QtWidgets --hidden-import=sqlite3 --hidden-import=psutil --add-data "src;src" "%~dp0src\main.py"
if errorlevel 1 (
    echo ERRO: Falha ao criar executavel!
    echo Verifique os erros acima.
    pause
    goto MENU
)

echo.
echo [4/4] Verificando resultado...
echo.

if exist "%~dp0dist\GameTranslator.exe" (
    echo ========================================================================
    echo  INSTALACAO CONCLUIDA COM SUCESSO!
    echo  Executavel criado em:
    echo  %~dp0dist\GameTranslator.exe
    echo ========================================================================
    echo.
    set /p ABRIR="Deseja abrir o programa agora? (S/N): "
    if /i "%ABRIR%"=="S" start "" "%~dp0dist\GameTranslator.exe"
    if /i "%ABRIR%"=="Y" start "" "%~dp0dist\GameTranslator.exe"
) else (
    echo ERRO: Falha ao criar executavel!
    echo Verifique os erros acima.
)

echo.
pause
goto MENU

:VERIFICAR
cls
echo ========================================================================
echo                  VERIFICACAO DE REQUISITOS
echo ========================================================================
echo.

echo Verificando Python...
call :VERIFICAR_PYTHON_SIMPLES
if errorlevel 1 goto MENU

echo.

echo Executando script de verificacao...
cd /d "%~dp0src"
py verificar_sistema.py
cd /d "%~dp0"

echo.
pause
goto MENU

:INSTALAR_DEPS
cls
echo ========================================================================
echo                  INSTALACAO DE DEPENDENCIAS
echo ========================================================================
echo.

echo Verificando Python...
call :VERIFICAR_PYTHON_SIMPLES
if errorlevel 1 goto MENU

echo.

echo Instalando dependencias...
echo.

echo [1/3] Atualizando pip...
py -m pip install --upgrade pip

echo.
echo [2/3] Instalando dependencias do requirements.txt...
py -m pip install -r requirements.txt

echo.
echo [3/3] Instalando PyInstaller...
py -m pip install pyinstaller

echo.
echo ========================================================================
echo  OK: Todas as dependencias foram instaladas!
echo ========================================================================
echo.
pause
goto MENU

:CRIAR_EXE
cls
echo ========================================================================
echo                  CRIACAO DO EXECUTAVEL
echo ========================================================================
echo.

echo Verificando Python...
call :VERIFICAR_PYTHON_SIMPLES
if errorlevel 1 goto MENU

echo.

echo Verificando PyInstaller...
where pyinstaller >nul 2>&1
if errorlevel 1 (
    echo AVISO: PyInstaller nao encontrado. Instalando...
    py -m pip install pyinstaller
    if errorlevel 1 (
        echo ERRO: Falha ao instalar PyInstaller.
        pause
        goto MENU
    )
)
echo OK: PyInstaller encontrado.
echo.

echo Criando executavel (isso pode levar alguns minutos)...
echo.

:: Limpa builds anteriores
if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist" rmdir /s /q "dist" >nul 2>&1

:: Comando PyInstaller completo em uma única linha
py -m PyInstaller --name="GameTranslator" --onefile --windowed --noconfirm --clean --paths="%~dp0src" --hidden-import=PySide6.QtCore --hidden-import=PySide6.QtGui --hidden-import=PySide6.QtWidgets --hidden-import=sqlite3 --hidden-import=psutil --add-data "src;src" "%~dp0src\main.py"
if errorlevel 1 (
    echo ERRO: Falha ao criar executavel!
    pause
    goto MENU
)

echo.

if exist "%~dp0dist\GameTranslator.exe" (
    echo OK: Executavel criado com sucesso!
    echo Local: %~dp0dist\GameTranslator.exe
    echo.
    set /p ABRIR="Abrir pasta? (S/N): "
    if /i "%ABRIR%"=="S" explorer "%~dp0dist"
    if /i "%ABRIR%"=="Y" explorer "%~dp0dist"
) else (
    echo ERRO: Falha ao criar executavel!
)

echo.
pause
goto MENU

:EXECUTAR
cls
echo ========================================================================
echo                  EXECUTAR PROGRAMA
echo ========================================================================
echo.

echo Verificando Python...
call :VERIFICAR_PYTHON_SIMPLES
if errorlevel 1 goto MENU

echo.

echo Iniciando Game Translator...
echo.

cd /d "%~dp0src"
py main.py

echo.
pause
goto MENU

:VERIFICAR_PYTHON
:: Verifica se o Python está no PATH. Se não estiver, exibe mensagem e retorna erro.
where py >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python de: https://www.python.org/downloads/
    echo Durante a instalacao, marque "Add Python to PATH"
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('py --version 2^>nul') do echo OK: %%i encontrado
exit /b 0

:VERIFICAR_PYTHON_SIMPLES
:: Verifica se o Python está no PATH. Se não estiver, exibe mensagem e retorna erro.
where py >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python de: https://www.python.org/downloads/
    echo Durante a instalacao, marque "Add Python to PATH"
    pause
    exit /b 1
)
echo OK: Python encontrado.
exit /b 0

:SAIR
echo.
echo Obrigado por usar o Game Translator!
echo.
timeout /t 2 >nul
exit /b 0
