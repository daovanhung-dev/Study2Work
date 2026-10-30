---
title: "Lịch sử"
order: 1
dd_id: "71"
api_name: "Khóa/mở khóa user Conditional"
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
| 1.0 | 2026-10-24 | Codex | Tạo DD theo catalog API #71, AC-31, source API #3/#4 và schema artifacts hiện có. | Draft; body/status/session policy chưa được xác nhận. |
| 1.1 | 2026-10-25 | Codex | Ghi nhận runtime #71; phân biệt direct contract và DERIVED body/status, current-state gate, refresh-token revoke, error mapping và access-JWT giới hạn. | 21 HTTP tests; live schema và policy vẫn chưa xác minh. |

## Tài liệu tham chiếu

- [Catalog API](../../../../../docs/lists/list_api.md) — contract #71 và reusable UserProfile/UserStatus.
- [AC-31 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — precondition và APIs #68–#72.
- [AC-31 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — STATUS branch, conditional session revoke, reload list/detail.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT `users` và `refresh_tokens`; không chứng minh live schema.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID identity projection có enum khác legacy model.
- [API #3 token queries](../../../app/modules/guest/api_03_auth_login/query.py) và [flow](../../../app/modules/guest/api_03_auth_login/view.py) — login/refresh, ACTIVE check và token rotation.
- [Current auth helper](../../../app/utils/auth.py) — access JWT claims/roles; không tra account status/session revocation.
- [API #4 profile model](../../../app/modules/guest/api_04_users_me/models.py) — response allowlist hiện có.
- [API #68 overview](../68_admin_users_list/02_Overview.md), [#69 open questions](../69_admin_user_detail/OPEN_QUESTIONS.md), [#70 data mapping](../70_admin_user_update/05_Data_Mapping.md) — AC-31 boundaries.
- [Implementation worklog](../../../../../.agents/worklog/2026-10-25/implement-api71-admin-user-status.md) — pre-code plan, source trace và verification.

## Ranh giới

API #71 chỉ đổi account status và thu hồi refresh credentials khi target là SUSPENDED. API #70 sở hữu profile/role; API #72 sở hữu soft-delete/anonymize. Không thêm audit, self-lock/last-admin policy hoặc cơ chế revoke access JWT chưa có nguồn.

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
