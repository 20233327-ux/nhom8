# 🔐 Hướng dẫn Đăng nhập - ABC Document Management System

**Cập nhật**: Tính năng đăng nhập được cải thiện với giao diện thân thiện hơn và các tính năng mới.

---

## ✨ Tính năng mới

### 1. **Xem/Ẩn mật khẩu** 👁️
- Nhấp vào biểu tượng **mắt** bên phải ô mật khẩu
- Hoặc nhấn **phím Tab** để điều hướng đến nút và nhấp
- Giúp kiểm tra mật khẩu trước khi đăng nhập

### 2. **Ghi nhớ tài khoản** 💾
- Tích vào ô **"Ghi nhớ tài khoản của tôi"**
- Lần đăng nhập tiếp theo, tên đăng nhập sẽ tự động điền
- Session sẽ kéo dài **30 ngày** nếu chọn "ghi nhớ"
- ⚠️ **Lưu ý**: Chỉ sử dụng trên máy công việc hoặc máy cá nhân, không phải máy công cộng

### 3. **Xác thực form tự động** ✅
- Form check giá trị trước khi gửi
- Thông báo nếu bỏ trống tên đăng nhập hoặc mật khẩu
- Ngăn chặn gửi form liên tiếp

### 4. **Loading indicator** ⏳
- Hiển thị **spinner** khi đang xử lý đăng nhập
- Nút đăng nhập vô hiệu hóa để tránh click liên tiếp
- **Trạng thái**: "Đang xử lý..."

### 5. **Thông báo lỗi rõ ràng** 📢
- Hiển thị lỗi cụ thể:
  - "Tài khoản này đã bị vô hiệu hóa"
  - "Tên đăng nhập hoặc mật khẩu không chính xác"
- Tự động ẩn thông báo sau **4 giây**
- Có nút **X** để đóng thủ công

### 6. **Phím tắt** ⌨️
- **Enter**: Gửi form từ bất kỳ ô nào
- **Tab**: Điều hướng giữa các ô
- **Tab + Space**: Tích/bỏ tích "Ghi nhớ"

### 7. **Quên mật khẩu** 🆘
- Nhấp vào **"Quên mật khẩu?"**
- Sẽ chuyển đến trang hỗ trợ
- Có danh sách liên hệ Admin

---

## 🎨 Cải thiện giao diện

### Thiết kế hiện đại
- ✅ Gradient màu sắc (tím + xanh)
- ✅ Animations mượt mà
- ✅ Bóng mờ chuyên nghiệp
- ✅ Icons rõ ràng với Font Awesome

### Responsive (thích ứng)
- ✅ Hoạt động tốt trên **desktop, tablet, điện thoại**
- ✅ Tự động điều chỉnh kích thước
- ✅ Touch-friendly trên mobile

### Accessibility (Tiếp cận)
- ✅ Hỗ trợ **keyboard navigation** đầy đủ
- ✅ Focus indicator rõ ràng
- ✅ Tương thích **màn hình nền** (screen reader)
- ✅ Độ tương phản cao để dễ đọc

---

## 📱 Cách sử dụng trên từng thiết bị

### Desktop (Máy tính)
```
1. Mở: http://127.0.0.1:8000/auth/login/
2. Nhập tên đăng nhập
3. Nhập mật khẩu (hoặc xem bằng cách nhấp vào mắt)
4. Tích "Ghi nhớ" nếu muốn (tùy chọn)
5. Nhấp "Đăng nhập" hoặc nhấn Enter
```

### Tablet/Điện thoại
```
1. Tương tự desktop
2. Giao diện tự động điều chỉnh
3. Các ô và nút được phóng to để dễ chạm
4. Bàn phím ảo tự động hiện
```

---

## 🔒 Bảo mật & Lưu ý

### ✅ An toàn
- Mật khẩu **không bao giờ** được lưu trữ
- Chỉ có **tên đăng nhập** được lưu (nếu chọn "ghi nhớ")
- Sử dụng **HTTPS** trên production
- Session **tự động đặt lại** khi đóng browser (nếu không chọn "ghi nhớ")

