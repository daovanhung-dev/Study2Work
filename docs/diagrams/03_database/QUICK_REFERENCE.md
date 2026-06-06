# Danh sách nhanh - Các bảng CSDL Song ngữ

## 📊 Bảng tham chiếu nhanh (Quick Reference)

### 1️⃣ XÁC-THỰC (AUTH)

| Tiếng Việt       | English                  | Mô tả                                   |
| ---------------- | ------------------------ | --------------------------------------- |
| người_dùng       | users                    | Tài khoản người dùng                    |
| vai_trò          | roles                    | Vai trò (Admin, Instructor, Student...) |
| quyền_người_dùng | user_roles               | Gán vai trò cho người dùng              |
| hồ_sơ_người_dùng | user_profiles            | Thông tin mở rộng (GitHub, LinkedIn...) |
| mã_xác_thực      | user_verification_tokens | OTP, email verification                 |
| phiên_đăng_nhập  | user_sessions            | Refresh token, thiết bị                 |
| thông_báo        | notifications            | In-app notifications                    |
| nhật_ký_quản_trị | admin_audit_logs         | Ghi nhật ký hành động admin             |

### 2️⃣ HỌC-TẬP (LEARNING)

| Tiếng Việt       | English            | Mô tả                    |
| ---------------- | ------------------ | ------------------------ |
| danh_mục_khóa    | course_categories  | Danh mục khóa học        |
| khóa_học         | courses            | Khóa học                 |
| chương_học       | course_modules     | Chương trong khóa        |
| bài_học          | course_lessons     | Bài học (video, text...) |
| tài_liệu_bài_học | lesson_resources   | Tài liệu, PDF, slides    |
| đăng_ký_khóa     | course_enrollments | Người dùng đăng ký khóa  |
| tiến_độ_bài_học  | lesson_progress    | Tiến độ học từng bài     |
| lịch_xem_video   | video_watch_logs   | Log xem video            |

### 3️⃣ VỊ-TRÍ & LỘ-TRÌNH AI (PLACEMENT & AI ROADMAP)

| Tiếng Việt       | English                    | Mô tả                       |
| ---------------- | -------------------------- | --------------------------- |
| kiểm*tra*đầu_vào | placement_tests            | Bài kiểm tra kỹ năng        |
| câu*hỏi*đầu_vào  | placement_questions        | Câu hỏi                     |
| lựa_chọn_câu_hỏi | placement_question_options | Lựa chọn (A, B, C, D)       |
| lần_làm_kiểm_tra | placement_attempts         | Kết quả làm bài             |
| câu_trả_lời      | placement_attempt_answers  | Chi tiết câu trả lời        |
| lộ_trình_học     | roadmaps                   | Lộ trình do AI tạo          |
| bước_lộ_trình    | roadmap_steps              | Bước (khóa học, bài lab...) |

### 4️⃣ ĐÁNH-GIÁ (ASSESSMENT)

| Tiếng Việt        | English                | Mô tả                    |
| ----------------- | ---------------------- | ------------------------ |
| bài_kiểm_tra      | quizzes                | Quiz kiểm tra            |
| câu_hỏi_quiz      | quiz_questions         | Câu hỏi                  |
| lựa_chọn_quiz     | quiz_options           | Lựa chọn                 |
| lần_làm_quiz      | quiz_attempts          | Kết quả                  |
| trả_lời_quiz      | quiz_answers           | Câu trả lời              |
| bài_tập           | assignments            | Bài tập                  |
| bài_nộp_tập       | assignment_submissions | Bài nộp                  |
| bài_lab_lập_trình | coding_labs            | Bài lab (C++, Python...) |
| lần_làm_lab       | coding_lab_attempts    | Kết quả lab              |
| xem_xét_code      | code_reviews           | Code review từ mentor    |

### 5️⃣ TUYỂN-DỤNG (RECRUITMENT)

| Tiếng Việt           | English            | Mô tả             |
| -------------------- | ------------------ | ----------------- |
| công_ty              | companies          | Thông tin công ty |
| thành_viên_công_ty   | company_members    | Nhân viên công ty |
| vị_trí_công_việc     | jobs               | Vị trí tuyển dụng |
| kỹ_năng_vị_trí       | job_skills         | Kỹ năng yêu cầu   |
| hồ*sơ*ứng_viên       | resumes            | CV/Hồ sơ          |
| học_vấn              | resume_educations  | Học vấn           |
| kinh_nghiệm_làm_việc | resume_experiences | Kinh nghiệm       |
| kỹ_năng_hồ_sơ        | resume_skills      | Kỹ năng           |
| đơn_ứng_tuyển        | job_applications   | Đơn ứng tuyển     |

