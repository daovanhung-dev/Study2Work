# AD-14 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-14-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Sửa Lesson, đổi status hoặc xóa theo policy; xử lý lỗi dependency ở server.
- Gate/status (giữ nguyên): **R** local #83–#86 route/module/query/model/test source; API DDs Draft. #84 full-replacement body `{title,content,video_url,order}` và #85 `{status}`/enum/audit là DERIVED; #86 rechecks `lesson_progress`, `resources`, `lesson_uploads` and returns 422 on any reference. **DD BLOCKED; IMPLEMENTATION BLOCKED:** #84 form/body mismatch (no `video_url`, course/type unmapped), #85 `ARCHIVED` vs local `SUSPENDED`, dependency set/output, `ADMIN` vs lesson-management permission, legacy/V1-PILOT/live schema, Study Web `UNWIRED`; **RUNTIME NOT VERIFIED**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
