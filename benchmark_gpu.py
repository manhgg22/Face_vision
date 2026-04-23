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

# Test 1: RetinaFace (chính xác nhưng chậm)
print("\n[TEST 1] RetinaFace Detector (Độ chính xác cao)")
print("-" * 70)
start = time.time()
try:
    result1 = DeepFace.find(
        img_path=sample_img,
        db_path=DB_DIR,
        model_name="Facenet512",
        detector_backend="retinaface",
        enforce_detection=False,
        silent=True
    )
    time1 = time.time() - start
    matches1 = len(result1[0]) if result1 and not result1[0].empty else 0
    print(f"✅ Thoi gian: {time1:.2f}s | Ket qua: {matches1} matches")
except Exception as e:
    time1 = 0
    print(f"❌ Loi: {e}")

# Test 2: OpenCV (cân bằng)
print("\n[TEST 2] OpenCV Detector (Can bang)")
print("-" * 70)
start = time.time()
try:
    result2 = DeepFace.find(
        img_path=sample_img,
        db_path=DB_DIR,
        model_name="Facenet512",
        detector_backend="opencv",
        enforce_detection=False,
        silent=True
    )
    time2 = time.time() - start
    matches2 = len(result2[0]) if result2 and not result2[0].empty else 0
    print(f"✅ Thoi gian: {time2:.2f}s | Ket qua: {matches2} matches")
except Exception as e:
    time2 = 0
    print(f"❌ Loi: {e}")

# Test 3: Skip (nhanh nhất)
print("\n[TEST 3] Skip Detector (Nhanh nhat)")
print("-" * 70)
start = time.time()
try:
    result3 = DeepFace.find(
        img_path=sample_img,
        db_path=DB_DIR,
        model_name="Facenet512",
        detector_backend="skip",
        enforce_detection=False,
        silent=True,
        align=False
    )
    time3 = time.time() - start
    matches3 = len(result3[0]) if result3 and not result3[0].empty else 0
    print(f"✅ Thoi gian: {time3:.2f}s | Ket qua: {matches3} matches")
except Exception as e:
    time3 = 0
    print(f"❌ Loi: {e}")

# Tổng kết
print("\n" + "="*70)
print("TONG KET")
print("="*70)

if time1 > 0:
    print(f"RetinaFace: {time1:.2f}s (baseline)")
if time2 > 0 and time1 > 0:
    speedup2 = time1 / time2
    print(f"OpenCV:     {time2:.2f}s (nhanh hon {speedup2:.1f}x)")
if time3 > 0 and time1 > 0:
    speedup3 = time1 / time3
    print(f"Skip:       {time3:.2f}s (nhanh hon {speedup3:.1f}x) ⚡")

print("\n💡 KHUYEN NGHI:")
if time3 > 0 and time3 < 3:
    print("   ✅ Dung detector='skip' cho FaceID/Unlock (nhanh nhat!)")
elif time2 > 0 and time2 < 5:
    print("   ✅ Dung detector='opencv' cho can bang toc do va do chinh xac")
else:
    print("   ⚠️ Can toi uu them hoac nang cap GPU")

print("\n" + "="*70)
