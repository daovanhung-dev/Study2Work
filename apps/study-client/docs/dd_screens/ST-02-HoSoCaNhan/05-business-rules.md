# ST-02 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-02-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Xem thông tin profile không lộ trường bảo mật; avatar/email/role/status.
- Gate/status (giữ nguyên): **R**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Quyết định còn mở / blocker

| Gate | Evidence | Impact / owner decision |
|---|---|---|
| Profile-ready UI | PNG body absent; HTML shows login card; no authenticated field layout in either asset. | Product/Design: approve ready state, field labels, avatar fallback and error/loading layouts before implementation. |
| Claims contract | AC-02 says `user_id`/`role`, source #03/#04 uses `sub`/`roles`. | Auth/Product: standardize token claims. Current source mapping remains as-is. |
| Permissions | AC-02 says permissions; #04 catalog/model/query have none. | Auth/Product/BE: identify source or remove expectation; no client permissions inference. |
| Bio | Catalog optional, AC-11 includes bio, API #04/#14 current source omit/ignore. | Product/BE/DB: decide persistence and response contract before display/update. |
| Role/status freshness | #04 checks JWT role only; response row role/status not authorization source; no active-status predicate; DDL permits nullable status. | Auth/BE/DB: decide revocation/account-lock/current-role policy and deployed status constraint. |
| Cache/duplicate GET | Inventory says cache profile; #03 login already returns base profile and F01 calls #04 again. | Product/FE/Auth: choose fetch/caching/invalidation/session boundary; no TTL inferred. |
| Login/route/history | All `href="#"`; Study Web app/router/session absent. | FE/Product: wire safe route and return path when app exists. |
| Error UI | Current #04 has 401/403/500; only static sign-in card exists. | Product/FE: approve 401/403/500/network recovery and SH-05 relationship. |

### Final classification

- `DD BLOCKED`: no authenticated/ready design and unresolved data/claims/permissions/status/cache decisions prevent a field-complete implementation spec.
- `IMPLEMENTATION BLOCKED`: Study Web is `UNWIRED`; loaded state, auth/session/navigation and profile contract decisions are not available.
- `RUNTIME NOT VERIFIED`: static HTML render and backend source do not prove screen/API end-to-end or deployed DB state. Tests were read, not run.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
