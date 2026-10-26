---
title: "Overview"
order: 2
dd_id: "57"
api_name: "Lưu feedback bài nộp Mentor"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 57 |
| Module | MENTOR / TEACHING & SUPPORT |
| Method | POST |
| Endpoint | /api/v1/mentor/submissions/{submission_id}/feedback |
| Purpose | Lưu feedback cho submission sau bước lưu điểm của API #56. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Shared guard yêu cầu role MENTOR; direct `courses.mentor_id` ownership là fallback DERIVED, chưa được contract owner xác nhận. |
| Basis | Catalog và AC-23 là DIRECT; mapping dữ liệu là candidate có nhãn DERIVED hoặc SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Transaction | View khóa submission, lặp lại owner predicate trong UPDATE, validate response rồi commit; lỗi rollback. Đây là runtime behavior, còn live DB chưa xác minh. |
| Side effects | Candidate cập nhật assignment_submissions.feedback; nơi lưu attachments chưa được xác định. |

## Sources

- [Catalog API và schema Submission / UploadAsset](../../../../../docs/lists/list_api.md).
- [AC/API index, AC-23](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [AC-23 activity diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md).
- [DB ERD](../../diagrams/DB_UNICA_ERD.drawio).
- [Legacy Study DDL candidate](../../../../../infra/postgres/study-server/DB.sql).
- [V1-PILOT schema artifact](../../../../../infra/postgres/02_study_db.sql).
- [Related API #54](../54_mentor_submissions_list/02_Overview.md), [#55](../55_mentor_submissions_detail/OPEN_QUESTIONS.md), [#56](../56_mentor_submissions_grade/OPEN_QUESTIONS.md).
- [Study route source](../../../../../apps/study-server/app/api/v1.py).
- [Study middleware](../../../../../apps/study-server/app/core/middleware.py) and [response helper](../../../../../apps/study-server/app/core/responses.py).
- [API Guidelines](../../../../../contracts/api-guidelines/README.md).
- [Study API DD workflow](../../../../../.agents/server-study/workflows/README.md).

## Tables read

- assignment_submissions — candidate source for submission existence, feedback, score and status.
- assignments — candidate relation to course for authorization scope.
- courses — direct-owner candidate for Mentor course scope.

## Tables write

- assignment_submissions — candidate UPDATE of feedback only.
- Feedback attachment storage — SOURCE_REQUIRED; no table or relation is selected.

## Mục chú ý

- AC-23 order is #54 list → #55 detail/files/rubric → #56 grade/status GRADED → #57 feedback → success.
- Catalog descriptor is the literal text feedback text:string!; `feedback_text` is the required DERIVED wire-key fallback.
- attachments:string! is required, but its encoding, storage, association and response field are not defined.
- Submission.files is the student-submitted asset collection; it is not assumed to contain Mentor feedback attachments.
- API #57 now has a route, view module and TestClient coverage; this records current local source only, not deployment or live-schema verification.
- API #54 provides a DERIVED constrained UploadAsset lookup; API #35 persistence compatibility remains unresolved, so #57 must retain that limitation.

## Assumptions

- assignment_submissions.feedback TEXT is a legacy DDL candidate; updating this existing field is DERIVED and overwrites the prior value. Live schema and approval remain unverified.
- The required `attachments` value is accepted as an opaque strict string and is not stored, returned or mapped to student `file_url`/`Submission.files`, because no approved target or format exists.
- The direct-owner check through courses.mentor_id is a DERIVED candidate consistent with #54–#56; assigned-Mentor access is not established.
- AC-23 UI order does not by itself make status=GRADED a direct-call precondition for API #57.

## Conflicts

- Request descriptor feedback text does not define a JSON wire key; `feedback_text` is the implementation fallback, not an approved catalog change.
- Request requires attachments, but Submission has no feedback-attachments property and legacy candidate DDL has no attachment relation.
- Diagram mentions INSERT/UPDATE feedback, while the simple legacy candidate is one nullable feedback column.
- V1-PILOT assessment_reviews.feedback_markdown belongs to UUID assessment records and is not linked to legacy BIGINT assignment_submissions.
- API Guidelines and current error_response() both use data=null when error data is omitted.
- Middleware matches exact paths and registered FastAPI route templates; #57's route template is now registered for design-contract errors.

## Security note

- Never return or mutate a submission outside the authenticated Mentor's approved course scope.
- Shared auth guard supports explicit MENTOR role and returns the numeric subject; direct-owner access is implemented as DERIVED fallback.
- Do not trust attachment URLs or identifiers until the upload/asset ownership contract is specified.

## Performance note

- Candidate lookup and update should target one submission by ID and scope it to its course.
- Feedback attachment storage remains unresolved. Student `Submission.files` reuses the #54 URL/owner/purpose/course lookup as DERIVED; API #35 producer compatibility remains open.

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
