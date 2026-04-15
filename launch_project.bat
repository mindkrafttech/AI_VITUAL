@echo off
TITLE DIAMOND AI - LOCALHOST LAUNCHER
SETLOCAL EnableDelayedExpansion
COLOR 0B

echo --------------------------------------------------
echo      DIAMOND AI MENTOR - 2026 LAUNCHER
echo --------------------------------------------------
echo.

:: Get absolute path of current folder
set "ROOT_DIR=%~dp0"
echo [LOG] Project Root: %ROOT_DIR%

:: 1. Verify Virtual Environment
if not exist "%ROOT_DIR%.venv\Scripts\python.exe" (
    echo [ERROR] .venv not found. Creating virtual environment...
    python -m venv .venv
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to create virtual environment. Please install Python.
        pause
        exit /b
    )
)
echo [OK] Virtual Environment ready.

:: 2. Sync AI Dependencies
echo [LOG] Checking/Updating modern AI libraries...
"%ROOT_DIR%.venv\Scripts\pip" install flask flask-cors flask-sqlalchemy chromadb google-genai google-generativeai openai python-dotenv sentence-transformers beautifulsoup4 requests pydantic<2.0
if !errorlevel! neq 0 (
    echo [WARNING] Dependency sync failed. Attempting manual fix...
    "%ROOT_DIR%.venv\Scripts\pip" install flask flask-cors flask-sqlalchemy chromadb google-genai google-generativeai openai python-dotenv sentence-transformers pydantic<2.0
)

:: 3. Launch Backend Brain
echo.
echo [LOG] Powering on the Digital Brain (Port 5000)...
echo [LOG] If the browser window shows "Connection Error", wait for
echo [LOG] the "DIAMOND AI - BACKEND" terminal to say "LIVE" and then
echo [LOG] refresh your browser!
echo.

:: Launch in a separate window so logs are visible
cd /d "%ROOT_DIR%ai-tutor-backend"
start "DIAMOND AI - BACKEND" cmd /k "..\\.venv\\Scripts\\python.exe run.py"

:: 4. Auto-Open Dashboard
echo [LOG] Waiting 8 seconds for server synchronization...
timeout /t 8 /nobreak > nul
echo [LOG] Opening Dashboard in browser...
start http://127.0.0.1:5000

echo.
echo ==========================================
echo       SYSTEM IS NOW ONLINE (127.0.0.1)
echo ==========================================
echo [INFO] Dashboard:     http://127.0.0.1:5000
echo [INFO] Memory Palace: http://127.0.0.1:5000/memory-palace.html
echo [INFO] Workspace:     http://127.0.0.1:5000/workspace.html
echo.
echo You can monitor logs in the other terminal.
echo.
pause
