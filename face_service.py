import os
import glob
import shutil
import uuid
import traceback
import time
from typing import Optional, List

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn

# Tự động nạp thư viện CUDA 11 tải từ pip để TF 2.10 nhận được GPU trên Windows
import site
import sys
import os

# Tối ưu TensorFlow TRƯỚC KHI import
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Giảm logging
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1'  # Enable oneDNN optimizations
os.environ['TF_GPU_THREAD_MODE'] = 'gpu_private'  # Tối ưu threading

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

# DeepFace import
from deepface import DeepFace
import threading
import tensorflow as tf

# Kiểm tra trạng thái GPU
gpus = tf.config.list_physical_devices('GPU')
DEVICE_STATUS = "🚀 [GPU] NVIDIA RTX ACTIVE" if gpus else "⚠️ [CPU] FALLBACK MODE"

# Optimized for Windows without full CUDA SDK (fixing ptxas.exe issue)
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices=false'

# Configure GPU memory growth to avoid OOM errors
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        tf.config.set_visible_devices(gpus[0], 'GPU')
        tf.config.optimizer.set_jit(False)  # Disable XLA to fix ptxas.exe error
        print(f"✅ GPU Memory Growth enabled (XLA disabled for stability)")
    except RuntimeError as e:
        print(f"GPU config error: {e}")

print("\n" + "="*60)
print(f"Hệ thống đang sử dụng: {DEVICE_STATUS}")
print("="*60 + "\n")

# Pre-load model at startup for faster first request
print("[STARTUP] Pre-loading model...")
try:
    from deepface.basemodels import Facenet
    model = Facenet.loadModel()
    print(f"[STARTUP] ✅ Model {DEFAULT_MODEL} loaded successfully!")
except Exception as e:
    print(f"[STARTUP] ⚠️ Model pre-load failed: {e}")

app = FastAPI(title="FaceID Pro - Fast Index Mode", version="3.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

TEMP_DIR = "face_temp_uploads"
DB_DIR = "face_db"
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

# Optimized for ACCURACY (OpenCV is the default in DeepFace)
DEFAULT_MODEL    = "Facenet512"  # Fast and accurate
DEFAULT_DETECTOR = "opencv"      # Standard face detection (more accurate than 'skip')
# Alternative: "retinaface" for maximum accuracy (slower)
# ──────────────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Dashboard file not found.</h1>"

def save_upload(upload: UploadFile) -> str:
    filename = upload.filename or "img.jpg"
    ext = os.path.splitext(filename)[1].lower() or ".jpg"
    path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}{ext}")
    with open(path, "wb") as f:
        shutil.copyfileobj(upload.file, f)
    
    # WebP conversion
    if ext == ".webp":
        try:
            from PIL import Image
            jpg_path = path.replace(".webp", ".jpg")
            Image.open(path).convert("RGB").save(jpg_path, "JPEG")
            os.remove(path)
            return jpg_path
        except: pass
    return path

def cleanup(*paths: str):
    for p in paths:
        try:
            if p and os.path.exists(p): os.remove(p)
        except: pass

def purge_pkl_cache():
    count = 0
    for pkl in glob.glob(os.path.join(DB_DIR, "**", "*.pkl"), recursive=True):
        try:
            os.remove(pkl)
            count += 1
        except: pass
    return count

@app.get("/health")
def health():
    return {"status": "ok", "model": DEFAULT_MODEL, "detector": DEFAULT_DETECTOR}

# --- BACKGROUND INDEXING ---
is_indexing = False

