# Giải Thích Các File Trong Project

## 📁 Folders

### `requirements/` - Thư mục chứa dependencies
Chứa tất cả các file requirements cho project

### `docs/` - Thư mục tài liệu
Chứa tất cả file markdown documentation

### `deepface/` - Thư viện DeepFace
Source code của thư viện DeepFace (không nên sửa)

### `face_db/` - Database khuôn mặt
Thư mục chứa ảnh khuôn mặt để nhận diện
```
face_db/
├── Minh/
│   ├── img1.jpg
│   └── img2.jpg
└── An/
    └── img1.jpg
```

### `face_temp_uploads/` - Thư mục tạm
Chứa ảnh upload tạm thời, tự động xóa sau khi xử lý

---

## 🐍 Python Files

### `face_service.py` - ⭐ SERVICE CHÍNH
**Mục đích:** API service cho face recognition
**Chức năng:**
- Endpoint `/find`: Tìm kiếm với RetinaFace (chính xác cao)
- Endpoint `/find-fast`: Tìm kiếm nhanh với OpenCV
- Tự động load CUDA libraries cho GPU
- Lọc kết quả trùng lặp (chỉ hiển thị % cao nhất)
- Error handling thân thiện

**Khi nào dùng:** Đây là file chính để chạy service
```cmd
python face_service.py
```

---

### `check_gpu.py` - Kiểm tra GPU
**Mục đích:** Kiểm tra GPU có hoạt động không
**Chức năng:**
- Hiển thị thông tin GPU
- Test tính toán trên GPU
- Kiểm tra CUDA paths

**Khi nào dùng:** Khi muốn kiểm tra GPU
```cmd
.venv\Scripts\python.exe check_gpu.py
```

---

### `benchmark_gpu.py` - Test hiệu suất
**Mục đích:** So sánh tốc độ giữa các detector
**Chức năng:**
- Test RetinaFace detector (chính xác nhất)
- Test OpenCV detector (cân bằng)
- Hiển thị thời gian và speedup

**Khi nào dùng:** Khi muốn test hiệu suất
```cmd
.venv\Scripts\python.exe benchmark_gpu.py
```

---

### `rebuild_cache_gpu.py` - Rebuild cache
**Mục đích:** Xóa và tạo lại cache embeddings
**Chức năng:**
- Xóa tất cả file .pkl (cache cũ)
- Tính lại embeddings cho tất cả ảnh
- Tạo cache mới

**Khi nào dùng:** Khi thêm/xóa ảnh trong database
```cmd
.venv\Scripts\python.exe rebuild_cache_gpu.py
```

---

### `setup.py` - Setup DeepFace
**Mục đích:** File cài đặt cho thư viện DeepFace
**Chức năng:**
- Định nghĩa metadata của package
- Đọc dependencies từ requirements.txt
- Cài đặt DeepFace như một package

**Khi nào dùng:** Khi cài đặt DeepFace từ source
```cmd
pip install -e .
```

---

## 🪟 Batch Files (Windows)

### `setup_gpu.bat` - Cài đặt GPU
**Mục đích:** Cài đặt TensorFlow GPU và CUDA libraries
**Chức năng:**
- Tạo virtual environment
- Cài đặt tensorflow-gpu==2.10.1
- Cài đặt CUDA 11.x libraries
- Cài đặt dependencies

**Khi nào dùng:** Lần đầu setup project
```cmd
setup_gpu.bat
```

---

### `start_gpu.bat` - Khởi động service
**Mục đích:** Khởi động face recognition service với GPU
**Chức năng:**
- Activate virtual environment
- Chạy face_service.py
- Service chạy trên port 8001

**Khi nào dùng:** Mỗi khi muốn khởi động service
```cmd
start_gpu.bat
```

---

## 🌐 HTML Files

### `index.html` - Dashboard
**Mục đích:** Dashboard chính của service
**Chức năng:**
- Hiển thị thông tin service
- UI để test các endpoint

**Khi nào dùng:** Mở trong browser khi service đang chạy
```
http://localhost:8001/
```

---

### `test_speed.html` - Test tốc độ
**Mục đích:** So sánh tốc độ giữa các endpoint
**Chức năng:**
- Upload ảnh
- Test endpoint `/find` (RetinaFace)
- Test endpoint `/find-fast` (OpenCV)
- Hiển thị thời gian và kết quả

**Khi nào dùng:** Khi muốn test và so sánh tốc độ
```
Mở file trong browser
```

