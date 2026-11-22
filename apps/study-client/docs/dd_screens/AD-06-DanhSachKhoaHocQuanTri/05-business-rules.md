# AD-06 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-06-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Danh sách course; search tên/mã/mentor và filter/status chỉ bật sau khi contract xác nhận; mở AD-07 bằng numeric `Course.id`.
- Gate/status: **R** source/API #73; API DD Draft; **DD BLOCKED; IMPLEMENTATION PARTIAL SOURCE:** Study Web route/page/#68 mentor source/#73 list/#104 create are present; product/API gates remain open for search, status/DELETED visibility, category, KPI, course code/lesson count, export/sync/policy and Admin permission mapping; **RUNTIME NOT VERIFIED**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).

## 4. User-approved create extension — source-backed rules (2026-11-22)

- API #104 is an explicit user-approved extension outside AC-32 and the original AC_UNICA set. It does not close other AD-06 gates or define a new review/publish policy.
- Required inputs are `title`, decimal-string `price`, and `mentor_id`; `description` and `thumbnail_url` are optional. The browser form uses a URL input for thumbnail; no upload occurs.
- Current server validation trims `title` and requires 1–200 characters; `mentor_id` must be a positive signed int64. Price follows `NUMERIC(12,2)` precision (up to 10 integer digits, at most 2 decimals); source does not enforce non-negative price, so do not add that policy in UI or DD.
- The selected mentor must currently have exact role `MENTOR` and status `ACTIVE`; the server rechecks this during create. API #68 supplies paged candidate choices, not the authorization decision.
- Server creates the record with `status='DRAFT'`, returns the Course projection with HTTP 201 `DESIGN_RESOURCE_CREATED`, and owns transaction commit/rollback.
- AD-06 proceeds only after validating the exact business code and response fields. It navigates to AD-07 only when the returned ID is positive and JavaScript-safe; otherwise it refreshes the list without coercion.
- Remaining unresolved rule: AC-32 course-management permission versus the current server `ADMIN` role mapping. Live database schema, deployment, and browser runtime are unverified.
