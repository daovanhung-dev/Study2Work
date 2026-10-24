---
title: "Lịch sử"
order: 1
dd_id: "70"
api_name: "Cập nhật thông tin/role Conditional"
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
| 1.0 | 2026-10-24 | Codex | Tạo DD theo catalog API #70, AC-31, API #14 precedent và source/schema hiện có. | Draft — Needs Confirmation; body, Admin policy và live schema chưa được xác nhận. |

## Tài liệu tham chiếu

- [Catalog API](../../../../../docs/lists/list_api.md) — contract #70, ApiEnvelope và UserProfile.
- [AC-31 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — precondition và chuỗi API quản lý user.
- [AC-31 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — chọn Update/Status/Delete; #70 update user/profile.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — legacy users candidate, design-only.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT users, không chứng minh live schema.
- [API #14 model](../../../app/modules/guest/api_14_users_me_profile/models.py), [validator](../../../app/modules/guest/api_14_users_me_profile/validate.py), [query](../../../app/modules/guest/api_14_users_me_profile/query.py) và [view](../../../app/modules/guest/api_14_users_me_profile/view.py) — profile mutation precedent hiện tại.
- [Current auth helper](../../../app/utils/auth.py) — guard hiện tại yêu cầu Student; chưa có Admin guard.
- [API #68 DD](../68_admin_users_list/02_Overview.md) và [API #69 DD](../69_admin_user_detail/02_Overview.md) — AC-31 context; macro-review được ghi nhận pending tại thời điểm tạo #70; document-level review hoàn tất sau khi tạo #72.
- [Worklog API #70](../../../../../.agents/worklog/2026-10-24/create-study-api70-dd.md) — preflight, plan và matrices trước khi author.

## Ranh giới

Không sửa router, schema, catalog hoặc diagram. Không invent enum members, validation rules, audit behavior hoặc session policy. Không coi candidate body/query là contract trực tiếp. Tại thời điểm tạo #70, macro-review còn chờ DD #71–#72; document-level review đã hoàn tất sau khi tạo #72.

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
