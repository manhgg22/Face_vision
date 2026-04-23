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

# DeepFace import
from deepface import DeepFace
import threading

app = FastAPI(title="FaceID Pro - Fast Index Mode", version="3.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

TEMP_DIR = "face_temp_uploads"
DB_DIR = "face_db"
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

# ── Consistent defaults ────────────────────────────────────────────────────────
# Switch to yolov8 and Facenet for MAX SPEED (under 1s)
DEFAULT_MODEL    = "Facenet512"
DEFAULT_DETECTOR = "retinaface"    
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
            print("[INDEXING] Đã tối ưu xong! Sẵn sàng nhận diện tốc độ cao.")
        else:
            print("[INDEXING] Database trống.")
    except Exception as e:
        print(f"[INDEXING ERROR] {e}")
    finally:
        is_indexing = False

@app.get("/db/status")
def get_status():
    global is_indexing
    return {"is_indexing": is_indexing}

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
        print(f"\n{'='*60}")
        print(f"[SEARCH] Query: {image.filename} -> {path}")
        print(f"[SEARCH] Model: {model_name} | Detector: {detector_backend}")

        # DeepFace.find
        # We set silent=False to see DeepFace logs in console
        dfs = DeepFace.find(
            img_path=path,
            db_path=DB_DIR,
            model_name=model_name,
            detector_backend=detector_backend,
            enforce_detection=False,
            silent=False,
            threshold=threshold
        )

        results = []
        best_candidate = {"name": "None", "distance": 1.0}

        for df in dfs:
            if df.empty: continue
            
            matches = df.to_dict('records')
            for match in matches:
                id_path = match.get('identity', '').replace('/', os.sep).replace('\\', os.sep)
                parts = id_path.split(os.sep)
                name = parts[-2] if len(parts) >= 2 else "Unknown"
                match['name'] = name
                
                # Tracking best overall candidate (even if above threshold)
                dist = float(match.get('distance', 1.0))
                if dist < best_candidate['distance']:
                    best_candidate = {"name": name, "distance": dist, "file": os.path.basename(id_path)}
                
                # Convert for JSON
                for k, v in match.items():
                    if hasattr(v, '__float__'): match[k] = float(v)
            
            results.append(matches)

        elapsed = time.time() - start_time
        match_count = sum(len(r) for r in results)
        
        print(f"[RESULT] Found {match_count} matches in {elapsed:.2f}s")
        if match_count > 0:
            for r in results:
                for m in r:
                    print(f"  > MATCH: {m['name']} (Dist: {m['distance']:.4f})")
        else:
            print(f"[DEBUG] No matches meet the threshold.")
            print(f"[DEBUG] Best candidate was: {best_candidate['name']} with distance {best_candidate['distance']:.4f}")
            if best_candidate['name'] != "None":
                print(f"        (Suggest: Try increasing threshold or improving image quality)")

        return {
            "success": True,
            "results": results,
            "match_count": match_count,
            "best_candidate": best_candidate if match_count == 0 else None,
            "debug_info": {
                "elapsed_seconds": round(elapsed, 2),
                "model": model_name,
                "detector": detector_backend
            }
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
