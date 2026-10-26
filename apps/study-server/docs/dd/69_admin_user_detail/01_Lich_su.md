---
title: "Lịch sử"
order: 1
dd_id: "69"
api_name: "Lấy chi tiết user"
source_sheet: "Lịch sử"
status: "Draft — Needs Confirmation"
---

# Lịch sử update

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Ngày tạo | 2026-10-24 |
| Ngày update cuối cùng | 2026-10-25 |

## Lịch sử thay đổi

| Version | Ngày update | Người update | Nội dung update | Remarks |
|---|---|---|---|---|
| 1.0 | 2026-10-24 | Codex | Tạo DD theo catalog API #69, AC-31 và source hiện có. | Draft — Needs Confirmation; schema và Admin authorization chưa được xác nhận. |
| 1.1 | 2026-10-25 | Codex | Triển khai route/detail query, ADMIN guard, signed-int64 path mapping và HTTP tests; cập nhật source evidence. | Các rule schema/quyền còn lại là DERIVED hoặc SOURCE_REQUIRED; DD giữ Draft. |

## Tài liệu tham chiếu

- [Catalog API](../../../../../docs/lists/list_api.md) — contract #69 và reusable UserProfile.
- [AC-31 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — precondition và thứ tự API quản lý user.
- [AC-31 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — chọn user → đọc user/profile/role → thao tác quản trị.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy users candidate, design-only.
- [API #4 query/model](../../../app/modules/guest/api_04_users_me/query.py) — safe profile projection hiện có.
- [API #14 query](../../../app/modules/guest/api_14_users_me_profile/query.py) — profile projection sau update hiện có.
- [API #68 Overview](../68_admin_users_list/02_Overview.md) — cùng AC-31; API #68 list hiện dùng `Page<UserProfile>`, còn #69 là detail.
- [Worklog API #69 design](../../../../../.agents/worklog/2026-10-24/create-study-api69-dd.md) — source review và plan authoring ban đầu.
- [Implementation worklog](../../../../../.agents/worklog/2026-10-25/implement-api69-admin-user-detail.md) — coding plan, decisions và verification.

## Ranh giới

API #69 không thay đổi catalog, diagram hoặc schema vì direct contract đã đủ cho detail. API #70–#72 vẫn sở hữu riêng profile/role, status và delete mutations; macro-review AC-31 vẫn theo dõi các policy/schema gaps còn lại.

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
