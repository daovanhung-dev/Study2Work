---
title: "Overview"
order: 2
dd_id: "36"
api_name: "Xác nhận dữ liệu đã nộp"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 36 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | GET |
| Endpoint | /api/v1/submissions/{submission_id} |
| Purpose | Đọc submission summary theo submission ID cho luồng AC-17. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | Student role theo catalog; resource access predicate SOURCE_REQUIRED. |
| Basis | APPROVED_DESIGN_CONTRACT; AC-17 flow |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND — API #36 has no route, query/module or test in the inspected Study source. |
| Transaction | N/A — read-only |
| Side effects | N/A — không ghi dữ liệu hay gọi external provider theo contract. |

## Sources

- [API catalog — API #36](../../../../../docs/lists/list_api.md) — contract và reusable Submission schema.
- [AC/API index — AC-17](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition và luồng API.
- [AC-17 — Nộp bài tập](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — API #36 đọc submission summary và UI hiển thị trạng thái đã nộp.
- [AC-23 — Chấm bài](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — Mentor đọc, chấm và ghi feedback; không chốt disclosure của API #36.
- [DB table design](../../diagrams/DB_UNICA_TABLES.md) and [ERD](../../diagrams/DB_UNICA_ERD.drawio) — candidate assignment_submissions fields and relations.
- [Checked-in Study DDL](../../../../../infra/postgres/study-server/DB.sql) — design evidence, not live-schema verification.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, safe errors and trace ID.
- [Adjacent API #33 DD](../33_assignments_detail/00_Cover.md), [API #34 DD](../34_uploads/00_Cover.md) and [API #35 DD](../35_assignments_submissions/00_Cover.md).
- Current [Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py) and tests inventory — current runtime boundary.
- Canonical template: .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD.

## Tables read

- assignment_submissions — candidate lookup by id and candidate response fields.

## Tables write

- N/A — GET API; no write is defined.

## Mục chú ý

- AC-17 diagram step 10 calls GET /api/v1/submissions/{submission_id}; step 11 reads the submission summary and step 12 displays “Đã nộp”.
- AC-23 allows a Mentor to read a submission and later save grade and feedback. It does not specify whether API #36 returns score or feedback, or when those values become visible to the Student.
- Keep the catalog error set exactly 401, 403, 404 and 500. The diagram does not add an API #36-specific error branch.

## Assumptions

- Preserve the API catalog method, endpoint, Student Bearer requirement, path type, Submission response, HTTP success and error set.
- Interpret “submission summary” using the reusable Submission schema only; do not add fields or narrow the schema without a canonical decision.
- Treat assignment_submissions columns as design candidates; no live database query or schema check is performed.
- Keep all unresolved access and projection policy in OPEN_QUESTIONS.md.

## Conflicts

- The reusable Submission schema requires files as UploadAsset[], while candidate assignment_submissions stores only one nullable file_url.
- DB_UNICA_TABLES.md describes assignment_id and user_id as required; checked-in DB.sql permits both foreign keys to be NULL.
- status has a candidate DDL default SUBMITTED, but the complete SubmissionStatus enum and lifecycle are not defined.
- score and feedback are optional in Submission; access timing and release policy are not defined by AC-17.

## Security note

- The request contract has no user_id parameter; any principal identity must come from the authenticated Bearer token.
- Student role is explicit, but whether the Student must own the row, satisfy enrollment/course access, or follow another predicate is SOURCE_REQUIRED.
- Do not decide whether an inaccessible row returns 403 or is masked as 404.

## Performance note

- The candidate physical key is assignment_submissions.id; no runtime query plan, index inventory, workload target or live schema is verified.

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
