# Kế Hoạch Lập Trình (Implementation Plan) Các API #21 – #25

> **Mục tiêu:** Xây dựng kế hoạch lập trình chi tiết cho các API `#21` đến `#25` trong `apps/study-server`, tuân thủ tuyệt đối kiến trúc module hiện có (`api_04_users_me`, `api_09_courses_curriculum`, `api_14_users_me_profile`, `api_15_courses_enrollment_status`).

---

## 1. Quy Tắc Kiến Trúc & Quy Ước Bắt Buộc Khi Lập Trình

### 1.1. Cấu trúc thư mục mỗi API
Mỗi API được đặt trong một package riêng dưới `apps/study-server/app/modules/guest/`:

```text
apps/study-server/app/modules/guest/
├── api_21_users_me_progress/
│   ├── __init__.py
│   ├── models.py     # Chỉ khai báo class Pydantic BaseModel, ConfigDict, fields
│   ├── query.py      # Chỉ chứa các hằng số chuỗi SQL (UPPER_SNAKE_CASE)
│   ├── validate.py   # Kiểm tra auth/input; chỉ trả lỗi bằng return error_response(...)
│   └── view.py       # Điều phối luồng chính, gọi DB helper, quản lý transaction & response
├── api_22_lessons_access/
│   ├── __init__.py
│   ├── models.py
│   ├── query.py
│   ├── validate.py
│   └── view.py
├── api_23_lessons_start/
│   ├── __init__.py
│   ├── models.py
│   ├── query.py
│   ├── validate.py
│   └── view.py
├── api_24_lessons_detail/
│   ├── __init__.py
│   ├── models.py
│   ├── query.py
│   ├── validate.py
│   └── view.py
└── api_25_lessons_progress/
    ├── __init__.py
    ├── models.py
    ├── query.py
    ├── validate.py
    └── view.py
```

### 1.2. Lưu ý đặc biệt về `try - except` trong `view.py` (QUAN TRỌNG)
- **Khi một khối `try` chỉ xử lý 1 loại lỗi / trả về cùng 1 kết quả lỗi**:
  - **KHÔNG** cần ghi phần tên lỗi như `SQLAlchemyError` hay `ValidationError` sau `except` (chỉ cần viết `except:`), thực hiện `db.rollback()` (nếu khối `try` có thao tác DB), `logger.exception(...)` và trả về `_internal_error(trace_id)`.
- **Trừ trường hợp 1 khối `try` trả về nhiều lỗi khác nhau** (ví dụ: trong cùng 1 khối `try` cần phân biệt `IntegrityError` trả `409 DESIGN_STATE_CONFLICT` với lỗi DB khác trả `500 DESIGN_INTERNAL_ERROR`):
  - Khi đó mới ghi rõ từng loại lỗi ở các nhánh `except IntegrityError:` / `except SQLAlchemyError:`.

**Ví dụ minh họa quy tắc `try - except` trong Plan này:**
```python
# Trường hợp 1: Khối try chỉ trả về 1 loại lỗi (500 Internal Error) -> KHÔNG ghi SQLAlchemyError
try:
    lesson_row = find_lesson_by_id(db, lesson_id=validated_lesson_id)
except:
    db.rollback()
    logger.exception("Lesson lookup failed; trace_id=%s", trace_id)
    return _internal_error(trace_id)

# Trường hợp 2: Map model cũng chỉ trả 1 loại lỗi (500 Internal Error) -> KHÔNG ghi ValidationError
try:
    data = LessonResponse.model_validate(lesson_row)
except:
    logger.exception("Lesson mapping failed; trace_id=%s", trace_id)
    return _internal_error(trace_id)
```

