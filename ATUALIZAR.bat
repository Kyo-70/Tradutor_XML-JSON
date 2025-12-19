@echo off
chcp 65001 >nul 2>&1
title Game Translator - Atualizador v1.0.1

:: Habilita suporte a cores ANSI no Windows 10+ via registro
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1

:: Define cores customizadas usando ANSI escape codes
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do set "ESC=%%b"

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
echo %COLOR_TITULO%     GAME TRANSLATOR - ATUALIZADOR v1.0.1                              %COLOR_RESET%
echo %COLOR_TITULO%                                                                        %COLOR_RESET%
echo %COLOR_TITULO%     Sistema de Atualizacao Automatica do Repositorio                  %COLOR_RESET%
echo %COLOR_TITULO%                                                                        %COLOR_RESET%
echo %COLOR_TITULO%========================================================================%COLOR_RESET%
echo.

:MENU
echo.
echo %COLOR_INFO%  [1]%COLOR_RESET% %COLOR_DESTAQUE%Atualizar Repositorio Completo%COLOR_RESET% (Recomendado)
echo %COLOR_INFO%  [2]%COLOR_RESET% Verificar Atualizacoes Disponiveis
echo %COLOR_INFO%  [3]%COLOR_RESET% Atualizar Apenas Dependencias Python
echo %COLOR_INFO%  [4]%COLOR_RESET% Recriar Executavel (.exe)
echo %COLOR_INFO%  [5]%COLOR_RESET% Verificar Estado do Repositorio
echo %COLOR_INFO%  [6]%COLOR_RESET% Verificar Sistema e Dependencias
echo %COLOR_INFO%  [0]%COLOR_RESET% Sair
echo.
set /p OPCAO="%COLOR_INFO%Digite sua opcao:%COLOR_RESET% "

if "%OPCAO%"=="1" goto ATUALIZAR_COMPLETO
if "%OPCAO%"=="2" goto VERIFICAR_UPDATES
if "%OPCAO%"=="3" goto ATUALIZAR_DEPS
if "%OPCAO%"=="4" goto CRIAR_EXE
if "%OPCAO%"=="5" goto VERIFICAR_REPO
if "%OPCAO%"=="6" goto VERIFICAR_SISTEMA
if "%OPCAO%"=="0" goto SAIR

echo.
echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Opcao invalida! Tente novamente.
echo.
pause
cls
goto MENU

:VERIFICAR_REPO
cls
echo.
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo %COLOR_SECAO%  VERIFICANDO ESTADO DO REPOSITORIO%COLOR_RESET%
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo.

:: Verifica se git esta instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Git nao encontrado!
    echo.
    echo %COLOR_INFO%Instale o Git em:%COLOR_RESET% https://git-scm.com/download/win
    echo.
    pause
    cls
    goto MENU
)

echo %COLOR_SUCESSO%[OK]%COLOR_RESET% Git encontrado
echo.

:: Verifica se e um repositorio git
if not exist ".git" (
    echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Este diretorio nao e um repositorio Git!
    echo.
    echo %COLOR_INFO%Para obter atualizacoes, baixe manualmente de:%COLOR_RESET%
    echo %COLOR_DESTAQUE%https://github.com/Kyo-70/game-translator%COLOR_RESET%
    echo.
    pause
    cls
    goto MENU
)

echo %COLOR_SECAO%[Estado Atual]%COLOR_RESET%
echo.
git status
echo.

echo %COLOR_SECAO%[Branch Atual]%COLOR_RESET%
echo.
git symbolic-ref --short HEAD 2>nul || echo Detached HEAD
echo.

echo %COLOR_SECAO%[Ultimo Commit]%COLOR_RESET%
echo.
git log -1 --pretty=format:"%COLOR_INFO%Commit:%COLOR_RESET% %%h%COLOR_INFO% | Data:%COLOR_RESET% %%ad%COLOR_INFO% | Autor:%COLOR_RESET% %%an%COLOR_INFO% | Mensagem:%COLOR_RESET% %%s" --date=short
echo.
echo.

