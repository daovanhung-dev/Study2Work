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
| Basis | `DIRECT — list_api.md + AC-11; upload-only và không DB mutation theo quyết định task.` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `N/A — không có DB transaction; Object Storage side effect chưa có transaction contract.` |
| Side effects | `Object Storage upload; không cập nhật users hoặc profile trong API #13.` |

## Sources

- [`docs/lists/list_api.md`](../../../docs/lists/list_api.md) — API #13: `POST`, endpoint, `body{image:string!}`, `ApiEnvelope<UserProfile>` và các status/error code.
- [`AC_02_STUDENT_LEARNING.drawio`](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-11: Student chọn avatar, API #13 lưu tại Object Storage, sau đó API #14 cập nhật profile.
- [`00_AC_API_INDEX.md`](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-11 actor, precondition, postcondition và API mapping.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — bảng `users`, `avatar_url` và quy tắc V1 không tự thêm bảng/cột.
- [`API #4 DD`](../04_users_me/02_Overview.md) — pattern auth/profile response và cảnh báo contract/ERD gap.
- [`createDD-markdown skill`](../../../.agents/skills/create_dd/docs/dd/createDD_MARKDOWN_SKILL.md) — source traceability, one-line rule và delivery gates.

## Tables read

- `N/A — không có DB read được source xác nhận cho API #13 upload-only.`

## Tables write

- `N/A — API #13 không cập nhật DB và không tạo mapping users.avatar_url.`

## External side effect

- `Object Storage` — nhận avatar và lưu asset; adapter, object key, output URL và policy chưa được source đặc tả.

## Mục chú ý

- Contract giữ nguyên `body{image:string!}`; không chuyển sang `multipart/form-data`.
- Diagram ghi validate MIME/size nhưng không cung cấp encoding, MIME allowlist hoặc size limit.
- Contract yêu cầu `ApiEnvelope<UserProfile>`, nhưng flow upload-only không cung cấp nguồn reload đầy đủ cho UserProfile.
- API #14 mới là bước `PUT /api/v1/users/me/profile` trong sequence AC-11.
- Runtime source hiện không có route API #13; Study server hiện `DECLARED_NOT_RUNNABLE`.

## Assumptions

- Upload-only là boundary của API #13; không `INSERT`, `UPDATE`, `DELETE` hoặc `SELECT` DB.
- `image` là `string` theo contract; không diễn giải string thành base64, data URI, URL hoặc format khác.
- Không tự tạo `storage_object_key`, `avatar_url`, MIME policy, size policy, TTL, retry hoặc cleanup rule.
- Response giữ `ApiEnvelope<UserProfile>`; phần profile chưa có source được ghi `SOURCE_REQUIRED` thay vì tự reload hoặc đổi response schema.

## Conflicts / Gaps

- `GAP-13-01`: Contract chỉ nói `image:string!`; transport, encoding, MIME và size validation chưa được khóa.
- `GAP-13-02`: AC-11 có Object Storage nhưng không có storage adapter, object-key rule hoặc response field mapping.
- `GAP-13-03`: `ApiEnvelope<UserProfile>` cần profile source, trong khi quyết định upload-only không cho phép profile reload hoặc DB update trong API #13.
- `GAP-13-04`: Cleanup/idempotency khi upload thành công nhưng response/profile flow thất bại chưa có contract.

## Security note

- Verify Bearer JWT trước khi upload và kiểm tra role `Student`.
- Không đưa token raw, credential, object key nội bộ, raw storage error hoặc stack trace vào response/log.
- Không suy ra storage namespace từ claim khi storage-key policy chưa được phê duyệt.
- MIME/size validation phải được khóa trước implementation; không dùng allowlist hoặc giới hạn tự chọn trong DD này.

## Performance note

- Object Storage là external dependency và có thể làm tăng latency của request.
- Timeout, retry, idempotency và cleanup chưa có source; giữ `TBD`.
- Không thêm DB query, cache, index hoặc transaction boundary ngoài contract.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/02_Overview.md`.
- Sheet logic: `Overview`.
