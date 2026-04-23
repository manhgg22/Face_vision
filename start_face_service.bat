@echo off
echo ============================================================
echo   Starting Face Analysis Service (DeepFace - Port 8001)
echo ============================================================
cd /d "%~dp0"
python face_service.py
pause