### 1.3. Quy ước phân tầng của Study Server
1. **`models.py`**: Chỉ chứa khai báo model (`BaseModel`), kiểu dữ liệu, giá trị mặc định. Không viết hàm helper hay logic kiểm tra tại đây.
2. **`validate.py`**:
   - Tái sử dụng `validate_current_user_request(authorization, trace_id=trace_id)` từ `app.utils.auth` để kiểm tra Bearer JWT và quyền `STUDENT`.
   - Khi dữ liệu không hợp lệ, chỉ trả lỗi bằng `return error_response(...)`, tuyệt đối không `raise HTTPException` và không truy vấn DB trong `validate.py`.
3. **`query.py`**: Chỉ chứa các biến hằng chuỗi SQL (`SELECT ...`, `INSERT ...`, `UPDATE ...`). Không import DB helper tại đây.
4. **`view.py`**:
   - Có comment tiếng Việt ngắn gọn trước mỗi bước xử lý có ý nghĩa.
   - Hàm handler chính có comment header `# API #XX <name>` ngay phía trên.
   - Mọi hàm đều có docstring tiếng Việt mô tả mục đích.
   - Với các API có ghi DB (`API #23`, `API #25`), `view.py` chịu trách nhiệm gọi `db.commit()` khi hoàn tất và `db.rollback()` khi gặp lỗi.

---

## 2. Chi Tiết Kế Hoạch Lập Trình Từng API

---

### 2.1. Plan Lập Trình API #21: `GET /api/v1/users/me/progress`

#### Bước 1: Tạo `apps/study-server/app/modules/guest/api_21_users_me_progress/models.py`
- Khai báo model query đầu vào `ProgressQuery` (`course_id: str | None = None`, `aggregate: str | None = None`).
- Khai báo model dữ liệu trả về:
  - Theo `list_api.md`, schema khai báo là `UserProfile` (có thể tái sử dụng hoặc khai báo `UserProgressProfile` khớp với `UserProfile` trong `api_04_users_me/models.py`: `id`, `full_name`, `email`, `role`, `avatar_url`, `phone`, `status`, `created_at`, `updated_at`).

#### Bước 2: Tạo `apps/study-server/app/modules/guest/api_21_users_me_progress/query.py`
- Khai báo hằng số SQL:
  - `FIND_CURRENT_USER_PROFILE`: Đọc thông tin user từ bảng `users` theo `:user_id`.
  - `FIND_USER_LESSON_PROGRESS`: Đọc tiến độ từ `lesson_progress AS lp` join `lessons AS l ON l.id = lp.lesson_id` theo `lp.user_id = :user_id` (phục vụ kiểm tra/tổng hợp tiến độ).

#### Bước 3: Tạo `apps/study-server/app/modules/guest/api_21_users_me_progress/validate.py`
- Viết hàm `validate_progress_request(authorization: str | None, *, trace_id: str) -> int | JSONResponse`:
  - Gọi `validate_current_user_request(authorization, trace_id=trace_id)`.
  - Nếu kết quả là `JSONResponse` (lỗi `401` hoặc `403`), trả về ngay `JSONResponse`.
  - Nếu hợp lệ, trả về `user_id`.

#### Bước 4: Tạo `apps/study-server/app/modules/guest/api_21_users_me_progress/view.py`
- Hàm helper truy vấn:
  - `find_current_user(db: Session, *, user_id: int) -> dict[str, Any] | None`
- Hàm điều phối chính `# API #21 users_me_progress` -> `get_user_progress(*, authorization: str | None, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse`:
  ```python
  # Xác thực Bearer token và kiểm tra quyền STUDENT.
  validated_user_id = validate_progress_request(authorization, trace_id=trace_id)
  if isinstance(validated_user_id, JSONResponse):
      return validated_user_id

  # Truy vấn thông tin người dùng hiện tại từ database.
  try:
      user_row = find_current_user(db, user_id=validated_user_id)
  except:
      db.rollback()
      logger.exception("User progress lookup failed; trace_id=%s", trace_id)
      return _internal_error(trace_id)

  # Trả lỗi 401 nếu user trong token không còn tồn tại.
  if user_row is None:
      return _authentication_error(trace_id)

  # Ánh xạ dữ liệu sang model response chuẩn.
  try:
      data = UserProfile.model_validate(user_row)
  except:
      logger.exception("User progress mapping failed; trace_id=%s", trace_id)
      return _internal_error(trace_id)

  # Trả về response thành công HTTP 200.
  return success_response(
      business_code="DESIGN_RESOURCE_RETRIEVED",
      message="Progress retrieved.",
      trace_id=trace_id,
      data=data.model_dump(mode="json"),
  )
  ```

