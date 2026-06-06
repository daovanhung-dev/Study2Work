# STUDY2WORK - CSDL PlantUML sang Markdown

Tài liệu này gộp toàn bộ các file `.puml` và file mô tả đi kèm thành **một file Markdown duy nhất** để dễ đọc, tìm nhanh và chia sẻ cho team.

## Danh mục nguồn đã gộp
- `00_OVERVIEW.puml` — 00. Tổng quan CSDL (EN)
- `00_OVERVIEW_BILINGUAL.puml` — 00. Tổng quan CSDL (VN/EN)
- `01_AUTH.puml` — 01. Xác thực (EN)
- `01_AUTH_BILINGUAL.puml` — 01. Xác thực (VN/EN)
- `02_LEARNING.puml` — 02. Học tập (EN)
- `02_LEARNING_BILINGUAL.puml` — 02. Học tập (VN/EN)
- `03_PLACEMENT_AND_AI_ROADMAP.puml` — 03. Kiểm tra đầu vào & lộ trình AI (EN)
- `03_PLACEMENT_AND_AI_ROADMAP_BILINGUAL.puml` — 03. Kiểm tra đầu vào & lộ trình AI (VN/EN)
- `04_ASSESSMENT.puml` — 04. Đánh giá (EN)
- `04_ASSESSMENT_BILINGUAL.puml` — 04. Đánh giá (VN/EN)
- `05_RECRUITMENT.puml` — 05. Tuyển dụng (EN)
- `05_RECRUITMENT_BILINGUAL.puml` — 05. Tuyển dụng (VN/EN)
- `06_PAYMENT.puml` — 06. Thanh toán (EN)
- `06_PAYMENT_BILINGUAL.puml` — 06. Thanh toán (VN/EN)
- `BILINGUAL_README.md` — Tài liệu mô tả song ngữ
- `QUICK_REFERENCE.md` — Bảng tham chiếu nhanh
- `README.txt` — Ghi chú pack

## Tóm tắt nhanh
- Hệ thống được chia theo mô-đun: **AUTH, LEARNING, PLACEMENT & AI ROADMAP, ASSESSMENT, RECRUITMENT, PAYMENT**.
- Mỗi mô-đun có thể đọc theo 2 lớp: **tổng quan quan hệ** và **chi tiết entity / bảng / trường**.
- Các file song ngữ dùng tên bảng tiếng Việt để hiểu ngữ cảnh, và tên tiếng Anh để code / SQL.

## 1. Tổng quan kiến trúc
- **XÁC-THỰC\n(AUTH)** (`AUTH`)
- **HỌC-TẬP\n(LEARNING)** (`LEARNING`)
- **VỊ-TRÍ & LỘ-TRÌNH\n(PLACEMENT & AI ROADMAP)** (`ROADMAP`)
- **ĐÁNH-GIÁ\n(ASSESSMENT)** (`ASSESSMENT`)
- **TUYỂN-DỤNG\n(RECRUITMENT)** (`RECRUITMENT`)
- **THANH-TOÁN\n(PAYMENT)** (`PAYMENT`)

### Quan hệ mô-đun
- `AUTH` .. `PAYMENT` — người dùng
- `AUTH` .. `LEARNING` — người dùng
- `AUTH` .. `ROADMAP` — người dùng
- `LEARNING` .. `ROADMAP` — khóa học
- `LEARNING` .. `ASSESSMENT` — khóa học
- `ASSESSMENT` .. `RECRUITMENT` — người dùng
- `RECRUITMENT` .. `PAYMENT` — đơn hàng

### Mô tả từng mô-đun
- **AUTH**: Quản lý tài khoản, vai trò, phiên đăng nhập / Manage accounts, roles, sessions
- **LEARNING**: Quản lý khóa học, bài học, tài liệu / Manage courses, lessons, resources
- **ROADMAP**: Kiểm tra đầu vào, tạo lộ trình học / Placement testing, AI-powered roadmaps
- **ASSESSMENT**: Quiz, bài tập, Coding Lab, xem xét code / Quizzes, assignments, coding labs, reviews
- **RECRUITMENT**: Quản lý công ty, vị trí, hồ sơ, ứng tuyển / Manage companies, jobs, resumes, applications
- **PAYMENT**: Quản lý đơn hàng, thanh toán, mã giảm giá / Manage orders, payments, coupons

