# Hướng Dẫn Cấu Hình GPU cho Face Recognition Service

## ✅ Trạng Thái: GPU ĐÃ HOẠT ĐỘNG

GPU của bạn (NVIDIA GeForce RTX 3050 Laptop) đã được cấu hình thành công!

## 📋 Cấu Hình Hiện Tại (Theo Tài Liệu DeepFace)

- **Model**: Facenet512 (98.4% accuracy - cao nhất)
- **Detector**: RetinaFace (chính xác nhất)
- **Endpoint `/find`**: RetinaFace detector (12-15s, độ chính xác cao nhất)
- **Endpoint `/find-fast`**: OpenCV detector (4-6s, cân bằng tốc độ và độ chính xác)

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

### 3. Test hiệu suất:
```cmd
.venv\Scripts\python.exe benchmark_gpu.py
```

## Hiệu Suất Thực Tế

### So Sánh Tốc Độ:

| Chế Độ | Detector | Thời Gian | Độ Chính Xác |
|--------|----------|-----------|--------------|
| CPU + RetinaFace | retinaface | 20-30s | ⭐⭐⭐⭐⭐ |
| GPU + RetinaFace | retinaface | 12-15s | ⭐⭐⭐⭐⭐ |
| GPU + OpenCV | opencv | 4-6s | ⭐⭐⭐⭐ |

### Khuyến Nghị (Theo Tài Liệu DeepFace):
- **Production/High Accuracy**: Dùng `/find` endpoint với RetinaFace (chính xác nhất)
- **Balanced**: Dùng `/find-fast` endpoint với OpenCV (cân bằng tốc độ và độ chính xác)

## Test Tốc Độ

Mở file `test_speed.html` trong trình duyệt để test và so sánh tốc độ giữa các chế độ!

## Lưu Ý Quan Trọng

1. **Luôn sử dụng `start_gpu.bat`** để khởi động service
2. File `face_service.py` đã được cấu hình theo tài liệu DeepFace
3. Service tự động lọc kết quả trùng lặp (chỉ hiển thị % cao nhất cho mỗi người)

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

## Kiểm Tra Cuối Cùng

Chạy lệnh này để xác nhận GPU hoạt động:

```cmd
.venv\Scripts\python.exe -c "import tensorflow as tf; print('GPU:', tf.config.list_physical_devices('GPU'))"
```

Kết quả phải hiển thị GPU của bạn!
