# ME-15 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-15-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Hiển thị status theo một notification ID do caller xác định; API #64 source-backed trả Operation-shaped status local cho notification đó, không phải tổng hợp cả batch. #63 trả một Operation UUID và nhiều notification IDs int64; selector/route handoff chưa chốt. Inventory `queued/sending/complete/failed` không khớp #64 source `QUEUED/FAILED/SENT`.
- Gate/status (giữ nguyên): **M**; #64 có local route/module/query/model/test, #18 D/UNWIRED. **DD READY; IMPLEMENTATION BLOCKED:** batch ID selection, status mapping/lifecycle, per-channel/recipient report and realtime contract, destination links, Study Web route/auth/client; live schema/provider/runtime chưa verified
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
