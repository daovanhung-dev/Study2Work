---
title: "Cover"
order: 0
dd_id: "101"
api_name: "Lấy KPI tổng quan"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Cover"
format: markdown
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Lấy KPI tổng quan

| Thuộc tính | Giá trị |
|---|---|
| API ID | #101 |
| Method | `GET` |
| Endpoint | `/api/v1/admin/reports/summary` |
| Actor | Admin |
| Authentication | Bearer JWT |
| Query | `from?:date`, `to?:date` |
| Request body | Không có |
| Direct response | `ApiEnvelope<Report>` |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED` |
| Errors | 401, 403, 500; xem [06_Error.md](./06_Error.md) |
| DD status | `Draft — Needs Confirmation` |
| Runtime status | `UNWIRED / NOT_FOUND` trong Study source hiện tại |

## Mục đích

Trả báo cáo KPI tổng quan cho Admin theo AC-38. Catalog quy định `Report` gồm kỳ báo cáo, danh sách `ImpactMetric` và thời điểm tạo; diagram chỉ yêu cầu “Aggregate KPI summary”, chưa liệt kê metric.

## Ranh giới bằng chứng

- Method, input, response và mã lỗi là contract trực tiếp từ catalog #101.
- Bốn metric đếm bản ghi theo timestamp là proposal `DERIVED`, dùng các cột đã có trong legacy DDL; tên và phạm vi vẫn cần xác nhận.
- Pilot `report_snapshots` là alternative design candidate, chưa có report code, writer hoặc JSON mapping được nối với API #101.
- Không có runtime route, query hoặc test cho API này. Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) trước implementation.
---
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
