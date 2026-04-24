# Phân tích Báo cáo Kiến trúc Tầng Dữ liệu - ABC Document Management System

## 1. Tổng quan Kiến trúc Dữ liệu

Hệ thống quản lý công văn ABC sử dụng kiến trúc **3-Tier Data Architecture**:
- **Presentation Layer:** Giao diện người dùng (Web Dashboard, Admin Interface)
- **Application Layer:** Logic xử lý (Django ORM, Business Logic)
- **Data Layer:** Lưu trữ dữ liệu vật lý (Database, File Storage, Cache)

---

## 2. Tầng Dữ liệu (Data Layer)

### 2.1 Database Layer - PostgreSQL/SQLite

#### 2.1.1 Cơ sở Dữ liệu Chính
```
Database: abc_documents (hoặc db.sqlite3 cho development)
Engine: PostgreSQL 12+ (Production) / SQLite3 (Development)
Encoding: UTF-8
```

#### 2.1.2 Sơ đồ Bảng (Schema Overview)

| Bảng | Mục đích | Số Record (dự kiến) | Kích thước |
|------|---------|-------------------|-----------|
| `auth_user` | Django's built-in user (override bởi vn_users.User) | <1000 | 500KB |
| `vn_users_department` | Phòng ban/Bộ phận công ty | 50-100 | 10KB |
| `vn_users_user` | Người dùng hệ thống (mở rộng auth.User) | 100-300 | 1MB |
| `vn_docs_document` | Công văn (Đến/Đi/Nội bộ) | 10,000-1M | Biến đổi |
| `vn_workflow_workflowdefinition` | Định nghĩa quy trình duyệt | 10-30 | 20KB |
| `vn_workflow_workflowstep` | Bước trong quy trình | 50-150 | 50KB |
| `vn_workflow_documentworkflow` | Liên kết công văn-quy trình xử lý | 10,000-1M | 10MB |
| `vn_workflow_approvalhistory` | Lịch sử phê duyệt/ký của từng công văn | 20,000-5M | 50MB |
| `django_session` | Quản lý phiên người dùng | 100-500 | 100KB |

---

### 2.2 Bảng Chi tiết & Mối Quan hệ (Detailed Schema)

#### 2.2.1 Bảng `vn_users_user` (Người dùng)
```sql
CREATE TABLE vn_users_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password_hash VARCHAR(128),
    role VARCHAR(20) NOT NULL,  -- admin, clerk, manager, staff
    department_id INTEGER REFERENCES vn_users_department(id),
    phone VARCHAR(15),
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    date_joined TIMESTAMP DEFAULT NOW()
);

INDEXES:
- username (UNIQUE)
- email (UNIQUE)
- department_id (FK)
- role (filtering by role)
```

#### 2.2.2 Bảng `vn_docs_document` (Công văn - Core)
```sql
CREATE TABLE vn_docs_document (
    id SERIAL PRIMARY KEY,
    doc_number VARCHAR(50) UNIQUE NOT NULL,  -- Số hiệu ngoài (VD: QĐ-2024-001)
    title TEXT NOT NULL,                      -- Trích yếu nội dung
    doc_type VARCHAR(5) NOT NULL,             -- IN (Đến), OUT (Đi), INT (Nội bộ)
    status VARCHAR(20) DEFAULT 'pending',    -- draft, pending, signed, archived
    
    sender_org VARCHAR(255),                  -- Cơ quan ban hành/gửi
    receiver_org VARCHAR(255),                -- Cơ quan nhận
    
    date_issued DATE NOT NULL,                -- Ngày ban hành trên văn bản
    date_created TIMESTAMP DEFAULT NOW(),    -- Ngày tiếp nhận/tạo trong hệ thống
    
    file_attachment VARCHAR(500),             -- Đường dẫn file tương đối (media/...)
    content_extracted TEXT,                   -- Nội dung đã OCR (for full-text search)
    
    created_by_id INTEGER NOT NULL REFERENCES vn_users_user(id),
    
    CONSTRAINT chk_doc_type CHECK (doc_type IN ('IN', 'OUT', 'INT')),
    CONSTRAINT chk_status CHECK (status IN ('draft', 'pending', 'signed', 'archived'))
);

INDEXES:
- doc_number (UNIQUE) -- Tra cứu nhanh theo số hiệu
- doc_type (Filtering)
- status (Filtering)
- date_issued (Range query)
- date_created (Range query)
- created_by_id (FK)
- FULLTEXT INDEX on (title, content_extracted) -- Tìm kiếm toàn văn bản
```

