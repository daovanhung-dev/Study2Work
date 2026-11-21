# ME-12 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-12-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Thread message/attachment, reply composer, resolve sau khi đủ điều kiện.
- Gate/status (giữ nguyên): **R**; #59–#61 local route/module/query/model/test source-backed, migration 008 local; API DD Draft/DERIVED, live schema chưa verified. **BLOCK:** loaded thread/full-thread scale và attachment UI chưa có thiết kế; counter 2000 khác #60 không max; #61 không enforce tối thiểu một message, AC satisfaction/confirmation chưa chốt; #60 vẫn nhận reply sau RESOLVED/CANCELLED; POST retry không idempotent, GET refresh policy cần thống nhất; Socket/TLS, SLA, auto-settlement/survey là prototype claim; Student producer chưa có; Study Web UNWIRED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