### 6️⃣ THANH-TOÁN (PAYMENT)

| Tiếng Việt   | English     | Mô tả               |
| ------------ | ----------- | ------------------- |
| mã_giảm_giá  | coupons     | Coupon/Voucher      |
| đơn_hàng     | orders      | Đơn hàng            |
| mặt*hàng*đơn | order_items | Mặt hàng trong đơn  |
| thanh_toán   | payments    | Ghi nhận thanh toán |

---

## 🔍 Tìm kiếm nhanh bảng

### Liên quan đến **NGƯỜI DÙNG**:

```
users → user_roles → roles
      → user_profiles
      → user_verification_tokens
      → user_sessions
      → notifications
      → admin_audit_logs
```

### Liên quan đến **KHÓA HỌC**:

```
course_categories → courses
                 → course_modules → course_lessons → lesson_resources
                                 → lesson_progress
                                 → video_watch_logs
                 → course_enrollments
```

### Liên quan đến **ĐÁNH GIÁ**:

```
quizzes → quiz_questions → quiz_options → quiz_answers
       → quiz_attempts

assignments → assignment_submissions → code_reviews
coding_labs → coding_lab_attempts → code_reviews
```

### Liên quan đến **TUYỂN DỤNG**:

```
companies → company_members
         → jobs → job_skills
              → job_applications

resumes → resume_educations
       → resume_experiences
       → resume_skills
       → job_applications
```

### Liên quan đến **THANH TOÁN**:

```
orders → order_items
      → payments
      → coupons (áp dụng mã giảm giá)
```

---

## 📂 File được tạo

```
📦 03_database/
 ├── 📄 00_OVERVIEW_BILINGUAL.puml
 ├── 📄 01_AUTH_BILINGUAL.puml
 ├── 📄 02_LEARNING_BILINGUAL.puml
 ├── 📄 03_PLACEMENT_AND_AI_ROADMAP_BILINGUAL.puml
 ├── 📄 04_ASSESSMENT_BILINGUAL.puml
 ├── 📄 05_RECRUITMENT_BILINGUAL.puml
 ├── 📄 06_PAYMENT_BILINGUAL.puml
 ├── 📄 BILINGUAL_README.md (Tài liệu chi tiết)
 └── 📄 QUICK_REFERENCE.md (File này - Tham chiếu nhanh)
```

---

## 🚀 Bắt đầu nhanh

### 1. Mở file trong VSCode

- **Cài đặt extension**: PlantUML extension by jebbs
- **Mở file**: `01_AUTH_BILINGUAL.puml`
- **Preview**: Alt + D (hoặc Cmd + D trên Mac)

### 2. Đọc biểu đồ

- **Tên Việt**: Để hiểu bảng là gì
- **Tên Anh**: Để dùng trong SQL/Code
- **[Mô tả]**: Để hiểu trường là gì

### 3. Viết SQL

```sql
-- Lấy thông tin người dùng (từ users)
SELECT id, full_name, email FROM users WHERE status = 'active';

-- Lấy hồ sơ người dùng (từ user_profiles)
SELECT * FROM user_profiles WHERE education_level = 'Bachelor';
```

---

## 💾 Cách lưu/export

### Xuất sang PNG/SVG

1. Click chuột phải trên file `.puml`
2. Chọn `Export Current Diagram as ...`
3. Chọn định dạng (PNG, SVG, PDF)

### Share với team

- Copy file `.puml` vào dự án
- Hoặc paste link PlantUML online editor

---

## ✅ Checklist cho Dev

- [ ] Đã cài PlantUML extension
- [ ] Đã mở file `00_OVERVIEW_BILINGUAL.puml` để hiểu tổng quan
- [ ] Đã xem file `01_AUTH_BILINGUAL.puml`
- [ ] Đã xem file tương ứng với feature đang làm
- [ ] Bookmark QUICK_REFERENCE.md để tham chiếu nhanh
- [ ] Hiểu tên Tiếng Anh của bảng/trường cần dùng

---

**Generated**: 2026-06-05
**Format**: PlantUML (Open source)
**Language**: Vietnamese + English (Bilingual)
