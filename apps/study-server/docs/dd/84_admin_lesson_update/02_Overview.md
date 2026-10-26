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
| Consumer/Actor | Admin; AC-34 yêu cầu lesson-management permission nhưng code hiện chỉ có shared role guard. |
| Authentication | Bearer JWT |
| Authorization | Shared `ADMIN` role guard theo catalog; chưa có policy lesson-management riêng trong Study source. |
| Direct request | `path{lesson_id:int64!}`; catalog và diagram không khai báo body/query. |
| Implemented DERIVED request | JSON full replacement gồm `title`, `content`, `video_url`, `order`; chi tiết tại [Request](./03_Request.md). |
| Direct response | `ApiEnvelope<Lesson>`; HTTP 200 `DESIGN_RESOURCE_UPDATED`. |
| Direct errors | 401/403/404/422/500 với mã `DESIGN_*` đúng catalog. |
| Basis | Method/path/auth/path type/response/status/error set DIRECT; body, mutation fields, schema mapping và transaction DERIVED hoặc SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Current implementation | Wired trong `app/api/v1.py` và `api_84_admin_lesson_update`; focused HTTP tests xác minh fake-session behavior. |
| Transaction | Một `UPDATE ... RETURNING`; view commit sau khi Lesson projection hợp lệ và rollback trên query/no-row/mapping/commit failure. |
| Side effects | Cập nhật metadata cùng `updated_at`; giữ course relation, status, audit và dependency records. |

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
| Legacy lessons | name, content, video_url, sort_order, updated_at | DERIVED từ request fallback/legacy DDL và #75 precedent; live schema chưa xác minh. |

## Mục chú ý

- #84 là nhánh UPDATE giữa detail #83 và reload; status transition/audit thuộc #85, delete/reference policy thuộc #86.
- Catalog và diagram chỉ khai báo path; body/runtime rules là DERIVED fallback, không phải direct contract.
- Runtime body yêu cầu title/content/video_url/order; null content/video_url xóa giá trị. Status thuộc #85, lesson_id ở path, course_id không thay đổi.
- Legacy course_id nullable trong khi response Lesson yêu cầu int64; V1-PILOT dùng schema khác; live DB chưa xác minh.
- Shared Admin guard yêu cầu role `ADMIN`; policy lesson-management riêng chưa có trong Study source.
- `error_response` hiện trả `data:null`; lỗi query/projection/mapping của #84 rollback và trả 500 an toàn.

## Assumptions

- title/content/video_url/order là metadata fallback dựa trên Lesson response, legacy DDL và #47 precedent; body yêu cầu đủ bốn field.
- content và video_url nhận null để clear; video_url không có URI validator vì reusable Lesson model chỉ yêu cầu string nullable.
- Một UPDATE theo lessons.id dùng RETURNING; không query dependency hoặc bảng khác.
- updated_at dùng server time theo legacy DDL và #75 precedent; không có trigger lessons trong DDL/migrations đã rà soát.
- Không thay đổi status, course_id, created_at, resource/progress records hoặc audit log.
- API #86 dùng `status='DELETED'` làm local tombstone; update query loại tombstone nên Lesson đã xóa trả 404.

## Conflicts

- Path-only catalog/diagram đối lập PUT/UPDATE intent; body runtime là DERIVED và DD giữ Draft.
- Legacy BIGINT lessons và V1-PILOT UUID/versioned lessons khác nhau; live schema chưa xác minh.
- course_id nullable trong legacy DDL nhưng required trong response Lesson.
- LessonStatus members/casing chưa có danh sách chuẩn.
- Shared guard kiểm tra `ADMIN` nhưng không chứng minh AC-34 permission riêng.
- Error guideline và helper hiện cùng dùng `data:null`; nhận định helper `{}` trước đây đã lỗi thời.

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
