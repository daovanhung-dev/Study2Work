# ME-14 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-14-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Soạn title/content/channels và preview recipients đã chọn ở ME-13.
- Current implementation status: ME-13 selected recipients flow through a one-use router-history handoff; ME-14 removes that payload from the history entry, validates the selected IDs, sends text and explicit `PUSH`/`EMAIL` values via #63, and routes a validated accepted UUID to SH-07. Accepted forms are locked; ambiguous network or malformed-success outcomes cannot be blindly resubmitted in the current page because #63 has no idempotency key. API #63 still has no `course_id`; exact course binding, attachment/draft persistence, worker/provider delivery and browser runtime remain unresolved or unverified. The broad DD stays Draft for those decisions.
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
