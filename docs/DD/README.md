# Study2Work — Detail Design API (157 APIs)

Bộ bàn giao gồm một workbook cho mỗi API, chia theo 20 plan. Mỗi workbook giữ cấu trúc template và chứa Overview, History, Request, Response, Data Mapping, Error, hướng dẫn; API ghi dữ liệu có thêm một DB sheet cho từng logical table bị thay đổi.

## Trạng thái

- Tất cả tài liệu đang ở Draft vì bundle nguồn thiếu bốn tài liệu bắt buộc mà plan viện dẫn.
- API `SUY DẪN` được gắn `Draft — Needs Confirmation`.
- API `TRỰC TIẾP` vẫn là Draft cho đến khi reconcile kiến trúc/schema.

## Quy ước khóa trong bản draft

- JSON/query: camelCase.
- URL path placeholder: giữ nguyên catalog.
- Database: snake_case logical naming.
- Canonical envelope: success, businessCode, message, data, meta, traceId; lỗi dùng errors[].
- Mutations: idempotency, transaction, audit/outbox/rollback được mô tả khi áp dụng.

Xem `MASTER_API_REGISTER.csv`, `TRACEABILITY_MATRIX.csv`, `QUALITY_REVIEW_REPORT.md` và `OPEN_QUESTIONS.md` trước khi review từng plan.
