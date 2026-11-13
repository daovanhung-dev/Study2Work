# Phân Tích Tác Dụng & Nghiệp Vụ Các API #21 – #25 (Study Server)

> **Phạm vi:** Phân tích 5 API thuộc nhóm `STUDENT / LEARNING & INTERACTION` (`#21` đến `#25`) trong `apps/study-server`.
>
> **Nguồn đối chiếu:**
> - Danh mục API chuẩn: [`docs/lists/list_api.md`](../../../../lists/list_api.md) (`APPROVED_DESIGN_CONTRACT`)
> - Chỉ mục Activity / Use Case: [`00_AC_API_INDEX.md`](../../../../apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) (`AC-13`, `AC-14`, `AC-15`, `AC-18`)
> - Thiết kế bảng & DDL: [`DB_UNICA_TABLES.md`](../../../../apps/study-server/docs/diagrams/DB_UNICA_TABLES.md), [`DB.sql`](../../../../infra/postgres/study-server/DB.sql)
> - Detail Design (DD Draft): [`21_users_me_progress`](../../../../apps/study-server/docs/dd/21_users_me_progress/02_Overview.md), [`22_lessons_access`](../../../../apps/study-server/docs/dd/22_lessons_access/02_Overview.md), [`23_lessons_start`](../../../../apps/study-server/docs/dd/23_lessons_start/02_Overview.md), [`24_lessons_detail`](../../../../apps/study-server/docs/dd/24_lessons_detail/02_Overview.md), [`25_lessons_progress`](../../../../apps/study-server/docs/dd/25_lessons_progress/02_Overview.md)
> - Trạng thái Runtime hiện tại (`apps/study-server/app/api/v1.py`): Cả 5 API đều **`UNWIRED / NOT_FOUND`** (chưa được lập trình và đăng ký vào router).

---

## 1. Bức Tranh Tổng Thể: Nhóm API #21 – #25 Giải Quyết Bài Toán Gì?

Trong hệ thống học trực tuyến (Study), sau khi học viên (`Student`) đã đăng ký khóa học (`enrollments`), học viên bước vào **vòng đời học tập và theo dõi tiến độ**. Nhóm 5 API từ `#21` đến `#25` đảm nhận trọn vẹn luồng cốt lõi này:

1. **Theo dõi tiến độ tổng quan (`API #21`)**: Giúp học viên nhìn thấy bức tranh tổng thể mình đã học được bao nhiêu phần trăm ở các khóa học đã ghi danh (dùng ở màn hình *Khóa học của tôi* `AC-13` và *Dashboard tiến độ* `AC-18`).
2. **Kiểm soát cổng vào bài học (`API #22`)**: Khi học viên bấm vào một bài học (`lesson`), hệ thống kiểm tra xem học viên đã ghi danh khóa học chứa bài đó chưa và có đạt điều kiện tiên quyết (`prerequisite`) hay không trước khi cho phép vào học (`AC-14`).
3. **Khởi tạo phiên học bài học (`API #23`)**: Ngay khi vượt qua bước kiểm tra quyền truy cập, hệ thống ghi nhận học viên đã bắt đầu học bài này (khởi tạo/cập nhật trạng thái `IN_PROGRESS` trong bảng `lesson_progress`) (`AC-14`).
4. **Tải nội dung chính của bài học (`API #24`)**: Trả về dữ liệu bài học (tiêu đề, nội dung chữ `content`, đường dẫn video `video_url`, thứ tự bài học `order`, trạng thái) để trình phát (player/viewer) hiển thị cho học viên (`AC-14`, `AC-15`).
5. **Lưu vị trí học và đánh dấu hoàn thành (`API #25`)**: Trong quá trình học viên xem video/đọc bài hoặc khi học xong, client định kỳ/cuối bài gọi API này để lưu lại vị trí (`position`), phần trăm hoàn thành (`percent`), và cờ hoàn thành (`completed` -> chuyển trạng thái sang `COMPLETED` hoặc giữ `IN_PROGRESS`) (`AC-14`).

### Sơ đồ luồng phối hợp giữa các API

