@echo off
title PCOS Saathi Local Server
echo Starting PCOS Saathi at http://localhost:5173/ ...
start http://localhost:5173/
powershell -ExecutionPolicy Bypass -File "%~dp0serve.ps1"
pause
