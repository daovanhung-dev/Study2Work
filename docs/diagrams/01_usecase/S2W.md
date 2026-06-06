# Study2Work - Use Case Diagram (Markdown)

## 1. Tác nhân (Actors)

### Người dùng hệ thống
- Khách (Guest)
- Người học (Learner)
- Người hướng dẫn (Mentor)
- Nhà tuyển dụng (Recruiter)
- Quản trị viên (Admin)

### Hệ thống bên ngoài
- Dịch vụ AI (AI Service)
- Cổng thanh toán (Payment Gateway)
- Dịch vụ thông báo (Notification Service)

---

# 2. Xác thực & Truy cập

## Use Cases
- Đăng ký tài khoản
- Đăng nhập
- Quên mật khẩu
- Quản lý hồ sơ
- Quản lý vai trò & quyền hạn

## Actors

### Khách
- Đăng ký tài khoản
- Đăng nhập
- Quên mật khẩu

### Người học
- Quản lý hồ sơ

### Người hướng dẫn
- Quản lý hồ sơ

### Nhà tuyển dụng
- Quản lý hồ sơ

### Quản trị viên
- Quản lý vai trò & quyền hạn

---

# 3. Lộ trình học tập

## Use Cases
- Làm bài test đầu vào
- Nhận lộ trình AI
- Đăng ký lộ trình học
- Xem nội dung khóa học
- Xem bài giảng video
- Tham gia buổi học trực tuyến
- Tải tài liệu
- Theo dõi tiến độ

## Actors

### Người học
- Làm bài test đầu vào
- Nhận lộ trình AI
- Đăng ký lộ trình học
- Xem nội dung khóa học
- Xem bài giảng video
- Tham gia buổi học trực tuyến
- Tải tài liệu
- Theo dõi tiến độ

## Quan hệ
- Làm bài test đầu vào → <<include>> Nhận lộ trình AI
- Nhận lộ trình AI → AI Service tạo lộ trình

---

# 4. Thực hành & Đánh giá

## Use Cases

### Người học
- Nộp bài tập
- Làm bài quiz
- Thực hiện lab lập trình
- Xem phản hồi

### Người hướng dẫn
- Tạo bài tập
- Chấm bài nộp
- Review code

## Quan hệ
- Review code → AI Service hỗ trợ

---

# 5. Hệ thống dự án nhóm

## Use Cases

### Người học
- Tham gia dự án nhóm
- Quản lý nhiệm vụ sprint
- Gửi pull request

### Người hướng dẫn
- Tạo dự án nhóm
- Xem tiến độ nhóm

---

# 6. Đánh giá kỹ năng

## Use Cases

### Người hướng dẫn
- Đánh giá ma trận kỹ năng
- Đánh giá kỹ năng kỹ thuật
- Đánh giá kỹ năng mềm
- Tạo báo cáo

### Người học
- Xem phân tích

---

# 7. Hồ sơ cá nhân & Nghề nghiệp

## Use Cases

### Người học
- Xây dựng portfolio
- Xây dựng CV
- Luyện phỏng vấn
- Nhận gợi ý CV
- Nhận gợi ý portfolio

## Quan hệ
- Nhận gợi ý CV → <<include>> AI Service
- Nhận gợi ý Portfolio → <<include>> AI Service

---

# 8. Nhà tuyển dụng & Tuyển dụng

## Use Cases

### Nhà tuyển dụng
- Tạo tài khoản công ty
- Đăng yêu cầu tuyển dụng
- Tìm kiếm ứng viên
- Lọc theo kỹ năng
- Xem portfolio
- Lọt danh sách ứng viên
- Liên hệ ứng viên

### Người học
- Ứng tuyển công việc

---

# 9. Cộng đồng & Sự kiện

## Use Cases

### Người học
- Tham gia cộng đồng
- Tham gia workshop
- Tham gia thử thách lập trình
- Tham gia mock interview
- Thảo luận & Hỏi đáp

### Người hướng dẫn
- Tham gia workshop
- Tham gia mock interview

---

# 10. Thanh toán & Gói dịch vụ

## Use Cases

### Người học
- Mua khóa học
- Mua mentoring
- Xem lịch sử thanh toán

### Hệ thống thanh toán
- Xử lý thanh toán

## Quan hệ
- Mua khóa học → <<include>> Xử lý thanh toán
- Mua mentoring → <<include>> Xử lý thanh toán
- Payment Gateway → Xử lý thanh toán

---

# 11. Hệ thống thông báo

## Use Cases
- Gửi nhắc nhở học tập
- Gửi hạn nộp bài
- Gửi thông báo phỏng vấn
- Gửi thông báo hệ thống

## Actor
### Notification Service
- Gửi nhắc nhở học tập
- Gửi hạn nộp bài
- Gửi thông báo phỏng vấn
- Gửi thông báo hệ thống

---

# 12. Quản trị hệ thống

## Use Cases

### Quản trị viên
- Quản lý người dùng
- Quản lý khóa học
- Quản lý mentor
- Quản lý công ty
- Quản lý nội dung
- Quản lý báo cáo
- Cài đặt hệ thống

---

# 13. Quan hệ Include / Tích hợp

| Use Case | Quan hệ |
|-----------|----------|
| Làm bài test đầu vào | Include → Nhận lộ trình AI |
| Nhận lộ trình AI | Tích hợp AI Service |
| Review code | Tích hợp AI Service |
| Nhận gợi ý CV | Include → AI Service |
| Nhận gợi ý Portfolio | Include → AI Service |
| Mua khóa học | Include → Xử lý thanh toán |
| Mua mentoring | Include → Xử lý thanh toán |
| Xử lý thanh toán | Tích hợp Payment Gateway |

---

# Tổng quan chức năng

| Module | Số lượng UC |
|----------|------------|
| Xác thực & Truy cập | 5 |
| Lộ trình học tập | 8 |
| Thực hành & Đánh giá | 7 |
| Dự án nhóm | 5 |
| Đánh giá kỹ năng | 5 |
| Hồ sơ & Nghề nghiệp | 5 |
| Tuyển dụng | 8 |
| Cộng đồng & Sự kiện | 5 |
| Thanh toán | 4 |
| Thông báo | 4 |
| Quản trị hệ thống | 7 |

**Tổng số Use Case: 63**
**Tổng số Actor: 8**