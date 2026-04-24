# Face Recognition Service - GPU Accelerated

Dịch vụ nhận diện khuôn mặt sử dụng DeepFace với GPU acceleration.

## 📋 Tài Liệu

- [README.md](README.md) - Tài liệu DeepFace gốc
- [GIAI_THICH_TOC_DO.md](GIAI_THICH_TOC_DO.md) - Giải thích về tốc độ xử lý
- [GPU_SETUP_GUIDE.md](GPU_SETUP_GUIDE.md) - Hướng dẫn cấu hình GPU

## 🚀 Khởi Động Nhanh

### 1. Cài Đặt Dependencies

```cmd
pip install -r requirements/requirements.txt
```

### 2. Khởi Động Service

```cmd
start_gpu.bat
```

### 3. Test Service

Mở `test_speed.html` trong trình duyệt để test.

## 📊 Cấu Hình Hiện Tại

- **Model**: Facenet512 (98.4% accuracy)
- **Detector**: RetinaFace (chính xác nhất)
- **GPU**: NVIDIA RTX 3050 Laptop

## 🔧 API Endpoints

### POST /find
Tìm kiếm khuôn mặt với độ chính xác cao nhất (RetinaFace detector)

**Request:**
```javascript
const formData = new FormData();
formData.append('image', imageFile);
formData.append('model_name', 'Facenet512');
formData.append('detector_backend', 'retinaface');
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "name": "Minh",
      "distance": 0.015,
      "confidence": 98.5
    }
  ],
  "match_count": 1,
  "total_matches": 5
}
```

### POST /find-fast
Tìm kiếm nhanh với OpenCV detector

**Response:**
```json
{
  "success": true,
  "best_match": {
    "name": "Minh",
    "distance": 0.015,
    "confidence": 98.5
  },
  "all_matches": [...],
  "unique_count": 1,
  "total_matches": 5
}
```

## 📁 Cấu Trúc Thư Mục

```
face_embeddings/
├── docs/                    # Tài liệu
│   ├── README.md           # DeepFace docs
│   ├── README_PROJECT.md   # Project docs (file này)
│   ├── GIAI_THICH_TOC_DO.md
│   └── GPU_SETUP_GUIDE.md
├── requirements/            # Dependencies
│   ├── requirements.txt    # Main dependencies
│   ├── requirements-dev.txt
│   ├── requirements_additional.txt
│   └── requirements_local.txt
├── deepface/               # DeepFace library
├── face_db/                # Face database
├── face_service.py         # Main service
├── check_gpu.py           # GPU checker
├── benchmark_gpu.py       # Performance test
└── test_speed.html        # UI test
```

## 🎯 Tính Năng

✅ GPU acceleration với NVIDIA CUDA
✅ Lọc kết quả trùng lặp (chỉ hiển thị % cao nhất)
✅ Error handling thân thiện
✅ 2 endpoints: chính xác cao và nhanh
✅ Model Facenet512 (98.4% accuracy)

## 📈 Hiệu Suất

| Endpoint | Detector | Thời Gian | Độ Chính Xác |
|----------|----------|-----------|--------------|
| /find | RetinaFace | 12-15s | ⭐⭐⭐⭐⭐ |
| /find-fast | OpenCV | 4-6s | ⭐⭐⭐⭐ |

## 🔍 Kiểm Tra

```cmd
# Kiểm tra GPU
.venv\Scripts\python.exe check_gpu.py

# Test hiệu suất
.venv\Scripts\python.exe benchmark_gpu.py

# Rebuild cache
.venv\Scripts\python.exe rebuild_cache_gpu.py
```

## 📝 Lưu Ý

- Service tự động lọc kết quả trùng lặp
- Nếu không phát hiện khuôn mặt, trả về error thân thiện
- Sử dụng RetinaFace detector theo khuyến nghị của DeepFace
