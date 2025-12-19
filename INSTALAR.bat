@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
:: GAME TRANSLATOR - INSTALADOR E CONSTRUTOR DE EXECUTAVEL
:: Versao: 1.0.3 - Compativel com Windows 11 e Python Launcher (py)
:: ============================================================================

:: Configura codepage para UTF-8
chcp 65001 >nul 2>&1

:: Variaveis de diretorio
set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%venv"
set "DIST_DIR=%SCRIPT_DIR%dist"
set "BUILD_DIR=%SCRIPT_DIR%build"

:: Detecta comando Python (py ou python)
set "PY_CMD=py"
py --version >nul 2>&1
if errorlevel 1 (
    set "PY_CMD=python"
    python --version >nul 2>&1
    if errorlevel 1 (
        set "PY_CMD="
    )
)

:: Titulo da janela
title Game Translator - Instalador v1.0.3

:MENU_PRINCIPAL
cls
echo.
echo ========================================================================
echo.
echo     GGGG   AAA  M   M EEEEE     TTTTT RRRR   AAA  N   N  SSSS L      AAA  TTTTT  OOO  RRRR
echo    G      A   A MM MM E           T   R   R A   A NN  N S     L     A   A   T   O   O R   R
echo    G  GG AAAAA M M M EEE         T   RRRR  AAAAA N N N  SSS  L     AAAAA   T   O   O RRRR
echo    G   G A   A M   M E           T   R  R  A   A N  NN     S L     A   A   T   O   O R  R
echo     GGG  A   A M   M EEEEE       T   R   R A   A N   N SSSS  LLLLL A   A   T    OOO  R   R
echo.
echo              Sistema Profissional de Traducao para Jogos e Mods
echo                              Versao 1.0.3
echo.
echo ========================================================================
echo.
echo    [1] Instalacao Completa (Recomendado)
echo.
echo    [2] Verificar Requisitos do Sistema
echo.
echo    [3] Instalar Dependencias (pip)
echo.
echo    [4] Criar Executavel (.exe)
echo.
echo    [5] Executar Programa (modo desenvolvimento)
echo.
echo    [6] Configurar PATH do Sistema
echo.
echo    [0] Sair
echo.
echo ========================================================================
echo.

set /p "OPCAO=Digite sua opcao: "

if "%OPCAO%"=="1" goto INSTALACAO_COMPLETA
if "%OPCAO%"=="2" goto VERIFICAR_REQUISITOS
if "%OPCAO%"=="3" goto INSTALAR_DEPENDENCIAS
if "%OPCAO%"=="4" goto CRIAR_EXECUTAVEL
if "%OPCAO%"=="5" goto EXECUTAR_PROGRAMA
if "%OPCAO%"=="6" goto CONFIGURAR_PATH
if "%OPCAO%"=="0" goto SAIR

echo.
echo [AVISO] Opcao invalida! Pressione qualquer tecla para continuar...
pause >nul
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
echo Esta opcao ira:
echo   [+] Verificar se Python esta instalado
echo   [+] Instalar todas as dependencias necessarias
echo   [+] Criar o executavel (.exe)
echo   [+] Configurar atalhos
echo.
echo [AVISO] Este processo pode levar alguns minutos.
echo.
set /p "CONFIRMA=Deseja continuar? (S/N): "
if /i not "%CONFIRMA%"=="S" goto MENU_PRINCIPAL

echo.
echo ========================================================================
echo ETAPA 1/4: Verificando Python...
echo ========================================================================
call :VERIFICAR_PYTHON
if errorlevel 1 goto MENU_PRINCIPAL

echo.
echo ========================================================================
echo ETAPA 2/4: Instalando dependencias...
echo ========================================================================
call :INSTALAR_DEPS
if errorlevel 1 goto MENU_PRINCIPAL

echo.
echo ========================================================================
echo ETAPA 3/4: Criando executavel...
echo ========================================================================
call :CRIAR_EXE
if errorlevel 1 goto MENU_PRINCIPAL

echo.
echo ========================================================================
echo ETAPA 4/4: Finalizando instalacao...
echo ========================================================================
call :FINALIZAR_INSTALACAO

