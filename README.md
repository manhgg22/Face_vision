# Face Recognition Service - GPU Accelerated

Dịch vụ nhận diện khuôn mặt sử dụng DeepFace với GPU NVIDIA RTX 3050.

## 🚀 Khởi Động Nhanh

### 1. Cài Đặt (Lần đầu tiên)
```cmd
SETUP.bat
```

### 2. Khởi Động Service
```cmd
START.bat
```

### 3. Mở Test UI
```
web/test_speed.html
```

## 📁 Cấu Trúc Project

```
face_embeddings/
├── SETUP.bat              # ⭐ Cài đặt lần đầu
├── START.bat              # ⭐ Khởi động service
├── face_service.py        # Service chính
│
├── scripts/               # Scripts và tools
│   ├── setup_gpu.bat     # Setup script
│   ├── start_gpu.bat     # Start script
│   ├── check_gpu.py      # Kiểm tra GPU
│   ├── benchmark_gpu.py  # Test hiệu suất
│   └── rebuild_cache_gpu.py  # Rebuild cache
│
├── web/                   # Web UI
│   ├── index.html        # Dashboard
│   └── test_speed.html   # Test speed UI
│
├── docs/                  # Tài liệu
│   ├── README_PROJECT.md
│   ├── GIAI_THICH_TOC_DO.md
│   ├── GPU_SETUP_GUIDE.md
│   └── FILE_EXPLANATIONS.md
│
├── requirements/          # Dependencies
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── requirements_additional.txt
│   └── requirements_local.txt
│
├── deepface/             # DeepFace library
├── face_db/              # Face database
└── face_temp_uploads/    # Temp uploads
```

## 🎯 Tính Năng

✅ GPU acceleration với NVIDIA CUDA  
✅ Model Facenet512 (98.4% accuracy)  
✅ Lọc kết quả trùng lặp  
✅ Error handling thân thiện  
✅ 2 endpoints: chính xác cao và nhanh  

## 📊 API Endpoints

### POST /find
Tìm kiếm với độ chính xác cao nhất (RetinaFace detector)
- Thời gian: 12-15 giây
- Độ chính xác: ⭐⭐⭐⭐⭐

### POST /find-fast
Tìm kiếm nhanh (OpenCV detector)
- Thời gian: 4-6 giây
- Độ chính xác: ⭐⭐⭐⭐

## 🔧 Scripts Hữu Ích

```cmd
# Kiểm tra GPU
.venv\Scripts\python.exe scripts\check_gpu.py

# Test hiệu suất
.venv\Scripts\python.exe scripts\benchmark_gpu.py

# Rebuild cache (sau khi thêm/xóa ảnh)
.venv\Scripts\python.exe scripts\rebuild_cache_gpu.py
```

## 📚 Tài Liệu

- [README_PROJECT.md](docs/README_PROJECT.md) - Tài liệu chi tiết
- [GIAI_THICH_TOC_DO.md](docs/GIAI_THICH_TOC_DO.md) - Giải thích tốc độ
- [GPU_SETUP_GUIDE.md](docs/GPU_SETUP_GUIDE.md) - Hướng dẫn GPU
- [FILE_EXPLANATIONS.md](docs/FILE_EXPLANATIONS.md) - Giải thích các file

## 💡 Lưu Ý

- Service chạy trên port 8001
- Database: `face_db/` (thêm ảnh vào đây)
- Temp uploads: `face_temp_uploads/` (tự động xóa)
- Cache: `*.pkl` files (tự động tạo)

## 📈 Hiệu Suất

| Endpoint | Detector | Thời Gian | Độ Chính Xác |
|----------|----------|-----------|--------------|
| /find | RetinaFace | 12-15s | ⭐⭐⭐⭐⭐ |
| /find-fast | OpenCV | 4-6s | ⭐⭐⭐⭐ |

## 🔍 Troubleshooting

Nếu gặp vấn đề, xem [GPU_SETUP_GUIDE.md](docs/GPU_SETUP_GUIDE.md)
