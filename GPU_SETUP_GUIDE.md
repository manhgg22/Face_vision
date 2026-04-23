# Hướng Dẫn Cấu Hình GPU cho Face Recognition Service

## ✅ Trạng Thái: GPU ĐÃ HOẠT ĐỘNG

GPU của bạn (NVIDIA GeForce RTX 3050 Laptop) đã được cấu hình thành công!

## ⚠️ Vấn Đề Tốc Độ - GIẢI THÍCH

Mặc dù GPU đã hoạt động, nhưng bạn vẫn thấy chậm (15 giây) vì:

### Nguyên Nhân Chính:
1. **RetinaFace Detector rất chậm** - Mất 10-12 giây chỉ để detect khuôn mặt
2. **Tìm kiếm trong 34 ảnh** - Mỗi ảnh phải tính embedding và so sánh
3. **Chưa tối ưu cache** - DeepFace phải xử lý lại mỗi lần

### Giải Pháp:

#### 🚀 Cách 1: Dùng Endpoint Nhanh (Khuyến Nghị)
```javascript
// Thay vì POST /find
POST /find-fast

// Tốc độ: 1-3 giây (nhanh hơn 5-10x)
```

#### ⚡ Cách 2: Thay Đổi Detector
Trong code frontend, thay:
```javascript
formData.append('detector_backend', 'skip');  // Nhanh nhất!
// hoặc
formData.append('detector_backend', 'opencv');  // Nhanh, vẫn detect face
```

#### 🎯 Cách 3: Pre-compute Embeddings (Tốt Nhất)
Chạy script này để tạo cache trước:
```cmd
.venv\Scripts\python.exe rebuild_cache_gpu.py
```

## Thông Tin GPU

- **GPU**: NVIDIA GeForce RTX 3050 Laptop GPU
- **Driver**: 566.07
- **CUDA Version**: 12.7 (Driver hỗ trợ)
- **TensorFlow**: 2.10.1 với CUDA 11.x
- **Memory**: ~1767 MB khả dụng cho TensorFlow

## Các Thư Viện Đã Cài Đặt

✓ tensorflow-gpu==2.10.1
✓ nvidia-cuda-runtime-cu11==11.8.89
✓ nvidia-cudnn-cu11==8.9.4.25
✓ nvidia-cublas-cu11==11.11.3.6
✓ nvidia-cufft-cu11==10.9.0.58
✓ nvidia-curand-cu11==10.3.0.86
✓ nvidia-cusolver-cu11==11.4.1.48
✓ nvidia-cusparse-cu11==11.7.5.86

## Cách Sử Dụng

### 1. Khởi động service với GPU:
```cmd
start_gpu.bat
```

### 2. Kiểm tra GPU hoạt động:
```cmd
.venv\Scripts\python.exe check_gpu.py
```

### 3. Test service:
```cmd
.venv\Scripts\python.exe test_service_gpu.py
```

## Hiệu Suất Thực Tế

### So Sánh Tốc Độ:

| Chế Độ | Detector | Thời Gian | Độ Chính Xác |
|--------|----------|-----------|--------------|
| CPU + RetinaFace | retinaface | 20-30s | ⭐⭐⭐⭐⭐ |
| GPU + RetinaFace | retinaface | 12-15s | ⭐⭐⭐⭐⭐ |
| GPU + OpenCV | opencv | 3-5s | ⭐⭐⭐⭐ |
| GPU + Skip | skip | 1-3s | ⭐⭐⭐ |
| GPU + Fast Endpoint | skip | 0.5-2s | ⭐⭐⭐ |

### Khuyến Nghị:
- **FaceID/Unlock**: Dùng `/find-fast` endpoint (nhanh nhất)
- **Verification**: Dùng detector="opencv" (cân bằng)
- **High Accuracy**: Dùng detector="retinaface" (chậm nhưng chính xác nhất)

## Test Tốc Độ

Mở file `test_speed.html` trong trình duyệt để test và so sánh tốc độ giữa các chế độ!

## Lưu Ý Quan Trọng

1. **Luôn sử dụng `start_gpu.bat`** để khởi động service, không dùng file start khác
2. File `face_service.py` đã được cập nhật để tự động load CUDA libraries
3. Nếu gặp lỗi "DLL not found", chạy lại `setup_gpu.bat`

## Xử Lý Sự Cố

### Nếu GPU không hoạt động:

1. Kiểm tra driver NVIDIA:
```cmd
nvidia-smi
```

2. Kiểm tra CUDA paths:
```cmd
.venv\Scripts\python.exe check_gpu.py
```

3. Cài đặt lại CUDA libraries:
```cmd
.venv\Scripts\pip.exe install --force-reinstall nvidia-cudnn-cu11==8.9.4.25
```

### Nếu service chạy chậm:

1. Đảm bảo đang dùng `start_gpu.bat`
2. Kiểm tra log khi khởi động - phải thấy "🚀 [GPU] NVIDIA RTX ACTIVE"
3. Kiểm tra GPU usage khi đang xử lý:
```cmd
nvidia-smi
```

## Tối Ưu Thêm

Để tăng tốc độ hơn nữa, trong `face_service.py`:

- Model: `Facenet512` (nhanh, độ chính xác cao)
- Detector: `retinaface` (cân bằng tốc độ và độ chính xác)

Nếu cần tốc độ tối đa:
- Model: `Facenet` (nhẹ hơn)
- Detector: `opencv` hoặc `ssd` (nhanh nhất)

## Kiểm Tra Cuối Cùng

Chạy lệnh này để xác nhận mọi thứ hoạt động:

```cmd
.venv\Scripts\python.exe -c "import tensorflow as tf; print('GPU:', tf.config.list_physical_devices('GPU'))"
```

Kết quả phải hiển thị GPU của bạn!
