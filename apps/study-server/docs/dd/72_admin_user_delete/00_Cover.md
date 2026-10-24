---
title: "Cover"
order: 0
dd_id: "72"
api_name: "Xóa/soft delete user Conditional; kiểm tra ràng buộc"
source_sheet: "Cover"
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Project/System | Study2Work — Study Server |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-31 |
| Loại tài liệu | API Detail Design |
| API ID | 72 |
| API name | Xóa/soft delete user; kiểm tra ràng buộc |
| HTTP method | DELETE |
| Endpoint | /api/v1/admin/users/{user_id} |
| Version | 1.0 |
| Status | Draft — Needs Confirmation |
| Created by | Codex |
| Reviewed by | Chờ xác nhận |
| Approved by | Chờ xác nhận |
| Created date | 2026-10-24 |
| Updated date | 2026-10-24 |

## Tên hiển thị

~~~text
DELETE /api/v1/admin/users/{user_id} — Xóa user theo policy AC-31
~~~

## Phạm vi và trạng thái

Catalog xác nhận Admin Bearer JWT, path user_id:int64!, response ApiEnvelope<DeleteResult>, HTTP 200 DESIGN_RESOURCE_DELETED và lỗi 401/403/404/422/500. AC-31 yêu cầu kiểm tra ràng buộc rồi soft delete/anonymize theo policy, sau đó reload danh sách/chi tiết.

Diagram không chọn chính sách xóa cụ thể hoặc schema vật lý. Legacy users không có cột deletion timestamp/state; schema V1-PILOT dùng UUID và không ánh xạ trực tiếp vào users BIGINT. Vì vậy DD không mô tả hard DELETE hoặc tự tạo cột/policy. Trường deleted_at của response chưa có nguồn persistence được duyệt.

Study Server chưa có route, module hoặc test API #72. Các bảng/query dưới đây được phân biệt là candidate hoặc SOURCE_REQUIRED; live schema chưa xác minh.

## Tài liệu tham chiếu

- [API catalog](../../../../../docs/lists/list_api.md) — API #72 và DeleteResult.
- [AC-31 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition và liên kết #68–#72.
- [AC-31 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — DELETE, kiểm tra ràng buộc, soft delete/anonymize theo policy và reload.
- [DD API #68](../68_admin_users_list/02_Overview.md), [#69](../69_admin_user_detail/02_Overview.md), [#70](../70_admin_user_update/02_Overview.md), [#71](../71_admin_user_status/02_Overview.md) — ranh giới list/detail/profile/status.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — users và quan hệ user-linked dạng BIGINT; artifact, không phải live schema.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID identity/profile lifecycle khác legacy users.
- [Worklog API #72](../../../../../.agents/worklog/2026-10-24/create-study-api72-dd.md) — preflight, plan và ma trận trước khi authoring.

## Phụ lục nguồn

API #72 chỉ có thể trở thành implementation-ready sau khi owner chọn policy soft-delete/anonymize, xác nhận physical schema, dependency rules, nguồn deleted_at và mapping lỗi tương ứng.

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Cover`
- Dimension: `A1:AN46`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `1`
- Số vùng merge: `40`

<details>
<summary>Danh sách vùng merge</summary>

- `O42:R42`
- `S42:Z42`
- `AA42:AD42`
- `AE42:AN42`
- `O43:R46`
- `S43:V46`
- `W43:Z46`
- `AA43:AD46`
- `AE43:AN46`
- `O40:R40`
- `S40:Z40`
- `AA40:AN40`
- `O41:R41`
- `S41:Z41`
- `AA41:AN41`
- `O38:R38`
- `S38:Z38`
- `AA38:AN38`
- `O39:R39`
- `S39:Z39`
- `AA39:AN39`
- `O36:R36`
- `S36:Z36`
- `AA36:AN36`
- `O37:R37`
- `S37:Z37`
- `AA37:AN37`
- `O34:R34`
- `S34:Z34`
- `AA34:AN34`
- `O35:R35`
- `S35:Z35`
- `AA35:AN35`
- `G14:AG20`
- `O32:R32`
- `S32:Z32`
- `AA32:AN32`
- `O33:R33`
- `S33:Z33`
- `AA33:AN33`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 14 | `G14` | Tên Project　API design<br>Tên API |  |

</details>
