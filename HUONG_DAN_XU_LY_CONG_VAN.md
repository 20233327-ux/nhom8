# Hướng dẫn Quy trình Xử lý Công văn - ABC Document Management System

## 📋 Tổng quan Quy trình

Hệ thống quản lý công văn ABC hỗ trợ xử lý **3 loại công văn** với quy trình riêng:
1. **Công văn Đến:** Tiếp nhận từ các cơ quan bên ngoài
2. **Công văn Đi:** Soạn thảo và ban hành ra ngoài
3. **Công văn Nội bộ:** Lưu trữ nội bộ công ty

---

## 1️⃣ Quy trình Tiếp nhận Công văn Đến (Incoming Documents)

### Bước 1: Nhân viên Văn thư tiếp nhận bản gốc
- Nhân viên Văn thư nhận bản giấy/file điện tử từ cơ quan gửi
- Ghi lại: Ngày tiếp nhận, cơ quan gửi, trích yếu sơ bộ

### Bước 2: Số hóa tài liệu (Digitization)
```
Hành động: Vào /admin/ → Chọn "Document" → Click "Add Document"
Nhập thông tin:
  ✓ Số hiệu công văn: VD-2024-001
  ✓ Trích yếu: "Yêu cầu cấp giấy chứng nhận..."
  ✓ Loại: Chọn "Công văn đến" (IN)
  ✓ Cơ quan gửi: "Sở Xây dựng TP.HCM"
  ✓ Upload file: scan_vd_2024_001.pdf
  ✓ Nhấn "Save"
```

### Bước 3: Hệ thống tự động xử lý OCR (Ngầm)
- Celery Worker sẽ tự động:
  - Đọc nội dung từ file PDF/Ảnh
  - Trích xuất text và lưu vào database
  - Tạo index cho tìm kiếm toàn văn
  - **Thời gian:** 2-5 giây cho 1 file (chạy ngầm, không làm treo hệ thống)

### Bước 4: Gán xử lý (Assignment)
- Văn thư xác định: "Công văn này cần phòng nào xử lý?"
- Tạo **Workflow** liên kết công văn với bộ phận phụ trách
- **Ví dụ:** Công văn này → Gán cho Phòng Nhân sự xử lý

```
Admin Panel: vn_workflow > DocumentWorkflow
  - Select document: VD-2024-001
  - Select workflow: "Xử lý Công văn Đến chuẩn"
  - Current step: "Phòng Nhân sự xem xét"
  - Status: pending
  - Save
```

### Bước 5: Phòng ban xử lý công văn
- Nhân viên phòng Nhân sự truy cập Dashboard hoặc /admin/
- Xem công văn được gán
- Thực hiện xử lý theo chỉ đạo: Cấp giấy, từ chối, yêu cầu bổ sung...

### Bước 6: Trình duyệt lãnh đạo (Approval)
- Phòng đã xử lý trình kết quả cho Trưởng phòng duyệt
- Hệ thống tự động chuyển sang bước "Trưởng phòng phê duyệt" (next workflow step)
- Trưởng phòng xem ý kiến, nhận xét, và chọn: **Duyệt** hoặc **Từ chối**

```
Hành động: /admin/ > ApprovalHistory > Add
  - Document workflow: VD-2024-001
  - Step: "Trưởng phòng phê duyệt"
  - Approver: Chọn "Trưởng phòng Nhân sự"
  - Action: "Duyệt" ✓
  - Comment: "Ý kiến: Duyệt đề xuất này"
  - Submit
```

### Bước 7: Lưu trữ công văn đã xử lý
- Sau khi hoàn tất phê duyệt, công văn chuyển trạng thái → **"Archived"** (Đã lưu trữ)
- Tạo bản sao lưu (backup) tự động hàng ngày
- Lưu lịch sử xử lý để phục vụ kiểm tra, truy vết

---

## 2️⃣ Quy trình Soạn thảo & Ban hành Công văn Đi (Outgoing Documents)

