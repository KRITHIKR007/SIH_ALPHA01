@echo off
echo Starting DyslexiaCare Backend Server...

cd /d "%~dp0..\backend"

echo Installing/updating dependencies...
pip install -r requirements.txt

echo Creating uploads and outputs directories...
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs
if not exist "database" mkdir database

echo Starting FastAPI server...
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause