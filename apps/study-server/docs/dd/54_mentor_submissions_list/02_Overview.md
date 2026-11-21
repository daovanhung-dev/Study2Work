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
| Purpose | Đọc một trang submissions thuộc course do Mentor trực tiếp sở hữu để chọn một bài và chuyển sang API #55 xem chi tiết. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Role MENTOR; `courses.mentor_id` phải bằng numeric JWT subject. Cách này theo API #46/#49; assigned Mentor chưa được hỗ trợ. |
| Basis | AC-23 list/select flow và catalog là DIRECT; pagination, cardinality và file URL lookup là fallback DERIVED theo yêu cầu của người dùng. |
| Status | Draft — Needs Confirmation |
| Transaction | N/A — READ-ONLY API |
| Side effects | Không mutation; không commit. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md).
- [AC/API index, AC-23](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [AC-23 diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [ERD](../../diagrams/DB_UNICA_ERD.drawio).
- [Checked-in V1-PILOT DDL](../../../../../infra/postgres/study-server/DB.sql) và [uploads migration](../../../../../infra/postgres/study-server/migrations/004_uploads.sql); chưa xác minh live schema.
- [Related API #34 UploadAsset](../34_uploads/02_Overview.md) và [API #35 submission create](../35_assignments_submissions/02_Overview.md), [API #36 submission detail](../36_submissions_detail/02_Overview.md).
- [Related APIs #55–#57](../55_mentor_submissions_detail/02_Overview.md), [grade](../56_mentor_submissions_grade/02_Overview.md), [feedback](../57_mentor_submissions_feedback/02_Overview.md).
- [Current Study route source](../../../../../apps/study-server/app/api/v1.py), [auth helper](../../../../../apps/study-server/app/utils/auth.py), API #46/#49 views and tests.
- [API Guidelines](../../../../../contracts/api-guidelines/README.md) and [Study Server declared routes](../../../../../.agents/server-study/apis/declared-routes.md).
- [createDD-markdown skill](../../../../../.agents/skills/create_dd_api/docs/dd/createDD_MARKDOWN_SKILL.md).

## Tables read

- `assignment_submissions` — Submission projection and legacy `file_url`.
- `assignments` — course relation for submission visibility.
- `courses` — direct Mentor ownership.
- `users` — required Student FK join.
- `uploads` — candidate asset metadata matched by exact URL, owner, purpose and course.

## Tables write

- N/A — READ-ONLY API.

## Mục chú ý

- AC-23 says Mentor opens the grading list, then selects one submission for API #55. The original catalog/diagram typed the response as singular `Submission`; this DD and the catalog/diagram row now use `Page<Submission>` to support that flow.
- `page` defaults to 1; page size is fixed to the existing shared default 20. Ordering is `submitted_at DESC, id DESC`; page metadata is inside `data.pagination`.
- `status` is matched exactly as supplied. No enum, trimming or case normalization is introduced.
- `assignment_submissions` stores one nullable `file_url`; the fallback resolves at most one API #34 asset by URL plus `owner_id=user_id`, `purpose='SUBMISSION'` and `course_id`. No FK proves this link.
- The API remains read-only. No rubric is returned here; AC-23 sends the selected ID to API #55.
- 409 remains declared by source artifacts but has no implemented trigger because AC-23 gives no conflict rule.

## Assumptions

- The collection interpretation follows the AC-23 list-and-select flow; the previous `ApiEnvelope<Submission>` declaration is a documented conflict resolved as `ApiEnvelope<Page<Submission>>` for this implementation.
- `courses.mentor_id = authenticated numeric sub` is used because current APIs #46/#49 and API #34 lecture upload use direct ownership. This does not cover assigned Mentors.
- Page defaults use shared `DEFAULT_PAGE=1`, fixed `DEFAULT_SIZE=20`, and the existing Page shape `{items, pagination}`.
- `assignment_submissions.file_url` is assumed to store the API #34 upload URL. Only a metadata row matching URL, student owner, SUBMISSION purpose and assignment course is returned; no match produces `files: []`.
- Inner joins through `assignments`, `courses` and `users` exclude rows with null/orphan relations, matching the ERD's required relationships without changing DDL.

## Conflicts

- The original API catalog and diagram declared singular `ApiEnvelope<Submission>` while the endpoint and AC-23 flow are list/select. The implementation uses `ApiEnvelope<Page<Submission>>`; catalog and diagram were updated to make the fallback explicit.
- ERD/table guide require assignment/course/user relations; checked-in DDL permits nullable FKs. Inner joins omit orphan rows; live schema remains unverified.
- `file_url` to `uploads.url` is a `DERIVED` association, not a declared FK or API #35 guarantee.
- 409 is listed without a trigger; it remains unreachable pending a business rule.

## Security note

- Every query is scoped to `courses.mentor_id = authenticated Mentor ID` before rows are returned.
- When `course_id` is supplied, an existing course owned by another Mentor returns 403. A missing course yields an empty page because the catalog has no 404 for #54.
- Assigned-Mentor authorization is not represented in the current source or schema.

## Performance note

- The route performs a count query and a paged list query; page size is capped implicitly at 20.
- The asset lookup is a lateral query restricted by exact URL, owner, purpose and course, with at most one asset returned.
- No live query plan, index check or deployment verification is claimed.

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
