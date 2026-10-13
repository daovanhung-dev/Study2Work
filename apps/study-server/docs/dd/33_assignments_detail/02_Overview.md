---
title: "Overview"
order: 2
dd_id: "33"
api_name: "Lấy đề bài/rule/deadline"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 33 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | GET |
| Endpoint | /api/v1/assignments/{assignment_id} |
| Purpose | Lấy Assignment để hiển thị đề bài, hạn nộp và điểm tối đa trước flow nộp bài; submission rule chưa có response schema được duyệt. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT theo API catalog. |
| Authorization | Catalog yêu cầu role Student; predicate xác nhận quyền xem assignment/course chưa được đặc tả. |
| Basis | DIRECT — API catalog và AC-17; DB mapping là candidate design. |
| Status | Draft — Needs Confirmation |
| Transaction | N/A — GET chỉ đọc theo contract. |
| Side effects | N/A — không có mutation hoặc external side effect được mô tả. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — endpoint, actor, `Assignment` response và error set của API #33.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — trace API #33 tới AC-17.
- [AC-17 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — bước đọc assignment/rule và nhánh còn được phép nộp.
- [Assignment table design](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — candidate assignment fields/relations; design-only.
- [Checked-in DB DDL](../../../../../infra/postgres/study-server/DB.sql) — physical DDL evidence, không xác nhận live schema.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — shared envelope, error and trace conventions.
- [Current Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), `apps/study-server/app/modules/` và `apps/study-server/tests/` — runtime route/auth/module/test surface.

## Tables read

- `assignments` — candidate source for Assignment fields; API #33 query is not implemented.
- `enrollments` — possible access evidence only; API #33 contract/AC-17 do not define a membership predicate or query.

## Tables write

- N/A — API #33 is GET/read-only.

## Mục chú ý

- Catalog defines `Assignment` as `id`, `course_id`, `title`, optional `description`, optional `due_at`, and required `max_score`.
- DB design maps `Assignment.title` to physical `assignments.name`.
- AC-17 says “Đọc Assignment + submission rule”, but the reusable `Assignment` schema does not define submission-rule fields.
- AC-17 shows overdue/no-permission as `403/409`; API #33 catalog lists `403` but not `409`.
- Checked-in DDL permits NULL for `course_id` and `max_score`; this conflicts with their required logical response fields and the DB table notes for `course_id`.
- No live schema or API #33 runtime query is verified.

## Assumptions

- Preserve the exact method, path, Student actor, `ApiEnvelope<Assignment>` and 200/401/403/404/500 code set from the catalog.
- Treat candidate `assignments` mapping as design evidence, not runtime behavior.
- Do not add submission-rule fields or an error code absent from the catalog.

## Conflicts

- `SOURCE_REQUIRED`: AC-17's submission-rule step has no corresponding `Assignment` response fields or rule definition.
- `DISCREPANCY`: AC-17 allows `409` for overdue/no-permission while API #33 catalog has no 409.
- `DISCREPANCY / DESIGN_ONLY`: logical `course_id` and `max_score` are required, but checked-in DDL allows NULL; live schema is not verified.
- `UNWIRED / NOT_FOUND`: Current Study route/module/test surface has no API #33.

## Security note

- Request identifies only `assignment_id`; do not accept `user_id` from the client.
- Current Student auth helper returns a numeric user ID, but API #33's course/assignment access predicate and 403-versus-404 policy are not defined.
- Do not infer permission solely from the client having opened another API earlier in the AC flow.

## Performance note

- Contract is a single-resource GET with no pagination, cache or latency objective.
- Do not add joins, indexes, or query limits while the access predicate and query shape remain unapproved.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>

