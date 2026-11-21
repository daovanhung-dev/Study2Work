---
title: "Overview"
order: 2
dd_id: "62"
api_name: "Lấy tập người nhận"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 62 |
| Module | MENTOR / TEACHING & SUPPORT — AC-25 |
| Method | GET |
| Endpoint | `/api/v1/mentor/courses/{course_id}/students` |
| Purpose | Cung cấp tập học viên để Mentor chọn người nhận thông báo trong course. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Bearer JWT role `MENTOR`; current Study principal là numeric user ID; direct owner `courses.mentor_id` theo fallback triển khai. |
| Basis | AC-25 active-recipient flow DIRECT; response `UserSummary[]`, legacy schema, `ACTIVE` filter và direct owner là `DERIVED — Draft — Needs Confirmation`. |
| Status | Draft — Needs Confirmation |
| Transaction | Read-only; không có mutation. |
| Side effects | Không có; tạo và phát Notification thuộc API #63. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #62–#64, Page, PageMeta, Course, Category, Enrollment, UserSummary.
- [AC/API index, AC-25](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [AC-25 flow diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — courses, users, enrollments.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql).
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql).
- [API #46 overview](../46_mentor_courses/02_Overview.md) — numeric Mentor principal and direct-owner precedent.
- [API #49 worklog](../../../../../.agents/worklog/2026-10-25/implement-api49-mentor-content-list.md) — implementation precedent for a list-purpose endpoint with singular initial output and no pagination input.
- [API #54 overview](../54_mentor_submissions_list/02_Overview.md) — pagination gap precedent.
- [API #61 overview](../61_mentor_support_resolve/02_Overview.md) — recent package convention.
- [Study router](../../../../../apps/study-server/app/api/v1.py), [response helper](../../../../../apps/study-server/app/core/responses.py), [middleware](../../../../../apps/study-server/app/core/middleware.py), [API Guidelines](../../../../../contracts/api-guidelines/README.md).
- [Study API DD workflow](../../../../../.agents/server-study/workflows/README.md).

## Tables read

- `courses`: xác minh course tồn tại và direct owner qua `id`, `mentor_id`.
- `enrollments`: lấy người dùng ghi danh tại `course_id` với `status = 'ACTIVE'`.
- `users`: lấy `id`, `full_name`, `avatar_url`; chỉ `role = 'STUDENT'`.
- V1-PILOT `course_enrollments`/`learner_profiles` không được dùng trong implementation legacy BIGINT này.

## Tables write

N/A — READ-ONLY API. API #62 does not create notifications, recipients, queue jobs or deliveries.

## Mục chú ý

- AC-25 yêu cầu đọc active enrollments, sau đó UI chọn người nhận; #63 tạo và phát Notification; #64 đọc trạng thái gửi.
- `Page<Course>` ban đầu không khớp `/students` và luồng chọn người nhận. Fallback đã đồng bộ catalog/diagram sang `UserSummary[]`; không dựng Course giả hoặc thêm pagination input.
- `UserSummary` chỉ trả ID, tên và avatar tùy chọn; không trả email, phone hoặc account status.
- Legacy `enrollments.status` là VARCHAR, default `ACTIVE`; fallback dùng đúng predicate này. V1-PILOT dùng UUID/versioned enrollment và status khác.
- `DISTINCT` theo projection người dùng cùng `ORDER BY users.id` tạo roster duy nhất và ổn định dù legacy DDL không có unique `(course_id,user_id)`.
- Course thiếu trả 404; course thuộc Mentor khác trả 403; roster rỗng trả 200 `data: []`.
- #63 khai báo `recipients:string!` nhưng chưa quy định encoding; API #62 chỉ trả numeric UserSummary IDs và không định nghĩa serialization.

## Assumptions

| ID | Quyết định triển khai | Cơ sở | Trạng thái |
|---|---|---|---|
| A-62-01 | Course tồn tại nhưng không có eligible Student trả 200 với `data: []`. | API đọc collection recipient. | DERIVED — cần xác nhận. |
| A-62-02 | Mỗi Student xuất hiện một lần và sort theo numeric user ID tăng dần. | AC-25 chọn recipient; legacy DDL không có unique course/user. | DERIVED — cần xác nhận. |
| A-62-03 | Enrollment đủ điều kiện là `status='ACTIVE'` và `users.role='STUDENT'`. | Diagram nói active; legacy DDL/API #34 dùng `ACTIVE`. | DERIVED — status/account policy cần xác nhận. |
| A-62-04 | Response là `UserSummary[]` không phân trang. | `/students` và AC-25 roster flow; request không có `page`/`size`. | DERIVED — contract cần owner duyệt. |
| A-62-05 | Chỉ Mentor trực tiếp sở hữu `courses.mentor_id` được đọc roster. | API #46/#49/#54 current source pattern. | DERIVED — assignment access chưa hỗ trợ. |

## Conflicts and decisions

| Nguồn A | Nguồn B | Xung đột | Ảnh hưởng |
|---|---|---|---|
| Diagram/catalog ban đầu | `/students` endpoint and AC-25 | `Page<Course>` không thể biểu diễn learner recipients. | Đã chọn `UserSummary[]`, đồng bộ diagram/catalog; cần API owner xác nhận. |
| `PageMeta` | Request #62 | Response cũ yêu cầu pagination nhưng không có page/size input. | Đã bỏ pagination trong fallback; không thêm request field. |
| Enrollment guide | Legacy DDL | Guide says user/course FKs required; DDL allows NULL and has no course/user unique. | Orphans and recipient dedup/count grain unresolved. |
| Legacy | V1-PILOT | BIGINT enrollments/users versus UUID course_enrollments/learner_profiles; statuses differ. | Implementation chọn legacy local DDL; live schema chưa xác minh. |
| API #63 | API #62 | `recipients:string!` chưa nói ID/encoding. | Giữ `UserSummary.id` numeric; serialization để #63 chốt. |

## Security note

- Validate Bearer and Mentor role before reading learner data.
- Scope course lookup and roster query by authenticated numeric Mentor ID and `courses.mentor_id`.
- Assigned-course relations are not present in the selected legacy schema and do not grant access.
- Do not expose roster before the course existence/owner checks pass.

## Performance note

Request không khai báo pagination, nên fallback trả toàn bộ distinct recipient roster. Đã thêm điều kiện `ACTIVE`/`STUDENT` và order ổn định; query plan, sản lượng và index trên DB live chưa kiểm tra.

## Trạng thái liên quan

- [Plan và ma trận nguồn](./PLAN_RESULT.md).
- [Open Questions](./OPEN_QUESTIONS.md).
- [Verification report](./VERIFICATION_REPORT.md).
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
