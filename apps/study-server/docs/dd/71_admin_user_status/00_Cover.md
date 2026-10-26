---
title: "Cover"
order: 0
dd_id: "71"
api_name: "Khóa/mở khóa user Conditional"
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
| API ID | 71 |
| API name | Khóa/mở khóa user Conditional |
| HTTP method | PATCH |
| Endpoint | /api/v1/admin/users/{user_id}/status |
| Version | 1.1 |
| Status | Draft — Needs Confirmation |
| Created by | Codex |
| Reviewed by | Chờ xác nhận |
| Approved by | Chờ xác nhận |
| Created date | 2026-10-24 |
| Updated date | 2026-10-25 |

## Tên hiển thị

~~~text
PATCH /api/v1/admin/users/{user_id}/status — Khóa/mở khóa user
~~~

## Phạm vi và trạng thái

Catalog trực tiếp xác nhận Bearer JWT/Admin, `user_id:int64!`, `ApiEnvelope<UserProfile>`, HTTP 200 `DESIGN_RESOURCE_UPDATED` và đúng errors 401/403/404/422/500. AC-31 đặt endpoint ở nhánh STATUS; diagram yêu cầu cập nhật account status, thu hồi session “nếu cần”, rồi reload list/detail.

Runtime hiện có route, module, Admin JWT role guard và HTTP tests. Body `{status}` với hai giá trị `ACTIVE`/`SUSPENDED`, rule không đổi trạng thái lifecycle khác, `updated_at`, và thu hồi refresh tokens còn hiệu lực khi khóa là các quyết định triển khai `DERIVED`; catalog/diagram không mô tả body hoặc enum. Legacy DDL chỉ là candidate, live schema chưa xác minh.

API chỉ thu hồi refresh credentials; shared access-JWT guard không kiểm tra `users.status` hoặc revocation, nên access JWT đã cấp có thể còn dùng đến expiry. DD giữ `Draft — Needs Confirmation` cho tới khi contract, policy và schema được xác nhận.

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
