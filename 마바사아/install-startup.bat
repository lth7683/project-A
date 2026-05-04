@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$startup=[Environment]::GetFolderPath('Startup'); $shortcut=Join-Path $startup 'YouTube Transcript Batch Web.lnk'; $shell=New-Object -ComObject WScript.Shell; $link=$shell.CreateShortcut($shortcut); $link.TargetPath='wscript.exe'; $link.Arguments='\"%~dp0start-hidden.vbs\"'; $link.WorkingDirectory='%~dp0'; $link.IconLocation='%SystemRoot%\System32\SHELL32.dll,220'; $link.Save()"
wscript.exe "%~dp0start-hidden.vbs"
powershell -NoProfile -Command "Start-Sleep -Seconds 2"
start "" "http://localhost:3000"
