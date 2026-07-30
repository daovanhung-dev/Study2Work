# Study2Work — Fake Data SQL

## Phạm vi

- Schema: `study_dev0`
- Số bảng: **23**
- Mỗi bảng có một file SQL riêng.
- UUID được cố định để bảo đảm quan hệ khóa ngoại nhất quán.
- Tất cả `INSERT` sử dụng `ON CONFLICT DO NOTHING`, có thể chạy lại.

## Chạy bằng VS Code Database Client

1. Kết nối database `s2w`.
2. Mở `00_run_all_vscode.sql`.
3. Nhấn `Ctrl + A`.
4. Nhấn nút **Run** của extension.
5. Refresh database tree.
6. Chạy `99_verify_seed.sql`.

## Chạy từng bảng

Chạy theo thứ tự số từ `01_...sql` đến `23_...sql`. Không đổi thứ tự vì có quan hệ khóa ngoại.

## Xóa toàn bộ dữ liệu

Chạy `00_clear_all_data.sql`.

**Cảnh báo:** script này xóa toàn bộ dữ liệu trong các bảng của schema `study_dev0`.

## Chạy bằng Terminal/psql

Tại thư mục này:

```bash
psql -h 127.0.0.1 -p 5432 -U s2w_user -d s2w -f 00_run_all_psql.sql
```

## Số lượng fake data tối thiểu

| Bảng | Số dòng |
|---|---:|
| `users` | 12 |
| `user_profiles` | 12 |
| `roles` | 6 |
| `user_roles` | 16 |
| `learning_paths` | 4 |
| `onboarding_records` | 10 |
| `courses` | 8 |
| `learning_path_courses` | 16 |
| `learning_path_enrollments` | 10 |
| `course_enrollments` | 16 |
| `chapters` | 16 |
| `lessons` | 32 |
| `course_materials` | 32 |
| `exercises` | 14 |
| `exercise_submissions` | 14 |
| `lesson_progress` | 24 |
| `completion_rules` | 12 |
| `notification_settings` | 12 |
| `notifications` | 20 |
| `community_groups` | 6 |
| `community_join_events` | 12 |
| `support_requests` | 6 |
| `audit_logs` | 12 |
