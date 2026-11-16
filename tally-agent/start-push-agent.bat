@echo off
title TallyAI Auto Push Agent
color 0A

echo ======================================================================
echo                TallyAI Automatic Push Service
echo ======================================================================
echo.
echo Connecting local Tally Prime (port 9000) to:
echo   https://tally.plystory.si
echo.

cd /d "%~dp0"

REM Step 1: Ensure lightweight dependencies are installed
echo [1/2] Verifying Python libraries...
python -m pip install --quiet requests xmltodict python-dotenv

REM Step 2: Run the push sync daemon
echo [2/2] Starting Tally Sync Loop (press Ctrl+C to stop)...
echo.
python push_agent.py

pause
