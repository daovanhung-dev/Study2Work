# ST-18 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ST-18-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Soạn nội dung, file đính kèm, kiểm tra tiến độ upload/nộp một lần.
- Gate/status (giữ nguyên): **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #33/#35 Student route/module/test NOT_FOUND; #33 access/deadline/rule và GET ownership trùng ST-17/AC-17 chưa chốt; #34 local route/module/provider/test source-backed nhưng không có application size/MIME cap, course_id optional, URL public-base; API index #034 cập nhật R, live DB/storage chưa verify; #35 file-ref key/encoding/cardinality, text constraints, persistence/idempotency, data.id vs submission_id open; draft/URL/checklist/consent and error-retention rules lack contract; candidate legacy BIGINT uploads/assignments/submissions vs V1-PILOT without business tables; #36 is assigned to ST-19 by inventory but AC-17 places read before submitted state; loaded PNG/Guest fallback HTML/hash route and Study Web design target differ; Study Web UNWIRED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

> CẦN_XÁC_NHẬN: DD nguồn không có section rule/security/blocker riêng; không tự tạo rule mới.


## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