### ⚠️ Cảnh báo
- **KHÔNG SỬ DỤNG** "Ghi nhớ tài khoản" trên máy công cộng
- **KHÔNG SỬ DỤNG** trên máy tính thuê
- **KHÔNG LƯU** mật khẩu trong trình duyệt
- **LÀM ĐĂNG XUẤT** khi dùng xong

---

## 🆘 Xử lý sự cố

### "Nhập sai mật khẩu 3 lần"
```
→ Thị hiệu lỗi: "Tên đăng nhập hoặc mật khẩu không chính xác"
→ Giải pháp: Nhấp "Quên mật khẩu?" → liên hệ Admin
```

### "Tài khoản bị khóa/vô hiệu"
```
→ Thị hiệu lỗi: "Tài khoản này đã bị vô hiệu hóa"
→ Giải pháp: Liên hệ quản trị viên để kích hoạt lại
```

### "Không thể đăng nhập"
```
→ Kiểm tra:
  ✓ Tên đăng nhập: phải điền đầy đủ
  ✓ Mật khẩu: phải chính xác (có phân biệt hoa thường)
  ✓ Kết nối Internet: phải bình thường
  ✓ Server: http://127.0.0.1:8000/ phải chạy

→ Nếu vẫn không được: xóa cookies/cache trình duyệt
```

### "Kí tự không hợp lệ"
```
→ Hiện tượng: Form không gửi được
→ Giải pháp: Kiểm tra không có khoảng trắng thừa ở đầu/cuối
```

---

## 📞 Hỗ trợ

### Quên mật khẩu
- **Cách 1**: Nhấp "Quên mật khẩu?" → liên hệ Admin
- **Cách 2**: Gọi điện: **0123-456-789**
- **Cách 3**: Email: **admin@abc.com**

### Lỗi kỹ thuật
- **Giờ hỗ trợ**: 8:00 - 17:30 (T2-T6)
- **Chi nhánh**: Hà Nội

---

## 🎓 Tips & Tricks

### Mẹo 1: Ctrl + Shift + Delete
Xóa dữ liệu đăng nhập cũ nếu muốn:
```
Trình duyệt → Settings → Privacy → Clear browsing data → Cookies
```

### Mẹo 2: Autofill không hoạt động?
```
Menu → Settings → Passwords → Mở form để kiểm tra
```

### Mẹo 3: Chia sẻ máy tính?
```
👉 Luôn đăng xuất trước khi rời khỏi máy
👉 Không tích "Ghi nhớ" trên máy chia sẻ
👉 Xóa dữ liệu đăng nhập sau khi dùng xong
```

---

## 🔍 Chi tiết kỹ thuật

### Session Management
| Trường hợp | Thời gian |
|-----------|----------|
| Bình thường | Hết khi đóng browser |
| Ghi nhớ | 30 ngày |
| Không hoạt động | 24 giờ (tùy cấu hình) |

### Bảo mật
- Mật khẩu: **PBKDF2** hashing
- CSRF: **Token** bảo vệ form
- SSL/TLS: **Https** (production)
- Rate limiting: **Theo IP** (sắp triển khai)

---

## 📋 Danh sách kiểm tra trước đăng nhập

- [ ] Máy tính kết nối Internet?
- [ ] Server khởi động đúng?
- [ ] URL đúng: **http://127.0.0.1:8000/auth/login/**?
- [ ] Tên người dùng chính xác?
- [ ] Mật khẩu chính xác?
- [ ] Caps Lock tắt (mật khẩu phân biệt hoa/thường)?
- [ ] Không có khoảng trắng thừa?

---

## 🎉 Kết luận

Giao diện đăng nhập mới được thiết kế để:
- ✅ **Dễ sử dụng**: Giao diện thân thiện
- ✅ **An toàn**: Bảo vệ tài khoản
- ✅ **Nhanh chóng**: Tiết kiệm thời gian
- ✅ **Tiếp cận**: Hỗ trợ tất cả thiết bị

**Chúc sử dụng tệ thống thành công!** 🚀

---

**Phiên bản**: 1.0.0  
**Cập nhật**: 2026  
**Ngôn ngữ**: Tiếng Việt
