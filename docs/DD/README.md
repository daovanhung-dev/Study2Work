# Study2Work Study — API Detailed Design

## Phạm vi

Bộ DD này được suy ra từ toàn bộ BD Study2Work Study trong `BD.zip`, áp dụng cho **Study V1**. Phạm vi không bao gồm hệ Work/Learn2Earn.

- Số API contract: **105**
- Base URL: `/api/v1`
- Chuẩn API: REST + JSON, camelCase ở request/response, UUID, ISO 8601 có timezone.
- Nội dung chi tiết từng API sử dụng đúng 7 phần của template: `README`, `01_Overview`, `02_History`, `03_Request`, `04_Response`, `05_DataMapping`, `06_Error`.

## Cách đọc

1. Đọc `API_CATALOG.md` để tìm endpoint.
2. Mở thư mục module/API tương ứng.
3. Đọc lần lượt các phần theo thứ tự số.
4. Khi code, contract response và rule tại `01_Overview` là nguồn quy ước; backend vẫn là nơi thực thi rule.

## Lưu ý thiết kế

- Một learner chỉ có một learning path ở trạng thái `ACTIVE`.
- Contact verification và onboarding hoàn chỉnh là điều kiện trước activate path và học nội dung giới hạn.
- Tiến độ, điểm, completion, unlock là server-authoritative.
- Zalo chỉ là external link; hệ thống không đồng bộ thành viên hay hội thoại.
- API admin rủi ro yêu cầu `reason`, kiểm tra RBAC và ghi audit log.
- `/internal/*` chỉ cho service-to-service; frontend không gọi trực tiếp.

Xem thêm: [API Catalog](API_CATALOG.md), [Coverage Matrix](API_COVERAGE_MATRIX.md), [Conventions](API_CONVENTIONS.md), [Traceability](SOURCE_TRACEABILITY.md), [Assumptions](DATA_MODEL_ASSUMPTIONS.md).
