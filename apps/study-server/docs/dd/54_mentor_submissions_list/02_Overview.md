---
title: "Overview"
order: 2
dd_id: "54"
api_name: "Lấy submissions"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 54 |
| Module | MENTOR / TEACHING & SUPPORT |
| Method | GET |
| Endpoint | /api/v1/mentor/submissions |
| Purpose | Đọc submissions theo quyền Mentor để chọn một submission và chuyển sang API #55 xem chi tiết. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Mentor có quyền chấm submissions thuộc course; predicate và identity mapping SOURCE_REQUIRED. |
| Basis | Catalog và AC-23 là DIRECT; query/schema là design candidate. |
| Status | Draft — Needs Confirmation |
| Transaction | N/A — READ-ONLY API |
| Side effects | Không có mutation được khai báo. |

## Sources

- [API catalog và reusable Submission schema](../../../../../docs/lists/list_api.md).
- [AC/API index, AC-23](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [AC-23 diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md).
- [DB ERD](../../diagrams/DB_UNICA_ERD.drawio).
- [Checked-in V1-PILOT DDL](../../../../../infra/postgres/study-server/DB.sql).
- [Related API #35 Overview](../35_assignments_submissions/02_Overview.md).
- [Current Study route source](../../../../../apps/study-server/app/api/v1.py).
- [Study auth helper](../../../../../apps/study-server/app/utils/auth.py).
- [API Guidelines](../../../../../contracts/api-guidelines/README.md).
- [Study Server declared route context](../../../../../.agents/server-study/apis/declared-routes.md).
- [createDD-markdown skill](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md).

## Tables read

- assignment_submissions — candidate source for Submission fields.
- assignments — candidate relation for course scope.
- courses — candidate direct-owner relation for Mentor access.

## Tables write

- N/A — READ-ONLY API.

## Mục chú ý

- API name and AC-23 flow describe a list, while the catalog response is singular `ApiEnvelope<Submission>`.
- Query `page` has no declared size, default, range, sort or pagination metadata.
- `status` is an optional string; allowed values and normalization are not defined.
- Logical `Submission.files` is an `UploadAsset[]`; candidate DDL exposes one nullable `file_url` and no approved asset metadata relation.
- AC-23 next calls API #55 for one selected submission and its files/rubric; rubric is outside API #54 response fields.
- API #54 has no current route, module or test in the Study Server.

## Assumptions

- Apply `course_id` and `status` filters only when the caller supplies them; do not assign defaults or enum values.
- `courses.mentor_id` is a DERIVED direct-owner candidate only; this does not establish support for assigned Mentors.
- Keep the catalog's singular `Submission` response in this draft until the contract owner resolves list cardinality.

## Conflicts

- List endpoint semantics conflict with singular `Submission` response shape.
- ERD/table guide show assignment/course references as required, while checked-in DDL permits NULL foreign keys.
- API Guidelines expect `data: null` on errors; current `error_response()` serializes omitted/None data as `{}`.
- Catalog includes 409 for a GET flow with no conflict branch in AC-23.

## Security note

- Never expose submissions outside the caller's Mentor course authorization.
- Current shared auth guard is Student-only; Mentor JWT claim and course assignment mapping are SOURCE_REQUIRED.
- Do not accept a student identity parameter; the endpoint has none.

## Performance note

- No supported page size, stable ordering or count contract exists, so query cost and response bounds cannot be specified.
- The exact asset lookup needed for `files[]` is not source-backed.

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
