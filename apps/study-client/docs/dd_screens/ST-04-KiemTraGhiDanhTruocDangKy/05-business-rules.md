# ST-04 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-04-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Xem giá, quyền học hiện có, nhánh khóa miễn phí/trả phí; không tự xác nhận đã ghi danh.
- Gate/source status: **#08/#15/#19/#20 current source callers exist; #15 no longer falls back to another Student.** **DISCREPANCY:** canonical API #15 still says Public/no-Bearer; this screen sends Student Bearer. Free flow is #19→#20; paid flow remains pending ST-05/#16–#18.
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> Source-backed current behavior is documented in Events/API Integration. Canonical #15 auth discrepancy and paid branch remain open; no live database/browser evidence is claimed.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: canonical API #15 actor still conflicts with the current Student-specific caller; paid flow continues through ST-05/#16–#18.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
