import os
import sys
import site
import glob
import time

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
print("XOA VA TAO LAI CACHE VOI GPU")
print("="*70)

# Check GPU
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"\n✅ Dang su dung GPU: {gpus[0].name}")
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
else:
    print("\n⚠️ Khong phat hien GPU, dang chay tren CPU")

# Xóa tất cả file .pkl (cache cũ)
print("\n[1/3] Xoa cache cu...")
pkl_files = glob.glob(os.path.join(DB_DIR, "**", "*.pkl"), recursive=True)
for pkl in pkl_files:
    try:
        os.remove(pkl)
        print(f"   Deleted: {pkl}")
    except Exception as e:
        print(f"   Error deleting {pkl}: {e}")

print(f"\n   Da xoa {len(pkl_files)} file cache")

# Đếm số ảnh trong database
print("\n[2/3] Kiem tra database...")
total_images = 0
identities = {}
for name in os.listdir(DB_DIR):
    folder = os.path.join(DB_DIR, name)
    if os.path.isdir(folder):
        images = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        if images:
            identities[name] = len(images)
            total_images += len(images)

print(f"   Tim thay {len(identities)} nguoi voi {total_images} anh")
for name, count in identities.items():
    print(f"   - {name}: {count} anh")

if total_images == 0:
    print("\n❌ Database trong! Khong co gi de index.")
    sys.exit(1)

# Tạo cache mới bằng cách chạy find với ảnh đầu tiên
print("\n[3/3] Tao cache moi voi GPU...")
sample_img = None
for root, dirs, files in os.walk(DB_DIR):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            sample_img = os.path.join(root, file)
            break
    if sample_img:
        break

if sample_img:
    print(f"   Dang xu ly: {sample_img}")
    start_time = time.time()
    
    try:
        # Sử dụng detector="skip" để nhanh nhất
        dfs = DeepFace.find(
            img_path=sample_img,
            db_path=DB_DIR,
            model_name="Facenet512",
            detector_backend="skip",  # FASTEST!
            enforce_detection=False,
            silent=True
        )
        
        elapsed = time.time() - start_time
        print(f"\n✅ THANH CONG!")
        print(f"   Thoi gian: {elapsed:.2f}s")
        print(f"   Toc do: {total_images/elapsed:.1f} anh/giay")
        
        # Kiểm tra cache đã được tạo
        new_pkl = glob.glob(os.path.join(DB_DIR, "**", "*.pkl"), recursive=True)
        print(f"   Da tao {len(new_pkl)} file cache")
        
        print("\n" + "="*70)
        print("CACHE DA DUOC TOI UU!")
        print("Lan tim kiem tiep theo se NHANH HON NHIEU!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ LOI: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\n❌ Khong tim thay anh nao trong database!")

print("\n")