```text
[Màn hình Khóa học của tôi (AC-13) / Dashboard tiến độ (AC-18)]
   ├── Gọi API #20 (GET /users/me/courses)  ──> Lấy danh sách khóa học đã đăng ký
   └── Gọi API #21 (GET /users/me/progress) ──> Lấy tiến độ tổng hợp để ghép (merge) trên UI

[Khi Student bấm vào học 1 bài học (AC-14 & AC-15)]
   │
   ├─ Bước 1: Gọi API #22 (GET /lessons/{lesson_id}/access)
   │          └─ Kiểm tra quyền học (Enrollment / Prerequisite)
   │             ├─ Nếu không đủ quyền -> Trả 403 DESIGN_ACCESS_DENIED (dừng luồng)
   │             └─ Nếu hợp lệ (200)   -> Đi tiếp Bước 2
   │
   ├─ Bước 2: Gọi API #23 (POST /lessons/{lesson_id}/start)
   │          └─ Ghi nhận bắt đầu học: UPSERT lesson_progress (status = 'IN_PROGRESS')
   │
   ├─ Bước 3: Gọi API #24 (GET /lessons/{lesson_id})
   │          └─ Nạp nội dung chính của bài học (title, content, video_url, order, status)
   │          └─ (Kết hợp cùng API #26 lấy resources đính kèm & API #27 tìm bài tiếp theo ở AC-15)
   │
   └─ Bước 4: Gọi API #25 (PATCH /lessons/{lesson_id}/progress)
              └─ Lưu vị trí đang học (position), phần trăm (percent) và trạng thái hoàn thành:
                 ├─ completed = true  -> status = 'COMPLETED', cập nhật completed_at
                 └─ completed = false -> giữ status = 'IN_PROGRESS'
```

---

## 2. Phân Tích Chi Tiết Từng API (21 – 25)

### 2.1. API #21 — Lấy tiến độ tổng hợp / tổng quan (`GET /api/v1/users/me/progress`)

- **Tác dụng nghiệp vụ**:
  - **Trong `AC-13` (Xem khóa học đã đăng ký)**: Client gọi song song hoặc nối tiếp `API #20` (`GET /api/v1/users/me/courses`) và `API #21` (`GET /api/v1/users/me/progress`), sau đó ghép (`merge`) danh sách khóa học với dữ liệu tiến độ để hiển thị phần trăm hoàn thành của từng khóa học.
  - **Trong `AC-18` (Theo dõi tiến độ học tập)**: Cung cấp số liệu tiến độ tổng hợp theo `user_id` để hiển thị trên trang Dashboard trước khi học viên bấm vào xem chi tiết từng khóa học (`API #37`) hoặc thành tích (`API #38`).
- **Quyền truy cập (Auth / RBAC)**:
  - Yêu cầu Header `Authorization: Bearer <jwt>` với `role = STUDENT` (sử dụng helper chung `validate_current_user_request` từ `app/utils/auth.py`).
- **Đầu vào (Input)**:
  - Header: `Authorization: Bearer <token>`
  - Query: Theo `list_api.md` ghi `query{course_id list hoặc aggregate?:string}`.
- **Đầu ra (Output) & Mã trạng thái**:
  - Thành công: `200 OK` — `businessCode = "DESIGN_RESOURCE_RETRIEVED"`.
  - Lỗi:
    - `401 DESIGN_AUTHENTICATION_REQUIRED`: Thiếu hoặc sai Bearer JWT, hoặc không tìm thấy user.
    - `403 DESIGN_ACCESS_DENIED`: Token hợp lệ nhưng role không phải `STUDENT`.
    - `500 DESIGN_INTERNAL_ERROR`: Lỗi truy vấn cơ sở dữ liệu hoặc lỗi ánh xạ dữ liệu.
- **Bảng DB liên quan**:
  - Đọc chủ yếu từ `lesson_progress` (kết hợp `lessons`, `courses`, `enrollments` và `users`).
- **Điểm cần lưu ý (`DISCREPANCY` / `SOURCE_REQUIRED`)**:
  - Trong `list_api.md`, cột Success response của API #21 đang ghi là `ApiEnvelope<UserProfile>`, trong khi mục đích của `AC-13`/`AC-18` là lấy tiến độ học tập (`lesson_progress`). Khi lập trình thực tế cần chú ý xem yêu cầu test/leader giữ schema `UserProfile` theo đúng bảng catalog hay trả kèm/trả theo schema tiến độ tổng hợp.
  - Cú pháp query parameter `course_id` (truyền chuỗi phân tách dấu phẩy hay danh sách) và `aggregate` trong catalog chưa ràng buộc lỗi `422`.