---

### 2.2. Plan Lập Trình API #22: `GET /api/v1/lessons/{lesson_id}/access`

#### Bước 1: Tạo `apps/study-server/app/modules/guest/api_22_lessons_access/models.py`
- Khai báo `LessonResponse(BaseModel)` theo đúng reusable schema `Lesson`:
  ```python
  class LessonResponse(BaseModel):
      """Mô hình thông tin bài học trả về khi kiểm tra quyền truy cập."""

      model_config = ConfigDict(extra="ignore")

      id: int
      course_id: int
      title: str
      content: str | None = None
      video_url: str | None = None
      order: int
      status: str
  ```

#### Bước 2: Tạo `apps/study-server/app/modules/guest/api_22_lessons_access/query.py`
- Khai báo các câu SQL:
  ```python
  FIND_LESSON_BY_ID = """
  SELECT
      l.id,
      l.course_id,
      l.name AS title,
      l.content,
      l.video_url,
      l.sort_order AS "order",
      l.status
  FROM lessons AS l
  WHERE l.id = :lesson_id
  LIMIT 1
  """

  FIND_ACTIVE_ENROLLMENT = """
  SELECT
      e.id,
      e.status
  FROM enrollments AS e
  WHERE e.user_id = :user_id
    AND e.course_id = :course_id
    AND e.status IN ('ACTIVE', 'COMPLETED')
  LIMIT 1
  """
  ```

#### Bước 3: Tạo `apps/study-server/app/modules/guest/api_22_lessons_access/validate.py`
- Viết hàm `validate_lesson_access_request(authorization: str | None, lesson_id_raw: str | int, *, trace_id: str) -> tuple[int, int] | JSONResponse`:
  - Bước 1: Gọi `validate_current_user_request(authorization, trace_id=trace_id)` để lấy `user_id` (trả `401` hoặc `403` nếu lỗi).
  - Bước 2: Chuyển đổi và kiểm tra `lesson_id_raw` là số nguyên dương (`> 0`). Nếu không hợp lệ, trả về `error_response(status_code=404, business_code="DESIGN_RESOURCE_NOT_FOUND", message="Lesson not found.", trace_id=trace_id)`.
  - Trả về `(user_id, lesson_id)`.

#### Bước 4: Tạo `apps/study-server/app/modules/guest/api_22_lessons_access/view.py`
- Hàm helper:
  - `find_lesson_by_id(db: Session, *, lesson_id: int) -> dict[str, Any] | None`
  - `find_active_enrollment(db: Session, *, user_id: int, course_id: int) -> dict[str, Any] | None`
