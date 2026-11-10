# ME-13 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-13-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Chọn course và học viên được phép nhận, không tự lấy toàn bộ users.
- Gate/status (giữ nguyên): **R**; #46/#62 route/module/query/model/test source-backed locally. **BLOCK:** prototype slugs không ánh xạ int64; #46 không có semester/assigned-course; course status eligibility; support_needed thiếu progress/attendance source; loaded roster/selection UI chưa có; #63 CSV recipient mapping vẫn Draft/DERIVED, không có course_id, content:int64 lệch text, privacy/email/WCAG claims chưa được xác nhận; live schema và Study Web UNWIRED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
