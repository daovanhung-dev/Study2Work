# Note các thay đổi Database cần thiết cho các màn Student (`ST-01` → `ST-26`)

> **Ngày lập**: 2026-11-26  
> **Cơ sở đối chiếu**: Schema thực tế `hoang_xuan_long` trên Neon PostgreSQL, source backend `apps/study-server`, báo cáo lỗi `Test Screen.xlsx`, và DD các màn `ST-01`..`ST-26`.

---

## 1. Các thay đổi Cột & Ràng buộc bắt buộc / khuyến nghị

### 1.1. Bảng `users` — Mở khóa trường `Bio` cho `ST-02` & `ST-03` (API `#04`, `#14`)
- **Hiện trạng**: Bảng `users` chưa có cột `bio`. Backend [api_14_users_me_profile/models.py](../../../apps/study-server/app/modules/student/api_14_users_me_profile/models.py) đang bỏ qua trường `bio` và FE `ST-03` phải khóa ô nhập giới thiệu bản thân.
- **Thay đổi cần thực hiện**:
  ```sql
  ALTER TABLE users
      ADD COLUMN IF NOT EXISTS bio TEXT NULL;
  ```
- **Tác động API**: Cập nhật `SELECT` trong API `#04` (`GET /api/v1/users/me`) và `UPDATE` trong API `#14` (`PUT /api/v1/users/me/profile`) để đọc/lưu `bio`.

---

### 1.2. Bảng `payments`, `orders`, `enrollments` — Mở khóa luồng thanh toán `ST-05` → `ST-06` → `ST-07` (API `#16`, `#17`, `#18`, `#19`)
- **Hiện trạng**:
  - Bảng `orders` (từ migration `015`) đã có `id, user_id, course_id, amount, currency, payment_provider, status, created_at, updated_at`.
  - Bảng `payments` hiện tại chỉ có `id, user_id, course_id, amount, provider, transaction_code, status, paid_at, created_at` — **thiếu liên kết tới `orders`**, **thiếu `operation_id`** để tra cứu qua API `#18`, và **thiếu `checkout_url` / `currency` / `updated_at`**.
  - Bảng `enrollments` chưa có `order_id` để truy vết khóa học trả phí được cấp quyền từ đơn hàng nào.
- **Thay đổi cần thực hiện**:
  ```sql
  -- 1. Liên kết payments với orders và hỗ trợ tracking/checkout
  ALTER TABLE payments
      ADD COLUMN IF NOT EXISTS order_id BIGINT NULL REFERENCES orders(id) ON DELETE RESTRICT,
      ADD COLUMN IF NOT EXISTS currency VARCHAR(3) NOT NULL DEFAULT 'VND',
      ADD COLUMN IF NOT EXISTS operation_id UUID NULL,
      ADD COLUMN IF NOT EXISTS checkout_url TEXT NULL,
      ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;

  CREATE INDEX IF NOT EXISTS idx_payments_order_id
      ON payments(order_id);

  CREATE INDEX IF NOT EXISTS idx_payments_operation_id
      ON payments(operation_id)
      WHERE operation_id IS NOT NULL;

  -- 2. Liên kết enrollments với orders (khóa miễn phí để NULL)
  ALTER TABLE enrollments
      ADD COLUMN IF NOT EXISTS order_id BIGINT NULL REFERENCES orders(id) ON DELETE SET NULL;

  CREATE INDEX IF NOT EXISTS idx_enrollments_order_id
      ON enrollments(order_id)
      WHERE order_id IS NOT NULL;
  ```
- **Tác động API**: Cho phép `ST-05` tạo đơn (`#16`), `ST-06` khởi tạo/xác nhận thanh toán (`#17`) gắn với `order_id`, và `ST-07` đối chiếu quyền học `ACTIVE` theo đơn hàng.

---

### 1.3. Bảng `lesson_progress` — Tùy chọn cho Video Resume & Thời lượng học (`ST-11`, `ST-20`, `ST-21`)
- **Hiện trạng**: Bảng `lesson_progress` hiện có `id, user_id, lesson_id, status, progress_percent, last_accessed_at, completed_at` (đủ để chạy `ST-11` đánh dấu hoàn thành `#25` và tính `%` tiến độ tổng hợp `#21` trên `ST-20`).
- **Thay đổi khuyến nghị (nếu cần resume video & thống kê thời lượng học)**:
  ```sql
  ALTER TABLE lesson_progress
      ADD COLUMN IF NOT EXISTS last_position_seconds INTEGER NOT NULL DEFAULT 0
          CHECK (last_position_seconds >= 0),
      ADD COLUMN IF NOT EXISTS study_duration_seconds INTEGER NOT NULL DEFAULT 0
          CHECK (study_duration_seconds >= 0);
  ```