def build_index_task():
    global is_indexing
    if is_indexing: return
    is_indexing = True
    print("\n[INDEXING] Đang quét toàn bộ Database ở chế độ chạy ngầm...")
    try:
        sample_img = None
        for root, dirs, files in os.walk(DB_DIR):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    sample_img = os.path.join(root, file)
                    break
            if sample_img: break
            
        if sample_img:
            DeepFace.find(
                img_path=sample_img,
                db_path=DB_DIR,
                model_name=DEFAULT_MODEL,
                detector_backend=DEFAULT_DETECTOR,
                enforce_detection=False,
                silent=True
            )
            print(f"[{DEVICE_STATUS}] [INDEXING] Đã tối ưu xong! Sẵn sàng nhận diện tốc độ cao.")
        else:
            print("[INDEXING] Database trống.")
    except Exception as e:
        print(f"[INDEXING ERROR] {e}")
    finally:
        is_indexing = False

@app.get("/db/status")
def get_status():
    global is_indexing
    return {"is_indexing": is_indexing, "device": DEVICE_STATUS}

@app.get("/db/build-index")
def trigger_build_index(background_tasks: BackgroundTasks):
    global is_indexing
    if is_indexing:
        return {"status": "already_running"}
    background_tasks.add_task(build_index_task)
    return {"status": "started"}

@app.get("/db/list")
def list_db():
    identities = {}
    for name in os.listdir(DB_DIR):
        folder = os.path.join(DB_DIR, name)
        if os.path.isdir(folder):
            identities[name] = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    return {"identities": identities}

@app.get("/db/purge-cache")
def purge_cache(background_tasks: BackgroundTasks):
    count = purge_pkl_cache()
    print(f"[CACHE] Purged {count} pkl files.")
    background_tasks.add_task(build_index_task) # Tự động quét lại luôn
    return {"success": True, "deleted": count}