echo.
echo ========================================================================
echo.
echo   [OK] INSTALACAO CONCLUIDA COM SUCESSO!
echo.
echo   O executavel foi criado em:
echo   %DIST_DIR%\GameTranslator.exe
echo.
echo   Voce pode executar o programa diretamente ou criar um atalho
echo   na area de trabalho.
echo.
echo ========================================================================
echo.
set /p "ABRIR=Deseja abrir o programa agora? (S/N): "
if /i "%ABRIR%"=="S" (
    start "" "%DIST_DIR%\GameTranslator.exe"
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

set "ERROS=0"
set "AVISOS=0"

:: Verifica Sistema Operacional
echo [INFO] Sistema Operacional:
for /f "tokens=*" %%a in ('systeminfo ^| findstr /B /C:"OS Name" /C:"Nome do sistema"') do echo    %%a
echo.

:: Verifica Python (tenta py primeiro, depois python)
echo [INFO] Verificando Python...

py --version >nul 2>&1
if errorlevel 1 (
    python --version >nul 2>&1
    if errorlevel 1 (
        echo    [ERRO] Python NAO encontrado
        echo    [INFO] Instale Python de: https://www.python.org/downloads/
        set /a ERROS+=1
    ) else (
        for /f "tokens=2" %%v in ('python --version 2^>nul') do echo    [OK] Python encontrado: %%v (comando: python)
        set "PY_CMD=python"
    )
) else (
    for /f "tokens=2" %%v in ('py --version 2^>nul') do echo    [OK] Python encontrado: %%v (comando: py)
    set "PY_CMD=py"
)

:: Verifica pip
echo.
echo [INFO] Verificando pip...
%PY_CMD% -m pip --version >nul 2>&1
if errorlevel 1 (
    echo    [ERRO] pip NAO encontrado
    set /a ERROS+=1
) else (
    for /f "tokens=2" %%v in ('%PY_CMD% -m pip --version 2^>nul') do echo    [OK] pip encontrado: %%v
)

:: Verifica bibliotecas
echo.
echo [INFO] Verificando bibliotecas Python...

%PY_CMD% -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo    [AVISO] PySide6: Nao instalado
    set /a AVISOS+=1
) else (
    echo    [OK] PySide6: Instalado
)

%PY_CMD% -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo    [AVISO] requests: Nao instalado
    set /a AVISOS+=1
) else (
    echo    [OK] requests: Instalado
)

%PY_CMD% -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo    [AVISO] psutil: Nao instalado
    set /a AVISOS+=1
) else (
    echo    [OK] psutil: Instalado
)

%PY_CMD% -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo    [AVISO] PyInstaller: Nao instalado (necessario para criar .exe)
    set /a AVISOS+=1
) else (
    echo    [OK] PyInstaller: Instalado
)

:: Verifica arquivos do projeto
echo.
echo [INFO] Verificando arquivos do projeto...

if exist "%SCRIPT_DIR%src\main.py" (
    echo    [OK] src\main.py: Encontrado
) else (
    echo    [ERRO] src\main.py: NAO ENCONTRADO
    set /a ERROS+=1
)

if exist "%SCRIPT_DIR%src\database.py" (
    echo    [OK] src\database.py: Encontrado
) else (
    echo    [ERRO] src\database.py: NAO ENCONTRADO
    set /a ERROS+=1
)

if exist "%SCRIPT_DIR%src\gui\main_window.py" (
    echo    [OK] src\gui\main_window.py: Encontrado
) else (
    echo    [ERRO] src\gui\main_window.py: NAO ENCONTRADO
    set /a ERROS+=1
)

if exist "%SCRIPT_DIR%dist\GameTranslator.exe" (
    echo    [OK] dist\GameTranslator.exe: Executavel criado
) else (
    echo    [INFO] dist\GameTranslator.exe: Executavel nao criado ainda
)

:: Resumo
echo.
echo ========================================================================
echo  RESUMO DA VERIFICACAO
echo ========================================================================
echo.

if !ERROS! EQU 0 (
    if !AVISOS! EQU 0 (
        echo   [OK] SISTEMA TOTALMENTE COMPATIVEL!
        echo.
        echo   Seu sistema esta pronto para executar o Game Translator.
        echo   Execute a opcao [1] para instalacao completa.
    ) else (
        echo   [AVISO] SISTEMA COMPATIVEL COM AVISOS
        echo.
        echo   Avisos encontrados: !AVISOS!
        echo   O programa deve funcionar, mas algumas dependencias precisam ser instaladas.
        echo   Execute a opcao [3] para instalar dependencias.
    )
) else (
    echo   [ERRO] PROBLEMAS ENCONTRADOS
    echo.
    echo   Erros criticos: !ERROS!
    echo   Avisos: !AVISOS!
    echo.
    echo   Corrija os erros antes de continuar.
)

