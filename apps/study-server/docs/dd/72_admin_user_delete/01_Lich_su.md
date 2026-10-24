---
title: "Lịch sử"
order: 1
dd_id: "72"
api_name: "Xóa user theo policy AC-31"
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
| 1.0 | 2026-10-24 | Codex | Tạo DD theo catalog API #72 và flow AC-31; tách intent xóa logic khỏi schema chưa có. | Draft — Needs Confirmation. |

## Tài liệu tham chiếu

- [Catalog API](../../../../../docs/lists/list_api.md) — endpoint, DeleteResult và business codes.
- [AC-31 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — API #68–#72.
- [AC-31 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — nhánh DELETE và reload.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — users và FK tham chiếu; không phải bằng chứng live.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — mô hình UUID và lifecycle khác legacy.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — users được đánh dấu DESIGN_ONLY.
- [API #68–#71 DD](../68_admin_users_list/OPEN_QUESTIONS.md) · [#69](../69_admin_user_detail/OPEN_QUESTIONS.md) · [#70](../70_admin_user_update/OPEN_QUESTIONS.md) · [#71](../71_admin_user_status/OPEN_QUESTIONS.md) — câu hỏi liên nhóm.
- [Worklog API #72](../../../../../.agents/worklog/2026-10-24/create-study-api72-dd.md) — kế hoạch và ma trận.

## Ranh giới

API #70 cập nhật profile/role; API #71 cập nhật trạng thái hoạt động; API #72 là nhánh soft-delete/anonymize theo policy. DD này không dùng API #71 để suy ra trạng thái xóa và không thêm mutation vào các API trước.

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