## 01. Xác thực

**Nguồn:** `01_AUTH_BILINGUAL.puml`

### Các bảng / entity
#### `users` — người_dùng\n(users)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `full_name` | `VARCHAR` | họ tên |
| 3 | `email` | `VARCHAR` | email |
| 4 | `phone` | `VARCHAR` | điện thoại |
| 5 | `password_hash` | `VARCHAR` | mã hóa mật khẩu |
| 6 | `primary_role` | `VARCHAR` | vai trò chính |
| 7 | `status` | `VARCHAR` | trạng thái |
| 8 | `created_at` | `DATETIME` | ngày tạo |
| 9 | `updated_at` | `DATETIME` | ngày cập nhật |

#### `roles` — vai_trò\n(roles)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `code` | `VARCHAR` | mã code |
| 3 | `name` | `VARCHAR` | tên vai trò |

#### `user_roles` — quyền_người_dùng\n(user_roles)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `user_id` **(PK)** | `BIGINT` |  |
| 2 | `role_id` **(PK)** | `BIGINT` |  |
| 3 | `assigned_at` | `DATETIME` | ngày gán |

#### `user_profiles` — hồ_sơ_người_dùng\n(user_profiles)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `user_id` **(PK)** | `BIGINT` |  |
| 2 | `headline` | `VARCHAR` | tiêu đề hồ sơ |
| 3 | `bio` | `TEXT` | giới thiệu bản thân |
| 4 | `location` | `VARCHAR` | địa điểm |
| 5 | `website_url` | `VARCHAR` | trang web |
| 6 | `github_url` | `VARCHAR` | GitHub |
| 7 | `linkedin_url` | `VARCHAR` | LinkedIn |
| 8 | `education_level` | `VARCHAR` | trình độ học vấn |
| 9 | `years_experience` | `TINYINT` | năm kinh nghiệm |
| 10 | `skills_summary` | `TEXT` | tóm tắt kỹ năng |

#### `user_verification_tokens` — mã_xác_thực\n(user_verification_tokens)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `user_id` | `BIGINT` |  |
| 3 | `token_type` | `VARCHAR` | loại token |
| 4 | `token_hash` | `VARCHAR` | mã hash token |
| 5 | `sent_to` | `VARCHAR` | gửi đến |
| 6 | `expires_at` | `DATETIME` | hết hạn lúc |
| 7 | `used_at` | `DATETIME` | sử dụng lúc |

#### `user_sessions` — phiên_đăng_nhập\n(user_sessions)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `user_id` | `BIGINT` |  |
| 3 | `refresh_token_hash` | `VARCHAR` | mã hash refresh token |
| 4 | `device_name` | `VARCHAR` | tên thiết bị |
| 5 | `expires_at` | `DATETIME` | hết hạn lúc |
| 6 | `revoked_at` | `DATETIME` | hủy lúc |

#### `notifications` — thông_báo\n(notifications)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `user_id` | `BIGINT` |  |
| 3 | `type` | `VARCHAR` | loại thông báo |
| 4 | `title` | `VARCHAR` | tiêu đề |
| 5 | `message` | `TEXT` | nội dung |
| 6 | `entity_type` | `VARCHAR` | loại đối tượng |
| 7 | `entity_id` | `BIGINT` | ID đối tượng |
| 8 | `is_read` | `BOOLEAN` | đã đọc |

#### `admin_audit_logs` — nhật_ký_quản_trị\n(admin_audit_logs)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `actor_user_id` | `BIGINT` | người thực hiện |
| 3 | `action` | `VARCHAR` | hành động |
| 4 | `entity_type` | `VARCHAR` | loại đối tượng |
| 5 | `entity_id` | `BIGINT` | ID đối tượng |
| 6 | `before_data` | `JSON` | dữ liệu trước |
| 7 | `after_data` | `JSON` | dữ liệu sau |
| 8 | `created_at` | `DATETIME` | ngày tạo |

