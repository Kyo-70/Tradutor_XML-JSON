@echo off
chcp 65001 >nul 2>&1
title Game Translator - Instalador v1.0.6

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
set "COLOR_DESTAQUE=%ESC%[97m%ESC%[1m"
set "COLOR_SECAO=%ESC%[94m%ESC%[1m"

cls
echo.
echo %COLOR_TITULO%========================================================================%COLOR_RESET%
echo %COLOR_TITULO%                                                                        %COLOR_RESET%
echo %COLOR_TITULO%     GAME TRANSLATOR - INSTALADOR v1.0.6                               %COLOR_RESET%
echo %COLOR_TITULO%                                                                        %COLOR_RESET%
echo %COLOR_TITULO%     Sistema Profissional de Traducao para Jogos e Mods                %COLOR_RESET%
echo %COLOR_TITULO%                                                                        %COLOR_RESET%
echo %COLOR_TITULO%========================================================================%COLOR_RESET%
echo.

:MENU
echo.
echo %COLOR_INFO%  [1]%COLOR_RESET% %COLOR_DESTAQUE%Instalacao Completa%COLOR_RESET% (Recomendado)
echo %COLOR_INFO%  [2]%COLOR_RESET% Verificar Requisitos
echo %COLOR_INFO%  [3]%COLOR_RESET% Instalar Dependencias
echo %COLOR_INFO%  [4]%COLOR_RESET% Criar Executavel (.exe)
echo %COLOR_INFO%  [5]%COLOR_RESET% Executar Programa (modo desenvolvedor)
echo %COLOR_INFO%  [0]%COLOR_RESET% Sair
echo.
set /p OPCAO="%COLOR_INFO%Digite sua opcao:%COLOR_RESET% "

if "%OPCAO%"=="1" goto INSTALACAO_COMPLETA
if "%OPCAO%"=="2" goto VERIFICAR
if "%OPCAO%"=="3" goto INSTALAR_DEPS
if "%OPCAO%"=="4" goto CRIAR_EXE
if "%OPCAO%"=="5" goto EXECUTAR
if "%OPCAO%"=="0" goto SAIR

echo.
echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Opcao invalida! Tente novamente.
echo.
pause
cls
goto MENU

:INSTALACAO_COMPLETA
cls
echo.
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo %COLOR_SECAO%  INSTALACAO COMPLETA%COLOR_RESET%
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo.

echo %COLOR_INFO%[1/4] Verificando Python...%COLOR_RESET%
echo.

py --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_ERRO%[ERRO] Python nao encontrado!%COLOR_RESET%
    echo.
    echo %COLOR_INFO%Instale Python de: https://www.python.org/downloads/%COLOR_RESET%
    echo %COLOR_INFO%Durante a instalacao, marque "Add Python to PATH"%COLOR_RESET%
    echo.
    pause
    goto MENU
)

for /f "tokens=*" %%i in ('py --version') do echo %COLOR_SUCESSO%[OK] %%i encontrado%COLOR_RESET%

echo.
echo %COLOR_INFO%[2/4] Instalando dependencias...%COLOR_RESET%
echo.

echo %COLOR_INFO%   Atualizando pip...%COLOR_RESET%
py -m pip install --upgrade pip --quiet

echo %COLOR_INFO%   Instalando PySide6...%COLOR_RESET%
py -m pip install PySide6 --quiet

echo %COLOR_INFO%   Instalando requests...%COLOR_RESET%
py -m pip install requests --quiet

echo %COLOR_INFO%   Instalando psutil...%COLOR_RESET%
py -m pip install psutil --quiet

echo %COLOR_INFO%   Instalando colorama...%COLOR_RESET%
py -m pip install colorama --quiet

echo %COLOR_INFO%   Instalando PyInstaller...%COLOR_RESET%
py -m pip install pyinstaller --quiet

echo.
echo %COLOR_SUCESSO%[OK] Dependencias instaladas!%COLOR_RESET%
echo.

echo %COLOR_INFO%[3/4] Criando executavel...%COLOR_RESET%
echo.
echo %COLOR_AVISO%   Isso pode levar alguns minutos, aguarde...%COLOR_RESET%
echo.

cd /d "%~dp0"

if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist" rmdir /s /q "dist" >nul 2>&1

py -m PyInstaller --name="GameTranslator" --onefile --windowed --noconfirm --clean --paths="%~dp0src" --hidden-import=PySide6.QtCore --hidden-import=PySide6.QtGui --hidden-import=PySide6.QtWidgets --hidden-import=sqlite3 --hidden-import=psutil --add-data "src;src" "%~dp0src\main.py"

echo.
echo %COLOR_INFO%[4/4] Verificando resultado...%COLOR_RESET%
echo.

