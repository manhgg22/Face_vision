import os
import sys
import site

# Tự động nạp thư viện CUDA 11
site_packages = [p for p in site.getsitepackages() if "site-packages" in p]
site_packages = site_packages[0] if site_packages else site.getsitepackages()[-1]

cuda_paths = [
    os.path.join(site_packages, "nvidia", "cuda_runtime", "bin"),
    os.path.join(site_packages, "nvidia", "cublas", "bin"),
    os.path.join(site_packages, "nvidia", "cudnn", "bin"),
    os.path.join(site_packages, "nvidia", "cufft", "bin"),
    os.path.join(site_packages, "nvidia", "curand", "bin"),
    os.path.join(site_packages, "nvidia", "cusolver", "bin"),
    os.path.join(site_packages, "nvidia", "cusparse", "bin"),
]

for p in cuda_paths:
    if os.path.exists(p):
        os.environ["PATH"] = p + os.pathsep + os.environ["PATH"]
        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(p)
            except Exception:
                pass

import tensorflow as tf
from deepface import DeepFace
import time

print("="*70)
print("TEST NHAN DIEN KHUON MAT VOI GPU")
print("="*70)

# Kiểm tra GPU
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"\n✅ GPU: {gpus[0].name}")
    gpu_details = tf.config.experimental.get_device_details(gpus[0])
    print(f"   Ten: {gpu_details.get('device_name', 'N/A')}")
    print(f"   Compute Capability: {gpu_details.get('compute_capability', 'N/A')}")
else:
    print("\n⚠️ Khong phat hien GPU, dang chay tren CPU")

print("\n" + "="*70)
print("Luu y: Service da san sang su dung GPU!")
print("Chay start_gpu.bat de khoi dong service.")
print("="*70)