### Bước 1: Nhân viên soạn thảo công văn
```
Hành động: /admin/ > Document > Add
  ✓ Số hiệu: QĐ-2024-001 (Tự sinh bởi hệ thống)
  ✓ Trích yếu: "Quy định quản lý....."
  ✓ Loại: "Công văn đi" (OUT)
  ✓ Cơ quan nhận: "Các phòng ban"
  ✓ Upload bản dự thảo (draft)
  ✓ Status: "draft" (Dự thảo)
```

### Bước 2: Trình duyệt cấp Phòng
- Nhân viên soạn trình Trưởng phòng
- Tạo quy trình duyệt:
  ```
  Workflow: "Ban hành Quy định"
  Step 1: Trưởng phòng xem xét
  Step 2: Giám đốc duyệt
  Step 3: Ký số
  ```

### Bước 3: Duyệt nội dung & Chỉnh sửa
- Trưởng phòng nhận thông báo (hoặc xem trong Dashboard)
- Xem nội dung, nhận xét, yêu cầu sửa (nếu cần)
- Nếu OK → **Duyệt** (Approve)

```
ApprovalHistory:
  Status: "Trưởng phòng đã duyệt" ✓
  Chuyển sang bước tiếp: Giám đốc
```

### Bước 4: Duyệt cấp Lãnh đạo
- Giám đốc xem công văn cuối cùng
- Có thêm ý kiến? → Yêu cầu sửa
- OK? → **Duyệt**

```
ApprovalHistory:
  Approver: Giám đốc
  Action: "Duyệt"
  Status: "Chờ ký số"
```

### Bước 5: Ký số (Digital Signature)
- Giám đốc/Ủy quyền người ký số
- Upload file chứng thư số (.p12 hoặc .pfx)
- Nhập mật khẩu chứng thư
- Hệ thống tạo bản PDF đã ký → `QĐ-2024-001_signed.pdf`

```
Hành động: Ký lên file PDF
  - File input: QĐ-2024-001.pdf (bản dự thảo)
  - P12 certificate: mycert.p12
  - Output: QĐ-2024-001_signed.pdf
  - Status: "signed" (Đã ký)
```

### Bước 6: Ban hành & Phát hành
- Văn thư phát hành bản PDF đã ký cho các phòng ban
- Gửi email hoặc in bản giấy
- Cập nhật trạng thái → **"Archived"** (Đã phát hành)

---

## 3️⃣ Quy trình Lưu trữ Công văn Nội bộ (Internal Documents)

### Bước 1: Tạo công văn nội bộ
```
/admin/ > Document > Add
  ✓ Loại: "Công văn nội bộ" (INT)
  ✓ Nhập metadata
  ✓ Upload tài liệu
```

### Bước 2: Phân quyền truy cập
- Chỉ nhân viên trong phòng/bộ phận được quyền xem
- Admin cấu hình quyền trong Model RBAC

### Bước 3: Lưu trữ dài hạn
- Hệ thống tự động backup hàng ngày
- Có thể dễ dàng phục hồi nếu mất dữ liệu

---

## 4️⃣ Tính năng Tìm kiếm & Tra cứu

### 4.1 Tìm kiếm theo metadata (Metadata Search)
```
/admin/ > Document
  - Search by số hiệu: VD-2024-001
  - Filter by loại: Công văn Đến
  - Filter by trạng thái: pending
  - Filter by khoảng thời gian: 01/01/2024 - 31/12/2024
```

### 4.2 Tìm kiếm toàn văn (Full-text Search)
- Tìm trong nội dung text đã OCR
- Ví dụ: Tìm "cấp giấy chứng nhận" → Hệ thống tìm trong nội dung tất cả file PDF
- **Lợi ích:** Giảm 80% thời gian tra cứu thủ công

```
Hành động: /admin/ > Document > Search
  - Keyword: "giấy chứng nhận"
  - Kết quả: Danh sách 23 công văn có từ này
```

---

## 5️⃣ Dashboard Thống kê & Cảnh báo

### 5.1 Xem thống kê tổng quan
Truy cập: `http://127.0.0.1:8000/dashboard/`
```
- Tổng số công văn: 150
- Đang xử lý: 23
- Đã ban hành: 127
- Công văn trễ hạn (>7 ngày): 5 ⚠️
```