pause
cls
goto MENU

:VERIFICAR_UPDATES
cls
echo.
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo %COLOR_SECAO%  VERIFICANDO ATUALIZACOES DISPONIVEIS%COLOR_RESET%
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo.

:: Verifica se git esta instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Git nao encontrado!
    echo.
    echo %COLOR_INFO%Instale o Git em:%COLOR_RESET% https://git-scm.com/download/win
    echo.
    pause
    cls
    goto MENU
)

:: Verifica se e um repositorio git
if not exist ".git" (
    echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Este diretorio nao e um repositorio Git!
    echo.
    pause
    cls
    goto MENU
)

echo %COLOR_INFO%Buscando atualizacoes do servidor remoto...%COLOR_RESET%
echo.

git fetch origin
if errorlevel 1 (
    echo.
    echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Falha ao buscar atualizacoes do servidor remoto
    echo %COLOR_AVISO%Verifique sua conexao com a internet%COLOR_RESET%
    echo.
    pause
    cls
    goto MENU
)

echo %COLOR_SUCESSO%[OK]%COLOR_RESET% Informacoes atualizadas do servidor remoto
echo.

:: Verifica se ha commits novos - obtém a branch atual primeiro
:: Usa symbolic-ref para compatibilidade com Git mais antigo
for /f "tokens=*" %%i in ('git symbolic-ref --short HEAD 2^>nul') do set BRANCH_ATUAL=%%i

:: Se não conseguiu obter a branch atual, tenta main/master
if "%BRANCH_ATUAL%"=="" (
    set "BRANCH_ATUAL=main"
)

:: Verifica se o remote branch existe antes de comparar
git rev-parse --verify origin/%BRANCH_ATUAL% >nul 2>&1
if errorlevel 1 (
    :: Branch remota não existe, tenta master
    set "BRANCH_ATUAL=master"
    git rev-parse --verify origin/%BRANCH_ATUAL% >nul 2>&1
    if errorlevel 1 (
        echo %COLOR_AVISO%[AVISO]%COLOR_RESET% Nao foi possivel determinar a branch remota
        echo.
        pause
        cls
        goto MENU
    )
)

:: Verifica se ha commits pendentes na branch atual
for /f %%i in ('git rev-list HEAD...origin/%BRANCH_ATUAL% --count 2^>nul') do set COMMITS_PENDENTES=%%i

if "%COMMITS_PENDENTES%"=="0" (
    echo %COLOR_SUCESSO%========================================================================%COLOR_RESET%
    echo %COLOR_SUCESSO%  [OK] REPOSITORIO ATUALIZADO!%COLOR_RESET%
    echo %COLOR_SUCESSO%========================================================================%COLOR_RESET%
    echo.
    echo %COLOR_INFO%Voce ja possui a versao mais recente do Game Translator.%COLOR_RESET%
) else (
    echo %COLOR_AVISO%========================================================================%COLOR_RESET%
    echo %COLOR_AVISO%  [!] ATUALIZACAO DISPONIVEL!%COLOR_RESET%
    echo %COLOR_AVISO%========================================================================%COLOR_RESET%
    echo.
    echo %COLOR_DESTAQUE%Commits pendentes:%COLOR_RESET% %COMMITS_PENDENTES%
    echo.
    echo %COLOR_INFO%Use a opcao [1] para atualizar o repositorio completo.%COLOR_RESET%
)

echo.
pause
cls
goto MENU

:ATUALIZAR_COMPLETO
cls
echo.
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo %COLOR_SECAO%  ATUALIZACAO COMPLETA DO REPOSITORIO%COLOR_RESET%
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo.

:: Verifica se git esta instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Git nao encontrado!
    echo.
    echo %COLOR_INFO%Instale o Git em:%COLOR_RESET% https://git-scm.com/download/win
    echo.
    pause
    cls
    goto MENU
)

echo %COLOR_SUCESSO%[OK]%COLOR_RESET% Git encontrado
echo.

