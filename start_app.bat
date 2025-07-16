@echo off
echo Starting Monkeypox Classifier Application...
echo.
echo Activating virtual environment...
call .venv\Scripts\activate

echo.
echo Starting Streamlit application...
cd faceemotion\app
streamlit run main.py

echo.
echo Application closed.
pause
