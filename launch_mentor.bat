@echo off
TITLE DIAMOND AI - MENTOR
SETLOCAL EnableDelayedExpansion
COLOR 0B

echo --------------------------------------------------
echo      DIAMOND AI MENTOR - 2026 LAUNCHER (MENTOR-MODE)
echo --------------------------------------------------
echo [1/3] Syncing AI Libraries...
"%~dp0.venv\Scripts\pip" install flask flask-cors flask-sqlalchemy chromadb google-genai google-generativeai openai python-dotenv sentence-transformers beautifulsoup4 requests pydantic<2.0

echo [2/3] Accessing Backend Logic...
cd /d "%~dp0ai-tutor-backend"

echo [3/3] Powering on the Brain (Gemini 2026 Core)...
"%~dp0.venv\Scripts\python" run.py

pause
