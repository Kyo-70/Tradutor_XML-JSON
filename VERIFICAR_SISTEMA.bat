@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
:: GAME TRANSLATOR - VERIFICACAO COMPLETA DO SISTEMA
:: Versao: 1.0.3 - Compativel com Windows 11 e Python Launcher (py)
:: ============================================================================

chcp 65001 >nul 2>&1
title Game Translator - Verificacao do Sistema

cls
echo.
echo ========================================================================
echo  GAME TRANSLATOR - VERIFICACAO COMPLETA DO SISTEMA
echo ========================================================================
echo.

set "ERROS=0"
set "AVISOS=0"
set "SCRIPT_DIR=%~dp0"
set "PY_CMD="

:: ============================================================================
:: DETECTAR COMANDO PYTHON
:: ============================================================================
echo ------------------------------------------------------------------------
echo  DETECTANDO PYTHON
echo ------------------------------------------------------------------------
echo.

:: Tenta py primeiro (Python Launcher do Windows - mais recente)
py --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=2" %%v in ('py --version 2^>nul') do (
        echo    [OK] Python Launcher encontrado: %%v
        echo    [INFO] Usando comando: py
    )
    set "PY_CMD=py"
    goto :PYTHON_FOUND
)

:: Tenta python
python --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=2" %%v in ('python --version 2^>nul') do (
        echo    [OK] Python encontrado: %%v
        echo    [INFO] Usando comando: python
    )
    set "PY_CMD=python"
    goto :PYTHON_FOUND
)

:: Nenhum encontrado
echo    [ERRO] Python NAO INSTALADO
echo.
echo    Para instalar:
echo    1. Acesse: https://www.python.org/downloads/
echo    2. Baixe a versao mais recente
echo    3. Durante instalacao, marque "Add Python to PATH"
echo.
set /a ERROS+=1
set /p "ABRIR=Deseja abrir o site de download? (S/N): "
if /i "!ABRIR!"=="S" start https://www.python.org/downloads/
goto :RESUMO

:PYTHON_FOUND
echo.

:: ============================================================================
:: VERIFICACAO DO SISTEMA OPERACIONAL
:: ============================================================================
echo ------------------------------------------------------------------------
echo  SISTEMA OPERACIONAL
echo ------------------------------------------------------------------------
echo.

for /f "tokens=*" %%a in ('systeminfo ^| findstr /B /C:"OS Name" /C:"Nome do sistema"') do (
    echo    %%a
)
for /f "tokens=*" %%a in ('systeminfo ^| findstr /B /C:"OS Version" /C:"Versao do sistema"') do (
    echo    %%a
)
echo.

:: ============================================================================
:: VERIFICACAO DO PIP
:: ============================================================================
echo ------------------------------------------------------------------------
echo  PIP (Gerenciador de Pacotes)
echo ------------------------------------------------------------------------
echo.

%PY_CMD% -m pip --version >nul 2>&1
if errorlevel 1 (
    echo    [ERRO] pip NAO INSTALADO
    echo    [INFO] Tentando instalar pip...
    %PY_CMD% -m ensurepip --upgrade >nul 2>&1
    %PY_CMD% -m pip --version >nul 2>&1
    if errorlevel 1 (
        set /a ERROS+=1
    ) else (
        echo    [OK] pip instalado com sucesso!
    )
) else (
    for /f "tokens=2" %%v in ('%PY_CMD% -m pip --version 2^>nul') do (
        echo    [OK] pip encontrado: %%v
    )
)
echo.

:: ============================================================================
:: VERIFICACAO DAS BIBLIOTECAS
:: ============================================================================
echo ------------------------------------------------------------------------
echo  BIBLIOTECAS PYTHON
echo ------------------------------------------------------------------------
echo.

:: PySide6
%PY_CMD% -c "import PySide6; print(PySide6.__version__)" >nul 2>&1
if errorlevel 1 (
    echo    [AVISO] PySide6: Nao instalado
    set /a AVISOS+=1
    set "NEED_PYSIDE=1"
) else (
    for /f %%v in ('%PY_CMD% -c "import PySide6; print(PySide6.__version__)" 2^>nul') do (
        echo    [OK] PySide6: %%v
    )
)

