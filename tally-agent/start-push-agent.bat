@echo off
title TallyAI Lightweight Push Agent
color 0A
echo ========================================================
echo        TallyAI Push Agent (Running on Tally PC)
echo ========================================================
echo.

cd /d "%~dp0"

REM If requirements not installed, install them once
python -m pip install -r requirements.txt

echo.
echo Starting push loop to remote Dokploy server...
python push_agent.py

pause
