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
| Transaction | `Expected: catalog chưa đặc tả persistence; current source insert refresh_tokens và commit sau khi phát hành token` |
| Side effects | `Expected: AC-02 yêu cầu token/session; current source phát hành access/refresh token và lưu refresh-token hash` |

## Sources

- [`docs/lists/list_api.md`](../../../../../docs/lists/list_api.md) — API #3 contract normative: input, `ApiEnvelope<UserProfile>`, `201/422/500`.
- [`AC-02 Đăng nhập`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — precondition, credential/status check, token/session note và các nhánh AC-only.
- [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) — bảng `users` và column-level design V1.
- [`createDD-markdown template`](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — cấu trúc 8 file DD.
- [`login route`](../../../app/api/v1.py), [module #03](../../../app/modules/guest/api_03_auth_login/view.py), [DDL candidate](../../../../../infra/postgres/study-server/DB.sql) — current source và schema artifact, không chứng minh runtime/live DB.

## Tables read

- Expected: catalog không xác định bảng/persistence.
- Current login source: `users` — lookup theo email, credential hash, role/status và các field profile được query.

## Tables write

- Expected: persistence chưa được catalog đặc tả.
- Current login source: `refresh_tokens` — INSERT `user_id`, `token_hash`, `expires_at`, `created_at`; chỉ token hash được lưu. Repo DDL là candidate, không phải bằng chứng live schema.

## Mục chú ý

- `list_api.md` là contract normative cho DD: success HTTP 201 với DESIGN_RESOURCE_CREATED; lỗi normative chỉ 422 và 500.
- `AC-02` và current source cùng dùng success HTTP 200, 401 cho credential không hợp lệ và 403 cho account không ACTIVE. Catalog vẫn là expected contract normative: 201 và chỉ 422/500.
- Current source trả profile cộng `access_token`, `refresh_token`, `token_type`, `expires_in`, `refresh_expires_in`; catalog `UserProfile` không khai báo token, vì vậy không đưa token fields vào ví dụ contract.
- Route `/api/v1/auth/refresh` hiện được đánh dấu cùng API #03 trong router/module nhưng không có catalog row hoặc AC-02 step riêng; DD này giữ nó là source-only discrepancy, không gộp vào login contract.

## Assumptions

- Expected validation: catalog chỉ nêu required/type/email-format, không đặc tả min/max hay password policy.
- Current source chuẩn hóa email bằng trim/email validator với max 255 và từ chối password chỉ có whitespace; đây là current behavior, chưa được nâng thành policy normative.
- Current source gọi `app.core.security.verify_password` trên `users.password_hash`; DD không tự xác định thuật toán/cost ngoài code/config hiện hành.
- `meta = {}` vì API #3 không khai báo metadata hoặc operation_id.

## Conflicts

- `DISCREPANCY/TBD: list_api.md ghi 201 DESIGN_RESOURCE_CREATED; AC-02 ghi 200 DESIGN_RESOURCE_RETRIEVED. DD chọn list_api.md làm chuẩn.`
- `DISCREPANCY/TBD: AC-02 ghi 401/403 nhưng list_api.md không khai báo các error code này; không tự reconcile.`
- `DISCREPANCY: current source phát hành token và ghi refresh_tokens, trong khi catalog không đặc tả response token hoặc persistence.`
- `DISCREPANCY: router cũng khai báo /auth/refresh nhưng catalog không có API ID/contract riêng.`
- `DISCREPANCY/TBD: UserProfile.bio có trong contract nhưng ERD users không có column tương ứng.`

## Security note

- `Không log hoặc trả plaintext password/password_hash; không trả raw DB/hash error detail.`
- `Không yêu cầu Bearer token cho login. Current token fields là source behavior; không đưa chúng vào contract UserProfile nếu chưa được duyệt.`

## Performance note

- `Lookup theo users.email; ERD đánh dấu email UNIQUE.`
- `Hash verification cost, rate limiting và lockout policy chưa được contract xác nhận; current source yêu cầu status ACTIVE nhưng không chứng minh rate limit/lockout policy.`


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


## Approved session contract — 2026-11-17

Login success is HTTP 200 `DESIGN_RESOURCE_RETRIEVED`. JSON `data` contains public profile fields plus `access_token`, `token_type`, and `expires_in`; raw refresh token and refresh expiry are not in JSON. The opaque refresh token is set as an HttpOnly, SameSite=Lax, host-only cookie at `/api/v1/auth`; Secure follows explicit environment configuration and is enabled outside local development. Login/refresh/logout require an exact configured Origin.

R-X01 remains a source-only, bodyless POST using the cookie and rotating the stored refresh-token hash atomically. R-X02 is a source-only bodyless POST logout that revokes the active cookie session and clears the cookie. Neither route receives a numeric API ID in this implementation. API #03 DD remains Draft for unresolved error-contract, cleanup and live-schema questions. Runtime/deployment remain unverified.

## Source/contract status update — 2026-11-17

The previously recorded login/refresh transport discrepancy is superseded for this approved temporary implementation: API #03 is HTTP 200 with public profile fields plus access-token metadata, and the refresh token is cookie-only. R-X01 is a separate bodyless source-only refresh route; R-X02 is a separate bodyless source-only logout route. Both intentionally have no numeric API ID in this task. The remaining Draft questions concern the normative error set, token claim/lifetime governance, cleanup/retention, permissions, and live schema/deployment; this note does not claim runtime verification.
