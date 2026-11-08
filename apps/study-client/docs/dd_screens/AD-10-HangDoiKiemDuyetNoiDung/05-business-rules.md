# AD-10 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-10-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: List pending content theo type/course/page; có trạng thái trống.
- Gate/status (giữ nguyên): **R** local #78 route/module/query/model/validator/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** catalog/AC singular Content vs local Page; pagination/order/422 và type enum còn DERIVED; thiếu course title, author, submitted time, version; stale/deleted visibility, moderation permission, live schema/deployment chưa chốt; Study Web UNWIRED. **RUNTIME NOT VERIFIED**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
