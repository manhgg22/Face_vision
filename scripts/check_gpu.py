import os
import sys
import site

# Tự động nạp thư viện CUDA 11 (giống như trong face_service.py)
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

print("="*70)
print("KIEM TRA TRANG THAI GPU")
print("="*70)

try:
    import tensorflow as tf
    print(f"\n✓ TensorFlow version: {tf.__version__}")
    
    # Kiểm tra GPU
    gpus = tf.config.list_physical_devices('GPU')
    
    if gpus:
        print(f"\n🎉 THANH CONG! Phat hien {len(gpus)} GPU:")
        for i, gpu in enumerate(gpus):
            print(f"   GPU {i}: {gpu.name}")
            try:
                gpu_details = tf.config.experimental.get_device_details(gpu)
                print(f"   Chi tiet: {gpu_details}")
            except:
                pass
        
        # Test tính toán trên GPU
        print("\n🧪 Dang test tinh toan tren GPU...")
        with tf.device('/GPU:0'):
            a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
            b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
            c = tf.matmul(a, b)
            print(f"   Ket qua test: {c.numpy()}")
        
        print("\n✅ GPU DANG HOAT DONG BINH THUONG!")
        print("   He thong se su dung GPU de xu ly nhan dien khuon mat.")
        
    else:
        print("\n⚠️ KHONG TIM THAY GPU!")
        print("   He thong dang chay tren CPU (cham hon nhieu).")
        print("\n📋 Cac nguyen nhan co the:")
        print("   1. Chua cai dat CUDA/cuDNN")
        print("   2. Driver NVIDIA chua cap nhat")
        print("   3. TensorFlow-GPU chua duoc cai dat dung")
        print("   4. GPU khong tuong thich")
        
    # Kiểm tra CUDA paths
    print("\n📂 Kiem tra CUDA paths:")
    for p in cuda_paths:
        exists = "✓" if os.path.exists(p) else "✗"
        print(f"   {exists} {p}")
    
    # Kiểm tra build info
    print("\n🔧 TensorFlow build info:")
    print(f"   CUDA support: {tf.test.is_built_with_cuda()}")
    print(f"   GPU available: {tf.test.is_gpu_available(cuda_only=True)}")
    
except ImportError as e:
    print(f"\n❌ LOI: Khong the import TensorFlow!")
    print(f"   Chi tiet: {e}")
    print("\n💡 Giai phap: Chay setup_gpu.bat de cai dat lai")
except Exception as e:
    print(f"\n❌ LOI: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
