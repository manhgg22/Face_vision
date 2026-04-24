import os
import sys
import site
import time
import glob

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

DB_DIR = "face_db"

print("="*70)
print("BENCHMARK TOC DO NHAN DIEN KHUON MAT VOI GPU")
print("="*70)

# Check GPU
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"\n✅ GPU: {gpus[0].name}")
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
else:
    print("\n⚠️ Khong phat hien GPU")

# Tìm ảnh test
sample_img = None
for root, dirs, files in os.walk(DB_DIR):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            sample_img = os.path.join(root, file)
            break
    if sample_img:
        break

if not sample_img:
    print("\n❌ Khong tim thay anh de test!")
    sys.exit(1)

print(f"\n📸 Test image: {sample_img}")
print("\n" + "="*70)

# Test 1: RetinaFace (chính xác nhất - theo tài liệu DeepFace)
print("\n[TEST 1] RetinaFace Detector (Chinh xac nhat - theo DeepFace)")
print("-" * 70)
start = time.time()
try:
    result1 = DeepFace.find(
        img_path=sample_img,
        db_path=DB_DIR,
        model_name="Facenet512",
        detector_backend="retinaface",
        enforce_detection=True,
        silent=True
    )
    time1 = time.time() - start
    matches1 = len(result1[0]) if result1 and not result1[0].empty else 0
    print(f"✅ Thoi gian: {time1:.2f}s | Ket qua: {matches1} matches")
except Exception as e:
    time1 = 0
    print(f"❌ Loi: {e}")

# Test 2: OpenCV (cân bằng tốc độ và độ chính xác)
print("\n[TEST 2] OpenCV Detector (Can bang toc do va do chinh xac)")
print("-" * 70)
start = time.time()
try:
    result2 = DeepFace.find(
        img_path=sample_img,
        db_path=DB_DIR,
        model_name="Facenet512",
        detector_backend="opencv",
        enforce_detection=True,
        silent=True
    )
    time2 = time.time() - start
    matches2 = len(result2[0]) if result2 and not result2[0].empty else 0
    print(f"✅ Thoi gian: {time2:.2f}s | Ket qua: {matches2} matches")
except Exception as e:
    time2 = 0
    print(f"❌ Loi: {e}")

# Tổng kết
print("\n" + "="*70)
print("TONG KET")
print("="*70)

if time1 > 0:
    print(f"RetinaFace: {time1:.2f}s (baseline - chinh xac nhat)")
if time2 > 0 and time1 > 0:
    speedup2 = time1 / time2
    print(f"OpenCV:     {time2:.2f}s (nhanh hon {speedup2:.1f}x)")

print("\n💡 KHUYEN NGHI (Theo tai lieu DeepFace):")
print("   ✅ RetinaFace: Do chinh xac cao nhat, phu hop cho production")
print("   ✅ OpenCV: Can bang toc do va do chinh xac, phu hop cho /find-fast")
print("\n📚 Model Facenet512: 98.4% accuracy (cao nhat trong benchmark)")

print("\n" + "="*70)
