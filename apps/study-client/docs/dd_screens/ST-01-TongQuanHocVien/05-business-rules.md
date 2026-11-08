# ST-01 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-01-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Tổng quan khóa đang học, tiến độ, thành tích và thông báo; widget độc lập.
- Gate/status (giữ nguyên): **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #20/#21 Draft response UserProfile không biểu diễn Course/progress theo AC-13; nhánh EMPTY/HAS DATA cùng tới node render; #21 query/formula/merge, #38 award/projection/filter/page và #43 recipient/fields/order còn mở; API routes/modules/tests NOT_FOUND; AC-18 order lệch inventory widget độc lập; HTML endpoint paths sai, anchors chỉ là `#`; Study Web UNWIRED và visual target lệch design guide
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
