# FaceID Intelligence - Standalone Face Recognition Service

Hệ thống nhận diện khuôn mặt và quản lý danh tính mạnh mẽ dựa trên thư viện DeepFace, được tối ưu hóa cho hiệu suất và tính ổn định. Hệ thống cung cấp cả REST API và giao diện Web Dashboard tích hợp.

![Dashboard Preview](https://img.shields.io/badge/FaceID-Pro-blue?style=for-the-badge)
![DeepFace](https://img.shields.io/badge/Powered%20by-DeepFace-orange?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/API-FastAPI-green?style=for-the-badge)

## 🚀 Tính năng chính

- **Nhận diện khuôn mặt**: Tìm kiếm danh tính trong cơ sở dữ liệu (`face_db`) với độ chính xác cao bằng model `Facenet512` và detector `retinaface`.
- **Web Dashboard**: Giao diện người dùng trực quan để thực hiện nhận diện, xem danh sách cơ sở dữ liệu và quản lý cache.
- **REST API**: Dễ dàng tích hợp với các ứng dụng khác (Web, App, Bot).
- **Xử lý thông minh**: Tự động chuyển đổi định dạng ảnh (WebP -> JPG) và xử lý đường dẫn tối ưu.
- **Log Debug**: Cung cấp thông tin chi tiết về khoảng cách (distance) và gợi ý kết quả gần đúng nhất.

## 📁 Cấu trúc thư mục

- `face_service.py`: Script chính chạy dịch vụ FastAPI.
- `index.html`: Giao diện Dashboard tích hợp.
- `face_db/`: Thư mục chứa cơ sở dữ liệu ảnh (được tổ chức theo thư mục tên người).
- `start_face_service.bat`: File chạy nhanh dịch vụ trên Windows.

## 🛠️ Cài đặt

1. **Yêu cầu**: Python 3.9+
2. **Cài đặt thư viện**:
   ```powershell
   pip install deepface fastapi uvicorn pillow
   ```
3. **Cấu trúc Database**:
   Chuẩn bị ảnh của bạn trong thư mục `face_db` theo định dạng:
   ```text
   face_db/
   ├── Son_Tung/
   │   ├── img1.jpg
   │   └── img2.jpg
   └── Do_Mixi/
       └── image.png
   ```
   *Lưu ý: Tránh đặt tên thư mục có dấu tiếng Việt để đảm bảo độ ổn định.*

## 📖 Hướng dẫn sử dụng

### Khởi chạy dịch vụ
Chạy file `.bat` hoặc lệnh:
```powershell
python face_service.py
```

### Sử dụng Giao diện Web
Truy cập: **[http://localhost:8001](http://localhost:8001)**

1. **Identify**: Kéo thả ảnh vào vùng nhận diện để tìm tên người trong Database.
2. **DB List**: Xem danh sách các cá nhân đã được hệ thống học.
3. **Purge Cache**: Nhấn xóa cache khi bạn có sự thay đổi (thêm/xóa ảnh) trong thư mục `face_db`.

### API Endpoints
- `GET /health`: Kiểm tra trạng thái dịch vụ.
- `POST /find`: Tìm kiếm danh tính (gửi ảnh qua form-data).
- `POST /register`: Đăng ký khuôn mặt mới.
- `GET /db/purge-cache`: Xóa sạch cache `.pkl`.

## 🛡️ License
Dự án được phát triển dựa trên DeepFace (MIT License). 

---
*Phát triển bởi manhgg22*
