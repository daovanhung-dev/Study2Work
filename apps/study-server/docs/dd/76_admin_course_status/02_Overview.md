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
| Authorization | Shared role `ADMIN` được kiểm tra; permission course-management riêng chưa có policy source. |
| Direct request | path{course_id:int64!}; không khai báo body/query. |
| Implemented fallback | JSON body `{status}` với `DRAFT`, `PUBLISHED`, `SUSPENDED`; strict/extra-forbid, DERIVED vì catalog thiếu body và enum. |
| Direct response | ApiEnvelope&lt;Page&lt;Course&gt;&gt;; 200 DESIGN_RESOURCE_UPDATED. |
| Direct errors | 401, 403, 404, 422, 500 với đúng business code trong catalog. |
| Status | Draft — Needs Confirmation |
| Current source state | Route/module có trong Study source; HTTP fake-DB tests pass cục bộ. Live schema/deployment chưa xác minh. |
| Transaction | Status update + `course_status_audit_logs` insert + Course readback nằm trong một transaction; mapping/table là DERIVED. |
| Side effects | Khi status đổi: cập nhật `courses.status`/`updated_at`, append audit row; same-status là no-op. Không đổi metadata/owner, enrollment/content hoặc soft-delete. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #76, ApiEnvelope, Page, PageMeta, Course, UserSummary.
- [AC-32 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, permission precondition và danh sách APIs #73–#77.
- [AC-32 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — nhánh STATUS: API #76 → UPDATE status + audit log → reload management.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy course model; các query là design-only.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT courses và bảng audit #76; không xác nhận live schema.
- [Migration 010](../../../../../infra/postgres/study-server/migrations/010_course_status_audit_logs.sql) — candidate incremental audit relation; chưa xác nhận đã áp dụng.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID courses/versioned course_versions và pilot audit_events; khác direct int64 API model.
- [API #71 status DD](../71_admin_user_status/02_Overview.md) — body status thiếu trong catalog được trình bày thành DERIVED proposal; user-specific session effects không áp dụng cho course.
- [API #73 list](../73_admin_courses_list/02_Overview.md), [API #74 detail](../74_admin_course_detail/02_Overview.md), [API #75 update](../75_admin_course_update/02_Overview.md) — giữ AC-32 flow, Page&lt;Course&gt; projection, singleton response proposal và metadata/status boundary.
- [Current router](../../../app/api/v1.py), [API #76 module](../../../app/modules/admin/api_76_admin_course_status/), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — source có route, shared ADMIN guard, riêng route-template allowlist và error helper.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — standard envelope, error data null và retryable mutation guidance.

## Tables read

| Relation | Candidate fields | Basis/status |
|---|---|---|
| Legacy courses | id, status, updated_at | Candidate từ DB.sql; id BIGSERIAL, status VARCHAR(20) default DRAFT; live schema chưa xác minh. |
| Legacy users | id, full_name, avatar_url | Candidate UserSummary projection theo courses.mentor_id; legacy mentor_id nullable. |
| Legacy course_status_audit_logs | course_id, actor_user_id, previous_status, new_status, changed_at | Candidate relation API #76; FK BIGINT theo legacy IDs, physical mapping DERIVED. |
| V1-PILOT courses/course_versions | UUID ids, versioned status | Khác int64 Course contract; course status nằm ở version model, không map ngầm. |
| V1-PILOT audit_events | actor_subject_id, resource_id, action, outcome, changes, trace_id | Pilot-only candidate; actor/resource IDs UUID, không khớp API/legacy int64. |

## Tables write

| Relation/effect | Candidate fields | Basis/status |
|---|---|---|
| Legacy courses | status, updated_at | Status update DIRECT intent; physical legacy mapping DERIVED; live schema unknown. |
| course_status_audit_logs | course_id, actor_user_id, previous_status, new_status | Diagram yêu cầu audit; legacy BIGINT table + actor mapping là fallback DERIVED; live schema chưa verify. |

## Mục chú ý

- Catalog và diagram không khai báo request body. Body {status:CourseStatus!} là proposal DERIVED để chỉ định target state.
- Catalog ghi các trạng thái draft/published/suspended; legacy DDL và public API #06 dùng DRAFT/PUBLISHED. Đề xuất uppercase DRAFT/PUBLISHED/SUSPENDED để khớp legacy/current convention, nhưng enum members/casing chưa được phê duyệt.
- V1-PILOT course model dùng UUID và course_versions.status gồm DRAFT/PUBLISHED/SUPERSEDED/DISCARDED; không có SUSPENDED. Pilot audit_events.resource_id là UUID; không dùng như bằng chứng persistence tương thích cho API int64.
- Diagram bắt buộc status + audit log. Runtime fallback bổ sung `course_status_audit_logs` vào legacy DDL/migration/ERD; đây là DERIVED và chưa chứng minh live schema.
- CourseStatus không có danh sách enum members trong reusable schema. Transition matrix, same-status behavior và publish readiness chưa được đặc tả.
- Public APIs #06/#08/#09 lọc PUBLISHED; status update có thể đổi public visibility. Quyền truy cập của learner đã enroll khi course suspended vẫn là policy gap.
- Response Page&lt;Course&gt; cho path mutation là DIRECT type; Page singleton với một item là DERIVED theo #74/#75.
- Course.category không có relation được duyệt; optional field được omit trong candidate response. Course.mentor và Course.price là required trong schema nhưng legacy candidate cho phép nullable/orphan values.
- API #76 có route template riêng `/api/v1/admin/courses/{course_id}/status` trong middleware allowlist; lỗi validation trả `DESIGN_VALIDATION_ERROR` và `data:null`. Tests hiện dùng fake DB.

## Assumptions

- Body chỉ chứa status; target semantics là một trong draft/published/suspended. Candidate JSON dùng uppercase DRAFT/PUBLISHED/SUSPENDED theo legacy status và API #06 convention; casing cần owner duyệt.
- Set trực tiếp target thuộc candidate enum, không thêm transition/readiness rule ngoài diagram; same-status là no-op để tránh audit duplicate (DERIVED).
- Q1 khóa course row; khi status đổi, M1 cập nhật status/updated_at và M2 ghi actor/old/new vào `course_status_audit_logs`; Q2 đọc Course projection; commit sau khi map response.
- Actor lấy numeric user ID từ shared auth JWT `sub`; FK legacy users.id là DERIVED, không dùng UUID pilot.
- Response giữ ApiEnvelope&lt;Page&lt;Course&gt;&gt; và singleton pagination như #74/#75.

## Conflicts

- Request body vắng trong catalog/diagram nhưng status cần target; body shape là contract gap.
- Giá trị target viết thường trong catalog nhưng runtime/legacy convention viết hoa; CourseStatus enum không liệt kê members.
- Legacy BIGINT courses model không có audit table. V1-PILOT có audit_events nhưng dùng UUID, trong khi API contract int64; live schema chưa xác minh.
- Page&lt;Course&gt; cardinality cho mutation by ID chưa được canonical hóa; singleton là proposal dựa #74/#75.
- Finer course-management permission chưa tồn tại; source chỉ kiểm tra shared role ADMIN. Route #76 đã có middleware template allowlist.
- API guidelines khuyến nghị Idempotency-Key cho retryable mutations; catalog không khai báo header, semantics audit khi retry chưa xác định.

## Security note

- Authenticate Bearer JWT và kiểm tra shared role ADMIN trước path parsing/query trong view; mapping sang finer course-management permission vẫn là SOURCE_REQUIRED.
- Audit actor là numeric user ID trả từ shared auth helper, ghi vào FK `actor_user_id`; không chuyển sang UUID pilot.
- Không trả email, phone, credential hoặc learner data trong Course/UserSummary projection.
- Không trả course existence trước khi authorization thành công.

## Performance note

- Candidate transaction khóa và cập nhật tối đa một course theo primary key, sau đó đọc một Course/UserSummary projection.
- Audit insert bắt buộc khi trạng thái đổi; hai index candidate hỗ trợ truy vấn theo course/actor và thời gian. Live query plan/schema chưa xác minh.
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
