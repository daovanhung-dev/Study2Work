---
title: "Cover"
order: 0
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "00 Cover"
format: markdown
dd_id: "45"
api_name: "Đánh dấu tất cả đã đọc"
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Project/System | Study2Work |
| Module | STUDENT / LEARNING & INTERACTION |
| Loại tài liệu | API Detail Design |
| API ID | 45 |
| API name | Đánh dấu tất cả đã đọc |
| HTTP method | `PATCH` |
| Endpoint | `/api/v1/notifications/read-all` |
| Version | API v1 / DD 1.0 |
| Status | Draft — Needs Confirmation |
| Created by | Codex |
| Reviewed by | Chưa thực hiện |
| Approved by | Chưa phê duyệt |
| Created date | 2026-10-23 |
| Updated date | 2026-10-23 |

## Tên hiển thị

~~~text
Study2Work API design
Đánh dấu tất cả đã đọc
~~~

## Phạm vi và trạng thái

- API #45 là nhánh ALL trong AC-20; API gọi sau khi danh sách thông báo được tải.
- Current runtime: `UNWIRED / NOT_FOUND` — Study Server chưa có route, module, query hoặc test cho API này.
- Candidate update dùng `notifications.is_read`; AC-20 yêu cầu trạng thái đọc theo recipient và timestamp `read_at`.
- Hai DDL Study trong repository mô tả hai mô hình Notification khác nhau; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
- Mọi quy tắc response `Page` và body rỗng trong tài liệu này đều là `DERIVED`; chưa phải contract đã duyệt.
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
