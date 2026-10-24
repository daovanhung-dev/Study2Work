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
| Authorization | Mentor có quyền chấm submission thuộc course; cách ánh xạ Mentor và predicate truy cập chưa được xác nhận. |
| Basis | Catalog và AC-23 là DIRECT; mapping dữ liệu là candidate có nhãn DERIVED hoặc SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Transaction | Chưa có transaction contract được duyệt; cần bảo đảm cập nhật feedback không ghi nhầm submission. |
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
- Catalog descriptor is the literal text feedback text:string!; its JSON property spelling is unresolved.
- attachments:string! is required, but its encoding, storage, association and response field are not defined.
- Submission.files is the student-submitted asset collection; it is not assumed to contain Mentor feedback attachments.
- No API #57 route, view module or test exists in current Study source.
- The complete Submission response remains blocked by the unresolved UploadAsset resolver.

## Assumptions

- assignment_submissions.feedback TEXT is a schema-backed legacy candidate for feedback text; an UPDATE to this existing field is only a DERIVED proposal.
- Repeated-call behavior is not chosen: diagram says INSERT/UPDATE, but there is no approved feedback history relation or overwrite rule.
- The direct-owner check through courses.mentor_id is a DERIVED candidate consistent with #54–#56; assigned-Mentor access is not established.
- AC-23 UI order does not by itself make status=GRADED a direct-call precondition for API #57.

## Conflicts

- Request descriptor feedback text does not define a JSON wire key; response schema names the field feedback.
- Request requires attachments, but Submission has no feedback-attachments property and legacy candidate DDL has no attachment relation.
- Diagram mentions INSERT/UPDATE feedback, while the simple legacy candidate is one nullable feedback column.
- V1-PILOT assessment_reviews.feedback_markdown belongs to UUID assessment records and is not linked to legacy BIGINT assignment_submissions.
- API Guidelines requires error data=null; current error_response() emits {} when data is omitted.
- Current middleware uses an exact-path allowlist and does not list this dynamic Mentor path.

## Security note

- Never return or mutate a submission outside the authenticated Mentor's approved course scope.
- Current shared auth guard is Student-only; Mentor claim extraction and ID mapping are SOURCE_REQUIRED.
- Do not trust attachment URLs or identifiers until the upload/asset ownership contract is specified.

## Performance note

- Candidate lookup and update should target one submission by ID and scope it to its course.
- Attachment storage and Submission.files lookup costs cannot be determined until an approved asset relation/resolver exists.

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