---

### 2.2. API #22 — Kiểm tra quyền truy cập bài học (`GET /api/v1/lessons/{lesson_id}/access`)

- **Tác dụng nghiệp vụ**:
  - Đóng vai trò là **cổng kiểm soát quyền (Access Gate)** mở đầu cho luồng `AC-14` (Học bài học).
  - Trước khi cho phép học viên bắt đầu học (`API #23`) hoặc tải nội dung bài học (`API #24`), hệ thống xác minh:
    1. Bài học `lesson_id` có tồn tại không? (Nếu không tồn tại -> trả `404`).
    2. Học viên hiện tại (lấy `user_id` từ JWT) đã ghi danh (`enrollments`) hợp lệ vào khóa học (`course_id`) chứa bài học đó chưa? (Nếu chưa ghi danh hoặc không đủ điều kiện -> trả `403`).
- **Quyền truy cập (Auth / RBAC)**:
  - Yêu cầu Header `Authorization: Bearer <jwt>` với `role = STUDENT`.
- **Đầu vào (Input)**:
  - Header: `Authorization: Bearer <token>`
  - Path parameter: `lesson_id: int64!` (bắt buộc).
- **Đầu ra (Output) & Mã trạng thái**:
  - Thành công: `200 OK` — `businessCode = "DESIGN_RESOURCE_RETRIEVED"`, trả về `ApiEnvelope<Lesson>` (`id`, `course_id`, `title`, `content`, `video_url`, `order`, `status`).
  - Lỗi:
    - `401 DESIGN_AUTHENTICATION_REQUIRED`: Thiếu/sai JWT.
    - `403 DESIGN_ACCESS_DENIED`: Không phải `STUDENT` hoặc chưa đăng ký khóa học (`enrollments`) / chưa đủ điều kiện học bài này.
    - `404 DESIGN_RESOURCE_NOT_FOUND`: `lesson_id` không hợp lệ hoặc không tìm thấy bài học.
    - `500 DESIGN_INTERNAL_ERROR`: Lỗi DB hoặc lỗi mapping model.
- **Bảng DB liên quan (Read-only)**:
  - `lessons` (đọc thông tin bài học theo `lesson_id`, map `name -> title`, `sort_order -> order`).
  - `enrollments` (kiểm tra bản ghi `user_id` + `course_id` có trạng thái hợp lệ như `ACTIVE`/`COMPLETED`).

---

### 2.3. API #23 — Khởi tạo / lưu lần bắt đầu học (`POST /api/v1/lessons/{lesson_id}/start`)

- **Tác dụng nghiệp vụ**:
  - Là bước thứ 2 trong `AC-14` (ngay sau khi `API #22` cho phép truy cập).
  - Đánh dấu học viên bắt đầu vào học bài `lesson_id` bằng thao tác ghi dữ liệu (**UPSERT** vào bảng `lesson_progress`):
    - Nếu học viên chưa từng có bản ghi tiến độ ở bài học này: Tạo mới (`INSERT`) bản ghi `lesson_progress` với `status = 'IN_PROGRESS'`, `progress_percent = 0`, `last_accessed_at = NOW()`.
    - Nếu học viên đã có bản ghi tiến độ ở bài học này: Cập nhật (`UPDATE`) `last_accessed_at = NOW()` (và đặt `status = 'IN_PROGRESS'` nếu bài học chưa `COMPLETED`, bảo toàn tiến độ cũ).
- **Quyền truy cập (Auth / RBAC)**:
  - Yêu cầu Header `Authorization: Bearer <jwt>` với `role = STUDENT`.
  - Cần kiểm tra bài học tồn tại (`404`) và học viên có quyền học khóa học đó (`403`) để tránh trường hợp client gọi thẳng `API #23` mà bỏ qua `API #22`.
- **Đầu vào (Input)**:
  - Header: `Authorization: Bearer <token>`
  - Path parameter: `lesson_id: int64!` (không có request body).
- **Đầu ra (Output) & Mã trạng thái**:
  - Thành công: `201 Created` — `businessCode = "DESIGN_RESOURCE_CREATED"`, trả về `ApiEnvelope<Lesson>`.
  - Lỗi:
    - `401 DESIGN_AUTHENTICATION_REQUIRED`
    - `403 DESIGN_ACCESS_DENIED`
    - `404 DESIGN_RESOURCE_NOT_FOUND`
    - `422 DESIGN_VALIDATION_ERROR` (khi `lesson_id` truyền vào không hợp lệ nếu áp dụng rule validate 422)
    - `500 DESIGN_INTERNAL_ERROR` (lỗi DB/mapping -> phải `db.rollback()`).
