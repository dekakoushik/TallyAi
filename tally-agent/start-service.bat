@echo off
title TallyAI - Local Sync Agent Service
color 0A
echo ========================================================
echo        TallyAI Local Sync Service (Background Agent)
echo ========================================================
echo.
echo Checking environment and starting service loop...
echo.

cd /d "%~dp0"

REM Activate virtualenv if present or use system python
if exist "..\backend\venv\Scripts\python.exe" (
    ..\backend\venv\Scripts\python.exe run_agent.py
) else if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe run_agent.py
) else (
    python run_agent.py
)

pause