- Hàm chính `# API #22 lessons_access` -> `check_lesson_access(*, lesson_id: str | int, authorization: str | None, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse`:
  ```python
  # Xác thực token Student và kiểm tra định dạng lesson_id.
  validation = validate_lesson_access_request(
      authorization,
      lesson_id,
      trace_id=trace_id,
  )
  if isinstance(validation, JSONResponse):
      return validation
  user_id, validated_lesson_id = validation

  # Tìm bài học theo lesson_id.
  try:
      lesson_row = find_lesson_by_id(db, lesson_id=validated_lesson_id)
  except:
      db.rollback()
      logger.exception("Lesson lookup failed; trace_id=%s", trace_id)
      return _internal_error(trace_id)

  # Nếu bài học không tồn tại hoặc thiếu course_id, trả về 404.
  if lesson_row is None or lesson_row.get("course_id") is None:
      return _not_found_error(trace_id)

  # Kiểm tra học viên đã ghi danh vào khóa học chứa bài học này chưa.
  try:
      enrollment = find_active_enrollment(
          db,
          user_id=user_id,
          course_id=lesson_row["course_id"],
      )
  except:
      db.rollback()
      logger.exception("Enrollment access check failed; trace_id=%s", trace_id)
      return _internal_error(trace_id)

  # Nếu chưa ghi danh hợp lệ, trả về 403 kèm lý do từ chối truy cập.
  if enrollment is None:
      return _access_denied_error(trace_id)

  # Ánh xạ thông tin bài học sang model LessonResponse.
  try:
      data = LessonResponse.model_validate(lesson_row)
  except:
      logger.exception("Lesson access mapping failed; trace_id=%s", trace_id)
      return _internal_error(trace_id)

  # Trả về response thành công HTTP 200.
  return success_response(
      business_code="DESIGN_RESOURCE_RETRIEVED",
      message="Lesson access granted.",
      trace_id=trace_id,
      data=data.model_dump(mode="json"),
  )
  ```

---

### 2.3. Plan Lập Trình API #23: `POST /api/v1/lessons/{lesson_id}/start`

#### Bước 1: Tạo `apps/study-server/app/modules/guest/api_23_lessons_start/models.py`
- Khai báo `LessonResponse(BaseModel)` (`id`, `course_id`, `title`, `content`, `video_url`, `order`, `status`).

#### Bước 2: Tạo `apps/study-server/app/modules/guest/api_23_lessons_start/query.py`
- Do bảng `lesson_progress` trong `DB.sql` không có `UNIQUE (user_id, lesson_id)`, thực hiện UPSERT an toàn bằng bộ câu lệnh:
  ```python
  FIND_LESSON_BY_ID = """
  SELECT
      l.id,
      l.course_id,
      l.name AS title,
      l.content,
      l.video_url,
      l.sort_order AS "order",
      l.status
  FROM lessons AS l
  WHERE l.id = :lesson_id
  LIMIT 1
  """

  FIND_ACTIVE_ENROLLMENT = """
  SELECT
      e.id
  FROM enrollments AS e
  WHERE e.user_id = :user_id
    AND e.course_id = :course_id
    AND e.status IN ('ACTIVE', 'COMPLETED')
  LIMIT 1
  """

  FIND_LESSON_PROGRESS = """
  SELECT
      lp.id,
      lp.status
  FROM lesson_progress AS lp
  WHERE lp.user_id = :user_id
    AND lp.lesson_id = :lesson_id
  ORDER BY lp.id DESC
  LIMIT 1
  """

  INSERT_LESSON_PROGRESS = """
  INSERT INTO lesson_progress (
      user_id,
      lesson_id,
      status,
      progress_percent,
      last_accessed_at
  )
  VALUES (
      :user_id,
      :lesson_id,
      'IN_PROGRESS',
      0,
      CURRENT_TIMESTAMP
  )
  RETURNING id
  """

  TOUCH_LESSON_PROGRESS = """
  UPDATE lesson_progress
  SET
      status = CASE
          WHEN status = 'COMPLETED' THEN status
          ELSE 'IN_PROGRESS'
      END,
      last_accessed_at = CURRENT_TIMESTAMP
  WHERE id = :progress_id
  RETURNING id
  """
  ```

