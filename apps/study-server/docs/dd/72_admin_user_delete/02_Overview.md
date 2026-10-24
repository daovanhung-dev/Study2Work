---
title: "Overview"
order: 2
dd_id: "72"
api_name: "Xóa user theo policy AC-31"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #72 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-31 |
| Method | DELETE |
| Endpoint | /api/v1/admin/users/{user_id} |
| Purpose | Yêu cầu xóa user theo policy quản trị đã được phê duyệt sau khi kiểm tra ràng buộc. |
| Consumer/Actor | Admin có quyền quản lý user theo precondition AC-31. |
| Authentication | Bearer JWT |
| Authorization | Role Admin và quyền user management; Study hiện chưa có Admin guard/policy. |
| Direct request | path user_id:int64!; không có body/query được khai báo. |
| Direct response | ApiEnvelope<DeleteResult>; 200 DESIGN_RESOURCE_DELETED. |
| DeleteResult | id:int64, status literal "deleted", deleted_at:date-time. |
| Direct errors | 401/403/404/422/500 với đúng mã DESIGN_* theo catalog. |
| Basis | Method/path/auth/input/response/codes DIRECT; physical policy, dependency rules và persistence SOURCE_REQUIRED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND — không có route, module hoặc test API #72. |
| Transaction | Chưa có policy/schema để xác định target, transaction hoặc rollback. |
| Side effects | AC-31 yêu cầu soft delete/anonymize theo policy; không yêu cầu physical DELETE. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #72, ApiEnvelope, DeleteResult.
- [AC/API index, AC-31](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — Admin user-management precondition và API group.
- [AC-31 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #68 list → #69 detail → Update/Status/Delete → #72 → reload.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate users BIGINT và FK relations; live schema chưa xác minh.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID identity_projections/account_status và learner_profiles.deleted_at; khác legacy users.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — users field/relationship overview ở trạng thái design-only.
- [API #68–#71 overview](../68_admin_users_list/02_Overview.md), [#69](../69_admin_user_detail/02_Overview.md), [#70](../70_admin_user_update/02_Overview.md), [#71](../71_admin_user_status/02_Overview.md) — group boundaries.

## Tables read

| Relation | Fields/relationship candidate | Basis/status |
|---|---|---|
| Legacy users | id, role, status and existing profile columns | Candidate lookup only from legacy DDL; no deleted_at/anonymized_at; live schema unknown. |
| Legacy user-linked relations | courses.mentor_id; enrollments.user_id; lesson_progress.user_id; quiz_attempts.user_id; assignment_submissions.user_id; discussions.user_id; notifications.user_id/sender_id; payments.user_id; refresh_tokens.user_id | Legacy DDL dependency candidates only; not proof of live FK constraints or deletion policy. |
| V1-PILOT identity_projections | UUID subject, account_status, identity_version | Different identity model; not a BIGINT users target. |
| V1-PILOT learner_profiles | UUID subject, deleted_at, profile fields | Different profile model; no approved mapping to API user_id. |

## Tables write

Chưa xác định physical relation/column để soft-delete hoặc anonymize. Không có physical DELETE/UPDATE được phê duyệt trong nguồn hiện tại.

## Mục chú ý

- Diagram chỉ định soft delete/anonymize theo policy; không chọn một trong hai và không nêu field/transition.
- DeleteResult yêu cầu deleted_at nhưng legacy users không có deletion timestamp.
- Legacy DDL cho thấy nhiều relation user-linked; diagram không định nghĩa relation nào chặn xóa, relation nào giữ lịch sử hoặc có cascade.
- Catalog 422 tồn tại nhưng không nói dependency condition cụ thể hoặc cách ánh xạ policy conflict.
- Không khẳng định refresh_tokens ON DELETE CASCADE được kích hoạt; đó là DDL artifact trong khi candidate flow không hard-delete.
- API #68 list response/cardinality mismatch vẫn tồn tại; API #72 không tự sửa #68.
- Email/phone là PII; response DeleteResult không trả profile/credential.

## Candidate mapping — DERIVED

Trước hết authorize Admin, sau đó locate target và đánh giá các ràng buộc theo policy đã được duyệt. Nếu policy cho phép, thực hiện soft-delete hoặc anonymization đã được chọn và trả DeleteResult. Đây chỉ là flow logic theo diagram; Q2 dependencies, physical mutation, transaction và deleted_at source đều SOURCE_REQUIRED. Không được dùng hard DELETE làm fallback.

## Conflicts

- Legacy users BIGINT không có deletion field; V1-PILOT UUID model có lifecycle/deleted_at nhưng không tương đương.
- Diagram cho phép soft-delete/anonymize nhưng physical policy chưa được chọn.
- Catalog yêu cầu deleted_at trong success response nhưng chưa có source.
- Legacy DDL có FK tới users; live constraints và retention/dependency policy chưa xác minh.
- Current Study không có Admin authorization; endpoint chưa được wire.
- Error guideline mong data null; current helper mặc định {}. Middleware allowlist chưa có path #72.

## Security note

- Authenticate và authorize Admin/user-management trước khi xác nhận target tồn tại hoặc đọc dữ liệu liên quan.
- Không đọc hoặc trả password_hash, refresh-token hash hay thông tin profile không cần thiết.
- Không log token, email, phone hoặc dữ liệu user trong response.
- Anonymization, retention, audit actor/reason và quyền xóa Admin/user cụ thể cần policy owner xác nhận.

## Performance note

- Lookup theo một user_id có thể dùng khóa chính nếu legacy schema được chọn; live index/query plan chưa xác minh.
- Dependency check không thể định cỡ hoặc tối ưu trước khi policy xác định các relation cần kiểm tra.
- Không đề xuất migration/index khi chưa có schema owner và workload.

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
