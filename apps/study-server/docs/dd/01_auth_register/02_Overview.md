---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `1` |
| Module | `GUEST / ACCOUNT & DISCOVERY` |
| Method | `POST` |
| Endpoint | `/api/v1/auth/register` |
| Purpose | `Tạo tài khoản mới từ email, mật khẩu và họ tên` |
| Consumer/Actor | `Guest` |
| Authentication | `Public; không yêu cầu Bearer token` |
| Authorization | `N/A — public registration` |
| Basis | `DIRECT — approved design contract + AC-01` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `Transaction cho INSERT vào users; không có profile table được ERD xác nhận` |
| Side effects | `Post-create verification dispatch theo AC-01; Email Provider failure được log/retry` |

## Sources

- [`docs/lists/list_api.md`](../../../docs/lists/list_api.md) — API #1 contract, schema và business code design-only.
- [`AC-01 Đăng ký tài khoản`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — actor, flow, validation, duplicate check và verification dispatch.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — bảng `users` và column-level design V1.
- [`createDD-markdown template`](../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/) — cấu trúc file DD.

## Tables read

- `users` — duplicate email lookup (design-only ERD).

## Tables write

- `users` — INSERT account record.

## Mục chú ý

- `API #1 chỉ mô tả register; không tạo DD riêng cho API #2 trong batch này.`
- `Folder name assumption: 01_auth_register được suy ra từ list number 1 và endpoint.`

## Assumptions

- `Verification dispatch là post-create side effect; registration không rollback sau COMMIT chỉ vì email retry.`
- `Exact password min/max policy chưa có trong contract; không tự đặt giới hạn.`
- `created_at/updated_at generation source chưa được ERD xác nhận.`

## Conflicts

- `DISCREPANCY: AC-01 ghi “user + hồ sơ mặc định”, nhưng ERD V1 chỉ có bảng users; DD chỉ map users.`
- `DISCREPANCY: UserProfile.bio có trong API schema nhưng không có column trong ERD; response mapping giữ gap/TBD.`

## Security note

- `Hash password trước khi persistence; không lưu hoặc trả plaintext password/password_hash trong response.`
- `Không trả raw SQL, DB error detail hoặc secret trong error response.`

## Performance note

- `Duplicate check dùng unique email; không có pagination.`
- `Verification dispatch tách khỏi transaction users để retry không tạo account trùng.`

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
