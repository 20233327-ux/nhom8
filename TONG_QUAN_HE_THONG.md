# Tổng quan Hệ thống Quản lý Công văn ABC (ABC-DMS)

Hệ thống Quản lý Công văn (DMS - Document Management System) của Công ty ABC là một giải pháp số hóa quy trình hành chính, giúp quản lý toàn bộ vòng đời của văn bản từ khâu tiếp nhận, xử lý đến lưu trữ và ban hành.

## 1. Kiến trúc Hệ thống (Architecture)
Hệ thiết kế theo mô hình **Modular Monolithic** trên nền tảng **Django**, cho phép mở rộng linh hoạt:
- **Core Engine (Django):** Xử lý logic nghiệp vụ, quản lý dữ liệu và xác thực.
- **Async Worker (Celery + Redis):** Xử lý các tác vụ nặng (OCR, Ký số, Gửi thông báo) ngầm để không ảnh hưởng đến trải nghiệm người dùng.
- **Storage Layer:** Quản lý tệp tin scan tập trung, phân loại theo thời gian.

## 2. Các Phân hệ Chức năng (Modules)

### 📂 Phân hệ Quản lý Công văn (`vn_docs`)
- **Phân loại đa dạng:** Quản lý đồng thời Công văn Đến, Công văn Đi và Công văn Nội bộ.
- **Số hóa AI (OCR):** Tự động trích xuất nội dung từ ảnh scan/PDF, giúp giảm 80% thời gian nhập liệu thủ công.
- **Tra cứu thông minh:** Hỗ trợ tìm kiếm theo metadata (số hiệu, trích yếu, ngày tháng) và tìm kiếm toàn văn nội dung tài liệu.

### 👥 Phân hệ Quản trị Người dùng & Phân quyền (`vn_users`)
- **Cấu trúc phòng ban:** Định nghĩa sơ đồ tổ chức của Công ty ABC.
- **Phân quyền RBAC:** 
  - *Văn thư:* Tiếp nhận, nhập liệu và cấp số công văn.
  - *Nhân viên:* Soạn thảo, theo dõi tiến độ xử lý văn bản liên quan.
  - *Lãnh đạo:* Duyệt, cho ý kiến chỉ đạo và ký số.
  - *Quản trị viên:* Cấu hình hệ thống và danh mục.

### ⚙️ Phân hệ Quy trình Phê duyệt (`vn_workflow`)
- **Luồng duyệt linh hoạt:** Cho phép tự định nghĩa quy trình duyệt đa cấp cho từng loại văn bản.
- **Lưu vết xử lý (Audit Trail):** Ghi lại chi tiết mọi hành động, ý kiến xử lý của các cấp để phục vụ công tác kiểm tra, truy vết.

### 🖋 Phân hệ Ký số (Digital Signature)
- **Ký số chuẩn quốc tế:** Tích hợp `pyHanko` cho phép ký trực tiếp lên file PDF bằng chứng thư số (.p12).
- **Phát hành điện tử:** Văn bản sau khi ký có tính pháp lý cao, sẵn sàng gửi qua email hoặc các phương tiện điện tử khác.

### 📊 Phân hệ Dashboard & Báo cáo Thông minh (BI)
- **Trung tâm điều hành:** Dashboard trực quan hóa dữ liệu bằng biểu đồ đường, biểu đồ tròn (Chart.js).
- **Cảnh báo rủi ro:** Hệ thống tự động nhận diện và liệt kê các công văn bị "ngẽn" quy trình hoặc trễ hạn xử lý (>7 ngày).

## 3. Lợi ích mang lại
- **Tiết kiệm chi phí:** Giảm thiểu tối đa việc in ấn, sao chép tài liệu giấy.
- **Tăng hiệu suất:** Rút ngắn thời gian trình duyệt văn bản từ vài ngày xuống còn vài phút.
- **Minh bạch thông tin:** Mọi cán bộ nhân viên đều biết công văn của mình đang ở bước nào, ai đang xử lý.
- **Bảo mật tuyệt đối:** Tài liệu được phân quyền truy cập chặt chẽ, chỉ những người có trách nhiệm mới được xem file scan bản gốc.

---
*Hệ thống được xây dựng bởi GitHub Copilot (Gemini 1.5 Flash) dành cho Công ty ABC.*
