---
title: "Overview"
order: 2
dd_id: "76"
api_name: "Thay đổi trạng thái khóa học Admin"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #76 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-32 |
| Method | PATCH |
| Endpoint | /api/v1/admin/courses/{course_id}/status |
| Purpose | Admin đặt trạng thái mới cho một khóa học; diagram yêu cầu cập nhật status và ghi audit log. |
| Consumer/Actor | Admin có quyền course management theo AC-32. |
| Authentication | Bearer JWT |
| Authorization | Role Admin + course-management permission; Study hiện chưa có Admin guard/policy. |
| Direct request | path{course_id:int64!}; không khai báo body/query. |
| Proposed request | JSON body {status:CourseStatus!}; DERIVED vì thao tác cần target state. |
| Direct response | ApiEnvelope&lt;Page&lt;Course&gt;&gt;; 200 DESIGN_RESOURCE_UPDATED. |
| Direct errors | 401, 403, 404, 422, 500 với đúng business code trong catalog. |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND; chưa có route/module/focused test API #76. |
| Transaction | Gộp update và audit write trong một transaction là DERIVED; physical audit table chưa được chọn. |
| Side effects | Cập nhật course.status và ghi một logical audit event theo AC-32; không thay metadata/owner, enrollment/content hoặc soft-delete. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #76, ApiEnvelope, Page, PageMeta, Course, UserSummary.
- [AC-32 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, permission precondition và danh sách APIs #73–#77.
- [AC-32 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — nhánh STATUS: API #76 → UPDATE status + audit log → reload management.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy course model; các query là design-only.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT courses; không xác nhận live schema.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID courses/versioned course_versions và pilot audit_events; khác direct int64 API model.
- [API #71 status DD](../71_admin_user_status/02_Overview.md) — body status thiếu trong catalog được trình bày thành DERIVED proposal; user-specific session effects không áp dụng cho course.
- [API #73 list](../73_admin_courses_list/02_Overview.md), [API #74 detail](../74_admin_course_detail/02_Overview.md), [API #75 update](../75_admin_course_update/02_Overview.md) — giữ AC-32 flow, Page&lt;Course&gt; projection, singleton response proposal và metadata/status boundary.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — hiện không có Admin course route/guard/path allowlist.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — standard envelope, error data null và retryable mutation guidance.

## Tables read

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy courses | id, status, updated_at | Candidate từ DB.sql; id BIGSERIAL, status VARCHAR(20) default DRAFT; live schema chưa xác minh. |
| Legacy users | id, full_name, avatar_url | Candidate UserSummary projection theo courses.mentor_id; legacy mentor_id nullable. |
| V1-PILOT courses/course_versions | UUID ids, versioned status | Khác int64 Course contract; course status nằm ở version model, không map ngầm. |
| V1-PILOT audit_events | actor_subject_id, resource_id, action, outcome, changes, trace_id | Pilot-only candidate; actor/resource IDs UUID, không khớp API/legacy int64. |

## Tables write

| Relation/effect | Candidate fields | Basis/status |
|---|---|---|
| Legacy courses | status, updated_at | Status update DIRECT intent; physical legacy mapping DERIVED; live schema unknown. |
| Audit event | Logical status-change event | Direct diagram intent; physical table/fields/key mapping SOURCE_REQUIRED. |

## Mục chú ý

- Catalog và diagram không khai báo request body. Body {status:CourseStatus!} là proposal DERIVED để chỉ định target state.
- Catalog ghi các trạng thái draft/published/suspended; legacy DDL và public API #06 dùng DRAFT/PUBLISHED. Đề xuất uppercase DRAFT/PUBLISHED/SUSPENDED để khớp legacy/current convention, nhưng enum members/casing chưa được phê duyệt.
- V1-PILOT course model dùng UUID và course_versions.status gồm DRAFT/PUBLISHED/SUPERSEDED/DISCARDED; không có SUSPENDED. Pilot audit_events.resource_id là UUID; không dùng như bằng chứng persistence tương thích cho API int64.
- Diagram bắt buộc status + audit log. Legacy DDL/ERD không có audit relation; chưa thể hoàn tất physical mapping.
- CourseStatus không có danh sách enum members trong reusable schema. Transition matrix, same-status behavior và publish readiness chưa được đặc tả.
- Public APIs #06/#08/#09 lọc PUBLISHED; status update có thể đổi public visibility. Quyền truy cập của learner đã enroll khi course suspended vẫn là policy gap.
- Response Page&lt;Course&gt; cho path mutation là DIRECT type; Page singleton với một item là DERIVED theo #74/#75.
- Course.category không có relation được duyệt; optional field được omit trong candidate response. Course.mentor và Course.price là required trong schema nhưng legacy candidate cho phép nullable/orphan values.
- Current middleware allowlist thiếu Admin course path và so sánh request.url.path bằng exact membership; dynamic course_id cần route-aware/path-pattern mapping khi wire. Guidelines yêu cầu error data null trong khi helper hiện trả {} khi data vắng mặt.

## Assumptions

- Body chỉ chứa status; target semantics là một trong draft/published/suspended. Candidate JSON dùng uppercase DRAFT/PUBLISHED/SUSPENDED theo legacy status và API #06 convention; casing cần owner duyệt.
- Đề xuất set trực tiếp target status nếu hợp lệ, không thêm transition/readiness rule ngoài diagram. Same-state/no-op behavior cần xác nhận.
- Q1 khóa course row; M1 cập nhật status và updated_at; M2 append logical audit event; Q2 dựng Course projection. Atomic transaction là DERIVED.
- Response giữ đúng ApiEnvelope&lt;Page&lt;Course&gt;&gt; và map singleton pagination như #74/#75.
- Nếu audit mapping không được chọn, không được coi mutation hoàn chỉnh; không báo thành công khi audit event bắt buộc chưa ghi.

## Conflicts

- Request body vắng trong catalog/diagram nhưng status cần target; body shape là contract gap.
- Giá trị target viết thường trong catalog nhưng runtime/legacy convention viết hoa; CourseStatus enum không liệt kê members.
- Legacy BIGINT courses model không có audit table. V1-PILOT có audit_events nhưng dùng UUID, trong khi API contract int64; live schema chưa xác minh.
- Page&lt;Course&gt; cardinality cho mutation by ID chưa được canonical hóa; singleton là proposal dựa #74/#75.
- Admin authorization và middleware error path chưa tồn tại trong current Study source.
- API guidelines khuyến nghị Idempotency-Key cho retryable mutations; catalog không khai báo header, semantics audit khi retry chưa xác định.

## Security note

- Authenticate Bearer JWT và authorize Admin/course-management permission trước khi đọc hoặc khóa course row.
- Không dùng Student guard hiện có cho Admin endpoint.
- Audit event cần gắn actor đã xác thực theo schema được duyệt; không suy luận numeric Admin ID sang UUID subject.
- Không trả email, phone, credential hoặc learner data trong Course/UserSummary projection.
- Không trả course existence trước khi authorization thành công.

## Performance note

- Candidate transaction khóa và cập nhật tối đa một course theo primary key, sau đó đọc một Course/UserSummary projection.
- Audit write là một event bắt buộc theo diagram; physical index, key type và latency chưa được xác minh.
- Không có counter query, enrollment scan hoặc content scan trong nhánh STATUS diagram.
- Không có live query plan/schema evidence.
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
