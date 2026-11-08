# AD-21 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-21-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Xem notification/status; sửa hoặc delete/cancel chỉ sau khi policy cho phép; SH-07 handoff có điều kiện.
- Gate/status (giữ nguyên): **R** local #94/#95/#96 routes/modules/query/validator/model/test source; API DDs Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** notification detail/projection, status/lifecycle mapping, AC-36 permission vs `ADMIN`, #94 body/edit gate, #95 cancel/delete/retention/worker coordination, delivery metrics/channel mapping, candidate legacy/live schema, #18 UUID/int64/owner/store, Study Web UNWIRED; **RUNTIME NOT VERIFIED**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
