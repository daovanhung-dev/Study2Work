---
title: "Cover"
order: 0
dd_id: "76"
api_name: "Thay đổi trạng thái khóa học Admin"
source_sheet: "Cover"
status: "Draft — Needs Confirmation"
---

# Study Server — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Project | Study2Work |
| Service | Study Server |
| API ID | #76 |
| Tên API | Thay đổi trạng thái khóa học Admin |
| Version | 0.1 |
| Trạng thái | Draft — Needs Confirmation |
| Ngày tạo | 2026-10-24 |
| Scope | server-study / AC-32 |

## Tên hiển thị

**PATCH /api/v1/admin/courses/{course_id}/status**

## Mục đích

Đổi trạng thái một khóa học theo thao tác Admin trong AC-32 và ghi audit event theo diagram. Request body, enum/casing, policy chuyển trạng thái, audit persistence và schema runtime chưa được xác nhận; proposal được gắn nhãn DERIVED hoặc SOURCE_REQUIRED trong các sheet.

## Phạm vi

- API #76 chỉ sở hữu thay đổi trạng thái khóa học.
- API #75 sở hữu cập nhật metadata; API #77 sở hữu xóa theo enrollment/content policy.
- Không tạo hoặc sửa source, database, schema, catalog, diagram hay runtime trong DD này.
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
