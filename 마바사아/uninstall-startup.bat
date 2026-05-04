@echo off
powershell -NoProfile -ExecutionPolicy Bypass -Command "$shortcut=Join-Path ([Environment]::GetFolderPath('Startup')) 'YouTube Transcript Batch Web.lnk'; Remove-Item -LiteralPath $shortcut -ErrorAction SilentlyContinue"
