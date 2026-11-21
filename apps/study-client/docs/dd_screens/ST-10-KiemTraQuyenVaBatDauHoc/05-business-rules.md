# ST-10 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-10-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Không phát video hay lộ nội dung khi chưa có entitlement được xác minh phía server.
- Gate/status: **DD BLOCKED; IMPLEMENTATION PARTIAL / SOURCE_WIRED; RUNTIME NOT VERIFIED.** Student #22–#24 routes/handlers and ST-10 caller source exist. Contract gaps remain for access/reason and publication predicates, #23 identity/idempotency/response, and #24 projection; public #09 exposes published `content`/`video_url` without enrollment check; BIGINT vs V1-PILOT UUID progress schema mismatch; ST-09 lessonId handoff absent; ST-11 owns #24; `423_LOCKED`/Session Token copy is static.
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
