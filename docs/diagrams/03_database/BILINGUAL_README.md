# STUDY2WORK - Biểu đồ CSDL Song ngữ (VN/EN)

## 📋 Giới thiệu

Bộ biểu đồ này chứa **các bảng dữ liệu (database tables/entities)** với **hai ngôn ngữ**:

- **Tiếng Việt**: Tên bảng, mô tả các trường để dev dễ hiểu ý nghĩa
- **Tiếng Anh**: Tên bảng, tên trường dùng cho lập trình (DB)

## 📁 Cấu trúc file

### File gốc (English only)

```
01_AUTH.puml                           - Xác thực (ngôn ngữ Anh)
02_LEARNING.puml                       - Học tập (ngôn ngữ Anh)
03_PLACEMENT_AND_AI_ROADMAP.puml       - Vị trí & Lộ trình AI (ngôn ngữ Anh)
04_ASSESSMENT.puml                     - Đánh giá (ngôn ngữ Anh)
05_RECRUITMENT.puml                    - Tuyển dụng (ngôn ngữ Anh)
06_PAYMENT.puml                        - Thanh toán (ngôn ngữ Anh)
00_OVERVIEW.puml                       - Tổng quan (ngôn ngữ Anh)
```

### File song ngữ (Bilingual)

```
01_AUTH_BILINGUAL.puml                 ✅ Xác thực - Song ngữ VN/EN
02_LEARNING_BILINGUAL.puml             ✅ Học tập - Song ngữ VN/EN
03_PLACEMENT_AND_AI_ROADMAP_BILINGUAL.puml ✅ Vị trí & Lộ trình AI - Song ngữ VN/EN
04_ASSESSMENT_BILINGUAL.puml           ✅ Đánh giá - Song ngữ VN/EN
05_RECRUITMENT_BILINGUAL.puml          ✅ Tuyển dụng - Song ngữ VN/EN
06_PAYMENT_BILINGUAL.puml              ✅ Thanh toán - Song ngữ VN/EN
00_OVERVIEW_BILINGUAL.puml             ✅ Tổng quan - Song ngữ VN/EN
```

## 🗂️ Các Mô-đun

### 1. **XÁC-THỰC (AUTH Module)**

📄 File: `01_AUTH_BILINGUAL.puml`

**Mục đích**: Quản lý người dùng, vai trò, phiên đăng nhập

**Bảng chính**:

- `người_dùng` (users) - Tài khoản người dùng
- `vai_trò` (roles) - Các vai trò trong hệ thống
- `quyền_người_dùng` (user_roles) - Gán vai trò cho người dùng
- `hồ_sơ_người_dùng` (user_profiles) - Thông tin cá nhân mở rộng
- `mã_xác_thực` (user_verification_tokens) - Mã xác thực email/OTP
- `phiên_đăng_nhập` (user_sessions) - Quản lý phiên làm việc
- `thông_báo` (notifications) - Thông báo cho người dùng
- `nhật_ký_quản_trị` (admin_audit_logs) - Ghi nhật ký hành động admin

---

### 2. **HỌC-TẬP (LEARNING Module)**

📄 File: `02_LEARNING_BILINGUAL.puml`

**Mục đích**: Quản lý khóa học, bài học, tài liệu, tiến độ học tập

**Bảng chính**:

- `danh_mục_khóa` (course_categories) - Phân loại khóa học
- `khóa_học` (courses) - Khóa học
- `chương_học` (course_modules) - Các chương trong khóa
- `bài_học` (course_lessons) - Bài học chi tiết
- `tài_liệu_bài_học` (lesson_resources) - Tài liệu bài học
- `đăng_ký_khóa` (course_enrollments) - Người dùng đăng ký khóa
- `tiến_độ_bài_học` (lesson_progress) - Theo dõi tiến độ
- `lịch_xem_video` (video_watch_logs) - Log xem video

---

### 3. **VỊ-TRÍ & LỘ-TRÌNH AI (PLACEMENT & AI ROADMAP Module)**

📄 File: `03_PLACEMENT_AND_AI_ROADMAP_BILINGUAL.puml`

**Mục đích**: Kiểm tra đầu vào kỹ năng, tạo lộ trình học được AI hỗ trợ

**Bảng chính**:

- `kiểm_tra_đầu_vào` (placement_tests) - Bài kiểm tra đầu vào
- `câu_hỏi_đầu_vào` (placement_questions) - Câu hỏi
- `lựa_chọn_câu_hỏi` (placement_question_options) - Lựa chọn
- `lần_làm_kiểm_tra` (placement_attempts) - Kết quả làm bài
- `câu_trả_lời` (placement_attempt_answers) - Câu trả lời chi tiết
- `lộ_trình_học` (roadmaps) - Lộ trình học được AI tạo
- `bước_lộ_trình` (roadmap_steps) - Các bước trong lộ trình

---

### 4. **ĐÁNH-GIÁ (ASSESSMENT Module)**

📄 File: `04_ASSESSMENT_BILINGUAL.puml`

**Mục đích**: Quản lý bài kiểm tra, bài tập, bài lab lập trình

**Bảng chính**:

- `bài_kiểm_tra` (quizzes) - Quiz trong khóa học
- `câu_hỏi_quiz` (quiz_questions) - Câu hỏi quiz
- `lựa_chọn_quiz` (quiz_options) - Lựa chọn câu hỏi
- `lần_làm_quiz` (quiz_attempts) - Kết quả làm quiz
- `trả_lời_quiz` (quiz_answers) - Câu trả lời
- `bài_tập` (assignments) - Bài tập
- `bài_nộp_tập` (assignment_submissions) - Bài nộp
- `bài_lab_lập_trình` (coding_labs) - Bài lab lập trình
- `lần_làm_lab` (coding_lab_attempts) - Kết quả làm lab
- `xem_xét_code` (code_reviews) - Đánh giá code

