@echo off
cd /d "%~dp0"
start "YouTube Transcript Server" /min node server.js
powershell -NoProfile -Command "Start-Sleep -Seconds 2"
start "" "http://localhost:3000"