#### 2.2.3 Bảng `vn_workflow_documentworkflow` & `approvalhistory` (Quy trình duyệt)
```sql
CREATE TABLE vn_workflow_documentworkflow (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL UNIQUE REFERENCES vn_docs_document(id),
    workflow_id INTEGER NOT NULL REFERENCES vn_workflow_workflowdefinition(id),
    current_step_id INTEGER REFERENCES vn_workflow_workflowstep(id),
    status VARCHAR(20) DEFAULT 'pending'     -- pending, approved, rejected
);

CREATE TABLE vn_workflow_approvalhistory (
    id SERIAL PRIMARY KEY,
    doc_workflow_id INTEGER NOT NULL REFERENCES vn_workflow_documentworkflow(id),
    step_id INTEGER REFERENCES vn_workflow_workflowstep(id),
    approver_id INTEGER REFERENCES vn_users_user(id),
    action VARCHAR(20) NOT NULL,             -- approve, reject
    comment TEXT,
    signature_data TEXT,                     -- Base64 hoặc Hash của chữ ký số
    timestamp TIMESTAMP DEFAULT NOW()
);

INDEXES:
- doc_workflow_id, timestamp (Ordering approval history)
- approver_id (Query by approver)
- step_id (Filter by step)
```

---

### 2.3 Storage Layer - File System

#### 2.3.1 Cấu trúc Thư mục Lưu trữ File
```
media/
├── documents/
│   ├── 2024/
│   │   ├── 01/              # Tháng 1
│   │   │   ├── 15/          # Ngày 15
│   │   │   │   ├── QĐ-2024-001_original.pdf
│   │   │   │   ├── QĐ-2024-001_signed.pdf   # Sau ký số
│   │   ├── 02/
│   ├── 2025/
```

**Lý do tổ chức theo tháng/ngày:**
- Dễ tìm kiếm theo thời gian
- Hỗ trợ backup incremental theo ngày
- Tránh tình trạng 1 thư mục có quá nhiều file

#### 2.3.2 Chế độ Truy cập File
- **Read:** Bất kỳ user nào có quyền xem công văn
- **Write:** Chỉ user có vai trò Văn thư (clerk) được phép upload/chỉnh sửa
- **Delete:** Chỉ Admin và Văn thư được xóa (Soft delete, giữ lại lịch sử)

---

### 2.4 Cache Layer - Redis

```yaml
Redis Configuration:
  Host: localhost:6379
  Database: 0 (Django cache)
  Database: 1 (Celery result backend)
  Database: 2 (Session storage - optional)
  
Caching Strategy:
  - Dashboard statistics: TTL 15 phút
  - User permissions: TTL 1 giờ
  - Document list pagination: TTL 5 phút
  - Workflow state: TTL real-time
```

---

## 3. Mối Quan hệ Dữ liệu (Entity Relationship)

```
vn_users_user (1) ──────────────────> (N) vn_docs_document
                    created_by
                    
vn_docs_document (1)──────────────────> (N) vn_workflow_documentworkflow
                      
vn_workflow_documentworkflow (1) ──────> (N) vn_workflow_approvalhistory
                                         
vn_users_user (1) ────────────────────> (N) vn_workflow_approvalhistory
                       approver

vn_users_department (1) ───────────────> (N) vn_users_user
```

---

## 4. Hiệu suất & Tối ưu hóa (Performance)

### 4.1 Các chỉ số Hiệu suất (Benchmarks)

| Hoạt động | Thời gian Trung bình | Ghi chú |
|-----------|-------------------|--------|
| Thêm công văn mới | <500ms | Không bao gồm OCR ngầm |
| Tra cứu công văn (by doc_number) | <50ms | Index UNIQUE |
| Danh sách công văn (pagination, 20 items) | <200ms | Với filter |
| Tìm kiếm Full-text (100 docs) | <100ms | Phụ thuộc FULLTEXT index |
| Lưu phê duyệt + Cập nhật workflow | <100ms | Bao gồm lịch sử |
| OCR 1 file PDF (5 trang) | 2-5s | Chạy ngầm (Celery) |

