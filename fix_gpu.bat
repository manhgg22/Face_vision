@echo off
echo ========================================================
echo FIXING DEPENDENCIES FOR TENSORFLOW GPU
echo ========================================================
echo.
echo [1/2] Activating virtual environment...
call .venv\Scripts\activate

echo.
echo [2/2] Forcing correct versions of Keras and Protobuf for TF 2.10.1...
python -m pip install keras==2.10.0 protobuf==3.19.6 tensorflow-gpu==2.10.1

echo.
echo ========================================================
echo DONE! The red text errors are now fixed.
echo ========================================================
echo Please run your server again:
echo python face_service.py
echo ========================================================
pause
