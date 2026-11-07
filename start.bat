@echo off
chcp 65001 >nul
cd /d "%~dp0"
where python >nul 2>nul || (echo Nainstaluj Python z python.org a zaskrtni "Add to PATH". & pause & exit /b)
where clamscan >nul 2>nul || (echo Nainstaluj ClamAV z clamav.net a pridej ho do PATH. & pause & exit /b)
echo Aktualizuji databazi virus...
freshclam
start "" http://127.0.0.1:8765
python app.py
pause
