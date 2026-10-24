---
title: "Lịch sử"
order: 1
dd_id: "68"
api_name: "Lấy danh sách user"
source_sheet: "Lịch sử"
status: "Draft — Needs Confirmation"
---

# Lịch sử update

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Ngày tạo | 2026-10-24 |
| Ngày update cuối cùng | 2026-10-24 |

## Lịch sử thay đổi

| Version | Ngày update | Người update | Nội dung update | Remarks |
|---|---|---|---|---|
| 1.0 | 2026-10-24 | Codex | Tạo DD từ catalog, AC-31 và source hiện có. | Draft — Needs Confirmation; giữ discrepancy response list/pagination. |

## Tài liệu tham chiếu

- [Catalog API](../../../../../docs/lists/list_api.md) — contract API #68 và UserProfile.
- [AC-31 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — precondition và danh sách API quản trị user.
- [AC-31 diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — list → pagination → chọn user/thao tác → reload.
- [API #4 Data Mapping](../04_users_me/05_Data_Mapping.md) và [API #14 Response](../14_users_me_profile/04_Response.md) — profile projection hiện có.
- [API #07 Data Mapping](../07_courses_search/05_Data_Mapping.md) — precedent phân trang kích thước cố định 20.
- [Worklog API #68](../../../../../.agents/worklog/2026-10-24/create-study-api68-dd.md) — preflight, plan, source trace và verification.

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Lịch sử`
- Dimension: `A1:F19`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `13`
- Số vùng merge: `17`

<details>
<summary>Danh sách vùng merge</summary>

- `E14:F14`
- `E15:F15`
- `E16:F16`
- `E17:F17`
- `E19:F19`
- `E18:F18`
- `E10:F10`
- `E11:F11`
- `E12:F12`
- `E13:F13`
- `E3:F3`
- `E4:F4`
- `E9:F9`
- `E7:F7`
- `E8:F8`
- `E5:F5`
- `E6:F6`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | Lịch sử update |  |
| 1 | `E1` | Ngày tạo |  |
| 1 | `F1` | Ngày update cuối cùng |  |
| 2 | `E2` | yyyy/mm/dd |  |
| 2 | `F2` | yyyy/mm/dd |  |
| 3 | `A3` | Version |  |
| 3 | `B3` | Ngày update |  |
| 3 | `C3` | Người update |  |
| 3 | `D3` | Nội dung update |  |
| 3 | `E3` | Remarks |  |
| 4 | `A4` | 1.0 |  |
| 4 | `B4` | yyyy/mm/dd |  |
| 4 | `D4` | Create new |  |

</details>