echo.
echo ========================================================================
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

call :VERIFICAR_PYTHON
if errorlevel 1 goto MENU_PRINCIPAL

echo.
echo [INFO] Atualizando pip...
%PY_CMD% -m pip install --upgrade pip

echo.
echo [INFO] Instalando dependencias do requirements.txt...
echo.

if exist "%SCRIPT_DIR%requirements.txt" (
    %PY_CMD% -m pip install -r "%SCRIPT_DIR%requirements.txt"
    if errorlevel 1 (
        echo.
        echo [ERRO] Erro ao instalar dependencias!
        pause
        goto MENU_PRINCIPAL
    )
) else (
    echo [AVISO] Arquivo requirements.txt nao encontrado. Instalando manualmente...
    %PY_CMD% -m pip install PySide6>=6.6.0
    %PY_CMD% -m pip install requests>=2.31.0
    %PY_CMD% -m pip install psutil>=5.9.0
)

echo.
echo [INFO] Instalando PyInstaller para criar executavel...
%PY_CMD% -m pip install pyinstaller

echo.
echo [OK] Todas as dependencias foram instaladas com sucesso!
echo.
pause
goto MENU_PRINCIPAL

:INSTALAR_DEPS
echo [INFO] Instalando dependencias...
%PY_CMD% -m pip install --upgrade pip >nul 2>&1
echo    [+] Instalando PySide6...
%PY_CMD% -m pip install PySide6>=6.6.0 >nul 2>&1
echo    [+] Instalando requests...
%PY_CMD% -m pip install requests>=2.31.0 >nul 2>&1
echo    [+] Instalando psutil...
%PY_CMD% -m pip install psutil>=5.9.0 >nul 2>&1
echo    [+] Instalando PyInstaller...
%PY_CMD% -m pip install pyinstaller >nul 2>&1
echo    [OK] Dependencias instaladas!
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

call :VERIFICAR_PYTHON
if errorlevel 1 goto MENU_PRINCIPAL

:: Verifica PyInstaller
echo [INFO] Verificando PyInstaller...
%PY_CMD% -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] PyInstaller nao encontrado. Instalando...
    %PY_CMD% -m pip install pyinstaller
)

echo.
echo [INFO] Criando executavel...
echo [AVISO] Este processo pode levar alguns minutos...
echo.

call :CRIAR_EXE

echo.
if exist "%DIST_DIR%\GameTranslator.exe" (
    echo [OK] Executavel criado com sucesso!
    echo.
    echo Localizacao: %DIST_DIR%\GameTranslator.exe
    echo.
    set /p "ABRIR_PASTA=Deseja abrir a pasta do executavel? (S/N): "
    if /i "!ABRIR_PASTA!"=="S" (
        explorer "%DIST_DIR%"
    )
) else (
    echo [ERRO] Erro ao criar executavel!
    echo Verifique os logs acima para mais detalhes.
)

echo.
pause
goto MENU_PRINCIPAL

:CRIAR_EXE
cd /d "%SCRIPT_DIR%"

:: Limpa builds anteriores
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%" >nul 2>&1
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%" >nul 2>&1

:: Cria diretorio de profiles se nao existir
if not exist "%SCRIPT_DIR%profiles" mkdir "%SCRIPT_DIR%profiles"

:: Cria o executavel usando py -m PyInstaller
%PY_CMD% -m PyInstaller --name="GameTranslator" ^
    --onefile ^
    --windowed ^
    --noconfirm ^
    --clean ^
    --hidden-import=PySide6.QtCore ^
    --hidden-import=PySide6.QtGui ^
    --hidden-import=PySide6.QtWidgets ^
    --hidden-import=sqlite3 ^
    --hidden-import=psutil ^
    src/main.py

if errorlevel 1 (
    echo [ERRO] Erro durante a criacao do executavel
    exit /b 1
)

:: Copia arquivos necessarios para a pasta dist
if not exist "%DIST_DIR%\profiles" mkdir "%DIST_DIR%\profiles"
if exist "%SCRIPT_DIR%profiles\*" xcopy /s /y "%SCRIPT_DIR%profiles\*" "%DIST_DIR%\profiles\" >nul 2>&1

echo [OK] Executavel criado!
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

call :VERIFICAR_PYTHON
if errorlevel 1 goto MENU_PRINCIPAL

echo [INFO] Iniciando Game Translator em modo desenvolvimento...
echo.

