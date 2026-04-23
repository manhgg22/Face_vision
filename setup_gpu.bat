@echo off
echo ========================================================
echo SETTING UP PYTHON 3.10 AND TENSORFLOW GPU
echo FOR NVIDIA RTX 3050 (NATIVE WINDOWS)
echo ========================================================
echo.
echo [1/4] Downloading and installing Python 3.10...
echo (Note: If a UAC prompt appears, please click Yes)
winget install --id Python.Python.3.10 -e --accept-package-agreements --accept-source-agreements

echo.
echo [2/4] Creating virtual environment (.venv)...
py -3.10 -m venv .venv

echo.
echo [3/4] Activating virtual environment...
call .venv\Scripts\activate

echo.
echo [4/4] Installing TensorFlow 2.10.1 (Last version with Windows GPU support)...
python -m pip install --upgrade pip
pip install tensorflow-gpu==2.10.1
pip install deepface fastapi uvicorn python-multipart pydantic

echo.
echo ========================================================
echo DONE!
echo The system is now configured to use your NVIDIA RTX 3050.
echo ========================================================
echo HOW TO RUN:
echo From now on, to start the server with GPU, run these 2 commands:
echo 1. call .venv\Scripts\activate
echo 2. python face_service.py
echo ========================================================
pause
