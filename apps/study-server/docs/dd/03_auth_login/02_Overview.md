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
| Purpose | `Xác thực thông tin đăng nhập và trả hồ sơ cùng token session` |
| Consumer/Actor | `Guest` |
| Authentication | `Public; không yêu cầu Bearer token` |
| Authorization | `N/A — public login` |
| Basis | `DIRECT — list_api.md reconciled to current Study Server source on 2026-11-21; AC-02 and ERD V1 remain comparison sources` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `Expected: catalog chưa đặc tả persistence; current source insert refresh_tokens và commit sau khi phát hành token` |
| Side effects | `Expected: AC-02 yêu cầu token/session; current source phát hành access/refresh token và lưu refresh-token hash` |

## Sources

- [`docs/lists/list_api.md`](../../../../../docs/lists/list_api.md) — API #3 contract: input, `ApiEnvelope<LoginData>`, current-source success/error statuses.
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

- **User decision (2026-11-21):** use current Study Server API #03 behavior for SH-02 and reconcile the catalog success contract. Catalog now declares HTTP 200 `DESIGN_RESOURCE_RETRIEVED` with `LoginData`, including the source profile fields and five token fields. The source route and checked-in tests remain the behavior evidence; live deployment is not verified.
- Current source returns HTTP 401 for invalid credentials, 403 for a non-ACTIVE account, 422 for invalid request, and 500 for internal failure. Catalog records those current response branches.
- `LoginData` intentionally omits `UserProfile.bio`, which the current login query does not return. Avatar and phone may be null as projected by the current source.
- Route `/api/v1/auth/refresh` hiện được đánh dấu cùng API #03 trong router/module nhưng không có catalog row hoặc AC-02 step riêng; DD này giữ nó là source-only discrepancy, không gộp vào login contract.

## Assumptions

- Expected validation: catalog chỉ nêu required/type/email-format, không đặc tả min/max hay password policy.
- Current source chuẩn hóa email bằng trim/email validator với max 255 và từ chối password chỉ có whitespace; đây là current behavior, chưa được nâng thành policy normative.
- Current source gọi `app.core.security.verify_password` trên `users.password_hash`; DD không tự xác định thuật toán/cost ngoài code/config hiện hành.
- `meta = {}` vì API #3 không khai báo metadata hoặc operation_id.

## Conflicts

- `RESOLVED_FOR_SH-02 (2026-11-21): catalog/API #03 success contract now matches current source HTTP 200, DESIGN_RESOURCE_RETRIEVED and LoginData fields.`
- `RESOLVED_FOR_SH-02 (2026-11-21): catalog/API #03 error statuses record current source 401/403/422/500 behavior.`
- `SOURCE_BACKED: token fields are part of LoginData; refresh-token hash persistence remains a source behavior and does not prove live schema/deployment.`
- `DISCREPANCY: router cũng khai báo /auth/refresh nhưng catalog không có API ID/contract riêng.`
- `LoginData omits UserProfile.bio because the current login source does not return that field; the reusable UserProfile schema remains unchanged.`

## Security note

- `Không log hoặc trả plaintext password/password_hash; không trả raw DB/hash error detail.`
- `Không yêu cầu Bearer token cho login. LoginData returns access and refresh tokens; the client keeps credentials in tab memory under the current Study Web session managers.`

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

