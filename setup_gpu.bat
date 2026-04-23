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
pip install tensorflow-gpu==2.10.1 keras==2.10.0 protobuf==3.19.6 numpy==1.23.5
echo.
echo Installing CUDA 11 libraries (full set for GPU support)...
pip install nvidia-cuda-runtime-cu11
pip install nvidia-cudnn-cu11==8.9.4.25
pip install nvidia-cublas-cu11
pip install nvidia-cufft-cu11
pip install nvidia-curand-cu11
pip install nvidia-cusolver-cu11
pip install nvidia-cusparse-cu11
echo.
echo Installing application dependencies...
pip install fastapi uvicorn python-multipart pydantic flask-cors opencv-python==4.9.0.80
pip install deepface==0.0.99 --no-deps
pip install retina-face==0.0.17 --no-deps
pip install fire gdown h5py>=2.9.0 mtcnn tqdm joblib lightecc lightphe gdown Pillow python-dotenv pandas pytz python-dateutil

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