### 5.2 Cảnh báo công văn trễ hạn
- Hệ thống tự động **nhận diện** các công văn chưa xử lý quá 7 ngày
- Hiển thị danh sách với **màu đỏ** (Warning)
- Giúp lãnh đạo can thiệp kịp thời

```
Công văn trễ hạn:
│ Số hiệu  │ Trích yếu              │ Ngày nhận │ Ngày trễ │
│ VD-2024-001 │ Yêu cầu cấp giấy... │ 31/03/2024 │ 5 ngày  │
│ VD-2024-002 │ Hợp tác quốc tế...  │ 01/04/2024 │ 4 ngày  │
```

---

## 6️⃣ Lịch sử & Audit Trail

### Mỗi công văn đều có lịch sử xử lý chi tiết:
```
Công văn: QĐ-2024-001

📅 Lịch sử xử lý:
  13/04/2024 10:30 → Văn thư (Lê Thị A) tạo công văn
  13/04/2024 14:00 → Trưởng phòng (Ngô Văn B) duyệt ✓
  13/04/2024 15:45 → Giám đốc (Trần Văn C) duyệt ✓
  13/04/2024 16:00 → Ký số hoàn tất
  13/04/2024 16:15 → Văn thư phát hành
```

### Lợi ích:
- **Truy trách:** Ai chậm xử lý? Ai phê duyệt?
- **Kiểm toán:** Kiểm tra quy trình phê duyệt
- **Phục hồi:** Nếu có tranh chấp, có lịch sử để chứng minh

---

## 7️⃣ Quyền hạn & Phân quyền (RBAC)

### 7.1 Vai trò & Quyền hạn

| Vai trò | Quyền hạn |
|--------|---------|
| **Admin** | Quản lý toàn bộ hệ thống, tạo workflow, cấu hình user |
| **Văn thư (Clerk)** | Tiếp nhận, nhập liệu, cấp số, phát hành công văn |
| **Lãnh đạo (Manager)** | Duyệt, ký số, xem báo cáo |
| **Nhân viên (Staff)** | Xem công văn, soạn thảo draft, theo dõi tiến độ |

### 7.2 Cấu hình quyền
```
/admin/ > VN_USERS > User
  - Chọn user
  - Role: "Văn thư"
  - Department: "Phòng Hành chính"
  - Save
```

---

## 8️⃣ Best Practices (Các quy tắc hay)

✅ **Luôn cập nhật metadata đầy đủ:**
- Số hiệu, ngày ban hành, cơ quan gửi/nhận phải đúng
- Giúp tìm kiếm chính xác sau này

✅ **Ghi chú rõ ràng trong Comment (Approval):**
- Không chỉ "Duyệt" mà cần "Duyệt - Không có ý kiến"
- Giúp người xử lý bước tiếp theo hiểu rõ

✅ **Không bao giờ xóa công văn:**
- Hệ thống chỉ **soft delete** (để lại dấu vết)
- Hay sử dụng **Archive** để lưu trữ

✅ **Backup hàng ngày:** 
- Đảm bảo không mất dữ liệu quan trọng

---

## ❓ Các câu hỏi thường gặp (FAQ)

**Q: Nếu quên mật khẩu ký số phải làm sao?**
A: Liên hệ Admin để cấp lại chứng thư số mới hoặc reset mật khẩu.

**Q: Công văn có thể sửa sau khi đã ký không?**
A: Không (để đảm bảo tính pháp lý). Nếu cần sửa, phải tạo công văn mới.

**Q: Tìm kiếm toàn văn mất bao lâu?**
A: Thường < 100ms. Nếu chậm hơn, cần kiểm tra server.

**Q: Lịch sử công văn có thể xóa được không?**
A: Không, lịch sử phê duyệt phải giữ lại vĩnh viễn (yêu cầu pháp lý).

---

## 📞 Hỗ trợ & Liên hệ

Nếu gặp sự cố:
- Truy cập `/admin/` để xem log chi tiết
- Liên hệ IT Support
- Gửi feedback: support@abc-company.com

---

*Tài liệu được cập nhật lần cuối: 2026-04-13*
