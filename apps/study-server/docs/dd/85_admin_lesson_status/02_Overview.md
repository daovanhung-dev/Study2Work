---
title: "Overview"
order: 2
dd_id: "85"
api_name: "Đổi trạng thái lesson"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #85 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-34 |
| Method | PATCH |
| Endpoint | `/api/v1/admin/lessons/{lesson_id}/status` |
| Purpose | Admin đổi trạng thái lesson đã chọn và tạo audit theo nhánh AC-34. |
| Consumer/Actor | Admin có lesson-management permission |
| Authentication | Bearer JWT |
| Authorization | Shared Study guard xác thực role `ADMIN`; permission lesson-management riêng theo AC-34 chưa được guard hiện tại kiểm tra. |
| Direct request | `path{lesson_id:int64!}`; catalog và diagram không định nghĩa body hoặc query. |
| Implemented request | Strict JSON body `{status}`; DERIVED enum `DRAFT`, `PUBLISHED`, `SUSPENDED` tái dùng tập candidate của API #76. Không có transition gate. |
| Direct response | `ApiEnvelope<Lesson>`; HTTP 200 `DESIGN_RESOURCE_UPDATED`. |
| Direct errors | 401/403/404/422/500 với đúng mã `DESIGN_*` trong catalog. |
| Basis | Method/path/auth/path type/response/status/error set và status+audit intent là DIRECT; request body, ba status value, legacy mapping và audit table là DERIVED. |
| Status | Draft — Needs Confirmation |
| Current implementation | SOURCE_BACKED locally — route, module, migration source, middleware path, and HTTP tests exist; live DB/deployment chưa xác minh. |
| Transaction | View khóa row, đổi status, append audit khi có thay đổi, map response rồi commit; lỗi rollback cả transaction. Cùng status là no-op, không audit trùng. |
| Side effects | Đổi status và ghi audit theo ý định AC-34; không sửa lesson metadata, course relation, dependencies hoặc progress. |

## Sources

- [Migration 012](../../../../../infra/postgres/study-server/migrations/012_lesson_status_audit_logs.sql) — local DERIVED audit table source; no deployment claim.

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #85, Lesson, ApiEnvelope và business codes.
- [AC/API index, AC-34](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin có lesson-management permission, nhóm API #82–#86.
- [AC-34 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — node n9 đổi status, n10 update status + audit, n13 reload danh sách.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT lessons có status và updated_at; không chứng minh live schema.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID/versioned Lesson không có status; audit_events dùng UUID resource ID.
- [API #82 list](../82_admin_lessons_list/02_Overview.md), [API #83 detail](../83_admin_lesson_detail/02_Overview.md), [API #84 update](../84_admin_lesson_update/02_Overview.md) — cùng AC-34; #84 giữ status ngoài metadata update.
- [API #76 course status](../76_admin_course_status/02_Overview.md) and API #80 — DERIVED precedents for strict status bodies, row locks and BIGINT audit relations.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — current source boundary.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — error envelope expectation.

## Tables read

| Relation | Fields/relationship | Basis/status |
|---|---|---|
| Legacy lessons | id, course_id, name, content, video_url, sort_order, status, updated_at | BIGINT source candidate được dùng bởi runtime APIs #82–#84; live schema chưa xác minh. |
| lesson_status_audit_logs | lesson_id BIGINT, actor_user_id BIGINT, previous_status, new_status, changed_at | Migration 012 DERIVED; source artifact không chứng minh đã deploy. |
| V1-PILOT lessons | UUID id, chapter_id, course_version_id, title, summary, position, estimated_minutes, is_preview | Không có status; khác ID và field set của Lesson API. |
| V1-PILOT audit_events | actor_subject_id UUID, resource_id UUID, action, outcome, business_code, trace_id, changes, metadata | Có trong pilot DDL nhưng không map trực tiếp vào legacy BIGINT lesson. |

## Tables write

| Relation | Candidate fields/effect | Basis/status |
|---|---|---|
| Legacy lessons | status; updated_at | Logical status change DIRECT; physical mapping DERIVED từ legacy DDL/runtime precedent; live target remains unverified. |
| lesson_status_audit_logs | Append actor, lesson, previous/new status | AC-34 intent DIRECT; physical mapping DERIVED từ legacy BIGINT và API #76/#80 audit pattern. |

## Mục chú ý

- API #84 cập nhật metadata; API #85 đổi status và audit; API #86 xử lý delete.
- Catalog/diagram chỉ khai báo path. Body `{status}` và enum `DRAFT/PUBLISHED/SUSPENDED` là fallback DERIVED; không áp transition matrix.
- Legacy DDL có status VARCHAR(20), default DRAFT; implementation chọn ba target value theo DERIVED fallback của API #76, chưa có owner approval riêng cho Lesson.
- V1-PILOT Lesson dùng UUID/versioned schema và không có status column. Không ghép ngầm với legacy lessons BIGINT.
- AC-34 yêu cầu audit; migration 012 khai báo bảng candidate `lesson_status_audit_logs` tương thích legacy BIGINT Lesson.
- Legacy course_id nullable trong khi reusable Lesson yêu cầu int64; live DB chưa xác minh.
- Shared ADMIN guard đã có và được dùng; fine-grained lesson-management permission theo diagram chưa được thực thi.
- Error helper hiện trả `data: null`; API #85 HTTP tests xác nhận envelope lỗi này.

## Assumptions

- Request body candidate gồm duy nhất status, required để chỉ định trạng thái đích; đây là DERIVED.
- Target status giới hạn ở `DRAFT`, `PUBLISHED`, `SUSPENDED` theo DERIVED fallback API #76; owner có thể thay đổi tập này. Không kiểm tra transition.
- Candidate legacy mutation đổi lessons.status và updated_at; không sửa metadata/dependencies.
- API #86 dùng target `DELETED` làm tombstone; #85 lock/update chỉ nhận Lesson chưa có marker này, không thể khôi phục tombstone bằng PATCH.
- Audit là tác dụng nghiệp vụ bắt buộc theo diagram; migration 012 và INSERT lưu actor, lesson, status cũ/mới. Không lưu reason chưa có trong contract.
- Status update và audit insert được commit cùng transaction; same-status request không ghi audit duplicate.

## Conflicts

- Direct path-only catalog/diagram không định nghĩa body; implementation thêm `{status}` theo DERIVED fallback.
- Legacy BIGINT source ban đầu thiếu audit relation; migration 012 thêm candidate riêng. V1-PILOT có audit_events nhưng Lesson UUID không có status.
- Lesson-specific enum/transition policy chưa có nguồn; local implementation reuses API #76 enum and adds no transition matrix.
- Shared ADMIN role guard có; route/template/module/tests API #85 hiện đã wire. Fine-grained AC-34 permission vẫn là discrepancy.
- Current helper returns `data: null`, verified by HTTP tests.

## Security note

- Xác thực Bearer JWT, role Admin và lesson-management permission trước mutation.
- Audit actor lấy numeric `sub` sau shared ADMIN validation; guard không xác nhận permission chuyên biệt.
- Không dùng Student guard cho Admin.
- Không trả SQL, stack trace hoặc token trong error.

## Performance note

- Candidate mutation lọc theo một lesson ID và trả tối đa một row.
- Không thêm dependency scan, cascade, progress rewrite, list query hoặc pagination.
- View dùng `SELECT ... FOR UPDATE` để đọc status cũ và giữ quyết định no-op/đổi status trong cùng transaction; lock là DERIVED.
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