---

### 5. **TUYỂN-DỤNG (RECRUITMENT Module)**

📄 File: `05_RECRUITMENT_BILINGUAL.puml`

**Mục đích**: Quản lý công ty, vị trí công việc, hồ sơ, ứng tuyển

**Bảng chính**:

- `công_ty` (companies) - Thông tin công ty
- `thành_viên_công_ty` (company_members) - Thành viên công ty
- `vị_trí_công_việc` (jobs) - Vị trí tuyển dụng
- `kỹ_năng_vị_trí` (job_skills) - Kỹ năng yêu cầu
- `hồ_sơ_ứng_viên` (resumes) - Hồ sơ cá nhân
- `học_vấn` (resume_educations) - Học vấn
- `kinh_nghiệm_làm_việc` (resume_experiences) - Kinh nghiệm
- `kỹ_năng_hồ_sơ` (resume_skills) - Kỹ năng
- `đơn_ứng_tuyển` (job_applications) - Đơn ứng tuyển

---

### 6. **THANH-TOÁN (PAYMENT Module)**

📄 File: `06_PAYMENT_BILINGUAL.puml`

**Mục đích**: Quản lý đơn hàng, thanh toán, mã giảm giá

**Bảng chính**:

- `mã_giảm_giá` (coupons) - Mã coupon/voucher
- `đơn_hàng` (orders) - Đơn hàng
- `mặt_hàng_đơn` (order_items) - Mặt hàng trong đơn
- `thanh_toán` (payments) - Ghi nhận thanh toán

---

### 7. **TỔNG QUAN (OVERVIEW)**

📄 File: `00_OVERVIEW_BILINGUAL.puml`

**Mục đích**: Biểu đồ tổng quan mối quan hệ giữa các mô-đun

---

## 🎯 Cách sử dụng

### Cho Developers (Dev)

- ✅ Mở các file `*_BILINGUAL.puml`
- ✅ Đọc **tên Tiếng Việt** để hiểu ý nghĩa của bảng dữ liệu
- ✅ Đọc **tên Tiếng Anh** khi viết code/query SQL
- ✅ Xem mô tả trường dưới dạng nhận xét `[mô tả]` để hiểu từng trường

**Ví dụ**:

```
entity "người_dùng\n(users)" as users {
  * id : BIGINT
  --
  full_name : VARCHAR [họ tên]
  email : VARCHAR [email]
  password_hash : VARCHAR [mã hóa mật khẩu]
  ...
}
```

- Dev hiểu là: Bảng **người_dùng** lưu thông tin cá nhân
- Dev code: `SELECT * FROM users WHERE email = '...'`

### Cho Database Architects

- ✅ Sử dụng file gốc (English) hoặc file `*_BILINGUAL.puml`
- ✅ Tên bảng + trường Tiếng Anh cho consistency
- ✅ Các file song ngữ giúp hiểu context nhanh hơn

### Cho Management/Product

- ✅ Xem file `00_OVERVIEW_BILINGUAL.puml` để hiểu toàn bộ hệ thống
- ✅ Đọc Tiếng Việt để nắm rõ từng mô-đun

---

## 📝 Ghi chú

### Quy ước đặt tên:

- **Tên bảng (English)**: `snake_case` (ví dụ: `user_profiles`)
- **Tên bảng (Việt)**: `snake_case` (ví dụ: `hồ_sơ_người_dùng`)
- **Trường**: `snake_case` (ví dụ: `created_at`)
- **Mô tả trường**: Ghi chú trong `[...]`

### Các ký hiệu quan hệ:

- `||--o{` : One-to-Many (1-n)
- `||--||` : One-to-One (1-1)

---

## 🔗 Liên kết giữa các mô-đun

```
AUTH (người dùng)
├─→ LEARNING (người dùng học tập)
├─→ PLACEMENT (người dùng làm bài kiểm tra)
├─→ ASSESSMENT (người dùng làm quiz/bài tập)
├─→ RECRUITMENT (người dùng ứng tuyển)
└─→ PAYMENT (người dùng thanh toán)

LEARNING (khóa học)
├─→ PLACEMENT (tạo lộ trình từ khóa học)
└─→ ASSESSMENT (quiz/lab trong khóa học)

RECRUITMENT (hồ sơ)
└─→ PAYMENT (đơn hàng cho khóa học)
```

---

## 💡 Lợi ích của bộ biểu đồ song ngữ

✅ **Dễ hiểu**: Dev Việt hiểu ý nghĩa từng bảng
✅ **Professional**: Tên bảng/trường Tiếng Anh chuẩn
✅ **Dễ bảo trì**: Mô tả chi tiết mỗi trường
✅ **Toàn bộ team**: Frontend, Backend, QA đều hiểu
✅ **Tài liệu sống**: Cập nhật khi schema thay đổi

---

## 📞 Hỗ trợ

Nếu cần cập nhật hoặc chỉnh sửa biểu đồ:

1. Chỉnh sửa file `.puml` tương ứng
2. Xem trước bằng PlantUML extension (VSCode)
3. Commit thay đổi với message rõ ràng

---

**Phiên bản**: 1.0 (2026-06-05)  
**Tạo bởi**: GitHub Copilot