#### Bước 3: Tạo `apps/study-server/app/modules/guest/api_23_lessons_start/validate.py`
- Viết hàm `validate_lesson_start_request(authorization: str | None, lesson_id_raw: str | int, *, trace_id: str) -> tuple[int, int] | JSONResponse`:
  - Kiểm tra Bearer JWT + role `STUDENT` qua `validate_current_user_request`.
  - Kiểm tra `lesson_id_raw`: nếu không parse được sang số nguyên hoặc `<= 0` thì trả `422 DESIGN_VALIDATION_ERROR` (hoặc `404` tùy test case yêu cầu; lưu ý catalog API #23 có khai báo `422 DESIGN_VALIDATION_ERROR`).

#### Bước 4: Tạo `apps/study-server/app/modules/guest/api_23_lessons_start/view.py`
- Hàm chính `# API #23 lessons_start` -> `start_lesson(*, lesson_id: str | int, authorization: str | None, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse`:
  ```python
  # Xác thực người dùng Student và kiểm tra tham số lesson_id.
  validation = validate_lesson_start_request(
      authorization,
      lesson_id,
      trace_id=trace_id,
  )
  if isinstance(validation, JSONResponse):
      return validation
  user_id, validated_lesson_id = validation

  # Kiểm tra bài học tồn tại, quyền ghi danh và khởi tạo/cập nhật tiến độ bài học.
  try:
      lesson_row = find_lesson_by_id(db, lesson_id=validated_lesson_id)
      if lesson_row is None or lesson_row.get("course_id") is None:
          db.rollback()
          return _not_found_error(trace_id)

      enrollment = find_active_enrollment(
          db,
          user_id=user_id,
          course_id=lesson_row["course_id"],
      )
      if enrollment is None:
          db.rollback()
          return _access_denied_error(trace_id)

      existing_progress = find_lesson_progress(
          db,
          user_id=user_id,
          lesson_id=validated_lesson_id,
      )
      if existing_progress is None:
          insert_lesson_progress(db, user_id=user_id, lesson_id=validated_lesson_id)
      else:
          touch_lesson_progress(db, progress_id=existing_progress["id"])

      data = LessonResponse.model_validate(lesson_row)
      db.commit()
  except:
      db.rollback()
      logger.exception("Start lesson failed; trace_id=%s", trace_id)
      return _internal_error(trace_id)

  # Trả về response thành công HTTP 201.
  return success_response(
      business_code="DESIGN_RESOURCE_CREATED",
      message="Lesson started.",
      trace_id=trace_id,
      data=data.model_dump(mode="json"),
  )
  ```
  *(Lưu ý: Toàn bộ khối `try` ở trên chỉ trả về 1 loại lỗi duy nhất khi có exception là `500 DESIGN_INTERNAL_ERROR`, nên chỉ dùng 1 nhánh `except:` gọn gàng, không tách `except SQLAlchemyError` và `except ValidationError` riêng).*

---

### 2.4. Plan Lập Trình API #24: `GET /api/v1/lessons/{lesson_id}`

#### Bước 1: Tạo `apps/study-server/app/modules/guest/api_24_lessons_detail/models.py`
- Khai báo `LessonResponse(BaseModel)` (`id`, `course_id`, `title`, `content`, `video_url`, `order`, `status`).

#### Bước 2: Tạo `apps/study-server/app/modules/guest/api_24_lessons_detail/query.py`
- Khai báo các câu SQL:
  ```python
  FIND_PUBLISHED_LESSON_BY_ID = """
  SELECT
      l.id,
      l.course_id,
      l.name AS title,
      l.content,
      l.video_url,
      l.sort_order AS "order",
      l.status,
      c.status AS course_status
  FROM lessons AS l
  INNER JOIN courses AS c ON c.id = l.course_id
  WHERE l.id = :lesson_id
  LIMIT 1
  """

  FIND_ACTIVE_ENROLLMENT = """
  SELECT
      e.id
  FROM enrollments AS e
  WHERE e.user_id = :user_id
    AND e.course_id = :course_id
    AND e.status IN ('ACTIVE', 'COMPLETED')
  LIMIT 1
  """
  ```

#### Bước 3: Tạo `apps/study-server/app/modules/guest/api_24_lessons_detail/validate.py`
- Viết hàm `validate_lesson_detail_request(authorization: str | None, lesson_id_raw: str | int, *, trace_id: str) -> tuple[int, int] | JSONResponse`:
  - Gọi `validate_current_user_request(authorization, trace_id=trace_id)` (trả `401` / `403`).
  - Kiểm tra `lesson_id_raw` là số nguyên dương; nếu sai trả `404 DESIGN_RESOURCE_NOT_FOUND`.

#### Bước 4: Tạo `apps/study-server/app/modules/guest/api_24_lessons_detail/view.py`
- Hàm chính `# API #24 lessons_detail` -> `get_lesson_detail(*, lesson_id: str | int, authorization: str | None, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse`:
  ```python
  # Xác thực token Student và kiểm tra tham số lesson_id.
  validation = validate_lesson_detail_request(
      authorization,
      lesson_id,
      trace_id=trace_id,
  )
  if isinstance(validation, JSONResponse):
      return validation
  user_id, validated_lesson_id = validation

  # Truy vấn bài học và trạng thái khóa học cha.
  try:
      lesson_row = find_lesson_with_course(db, lesson_id=validated_lesson_id)
  except:
      db.rollback()
      logger.exception("Lesson detail lookup failed; trace_id=%s", trace_id)
      return _internal_error(trace_id)

  # Trả về 404 nếu không tìm thấy bài học hoặc chưa được PUBLISHED.
  if (
      lesson_row is None
      or lesson_row.get("status") != "PUBLISHED"
      or lesson_row.get("course_status") != "PUBLISHED"
  ):
      return _not_found_error(trace_id)

  # Kiểm tra quyền truy cập (enrollment) của học viên đối với khóa học.
  try:
      enrollment = find_active_enrollment(
          db,
          user_id=user_id,
          course_id=lesson_row["course_id"],
      )
  except:
      db.rollback()
      logger.exception("Lesson enrollment check failed; trace_id=%s", trace_id)
      return _internal_error(trace_id)

  if enrollment is None:
      return _access_denied_error(trace_id)

  # Ánh xạ dữ liệu bài học sang model LessonResponse.
  try:
      data = LessonResponse.model_validate(lesson_row)
  except:
      logger.exception("Lesson detail mapping failed; trace_id=%s", trace_id)
      return _internal_error(trace_id)

  # Trả về response thành công HTTP 200.
  return success_response(
      business_code="DESIGN_RESOURCE_RETRIEVED",
      message="Lesson retrieved.",
      trace_id=trace_id,
      data=data.model_dump(mode="json"),
  )
  ```

---

### 2.5. Plan Lập Trình API #25: `PATCH /api/v1/lessons/{lesson_id}/progress`

#### Bước 1: Tạo `apps/study-server/app/modules/guest/api_25_lessons_progress/models.py`
- Khai báo model request và response:
  ```python
  class LessonProgressUpdateRequest(BaseModel):
      """Dữ liệu đầu vào cập nhật vị trí và trạng thái tiến độ bài học."""

      model_config = ConfigDict(extra="forbid")

      position: int
      percent: int
      completed: bool


  class LessonResponse(BaseModel):
      """Mô hình bài học trả về sau khi cập nhật tiến độ."""

      model_config = ConfigDict(extra="ignore")

      id: int
      course_id: int
      title: str
      content: str | None = None
      video_url: str | None = None
      order: int
      status: str
  ```

#### Bước 2: Tạo `apps/study-server/app/modules/guest/api_25_lessons_progress/query.py`
- Khai báo các câu SQL:
  ```python
  FIND_LESSON_BY_ID = """
  SELECT
      l.id,
      l.course_id,
      l.name AS title,
      l.content,
      l.video_url,
      l.sort_order AS "order",
      l.status
  FROM lessons AS l
  WHERE l.id = :lesson_id
  LIMIT 1
  """

  FIND_ACTIVE_ENROLLMENT = """
  SELECT
      e.id
  FROM enrollments AS e
  WHERE e.user_id = :user_id
    AND e.course_id = :course_id
    AND e.status IN ('ACTIVE', 'COMPLETED')
  LIMIT 1
  """

  FIND_LESSON_PROGRESS = """
  SELECT
      lp.id,
      lp.status,
      lp.progress_percent,
      lp.completed_at
  FROM lesson_progress AS lp
  WHERE lp.user_id = :user_id
    AND lp.lesson_id = :lesson_id
  ORDER BY lp.id DESC
  LIMIT 1
  """

  INSERT_LESSON_PROGRESS_WITH_STATE = """
  INSERT INTO lesson_progress (
      user_id,
      lesson_id,
      status,
      progress_percent,
      last_accessed_at,
      completed_at
  )
  VALUES (
      :user_id,
      :lesson_id,
      :status,
      :progress_percent,
      CURRENT_TIMESTAMP,
      CASE WHEN :completed THEN CURRENT_TIMESTAMP ELSE NULL END
  )
  RETURNING id
  """

  UPDATE_LESSON_PROGRESS_BY_ID = """
  UPDATE lesson_progress
  SET
      status = :status,
      progress_percent = :progress_percent,
      last_accessed_at = CURRENT_TIMESTAMP,
      completed_at = CASE
          WHEN :completed THEN COALESCE(completed_at, CURRENT_TIMESTAMP)
          ELSE completed_at
      END
  WHERE id = :progress_id
  RETURNING id
  """
  ```

#### Bước 3: Tạo `apps/study-server/app/modules/guest/api_25_lessons_progress/validate.py`
- Viết hàm `validate_lesson_progress_request(authorization: str | None, lesson_id_raw: str | int, payload: LessonProgressUpdateRequest, *, trace_id: str) -> tuple[int, int, LessonProgressUpdateRequest] | JSONResponse`:
  - Bước 1: Kiểm tra Bearer JWT + role `STUDENT` qua `validate_current_user_request`.
  - Bước 2: Kiểm tra `lesson_id_raw` là số nguyên dương (nếu không hợp lệ trả `404` hoặc `422`).
  - Bước 3: Kiểm tra giá trị `payload.position >= 0` và `0 <= payload.percent <= 100`. Nếu vi phạm, gom `ErrorDetail` và trả về `error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", ...)`.

#### Bước 4: Tạo `apps/study-server/app/modules/guest/api_25_lessons_progress/view.py`
- Hàm chính `# API #25 lessons_progress` -> `update_lesson_progress(*, lesson_id: str | int, progress_data: LessonProgressUpdateRequest, authorization: str | None, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse`:
  ```python
  # Xác thực người dùng Student, lesson_id và dữ liệu tiến độ gửi lên.
  validation = validate_lesson_progress_request(
      authorization,
      lesson_id,
      progress_data,
      trace_id=trace_id,
  )
  if isinstance(validation, JSONResponse):
      return validation
  user_id, validated_lesson_id, validated_payload = validation

  # Xác định trạng thái đích dựa theo cờ completed (AC-14).
  target_status = "COMPLETED" if validated_payload.completed else "IN_PROGRESS"

  # Kiểm tra bài học, quyền ghi danh và cập nhật tiến độ trong một transaction.
  try:
      lesson_row = find_lesson_by_id(db, lesson_id=validated_lesson_id)
      if lesson_row is None or lesson_row.get("course_id") is None:
          db.rollback()
          return _not_found_error(trace_id)

      enrollment = find_active_enrollment(
          db,
          user_id=user_id,
          course_id=lesson_row["course_id"],
      )
      if enrollment is None:
          db.rollback()
          return _access_denied_error(trace_id)

      existing_progress = find_lesson_progress(
          db,
          user_id=user_id,
          lesson_id=validated_lesson_id,
      )
      if existing_progress is None:
          insert_lesson_progress_state(
              db,
              user_id=user_id,
              lesson_id=validated_lesson_id,
              status=target_status,
              progress_percent=validated_payload.percent,
              completed=validated_payload.completed,
          )
      else:
          update_lesson_progress_state(
              db,
              progress_id=existing_progress["id"],
              status=target_status,
              progress_percent=validated_payload.percent,
              completed=validated_payload.completed,
          )

      data = LessonResponse.model_validate(lesson_row)
      db.commit()
  except:
      db.rollback()
      logger.exception("Update lesson progress failed; trace_id=%s", trace_id)
      return _internal_error(trace_id)

  # Trả về response thành công HTTP 200.
  return success_response(
      business_code="DESIGN_RESOURCE_UPDATED",
      message="Lesson progress updated.",
      trace_id=trace_id,
      data=data.model_dump(mode="json"),
  )
  ```

---

## 3. Kế Hoạch Đăng Ký Route Trong `apps/study-server/app/api/v1.py`

Thêm khai báo import và đăng ký 5 route mới vào `app/api/v1.py` theo đúng chuẩn mỏng (thin router):

1. **`GET /users/me/progress`** (`status.HTTP_200_OK`) -> gọi `get_user_progress(...)`
2. **`GET /lessons/{lesson_id}/access`** (`status.HTTP_200_OK`) -> gọi `check_lesson_access(...)`
3. **`POST /lessons/{lesson_id}/start`** (`status.HTTP_201_CREATED`) -> gọi `start_lesson(...)`
4. **`GET /lessons/{lesson_id}`** (`status.HTTP_200_OK`) -> gọi `get_lesson_detail(...)`
5. **`PATCH /lessons/{lesson_id}/progress`** (`status.HTTP_200_OK`) -> gọi `update_lesson_progress(...)`

---

## 4. Kế Hoạch Viết Unit Test & Kiểm Thử (`apps/study-server/tests/modules/guest/`)

Tạo 5 thư mục test tương ứng dưới `apps/study-server/tests/modules/guest/`:
- `api_21_users_me_progress/test_users_me_progress.py`
- `api_22_lessons_access/test_lessons_access.py`
- `api_23_lessons_start/test_lessons_start.py`
- `api_24_lessons_detail/test_lessons_detail.py`
- `api_25_lessons_progress/test_lessons_progress.py`

### Các kịch bản test bắt buộc cho mỗi API:
1. **Happy Path (`200` / `201`)**:
   - Token `STUDENT` hợp lệ, dữ liệu DB đầy đủ -> trả đúng `businessCode`, `data`, `traceId` (và kiểm tra `db.commit()` được gọi ở API `#23`, `#25`).
2. **Authentication Error (`401 DESIGN_AUTHENTICATION_REQUIRED`)**:
   - Không truyền Header `Authorization`, sai scheme `Bearer`, hoặc token hết hạn/sai chữ ký.
3. **Authorization Error (`403 DESIGN_ACCESS_DENIED`)**:
   - Token có role `MENTOR` / `ADMIN` (không phải `STUDENT`).
   - Với API `#22` – `#25`: User là `STUDENT` nhưng chưa có bản ghi `enrollments` hợp lệ trong khóa học chứa bài học đó.
4. **Not Found Error (`404 DESIGN_RESOURCE_NOT_FOUND`)**:
   - Với API `#22` – `#25`: `lesson_id` không tồn tại trong DB hoặc không hợp lệ.
5. **Validation Error (`422 DESIGN_VALIDATION_ERROR`)**:
   - Với API `#23`, `#25`: Dữ liệu đầu vào sai kiểu, thiếu trường bắt buộc (`position`, `percent`, `completed`) hoặc nằm ngoài miền hợp lệ.
6. **Database / Internal Error (`500 DESIGN_INTERNAL_ERROR`)**:
   - Giả lập exception khi truy vấn DB hoặc khi map dữ liệu -> xác nhận `db.rollback()` được gọi và không làm lộ chi tiết lỗi SQL ra ngoài response.
