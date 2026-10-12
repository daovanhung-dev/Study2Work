---
title: "Overview"
order: 2
dd_id: "24"
api_name: "Nạp nội dung bài học / Lấy nội dung chính"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 24 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | GET |
| Endpoint | /api/v1/lessons/{lesson_id} |
| Purpose | Lấy Lesson và nội dung chính để hiển thị trong AC-14/AC-15. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT theo API catalog. |
| Authorization | Catalog yêu cầu role Student; AC-14 có precondition đã enrolled; AC-15 yêu cầu có access và sơ đồ ghi kiểm tra access + trạng thái publish. Predicate và cách áp dụng cho lời gọi trực tiếp chưa xác nhận. |
| Basis | DIRECT — API catalog và AC-14/AC-15 |
| Status | Draft — Needs Confirmation |
| Transaction | N/A — GET read-only; transaction không được contract mô tả. |
| Side effects | N/A — không có write hoặc side effect được mô tả. |

## Sources

- [API #24 catalog row và reusable schema](../../../../../docs/lists/list_api.md) — method, path, actor, request, response và status/business codes.
- [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và chuỗi API AC-14/15.
- [AC-14/AC-15 diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — API #24 đọc Lesson/content; AC-15 ghi bước check access và publish status.
- [DB design](../../diagrams/DB_UNICA_TABLES.md) và [checked-in DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate Lesson mapping; không xác nhận query hoặc live schema.
- [Current router](../../../app/api/v1.py), [Study modules](../../../app/modules/) và [Study tests](../../../tests/) — đối chiếu runtime wiring hiện tại.

## Tables read

- `lessons` — candidate nguồn cho Lesson; query API #24 chưa được tìm thấy.
- `courses` và `enrollments` — candidate nguồn liên quan publish/access; predicate và việc API #24 đọc các bảng này chưa được xác nhận.

## Tables write

- N/A — catalog/diagram không mô tả mutation cho API GET #24.

## Mục chú ý

- API #24 là bước đọc nội dung riêng sau API #22 access và API #23 start trong AC-14; thứ tự phía client không tự xác lập authorization cho lời gọi trực tiếp.
- AC-15 yêu cầu kiểm tra access + trạng thái publish nhưng không chỉ rõ entity, status values, enrollment eligibility hoặc prerequisite rule.
- Reusable `Lesson` gồm `id`, `course_id`, `title`, `content?`, `video_url?`, `order`, `status`; đây là schema thiết kế của catalog.
- Checked-in DDL và ERD là bằng chứng thiết kế, không chứng minh schema live hoặc query runtime.

## Assumptions

- Không chọn access predicate, publish predicate, query, 403/404 split, status enum hoặc null/omit serialization; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
- Không trả thêm trường ngoài reusable schema `Lesson` khi chưa có contract nguồn.

## Expected behavior

- Student gọi `GET /api/v1/lessons/{lesson_id}` với Bearer JWT và `lesson_id:int64!`.
- Catalog quy định HTTP 200 `DESIGN_RESOURCE_RETRIEVED` với `ApiEnvelope<Lesson>`; lỗi khai báo gồm 401, 403, 404 và 500 cùng business codes tương ứng.
- AC-14 đặt API #24 sau access check và start; AC-15 đặt kiểm tra access/trạng thái publish trước khi đọc Lesson/content.

## Current behavior

- Không tìm thấy route, module, query hoặc focused test API #24 trong Study source/test hiện tại.
- API #12 có query lesson để xác định parent course của resource; không phải implementation API #24.
- Runtime status của API #24: `UNWIRED / NOT_FOUND`.

## Conflicts

- `DISCREPANCY`: Catalog khai báo `ApiEnvelope<Lesson>`; AC diagram ghi `ApiEnvelope` không có generic, nên DD giữ payload chi tiết theo catalog và ghi diagram là biểu diễn tổng quát.
- `SOURCE_REQUIRED`: Catalog/AC-15 yêu cầu authorization/publish gate nhưng không định nghĩa predicate hoặc error visibility semantics.
- `DESIGN_ONLY`: DDL `lessons.course_id` không có `NOT NULL`, trong khi DB design mô tả quan hệ này là bắt buộc và catalog yêu cầu `Lesson.course_id`.

## Security note

- Không nhận `user_id` từ client; claim/identity mapping cho entitlement lookup chưa được xác nhận cho API #24.
- Không coi lần gọi API #22 trước đó là thay thế server-side authorization của API #24 khi gọi độc lập.
- Không suy ra API #24 phải trả reason field từ nhánh 403 của API #22; catalog không định nghĩa error-specific payload.

## Performance note

- Contract không quy định latency, cache, index, query plan hoặc pagination.
- Query/projection chưa có trong source; không đề xuất SQL/index hoặc cache behavior trong DD này.

---
## Phụ lục đối chiếu template Markdown

- Template: [02_Overview.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/02_Overview.md).
- Sheet nguồn: Overview.