:: Verifica se e um repositorio git
if not exist ".git" (
    echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Este diretorio nao e um repositorio Git!
    echo.
    echo %COLOR_INFO%Para obter atualizacoes, baixe manualmente de:%COLOR_RESET%
    echo %COLOR_DESTAQUE%https://github.com/Kyo-70/game-translator%COLOR_RESET%
    echo.
    pause
    cls
    goto MENU
)

echo %COLOR_SUCESSO%[OK]%COLOR_RESET% Repositorio Git encontrado
echo.

:: Passo 1: Verifica alteracoes locais
echo %COLOR_INFO%[1/5]%COLOR_RESET% Verificando alteracoes locais...
echo.

git diff --quiet
if errorlevel 1 (
    echo %COLOR_AVISO%[AVISO]%COLOR_RESET% Existem alteracoes locais nao commitadas
    echo.
    set /p CONTINUAR="%COLOR_AVISO%Deseja continuar? Alteracoes locais podem ser sobrescritas (S/N):%COLOR_RESET% "
    if /i not "%CONTINUAR%"=="S" (
        echo.
        echo %COLOR_INFO%Atualizacao cancelada.%COLOR_RESET%
        echo.
        pause
        cls
        goto MENU
    )
    echo.
    echo %COLOR_INFO%Salvando alteracoes locais temporariamente...%COLOR_RESET%
    git stash push -m "Backup automatico antes da atualizacao"
    echo.
)

:: Passo 2: Busca atualizacoes
echo %COLOR_INFO%[2/5]%COLOR_RESET% Buscando atualizacoes do servidor remoto...
echo.

git fetch origin
if errorlevel 1 (
    echo.
    echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Falha ao buscar atualizacoes
    echo %COLOR_AVISO%Verifique sua conexao com a internet%COLOR_RESET%
    echo.
    pause
    cls
    goto MENU
)

echo %COLOR_SUCESSO%[OK]%COLOR_RESET% Atualizacoes obtidas do servidor
echo.

:: Passo 3: Faz o pull - obtém a branch atual primeiro
:: Usa symbolic-ref para compatibilidade com Git mais antigo
for /f "tokens=*" %%i in ('git symbolic-ref --short HEAD 2^>nul') do set BRANCH_PULL=%%i

:: Se não conseguiu obter a branch (detached HEAD), avisa e cancela
if "%BRANCH_PULL%"=="" (
    echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Estado detached HEAD detectado
    echo %COLOR_AVISO%Nao e possivel atualizar em estado detached HEAD%COLOR_RESET%
    echo %COLOR_INFO%Faca checkout em uma branch primeiro: git checkout main%COLOR_RESET%
    echo.
    pause
    cls
    goto MENU
)

echo %COLOR_INFO%[3/5]%COLOR_RESET% Aplicando atualizacoes...
echo.

git pull origin "%BRANCH_PULL%"
if errorlevel 1 (
    echo.
    echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Falha ao aplicar atualizacoes
    echo %COLOR_AVISO%Pode haver conflitos que precisam ser resolvidos manualmente%COLOR_RESET%
    echo.
    pause
    cls
    goto MENU
)

echo %COLOR_SUCESSO%[OK]%COLOR_RESET% Repositorio atualizado
echo.

:: Passo 4: Atualiza dependencias
echo %COLOR_INFO%[4/5]%COLOR_RESET% Verificando dependencias Python...
echo.

py --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_AVISO%[AVISO]%COLOR_RESET% Python nao encontrado, pulando atualizacao de dependencias
    echo %COLOR_INFO%Instale Python em: https://www.python.org/downloads/%COLOR_RESET%
    echo.
) else (
    echo %COLOR_SUCESSO%[OK]%COLOR_RESET% Python encontrado
    echo.
    echo %COLOR_INFO%Atualizando dependencias...%COLOR_RESET%
    echo.
    
    py -m pip install --upgrade pip --quiet
    py -m pip install -r requirements.txt --upgrade --quiet
    
    if errorlevel 1 (
        echo %COLOR_AVISO%[AVISO]%COLOR_RESET% Algumas dependencias podem nao ter sido atualizadas
        echo.
    ) else (
        echo %COLOR_SUCESSO%[OK]%COLOR_RESET% Dependencias atualizadas
        echo.
    )
)

