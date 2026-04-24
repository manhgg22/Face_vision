@echo off
echo ========================================================
echo KHOI DONG HE THONG FACE ID (CHE DO GPU)
echo ========================================================

cd /d "%~dp0.."
set PYTHON_EXE=.venv\Scripts\python.exe

if not exist %PYTHON_EXE% (
    echo [LOI] Khong tim thay moi truong ao .venv!
    echo Vui long chay setup_gpu.bat truoc.
    pause
    exit /b
)

%PYTHON_EXE% face_service.py
pause
