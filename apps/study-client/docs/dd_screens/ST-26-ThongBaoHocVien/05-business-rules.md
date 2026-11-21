# ST-26 — Business Rules

## Current source rules — 2026-11-20

- Student Bearer identity is resolved by the backend; list/read queries are scoped to rows addressable by the authenticated principal.
- Read state comes from `is_read` and `read_at`; #44 is idempotent through recipient upsert, and #45 updates all currently unread addressable rows.
- No notification action URL is returned. The client leaves destination navigation unavailable and does not route from title/content.
- The #45 `{updated_count}` response differs from catalog `Page<Notification>`; source behavior is used by the client and the contract remains open.

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-26-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Lọc chưa đọc, mở deep link an toàn, mark-one/mark-all.
- Gate/status (giữ nguyên): **D**; **BLOCK:** Payload deep-link thông báo chưa định nghĩa
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
