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
| API ID | 15 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | GET |
| Endpoint | /api/v1/courses/{course_id}/enrollment-status |
| Purpose | Kiểm tra trạng thái enrollment liên quan đến course |
| Consumer/Actor | Public; no Bearer token |
| Authentication | N/A — public endpoint |
| Authorization | N/A — không kiểm tra role |
| Basis | DIRECT — approved API contract + AC-12 + current schema evidence |
| Status | Draft — Needs Confirmation |
| Completion | PARTIALLY COMPLETED |
| Decision status | NEEDS USER DECISION |
| Transaction | N/A — read-only API |
| Side effects | N/A — không có mutation hoặc external side effect |

## Sources

- [list_api.md](../../../../../docs/lists/list_api.md) — API #15 method, path, public access, Enrollment response và status/error contract.
- [AC_02_STUDENT_LEARNING.drawio](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — AC-12 sequence.
- [00_AC_API_INDEX.md](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-12 mapping.
- [DB.sql](../../../../../infra/postgres/study-server/DB.sql) — courses và enrollments columns.
- [DB_UNICA_TABLES.md](../../../docs/diagrams/DB_UNICA_TABLES.md) — enrollment relationship.
- [v1.py](../../../app/api/v1.py) — xác nhận API #15 chưa được route.

## Tables read

- courses — dùng để xác định course tồn tại; PUBLISHED predicate là evidence từ AC-12 nhưng cần confirmation cho API #15.
- enrollments — source-backed response fields id, user_id, course_id, status, enrolled_at, completed_at.

## Tables write

- N/A — read-only API; không có DB mutation.

## Mục chú ý

- Public được giữ nguyên; không tự thêm Bearer JWT, JWT.sub, query user_id hoặc user identity header.
- Enrollment là quan hệ có user_id; contract không cung cấp điều kiện chọn một enrollment duy nhất.
- HTTP 404 được giữ theo contract nhưng semantics course-not-found/enrollment-not-found cần được xác nhận.
- enrollments.status là VARCHAR(20); enum business chưa được source xác nhận.

## Assumptions

- course_id chỉ được lấy từ path và parse thành int64.
- Không invent min/max hoặc positive-number rule ngoài contract.
- Không trả một enrollment chọn ngẫu nhiên khi selection predicate chưa được khóa.

## Conflicts

- DISCREPANCY: Contract/diagram ghi Public, nhưng Enrollment có user_id và bảng enrollments có thể có nhiều row theo course_id.
- PLAN/CANONICAL DISCREPANCY: Một dòng trong execution plan ghi thiếu suffix `/enrollment-status`; list_api.md, AC index và diagram xác nhận endpoint canonical có suffix này. DD follows canonical source.
- SOURCE_REQUIRED: Chưa có source xác định user identity, 404 semantics, PUBLISHED predicate và duplicate enrollment handling.
- RUNTIME_STATUS: API #15 chưa có route/module/query/test; current status UNWIRED / NOT_FOUND.

## Security note

- Không decode token vì contract là public.
- Không expose thêm user data ngoài Enrollment contract.
- Không trả raw SQL, stack trace hoặc internal DB details.

## Performance note

- Course lookup có thể dùng courses.id.
- Enrollment lookup có thể cần enrollments.course_id; index/unique selection policy chưa được source xác nhận.
- Không thiết kế cache hoặc pagination vì contract không yêu cầu.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/02_Overview.md.
- Sheet logic: Overview.
