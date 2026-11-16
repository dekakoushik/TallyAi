@echo off
title TallyAI - Mock Tally Prime Server (Port 9000)
echo ========================================================
echo       Mock Tally Prime XML HTTP Gateway (Port 9000)
echo       Use this for testing whenever Tally is offline
echo ========================================================
echo.
cd tally-agent
..\backend\venv\Scripts\python mock_tally_server.py
pause