- **Bảng DB liên quan (Read & Write)**:
  - Đọc: `lessons`, `enrollments`, `lesson_progress`.
  - Ghi: `lesson_progress` (có `db.commit()` khi thành công và `db.rollback()` khi lỗi).
- **Điểm cần lưu ý (`DISCREPANCY`)**:
  - Trong `DB.sql`, bảng `lesson_progress` chỉ khai báo `id BIGSERIAL PRIMARY KEY` mà **chưa có `UNIQUE (user_id, lesson_id)`**. Do đó, thay vì dùng `INSERT ... ON CONFLICT (user_id, lesson_id) DO UPDATE` (sẽ lỗi trên PostgreSQL nếu thiếu unique constraint), khi lập trình nên kiểm tra bản ghi tồn tại bằng `SELECT` trước rồi nhánh sang `UPDATE` hoặc `INSERT` trong cùng 1 transaction.

---

### 2.4. API #24 — Nạp nội dung bài học / Lấy nội dung chính (`GET /api/v1/lessons/{lesson_id}`)

- **Tác dụng nghiệp vụ**:
  - Dùng trong cả `AC-14` (Học bài học - bước 3 sau khi start) và `AC-15` (Xem nội dung bài học).
  - Cung cấp toàn bộ nội dung chính của bài học (`title`, `content`, `video_url`, `order`, `status`) để hiển thị lên giao diện học tập của học viên.
  - Theo `AC-15`, API này đi kèm với `API #26` (`GET /lessons/{lesson_id}/resources` - lấy tài liệu đính kèm) và `API #27` (`GET /lessons/{lesson_id}/next` - điều hướng bài học tiếp theo).
- **Quyền truy cập (Auth / RBAC)**:
  - Yêu cầu Header `Authorization: Bearer <jwt>` với `role = STUDENT`.
  - Theo `AC-15`, cần kiểm tra học viên có quyền truy cập (`enrollments`) và trạng thái xuất bản (`PUBLISHED`) của bài học/khóa học.
- **Đầu vào (Input)**:
  - Header: `Authorization: Bearer <token>`
  - Path parameter: `lesson_id: int64!`.
- **Đầu ra (Output) & Mã trạng thái**:
  - Thành công: `200 OK` — `businessCode = "DESIGN_RESOURCE_RETRIEVED"`, trả về `ApiEnvelope<Lesson>`.
  - Lỗi:
    - `401 DESIGN_AUTHENTICATION_REQUIRED`
    - `403 DESIGN_ACCESS_DENIED` (không phải Student hoặc chưa ghi danh vào khóa học của bài học này)
    - `404 DESIGN_RESOURCE_NOT_FOUND` (bài học không tồn tại hoặc chưa `PUBLISHED`)
    - `500 DESIGN_INTERNAL_ERROR`
- **Bảng DB liên quan (Read-only)**:
  - `lessons` (kèm join/check `courses` và `enrollments`).

---

### 2.5. API #25 — Lưu vị trí và trạng thái tiến độ bài học (`PATCH /api/v1/lessons/{lesson_id}/progress`)

- **Tác dụng nghiệp vụ**:
  - Là bước thứ 4 trong `AC-14` (Học bài học).
  - Khi học viên đang xem bài giảng hoặc hoàn thành bài học, client gửi yêu cầu cập nhật tiến độ gồm 3 thông tin:
    - `position` (`int32!`): Vị trí đang học (ví dụ: giây thứ bao nhiêu của video hoặc vị trí trang).
    - `percent` (`int32!`): Phần trăm hoàn thành bài học (`0..100`).
    - `completed` (`boolean!`): Đánh dấu đã hoàn thành bài học hay chưa.
  - Quy tắc trạng thái theo sơ đồ `AC-14`:
    - Nếu `completed == True`: Đánh dấu `status = 'COMPLETED'`, cập nhật `completed_at = NOW()`, `progress_percent = percent` (hoặc `100`).
    - Nếu `completed == False`: Giữ `status = 'IN_PROGRESS'`, cập nhật `progress_percent = percent`, `last_accessed_at = NOW()`.
