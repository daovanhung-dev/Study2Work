---
title: "Cover"
order: 0
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Cover"
format: markdown
dd_id: "50"
api_name: "Tạo nội dung mới Conditional"
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Project/System | Study2Work / Study Server |
| Module | MENTOR / TEACHING |
| Loại tài liệu | API Detail Design |
| API ID | 50 |
| API name | Tạo nội dung mới Conditional |
| HTTP method | POST |
| Endpoint | `/api/v1/mentor/content` |
| Phiên bản DD | 0.1 |
| Trạng thái | Draft — Needs Confirmation |
| Ngày lập | 2026-10-24 |

## Mục đích

Đặc tả source-aware cho thao tác tạo một Content theo catalog và AC-22. Endpoint hiện chưa được nối vào Study Server runtime. Tài liệu chưa phải bằng chứng implementation hoặc live-schema mapping.

## Trạng thái xác nhận

`PENDING_REVIEW` là trạng thái dự kiến ban đầu theo tiền điều kiện của AC-33. Bảng/column lưu Content, schema payload, enum members và một số quy tắc placement còn cần xác nhận.

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
