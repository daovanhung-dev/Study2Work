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
| Authorization | Role Admin theo catalog và lesson-management permission theo AC-34; Study hiện chưa có Admin guard/policy. |
| Direct request | `path{lesson_id:int64!}`; catalog và diagram không định nghĩa body hoặc query. |
| Proposed request | JSON body có một field `status: LessonStatus`; DERIVED để chỉ định trạng thái đích. Enum, casing và transition chưa biết. |
| Direct response | `ApiEnvelope<Lesson>`; HTTP 200 `DESIGN_RESOURCE_UPDATED`. |
| Direct errors | 401/403/404/422/500 với đúng mã `DESIGN_*` trong catalog. |
| Basis | Method/path/auth/path type/response/status/error set và status+audit intent là DIRECT; body, physical mapping và transaction cụ thể là DERIVED hoặc SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Current implementation | UNWIRED / NOT_FOUND — không có route/module/test API #85 trong Study source. |
| Transaction | DERIVED proposal: status và audit cùng transaction để tránh partial success; physical audit mapping và caller chưa được xác định. |
| Side effects | Đổi status và ghi audit theo ý định AC-34; không sửa lesson metadata, course relation, dependencies hoặc progress. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #85, Lesson, ApiEnvelope và business codes.
- [AC/API index, AC-34](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin có lesson-management permission, nhóm API #82–#86.
- [AC-34 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — node n9 đổi status, n10 update status + audit, n13 reload danh sách.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT lessons có status và updated_at; không chứng minh live schema.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID/versioned Lesson không có status; audit_events dùng UUID resource ID.
- [API #82 list](../82_admin_lessons_list/02_Overview.md), [API #83 detail](../83_admin_lesson_detail/02_Overview.md), [API #84 update](../84_admin_lesson_update/02_Overview.md) — cùng AC-34; #84 giữ status ngoài metadata update.
- [API #71 user status](../71_admin_user_status/02_Overview.md) and [API #76 course status](../76_admin_course_status/02_Overview.md) — precedent giữ body/enum/audit gaps rõ ràng.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — current source boundary.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — error envelope expectation.

## Tables read

| Relation | Fields/relationship | Basis/status |
|---|---|---|
| Legacy lessons | id, course_id, name, content, video_url, sort_order, status, updated_at | Candidate BIGINT DDL; status default DRAFT; live schema chưa xác minh. |
| V1-PILOT lessons | UUID id, chapter_id, course_version_id, title, summary, position, estimated_minutes, is_preview | Không có status; khác ID và field set của Lesson API. |
| V1-PILOT audit_events | actor_subject_id UUID, resource_id UUID, action, outcome, business_code, trace_id, changes, metadata | Có trong pilot DDL nhưng không map trực tiếp vào legacy BIGINT lesson. |

## Tables write

| Relation | Candidate fields/effect | Basis/status |
|---|---|---|
| Legacy lessons | status; updated_at candidate | Logical status change DIRECT; physical mapping DERIVED từ legacy DDL; live target chưa chọn. |
| Audit event | Append logical status-change event | AC-34 intent DIRECT; physical table/key/payload SOURCE_REQUIRED. Không suy diễn INSERT. |

## Mục chú ý

- API #84 cập nhật metadata; API #85 đổi status và audit; API #86 xử lý delete.
- Catalog/diagram chỉ khai báo path. Một field body status là phương án tối thiểu DERIVED; không có enum member hoặc transition matrix được phê duyệt.
- Legacy DDL có status VARCHAR(20), default DRAFT; điều này không xác nhận tập target status hợp lệ.
- V1-PILOT Lesson dùng UUID/versioned schema và không có status column. Không ghép ngầm với legacy lessons BIGINT.
- AC-34 yêu cầu audit nhưng chưa có physical mapping dùng được với schema Lesson được chọn.
- Legacy course_id nullable trong khi reusable Lesson yêu cầu int64; live DB chưa xác minh.
- Admin guard/policy chưa có; current helper là Student-only.
- API guideline yêu cầu error data:null; current helper mặc định absent data thành {}.

## Assumptions

- Request body candidate gồm duy nhất status, required để chỉ định trạng thái đích; đây là DERIVED.
- Target status được kiểm tra theo enum được owner phê duyệt; enum và transition chưa được đặt ra trong DD.
- Candidate legacy mutation chỉ đổi lessons.status và có thể chạm updated_at; không sửa metadata/dependencies.
- Audit là tác dụng nghiệp vụ bắt buộc theo diagram; không định nghĩa physical INSERT, action name hoặc payload.
- DERIVED proposal: chỉ coi status update thành công khi audit được ghi theo mapping được duyệt và transaction hoàn tất.

## Conflicts

- Direct path-only input đối lập với thao tác cần trạng thái đích; request body chưa có trong catalog/diagram.
- Legacy BIGINT schema có status nhưng thiếu audit relation; V1-PILOT có audit_events nhưng Lesson UUID không có status.
- LessonStatus member values/casing/transition policy chưa có nguồn.
- Current Admin route/guard/test không tồn tại.
- API guideline error data:null khác default data:{} trong current helper.

## Security note

- Xác thực Bearer JWT, role Admin và lesson-management permission trước mutation.
- Audit actor cần ánh xạ từ Admin principal; claim shape và principal ID chưa có nguồn.
- Không dùng Student guard cho Admin.
- Không trả SQL, stack trace hoặc token trong error.

## Performance note

- Candidate mutation lọc theo một lesson ID và trả tối đa một row.
- Không thêm dependency scan, cascade, progress rewrite, list query hoặc pagination.
- Lock/version/index/SLA chưa được đặc tả; chưa đề xuất lock hay compare-and-swap.
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
