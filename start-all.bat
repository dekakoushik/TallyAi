@echo off
title TallyAI - All-in-One Launcher
color 0B
echo ========================================================
echo       TallyAI System Launcher (Remote and Local)
echo ========================================================
echo.
echo Configuration:
echo - Tally Server (Local LAN): 192.168.2.100:9000
echo - Remote Static IP        : 115.246.171.163
echo - Frontend Dashboard Port : 3000
echo - Backend API Port        : 8000
echo.

set PYTHONPATH=%CD%\backend

echo [1/2] Starting Backend API Server on 0.0.0.0:8000...
start "TallyAI Backend" cmd /k "cd /d "%~dp0backend" && venv\Scripts\activate && set PYTHONPATH=.. && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo [2/2] Starting Frontend Dashboard on 0.0.0.0:3000...
start "TallyAI Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev -- --host 0.0.0.0 --port 3000"

echo.
echo ========================================================
echo TallyAI is running!
echo - Local Machine Access : http://localhost:3000
echo - Office LAN Access    : http://192.168.2.100:3000
echo - Worldwide Access     : http://115.246.171.163:3000
echo - Backend API Docs     : http://115.246.171.163:8000/docs
echo ========================================================
echo.
pause
