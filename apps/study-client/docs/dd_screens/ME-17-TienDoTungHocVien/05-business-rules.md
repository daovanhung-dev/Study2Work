# ME-17 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-17-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Timeline và bài còn thiếu là expected design; current #67 chỉ trả snapshot trạng thái lesson theo curriculum order, không có event history hoặc assignment/quiz activity.
- Gate/status (giữ nguyên): **R**; #67 route/module/query/model/focused test source có local implementation. **DD BLOCKED; IMPLEMENTATION BLOCKED:** catalog/local response mismatch, AC-26 ordering, selected-row carrier, loaded timeline/metrics, owner/ACTIVE-roster/privacy and live-schema confirmation; Study Web UNWIRED; RUNTIME NOT VERIFIED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
