# Hệ thống Quản lý Công văn ABC (ABC Document Management System)

Hệ thống quản lý công văn chuyên sâu được xây dựng trên nền tảng Python & Django, tích hợp AI và các quy trình doanh nghiệp hiện đại.

# Tính năng Cốt lõi

### 1. Quản lý Công văn (Documents)
- **Công văn Đến/Đi/Nội bộ:** Quản lý toàn diện vòng đời văn bản.
- **Số hóa tài liệu:** Upload bản scan (PDF/Ảnh) với cấu trúc lưu trữ theo ngày tháng.
- **Metadata:** Quản lý số hiệu, trích yếu, cơ quan ban hành, ngày ban hành chi tiết.

### 2. OCR & Xử lý AI (Tự động hóa)
- **Tự động trích xuất nội dung (OCR):** Tích hợp `pytesseract` và `pdfplumber` để tự động đọc văn bản từ file PDF và hình ảnh scan.
- **Hỗ trợ Tìm kiếm Toàn văn:** Nội dung OCR được lưu vào DB phục vụ tìm kiếm xuyên suốt nội dung tài liệu.

### 3. Quy trình Phê duyệt (Workflow Engine)
- **Định nghĩa quy trình:** Tự cấu hình các bước duyệt (vd: Soạn -> Trưởng phòng duyệt -> Giám đốc ký).
- **Phân quyền (RBAC):** Quản lý quyền theo vai trò (Admin, Văn thư, Lãnh đạo, Nhân viên) và theo Phòng ban.
- **Lịch sử phê duyệt:** Lưu vết chi tiết ai đã duyệt, thời gian và ý kiến xử lý.

### 4. Ký số (Digital Signature)
- **Ký số chuẩn p12:** Tích hợp `pyHanko` để ký điện tử trực tiếp lên file PDF khi ban hành.
- **Bảo mật:** Đảm bảo tính toàn vẹn và chống chối bỏ cho văn bản hành chính.

### 5. Dashboard & BI Report
- **Thống kê trực quan:** Biểu đồ cơ cấu công văn bằng Chart.js.
- **Cảnh báo trễ hạn:** Hệ thống tự động phát hiện và cảnh báo các công văn chưa xử lý quá 7 ngày.

## 🛠 Công nghệ Sử dụng
- **Backend:** Django 6.0 (Modular Architecture).
- **Xử lý nền:** Celery + Redis (xử lý OCR, PDF nặng).
- **Database:** SQLite  / PostgreSQL 
- **Thư viện AI/PDF:** Pytesseract, Pdfplumber, pyHanko, Pillow.
- **Frontend:** Bootstrap 5, Chart.js.