:: Passo 5: Verifica sistema
echo %COLOR_INFO%[5/5]%COLOR_RESET% Verificando sistema...
echo.

py --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_AVISO%[AVISO]%COLOR_RESET% Pulando verificacao do sistema (Python nao encontrado)
    echo.
) else (
    cd /d "%~dp0src"
    :: Verifica sistema apos atualizacao
    py verificar_sistema.py
    cd /d "%~dp0"
)

:: Resumo final
echo %COLOR_SUCESSO%========================================================================%COLOR_RESET%
echo %COLOR_SUCESSO%                                                                        %COLOR_RESET%
echo %COLOR_SUCESSO%  [OK] ATUALIZACAO CONCLUIDA COM SUCESSO!                              %COLOR_RESET%
echo %COLOR_SUCESSO%                                                                        %COLOR_RESET%
echo %COLOR_SUCESSO%========================================================================%COLOR_RESET%
echo.
echo %COLOR_INFO%O Game Translator foi atualizado para a versao mais recente.%COLOR_RESET%
echo.

:: Pergunta se deseja recriar o executavel
set /p RECRIAR="%COLOR_INFO%Deseja recriar o executavel agora? (S/N):%COLOR_RESET% "
if /i "%RECRIAR%"=="S" goto DO_REBUILD
if /i "%RECRIAR%"=="Y" goto DO_REBUILD
echo %COLOR_INFO%Execute EXECUTAR.bat para iniciar o programa em modo desenvolvedor.%COLOR_RESET%
echo %COLOR_INFO%Ou use a opcao [4] do menu para criar o executavel.%COLOR_RESET%
echo.
goto END_UPDATE

:DO_REBUILD
echo.
echo %COLOR_INFO%Recriando executavel...%COLOR_RESET%
echo.

call :BUILD_EXECUTAVEL

if exist "%~dp0dist\GameTranslator.exe" (
    echo.
    echo %COLOR_SUCESSO%[OK] Executavel recriado com sucesso!%COLOR_RESET%
    echo %COLOR_INFO%Local:%COLOR_RESET% %~dp0dist\GameTranslator.exe
) else (
    echo.
    echo %COLOR_ERRO%[ERRO] Falha ao recriar executavel!%COLOR_RESET%
    echo %COLOR_AVISO%Use a opcao [4] do menu para tentar novamente.%COLOR_RESET%
)
echo.

:END_UPDATE

pause
cls
goto MENU

:ATUALIZAR_DEPS
cls
echo.
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo %COLOR_SECAO%  ATUALIZANDO DEPENDENCIAS PYTHON%COLOR_RESET%
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo.

:: Verifica se Python esta disponivel
py --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Python nao encontrado!
    echo.
    echo %COLOR_INFO%Instale Python em:%COLOR_RESET% https://www.python.org/downloads/
    echo %COLOR_INFO%Durante a instalacao, marque "Add Python to PATH"%COLOR_RESET%
    echo.
    pause
    cls
    goto MENU
)

echo %COLOR_SUCESSO%[OK]%COLOR_RESET% Python encontrado
echo.

echo %COLOR_INFO%Atualizando pip...%COLOR_RESET%
echo.
py -m pip install --upgrade pip

echo.
echo %COLOR_INFO%Atualizando dependencias do requirements.txt...%COLOR_RESET%
echo.

if exist "requirements.txt" (
    py -m pip install -r requirements.txt --upgrade
    echo.
    echo %COLOR_SUCESSO%========================================================================%COLOR_RESET%
    echo %COLOR_SUCESSO%  [OK] DEPENDENCIAS ATUALIZADAS!%COLOR_RESET%
    echo %COLOR_SUCESSO%========================================================================%COLOR_RESET%
) else (
    echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Arquivo requirements.txt nao encontrado!
    echo.
)

