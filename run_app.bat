@echo off
setlocal
cd /d "%~dp0"
set "PYTHON=C:\Users\Manasa C\AppData\Local\Programs\Python\Python313\python.exe"

if not exist "%PYTHON%" (
  echo Python was not found at the remembered path.
  echo Install Python 3.11 or 3.12, or edit this file to point to your python.exe.
  pause
  exit /b 1
)

echo Installing project requirements...
"%PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 (
  echo Requirement installation failed.
  pause
  exit /b 1
)

if not exist "best_malnutrition_yolov8n.pt" (
  echo.
  echo MODEL FILE MISSING:
  echo Copy your verified model into this folder and name it:
  echo best_malnutrition_yolov8n.pt
  pause
  exit /b 1
)

echo Starting Streamlit...
"%PYTHON%" -m streamlit run app.py
pause
