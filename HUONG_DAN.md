# 📖 HƯỚNG DẪN SỬ DỤNG

## 🚀 BẮT ĐẦU NHANH

### Bước 1: Cài Đặt (Chỉ làm 1 lần)
```cmd
SETUP.bat
```
Chờ khoảng 5-10 phút để cài đặt xong.

### Bước 2: Khởi Động Service
```cmd
START.bat
```
Service sẽ chạy trên: `http://localhost:8001`

### Bước 3: Test
Mở file `web/test_speed.html` trong trình duyệt.

---

## 📁 THÊM KHUÔN MẶT VÀO DATABASE

1. Vào folder `face_db/`
2. Tạo folder mới với tên người (ví dụ: `Minh`)
3. Thêm ảnh khuôn mặt vào folder đó
4. Chạy rebuild cache:
```cmd
.venv\Scripts\python.exe scripts\rebuild_cache_gpu.py
```

**Ví dụ:**
```
face_db/
├── Minh/
│   ├── img1.jpg
│   └── img2.jpg
└── An/
    └── img1.jpg
```

---

## 🔧 CÁC LỆNH HỮU ÍCH

### Kiểm tra GPU
```cmd
.venv\Scripts\python.exe scripts\check_gpu.py
```

### Test hiệu suất
```cmd
.venv\Scripts\python.exe scripts\benchmark_gpu.py
```

### Rebuild cache
```cmd
.venv\Scripts\python.exe scripts\rebuild_cache_gpu.py
```

---

## 🌐 SỬ DỤNG API

### Endpoint 1: /find (Chính xác cao)
```javascript
const formData = new FormData();
formData.append('image', imageFile);

const response = await fetch('http://localhost:8001/find', {
    method: 'POST',
    body: formData
});

const result = await response.json();
console.log(result);
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
  "match_count": 1
}
```

### Endpoint 2: /find-fast (Nhanh hơn)
```javascript
const response = await fetch('http://localhost:8001/find-fast', {
    method: 'POST',
    body: formData
});
```

---

## ❓ XỬ LÝ LỖI

### Lỗi: Không tìm thấy GPU
```cmd
# Kiểm tra GPU
nvidia-smi

# Kiểm tra trong Python
.venv\Scripts\python.exe scripts\check_gpu.py
```

### Lỗi: Service chạy chậm
- Đảm bảo đang dùng `START.bat`
- Kiểm tra log phải thấy "🚀 [GPU] NVIDIA RTX ACTIVE"

### Lỗi: Không phát hiện khuôn mặt
- Đảm bảo ảnh có khuôn mặt rõ ràng
- Thử dùng endpoint `/find-fast` (detector khác)

---

## 📚 TÀI LIỆU CHI TIẾT

- [README.md](README.md) - Tổng quan
- [docs/GIAI_THICH_TOC_DO.md](docs/GIAI_THICH_TOC_DO.md) - Giải thích tốc độ
- [docs/GPU_SETUP_GUIDE.md](docs/GPU_SETUP_GUIDE.md) - Hướng dẫn GPU
- [docs/FILE_EXPLANATIONS.md](docs/FILE_EXPLANATIONS.md) - Giải thích các file

---

## 💡 MẸO

1. **Tốc độ nhanh nhất:** Dùng endpoint `/find-fast`
2. **Độ chính xác cao nhất:** Dùng endpoint `/find`
3. **Thêm ảnh mới:** Nhớ chạy `rebuild_cache_gpu.py`
4. **Test UI:** Mở `web/test_speed.html` để test trực quan

---

## 🎯 CẤU TRÚC FOLDER CHÍNH

```
📁 face_embeddings/
├── 🚀 SETUP.bat          # Cài đặt lần đầu
├── 🚀 START.bat          # Khởi động service
├── 📖 HUONG_DAN.md       # File này
├── 📖 README.md          # Tổng quan
│
├── 📁 scripts/           # Scripts và tools
├── 📁 web/               # Web UI
├── 📁 docs/              # Tài liệu
├── 📁 requirements/      # Dependencies
├── 📁 face_db/           # ⭐ Database (thêm ảnh vào đây)
└── 📁 deepface/          # DeepFace library
```

---

## ✅ CHECKLIST

- [ ] Đã chạy `SETUP.bat`
- [ ] Đã thêm ảnh vào `face_db/`
- [ ] Đã chạy `rebuild_cache_gpu.py`
- [ ] Đã chạy `START.bat`
- [ ] Đã test với `web/test_speed.html`

---

**Chúc bạn sử dụng thành công! 🎉**
