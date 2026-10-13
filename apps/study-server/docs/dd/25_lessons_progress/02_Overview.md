---
title: "Overview"
order: 2
dd_id: "25"
api_name: "Lưu vị trí và trạng thái"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 25 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | PATCH |
| Endpoint | `/api/v1/lessons/{lesson_id}/progress` |
| Purpose | Lưu tiến độ và trạng thái học của Student trên một Lesson theo contract thiết kế. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT theo API catalog. |
| Authorization | Catalog yêu cầu role Student; entitlement, direct-call check và token-to-user mapping chưa được API-specific source xác nhận. |
| Basis | DIRECT — API catalog và AC-14 |
| Status | Draft — Needs Confirmation |
| Transaction | SOURCE_REQUIRED — AC-14 mô tả mutation; transaction boundary/atomicity chưa xác định. |
| Side effects | AC-14 ghi “UPDATE lesson progress + course aggregate”; target và cách tính aggregate chưa được xác nhận. |

## Sources

- [API #25 catalog row and reusable schema](../../../../../docs/lists/list_api.md) — method, path, actor, request, response và business codes.
- [AC API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-14 actor, precondition, postcondition và API sequence.
- [AC-14 diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — mutation intent và nhánh completed.
- [DB design](../../diagrams/DB_UNICA_TABLES.md) và [checked-in DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate `lesson_progress`; không xác nhận live schema.
- [Current router](../../../app/api/v1.py), [Study modules](../../../app/modules/) và [Study tests](../../../tests/) — đối chiếu wiring hiện tại.

## Tables read

- `lessons` — candidate source cho Lesson response; API #25 query/projection chưa được tìm thấy.
- `lesson_progress` — candidate context/mutation target; lookup query và identity binding chưa được xác nhận.
- Course aggregate source/target — SOURCE_REQUIRED; AC-14 không chỉ ra table, query hoặc formula.

## Tables write

- `lesson_progress` — candidate UPDATE/upsert target theo DB design và AC-14; conflict key/cột ghi chưa được xác nhận.
- Course aggregate — AC-14 nêu update nhưng không định nghĩa persistence target hoặc phép tính.

## Mục chú ý

- API contract: path `lesson_id:int64!`; body `position:int32!`, `percent:int32!`, `completed:boolean!`; HTTP 200 `DESIGN_RESOURCE_UPDATED`.
- AC-14 ghi `completed = YES` → mark `COMPLETED`; `NO` → giữ `IN_PROGRESS`. Cột lưu, timestamp và state transition đầy đủ chưa được xác định.
- `lesson_progress` ERD/DDL có `progress_percent`, nhưng không có cột `position`; checked-in DDL không khai báo unique key `(user_id, lesson_id)`.
- Catalog trả `ApiEnvelope<Lesson>`; node API trong diagram cũng ghi generic `ApiEnvelope` nhưng không có payload detail.
- DDL và ERD là design evidence, không chứng minh schema live hay runtime behavior.

## Assumptions

- Chỉ tài liệu hóa contract và logical flow từ nguồn; không chọn SQL, upsert key, range validation, aggregate formula, transaction behavior hoặc serialization chưa được xác nhận.
- Runtime status là `UNWIRED / NOT_FOUND` theo source/module/test inventory hiện tại.

## Conflicts

- `DISCREPANCY`: Catalog khai báo `ApiEnvelope<Lesson>`; diagram biểu diễn `ApiEnvelope` tổng quát. DD giữ response type cụ thể của catalog.
- `SOURCE_REQUIRED`: Body có `position`, nhưng ERD/DDL không có cột tương ứng.
- `SOURCE_REQUIRED`: AC-14 nói cập nhật course aggregate nhưng không chỉ ra nguồn, đích hoặc công thức.
- `DISCREPANCY`: ERD mô tả `user_id` và `lesson_id` là bắt buộc; checked-in DDL không ghi `NOT NULL` cho hai cột này.

## Security note

- Không nhận `user_id` từ body; request không khai báo field này. Nguồn identity từ JWT và cách bind vào progress ownership predicate chưa được API #25 xác nhận.
- Không coi việc client gọi API #22 trước đó là bằng chứng API #25 tự thực hiện authorization cho direct call.

## Performance note

- Contract không quy định latency, index, query plan, cache hoặc batch behavior.
- Không đề xuất index/upsert SQL khi uniqueness và query chưa được xác nhận.

## Expected behavior

- Student gọi PATCH với Bearer JWT, `lesson_id:int64!` và ba field body theo catalog.
- Catalog khai báo HTTP 200 `DESIGN_RESOURCE_UPDATED`, response `ApiEnvelope<Lesson>` và các lỗi 401/403/404/422/500.
- AC-14 mô tả cập nhật lesson progress + course aggregate và phân nhánh trạng thái hoàn thành.

## Current behavior

- Không tìm thấy route, module, query hoặc focused test API #25 trong Study source/test hiện tại.
- Runtime status: `UNWIRED / NOT_FOUND`; DB design/DDL không xác nhận runtime schema.

---
## Phụ lục đối chiếu template Markdown

- Template: [02_Overview.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/02_Overview.md).
- Sheet nguồn: Overview.
