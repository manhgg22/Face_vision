# 📁 CẤU TRÚC PROJECT

## 🎯 ROOT FOLDER (Gọn gàng, dễ nhìn)

```
face_embeddings/
│
├── 🚀 SETUP.bat              # ⭐ Cài đặt lần đầu
├── 🚀 START.bat              # ⭐ Khởi động service
├── 📖 HUONG_DAN.md           # ⭐ Hướng dẫn tiếng Việt
├── 📖 README.md              # Tổng quan project
│
├── 🐍 face_service.py        # Service chính (API)
│
├── 📁 scripts/               # Scripts và tools
├── 📁 web/                   # Web UI
├── 📁 docs/                  # Tài liệu
├── 📁 requirements/          # Dependencies
├── 📁 face_db/               # ⭐ Database (thêm ảnh vào đây)
│
├── 📁 deepface/              # DeepFace library
├── 📁 .venv/                 # Virtual environment
│
└── ⚙️ Config files           # .gitignore, .pylintrc, etc.
```

---

## 📁 CHI TIẾT CÁC FOLDER

### 📁 scripts/ - Scripts và Tools
```
scripts/
├── setup_gpu.bat           # Setup script (gọi bởi SETUP.bat)
├── start_gpu.bat           # Start script (gọi bởi START.bat)
├── check_gpu.py            # Kiểm tra GPU
├── benchmark_gpu.py        # Test hiệu suất
└── rebuild_cache_gpu.py    # Rebuild cache
```

**Mục đích:** Chứa tất cả scripts test, check, setup để root folder gọn gàng.

---

### 📁 web/ - Web UI
```
web/
├── index.html              # Dashboard
└── test_speed.html         # Test speed UI
```

**Mục đích:** Chứa tất cả file HTML/UI.

**Cách dùng:** Mở `web/test_speed.html` trong browser để test.

---

### 📁 docs/ - Tài Liệu
```
docs/
├── README.md               # DeepFace docs gốc
├── README_PROJECT.md       # Tài liệu project
├── GIAI_THICH_TOC_DO.md   # Giải thích tốc độ
├── GPU_SETUP_GUIDE.md     # Hướng dẫn GPU
├── FILE_EXPLANATIONS.md   # Giải thích các file
└── STRUCTURE.md           # File này
```

**Mục đích:** Tất cả tài liệu ở một chỗ.

---

### 📁 requirements/ - Dependencies
```
requirements/
├── requirements.txt        # Main dependencies
├── requirements-dev.txt    # Dev dependencies
├── requirements_additional.txt  # Optional
└── requirements_local.txt  # Docker dependencies
```

**Mục đích:** Tổ chức các file requirements.

---

### 📁 face_db/ - Database ⭐
```
face_db/
├── Minh/
│   ├── img1.jpg
│   └── img2.jpg
├── An/
│   └── img1.jpg
└── *.pkl                   # Cache files (tự động tạo)
```

**Mục đích:** Chứa ảnh khuôn mặt để nhận diện.

**Cách dùng:**
1. Tạo folder mới với tên người
2. Thêm ảnh vào folder đó
3. Chạy `rebuild_cache_gpu.py`

---

### 📁 face_temp_uploads/ - Temp Uploads
```
face_temp_uploads/
└── (ảnh tạm thời, tự động xóa)
```

**Mục đích:** Chứa ảnh upload tạm thời, tự động xóa sau khi xử lý.

---

### 📁 deepface/ - DeepFace Library
```
deepface/
├── DeepFace.py
├── models/
├── modules/
└── ...
```

**Mục đích:** Source code của thư viện DeepFace (không nên sửa).

---

## 🎯 FILES QUAN TRỌNG Ở ROOT

### ⭐ Files Người Dùng Cần Biết

1. **SETUP.bat** - Cài đặt lần đầu
2. **START.bat** - Khởi động service
3. **HUONG_DAN.md** - Hướng dẫn tiếng Việt
4. **README.md** - Tổng quan

### 🐍 Files Python

5. **face_service.py** - Service chính (API endpoints)

### ⚙️ Files Config (Không cần sửa)

6. **.gitignore** - Git ignore
7. **.pylintrc** - Pylint config
8. **mypy.ini** - MyPy config
9. **Makefile** - Build commands
10. **setup.py** - Package setup
11. **package_info.json** - Version
12. **Dockerfile** - Docker config
13. **entrypoint.sh** - Docker entrypoint
14. **LICENSE** - MIT License
15. **CITATION.cff** - Citation info

---

## 📊 SO SÁNH TRƯỚC VÀ SAU

### ❌ TRƯỚC (Lộn xộn)
```
face_embeddings/
├── check_gpu.py
├── benchmark_gpu.py
├── rebuild_cache_gpu.py
├── setup_gpu.bat
├── start_gpu.bat
├── index.html
├── test_speed.html
├── README.md
├── GIAI_THICH_TOC_DO.md
├── GPU_SETUP_GUIDE.md
├── requirements.txt
├── requirements-dev.txt
├── requirements_additional.txt
├── .gitignore
├── .pylintrc
├── mypy.ini
├── Makefile
├── setup.py
├── Dockerfile
├── entrypoint.sh
├── LICENSE
├── CITATION.cff
└── ... (20+ files ở root)
```

### ✅ SAU (Gọn gàng)
```
face_embeddings/
├── 🚀 SETUP.bat
├── 🚀 START.bat
├── 📖 HUONG_DAN.md
├── 📖 README.md
├── 🐍 face_service.py
│
├── 📁 scripts/      (5 files)
├── 📁 web/          (2 files)
├── 📁 docs/         (6 files)
├── 📁 requirements/ (4 files)
├── 📁 face_db/
├── 📁 deepface/
│
└── ⚙️ Config files (10 files)
```

**Kết quả:**
- Root folder chỉ còn 4 files quan trọng + 1 service file
- Tất cả scripts, docs, requirements đã được tổ chức vào folders
- Dễ nhìn, dễ tìm, dễ sử dụng!

---

## 💡 LỢI ÍCH

✅ **Gọn gàng:** Root folder chỉ còn 15 items thay vì 30+  
✅ **Dễ tìm:** Mọi thứ được phân loại rõ ràng  
✅ **Dễ dùng:** Chỉ cần biết SETUP.bat và START.bat  
✅ **Chuyên nghiệp:** Cấu trúc giống các project lớn  
✅ **Giữ nguyên chức năng:** Tất cả vẫn hoạt động bình thường  

---

## 🚀 CÁCH SỬ DỤNG

### Lần đầu tiên:
```cmd
SETUP.bat
```

### Mỗi lần khởi động:
```cmd
START.bat
```

### Test:
```
Mở web/test_speed.html
```

### Thêm ảnh:
```
1. Thêm vào face_db/
2. Chạy: .venv\Scripts\python.exe scripts\rebuild_cache_gpu.py
```

---

**Đơn giản, gọn gàng, chuyên nghiệp! 🎉**
