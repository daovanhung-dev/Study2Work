# AD-16 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-16-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Builder create/update với dirty/draft-loss guard cần được chốt; AD-15 là entry, AD-17 là statistics handoff theo AC-35.
- Gate/status (giữ nguyên): **R** local #88/#89 route/module/query/model/validator/test source; API DDs remain Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** thiếu GET detail/question set, #89 body discrepancy, question/choice editor và course option mapping; field/range rules, AC-35 permission vs `ADMIN`, legacy/V1-PILOT/live schema, autosave/navigation và Study Web `UNWIRED`; **RUNTIME NOT VERIFIED**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
