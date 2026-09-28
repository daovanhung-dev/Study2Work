---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `14` |
| Module | `STUDENT / LEARNING & INTERACTION` |
| Method | `PUT` |
| Endpoint | `/api/v1/users/me/profile` |
| Purpose | `Cập nhật các thông tin profile được Student gửi và phản ánh lại UserProfile.` |
| Consumer/Actor | `Authenticated Student` |
| Authentication | `Bearer JWT bắt buộc` |
| Authorization | `Role = Student; user identity lấy từ JWT.sub` |
| Basis | `DIRECT — approved design contract + AC-11; current source dùng để ghi discrepancy/runtime status.` |
| Status | `Draft — Needs Confirmation / PARTIALLY COMPLETED` |
| Transaction | `Caller-owned transaction: COMMIT khi update thành công; ROLLBACK khi mutation hoặc mapping lỗi. Runtime module chưa tồn tại.` |
| Side effects | `UPDATE users; không gọi external service.` |

## Sources

- [`docs/lists/list_api.md`](../../../../../docs/lists/list_api.md) — API #14 contract và reusable `UserProfile`.
- [`AC_02_STUDENT_LEARNING.drawio`](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-11 sequence và postcondition.
- [`00_AC_API_INDEX.md`](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) — Student precondition và API mapping.
- [`DB.sql`](../../../../../infra/postgres/study-server/DB.sql) — `users` columns hiện có.
- [`API #4 query.py`](../../../app/modules/guest/api_04_users_me/query.py) — safe profile projection hiện hành.
- [`API #4 view.py`](../../../app/modules/guest/api_04_users_me/view.py) — JWT/Student/error mapping pattern hiện hành.
- [`code_http.md`](../../business_code/code_http.md) — `DESIGN_RESOURCE_UPDATED` và `DESIGN_*` status design-only.

## Tables read

- `users` — reload safe profile sau update theo AC-11.

## Tables write

- `users` — update `full_name`, `phone`, `avatar_url`, `updated_at` theo source-backed columns.
- `users.bio` — `SOURCE_REQUIRED`; không có column trong current `DB.sql` hoặc ERD, không được tự tạo mapping persistence.

## Mục chú ý

- API #14 chưa có route trong `app/api/v1.py`.
- API #14 chưa có `models.py`, `validate.py`, `query.py`, `view.py` hoặc test runtime.
- API #4 là current source pattern, không phải implementation của API #14.
- Contract giữ `bio` nhưng current schema không source-back `users.bio`.
- Contract ghi `avatar_url...:uri!`; requiredness và nullable semantics chưa được khóa.

## Assumptions

- Identity dùng numeric `JWT.sub` và role list hiện hành `roles`, theo API #4 current source.
- Mutation chỉ scope theo `users.id = user_id` từ JWT; không cho client gửi `user_id`.
- Không update `email`, `role`, `status`, `password_hash`, `created_at` hoặc các column khác ngoài mapping được khóa.
- Profile response dùng safe projection và không trả `password_hash`.
- `bio` được giữ ở trạng thái `SOURCE_REQUIRED`; không thêm table/column/migration.

## Conflicts

- `CONFLICT-14-01`: Contract yêu cầu `bio:string!`, nhưng `users.bio` không có trong `DB.sql`, ERD hoặc current API #4 projection.
- `CONFLICT-14-02`: Contract yêu cầu `phone:string!`, nhưng current `users.phone` là nullable.
- `CONFLICT-14-03`: `avatar_url...:uri!` không xác định rõ field name semantics, requiredness và nullable behavior.
- `CONFLICT-14-04`: Contract response là `UserProfile`, nhưng current profile model không có `bio`.

## Security note

- Verify Bearer JWT trước khi query hoặc mutation.
- Chỉ cho role `Student` thực hiện update.
- Scope update bằng `JWT.sub`, không nhận `user_id` từ body.
- Không update hoặc trả `password_hash`.
- Không trả raw SQL error, stack trace, token hoặc credential.

## Performance note

- Flow dự kiến gồm một `UPDATE users` và một safe profile read/reload.
- Không thêm external call, cache, index hoặc query theo user input ngoài scope identity.
- Số query và lựa chọn `RETURNING` versus reload cần được khóa khi runtime implementation được phê duyệt.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/02_Overview.md`.
- Sheet logic: `Overview`.
