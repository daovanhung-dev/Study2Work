# AD-12 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-12-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: List lesson; mở AD-13 bằng numeric `Lesson.id`; course filter sends raw signed-int64 text in exact query `course`; refresh repeats the applied read and reset clears it. Search/type/status/paging/Add remain unavailable until their mappings/contracts are source-backed.
- Gate/status (giữ nguyên): **R** Angular route/page/GET #82 caller and API route/module/query/model/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION PARTIAL SOURCE:** course filter and manual refresh wired; cardinality, remaining filters, pagination, Add API, lesson-management permission, legacy nullability/live schema còn mở; **RUNTIME NOT VERIFIED**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
