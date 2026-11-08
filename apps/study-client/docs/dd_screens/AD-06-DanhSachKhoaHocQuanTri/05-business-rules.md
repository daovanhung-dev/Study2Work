# AD-06 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-06-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Danh sách course; search tên/mã/mentor và filter/status chỉ bật sau khi contract xác nhận; mở AD-07 bằng numeric `Course.id`.
- Gate/status (giữ nguyên): **R** source/API #73; test report 2026-11-01 pass trên temporary schema; API DD Draft; **DD BLOCKED; IMPLEMENTATION BLOCKED:** search, status/DELETED visibility, category relation, mentor options, KPI, course code/lesson count, export/create/sync/policy, Admin permission mapping và Study Web UNWIRED còn mở; **RUNTIME NOT VERIFIED**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
