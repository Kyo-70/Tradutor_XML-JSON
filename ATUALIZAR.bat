@echo off
chcp 65001 >nul 2>&1
title Game Translator - Atualizador Simples

:MENU
cls
echo ========================================================================
echo                  GAME TRANSLATOR - ATUALIZADOR SIMPLES
echo ========================================================================
echo.
echo   [1] Atualizar Repositorio Completo (Recomendado)
echo   [2] Verificar Atualizacoes Disponiveis
echo   [3] Atualizar Apenas Dependencias Python
echo   [4] Recriar Executavel (.exe)
echo   [0] Sair
echo.
set /p OPCAO="Digite sua opcao: "
echo.

if "%OPCAO%"=="1" goto ATUALIZAR_COMPLETO
if "%OPCAO%"=="2" goto VERIFICAR_UPDATES
if "%OPCAO%"=="3" goto ATUALIZAR_DEPS
if "%OPCAO%"=="4" goto CRIAR_EXE
if "%OPCAO%"=="0" goto SAIR

echo ERRO: Opcao invalida! Tente novamente.
pause
goto MENU

:VERIFICAR_GIT
:: Função para verificar se o Git está instalado e se é um repositório
git --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Git nao encontrado!
    echo Instale o Git em: https://git-scm.com/download/win
    pause
    exit /b 1
)

if not exist ".git" (
    echo ERRO: Este diretorio nao e um repositorio Git!
    echo Para obter atualizacoes, baixe manualmente de:
    echo https://github.com/Kyo-70/Tradutor_XML-JSON
    pause
    exit /b 1
)
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

:VERIFICAR_UPDATES
cls
echo ========================================================================
echo                  VERIFICANDO ATUALIZACOES DISPONIVEIS
echo ========================================================================
echo.

call :VERIFICAR_GIT
if errorlevel 1 goto MENU

echo Buscando atualizacoes do servidor remoto...
echo.

git fetch origin
if errorlevel 1 (
    echo ERRO: Falha ao buscar atualizacoes do servidor remoto
    echo Verifique sua conexao com a internet
    pause
    goto MENU
)

echo OK: Informacoes atualizadas do servidor remoto
echo.

:: Verifica se ha commits novos
git status -uno | find "Your branch is behind" >nul
if errorlevel 0 (
    echo ATUALIZACAO DISPONIVEL!
    echo Use a opcao [1] para atualizar o repositorio completo.
) else (
    echo REPOSITORIO ATUALIZADO!
    echo Voce ja possui a versao mais recente do Game Translator.
)

echo.
pause
goto MENU

:ATUALIZAR_COMPLETO
cls
echo ========================================================================
echo                  ATUALIZACAO COMPLETA DO REPOSITORIO
echo ========================================================================
echo.

call :VERIFICAR_GIT
if errorlevel 1 goto MENU

:: Passo 1: Verifica alteracoes locais e faz stash se necessario
echo [1/3] Verificando alteracoes locais...
echo.

git diff --quiet
if errorlevel 1 (
    echo AVISO: Existem alteracoes locais nao commitadas
    echo.
    set /p CONTINUAR="Deseja continuar? Alteracoes locais serao salvas temporariamente (S/N): "
    if /i not "%CONTINUAR%"=="S" (
        echo Atualizacao cancelada.
        pause
        goto MENU
    )
    echo.
    echo Salvando alteracoes locais temporariamente...
    git stash push -m "Backup automatico antes da atualizacao"
    echo.
)

:: Passo 2: Faz o pull
echo [2/3] Aplicando atualizacoes...
echo.

git pull
if errorlevel 1 (
    echo ERRO: Falha ao aplicar atualizacoes
    echo Pode haver conflitos que precisam ser resolvidos manualmente
    pause
    goto MENU
)

echo OK: Repositorio atualizado com sucesso!
echo.

:: Passo 3: Aplica stash se houver
git stash pop --quiet 2>nul
if not errorlevel 1 (
    echo [3/3] Aplicando alteracoes locais salvas...
    echo AVISO: Conflitos podem ter ocorrido. Verifique o status do Git.
    echo.
)

echo ========================================================================
echo  ATUALIZACAO CONCLUIDA!
echo ========================================================================
echo.
pause
goto MENU

:ATUALIZAR_DEPS
cls
echo ========================================================================
echo                  ATUALIZACAO DE DEPENDENCIAS PYTHON
echo ========================================================================
echo.

echo Verificando Python...
call :VERIFICAR_PYTHON_SIMPLES
if errorlevel 1 goto MENU

echo.

echo Atualizando dependencias...
echo.

echo [1/2] Atualizando pip...
py -m pip install --upgrade pip

echo.
echo [2/2] Instalando/Atualizando dependencias do requirements.txt...
py -m pip install -r requirements.txt --upgrade

echo.
echo ========================================================================
echo  OK: Dependencias atualizadas!
echo ========================================================================
echo.
pause
goto MENU

:CRIAR_EXE
cls
echo ========================================================================
echo                  RECRIACAO DO EXECUTAVEL
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
) else (
    echo ERRO: Falha ao criar executavel!
)

echo.
pause
goto MENU

:SAIR
echo.
echo Obrigado por usar o Game Translator!
echo.
timeout /t 2 >nul
exit /b 0
