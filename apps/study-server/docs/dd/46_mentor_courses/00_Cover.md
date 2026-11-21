---
title: "Cover"
order: 0
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Cover"
format: markdown
dd_id: "46"
api_name: "Lấy course Mentor được quản lý"
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Project/System | Study2Work |
| Module | MENTOR / TEACHING & SUPPORT |
| Loại tài liệu | API Detail Design |
| API ID | 46 |
| API name | Lấy course Mentor được quản lý |
| HTTP method | `GET` |
| Endpoint | `/api/v1/mentor/courses` |
| Version | API v1 / DD 1.0 |
| Status | Draft — Needs Confirmation |
| Created by | Codex |
| Reviewed by | Chưa thực hiện |
| Approved by | Chưa phê duyệt |
| Created date | 2026-10-23 |
| Updated date | 2026-10-23 |

## Tên hiển thị

```text
Study2Work API design
Lấy course Mentor được quản lý
```

## Phạm vi và trạng thái

- API #46 đọc danh sách course trong luồng Mentor đăng bài giảng AC-21; API này không ghi dữ liệu.
- Contract: Bearer JWT, role Mentor; query `status`, `page`, `size`; response `ApiEnvelope<Page<Course>>`.
- Current Study source: `UNWIRED / NOT_FOUND`; chưa có route, module hoặc test riêng cho API #46.
- Cách lọc theo `courses.mentor_id` là candidate `DERIVED`; AC-21 cho phép cả course được phân công nhưng chưa tìm thấy assignment relation trong nguồn đã kiểm tra.
- Hai DDL course khác nhau; live schema chưa xác minh. Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
- DD này không thay đổi runtime, catalog, schema hoặc diagram; không chứng minh implementation hay deployment.
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
