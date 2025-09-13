@echo off
echo Starting DyslexiaCare Frontend...

cd /d "%~dp0..\src\dyslexia_platform\frontend"

echo Installing/updating dependencies...
pip install -r requirements.txt

echo Launching Streamlit application...
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

pause