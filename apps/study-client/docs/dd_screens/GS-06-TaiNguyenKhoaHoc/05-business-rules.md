# GS-06 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `GS-06-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Tài nguyên public theo khóa học; thể hiện quyền mở/tải theo metadata từ BE.
- Gate/status (giữ nguyên): **D (#11) / R (#12 source-backed locally; API DD Draft)**; **BLOCK:** #11 chưa có route/module/test và catalog trả `Resource` đơn, thiếu collection/empty/order/pagination contract; thiếu nguồn `visibility`; AC-06 public-or-authorized/403/private signed URL khác catalog và #12 hiện tại public/no-auth/direct URL, chỉ gate parent khi `lesson_id` có giá trị; không có 410/TTL/signer; legacy DDL có `resources` nhưng V1-PILOT không có bảng này; list/loaded/error UI và Study Web route UNWIRED; prototype lệch Study design target, WCAG chưa đo; live schema/deployment chưa xác minh
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