- **Quyền truy cập (Auth / RBAC)**:
  - Yêu cầu Header `Authorization: Bearer <jwt>` với `role = STUDENT` và quyền học trên bài học đó.
- **Đầu vào (Input)**:
  - Header: `Authorization: Bearer <token>`
  - Path parameter: `lesson_id: int64!`
  - Request Body (JSON):
    ```json
    {
      "position": 120,
      "percent": 45,
      "completed": false
    }
    ```
- **Đầu ra (Output) & Mã trạng thái**:
  - Thành công: `200 OK` — `businessCode = "DESIGN_RESOURCE_UPDATED"`, trả về `ApiEnvelope<Lesson>`.
  - Lỗi:
    - `401 DESIGN_AUTHENTICATION_REQUIRED`
    - `403 DESIGN_ACCESS_DENIED`
    - `404 DESIGN_RESOURCE_NOT_FOUND`
    - `422 DESIGN_VALIDATION_ERROR` (sai kiểu dữ liệu body, thiếu trường bắt buộc `position`, `percent`, `completed` hoặc giá trị âm / vượt ngưỡng)
    - `500 DESIGN_INTERNAL_ERROR` (lỗi DB/mapping -> `db.rollback()`).
- **Bảng DB liên quan (Read & Write)**:
  - Đọc: `lessons`, `enrollments`, `lesson_progress`.
  - Ghi: `lesson_progress` (cập nhật `status`, `progress_percent`, `last_accessed_at`, `completed_at`).
- **Điểm cần lưu ý (`DISCREPANCY` / `SOURCE_REQUIRED`)**:
  - Bảng `lesson_progress` trong `DB.sql` / `DB_UNICA_TABLES.md` chỉ có các cột: `id`, `user_id`, `lesson_id`, `status`, `progress_percent`, `last_accessed_at`, `completed_at` — **không có cột vật lý `position`**. Do đó, `position` được nhận và validate ở tầng Request model (`models.py` / `validate.py`) theo đúng contract, còn khi lưu vào bảng `lesson_progress` chỉ lưu các cột hiện có trong DB (`status`, `progress_percent`, `last_accessed_at`, `completed_at`).
  - Tương tự API #23, response trả về theo `list_api.md` là `ApiEnvelope<Lesson>` (dữ liệu bài học vừa cập nhật tiến độ).

---

## 3. Bảng Tổng Hợp So Sánh Nhanh API #21 – #25

| API | Method & Endpoint | Vai trò chính | Bảng Đọc | Bảng Ghi | Response Data (`list_api.md`) | Mã HTTP chuẩn |
|---:|---|---|---|---|---|---|
| **#21** | `GET /api/v1/users/me/progress` | Lấy tiến độ tổng hợp của Student (`AC-13`, `AC-18`) | `users`, `lesson_progress`, `lessons`, `courses` | *Không* | `ApiEnvelope<UserProfile>` *(discrepancy với progress)* | `200`, `401`, `403`, `500` |
| **#22** | `GET /api/v1/lessons/{lesson_id}/access` | Kiểm tra quyền vào học bài học (`AC-14`) | `lessons`, `enrollments` | *Không* | `ApiEnvelope<Lesson>` | `200`, `401`, `403`, `404`, `500` |
| **#23** | `POST /api/v1/lessons/{lesson_id}/start` | Khởi tạo/lưu bắt đầu học `IN_PROGRESS` (`AC-14`) | `lessons`, `enrollments`, `lesson_progress` | `lesson_progress` | `ApiEnvelope<Lesson>` | `201`, `401`, `403`, `404`, `422`, `500` |
| **#24** | `GET /api/v1/lessons/{lesson_id}` | Lấy nội dung chính của bài học (`AC-14`, `AC-15`) | `lessons`, `courses`, `enrollments` | *Không* | `ApiEnvelope<Lesson>` | `200`, `401`, `403`, `404`, `500` |
| **#25** | `PATCH /api/v1/lessons/{lesson_id}/progress` | Lưu vị trí, `%` tiến độ và trạng thái hoàn thành (`AC-14`) | `lessons`, `enrollments`, `lesson_progress` | `lesson_progress` | `ApiEnvelope<Lesson>` | `200`, `401`, `403`, `404`, `422`, `500` |

