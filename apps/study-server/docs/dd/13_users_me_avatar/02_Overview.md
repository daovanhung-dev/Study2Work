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
| API ID | `13` |
| Module | `STUDENT / LEARNING & INTERACTION` |
| Method | `POST` |
| Endpoint | `/api/v1/users/me/avatar` |
| Purpose | `Nhận chuỗi avatar từ Student và lưu avatar vào Object Storage; API #14 chịu trách nhiệm cập nhật profile theo sequence AC-11.` |
| Consumer/Actor | `Authenticated Student` |
| Authentication | `Bearer JWT bắt buộc` |
| Authorization | `Role = Student` |
| Basis | `DIRECT — list_api.md + AC-11, cập nhật theo các lựa chọn được user duyệt trong implementation plan.` |
| Status | `Implemented; local tests verify route and S3 adapter stub.` |
| Transaction | `N/A — không có DB transaction; Object Storage side effect chưa có transaction contract.` |
| Side effects | `S3-compatible Object Storage upload; không cập nhật users hoặc profile trong API #13.` |

## Sources

- [`docs/lists/list_api.md`](../../../../../docs/lists/list_api.md) — API #13 contract và response `AvatarUploadResult`.
- [`AC_02_STUDENT_LEARNING.drawio`](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-11: API #13 upload avatar, sau đó API #14 cập nhật profile.
- [`00_AC_API_INDEX.md`](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-11 actor, precondition, postcondition và API mapping.
- [`DB_UNICA_ERD.drawio`](../../diagrams/DB_UNICA_ERD.drawio) — bảng `users`; API #13 không truy cập hoặc sửa bảng này.
- [`API #4 DD`](../04_users_me/02_Overview.md) — pattern auth/profile response và cảnh báo contract/ERD gap.
- [`createDD-markdown skill`](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md) — source traceability, one-line rule và delivery gates.

## Tables read

- `N/A — không có DB read được source xác nhận cho API #13 upload-only.`

## Tables write

- `N/A — API #13 không cập nhật DB và không tạo mapping users.avatar_url.`

## External side effect

- `S3-compatible Object Storage` — PUT object `avatars/{user_id}`, URL dựng từ public base URL.

## Mục chú ý

- `image` là JSON Data URL `data:image/<mime>;base64,...`; chỉ nhận PNG, JPEG hoặc WebP.
- Payload tối đa 5 MiB sau giải mã; MIME khai báo phải khớp chữ ký ảnh.
- Storage dùng process environment, key cố định `avatars/{user_id}` và URL từ public base URL.
- Response là `ApiEnvelope<AvatarUploadResult>`; `data` chỉ chứa `avatar_url`.
- API #14 mới là bước `PUT /api/v1/users/me/profile` trong sequence AC-11.
- API #13 không query hoặc mutation DB; source route/parser/provider hiện được kiểm chứng cục bộ.

## Assumptions

- Upload-only là boundary của API #13; không `INSERT`, `UPDATE`, `DELETE` hoặc `SELECT` DB.
- `image` chỉ nhận Data URL Base64 theo allowlist PNG/JPEG/WebP; không nhận multipart, URL đầu vào hoặc field khác.
- Object key là `avatars/{user_id}`; upload mới ghi đè object của cùng user.
- Timeout storage là connect 5 giây, read 30 giây, tối đa một attempt.
- API #13 không truy cập DB; API #14 lưu URL vào profile ở bước tiếp theo.
- Thiếu cấu hình storage chỉ làm request API #13 trả 500 an toàn, không ảnh hưởng startup.

## Conflicts / Gaps

- Các khoảng trống Q-13-01..04 được giải quyết theo lựa chọn user duyệt và ghi trong `PLAN_RESULT.md`.
- API #13 trả URL upload; API #14 vẫn là bước cập nhật `users.avatar_url`.
- Remote storage/credential verification không nằm trong scope task.

## Security note

- Verify Bearer JWT trước khi upload và kiểm tra role `Student`.
- Không đưa token, credentials, raw provider error hoặc stack trace vào response/log.
- Object key chỉ được dựng từ user ID đã xác thực; client không gửi object key.
- So khớp chữ ký PNG/JPEG/WebP và giới hạn bytes sau giải mã trước khi upload.

## Performance note

- Object Storage là external dependency và có thể làm tăng latency của request.
- Timeout là 5 giây kết nối và 30 giây đọc; một attempt, không retry.
- Cùng user upload lần mới ghi đè cùng key; không có cleanup riêng.
- Không thêm DB query, cache, index hoặc transaction boundary ngoài contract.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/02_Overview.md`.
- Sheet logic: `Overview`.
