@echo off
title SolarView - Solar System Simulation
cd /d "%~dp0"
python main.py
if errorlevel 1 (
    echo.
    echo Simulation exited with an error.
    pause
)
