---
title: "Cover"
order: 0
dd_id: "102"
api_name: "Lấy dữ liệu tác động cộng đồng"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Cover"
format: markdown
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Lấy dữ liệu tác động cộng đồng

| Thuộc tính | Giá trị |
|---|---|
| API ID | #102 |
| Method | `GET` |
| Endpoint | `/api/v1/admin/reports/community-impact` |
| Actor | Admin |
| Authentication | Bearer JWT |
| Query | `from?:string`, `to?:string`, `segment?:string` |
| Request body | Không có |
| Direct response | `ApiEnvelope<Report>` |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED` |
| Errors | 401, 403, 500; xem [06_Error.md](./06_Error.md) |
| DD status | `Draft — Needs Confirmation` |
| Runtime status | `UNWIRED / NOT_FOUND` trong Study source hiện tại |

## Mục đích

Cung cấp các metric tác động học tập và cộng đồng cho dashboard Admin theo AC-38, cùng kỳ báo cáo và bộ lọc `segment` tùy chọn. API #101 đứng trước để lấy KPI tổng quan; #102 tập trung vào metric chi tiết hơn; #103 là nhánh export tùy chọn.

## Ranh giới bằng chứng

- Method, path, actor, kiểu query, `Report`, status và error codes là contract trực tiếp từ catalog/AC-38.
- Bốn metric theo ghi danh/hoàn thành/topic/reply và hai giá trị segment `learning`/`community` là đề xuất `DERIVED`, dựa riêng trên legacy Study DDL/ERD; chưa được duyệt và live schema chưa xác minh.
- AC-19 biểu diễn Comment riêng, trong khi legacy ERD/DDL dùng `discussions.parent_id` cho reply; đây là discrepancy cần xác nhận.
- Không có route/query/test #102 trong Study source. Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) trước implementation.
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
