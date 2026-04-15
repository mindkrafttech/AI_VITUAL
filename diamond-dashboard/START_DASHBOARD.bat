@echo off
title Diamond AI Dashboard - Launcher
color 0B

:: %~dp0 = THIS folder, works on ANY laptop, ANY drive, ANY path
set DASHBOARD=%~dp0workspace.html

echo.
echo  ==========================================
echo    DIAMOND AI DASHBOARD - STARTING...
echo  ==========================================
echo.
echo  Opening dashboard from:
echo  %DASHBOARD%
echo.

:: Check if workspace.html exists
if not exist "%DASHBOARD%" (
    echo  ERROR: workspace.html not found in this folder!
    echo  Make sure all files are in the same folder as this .bat file.
    echo.
    pause
    exit
)

:: Open in default browser (works on any Windows laptop)
start "" "%DASHBOARD%"

echo  Dashboard opened in your browser!
echo.
echo  ==========================================
echo   HOW TO USE:
echo   - Click "Generate Quiz"  = Works offline
echo   - Click "Scan Problem"   = Upload any image
echo   - Click "Ask Knowledge"  = Needs Flask server
echo  ==========================================
echo.

:: Ask if user wants to start Flask backend too
echo  Do you want to start the AI Backend (Flask) too?
echo  (Only needed for live AI answers - requires Python)
echo.
set /p choice="Type Y for Yes, N for No: "

if /i "%choice%"=="Y" (
    echo.
    echo  Starting Flask Backend...
    if exist "%~dp0app.py" (
        start cmd /k "cd /d "%~dp0" && python app.py"
        echo  Flask backend started! AI features now fully active.
    ) else (
        echo  app.py not found. Running in offline mode only.
    )
)

echo.
echo  Enjoy Diamond AI Dashboard!
echo  Press any key to close this window...
pause >nul
