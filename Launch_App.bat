@echo off
title TalentMatch AI - Resume Screener
echo ========================================================
echo    Starting TalentMatch AI Resume Screener...
echo ========================================================
cd /d "%~dp0"

:: Wait 2 seconds and open the browser automatically
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8000"

:: Start the Python application
.\.venv\Scripts\python.exe run.py

pause
