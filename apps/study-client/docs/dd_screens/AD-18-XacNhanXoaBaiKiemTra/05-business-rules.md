# AD-18 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-18-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Admin xem Quiz/tác động history rồi xác nhận; AD-15 là entry và đường quay lại dự kiến.
- Gate/status (giữ nguyên): **R** local #90 route/module/query/model/validator/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** AC-35 chỉ yêu cầu soft-delete khi có attempts, no-attempt branch không xác định; local hard-delete/no-history và soft-delete on linked answer are DERIVED; tombstone/timestamp/repeat, #29 race, permission, #87/#89/#91 visibility, target data/detail API, live schema and Study Web UNWIRED remain open; **RUNTIME NOT VERIFIED**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
