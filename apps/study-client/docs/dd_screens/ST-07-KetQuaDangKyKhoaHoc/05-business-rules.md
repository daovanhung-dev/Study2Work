# ST-07 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-07-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Hiển thị kết quả chỉ sau backend xác nhận entitlement/enrollment; không suy ra success từ callback hay static copy.
- Gate/status (giữ nguyên): **#18/#19/#20 D; DD BLOCKED**; **BLOCK:** AC-12 không nêu ST-07 riêng/#18 detached; Operation ID/access/lifecycle và ST-06 handoff chưa rõ; #19 identity/eligibility/duplicate/transaction chưa chốt; #20 UserProfile không biểu diễn Course list; Study Web/API UNWIRED; post-#19 reload recovery và destination chưa rõ
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
