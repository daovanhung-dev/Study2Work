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
| Purpose | Lưu score và đặt status GRADED theo AC-23 |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT, explicit MENTOR role |
| Authorization | Direct course owner qua courses.mentor_id; DERIVED fallback |
| Basis | Catalog method/path/body/response/error DIRECT; AC-23 mutation DIRECT; DB mapping và score range DERIVED theo DDL legacy |
| Status | Runtime source và TestClient test có mặt; schema live chưa xác minh; rubric persistence còn gap |
| Transaction | Handler khóa submission, kiểm tra quyền, cập nhật, dựng response rồi commit; rollback trước commit khi lỗi |
| Side effects | Chỉ assignment_submissions.score/status; feedback được giữ; API #57 vẫn là mutation riêng |

## Sources

- API catalog và reusable Submission/Assignment/UploadAsset schemas.
- AC-23 index/activity diagram: #54 → #55 → grade input → #56 → #57 feedback.
- DB table guide, legacy Study DDL và V1-PILOT DDL.
- API Guidelines, current response helper và middleware.
- API #54/#55 DD và source: shared Submission response, direct-owner policy, constrained upload lookup.
- API #56 source: app/modules/mentor/api_56_mentor_submissions_grade/.
- API #56 TestClient tests.

## Tables read

- assignment_submissions, assignments, courses.
- uploads only when file_url is non-null, for the constrained Submission.files projection.
- No UUID assessment/rubric table is joined to the legacy BIGINT submission.

## Tables write

- assignment_submissions.score and assignment_submissions.status only.
- No rubric persistence target is supported by the checked-in legacy schema.
- feedback is not changed; API #57 owns the separate feedback step.

## Mục chú ý

- Request uses required strict int32 score and required strict string rubric_items. The wire spelling rubric_items is a DERIVED fallback for catalog descriptor “rubric items”.
- rubric_items is accepted for request compatibility but is not persisted or returned. No schema relation or approved target exists; this remains an implementation gap for contract-owner confirmation.
- Integer score is stored in legacy candidate NUMERIC(6,2). DERIVED validation requires 0 <= score <= assignments.max_score; an out-of-range value maps to catalog 422.
- The source permits grading from any current status because catalog declares no 409 and no source-backed prior-state restriction.
- Submission.files reuses API #54/#55 lookup: exact file_url, submission owner, SUBMISSION purpose, course; deterministic first asset by id. No match yields files=[].
- API #35 producer compatibility remains unresolved; local fake-DB tests do not prove file_url association in a live database.
- The dynamic route is registered in DESIGN_CONTRACT_PATHS. Current error_response(None) emits data=null, matching the API Guidelines shape.
- API #56 preserves the exact catalog success and error business codes.

## Assumptions and conflicts

- Direct ownership through courses.mentor_id and numeric JWT subject mapping follow the implemented API #54/#55 fallback; assigned-Mentor access remains unverified.
- The score range [0, assignments.max_score] is a DERIVED fallback based on available columns, not an approved business rule.
- rubric_items remains required on the wire but has no persistence owner. The endpoint cannot truthfully claim durable rubric storage.
- AC-23 says grade/status update; the legacy DDL is only a checked-in candidate and does not establish deployed availability.

## Security note

The explicit MENTOR guard runs before parsing the path or reading data. The view checks direct course ownership before returning submission fields and repeats the ownership predicate in UPDATE. SQL/exception details are not returned.

## Performance note

The submission row is selected by ID and locked FOR UPDATE. The upload lookup is limited to one matching row. No live query plan or deployment behavior is claimed.
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
