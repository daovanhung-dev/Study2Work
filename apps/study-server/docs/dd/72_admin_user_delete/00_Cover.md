---
title: "Cover"
order: 0
dd_id: "72"
api_name: "Xóa user theo policy AC-31"
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
| API name | Xóa/soft-delete user Conditional |
| HTTP method | DELETE |
| Endpoint | /api/v1/admin/users/{user_id} |
| Version | 1.1 |
| Status | Draft — Needs Confirmation |
| Created by | Codex |
| Reviewed by | Chờ xác nhận |
| Approved by | Chờ xác nhận |
| Created date | 2026-10-24 |
| Updated date | 2026-10-25 |

## Tên hiển thị

~~~text
DELETE /api/v1/admin/users/{user_id} — Soft-delete user
~~~

## Phạm vi và trạng thái

Catalog xác nhận Bearer JWT/Admin, `user_id:int64!`, `ApiEnvelope<DeleteResult>`, HTTP 200 `DESIGN_RESOURCE_DELETED` và đúng errors 401/403/404/422/500. AC-31 yêu cầu soft-delete hoặc anonymize theo policy rồi reload danh sách/chi tiết. Runtime hiện dùng shared ADMIN guard và đánh dấu user bằng `users.status='DELETED'`; không hard-delete và không xóa các hàng liên quan.

Do legacy `users` không có `deleted_at`, response lấy `DeleteResult.deleted_at` từ `updated_at` trả về bởi cùng câu UPDATE. Timestamp này không được lưu riêng. `DELETED` là fallback DERIVED trong cột VARCHAR không có enum constraint; API #03 login/refresh từ chối trạng thái khác ACTIVE, nhưng access JWT đã cấp có thể còn hiệu lực tới expiry. Không có live schema hoặc policy owner approval; DD giữ `Draft — Needs Confirmation`.

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
