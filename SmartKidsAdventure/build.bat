@echo off
echo ============================================
echo   Smart Kids Adventure - Build Script
echo ============================================
echo.
echo Installing dependencies...
pip install pygame pyinstaller
echo.
echo Building executable...
cd /d "%~dp0"
pyinstaller --onefile --noconsole --name SmartKidsAdventure main.py
echo.
echo ============================================
echo   Build complete!
echo   Executable: dist\SmartKidsAdventure.exe
echo ============================================
pause
