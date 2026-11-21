# ME-11 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-11-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Inbox request thuộc course Mentor phụ trách; status/course filters và empty/ready/error states.
- Gate/status (giữ nguyên): **R**; **BLOCK:** #58 có route/view/query/model/test source và DDL/migration 008 local, nhưng projection/lifecycle là DERIVED, live schema chưa xác minh; loaded-row design, status grouping/counts, course slug→int64 mapping, full-thread không pagination, AC-24 precondition vs empty state, SLA/realtime/Meet claims và Study Web UNWIRED còn chặn
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
