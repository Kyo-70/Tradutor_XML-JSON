@echo off
echo ========================================
echo  Game Translator - Build Script
echo ========================================
echo.

echo Instalando PyInstaller...
pip install pyinstaller

echo.
echo Gerando executavel...
pyinstaller --name="GameTranslator" --onefile --windowed --add-data "profiles;profiles" src/main.py

echo.
echo ========================================
echo Build concluido!
echo Executavel criado em: dist\GameTranslator.exe
echo ========================================
pause