---

## ⚙️ Config Files

### `.gitignore` - Git ignore
**Mục đích:** Chỉ định file/folder không commit lên Git
**Nội dung:**
- `.venv/` - Virtual environment
- `*.pkl` - Cache files
- `face_temp_uploads/` - Temp uploads
- `face_db/` - Database (có thể chứa ảnh cá nhân)
- `__pycache__/` - Python cache

**Khi nào dùng:** Tự động, không cần chỉnh sửa

---

### `.gitattributes` - Git attributes
**Mục đích:** Cấu hình Git attributes
**Nội dung:**
- `*.ipynb linguist-vendored` - Đánh dấu Jupyter notebooks là vendored code

**Khi nào dùng:** Tự động, không cần chỉnh sửa

---

### `.pylintrc` - Pylint config
**Mục đích:** Cấu hình Pylint (Python linter)
**Chức năng:**
- Kiểm tra code quality
- Enforce coding standards
- Tắt một số warnings không cần thiết

**Khi nào dùng:** Khi chạy linting
```cmd
python -m pylint deepface/
```

---

### `mypy.ini` - MyPy config
**Mục đích:** Cấu hình MyPy (type checker)
**Chức năng:**
- Kiểm tra type hints
- Strict mode enabled
- Ignore missing imports

**Khi nào dùng:** Khi chạy type checking
```cmd
mypy deepface/
```

---

### `Makefile` - Build commands
**Mục đích:** Định nghĩa các lệnh build/test
**Commands:**
- `make test` - Chạy unit tests
- `make integration-test` - Chạy integration tests
- `make lint` - Chạy pylint và mypy
- `make coverage` - Chạy test coverage

**Khi nào dùng:** Khi develop DeepFace library
```cmd
make lint
```

---

### `package_info.json` - Package version
**Mục đích:** Lưu version của DeepFace
**Nội dung:**
```json
{
    "version": "0.0.99"
}
```

**Khi nào dùng:** Được đọc bởi setup.py

---

## 🐳 Docker Files

### `Dockerfile` - Docker image
**Mục đích:** Build Docker image cho DeepFace
**Chức năng:**
- Base image: Python 3.8.12
- Cài đặt system dependencies
- Copy source code
- Cài đặt Python dependencies
- Expose port 5000

**Khi nào dùng:** Khi muốn chạy trong Docker
```cmd
docker build -t deepface .
docker run -p 5000:5000 deepface
```

---

### `entrypoint.sh` - Docker entrypoint
**Mục đích:** Script khởi động cho Docker container
**Chức năng:**
- Khởi động gunicorn server
- Chạy DeepFace API

**Khi nào dùng:** Tự động chạy khi start Docker container

---

## 📄 Documentation Files

### `LICENSE` - MIT License
**Mục đích:** Giấy phép sử dụng
**Nội dung:** MIT License - cho phép sử dụng tự do

---

### `CITATION.cff` - Citation info
**Mục đích:** Thông tin để cite DeepFace trong nghiên cứu
**Nội dung:**
- Tác giả: Sefik Ilkin Serengil
- DOI: 10.35378/gujs.1794891
- Journal: Gazi University Journal of Science

**Khi nào dùng:** Khi cite DeepFace trong paper

---

## 📋 Tóm Tắt - Files Quan Trọng

### ⭐ CẦN DÙNG THƯỜNG XUYÊN:
1. `start_gpu.bat` - Khởi động service
2. `face_service.py` - Service chính
3. `test_speed.html` - Test UI
4. `check_gpu.py` - Kiểm tra GPU

### 🔧 DÙNG KHI CẦN:
1. `setup_gpu.bat` - Setup lần đầu
2. `benchmark_gpu.py` - Test hiệu suất
3. `rebuild_cache_gpu.py` - Rebuild cache

### 📚 KHÔNG CẦN SỬA:
1. `.gitignore`, `.gitattributes` - Git config
2. `.pylintrc`, `mypy.ini` - Linting config
3. `Makefile` - Build commands (cho dev)
4. `setup.py` - Package setup
5. `Dockerfile`, `entrypoint.sh` - Docker
6. `LICENSE`, `CITATION.cff` - Legal/Citation

### ❌ KHÔNG NÊN XÓA:
Tất cả các file đều có mục đích riêng. Nếu không dùng Docker thì có thể bỏ qua `Dockerfile` và `entrypoint.sh`, nhưng không nên xóa.