### 4.2 Chiến lược Tối ưu

1. **Indexing:**
   - Primary Key: Tất cả các ID
   - Foreign Key: department_id, created_by_id, approver_id
   - Unique Key: username, email, doc_number
   - Full-text: title, content_extracted

2. **Query Optimization:**
   - Sử dụng `select_related()` cho FK
   - Sử dụng `prefetch_related()` cho reverse FK
   - Pagination cho danh sách dài

3. **Partitioning (cho production):**
   - Partition bảng `vn_workflow_approvalhistory` theo năm
   - Partition bảng `vn_docs_document` theo doc_type

---

## 5. Backup & Recovery

### 5.1 Chiến lược Backup

```yaml
Database Backup:
  - Frequency: Hàng ngày lúc 2:00 AM
  - Type: Full dump + Incremental
  - Retention: 30 ngày
  
File Backup:
  - Frequency: Hàng ngày
  - Method: rsync / Minio S3 backup
  - Retention: 90 ngày
  
Disaster Recovery:
  - Recovery Time Objective (RTO): 4 giờ
  - Recovery Point Objective (RPO): 1 giờ
```

### 5.2 Backup Commands

```bash
# Full database backup
pg_dump -U abc_user -h localhost abc_documents > backup_$(date +%Y%m%d).sql

# Restore
psql -U abc_user -h localhost abc_documents < backup_20260413.sql

# File backup
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

---

## 6. Bảo mật Dữ liệu

### 6.1 Mã hóa (Encryption)

| Loại dữ liệu | Mã hóa | Phương pháp |
|------------|--------|-----------|
| Password | Có | PBKDF2 (Django default) |
| File PDF | Có (optional) | AES-256 |
| Dữ liệu in transit | Có | HTTPS/TLS 1.3 |
| Backup | Có | GPG hoặc 7zip encrypted |

### 6.2 Audit Trail (Ghi nhật ký bảo mật)

Tất cả hành động quan trọng đều được ghi log:
```
- Ai tạo/sửa công văn: approvalhistory.approver_id
- Thời gian thao tác: approvalhistory.timestamp
- Hành động: approvalhistory.action
- IP address: (có thể thêm vào middleware)
- Ý kiến: approvalhistory.comment
```

---

## 7. Quản lý Dung lượng (Capacity Planning)

### 7.1 Ước tính Dung lượng (1 năm hoạt động)

```
Documents database: ~500MB (10,000 công văn chưa OCR)
With OCR content: ~2GB (average 200KB text per doc)
File storage: ~100GB (average 10MB per file scan)
Archive (5 năm): ~500GB
Total: ~600GB
```

### 7.2 Mở rộng (Scaling)

Khi dung lượng vượt 500GB:
- **Vertical Scaling:** Upgrade server CPU/RAM
- **Horizontal Scaling:** Replica database + Load balancer
- **Archive:** Di chuyển công văn cũ sang storage lạnh (Glacier/S3)

---

## 8. Monitoring & Alerting

### 8.1 Các chỉ số Giám sát (Metrics)

```yaml
Database:
  - Connection pool usage
  - Slow query log (>500ms)
  - Replication lag (if replica)
  
File Storage:
  - Disk usage percentage
  - I/O throughput
  - File count growth rate
  
Application:
  - API response time
  - Error rate (5xx)
  - Task queue length (Celery)
```

### 8.2 Alert Thresholds

- **Disk usage > 80%:** Warning
- **DB connection pool > 90%:** Error
- **API response time > 2s:** Warning
- **Failed task rate > 5%:** Error

---

## 9. Kết Luận

Kiến trúc dữ liệu của hệ thống ABC DMS được thiết kế để:
✅ **Scalability:** Hỗ trợ từ 100 đến 1M công văn  
✅ **Performance:** Thời gian phản hồi < 500ms  
✅ **Reliability:** Backup hàng ngày, RTO 4 giờ  
✅ **Security:** Mã hóa dữ liệu, audit trail đầy đủ  
✅ **Maintainability:** Cấu trúc rõ ràng, dễ mở rộng  

---

*Tài liệu được cập nhật lần cuối: 2026-04-13*
