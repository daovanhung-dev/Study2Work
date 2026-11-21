# AD-19 — Business Rules

> Current source verification (2026-11-16): AD-19 route/page/caller and API #92 tests are source-wired (FE 6/6; API fake-session 20/20). The allowed local behavior remains partial; this does not close contract, permission, schema, browser, or live DB gates.

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-19-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Admin xem notification list; inventory mockup search/status/channel và draft/scheduled/sent là expected nhưng cần contract mapping.
- Gate/status: API #92 DD Draft; **DD BLOCKED; IMPLEMENTATION PARTIAL SOURCE**. Current Angular route/page/caller and focused specs are wired; tests pass FE 6/6 and API fake-session 20/20. Keep singleton/Page, enum/search/metric/recipient/send-time, AC-36 permission vs ADMIN, notification grain/live schema and runtime gates open.
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