---

### 1.4. Bảng `user_achievements` — Tùy chọn cho mô tả & chứng nhận (`ST-22`, API `#38`)
- **Hiện trạng**: Bảng `user_achievements` có `id, user_id, course_id, achievement_code, title, awarded_at`.
- **Thay đổi khuyến nghị (nếu sau này mở hiển thị mô tả huy hiệu / link tải chứng nhận thật)**:
  ```sql
  ALTER TABLE user_achievements
      ADD COLUMN IF NOT EXISTS description TEXT NULL,
      ADD COLUMN IF NOT EXISTS certificate_url TEXT NULL;
  ```

---

## 2. Lỗi kỹ thuật trong Migration & Default Timestamp cần sửa chung

### 2.1. Migrations `015`–`020` đang hardcode schema `nguyen_anh_duc`
- **File ảnh hưởng**:
  - `infra/postgres/study-server/migrations/015_orders.sql`
  - `infra/postgres/study-server/migrations/016_uploads_operation_notifications.sql`
  - `infra/postgres/study-server/migrations/017_quiz_objective_questions.sql`
  - `infra/postgres/study-server/migrations/018_discussions_achievements.sql`
  - `infra/postgres/study-server/migrations/019_lesson_progress_user_lesson_unique.sql`
  - `infra/postgres/study-server/migrations/020_resource_visibility_storage.sql`
- **Vấn đề**: Tất cả 6 file trên đều ghi cứng `nguyen_anh_duc.<table_name>`. Khi dev khác chạy migration trên schema riêng (như `hoang_xuan_long`, `dao_van_hung`), các bảng/cột mới không được tạo vào schema của họ → gây lỗi `500 UndefinedTable` hoặc `UndefinedColumn` khi chạy các màn ST.
- **Cách xử lý**: Bỏ prefix `nguyen_anh_duc.` và dựa vào `SET search_path TO <schema>, public;` (giống chuẩn của migrations `002`–`014`).

### 2.2. Thiếu `DEFAULT CURRENT_TIMESTAMP` cho `created_at` / `updated_at` ở các bảng gốc
- **Bảng ảnh hưởng**: `users`, `courses`, `lessons`, `quizzes`, `assignments`, `discussions`, `notifications`, `enrollments`, `payments`.
- **Vấn đề**: Cột `created_at` / `updated_at` là `NOT NULL` nhưng không có `DEFAULT`, dễ gây lỗi `NotNullViolation` khi insert dữ liệu mới hoặc seed test.
- **Khuyến nghị**:
  ```sql
  ALTER TABLE courses       ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP, ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;
  ALTER TABLE lessons       ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP, ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;
  ALTER TABLE quizzes       ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP, ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;
  ALTER TABLE assignments   ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP, ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;
  ALTER TABLE discussions   ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP, ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;
  ALTER TABLE notifications ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;
  ALTER TABLE enrollments   ALTER COLUMN enrolled_at SET DEFAULT CURRENT_TIMESTAMP;
  ALTER TABLE payments      ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;
  ```

---

## 3. Tóm tắt bảng nào KHÔNG cần sửa DB để fix ngay
Các lỗi sau **không cần thay đổi schema DB** (chỉ sửa FE hoặc Backend query):
- **ST-21, ST-23**: Đổi `shell: 'blank'` → `'portal'` ở FE.
- **ST-04**: Sửa điều hướng nút "Tiếp tục thanh toán" ở FE.
- **ST-11, ST-13**: Thay ký tự `♧` bằng SVG icon chuông ở `StudentLayout`.
- **ST-01** (header): Ẩn nút Đăng nhập/Đăng ký khi đã đăng nhập ở `StudentPublicFrame`.
- **ST-08**: Thêm filter `COMPLETED` và map nhãn `"Đã hoàn thành"` ở FE (API `#20` đã hỗ trợ).
- **ST-11** (`#24`, `#25`, `#27`): Mở khóa UI player, nút hoàn thành & bài tiếp theo ở FE (3 API đã chạy 200 OK).
- **ST-20 & ST-01** (`#21`): Sửa Backend API `#21` tính tổng hợp tiến độ từ các bảng sẵn có (`enrollments`, `lessons`, `lesson_progress`) thay vì trả `UserProfile`.
