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
| Purpose | Đánh dấu user đã xóa logic theo fallback soft-delete. |
| Consumer/Actor | Admin theo precondition AC-31. |
| Authentication | Bearer JWT |
| Authorization | Shared `ADMIN` JWT role theo API #68–#71; dedicated permission/tenant/MFA chưa có source. |
| Direct request | `path{user_id:int64!}`; không body/query. |
| Direct response | `ApiEnvelope<DeleteResult>`; 200 `DESIGN_RESOURCE_DELETED`. |
| DeleteResult | `id:int64`, `status:"deleted"`, `deleted_at:date-time`. |
| Direct errors | 401/403/404/422/500 với đúng mã `DESIGN_*`. |
| Basis | Method/path/auth/input/response/codes DIRECT; `status='DELETED'`, timestamp mapping và dependency behavior DERIVED. |
| Status | Draft — Needs Confirmation |
| Runtime state | SOURCE_BACKED_WITH_DERIVED_CONTRACT; route/module/focused HTTP tests đã wire. |
| Transaction | Một conditional `UPDATE users`; map DeleteResult trước commit; lỗi query/mapping/commit rollback. |
| Side effects | Đổi status và updated_at; giữ profile, refresh-token rows và mọi user-linked records. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #72 và DeleteResult.
- [AC-31 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — DELETE branch, logical delete theo policy, reload.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — BIGINT users, VARCHAR status, updated_at và FK relations; live schema chưa xác minh.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID identity lifecycle; không dùng làm target API int64.
- [API #03 auth](../../../app/modules/guest/api_03_auth_login/view.py) — login/refresh yêu cầu status ACTIVE.
- [API #68–#71 DD](../68_admin_users_list/02_Overview.md), [#69](../69_admin_user_detail/02_Overview.md), [#70](../70_admin_user_update/02_Overview.md), [#71](../71_admin_user_status/02_Overview.md) — cùng Admin group.

## Tables read

| Relation | Fields/relationship | Basis/status |
|---|---|---|
| Legacy `users` | `id`, `status`, `updated_at` | Conditional UPDATE dùng primary key và trạng thái để tránh lặp marker; checked-in candidate. |

## Tables write

| Relation | Fields | Operation/status |
|---|---|---|
| Legacy `users` | `status`, `updated_at` | Đặt `status='DELETED'`, `updated_at=CURRENT_TIMESTAMP`; fallback DERIVED, không migration. |

## Mục chú ý

- Soft-delete giữ nguyên user row nên mọi foreign-key reference vẫn còn hợp lệ; không cần hard-delete dependency blocker/cascade query cho fallback này.
- User đã có `status='DELETED'` hoặc không tồn tại nhận 404; không thêm 409.
- Response `deleted_at` là alias của `updated_at` từ mutation hiện tại, không phải column được lưu riêng.
- API #03 chặn login/refresh do chỉ cho ACTIVE; shared access-JWT guard không đọc status nên token đã cấp có thể còn hiệu lực tới expiry.
- API #68/#69 không lọc status; user DELETED vẫn hiển thị cho Admin với marker trạng thái. API #70 không đổi status; API #71 từ chối state ngoài ACTIVE/SUSPENDED.
- Soft-delete giữ PII và không có self/last-Admin, audit, retention hoặc anonymization rule được phê duyệt.

## Assumptions

- Chọn soft-delete marker `DELETED` vì không có field physical delete/anonymization được duyệt; đây là DERIVED fallback theo chỉ thị chọn phương án đơn giản.
- Mọi linked records được giữ lại; status marker không làm thay đổi relation.
- `updated_at` được dùng làm timestamp sự kiện trong response; không khẳng định timestamp xóa được lưu độc lập.

## Conflicts

- Diagram/catelog yêu cầu logical deletion/DeleteResult; legacy users thiếu `deleted_at`, còn V1-PILOT dùng UUID khác model.
- Catalog nói kiểm tra ràng buộc nhưng không chỉ ra relation nào chặn; soft-delete được chọn để bảo toàn toàn bộ FK row.
- Policy owner vẫn cần xác nhận marker, PII retention/anonymization, timestamp persistence, idempotency và Admin safeguards.

## Security note

- Shared ADMIN JWT guard chạy trước path parsing/query; dedicated permission policy chưa có source.
- Không đọc/trả password hash, token hash hoặc profile trong DeleteResult.
- Status DELETED chặn login/refresh mới nhưng không thu hồi access JWT đang tồn tại.

## Performance note

- Mutation theo `users.id` primary key; một statement, không quét các quan hệ user-linked.
- Không có live query plan hoặc schema metadata; fake DB test không đo hiệu năng database.

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
