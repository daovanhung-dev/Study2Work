# Đề xuất & Yêu cầu gửi Nhóm trưởng — Cụm màn hình Student (`ST-01` → `ST-26`)

> **Người gửi**: Hoàng Xuân Long  
> **Ngày lập**: 2026-11-26  
> **Tài liệu đính kèm**:
> - Kết quả kiểm thử: `Test Screen.xlsx` (tab `ST`) và Google Sheet [Test Screen — ST](https://docs.google.com/spreadsheets/d/1GM9aCdCmBZ4hRX-lsrsRw9qlegH78lrtndiYar5c1sI/edit?gid=20261002#gid=20261002)
> - Chi tiết SQL & cấu trúc DB: `DB_Changes_Note_ST_Screens.md`

---

## 1. Tóm tắt hiện trạng cụm màn Student (`ST-01` → `ST-26`)

Sau khi rà soát DD, sửa toàn bộ lỗi FE và lỗi API không cần thay đổi cấu trúc DB, kết quả hiện tại của 26 màn Student:

- **Đạt**: **22 / 26 màn** (`ST-01..ST-03`, `ST-08..ST-26`).
- **Không đạt**: **0 / 26 màn** (đã sửa dứt điểm `ST-04` TC06, `ST-21` TC02, `ST-23` TC02, icon `♧`, header khi đã login, bộ lọc `COMPLETED` ở `ST-08`, mở khóa `ST-11` `#25/#27`, sửa `API #21` cho `ST-20` & `ST-01`).
- **Bị chặn**: **4 / 26 màn** (`ST-04` nhánh trả phí, `ST-05`, `ST-06`, `ST-07`) — đều phụ thuộc quyết định về luồng thanh toán và bổ sung cột DB.

---

## 2. Các yêu cầu cần Nhóm trưởng chốt & hỗ trợ xử lý

### 2.1. [Ưu tiên cao] Chốt luồng thanh toán khóa trả phí (`ST-04` → `ST-05` → `ST-06` → `ST-07`)
- **Hiện trạng**:
  - `API #16 (POST /api/v1/orders)` đã có code ở Backend nhưng phía FE (`api.constants.ts`) đang gắn `UNWIRED`.
  - `API #17 (POST /api/v1/payments)` ở Backend hiện đang là stub trả `503 Payment provider is unavailable.`.
  - Bảng `payments` chưa có cột `order_id`, `operation_id`, `checkout_url`; bảng `enrollments` chưa có `order_id`.
- **Cần Nhóm trưởng chốt**:
  1. Cho môi trường dev/demo, chọn **Phương án A (Sandbox / Mock Payment Provider tự xác nhận `PENDING → PAID` và tạo enrollment `ACTIVE`)** hay **Phương án B (tích hợp cổng thanh toán thật như VNPay/MoMo/SePay)**?
  2. Duyệt bổ sung các cột sau vào DB (chi tiết SQL ở `DB_Changes_Note_ST_Screens.md`):
     - `payments`: `order_id`, `currency`, `operation_id`, `checkout_url`, `updated_at`
     - `enrollments`: `order_id`
  3. Xác nhận mở `API_016` sang `WIRED` trên FE để kích hoạt màn `ST-05`.

---

### 2.2. [Ưu tiên cao] Chuẩn hóa 6 file Migration SQL đang hardcode schema `nguyen_anh_duc`
- **Hiện trạng**:
  - Các file `infra/postgres/study-server/migrations/015_orders.sql` → `020_resource_visibility_storage.sql` đều đang ghi cứng prefix `nguyen_anh_duc.<table_name>`.
  - Khi thành viên khác chạy migration trên schema cá nhân (`hoang_xuan_long`, `dao_van_hung`...), các bảng/cột mới không được tạo vào đúng schema → gây lỗi `500 UndefinedTable / UndefinedColumn`.
  - Ngoài ra các bảng gốc (`courses`, `lessons`, `quizzes`, `assignments`, `discussions`, `notifications`, `enrollments`, `payments`) đang thiếu `DEFAULT CURRENT_TIMESTAMP` cho `created_at` / `updated_at`.
- **Đề xuất**: Cho phép chuẩn hóa `015`–`020` bỏ hardcode `nguyen_anh_duc.` (dùng `search_path` giống `002`–`014`) và bổ sung `DEFAULT CURRENT_TIMESTAMP`.

---

### 2.3. [Ưu tiên trung bình] Duyệt thêm cột `users.bio` cho `ST-02` & `ST-03`
- **Hiện trạng**: Bảng `users` chưa có cột `bio`, nên `API #14 (PUT /users/me/profile)` đang bỏ qua trường `bio` và `ST-03` phải khóa ô nhập giới thiệu bản thân.
- **Đề xuất**: Duyệt thêm `users.bio TEXT NULL` và cập nhật `API #04` + `API #14` để mở khóa đầy đủ form `ST-03`.

---

### 2.4. [Ưu tiên trung bình] Cấu hình Object Storage (S3 / R2 / MinIO) cho môi trường dev
- **Hiện trạng**: Do local chưa có cấu hình Object Storage nên 3 luồng sau đang trả `503`:
  - `ST-03` (`API #13`): Upload avatar học viên.
  - `ST-12` / `GS-07` (`API #12`): Xem/tải tài nguyên có `visibility = PRIVATE` (ký signed URL).
  - `ST-18` (`API #34`): Tải tệp đính kèm khi nộp bài tập.
- **Đề xuất**: Nhóm trưởng cung cấp biến môi trường S3/R2 dev chung hoặc thống nhất dùng MinIO local để test khép kín 3 luồng upload/tài nguyên này.

---

### 2.5. [Đồng bộ nhánh `develop`] Contract API `#21` & lỗi CSS budget khi `ng build`
- **API `#21` (`GET /api/v1/users/me/progress`)**: Trước đây API này trả về `UserProfile` khiến `ST-20` và widget tiến độ trên `ST-01` bị chặn. Đã sửa API `#21` trả về tiến độ tổng hợp thật (`total_enrolled_courses`, `active_courses`, `completed_courses`, `total_lessons`, `completed_lessons`, `overall_progress_percent`, `courses[]`) từ các bảng sẵn có → cần Nhóm trưởng xác nhận contract này để đồng bộ DD API `#21`.
- **Lỗi `npm run build` (production) trên `develop`**: File `apps/study-client/src/app/features/student/ST03/pages/st03-page.css` (17.40 kB) đang vượt budget `8.00 kB` của `angular.json` (dev server `ng serve` vẫn chạy bình thường). Đề xuất tách CSS `ST-03` sang global host-scoped giống các màn `AD-*` hoặc điều chỉnh budget trong `angular.json`.

---

### 2.6. [Tùy chọn — Giai đoạn sau] Mở rộng cột cho Video Resume & Chứng nhận
- Nếu cần lưu vị trí xem video (`ST-11`) và tổng thời lượng học (`ST-20`): bổ sung `lesson_progress.last_position_seconds`, `lesson_progress.study_duration_seconds`.
- Nếu mở hiển thị mô tả huy hiệu / link chứng nhận thật (`ST-22`): bổ sung `user_achievements.description`, `user_achievements.certificate_url`.

---

## 3. Checklist duyệt nhanh cho Nhóm trưởng

| STT | Hạng mục | Quyết định cần chốt | Trạng thái |
|---:|---|---|---|
| 1 | Thanh toán `ST-05`–`ST-07` (`API #16/#17`) | Chọn Sandbox/Mock hay cổng thanh toán thật + duyệt thêm cột `payments`/`enrollments` | `[ ] Chờ duyệt` |
| 2 | Migrations `015`–`020` | Cho phép bỏ hardcode `nguyen_anh_duc.` dùng `search_path` chung | `[ ] Chờ duyệt` |
| 3 | Hồ sơ `Bio` (`ST-02`/`ST-03`) | Duyệt thêm cột `users.bio` và mở `API #04/#14` | `[ ] Chờ duyệt` |
| 4 | Object Storage dev (`#12/#13/#34`) | Cung cấp cấu hình S3/R2 dev hoặc MinIO local | `[ ] Chờ duyệt` |
| 5 | Contract `API #21` & CSS budget `ST-03` | Xác nhận contract `OverallProgressSummary` + cách xử lý budget `ng build` | `[ ] Chờ duyệt` |