if exist "%~dp0dist\GameTranslator.exe" (
    echo %COLOR_SUCESSO%========================================================================%COLOR_RESET%
    echo %COLOR_SUCESSO%                                                                        %COLOR_RESET%
    echo %COLOR_SUCESSO%  [OK] INSTALACAO CONCLUIDA COM SUCESSO!                              %COLOR_RESET%
    echo %COLOR_SUCESSO%                                                                        %COLOR_RESET%
    echo %COLOR_SUCESSO%  Executavel criado em:                                               %COLOR_RESET%
    echo %COLOR_SUCESSO%  %~dp0dist\GameTranslator.exe                                        %COLOR_RESET%
    echo %COLOR_SUCESSO%                                                                        %COLOR_RESET%
    echo %COLOR_SUCESSO%========================================================================%COLOR_RESET%
    echo.
    set /p ABRIR="%COLOR_INFO%Deseja abrir o programa agora? (S/N):%COLOR_RESET% "
    if /i "%ABRIR%"=="S" start "" "%~dp0dist\GameTranslator.exe"
) else (
    echo %COLOR_ERRO%[ERRO] Falha ao criar executavel!%COLOR_RESET%
    echo %COLOR_AVISO%Verifique os erros acima.%COLOR_RESET%
)

echo.
pause
cls
goto MENU

:VERIFICAR
cls
echo.
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo %COLOR_SECAO%  VERIFICACAO DE REQUISITOS%COLOR_RESET%
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo.

:: Verifica se Python esta disponivel primeiro
py --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_ERRO%[ERRO] Python nao encontrado!%COLOR_RESET%
    echo.
    echo %COLOR_INFO%Instale Python de: https://www.python.org/downloads/%COLOR_RESET%
    echo %COLOR_INFO%Durante a instalacao, marque "Add Python to PATH"%COLOR_RESET%
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
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo %COLOR_SECAO%  INSTALACAO DE DEPENDENCIAS%COLOR_RESET%
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo.

echo %COLOR_INFO%Verificando Python...%COLOR_RESET%
py --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_ERRO%[ERRO] Python nao encontrado!%COLOR_RESET%
    echo %COLOR_INFO%Instale Python de: https://www.python.org/downloads/%COLOR_RESET%
    pause
    goto MENU
)

echo.
echo %COLOR_INFO%Instalando dependencias...%COLOR_RESET%
echo.

echo %COLOR_INFO%[1/5] Atualizando pip...%COLOR_RESET%
py -m pip install --upgrade pip

echo.
echo %COLOR_INFO%[2/5] Instalando PySide6...%COLOR_RESET%
py -m pip install PySide6

echo.
echo %COLOR_INFO%[3/5] Instalando requests...%COLOR_RESET%
py -m pip install requests

echo.
echo %COLOR_INFO%[4/5] Instalando psutil e colorama...%COLOR_RESET%
py -m pip install psutil colorama

echo.
echo %COLOR_INFO%[5/5] Instalando PyInstaller...%COLOR_RESET%
py -m pip install pyinstaller

echo.
echo %COLOR_SUCESSO%========================================================================%COLOR_RESET%
echo %COLOR_SUCESSO%  [OK] Todas as dependencias foram instaladas!%COLOR_RESET%
echo %COLOR_SUCESSO%========================================================================%COLOR_RESET%
echo.
pause
cls
goto MENU

:CRIAR_EXE
cls
echo.
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo %COLOR_SECAO%  CRIACAO DO EXECUTAVEL%COLOR_RESET%
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo.

echo %COLOR_INFO%Verificando Python...%COLOR_RESET%
py --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_ERRO%[ERRO] Python nao encontrado!%COLOR_RESET%
    pause
    goto MENU
)

echo.
echo %COLOR_INFO%Criando executavel (isso pode levar alguns minutos)...%COLOR_RESET%
echo.

cd /d "%~dp0"

if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist" rmdir /s /q "dist" >nul 2>&1

py -m PyInstaller --name="GameTranslator" --onefile --windowed --noconfirm --clean --paths="%~dp0src" --hidden-import=PySide6.QtCore --hidden-import=PySide6.QtGui --hidden-import=PySide6.QtWidgets --hidden-import=sqlite3 --hidden-import=psutil --add-data "src;src" "%~dp0src\main.py"

echo.

if exist "%~dp0dist\GameTranslator.exe" (
    echo %COLOR_SUCESSO%[OK] Executavel criado com sucesso!%COLOR_RESET%
    echo %COLOR_INFO%Local: %~dp0dist\GameTranslator.exe%COLOR_RESET%
    echo.
    set /p ABRIR="%COLOR_INFO%Abrir pasta? (S/N):%COLOR_RESET% "
    if /i "%ABRIR%"=="S" explorer "%~dp0dist"
) else (
    echo %COLOR_ERRO%[ERRO] Falha ao criar executavel!%COLOR_RESET%
)

echo.
pause
cls
goto MENU

:EXECUTAR
cls
echo.
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo %COLOR_SECAO%  EXECUTAR PROGRAMA%COLOR_RESET%
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo.

echo %COLOR_INFO%Verificando Python...%COLOR_RESET%
py --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_ERRO%[ERRO] Python nao encontrado!%COLOR_RESET%
    pause
    goto MENU
)

echo.
echo %COLOR_INFO%Iniciando Game Translator...%COLOR_RESET%
echo.

cd /d "%~dp0src"
py main.py

echo.
pause
cls
goto MENU

:SAIR
echo.
echo %COLOR_DESTAQUE%Obrigado por usar o Game Translator!%COLOR_RESET%
echo.
timeout /t 2 >nul
exit /b 0
