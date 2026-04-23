"""
Script để tối ưu TensorFlow GPU settings
"""
import os
import sys
import site

# Load CUDA paths
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

# Tối ưu TensorFlow TRƯỚC KHI import
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Giảm logging
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1'  # Enable oneDNN optimizations
os.environ['TF_GPU_THREAD_MODE'] = 'gpu_private'  # Tối ưu threading
os.environ['TF_GPU_THREAD_COUNT'] = '2'  # Số threads cho GPU

import tensorflow as tf

print("="*70)
print("TOI UU TENSORFLOW GPU")
print("="*70)

# Cấu hình GPU
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        # Enable memory growth
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        
        # Set visible devices
        tf.config.set_visible_devices(gpus[0], 'GPU')
        
        # Tối ưu XLA (Accelerated Linear Algebra)
        tf.config.optimizer.set_jit(True)
        
        # Mixed precision (nhanh hơn trên GPU hiện đại)
        # policy = tf.keras.mixed_precision.Policy('mixed_float16')
        # tf.keras.mixed_precision.set_global_policy(policy)
        
        print(f"\n✅ GPU: {gpus[0].name}")
        print(f"✅ Memory growth: Enabled")
        print(f"✅ XLA JIT: Enabled")
        # print(f"✅ Mixed precision: Enabled")
        
        # Test performance
        print("\n🧪 Testing GPU performance...")
        import time
        
        with tf.device('/GPU:0'):
            # Warm up
            a = tf.random.normal([1000, 1000])
            b = tf.random.normal([1000, 1000])
            c = tf.matmul(a, b)
            
            # Benchmark
            start = time.time()
            for _ in range(100):
                c = tf.matmul(a, b)
            elapsed = time.time() - start
            
            print(f"   100 matrix multiplications: {elapsed:.3f}s")
            print(f"   Performance: {100/elapsed:.1f} ops/sec")
        
        print("\n✅ GPU da duoc toi uu!")
        
    except RuntimeError as e:
        print(f"❌ Loi: {e}")
else:
    print("\n⚠️ Khong phat hien GPU")

print("\n" + "="*70)