:: requests
%PY_CMD% -c "import requests; print(requests.__version__)" >nul 2>&1
if errorlevel 1 (
    echo    [AVISO] requests: Nao instalado
    set /a AVISOS+=1
    set "NEED_REQUESTS=1"
) else (
    for /f %%v in ('%PY_CMD% -c "import requests; print(requests.__version__)" 2^>nul') do (
        echo    [OK] requests: %%v
    )
)

:: psutil
%PY_CMD% -c "import psutil; print(psutil.__version__)" >nul 2>&1
if errorlevel 1 (
    echo    [AVISO] psutil: Nao instalado
    set /a AVISOS+=1
    set "NEED_PSUTIL=1"
) else (
    for /f %%v in ('%PY_CMD% -c "import psutil; print(psutil.__version__)" 2^>nul') do (
        echo    [OK] psutil: %%v
    )
)

:: PyInstaller
%PY_CMD% -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo    [AVISO] PyInstaller: Nao instalado (necessario para criar .exe)
    set /a AVISOS+=1
    set "NEED_PYINSTALLER=1"
) else (
    for /f %%v in ('%PY_CMD% -m PyInstaller --version 2^>nul') do (
        echo    [OK] PyInstaller: %%v
    )
)
echo.

:: ============================================================================
:: VERIFICACAO DOS ARQUIVOS DO PROJETO
:: ============================================================================
echo ------------------------------------------------------------------------
echo  ARQUIVOS DO PROJETO
echo ------------------------------------------------------------------------
echo.

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

if exist "%SCRIPT_DIR%requirements.txt" (
    echo    [OK] requirements.txt: Encontrado
) else (
    echo    [AVISO] requirements.txt: Nao encontrado
    set /a AVISOS+=1
)

if exist "%SCRIPT_DIR%dist\GameTranslator.exe" (
    echo    [OK] dist\GameTranslator.exe: Executavel criado
) else (
    echo    [INFO] dist\GameTranslator.exe: Executavel nao criado ainda
)
echo.

:: ============================================================================
:: INSTALAR DEPENDENCIAS FALTANTES
:: ============================================================================
if !AVISOS! GTR 0 (
    if defined PY_CMD (
        echo ------------------------------------------------------------------------
        echo  INSTALAR DEPENDENCIAS FALTANTES
        echo ------------------------------------------------------------------------
        echo.
        set /p "INSTALAR=Deseja instalar as dependencias faltantes agora? (S/N): "
        if /i "!INSTALAR!"=="S" (
            echo.
            echo [INFO] Instalando dependencias...
            echo.
            
            if defined NEED_PYSIDE (
                echo    [+] Instalando PySide6...
                %PY_CMD% -m pip install PySide6>=6.6.0
            )
            
            if defined NEED_REQUESTS (
                echo    [+] Instalando requests...
                %PY_CMD% -m pip install requests>=2.31.0
            )
            
            if defined NEED_PSUTIL (
                echo    [+] Instalando psutil...
                %PY_CMD% -m pip install psutil>=5.9.0
            )
            
            if defined NEED_PYINSTALLER (
                echo    [+] Instalando PyInstaller...
                %PY_CMD% -m pip install pyinstaller
            )
            
            echo.
            echo [OK] Dependencias instaladas!
            echo.
            echo Pressione qualquer tecla para verificar novamente...
            pause >nul
            call "%~f0"
            exit /b
        )
    )
)

:: ============================================================================
:: RESUMO FINAL
:: ============================================================================
:RESUMO
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
        echo   Execute INSTALAR.bat para criar o executavel.
    ) else (
        echo   [AVISO] SISTEMA COMPATIVEL COM AVISOS
        echo.
        echo   Avisos encontrados: !AVISOS!
        echo   Execute novamente e escolha S para instalar dependencias.
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
