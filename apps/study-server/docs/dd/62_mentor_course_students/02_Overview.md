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
| Authorization | Role Mentor; course phải thuộc scope được cấp. Claim và owner/assignment rule chưa có runtime source. |
| Basis | Contract/actor/path/response/errors DIRECT từ catalog; active-enrollment step DIRECT từ diagram; query/projection là candidate hoặc SOURCE_REQUIRED. |
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
- [API #46 overview](../46_mentor_courses/02_Overview.md) — owner/Page<Course> precedent, not API #62 contract.
- [API #54 overview](../54_mentor_submissions_list/02_Overview.md) — pagination gap precedent.
- [API #61 overview](../61_mentor_support_resolve/02_Overview.md) — recent package convention.
- [Study router](../../../../../apps/study-server/app/api/v1.py), [response helper](../../../../../apps/study-server/app/core/responses.py), [middleware](../../../../../apps/study-server/app/core/middleware.py), [API Guidelines](../../../../../contracts/api-guidelines/README.md).
- [Study API DD workflow](../../../../../.agents/server-study/workflows/README.md).

## Tables read

- Logical intent: course roster and active enrollments.
- Legacy candidates: `courses`, `enrollments`, `users`; live use not verified.
- V1-PILOT alternative: `courses` → `course_versions` → `course_enrollments` → `learner_profiles`; UUID/versioned model, not interchangeable with legacy IDs.

## Tables write

N/A — READ-ONLY API. API #62 does not create notifications, recipients, queue jobs or deliveries.

## Mục chú ý

- AC-25 yêu cầu đọc active enrollments, sau đó UI chọn người nhận; #63 tạo và phát Notification; #64 đọc trạng thái gửi.
- `Page<Course>` trong catalog không khớp với `/students` và luồng chọn người nhận. Giữ nguyên response theo catalog, ghi mapping là `DISCREPANCY`; không dựng các dòng Course từ learner.
- PageMeta là bắt buộc, nhưng #62 không có input `page`/`size`. Không kế thừa default từ API #6/#46 hoặc tự thêm query field.
- Legacy `enrollments.status` là VARCHAR, default `ACTIVE`, chưa có enum đầy đủ. V1-PILOT dùng status `ENROLLED|IN_PROGRESS|COMPLETED` và ID UUID. Chưa nguồn nào xác nhận schema live.
- Chỉ đề xuất `Page<UserSummary>` làm projection người nhận tối giản nếu chủ sở hữu contract duyệt sửa đổi.

## Assumptions

| ID | Đề xuất | Cơ sở | Trạng thái |
|---|---|---|---|
| A-62-01 | Danh sách đủ điều kiện rỗng trả 200 với `items` rỗng, không trả 404. | Ngữ nghĩa đọc collection và Page<T>. | DERIVED — cần xác nhận. |
| A-62-02 | Mỗi learner chỉ xuất hiện một lần dù có nhiều enrollment row phù hợp. | AC-25 cho Mentor chọn người; legacy DDL không có unique course/user. | DERIVED — cần xác nhận. |
| A-62-03 | Nếu chọn legacy schema, `status='ACTIVE'` là predicate active dự kiến. | Diagram ghi active; default trong legacy DDL là ACTIVE. | DERIVED — enum/vòng đời chưa rõ. |
| A-62-04 | Response roster sau khi chỉnh contract nên dùng `Page<UserSummary>`. | Schema dùng chung hiện có `id`, `full_name`, `avatar_url?`. | DERIVED — cần phê duyệt. |

## Conflicts

| Nguồn A | Nguồn B | Xung đột | Ảnh hưởng |
|---|---|---|---|
| Catalog | `/students` endpoint and AC-25 | Catalog is `Page<Course>`; diagram reads enrollments for students. | No valid recipient mapping to Course fields. |
| PageMeta | Request row #62 | Required pagination fields but no page/size inputs. | Bounds, defaults and next-page behavior unspecified. |
| Enrollment guide | Legacy DDL | Guide says user/course FKs required; DDL allows NULL and has no course/user unique. | Orphans and recipient dedup/count grain unresolved. |
| Legacy | V1-PILOT | BIGINT enrollments/users versus UUID course_enrollments/learner_profiles; statuses differ. | No schema/key/status can be selected as live. |
| API Guidelines | Current helper | Expected error `data:null`; helper defaults absent data to `{}`. | Future wiring discrepancy; route is absent. |

## Security note

- Validate Bearer and Mentor role before reading learner data.
- Scope using authenticated Mentor's approved ownership/assignment relation; path course_id is not proof of access.
- Legacy `courses.mentor_id` is a direct-owner candidate only. Mentor claim binding and assigned-course semantics remain SOURCE_REQUIRED.
- 403/404 order is a privacy policy question; do not expose roster before access succeeds.

## Performance note

Roster có thể lớn nhưng catalog không có input phân trang. Không chốt query trả toàn bộ dữ liệu hoặc tự đặt page size. Chưa kiểm tra query plan, sản lượng hay index trên DB live.

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
