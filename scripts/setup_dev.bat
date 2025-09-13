@echo off
echo DyslexiaCare Platform Setup
echo ========================

cd /d "%~dp0.."

echo Creating Python virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Setting up backend...
cd backend
pip install -r requirements.txt
cd ..

echo Setting up frontend...
cd frontend
pip install -r requirements.txt
cd ..

echo Creating necessary directories...
if not exist "backend\uploads" mkdir backend\uploads
if not exist "backend\outputs" mkdir backend\outputs
if not exist "backend\database" mkdir backend\database
if not exist "logs" mkdir logs

echo Copying environment configuration...
copy config\.env.example .env

echo Setup complete!
echo.
echo To run the platform:
echo 1. Backend: scripts\run_backend.bat
echo 2. Frontend: scripts\run_frontend.bat
echo.
echo Visit http://localhost:8501 for the frontend
echo Visit http://localhost:8000/docs for API documentation
echo.
pause