### Quan hệ
- `users` ||--o{ `user_roles` — có quyền
- `roles` ||--o{ `user_roles` — được gán
- `users` ||--|| `user_profiles` — có hồ sơ
- `users` ||--o{ `user_verification_tokens` — có mã xác thực
- `users` ||--o{ `user_sessions` — có phiên
- `users` ||--o{ `notifications` — nhận
- `users` ||--o{ `admin_audit_logs` — thực hiện

## 02. Học tập

**Nguồn:** `02_LEARNING_BILINGUAL.puml`

### Các bảng / entity
#### `course_categories` — danh_mục_khóa\n(course_categories)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `parent_id` | `BIGINT` | danh mục cha |
| 3 | `code` | `VARCHAR` | mã code |
| 4 | `name` | `VARCHAR` | tên danh mục |
| 5 | `is_active` | `BOOLEAN` | kích hoạt |

#### `courses` — khóa_học\n(courses)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `category_id` | `BIGINT` | danh mục |
| 3 | `instructor_user_id` | `BIGINT` | giảng viên |
| 4 | `code` | `VARCHAR` | mã khóa |
| 5 | `slug` | `VARCHAR` | URL slug |
| 6 | `title` | `VARCHAR` | tên khóa học |
| 7 | `level` | `VARCHAR` | cấp độ |
| 8 | `price` | `DECIMAL` | giá |
| 9 | `is_free` | `BOOLEAN` | miễn phí |
| 10 | `status` | `VARCHAR` | trạng thái |

#### `course_modules` — chương_học\n(course_modules)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `course_id` | `BIGINT` | khóa học |
| 3 | `title` | `VARCHAR` | tên chương |
| 4 | `sort_order` | `INT` | thứ tự |

#### `course_lessons` — bài_học\n(course_lessons)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `course_id` | `BIGINT` | khóa học |
| 3 | `module_id` | `BIGINT` | chương |
| 4 | `lesson_type` | `VARCHAR` | loại bài |
| 5 | `title` | `VARCHAR` | tên bài |
| 6 | `duration_seconds` | `INT` | thời lượng (giây) |
| 7 | `is_preview` | `BOOLEAN` | xem trước |
| 8 | `status` | `VARCHAR` | trạng thái |

#### `lesson_resources` — tài_liệu_bài_học\n(lesson_resources)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `lesson_id` | `BIGINT` | bài học |
| 3 | `resource_type` | `VARCHAR` | loại tài liệu |
| 4 | `file_name` | `VARCHAR` | tên file |
| 5 | `file_url` | `VARCHAR` | URL file |
| 6 | `file_size_bytes` | `BIGINT` | dung lượng |
| 7 | `mime_type` | `VARCHAR` | loại file |

#### `course_enrollments` — đăng_ký_khóa\n(course_enrollments)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `user_id` | `BIGINT` | người dùng |
| 3 | `course_id` | `BIGINT` | khóa học |
| 4 | `order_id` | `BIGINT` | đơn hàng |
| 5 | `status` | `VARCHAR` | trạng thái |
| 6 | `progress_percent` | `DECIMAL` | tiến độ % |
| 7 | `completed_at` | `DATETIME` | hoàn thành lúc |

#### `lesson_progress` — tiến_độ_bài_học\n(lesson_progress)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `enrollment_id` | `BIGINT` | đăng ký |
| 3 | `lesson_id` | `BIGINT` | bài học |
| 4 | `status` | `VARCHAR` | trạng thái |
| 5 | `last_position_seconds` | `INT` | vị trí cuối (giây) |
| 6 | `completed_at` | `DATETIME` | hoàn thành lúc |

#### `video_watch_logs` — lịch_xem_video\n(video_watch_logs)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `user_id` | `BIGINT` | người dùng |
| 3 | `lesson_id` | `BIGINT` | bài học |
| 4 | `watched_seconds` | `INT` | đã xem (giây) |
| 5 | `last_position_seconds` | `INT` | vị trí cuối (giây) |
| 6 | `completed_flag` | `BOOLEAN` | đã hoàn thành |
| 7 | `watched_at` | `DATETIME` | xem lúc |

### Quan hệ
- `course_categories` ||--o{ `courses` — chứa
- `courses` ||--o{ `course_modules` — có
- `courses` ||--o{ `course_lessons` — chứa
- `course_modules` ||--o{ `course_lessons` — có
- `course_lessons` ||--o{ `lesson_resources` — có
- `courses` ||--o{ `course_enrollments` — được đăng ký
- `course_enrollments` ||--o{ `lesson_progress` — theo dõi
- `course_lessons` ||--o{ `lesson_progress` — liên quan
- `course_lessons` ||--o{ `video_watch_logs` — được xem

## 03. Kiểm tra đầu vào & Lộ trình AI

**Nguồn:** `03_PLACEMENT_AND_AI_ROADMAP_BILINGUAL.puml`

### Các bảng / entity
#### `placement_tests` — kiểm_tra_đầu_vào\n(placement_tests)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `code` | `VARCHAR` | mã code |
| 3 | `title` | `VARCHAR` | tên kiểm tra |
| 4 | `duration_minutes` | `INT` | thời gian (phút) |
| 5 | `passing_score` | `DECIMAL` | điểm đạt |
| 6 | `status` | `VARCHAR` | trạng thái |

#### `placement_questions` — câu_hỏi_đầu_vào\n(placement_questions)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `test_id` | `BIGINT` | kiểm tra |
| 3 | `question_text` | `LONGTEXT` | nội dung câu hỏi |
| 4 | `question_type` | `VARCHAR` | loại câu hỏi |
| 5 | `difficulty_level` | `VARCHAR` | độ khó |
| 6 | `score_weight` | `DECIMAL` | trọng số |
| 7 | `sort_order` | `INT` | thứ tự |

#### `placement_question_options` — lựa_chọn_câu_hỏi\n(placement_question_options)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `question_id` | `BIGINT` | câu hỏi |
| 3 | `option_text` | `VARCHAR` | nội dung lựa chọn |
| 4 | `is_correct` | `BOOLEAN` | đúng |
| 5 | `sort_order` | `INT` | thứ tự |

#### `placement_attempts` — lần_làm_kiểm_tra\n(placement_attempts)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `test_id` | `BIGINT` | kiểm tra |
| 3 | `user_id` | `BIGINT` | người dùng |
| 4 | `started_at` | `DATETIME` | bắt đầu lúc |
| 5 | `submitted_at` | `DATETIME` | nộp lúc |
| 6 | `raw_score` | `DECIMAL` | điểm thô |
| 7 | `percentile` | `DECIMAL` | phần trăm |
| 8 | `result_level` | `VARCHAR` | cấp độ kết quả |
| 9 | `status` | `VARCHAR` | trạng thái |

#### `placement_attempt_answers` — câu_trả_lời\n(placement_attempt_answers)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `attempt_id` | `BIGINT` | lần làm |
| 3 | `question_id` | `BIGINT` | câu hỏi |
| 4 | `selected_option_id` | `BIGINT` | lựa chọn |
| 5 | `answer_text` | `LONGTEXT` | nội dung trả lời |
| 6 | `is_correct` | `BOOLEAN` | đúng |
| 7 | `score_earned` | `DECIMAL` | điểm |

#### `roadmaps` — lộ_trình_học\n(roadmaps)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `user_id` | `BIGINT` | người dùng |
| 3 | `source_attempt_id` | `BIGINT` | lần kiểm tra |
| 4 | `target_role` | `VARCHAR` | vị trí mục tiêu |
| 5 | `current_level` | `VARCHAR` | cấp độ hiện tại |
| 6 | `goal_text` | `VARCHAR` | mục tiêu |
| 7 | `ai_model` | `VARCHAR` | mô hình AI |
| 8 | `status` | `VARCHAR` | trạng thái |

#### `roadmap_steps` — bước_lộ_trình\n(roadmap_steps)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `roadmap_id` | `BIGINT` | lộ trình |
| 3 | `step_order` | `INT` | thứ tự bước |
| 4 | `step_type` | `VARCHAR` | loại bước |
| 5 | `title` | `VARCHAR` | tiêu đề |
| 6 | `description` | `VARCHAR` | mô tả |
| 7 | `estimated_hours` | `DECIMAL` | giờ ước tính |
| 8 | `course_id` | `BIGINT` | khóa học |
| 9 | `lesson_id` | `BIGINT` | bài học |
| 10 | `status` | `VARCHAR` | trạng thái |

### Quan hệ
- `placement_tests` ||--o{ `placement_questions` — có
- `placement_questions` ||--o{ `placement_question_options` — có
- `placement_tests` ||--o{ `placement_attempts` — được làm
- `placement_attempts` ||--o{ `placement_attempt_answers` — trả lời
- `placement_questions` ||--o{ `placement_attempt_answers` — liên quan
- `placement_question_options` ||--o{ `placement_attempt_answers` — được chọn
- `placement_attempts` ||--o{ `roadmaps` — tạo
- `roadmaps` ||--o{ `roadmap_steps` — có

## 04. Đánh giá

**Nguồn:** `04_ASSESSMENT_BILINGUAL.puml`

### Các bảng / entity
#### `quizzes` — bài_kiểm_tra\n(quizzes)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `course_id` | `BIGINT` | khóa học |
| 3 | `title` | `VARCHAR` | tên quiz |
| 4 | `time_limit_minutes` | `INT` | giới hạn thời gian (phút) |
| 5 | `passing_score` | `DECIMAL` | điểm đạt |
| 6 | `max_attempts` | `INT` | số lần tối đa |
| 7 | `status` | `VARCHAR` | trạng thái |

#### `quiz_questions` — câu_hỏi_quiz\n(quiz_questions)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `quiz_id` | `BIGINT` | quiz |
| 3 | `question_text` | `LONGTEXT` | nội dung câu hỏi |
| 4 | `question_type` | `VARCHAR` | loại câu hỏi |
| 5 | `difficulty_level` | `VARCHAR` | độ khó |
| 6 | `score_weight` | `DECIMAL` | trọng số |
| 7 | `sort_order` | `INT` | thứ tự |

#### `quiz_options` — lựa_chọn_quiz\n(quiz_options)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `question_id` | `BIGINT` | câu hỏi |
| 3 | `option_text` | `VARCHAR` | nội dung lựa chọn |
| 4 | `is_correct` | `BOOLEAN` | đúng |
| 5 | `sort_order` | `INT` | thứ tự |

#### `quiz_attempts` — lần_làm_quiz\n(quiz_attempts)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `quiz_id` | `BIGINT` | quiz |
| 3 | `user_id` | `BIGINT` | người dùng |
| 4 | `started_at` | `DATETIME` | bắt đầu lúc |
| 5 | `submitted_at` | `DATETIME` | nộp lúc |
| 6 | `score` | `DECIMAL` | điểm |
| 7 | `passed` | `BOOLEAN` | đạt |
| 8 | `status` | `VARCHAR` | trạng thái |

#### `quiz_answers` — trả_lời_quiz\n(quiz_answers)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `attempt_id` | `BIGINT` | lần làm |
| 3 | `question_id` | `BIGINT` | câu hỏi |
| 4 | `selected_option_id` | `BIGINT` | lựa chọn |
| 5 | `answer_text` | `LONGTEXT` | nội dung trả lời |
| 6 | `is_correct` | `BOOLEAN` | đúng |
| 7 | `score_earned` | `DECIMAL` | điểm |

#### `assignments` — bài_tập\n(assignments)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `course_id` | `BIGINT` | khóa học |
| 3 | `title` | `VARCHAR` | tên bài tập |
| 4 | `due_at` | `DATETIME` | hạn chót |
| 5 | `allow_late_submission` | `BOOLEAN` | cho phép nộp muộn |
| 6 | `max_score` | `DECIMAL` | điểm tối đa |
| 7 | `status` | `VARCHAR` | trạng thái |

#### `assignment_submissions` — bài_nộp_tập\n(assignment_submissions)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `assignment_id` | `BIGINT` | bài tập |
| 3 | `user_id` | `BIGINT` | người dùng |
| 4 | `content_text` | `LONGTEXT` | nội dung |
| 5 | `file_url` | `VARCHAR` | URL file |
| 6 | `submitted_at` | `DATETIME` | nộp lúc |
| 7 | `status` | `VARCHAR` | trạng thái |
| 8 | `score` | `DECIMAL` | điểm |
| 9 | `reviewed_by` | `BIGINT` | người chấm |
| 10 | `reviewed_at` | `DATETIME` | chấm lúc |

#### `coding_labs` — bài_lab_lập_trình\n(coding_labs)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `course_id` | `BIGINT` | khóa học |
| 3 | `title` | `VARCHAR` | tên lab |
| 4 | `starter_code` | `LONGTEXT` | mã khởi đầu |
| 5 | `expected_output` | `LONGTEXT` | đầu ra mong muốn |
| 6 | `time_limit_minutes` | `INT` | giới hạn thời gian (phút) |
| 7 | `max_score` | `DECIMAL` | điểm tối đa |
| 8 | `status` | `VARCHAR` | trạng thái |

#### `coding_lab_attempts` — lần_làm_lab\n(coding_lab_attempts)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `coding_lab_id` | `BIGINT` | lab |
| 3 | `user_id` | `BIGINT` | người dùng |
| 4 | `source_code` | `LONGTEXT` | mã nguồn |
| 5 | `submitted_at` | `DATETIME` | nộp lúc |
| 6 | `compile_status` | `VARCHAR` | trạng thái biên dịch |
| 7 | `test_status` | `VARCHAR` | trạng thái test |
| 8 | `score` | `DECIMAL` | điểm |
| 9 | `status` | `VARCHAR` | trạng thái |

#### `code_reviews` — xem_xét_code\n(code_reviews)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `review_type` | `VARCHAR` | loại xem xét |
| 3 | `submission_id` | `BIGINT` | bài nộp |
| 4 | `lab_attempt_id` | `BIGINT` | lần làm lab |
| 5 | `mentor_user_id` | `BIGINT` | người mentor |
| 6 | `review_text` | `LONGTEXT` | nhận xét |
| 7 | `status` | `VARCHAR` | trạng thái |

### Quan hệ
- `quizzes` ||--o{ `quiz_questions` — có
- `quiz_questions` ||--o{ `quiz_options` — có
- `quizzes` ||--o{ `quiz_attempts` — được làm
- `quiz_attempts` ||--o{ `quiz_answers` — trả lời
- `quiz_questions` ||--o{ `quiz_answers` — liên quan
- `quiz_options` ||--o{ `quiz_answers` — được chọn
- `assignments` ||--o{ `assignment_submissions` — được nộp
- `coding_labs` ||--o{ `coding_lab_attempts` — được làm
- `assignment_submissions` ||--o{ `code_reviews` — được xem xét
- `coding_lab_attempts` ||--o{ `code_reviews` — được xem xét

## 05. Tuyển dụng

**Nguồn:** `05_RECRUITMENT_BILINGUAL.puml`

### Các bảng / entity
#### `companies` — công_ty\n(companies)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `owner_user_id` | `BIGINT` | chủ sở hữu |
| 3 | `name` | `VARCHAR` | tên công ty |
| 4 | `tax_code` | `VARCHAR` | mã số thuế |
| 5 | `website_url` | `VARCHAR` | trang web |
| 6 | `industry` | `VARCHAR` | ngành |
| 7 | `company_size` | `VARCHAR` | quy mô |
| 8 | `status` | `VARCHAR` | trạng thái |

#### `company_members` — thành_viên_công_ty\n(company_members)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `company_id` **(PK)** | `BIGINT` |  |
| 2 | `user_id` **(PK)** | `BIGINT` |  |
| 3 | `member_role` | `VARCHAR` | vai trò thành viên |
| 4 | `joined_at` | `DATETIME` | tham gia lúc |

#### `jobs` — vị_trí_công_việc\n(jobs)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `company_id` | `BIGINT` | công ty |
| 3 | `posted_by_user_id` | `BIGINT` | người đăng |
| 4 | `code` | `VARCHAR` | mã code |
| 5 | `title` | `VARCHAR` | tên vị trí |
| 6 | `slug` | `VARCHAR` | URL slug |
| 7 | `job_type` | `VARCHAR` | loại công việc |
| 8 | `work_mode` | `VARCHAR` | hình thức làm |
| 9 | `location` | `VARCHAR` | địa điểm |
| 10 | `salary_min` | `DECIMAL` | lương tối thiểu |
| 11 | `salary_max` | `DECIMAL` | lương tối đa |
| 12 | `currency` | `VARCHAR` | tiền tệ |
| 13 | `application_deadline` | `DATETIME` | hạn chót nộp đơn |
| 14 | `status` | `VARCHAR` | trạng thái |

#### `job_skills` — kỹ_năng_vị_trí\n(job_skills)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `job_id` | `BIGINT` | vị trí |
| 3 | `skill_name` | `VARCHAR` | tên kỹ năng |
| 4 | `is_must_have` | `BOOLEAN` | bắt buộc |
| 5 | `sort_order` | `INT` | thứ tự |

#### `resumes` — hồ_sơ_ứng_viên\n(resumes)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `user_id` | `BIGINT` | người dùng |
| 3 | `title` | `VARCHAR` | tiêu đề |
| 4 | `summary` | `LONGTEXT` | tóm tắt |
| 5 | `file_url` | `VARCHAR` | URL file |
| 6 | `is_default` | `BOOLEAN` | mặc định |
| 7 | `status` | `VARCHAR` | trạng thái |

#### `resume_educations` — học_vấn\n(resume_educations)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `resume_id` | `BIGINT` | hồ sơ |
| 3 | `institution` | `VARCHAR` | cơ sở giáo dục |
| 4 | `major` | `VARCHAR` | chuyên ngành |
| 5 | `degree` | `VARCHAR` | bằng cấp |
| 6 | `start_date` | `DATE` | ngày bắt đầu |
| 7 | `end_date` | `DATE` | ngày kết thúc |
| 8 | `description` | `TEXT` | mô tả |
| 9 | `sort_order` | `INT` | thứ tự |

#### `resume_experiences` — kinh_nghiệm_làm_việc\n(resume_experiences)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `resume_id` | `BIGINT` | hồ sơ |
| 3 | `company_name` | `VARCHAR` | tên công ty |
| 4 | `position_title` | `VARCHAR` | chức danh |
| 5 | `start_date` | `DATE` | ngày bắt đầu |
| 6 | `end_date` | `DATE` | ngày kết thúc |
| 7 | `description` | `TEXT` | mô tả |
| 8 | `sort_order` | `INT` | thứ tự |

#### `resume_skills` — kỹ_năng_hồ_sơ\n(resume_skills)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `resume_id` | `BIGINT` | hồ sơ |
| 3 | `skill_name` | `VARCHAR` | tên kỹ năng |
| 4 | `proficiency_level` | `VARCHAR` | cấp độ |
| 5 | `sort_order` | `INT` | thứ tự |

#### `job_applications` — đơn_ứng_tuyển\n(job_applications)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `job_id` | `BIGINT` | vị trí |
| 3 | `user_id` | `BIGINT` | người dùng |
| 4 | `resume_id` | `BIGINT` | hồ sơ |
| 5 | `cover_letter` | `LONGTEXT` | thư xin việc |
| 6 | `status` | `VARCHAR` | trạng thái |
| 7 | `applied_at` | `DATETIME` | nộp đơn lúc |
| 8 | `reviewed_at` | `DATETIME` | xem xét lúc |
| 9 | `reviewed_by` | `BIGINT` | người xem xét |

### Quan hệ
- `companies` ||--o{ `company_members` — có thành viên
- `companies` ||--o{ `jobs` — đăng
- `jobs` ||--o{ `job_skills` — yêu cầu
- `resumes` ||--o{ `resume_educations` — có
- `resumes` ||--o{ `resume_experiences` — có
- `resumes` ||--o{ `resume_skills` — có
- `jobs` ||--o{ `job_applications` — nhận
- `resumes` ||--o{ `job_applications` — sử dụng

## 06. Thanh toán

**Nguồn:** `06_PAYMENT_BILINGUAL.puml`

### Các bảng / entity
#### `coupons` — mã_giảm_giá\n(coupons)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `code` | `VARCHAR` | mã code |
| 3 | `discount_type` | `VARCHAR` | loại giảm giá |
| 4 | `discount_value` | `DECIMAL` | giá trị giảm |
| 5 | `start_at` | `DATETIME` | bắt đầu lúc |
| 6 | `end_at` | `DATETIME` | kết thúc lúc |
| 7 | `status` | `VARCHAR` | trạng thái |

#### `orders` — đơn_hàng\n(orders)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `order_no` | `VARCHAR` | số đơn hàng |
| 3 | `user_id` | `BIGINT` | người dùng |
| 4 | `coupon_id` | `BIGINT` | mã giảm giá |
| 5 | `subtotal_amount` | `DECIMAL` | tổng cộng |
| 6 | `discount_amount` | `DECIMAL` | tổng giảm |
| 7 | `total_amount` | `DECIMAL` | tổng thanh toán |
| 8 | `currency` | `VARCHAR` | tiền tệ |
| 9 | `status` | `VARCHAR` | trạng thái |
| 10 | `paid_at` | `DATETIME` | thanh toán lúc |

#### `order_items` — mặt_hàng_đơn\n(order_items)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `order_id` | `BIGINT` | đơn hàng |
| 3 | `item_type` | `VARCHAR` | loại mặt hàng |
| 4 | `item_id` | `BIGINT` | ID mặt hàng |
| 5 | `item_name` | `VARCHAR` | tên mặt hàng |
| 6 | `quantity` | `INT` | số lượng |
| 7 | `unit_price` | `DECIMAL` | giá đơn vị |
| 8 | `total_price` | `DECIMAL` | tổng giá |

#### `payments` — thanh_toán\n(payments)
| # | Trường | Kiểu | Ghi chú |
|---|---|---|---|
| 1 | `id` **(PK)** | `BIGINT` |  |
| 2 | `order_id` | `BIGINT` | đơn hàng |
| 3 | `gateway` | `VARCHAR` | cổng thanh toán |
| 4 | `gateway_transaction_id` | `VARCHAR` | ID giao dịch |
| 5 | `payment_method` | `VARCHAR` | phương thức thanh toán |
| 6 | `amount` | `DECIMAL` | số tiền |
| 7 | `currency` | `VARCHAR` | tiền tệ |
| 8 | `status` | `VARCHAR` | trạng thái |
| 9 | `paid_at` | `DATETIME` | thanh toán lúc |

### Quan hệ
- `coupons` ||--o{ `orders` — áp dụng
- `orders` ||--o{ `order_items` — chứa
- `orders` ||--o{ `payments` — có

## 7. Ghi chú tham chiếu nhanh

### Tóm tắt song ngữ
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


### Tham chiếu nhanh
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


### Ghi chú pack
STUDY2WORK CSDL PlantUML - Clean Pack

Included:
- 00_OVERVIEW.puml
- 01_AUTH.puml
- 02_LEARNING.puml
- 03_PLACEMENT_AND_AI_ROADMAP.puml
- 04_ASSESSMENT.puml
- 05_RECRUITMENT.puml
- 06_PAYMENT.puml

Why this version is easier to read:
- The schema is split by module
- Each module is rendered separately
- The same entities and relationships are preserved, but they are no longer all forced into one crowded canvas

Use 00_OVERVIEW.puml for architecture, and the module files for detailed ERD views.


_Tài liệu được tự động tổng hợp từ toàn bộ file CSDL đã cung cấp._