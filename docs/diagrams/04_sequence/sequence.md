# Study2Work - Tài liệu Markdown chuyển đổi từ PlantUML

Tài liệu này gom toàn bộ các file `.puml` vào một file Markdown duy nhất để tiện đọc, chỉnh sửa và chia sẻ.

## Mục lục
- [01_DangKyTaiKhoan](#01-dangkytaikhoan)
- [02_DangNhap](#02-dangnhap)
- [03_QuenMatKhau](#03-quenmatkhau)
- [04_QuanLyHoSo](#04-quanlyhoso)
- [05_KiemTraDauVao](#05-kiemtradauvao)
- [06_TaoLoTrinhAI](#06-taolotrinhai)
- [07_XemKhoaHoc_DangKy](#07-xemkhoahoc-dangky)
- [08_XemVideo](#08-xemvideo)
- [09_TaiTaiLieu](#09-taitailieu)
- [10_NopBaiTap](#10-nopbaitap)
- [11_LamQuiz](#11-lamquiz)
- [12_CodingLab](#12-codinglab)
- [13_ReviewCode](#13-reviewcode)
- [14_DangTinTuyenDung](#14-dangtintuyendung)
- [15_TimKiemUngVien](#15-timkiemungvien)
- [16_UngTuyenCongViec](#16-ungtuyencongviec)
- [17_ThanhToanKhoaHoc](#17-thanhtoankhoahoc)
- [18_QuanTriNguoiDung](#18-quantringuoidung)
- [19_QuanTriKhoaHoc](#19-quantrikhoahoc)
- [study2work_usecase_diagram](#study2work-usecase-diagram)

## study2work_usecase_diagram.puml

**Tiêu đề:** Study2Work - Biểu đồ Use Case

### Tác nhân
- **Khách** (`Guest`)
- **Người học** (`Learner`)
- **Người hướng dẫn** (`Mentor`)
- **Nhà tuyển dụng** (`Recruiter`)
- **Quản trị viên** (`Admin`)
- **Dịch vụ AI** (`AI`)
- **Cổng thanh toán** (`Payment`)
- **Dịch vụ thông báo** (`Notify`)

### Các nhóm chức năng
#### XÁC THỰC & TRUY CẬP
- `UC_Register` — Đăng ký tài khoản
- `UC_Login` — Đăng nhập
- `UC_Forgot` — Quên mật khẩu
- `UC_Profile` — Quản lý hồ sơ
- `UC_Roles` — Quản lý vai trò & quyền hạn

#### LỘ TRÌNH HỌC TẬP
- `UC_Placement` — Làm bài test đầu vào
- `UC_Roadmap` — Nhận lộ trình AI
- `UC_Enroll` — Đăng ký lộ trình học
- `UC_ViewCourse` — Xem nội dung khóa học
- `UC_Video` — Xem bài giảng video
- `UC_Live` — Tham gia buổi học trực tuyến
- `UC_Materials` — Tải tài liệu
- `UC_Progress` — Theo dõi tiến độ

#### THỰC HÀNH & ĐÁNH GIÁ
- `UC_Submit` — Nộp bài tập
- `UC_Quiz` — Làm bài quiz
- `UC_Lab` — Thực hiện lab lập trình
- `UC_Feedback` — Xem phản hồi
- `UC_CreateAssignment` — Tạo bài tập
- `UC_Grade` — Chấm bài nộp
- `UC_CodeReview` — Review code

#### HỆ THỐNG DỰ ÁN NHÓM
- `UC_CreateProject` — Tạo dự án nhóm
- `UC_JoinProject` — Tham gia dự án nhóm
- `UC_Sprint` — Quản lý nhiệm vụ sprint
- `UC_PR` — Gửi pull request
- `UC_TeamProgress` — Xem tiến độ nhóm

#### ĐÁNH GIÁ KỸ NĂNG
- `UC_SkillMatrix` — Đánh giá ma trận kỹ năng
- `UC_TechSkill` — Đánh giá kỹ năng kỹ thuật
- `UC_SoftSkill` — Đánh giá kỹ năng mềm
- `UC_Performance` — Tạo báo cáo
- `UC_Analytics` — Xem phân tích

#### HỒ SƠ CÁ NHÂN & NGHỀ NGHIỆP
- `UC_Portfolio` — Xây dựng portfolio
- `UC_CV` — Xây dựng CV
- `UC_Interview` — Luyện phỏng vấn
- `UC_CVAI` — Nhận gợi ý CV
- `UC_PortfolioAI` — Nhận gợi ý portfolio

#### NHÀ TUYỂN DỤNG & TUYỂN DỤNG
- `UC_Company` — Tạo tài khoản công ty
- `UC_PostJob` — Đăng yêu cầu tuyển dụng
- `UC_SearchCandidate` — Tìm kiếm ứng viên
- `UC_FilterSkill` — Lọc theo kỹ năng
- `UC_ViewPortfolio` — Xem portfolio
- `UC_Shortlist` — Lọt danh sách ứng viên
- `UC_Contact` — Liên hệ ứng viên
- `UC_Apply` — Ứng tuyển công việc

#### CỘNG ĐỒNG & SỰ KIỆN
- `UC_Community` — Tham gia cộng đồng
- `UC_Workshop` — Tham gia workshop
- `UC_Challenge` — Tham gia thử thách lập trình
- `UC_MockInterview` — Tham gia mock interview
- `UC_QA` — Thảo luận & Hỏi đáp

#### THANH TOÁN & GÓI DỊCH VỤ
- `UC_Purchase` — Mua khóa học
- `UC_Mentoring` — Mua mentoring
- `UC_ProcessPayment` — Xử lý thanh toán
- `UC_History` — Xem lịch sử thanh toán

#### HỆ THỐNG THÔNG BÁO
- `UC_Reminder` — Gửi nhắc nhở học tập
- `UC_Deadline` — Gửi hạn nộp bài
- `UC_InterviewNotify` — Gửi thông báo phỏng vấn
- `UC_SystemNotify` — Gửi thông báo hệ thống

#### QUẢN TRỊ HỆ THỐNG
- `UC_ManageUser` — Quản lý người dùng
- `UC_ManageCourse` — Quản lý khóa học
- `UC_ManageMentor` — Quản lý mentor
- `UC_ManageCompany` — Quản lý công ty
- `UC_ManageContent` — Quản lý nội dung
- `UC_ManageReports` — Quản lý báo cáo
- `UC_Settings` — Cài đặt hệ thống

### Quan hệ chính
- `Guest --> UC_Register`
- `Guest --> UC_Login`
- `Guest --> UC_Forgot`
- `Learner --> UC_Profile`
- `Mentor --> UC_Profile`
- `Recruiter --> UC_Profile`
- `Admin --> UC_Roles`
- `Learner --> UC_Placement`
- `Learner --> UC_Roadmap`
- `Learner --> UC_Enroll`
- `Learner --> UC_ViewCourse`
- `Learner --> UC_Video`
- `Learner --> UC_Live`
- `Learner --> UC_Materials`
- `Learner --> UC_Progress`
- `UC_Placement ..> UC_Roadmap : <<bao gồm>>`
- `UC_Roadmap ..> AI : <<AI tạo>>`
- `Learner --> UC_Submit`
- `Learner --> UC_Quiz`
- `Learner --> UC_Lab`
- `Learner --> UC_Feedback`
- `Mentor --> UC_CreateAssignment`
- `Mentor --> UC_Grade`
- `Mentor --> UC_CodeReview`
- `UC_CodeReview ..> AI : <<AI hỗ trợ>>`
- `Learner --> UC_JoinProject`
- `Learner --> UC_Sprint`
- `Learner --> UC_PR`
- `Mentor --> UC_CreateProject`
- `Mentor --> UC_TeamProgress`
- `Mentor --> UC_SkillMatrix`
- `Mentor --> UC_TechSkill`
- `Mentor --> UC_SoftSkill`
- `Mentor --> UC_Performance`
- `Learner --> UC_Analytics`
- `Learner --> UC_Portfolio`
- `Learner --> UC_CV`
- `Learner --> UC_Interview`
- `Learner --> UC_CVAI`
- `Learner --> UC_PortfolioAI`
- `UC_CVAI ..> AI : <<bao gồm>>`
- `UC_PortfolioAI ..> AI : <<bao gồm>>`
- `Recruiter --> UC_Company`
- `Recruiter --> UC_PostJob`
- `Recruiter --> UC_SearchCandidate`
- `Recruiter --> UC_FilterSkill`
- `Recruiter --> UC_ViewPortfolio`
- `Recruiter --> UC_Shortlist`
- `Recruiter --> UC_Contact`
- `Learner --> UC_Apply`
- `Learner --> UC_Community`
- `Learner --> UC_Workshop`
- `Learner --> UC_Challenge`
- `Learner --> UC_MockInterview`
- `Learner --> UC_QA`
- `Mentor --> UC_Workshop`
- `Mentor --> UC_MockInterview`
- `Learner --> UC_Purchase`
- `Learner --> UC_Mentoring`
- `Learner --> UC_History`
- `UC_Purchase ..> UC_ProcessPayment : <<bao gồm>>`
- `UC_Mentoring ..> UC_ProcessPayment : <<bao gồm>>`
- `Payment --> UC_ProcessPayment`
- `Notify --> UC_Reminder`
- `Notify --> UC_Deadline`
- `Notify --> UC_InterviewNotify`
- `Notify --> UC_SystemNotify`
- `Admin --> UC_ManageUser`
- `Admin --> UC_ManageCourse`
- `Admin --> UC_ManageMentor`
- `Admin --> UC_ManageCompany`
- `Admin --> UC_ManageContent`
- `Admin --> UC_ManageReports`
- `Admin --> UC_Settings`

---

## 01_DangKyTaiKhoan.puml

**Tiêu đề:** STUDY2WORK - Sequence Diagram - Đăng ký tài khoản (DD Ready)

### Thành phần
- **Actor**: Khách truy cập (`Guest`)
- **Boundary**: Frontend UI\n(Web/Mobile) (`UI`)
- **Control**: AuthController\n/api/v1/auth (`AC`)
- **Control**: Validation Layer (`VL`)
- **Entity**: AuthService (`AS`)
- **Entity**: UserRepository (`UR`)
- **Entity**: RoleRepository (`RR`)
- **Entity**: ProfileRepository (`PR`)
- **Entity**: VerificationTokenRepository (`TR`)
- **Database**: Redis Cache (`Redis`)
- **Database**: MySQL Database (`DB`)

### Luồng chính / các giai đoạn
1. Người dùng gửi yêu cầu đăng ký
2. Kiểm tra email hoặc phone đã tồn tại
3. Hash mật khẩu
4. Tạo user
5. Gán role mặc định
6. Tạo hồ sơ mặc định
7. Sinh OTP / Verification Token
8. Cache OTP
9. Gửi email xác thực
10. Commit transaction

### Mã phản hồi / trạng thái xuất hiện trong file
201 CREATED, 400 BAD, 409 CONFLICT

---

## 02_DangNhap.puml

**Tiêu đề:** STUDY2WORK - Sequence Diagram - Đăng nhập hệ thống (Authentication Flow)

### Thành phần
- **Actor**: Người dùng (`USER`)
- **Boundary**: Auth Screen\n(Login UI) (`UI`)
- **Control**: API Gateway (`GATEWAY`)
- **Control**: AuthController (`AUTH_CONTROLLER`)
- **Control**: Validation Layer (`VALIDATOR`)
- **Control**: AuthService (`AUTH_SERVICE`)
- **Control**: JWT Provider (`JWT_PROVIDER`)
- **Control**: BCrypt Security (`BCRYPT`)
- **Control**: Session Service (`SESSION_SERVICE`)
- **Entity**: UserRepository (`USER_REPO`)
- **Entity**: SessionRepository (`SESSION_REPO`)
- **Entity**: PermissionRepository (`PERMISSION_REPO`)
- **Database**: MySQL / PostgreSQL (`DB`)

### Luồng chính / các giai đoạn
1. Người dùng nhập thông tin đăng nhập
2. Validation Layer
3. Business Authentication
4. Truy vấn người dùng
5. Kiểm tra trạng thái tài khoản
6. Verify Password
7. Transaction Begin
8. Generate JWT Token
9. Load Permission
10. Update Last Login
11. Save Token Cache
12. Commit Transaction
13. Exception Handling

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK, 401 UNAUTHORIZED, 403 FORBIDDEN, 404 NOT_FOUND, 422 VALIDATION_ERROR, 500 SYSTEM_ERROR

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB insert failed
  - Redis failed
  - Token generation failed
  - **Hành động:**
    - rollback transaction
    - write audit log
    - monitoring alert

---

## 03_QuenMatKhau.puml

**Tiêu đề:** STUDY2WORK - Sequence - Quên mật khẩu

### Thành phần
- **Actor**: Người dùng (`USER`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: AuthController (`AUTH_CONTROLLER`)
- **Control**: Validation Layer (`VALIDATOR`)
- **Control**: AuthService (`AUTH_SERVICE`)
- **Control**: PasswordResetService (`RESET_SERVICE`)
- **Control**: Notification Service (`NOTIFY_SERVICE`)
- **Entity**: UserRepository (`USER_REPO`)
- **Entity**: TokenRepository (`TOKEN_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Yêu cầu quên mật khẩu
2. VALIDATION FLOW
3. BUSINESS FLOW
4. Business Rule
5. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK, 404 NOT_FOUND, 422 VALIDATION_ERROR, 500 INTERNAL_SERVER_ERROR, 403 FORBIDDEN

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB insert thất bại
  - notification thất bại
  - token tạo lỗi
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---

## 04_QuanLyHoSo.puml

**Tiêu đề:** STUDY2WORK - Sequence - Quản lý hồ sơ

### Thành phần
- **Actor**: Người dùng (`USER`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: ProfileController (`PROFILE_CONTROLLER`)
- **Control**: Validation Layer (`VALIDATOR`)
- **Control**: ProfileService (`PROFILE_SERVICE`)
- **Entity**: UserRepository (`USER_REPO`)
- **Entity**: ProfileRepository (`PROFILE_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Lấy thông tin hồ sơ
2. Cập nhật thông tin hồ sơ
3. VALIDATION FLOW
4. BUSINESS FLOW
5. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK, 401 UNAUTHORIZED, 403 FORBIDDEN, 404 NOT_FOUND, 500 INTERNAL_SERVER_ERROR, 422 VALIDATION_ERROR

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB update thất bại
  - field validation lỗi
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---

## 05_KiemTraDauVao.puml

**Tiêu đề:** STUDY2WORK - Sequence - Kiểm tra đầu vào

### Thành phần
- **Actor**: Học viên (`LEARNER`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: PlacementController (`PLACEMENT_CONTROLLER`)
- **Control**: PlacementService (`PLACEMENT_SERVICE`)
- **Control**: ScoringService (`SCORING_SERVICE`)
- **Entity**: TestRepository (`TEST_REPO`)
- **Entity**: QuestionRepository (`QUESTION_REPO`)
- **Entity**: AttemptRepository (`ATTEMPT_REPO`)
- **Entity**: AnswerRepository (`ANSWER_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Bắt đầu test đầu vào
2. Làm bài test
3. Nộp bài test
4. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK, 401 UNAUTHORIZED, 403 FORBIDDEN, 404 NOT_FOUND, 500 INTERNAL_SERVER_ERROR

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB insert/update thất bại
  - scoring logic lỗi
  - answer validation lỗi
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---

## 06_TaoLoTrinhAI.puml

**Tiêu đề:** STUDY2WORK - Sequence - Tạo lộ trình học bằng AI

### Thành phần
- **Actor**: Học viên (`LEARNER`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: RoadmapController (`ROADMAP_CONTROLLER`)
- **Control**: Validation Layer (`VALIDATOR`)
- **Control**: RoadmapService (`ROADMAP_SERVICE`)
- **Control**: AIRoadmapService (`AI_SERVICE`)
- **Control**: AI Engine (`AI_ENGINE`)
- **Entity**: PlacementRepository (`PLACEMENT_REPO`)
- **Entity**: CourseRepository (`COURSE_REPO`)
- **Entity**: LessonRepository (`LESSON_REPO`)
- **Entity**: RoadmapRepository (`ROADMAP_REPO`)
- **Entity**: RoadmapStepRepository (`ROADMAP_STEP_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Yêu cầu tạo lộ trình
2. VALIDATION FLOW
3. BUSINESS FLOW
4. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK, 401 UNAUTHORIZED, 422 VALIDATION_ERROR, 500 INTERNAL_SERVER_ERROR

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - AI engine lỗi
  - DB insert thất bại
  - course/lesson không tồn tại
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---

## 07_XemKhoaHoc_DangKy.puml

**Tiêu đề:** STUDY2WORK - Sequence - Xem khóa học và đăng ký

### Thành phần
- **Actor**: Học viên (`LEARNER`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: CourseController (`COURSE_CONTROLLER`)
- **Control**: Validation Layer (`VALIDATOR`)
- **Control**: CourseService (`COURSE_SERVICE`)
- **Control**: EnrollmentService (`ENROLLMENT_SERVICE`)
- **Entity**: CourseRepository (`COURSE_REPO`)
- **Entity**: EnrollmentRepository (`ENROLLMENT_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Xem chi tiết khóa học
2. Đăng ký khóa học
3. VALIDATION FLOW
4. BUSINESS FLOW
5. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK, 401 UNAUTHORIZED, 404 NOT_FOUND, 500 INTERNAL_SERVER_ERROR, 201 CREATED, 403 FORBIDDEN, 409 CONFLICT, 422 VALIDATION_ERROR, 402 PAYMENT_REQUIRED

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB insert thất bại
  - course status invalid
  - user already enrolled
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---

## 08_XemVideo.puml

**Tiêu đề:** STUDY2WORK - Sequence - Xem video

### Thành phần
- **Actor**: Học viên (`LEARNER`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: LessonController (`LESSON_CONTROLLER`)
- **Control**: LessonService (`LESSON_SERVICE`)
- **Control**: ProgressService (`PROGRESS_SERVICE`)
- **Control**: CDN / Streaming Service (`CDN_SERVICE`)
- **Entity**: LessonRepository (`LESSON_REPO`)
- **Entity**: ProgressRepository (`PROGRESS_REPO`)
- **Entity**: WatchLogRepository (`WATCHLOG_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Phát video
2. Cập nhật tiến độ xem
3. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK, 401 UNAUTHORIZED, 403 FORBIDDEN, 404 NOT_FOUND, 500 INTERNAL_SERVER_ERROR

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB update thất bại
  - CDN service lỗi
  - access check lỗi
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---

## 09_TaiTaiLieu.puml

**Tiêu đề:** STUDY2WORK - Sequence - Tải tài liệu

### Thành phần
- **Actor**: Học viên (`LEARNER`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: ResourceController (`RESOURCE_CONTROLLER`)
- **Control**: DocumentService (`DOCUMENT_SERVICE`)
- **Control**: AccessService (`ACCESS_SERVICE`)
- **Control**: Storage Service (S3) (`STORAGE_SERVICE`)
- **Entity**: ResourceRepository (`RESOURCE_REPO`)
- **Entity**: LessonRepository (`LESSON_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Yêu cầu tải tài liệu
2. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK, 301 REDIRECT, 401 UNAUTHORIZED, 403 FORBIDDEN, 404 NOT_FOUND, 500 INTERNAL_SERVER_ERROR

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB query thất bại
  - storage service lỗi
  - access verification lỗi
  - **Hành động:**
    - ghi log audit
    - cảnh báo monitoring

---

## 10_NopBaiTap.puml

**Tiêu đề:** STUDY2WORK - Sequence - Nộp bài tập

### Thành phần
- **Actor**: Học viên (`LEARNER`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: AssignmentController (`ASSIGNMENT_CONTROLLER`)
- **Control**: Validation Layer (`VALIDATOR`)
- **Control**: AssignmentService (`ASSIGNMENT_SERVICE`)
- **Control**: NotificationService (`NOTIFY_SERVICE`)
- **Entity**: AssignmentRepository (`ASSIGNMENT_REPO`)
- **Entity**: SubmissionRepository (`SUBMISSION_REPO`)
- **Entity**: NotificationRepository (`NOTIFICATION_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Nộp bài tập
2. VALIDATION FLOW
3. BUSINESS FLOW
4. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK, 201 CREATED, 401 UNAUTHORIZED, 403 FORBIDDEN, 404 NOT_FOUND, 422 VALIDATION_ERROR, 409 CONFLICT, 500 INTERNAL_SERVER_ERROR

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB insert thất bại
  - assignment validation lỗi
  - notification service lỗi
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---

## 11_LamQuiz.puml

**Tiêu đề:** STUDY2WORK - Sequence - Làm quiz

### Thành phần
- **Actor**: Học viên (`LEARNER`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: QuizController (`QUIZ_CONTROLLER`)
- **Control**: QuizService (`QUIZ_SERVICE`)
- **Control**: ScoringService (`SCORING_SERVICE`)
- **Entity**: QuizRepository (`QUIZ_REPO`)
- **Entity**: QuestionRepository (`QUESTION_REPO`)
- **Entity**: OptionRepository (`OPTION_REPO`)
- **Entity**: AttemptRepository (`ATTEMPT_REPO`)
- **Entity**: AnswerRepository (`ANSWER_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Bắt đầu quiz
2. Trả lời quiz
3. Nộp quiz
4. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB insert/update thất bại
  - scoring logic lỗi
  - answer validation lỗi
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---

## 12_CodingLab.puml

**Tiêu đề:** STUDY2WORK - Sequence - Coding lab

### Thành phần
- **Actor**: Học viên (`LEARNER`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: LabController (`LAB_CONTROLLER`)
- **Control**: LabService (`LAB_SERVICE`)
- **Control**: CodeCompilerService (`COMPILER_SERVICE`)
- **Control**: TestRunnerService (`TEST_SERVICE`)
- **Control**: Code Compiler (`COMPILER`)
- **Control**: Test Engine (`TEST_ENGINE`)
- **Entity**: LabRepository (`LAB_REPO`)
- **Entity**: LabAttemptRepository (`ATTEMPT_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Mở Coding Lab
2. Viết code và Submit
3. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK, 401 UNAUTHORIZED, 403 FORBIDDEN, 404 NOT_FOUND, 422 VALIDATION_ERROR, 500 INTERNAL_SERVER_ERROR

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB update thất bại
  - compiler service lỗi
  - test runner lỗi
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---

## 13_ReviewCode.puml

**Tiêu đề:** STUDY2WORK - Sequence - Review code

### Thành phần
- **Actor**: Mentor (`MENTOR`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: ReviewController (`REVIEW_CONTROLLER`)
- **Control**: ReviewService (`REVIEW_SERVICE`)
- **Control**: NotificationService (`NOTIFY_SERVICE`)
- **Entity**: SubmissionRepository (`SUBMISSION_REPO`)
- **Entity**: LabAttemptRepository (`ATTEMPT_REPO`)
- **Entity**: CodeReviewRepository (`REVIEW_REPO`)
- **Entity**: NotificationRepository (`NOTIFICATION_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Xem danh sách cần review
2. Review bài nộp hoặc coding lab
3. VALIDATION FLOW
4. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK, 201 CREATED, 401 UNAUTHORIZED, 403 FORBIDDEN, 404 NOT_FOUND, 422 VALIDATION_ERROR, 500 INTERNAL_SERVER_ERROR

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB insert/update thất bại
  - submission/attempt không tồn tại
  - notification service lỗi
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---

## 14_DangTinTuyenDung.puml

**Tiêu đề:** STUDY2WORK - Sequence - Đăng tin tuyển dụng

### Thành phần
- **Actor**: Doanh nghiệp (`RECRUITER`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: JobController (`JOB_CONTROLLER`)
- **Control**: Validation Layer (`VALIDATOR`)
- **Control**: JobService (`JOB_SERVICE`)
- **Control**: NotificationService (`NOTIFY_SERVICE`)
- **Entity**: CompanyRepository (`COMPANY_REPO`)
- **Entity**: JobRepository (`JOB_REPO`)
- **Entity**: JobSkillRepository (`SKILL_REPO`)
- **Entity**: NotificationRepository (`NOTIFICATION_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Tạo tin tuyển dụng
2. VALIDATION FLOW
3. BUSINESS FLOW
4. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
201 CREATED, 401 UNAUTHORIZED, 403 FORBIDDEN, 422 VALIDATION_ERROR, 500 INTERNAL_SERVER_ERROR

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB insert thất bại
  - company validation lỗi
  - skill insertion lỗi
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---

## 15_TimKiemUngVien.puml

**Tiêu đề:** STUDY2WORK - Sequence - Tìm kiếm ứng viên

### Thành phần
- **Actor**: Doanh nghiệp (`RECRUITER`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: CandidateSearchController (`SEARCH_CONTROLLER`)
- **Control**: CandidateSearchService (`SEARCH_SERVICE`)
- **Control**: CandidateMatchingService (`MATCHING_SERVICE`)
- **Entity**: ResumeRepository (`RESUME_REPO`)
- **Entity**: ResumeSkillRepository (`SKILL_REPO`)
- **Entity**: ResumeExperienceRepository (`EXPERIENCE_REPO`)
- **Entity**: ResumeEducationRepository (`EDUCATION_REPO`)
- **Entity**: ApplicationRepository (`APPLICATION_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Tìm kiếm ứng viên
2. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK, 401 UNAUTHORIZED, 422 VALIDATION_ERROR, 500 INTERNAL_SERVER_ERROR

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB query thất bại
  - resume data incomplete
  - matching algorithm lỗi
  - **Hành động:**
    - ghi log audit
    - cảnh báo monitoring
    - return empty result gracefully

---

## 16_UngTuyenCongViec.puml

**Tiêu đề:** STUDY2WORK - Sequence - Ứng tuyển công việc

### Thành phần
- **Actor**: Học viên (`LEARNER`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: ApplicationController (`APPLICATION_CONTROLLER`)
- **Control**: Validation Layer (`VALIDATOR`)
- **Control**: ApplicationService (`APPLICATION_SERVICE`)
- **Control**: NotificationService (`NOTIFY_SERVICE`)
- **Entity**: JobRepository (`JOB_REPO`)
- **Entity**: ResumeRepository (`RESUME_REPO`)
- **Entity**: ApplicationRepository (`APPLICATION_REPO`)
- **Entity**: NotificationRepository (`NOTIFICATION_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Ứng tuyển công việc
2. VALIDATION FLOW
3. BUSINESS FLOW
4. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
201 CREATED, 401 UNAUTHORIZED, 403 FORBIDDEN, 404 NOT_FOUND, 409 CONFLICT, 422 VALIDATION_ERROR, 500 INTERNAL_SERVER_ERROR

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB insert thất bại
  - job validation lỗi
  - notification service lỗi
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---

## 17_ThanhToanKhoaHoc.puml

**Tiêu đề:** STUDY2WORK - Sequence - Thanh toán khóa học

### Thành phần
- **Actor**: Học viên (`LEARNER`)
- **Boundary**: Web/App UI (`UI`)
- **Control**: PaymentController (`PAYMENT_CONTROLLER`)
- **Control**: OrderService (`ORDER_SERVICE`)
- **Control**: PaymentService (`PAYMENT_SERVICE`)
- **Control**: EnrollmentService (`ENROLLMENT_SERVICE`)
- **Control**: Payment Gateway (`PAYMENT_GATEWAY`)
- **Entity**: CourseRepository (`COURSE_REPO`)
- **Entity**: CouponRepository (`COUPON_REPO`)
- **Entity**: OrderRepository (`ORDER_REPO`)
- **Entity**: PaymentRepository (`PAYMENT_REPO`)
- **Entity**: EnrollmentRepository (`ENROLLMENT_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Checkout khóa học
2. Xử lý thanh toán
3. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK, 201 CREATED, 401 UNAUTHORIZED, 403 FORBIDDEN, 404 NOT_FOUND, 422 VALIDATION_ERROR, 500 INTERNAL_SERVER_ERROR, 402 PAYMENT_REQUIRED

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - payment gateway lỗi
  - DB insert/update thất bại
  - order validation lỗi
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---

## 18_QuanTriNguoiDung.puml

**Tiêu đề:** STUDY2WORK - Sequence - Quản trị người dùng

### Thành phần
- **Actor**: Quản trị viên (`ADMIN`)
- **Boundary**: Admin UI (`UI`)
- **Control**: AdminUserController (`ADMIN_CONTROLLER`)
- **Control**: AdminUserService (`ADMIN_SERVICE`)
- **Control**: AuditService (`AUDIT_SERVICE`)
- **Entity**: UserRepository (`USER_REPO`)
- **Entity**: RoleRepository (`ROLE_REPO`)
- **Entity**: ProfileRepository (`PROFILE_REPO`)
- **Entity**: AuditLogRepository (`AUDIT_REPO`)
- **Entity**: NotificationRepository (`NOTIFICATION_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Xem quản lý người dùng
2. Cập nhật người dùng
3. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
200 OK, 401 UNAUTHORIZED, 403 FORBIDDEN, 500 INTERNAL_SERVER_ERROR, 404 NOT_FOUND, 422 VALIDATION_ERROR

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB update thất bại
  - role assignment lỗi
  - audit log thất bại
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---

## 19_QuanTriKhoaHoc.puml

**Tiêu đề:** STUDY2WORK - Sequence - Quản trị khóa học

### Thành phần
- **Actor**: Quản trị viên (`ADMIN`)
- **Boundary**: Admin UI (`UI`)
- **Control**: CourseAdminController (`COURSE_ADMIN_CONTROLLER`)
- **Control**: Validation Layer (`VALIDATOR`)
- **Control**: CourseAdminService (`COURSE_ADMIN_SERVICE`)
- **Control**: AuditService (`AUDIT_SERVICE`)
- **Entity**: CourseRepository (`COURSE_REPO`)
- **Entity**: ModuleRepository (`MODULE_REPO`)
- **Entity**: LessonRepository (`LESSON_REPO`)
- **Entity**: ResourceRepository (`RESOURCE_REPO`)
- **Entity**: QuizRepository (`QUIZ_REPO`)
- **Entity**: AssignmentRepository (`ASSIGNMENT_REPO`)
- **Entity**: LabRepository (`LAB_REPO`)
- **Entity**: AuditLogRepository (`AUDIT_REPO`)
- **Database**: MySQL DB (`DB`)

### Luồng chính / các giai đoạn
1. Tạo / sửa khóa học
2. VALIDATION FLOW
3. BUSINESS FLOW
4. ERROR FLOW

### Mã phản hồi / trạng thái xuất hiện trong file
201 CREATED, 200 OK, 401 UNAUTHORIZED, 403 FORBIDDEN, 422 VALIDATION_ERROR, 500 INTERNAL_SERVER_ERROR

### Ghi chú lỗi / rollback
- **Điều kiện 1:**
  - DB insert/update thất bại
  - nested entity save lỗi
  - audit log thất bại
  - **Hành động:**
    - rollback transaction
    - ghi log audit
    - cảnh báo monitoring

---
