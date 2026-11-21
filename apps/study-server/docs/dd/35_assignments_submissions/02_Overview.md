---
title: "Overview"
order: 2
dd_id: "35"
api_name: "Tạo/nộp submission"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 35 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | POST |
| Endpoint | /api/v1/assignments/{assignment_id}/submissions |
| Purpose | Tạo hoặc cập nhật bài nộp của Student cho một assignment theo contract thiết kế. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | Student role; assignment eligibility/access predicate SOURCE_REQUIRED. |
| Basis | APPROVED_DESIGN_CONTRACT; AC-17 design flow |
| Status | Draft — Needs Confirmation |
| Transaction | SOURCE_REQUIRED |
| Side effects | Candidate INSERT/UPDATE assignment_submissions; AC-17 đặt trạng thái Submission là SUBMITTED. |

## Sources

- [API catalog — API #35](../../../../../docs/lists/list_api.md).
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [AC-17 — Nộp bài tập](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- [DB table design](../../diagrams/DB_UNICA_TABLES.md) and [ERD](../../diagrams/DB_UNICA_ERD.drawio).
- [Checked-in Study DDL](../../../../../infra/postgres/study-server/DB.sql), design evidence only.
- [API guidelines](../../../../../contracts/api-guidelines/README.md).
- [Adjacent API #33 DD](../33_assignments_detail/00_Cover.md) and [API #34 DD](../34_uploads/00_Cover.md).
- Current Study router/module/test inventory; API #35 is not wired.
- Canonical template: .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD.

## Tables read

- assignments — candidate lookup for the requested assignment and due_at.
- assignment_submissions — candidate existing-row lookup only if INSERT/UPDATE semantics are confirmed.

## Tables write

- assignment_submissions — candidate table named by AC-17 and DB design; physical runtime persistence is not verified.

## Mục chú ý

- AC-17 precondition says the assignment is not overdue and the Student is allowed to submit.
- AC-17 describes INSERT/UPDATE Submission = SUBMITTED, but it does not state the branch predicate or duplicate-submission rule.
- API #34 performs the preceding file upload/Object Storage flow; API #35 receives file-reference notation and does not specify a separate storage call.

## Assumptions

- Preserve API catalog method, endpoint, request tokens, response type, success code and exact error-code set.
- Keep file refs as catalog notation in the request sheet and example; the concrete JSON property and value representation remain unresolved.
- Treat DB columns and mappings as candidates from design artifacts, never as live-schema facts.
- The initial status SUBMITTED is stated by AC-17; the full SubmissionStatus enum is not defined.

## Conflicts

- Request text is required, while logical Submission.content and physical assignment_submissions.content are optional/nullable.
- Logical Submission.files is UploadAsset[], while candidate assignment_submissions has one nullable file_url and no confirmed asset-reference table.
- Table notes describe assignment_id/user_id as required; checked-in DDL permits both foreign keys to be NULL.
- The AC-17 INSERT/UPDATE flow has no declared unique key or upsert condition for assignment/user.

## Security note

- The client must not supply user_id; the intended actor identity comes from the authenticated Student principal.
- The exact enrollment, ownership, assignment visibility and direct-call authorization predicates are SOURCE_REQUIRED.
- Do not inherit API #34 upload purpose, URL, object-key or file validation policy as API #35 behavior.

## Performance note

- No query plan, workload target, index requirement or transaction boundary is specified by the design sources.
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