echo.
pause
cls
goto MENU

:VERIFICAR_SISTEMA
cls
echo.
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo %COLOR_SECAO%  VERIFICACAO DO SISTEMA%COLOR_RESET%
echo %COLOR_SECAO%========================================================================%COLOR_RESET%
echo.

:: Verifica se Python esta disponivel
py --version >nul 2>&1
if errorlevel 1 (
    echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Python nao encontrado!
    echo.
    echo %COLOR_INFO%Instale Python em:%COLOR_RESET% https://www.python.org/downloads/
    echo %COLOR_INFO%Durante a instalacao, marque "Add Python to PATH"%COLOR_RESET%
    echo.
    pause
    cls
    goto MENU
)

:: Usa o script Python com cores para verificacao
cd /d "%~dp0src"
py verificar_sistema.py --auto-instalar
cd /d "%~dp0"

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
    echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Python nao encontrado!
    echo.
    echo %COLOR_INFO%Instale Python em:%COLOR_RESET% https://www.python.org/downloads/
    echo.
    pause
    cls
    goto MENU
)

echo %COLOR_SUCESSO%[OK]%COLOR_RESET% Python encontrado
echo.

echo %COLOR_INFO%Verificando PyInstaller...%COLOR_RESET%
py -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo %COLOR_AVISO%[AVISO]%COLOR_RESET% PyInstaller nao encontrado, instalando...
    echo.
    py -m pip install pyinstaller --quiet
    if errorlevel 1 (
        echo %COLOR_ERRO%[ERRO]%COLOR_RESET% Falha ao instalar PyInstaller!
        echo.
        pause
        cls
        goto MENU
    )
)

echo %COLOR_SUCESSO%[OK]%COLOR_RESET% PyInstaller disponivel
echo.

call :BUILD_EXECUTAVEL

if exist "%~dp0dist\GameTranslator.exe" (
    echo %COLOR_SUCESSO%========================================================================%COLOR_RESET%
    echo %COLOR_SUCESSO%  [OK] EXECUTAVEL CRIADO COM SUCESSO!%COLOR_RESET%
    echo %COLOR_SUCESSO%========================================================================%COLOR_RESET%
    echo.
    echo %COLOR_INFO%Local:%COLOR_RESET% %~dp0dist\GameTranslator.exe
    echo.
    set /p ABRIR="%COLOR_INFO%Abrir pasta? (S/N):%COLOR_RESET% "
    if /i "%ABRIR%"=="S" explorer "%~dp0dist"
    if /i "%ABRIR%"=="Y" explorer "%~dp0dist"
) else (
    echo %COLOR_ERRO%========================================================================%COLOR_RESET%
    echo %COLOR_ERRO%  [ERRO] FALHA AO CRIAR EXECUTAVEL!%COLOR_RESET%
    echo %COLOR_ERRO%========================================================================%COLOR_RESET%
    echo.
    echo %COLOR_AVISO%Verifique os erros acima.%COLOR_RESET%
)

echo.
pause
cls
goto MENU

:BUILD_EXECUTAVEL
:: Funcao compartilhada para criar o executavel
echo %COLOR_INFO%Criando executavel (isso pode levar alguns minutos)...%COLOR_RESET%
echo %COLOR_AVISO%Aguarde, nao feche esta janela...%COLOR_RESET%
echo.

cd /d "%~dp0"

if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist" rmdir /s /q "dist" >nul 2>&1

py -m PyInstaller --name="GameTranslator" --onefile --windowed --noconfirm --clean --paths="%~dp0src" --hidden-import=PySide6.QtCore --hidden-import=PySide6.QtGui --hidden-import=PySide6.QtWidgets --hidden-import=sqlite3 --hidden-import=psutil --add-data "src;src" "%~dp0src\main.py"

echo.
exit /b %ERRORLEVEL%

:SAIR
echo.
echo %COLOR_DESTAQUE%Obrigado por usar o Game Translator!%COLOR_RESET%
echo.
timeout /t 2 >nul
exit /b 0
