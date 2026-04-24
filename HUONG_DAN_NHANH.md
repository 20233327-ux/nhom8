# 🚀 Hướng dẫn Nhanh - ABC Document Management System

## 📋 Mục lục
1. [Cài đặt và chạy](#-cài-đặt-và-chạy)
2. [Tài khoản mặc định](#-tài-khoản-mặc-định)
3. [Hướng dẫn sử dụng bằng Web](#-hướng-dẫn-sử-dụng-bằng-web)
4. [Hướng dẫn sử dụng Admin Panel](#-hướng-dẫn-sử-dụng-admin-panel)
5. [Các vai trò và quyền hạn](#-các-vai-trò-và-quyền-hạn)

---

## 💻 Cài đặt và chạy

### Bước 1: Cấu hình môi trường Python
```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Trên Windows:
venv\Scripts\activate

# Trên Linux/Mac:
source venv/bin/activate
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy migrations
```bash
python manage.py migrate
```

### Bước 4: Tạo superuser (Admin)
```bash
python manage.py createsuperuser
# Nhập thông tin:
# Username: admin
# Email: admin@abc.com
# Password: (nhập mật khẩu của bạn)
# Password (again): (xác nhận mật khẩu)
```

### Bước 5: Chạy server
```bash
python manage.py runserver
```

Server sẽ chạy tại: **http://127.0.0.1:8000/**

---

## 👤 Tài khoản mặc định

### Đăng nhập qua Web Interface
- **URL**: http://127.0.0.1:8000/auth/login/
- **Tài khoản Admin**: 
  - Username: `admin`
  - Password: (tự nhập khi tạo superuser)

### Hoặc sử dụng Django Shell
```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
User = get_user_model()

# Tạo người dùng test
user1 = User.objects.create_user(
    username='staff_user',
    email='staff@abc.com',
    password='secure123',
    role='staff'  # Vai trò: staff, clerk, manager, admin
)

user2 = User.objects.create_user(
    username='manager_user',
    email='manager@abc.com',
    password='secure123',
    role='manager'
)

user3 = User.objects.create_user(
    username='clerk_user',
    email='clerk@abc.com',
    password='secure123',
    role='clerk'
)
```

---

## 🌐 Hướng dẫn sử dụng bằng Web

### 1. Đăng nhập
- Truy cập: http://127.0.0.1:8000/auth/login/
- Nhập tên đăng nhập và mật khẩu
- Hệ thống sẽ tự động chuyển hướng đến dashboard tương ứng với vai trò

### 2. Dashboard Nhân viên (`/auth/dashboard/staff/`)
**Dành cho**: Nhân viên bình thường
- ✅ Xem công văn của mình
- ✅ Xem công văn chờ phê duyệt
- ✅ Xem thống kê cơ bản

**Chức năng**: Xem thống kê, công văn của tôi, công văn chờ duyệt

### 3. Dashboard Lãnh đạo/Văn thư (`/auth/dashboard/manager/`)
**Dành cho**: Lãnh đạo, Văn thưa
- ✅ Xem công văn chờ ký/duyệt
- ✅ Duyệt/từ chối công văn
- ✅ Xem lịch sử duyệt

**Chức năng**: Công văn chờ duyệt, thống kê, duyệt công văn

### 4. Dashboard Admin (`/auth/dashboard/admin/`)
**Dành cho**: Quản trị viên hệ thống
- ✅ Xem thống kê toàn hệ thống
- ✅ Xem người dùng mới
- ✅ Xem công văn mới
- ✅ Quản lý quy trình workflow

**Chức năng**: Thống kê, người dùng, công văn, quy trình

---

## 🔧 Hướng dẫn sử dụng Admin Panel

### 1. Truy cập Admin
- URL: http://127.0.0.1:8000/admin/
- Đăng nhập với tài khoản superuser (admin)

### 2. Quản lý Người dùng
**Đường dẫn**: Admin → Users
- Tạo người dùng mới
- Chỉnh sửa vai trò (role): admin, clerk, manager, staff
- Gán bộ phận (Department)

### 3. Quản lý Công văn
**Đường dẫn**: Admin → Documents
- Thêm công văn mới
- Chỉnh sửa loại công văn (IN/OUT/INT)
- Upload file đính kèm
- Xem OCR content được trích xuất tự động

### 4. Quản lý Workflow
**Đường dẫn**: Admin → Workflow Definitions
- Tạo quy trình phê duyệt mới
- Thêm các bước duyệt
- Gán vai trò yêu cầu cho mỗi bước

### 5. Quản lý Phê duyệt
**Đường dẫn**: Admin → Approval Histories
- Xem lịch sử phê duyệt
- Xem nhận xét, chữ ký điện tử

---

## 🔐 Các vai trò và quyền hạn

### 1. **Admin (Quản trị viên)**
- Quyền: Toàn quyền quản lý hệ thống
- Dashboard: Admin Panel
- Chức năng:
  - Quản lý người dùng, phòng ban
  - Quản lý công văn, quy trình
  - Xem thống kê toàn hệ thống
  - Ký/duyệt công văn

### 2. **Manager (Lãnh đạo/Văn thư)**
- Quyền: Ký duyệt công văn
- Dashboard: Manager Dashboard
- Chức năng:
  - Xem công văn chờ ký/duyệt
  - Duyệt/từ chối công văn
  - Thêm nhận xét, chữ ký

### 3. **Clerk (Văn thư/Nhân viên)**
- Quyền: Nhập liệu công văn
- Dashboard: Staff Dashboard
- Chức năng:
  - Nhập công văn mới
  - Xem công văn của mình
  - Upload file đính kèm

### 4. **Staff (Nhân viên bình thường)**
- Quyền: Xem công văn
- Dashboard: Staff Dashboard
- Chức năng:
  - Xem công văn liên quan
  - Xem tình trạng duyệt

---

## 🎯 Quy trình xử lý công văn

```
1. NHẬP CÔNG VĂN (Clerk)
   ↓
2. OCR TỰ ĐỘNG (Hệ thống - Async)
   ↓
3. CHỜ DUYỆT (Pending)
   ↓
4. KÝ/DUYỆT (Manager/Admin)
   ↓
5. ĐÃ BAN HÀNH (Signed)
```

### Chi tiết từng bước:
1. **Nhập công văn**: Clerk vào Admin Panel → Documents → Add → Điền thông tin
2. **OCR tự động**: Hệ thống trích xuất text từ file upload (ảnh/PDF)
3. **Chờ duyệt**: Công văn được gán vào workflow
4. **Ký duyệt**: Manager/Admin xem công văn → Duyệt → Thêm chữ ký
5. **Đã hoàn thành**: Công văn được lưu trữ với chữ ký điện tử

---

## 🔍 Tìm kiếm và Lọc

### Trong Admin Panel
- **Tìm kiếm**: Nhập từ khóa vào thanh tìm kiếm
- **Lọc theo**:
  - Loại công văn: Đến (IN), Đi (OUT), Nội bộ (INT)
  - Trạng thái: Draft, Pending, Signed, Rejected
  - Ngày: Ngày tạo, ngày phát hành

### Trong Web Interface
- Dashboard hiển thị 10 công văn gần nhất
- Xem chi tiết: Vào Admin Panel

---

## 📁 Cấu trúc thư mục

```
abc_core/
├── settings.py          # Cấu hình Django
├── urls.py              # URL routing
├── wsgi.py              # WSGI config
├── celery.py            # Celery config
│
apps/
├── vn_users/            # Module Người dùng
│   ├── models.py        # User, Department models
│   ├── views.py         # Auth views
│   ├── urls.py          # Auth URLs
│   └── admin.py         # Admin interface
│
├── vn_docs/             # Module Công văn
│   ├── models.py        # Document model
│   ├── views.py         # Dashboard view
│   ├── tasks.py         # Celery OCR tasks
│   ├── signals.py       # Post-save signals
│   └── admin.py         # Admin interface
│
└── vn_workflow/         # Module Quy trình
    ├── models.py        # Workflow models
    └── admin.py         # Admin interface

templates/
├── base.html            # Base template
├── auth/login.html      # Login form
└── dashboard/
    ├── staff.html       # Staff dashboard
    ├── manager.html     # Manager dashboard
    └── admin.html       # Admin dashboard
```

---

## ⚠️ Xử lý sự cố

### 1. Lỗi "ModuleNotFoundError"
```bash
# Giải pháp: Cài đặt lại dependencies
pip install -r requirements.txt
```

### 2. Lỗi "port 8000 already in use"
```bash
# Giải pháp: Chạy trên port khác
python manage.py runserver 8001
```

### 3. Lỗi Database
```bash
# Giải pháp: Reset migrations
python manage.py migrate vn_docs zero
python manage.py migrate
```

### 4. Lỗi Static Files
```bash
# Giải pháp: Collect static files
python manage.py collectstatic --noinput
```

---

## 📞 Hỗ trợ

Nếu bạn gặp vấn đề:
1. Kiểm tra logs: `python manage.py runserver` (xem terminal)
2. Kiểm tra database: `db.sqlite3`
3. Liên hệ quản trị viên hệ thống

---

**Chúc bạn sử dụng hệ thống thành công! 🎉**
