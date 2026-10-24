---
title: "Overview"
order: 2
dd_id: "84"
api_name: "Cập nhật lesson"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #84 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-34 |
| Method | PUT |
| Endpoint | `/api/v1/admin/lessons/{lesson_id}` |
| Purpose | Admin cập nhật metadata của lesson được chọn. |
| Consumer/Actor | Admin có lesson-management permission |
| Authentication | Bearer JWT |
| Authorization | Role Admin theo catalog và lesson-management permission theo AC-34; Study chưa có Admin guard/policy. |
| Direct request | `path{lesson_id:int64!}`; catalog và diagram không khai báo body/query. |
| Proposed request | JSON full-replacement candidate gồm `title`, `content`, `video_url`, `order`; tất cả DERIVED. |
| Direct response | `ApiEnvelope<Lesson>`; HTTP 200 `DESIGN_RESOURCE_UPDATED`. |
| Direct errors | 401/403/404/422/500 với mã `DESIGN_*` đúng catalog. |
| Basis | Method/path/auth/path type/response/status/error set DIRECT; body, mutation fields, schema mapping và transaction DERIVED hoặc SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Current implementation | UNWIRED / NOT_FOUND — không có route/module/test API #84 trong Study source. |
| Transaction | Candidate một UPDATE nguyên tử; caller sở hữu commit/rollback theo DB helper convention; API boundary chưa xác nhận. |
| Side effects | Candidate cập nhật lesson metadata; không đổi course relation, status, audit hoặc dependency records. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #84, ApiEnvelope và Lesson.
- [AC/API index, AC-34](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin có lesson-management permission và nhóm API #82–#86.
- [AC-34 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #84 nhận path, UPDATE lesson, rồi reload danh sách.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT lessons columns; không phải live-schema proof.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID/versioned Lesson khác contract BIGINT.
- [API #09 query](../../../app/modules/guest/api_09_courses_curriculum/query.py) — alias name/title và sort_order/order.
- [API #82 list](../82_admin_lessons_list/02_Overview.md) và [API #83 detail](../83_admin_lesson_detail/02_Overview.md) — AC-34 boundary và gaps.
- [API #75 update precedent](../75_admin_course_update/02_Overview.md) — body thiếu trong catalog được giữ thành proposal DERIVED.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — current runtime boundary.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — error envelope expectation.

## Tables read

| Relation | Fields/relationship | Basis/status |
|---|---|---|
| Legacy lessons | id, course_id, name, content, video_url, sort_order, status, updated_at | Candidate BIGINT DDL; live schema chưa xác minh. |
| V1-PILOT lessons | UUID id, chapter_id, course_version_id, title, summary, position, estimated_minutes, is_preview | Mô hình khác API BIGINT; không map ngầm. |

## Tables write

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy lessons | name, content, video_url, sort_order, possibly updated_at | DERIVED từ body proposal/legacy DDL; live schema và timestamp owner chưa xác minh. |

## Mục chú ý

- #84 là nhánh UPDATE giữa detail #83 và reload; status transition/audit thuộc #85, delete/reference policy thuộc #86.
- Catalog và diagram chỉ khai báo path; body fields, requiredness, null/omission và PUT semantics chưa được đặc tả.
- Candidate body gồm title/content/video_url/order; status thuộc #85, lesson_id ở path, course_id không được đề xuất thay đổi.
- Legacy course_id nullable trong khi response Lesson yêu cầu int64; V1-PILOT dùng schema khác; live DB chưa xác minh.
- Admin auth helper chưa có; current helper chỉ có Student guard.
- API guideline yêu cầu error data:null; current helper mặc định data:{}.

## Assumptions

- title/content/video_url/order là candidate metadata fields dựa trên Lesson response và legacy columns; cần xác nhận.
- Candidate PUT dùng đủ bốn field; content/video_url có thể nhận null để clear chỉ là DERIVED.
- Candidate một UPDATE theo lessons.id dùng RETURNING để dựng response; không query dependency hoặc bảng khác.
- updated_at dùng server time chỉ khi không có trigger/owner khác.
- Không thay đổi status, course_id, created_at, resource/progress records hoặc audit log.

## Conflicts

- Path-only catalog/diagram đối lập PUT/UPDATE intent; body là SOURCE_REQUIRED, candidate chưa phải contract.
- Legacy BIGINT lessons và V1-PILOT UUID/versioned lessons khác nhau; live schema chưa xác minh.
- course_id nullable trong legacy DDL nhưng required trong response Lesson.
- LessonStatus members/casing chưa có danh sách chuẩn.
- Current Student-only guard/middleware allowlist chưa hỗ trợ Admin route.
- Error guideline data:null khác helper data:{}.

## Security note

- Xác thực Bearer, role Admin và lesson-management permission trước mutation.
- Không dùng Student guard thay Admin policy.
- Không nhận status hoặc course_id trong body proposal để giữ ranh giới #85/course ownership.
- Không trả SQL, stack trace hoặc token trong error.

## Performance note

- Candidate UPDATE lọc theo lessons.id và trả tối đa một row.
- Không có pagination, SLA, lock/version hay index contract; không thêm query/lock chưa được duyệt.
- Live query plan/index chưa xác minh.

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