cd /d "%SCRIPT_DIR%src"
%PY_CMD% main.py

echo.
echo [INFO] Programa encerrado.
pause
goto MENU_PRINCIPAL

:: ============================================================================
:: CONFIGURAR PATH
:: ============================================================================
:CONFIGURAR_PATH
cls
echo.
echo ========================================================================
echo  CONFIGURAR PATH DO SISTEMA
echo ========================================================================
echo.
echo [AVISO] Esta operacao requer privilegios de administrador.
echo.
echo Esta opcao ira adicionar o diretorio do executavel ao PATH do sistema,
echo permitindo executar 'GameTranslator' diretamente do CMD.
echo.
echo Diretorio a ser adicionado:
echo    %DIST_DIR%
echo.

set /p "CONFIRMA=Deseja continuar? (S/N): "
if /i not "%CONFIRMA%"=="S" goto MENU_PRINCIPAL

:: Verifica se o executavel existe
if not exist "%DIST_DIR%\GameTranslator.exe" (
    echo.
    echo [ERRO] Executavel nao encontrado!
    echo Execute a opcao [4] primeiro para criar o executavel.
    echo.
    pause
    goto MENU_PRINCIPAL
)

:: Cria script temporario para executar como admin
echo @echo off > "%TEMP%\add_path.bat"
echo setx PATH "%%PATH%%;%DIST_DIR%" /M >> "%TEMP%\add_path.bat"
echo echo. >> "%TEMP%\add_path.bat"
echo echo PATH atualizado com sucesso! >> "%TEMP%\add_path.bat"
echo pause >> "%TEMP%\add_path.bat"

echo.
echo [INFO] Solicitando privilegios de administrador...
powershell -Command "Start-Process '%TEMP%\add_path.bat' -Verb RunAs"

echo.
echo Apos reiniciar o terminal, voce podera executar:
echo    GameTranslator
echo.
pause
goto MENU_PRINCIPAL

:: ============================================================================
:: FINALIZAR INSTALACAO
:: ============================================================================
:FINALIZAR_INSTALACAO
:: Cria atalho na area de trabalho
echo [INFO] Criando atalho na area de trabalho...

set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT=%DESKTOP%\Game Translator.lnk"

:: Usa PowerShell para criar atalho
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%DIST_DIR%\GameTranslator.exe'; $Shortcut.WorkingDirectory = '%DIST_DIR%'; $Shortcut.Description = 'Game Translator - Sistema de Traducao para Jogos'; $Shortcut.Save()" >nul 2>&1

if exist "%SHORTCUT%" (
    echo [OK] Atalho criado na area de trabalho!
) else (
    echo [AVISO] Nao foi possivel criar atalho automaticamente
)

exit /b 0

:: ============================================================================
:: FUNCOES AUXILIARES
:: ============================================================================

:VERIFICAR_PYTHON
:: Tenta py primeiro (Python Launcher do Windows)
py --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=2" %%v in ('py --version 2^>nul') do set "PYTHON_VERSION=%%v"
    set "PY_CMD=py"
    echo [OK] Python encontrado: !PYTHON_VERSION! (comando: py)
    exit /b 0
)

:: Tenta python
python --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=2" %%v in ('python --version 2^>nul') do set "PYTHON_VERSION=%%v"
    set "PY_CMD=python"
    echo [OK] Python encontrado: !PYTHON_VERSION! (comando: python)
    exit /b 0
)

:: Nenhum encontrado
echo.
echo ========================================================================
echo  [ERRO] PYTHON NAO ENCONTRADO!
echo ========================================================================
echo.
echo  O Python e necessario para executar este programa.
echo.
echo  Para instalar o Python:
echo  1. Acesse: https://www.python.org/downloads/
echo  2. Baixe a versao mais recente (3.8 ou superior)
echo  3. Durante a instalacao, marque "Add Python to PATH"
echo  4. Reinicie este instalador
echo.
echo ========================================================================
echo.
set /p "ABRIR_SITE=Deseja abrir o site de download do Python? (S/N): "
if /i "!ABRIR_SITE!"=="S" (
    start https://www.python.org/downloads/
)
echo.
pause
exit /b 1

:SAIR
cls
echo.
echo ========================================================================
echo.
echo   Obrigado por usar o Game Translator!
echo.
echo   Desenvolvido por Manus AI
echo.
echo ========================================================================
echo.
timeout /t 2 >nul
exit /b 0
