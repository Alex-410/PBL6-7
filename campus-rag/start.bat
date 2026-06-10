@echo off
title Campus Rules RAG Service
set PORT=9001

echo =========================================
echo   Campus Rules Knowledge Base (RAG)
echo =========================================
echo.

:: Step 1: Check Ollama
echo [1/3] Checking Ollama...
curl -s http://localhost:11434 >nul 2>&1
if errorlevel 1 (
    echo   ERROR: Ollama is not running!
    echo   Please start Ollama first: ollama serve
    echo   Then pull the embedding model: ollama pull qwen3-embedding:0.6b
    pause
    exit /b 1
) else (
    echo   Ollama is running
)

:: Step 2: Install dependencies
echo [2/3] Installing Python dependencies...
cd /d "%~dp0"
pip install -r requirements.txt -q

:: Step 3: Start backend
echo [3/3] Starting RAG backend on port %PORT%...
python main.py

pause
