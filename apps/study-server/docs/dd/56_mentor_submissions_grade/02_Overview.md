---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "56"
api_name: "Lưu điểm bài làm Mentor"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #56 |
| Module | Mentor / submissions |
| Method | POST |
| Endpoint | /api/v1/mentor/submissions/{submission_id}/grade |
| Purpose | Lưu điểm submission và đặt trạng thái GRADED theo AC-23 |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Catalog yêu cầu role Mentor; quyền theo course là precondition AC-23 |
| Basis | API method/path/field/error contract DIRECT; AC-23 mutation DIRECT; DB mapping là candidate DESIGN_ONLY |
| Status | Draft — Needs Confirmation |
| Transaction | SOURCE_REQUIRED; current DB helpers do not commit, and no API #56 transaction rule exists |
| Side effects | Candidate update submission score/status; rubric persistence unresolved; feedback belongs to API #57 |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — API #56 and reusable Submission/Assignment/UploadAsset schemas.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-23 actor, precondition and postcondition.
- [AC-23 activity diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — call order and grade/status action.
- [Submission table guide](../../diagrams/DB_UNICA_TABLES.md) — design-only candidate columns.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT-era tables.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — separate UUID assessment rubric model.
- [API Guidelines](../../../../../contracts/api-guidelines/README.md) — shared error envelope contract.
- [Current response helper](../../../app/core/responses.py) — current error data serialization.
- [Current middleware](../../../app/core/middleware.py) — validation/system business-code path mapping.
- [API #55 detail DD](../55_mentor_submissions_detail/02_Overview.md) — access, files and rubric gaps.
- [Open Questions](./OPEN_QUESTIONS.md) — unresolved contract and schema decisions.

## Tables read

- Candidate: assignment_submissions.
- Candidate: assignments.
- Candidate: courses.
- Rubric tables: not selected; the pilot rubric model has no approved relation to assignment_submissions.

## Tables write

- Candidate only: assignment_submissions.score and assignment_submissions.status.
- No rubric table is approved for this endpoint.
- No feedback write; API #57 is a separate call.

## Mục chú ý

- Preserve the exact catalog success and error business codes.
- Catalog body field rubric items is required string, but its wire-key spelling and value schema are unresolved.
- Request score is int32 while response score is optional decimal-string and assignment max_score is decimal(6,2); range and conversion are unconfirmed.
- Response files[] is required by Submission, but legacy DDL has only one file_url column and no approved asset resolver.
- API Guidelines expects error data=null; current error_response() serializes {} when data is None. The API #56 route does not exist yet.
- Middleware uses exact path equality for its design-code allowlist; the dynamic API #56 path is not present, so generic validation/system fallbacks would not emit the catalog DESIGN_* codes.
- The AC-23 group review #54–#57 remains pending until API #57 DD exists.

## Assumptions

- Direct ownership through courses.mentor_id is a DERIVED access candidate only; it does not establish assigned Mentor support or JWT subject mapping.
- The API #56 update is limited to score and status GRADED because that is the mutation shown by AC-23. No rubric persistence is implied.

## Conflicts

- Request score:int32 differs from response Submission.score:decimal-string?.
- rubric items:string! has no field spelling/item encoding or assignment-rubric storage contract.
- AC-23 requests rubric in #55, but Submission schema has no rubric field.
- API #54 is singular in catalog although AC-23 uses it as a submission list.
- Error-envelope expected data=null differs from the current helper output {}; the API #56 dynamic route is also absent from the middleware design-code allowlist.

## Security note

Do not serialize candidate Submission fields until the authenticated Mentor access check succeeds. Current Study auth helper exposes a Student guard only; a Mentor guard and principal mapping are not implemented.

## Performance note

The endpoint is unwired and live schema is unverified. No query plan, lock strategy or load claim is made.
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
