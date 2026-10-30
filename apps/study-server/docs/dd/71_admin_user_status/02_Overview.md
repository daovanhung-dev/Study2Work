---
title: "Overview"
order: 2
dd_id: "71"
api_name: "Khóa/mở khóa user Conditional"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #71 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-31 |
| Method | PATCH |
| Endpoint | /api/v1/admin/users/{user_id}/status |
| Purpose | Khóa hoặc mở khóa account bằng status. |
| Consumer/Actor | Admin theo precondition AC-31. |
| Authentication | Bearer JWT |
| Authorization | Shared `ADMIN` JWT role theo pattern #68–#70; quyền user-management riêng chưa có source. |
| Direct request | `path{user_id:int64!}`; catalog/diagram không đặc tả body. |
| Implemented candidate body | Required strict JSON `{status: "ACTIVE" | "SUSPENDED"}`; `DERIVED`, extra fields bị từ chối. |
| Direct response | `ApiEnvelope<UserProfile>`; 200 `DESIGN_RESOURCE_UPDATED`. |
| Direct errors | 401/403/404/422/500 với đúng mã `DESIGN_*`. |
| Basis | Method/path/auth/path type/response/status/errors DIRECT; body/status transition/session effects DERIVED. |
| Status | Draft — Needs Confirmation |
| Runtime state | SOURCE_BACKED_WITH_DERIVED_CONTRACT; route/module/focused HTTP tests đã wired. |
| Transaction | `SELECT ... FOR UPDATE`, user status update và conditional refresh-token revoke nằm trong một transaction. |
| Side effects | Target SUSPENDED revoke refresh rows chưa revoke/chưa hết hạn; target ACTIVE không restore token. Access JWT hiện hữu không bị vô hiệu ngay. |

## Sources

- [Catalog và reusable schemas](../../../../../docs/lists/list_api.md) — API #71, ApiEnvelope, UserProfile, UserStatus.
- [AC-31 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — STATUS branch, conditional revoke, reload list/detail.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate `users.status`, `refresh_tokens.revoked_at/expires_at`.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID enum khác legacy users; không dùng làm target.
- [API #3 query/view](../../../app/modules/guest/api_03_auth_login/query.py) — refresh eligibility and single-token rotation.
- [Current auth helper](../../../app/utils/auth.py) — access guard parses JWT claims/roles without DB status checks.
- [API #4 UserProfile](../../../app/modules/guest/api_04_users_me/models.py) — safe response fields.
- [API #68/#69/#70 DDs](../68_admin_users_list/02_Overview.md) — adjacent AC-31 list/detail/profile boundaries.

## Tables read/written

| Relation | Fields | Operation and status |
|---|---|---|
| Legacy `users` | `id`, `status`, profile fields, timestamps | Read/lock current status; update `status`, `updated_at`; return safe UserProfile. Candidate local source only. |
| Legacy `refresh_tokens` | `user_id`, `revoked_at`, `expires_at` | When target is SUSPENDED, set `revoked_at` on active rows in same transaction. Derived side effect; live schema unverified. |
| V1-PILOT `identity_projections` | UUID subject, `account_status`, `identity_version` | Not queried or updated; schema differs from legacy BIGINT users. |

## Quyết định implementation — DERIVED

- Body requires one field `status`; only `ACTIVE` and `SUSPENDED` are accepted for lock/unlock. This is not an approved complete `UserStatus` enum.
- Only a current `ACTIVE` or `SUSPENDED` row can transition through this endpoint. Other current states return catalog 422 to avoid activating verification/deletion lifecycle states.
- Same target state returns 200 and writes `updated_at`; a SUSPENDED request reapplies the active-refresh revoke. Activation never restores revoked rows.
- Revoke currently valid refresh credentials when suspending. API #3 also checks ACTIVE on login/refresh; current stateless access-JWT checks do not query account status, so an existing access JWT can remain usable until expiry.
- No audit, tenant/MFA, self-lock or last-Admin rule is added. API #70 and #72 mutations remain separate.

## Giới hạn

The legacy BIGINT schema and migration state are not live-verified. The Admin claim is the local adjacent-API pattern, not proof of a dedicated permission policy. DD remains Draft.

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