@app.post("/find")
async def find_identity(
    image: UploadFile = File(...),
    model_name: str = Form(DEFAULT_MODEL),
    detector_backend: str = Form(DEFAULT_DETECTOR),
    threshold: Optional[float] = Form(None)
):
    path = None
    start_time = time.time()
    try:
        path = save_upload(image)
        from PIL import Image
        with Image.open(path) as img:
            img_w, img_h = img.size

        print(f"\n{'='*60}")
        print(f"[{DEVICE_STATUS}]")
        print(f"[SEARCH] Query: {image.filename} ({img_w}x{img_h}) -> {path}")
        print(f"[SEARCH] Params: Model={model_name} | Detector={detector_backend} | Threshold={threshold or 'Auto'}")

        # IMPORTANT: Validate that image contains a face first
        try:
            from deepface.modules import detection
            # Use opencv for validation even if skip is requested for search
            val_detector = detector_backend if detector_backend != "skip" else "opencv"
            face_objs = detection.extract_faces(
                img_path=path,
                detector_backend=val_detector,
                enforce_detection=True,
                align=True
            )
            
            if not face_objs or len(face_objs) == 0:
                print(f"[VALIDATION] ❌ No face detected using {val_detector}")
                return {
                    "success": False,
                    "error": "NO_FACE_DETECTED",
                    "message": "Không phát hiện khuôn mặt trong ảnh. Vui lòng sử dụng ảnh rõ mặt.",
                    "match_count": 0
                }
            
            print(f"[VALIDATION] ✅ Detected {len(face_objs)} face(s) using {val_detector}")
            
        except Exception as e:
            print(f"[VALIDATION] ⚠️ Face detection check failed: {e}")
            # We continue anyway but log the warning

        # DeepFace.find with optimized settings
        dfs = DeepFace.find(
            img_path=path,
            db_path=DB_DIR,
            model_name=model_name,
            detector_backend=detector_backend,
            enforce_detection=False,
            silent=True,
            threshold=threshold,
            align=True,
            normalization="base"
        )

        # Collect all matches
        all_matches = []
        for df in dfs:
            if df.empty: continue
            matches = df.to_dict('records')
            for match in matches:
                id_path = match.get('identity', '').replace('/', os.sep).replace('\\', os.sep)
                parts = id_path.split(os.sep)
                name = parts[-2] if len(parts) >= 2 else "Unknown"
                match['name'] = name
                
                # Convert for JSON
                for k, v in match.items():
                    if hasattr(v, '__float__'): match[k] = float(v)
                all_matches.append(match)

        # Sort by distance
        all_matches = sorted(all_matches, key=lambda x: x['distance'])
        
        best_match = all_matches[0] if all_matches else None
        results = [[best_match]] if best_match else []
        
        elapsed = time.time() - start_time
        match_count = 1 if best_match else 0
        
        print(f"[RESULT] Search finished in {elapsed:.2f}s")
        if all_matches:
            print(f"  > TOP 3 CANDIDATES:")
            for i, m in enumerate(all_matches[:3]):
                indicator = "⭐" if i == 0 else "  "
                print(f"    {indicator} {m['name']} (Dist: {m['distance']:.4f} | Conf: {(1-m['distance'])*100:.1f}%)")
        else:
            print(f"  > ❌ No matches found below threshold.")
            # Show closest if any
            if hasattr(DeepFace, 'last_results') or True: # Just a placeholder concept
                pass 

        best_candidate = {
            "name": all_matches[0]['name'], 
            "distance": all_matches[0]['distance'], 
            "file": os.path.basename(all_matches[0].get('identity', ''))
        } if all_matches else {"name": "None", "distance": 1.0}

        return {
            "success": True,
            "results": results,
            "match_count": match_count,
            "best_candidate": best_candidate if match_count == 0 else None,
            "debug_info": {
                "elapsed_seconds": round(elapsed, 2),
                "model": model_name,
                "detector": detector_backend,
                "device": DEVICE_STATUS
            }
        }
    except Exception as e:
        print(f"[ERROR] {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cleanup(path)

@app.post("/find-fast")
async def find_identity_fast(
    image: UploadFile = File(...)
):
    """Ultra-fast face recognition endpoint - optimized for speed"""
    path = None
    start_time = time.time()
    try:
        path = save_upload(image)
        from PIL import Image
        with Image.open(path) as img:
            img_w, img_h = img.size

        print(f"\n{'='*60}")
        print(f"[{DEVICE_STATUS}]")
        print(f"[FAST-SEARCH] Query: {image.filename} ({img_w}x{img_h})")

        # Fast search but still using a detector for accuracy
        dfs = DeepFace.find(
            img_path=path,
            db_path=DB_DIR,
            model_name="Facenet512",
            detector_backend="opencv", # Use opencv instead of skip for better accuracy
            enforce_detection=False,
            silent=True,
            align=False,  # Skip alignment for speed
            normalization="base"
        )

        results = []
        best_match = None
        best_distance = 1.0

        for df in dfs:
            if df.empty: continue
            
            matches = df.to_dict('records')
            for match in matches:
                id_path = match.get('identity', '').replace('/', os.sep).replace('\\', os.sep)
                parts = id_path.split(os.sep)
                name = parts[-2] if len(parts) >= 2 else "Unknown"
                
                dist = float(match.get('distance', 1.0))
                if dist < best_distance:
                    best_distance = dist
                    best_match = {
                        "name": name,
                        "distance": dist,
                        "confidence": round((1 - dist) * 100, 2)
                    }

        elapsed = time.time() - start_time
        
        print(f"[FAST-RESULT] Search finished in {elapsed:.2f}s")
        if best_match:
            print(f"  > MATCH FOUND: {best_match['name']} (Conf: {best_match['confidence']:.1f}% | Dist: {best_match['distance']:.4f})")
        else:
            print(f"  > ❌ No matches found.")

        return {
            "success": True,
            "match": best_match,
            "match_count": 1 if best_match else 0,
            "elapsed_seconds": round(elapsed, 3),
            "device": DEVICE_STATUS
        }
    except Exception as e:
        print(f"[ERROR] {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cleanup(path)

if __name__ == "__main__":
    print(f"\n🚀 FaceID Pro Service starting on port 8001...")
    print(f"📁 Database: {os.path.abspath(DB_DIR)}")
    uvicorn.run(app, host="0.0.0.0", port=8001)
