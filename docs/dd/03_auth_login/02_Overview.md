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
| API ID | `3` |
| Module | `GUEST / ACCOUNT & DISCOVERY` |
| Method | `POST` |
| Endpoint | `/api/v1/auth/login` |
| Purpose | `Xác thực thông tin đăng nhập và trả UserProfile` |
| Consumer/Actor | `Guest` |
| Authentication | `Public; không yêu cầu Bearer token` |
| Authorization | `N/A — public login` |
| Basis | `DIRECT — list_api.md normative + AC-02 + ERD V1` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `N/A — login chỉ đọc users; không có DB mutation` |
| Side effects | `Token/session issuance sau khi credential hợp lệ; schema/transport TBD` |

## Sources

- [`docs/lists/list_api.md`](../../../docs/lists/list_api.md) — API #3 contract normative: input, `ApiEnvelope<UserProfile>`, `201/422/500`.
- [`AC-02 Đăng nhập`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — precondition, credential/status check, token/session note và các nhánh AC-only.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — bảng `users` và column-level design V1.
- [`createDD-markdown template`](../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/) — cấu trúc 8 file DD.

## Tables read

- `users` — lookup theo `email`, đọc credential hash và các column UserProfile được ERD xác nhận.

## Tables write

- `N/A — không có DB mutation được source xác nhận`.

## Mục chú ý

- `list_api.md` là contract normative cho DD: success HTTP 201 với DESIGN_RESOURCE_CREATED; lỗi normative chỉ 422 và 500.
- `AC-02` mô tả success 200, 401 cho account không tồn tại/sai mật khẩu và 403 cho account bị khóa; các nhánh này được giữ ở mục discrepancy, không thêm vào contract normative.
- `AC-02` nói client nhận token và profile, nhưng UserProfile schema không khai báo token; không tự thêm access_token vào response.

## Assumptions

- `password` được verify với `users.password_hash` bằng cơ chế hash đã được phê duyệt; algorithm/cost chưa được source xác nhận.
- `email` và `password` chỉ áp dụng required/type/email-format validation theo contract; không tự đặt min/max hoặc password policy.
- `meta = {}` vì API #3 không khai báo metadata hoặc operation_id.

## Conflicts

- `DISCREPANCY/TBD: list_api.md ghi 201 DESIGN_RESOURCE_CREATED; AC-02 ghi 200 DESIGN_RESOURCE_RETRIEVED. DD chọn list_api.md làm chuẩn.`
- `DISCREPANCY/TBD: AC-02 ghi 401/403 nhưng list_api.md không khai báo các error code này; không tự reconcile.`
- `DISCREPANCY/TBD: token/session issuance và transport chưa có response schema hoặc persistence source.`
- `DISCREPANCY/TBD: UserProfile.bio có trong contract nhưng ERD users không có column tương ứng.`

## Security note

- `Không log hoặc trả plaintext password/password_hash; không trả raw DB/hash error detail.`
- `Không yêu cầu Bearer token cho login; token/session output chỉ được mô tả là TBD, không tự tạo field.`

## Performance note

- `Lookup theo users.email; ERD đánh dấu email UNIQUE.`
- `Hash verification cost, rate limiting và lockout policy chưa được source xác nhận; không tự đặt rule.`


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

