# AD-20 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-20-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Chọn recipients/segment, channels, preview và xác nhận; accepted không có nghĩa đã delivered.
- Gate/status (giữ nguyên): **R** local #93 route/module/model/validator/query/view/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** response Notification vs Operation; #18 int64 vs UUID/no Study handler/store; local source requires explicit recipients but UI only supplies unresolved segments; app→PUSH/channel, audience predicate/eligibility/grain, permission vs ADMIN, draft/send/priority, legacy live schema and provider delivery unresolved; Study Web UNWIRED; **RUNTIME NOT VERIFIED**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
