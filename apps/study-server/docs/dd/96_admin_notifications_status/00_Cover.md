---
title: "Cover"
order: 0
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Cover"
format: markdown
dd_id: "96"
api_name: "Xem trạng thái delivery notification Admin"
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Xem trạng thái delivery notification Admin

| Thuộc tính | Giá trị |
|---|---|
| API ID | #96 |
| Method | `GET` |
| Endpoint | `/api/v1/admin/notifications/{notification_id}/status` |
| Actor | Admin |
| Authentication | Bearer JWT |
| Request | Path `notification_id:int64!`; không body/query |
| Direct response | `ApiEnvelope<Notification>` |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED` |
| DD status | `Draft — Needs Confirmation` |
| Runtime status | `UNWIRED / NOT_FOUND` theo source Study hiện tại |

## Mục đích

Đặc tả contract trực tiếp của API #96 và ghi rõ khoảng cách giữa response `Notification` trong catalog với bước “Đọc delivery aggregate” trong AC-36. Không tự thêm count, channel-result hoặc operation field vào response.

## Ranh giới bằng chứng

- Catalog và AC-36 xác định contract/flow thiết kế, chưa chứng minh behavior runtime.
- Legacy DDL và V1-PILOT DDL là hai nguồn schema khác grain; không coi chúng là Admin persistence đã duyệt.
- Đọc [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) trước khi chuyển DD sang Final hoặc lập trình.
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

