@echo off
title Diamond Dashboard - Save All Files
color 0B

:: %~dp0 = the folder where THIS .bat file lives (works on ANY laptop, ANY path)
set SOURCE=%~dp0
set BACKUP=%~dp0backup

echo.
echo  ============================================
echo   DIAMOND AI DASHBOARD - SAVING ALL FILES
echo  ============================================
echo   Folder: %SOURCE%
echo  ============================================
echo.

:: Create backup folder if it doesn't exist
if not exist "%BACKUP%" mkdir "%BACKUP%"

:: Copy all main files to backup
echo  [1] Saving workspace.html ...
copy /Y "%SOURCE%workspace.html" "%BACKUP%\workspace.html" >nul 2>&1
echo      Done!

echo  [2] Saving styles.css ...
copy /Y "%SOURCE%styles.css" "%BACKUP%\styles.css" >nul 2>&1
echo      Done!

echo  [3] Saving script.js ...
copy /Y "%SOURCE%script.js" "%BACKUP%\script.js" >nul 2>&1
echo      Done!

echo  [4] Saving all HTML, CSS, JS, Python files ...
for %%f in ("%SOURCE%*.html" "%SOURCE%*.css" "%SOURCE%*.js" "%SOURCE%*.py" "%SOURCE%*.png" "%SOURCE%*.jpg" "%SOURCE%*.gif") do (
    copy /Y "%%f" "%BACKUP%\" >nul 2>&1
)
echo      Done!

echo.
echo  ============================================
echo   ALL FILES SAVED TO: backup\ folder
echo  ============================================
echo.
pause
