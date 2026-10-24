# VERIFICATION_REPORT — Study API #58

## Kết quả

- DD status: `Draft — Needs Confirmation`.
- Tài liệu: `VERIFIED_STATIC_ONLY` với open questions chặn mapping implementation.
- Runtime API #58: `UNWIRED / NOT_FOUND`; không khẳng định runtime behavior.
- Scope: Markdown DD và worklog; không sửa source, test, schema, catalog, diagram hoặc DB.

## Deliverable manifest

| Nhóm | Kết quả |
|---|---|
| Sheet template | Đủ 8 file: 00_Cover đến 07_table. |
| Reports | PLAN_RESULT.md, OPEN_QUESTIONS.md, VERIFICATION_REPORT.md. |
| Tổng | 11 Markdown files; không tạo ZIP theo Study workflow. |

## Kiểm tra đã chạy

| Check | Kết quả | Trạng thái |
|---|---|---|
| Skill/template registry | createDD-markdown được wire cho server-study; 8 template Markdown mở được và hash nằm trong PLAN_RESULT.md. | PASS |
| Template appendix | Appendix của cả 8 sheet output trùng byte-for-byte với template tương ứng. | PASS |
| Front matter | Cả 8 sheet có dd_id 58 và Draft — Needs Confirmation. | PASS |
| API contract | GET path, Mentor Bearer, query course_id/status, singular ApiEnvelope<SupportRequest>, HTTP 200 và 3 error codes giữ đúng catalog. | PASS |
| Error set | Chỉ 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 500 DESIGN_INTERNAL_ERROR trong 06_Error.md. | PASS |
| Response coverage | Mọi field SupportRequest, UserSummary, SupportMessage và UploadAsset có row trong response matrix. | PASS |
| JSON examples | Success/error code fences parse thành JSON hợp lệ. | PASS |
| Markdown | Table column count nhất quán; code fences cân bằng; không trailing whitespace. | PASS |
| Links and anchors | Các relative path và anchor đang có resolve được; report link hoàn chỉnh trong final check. | PASS |
| Source trace | Catalog/AC-24/DB candidates và missing API #58 source được ghi; không tạo SQL vật lý ngoài schema đã được chọn. | PASS |
| Runtime tests | Không chạy; docs-only và API #58 không có route để thực thi. | NOT_RUN |
| Agent context validator | Đã chạy nhưng trả `AGENT_CONTEXT_INVALID`: thiếu cây context/source DB Admin và báo `CONTEXT_STALE server-study` do source drift sẵn có. Không có báo lỗi worklog; API #58 không sửa source/context page. | FAILED — UNRELATED REPOSITORY DRIFT |
| AC-24 macro-review | Đã review cùng #59–#61: luồng/ranh giới mutation khớp; giữ cardinality conflict và shared schema/access/projection blockers mở. | VERIFIED_WITH_OPEN_QUESTIONS |

## Open implementation blockers

- List response cardinality và empty-result behavior.
- Physical support model và int64/UUID boundary.
- Course association/filter.
- Mentor identity/assignment scope.
- SupportStatus members và invalid-query error behavior.
- Inclusion/order/bounds của messages[] trong list response.
- Student/author projection, UploadAsset ID/status và signed URL resolver.

## Kết quả macro-review AC-24 #58–#61

`VERIFIED_WITH_OPEN_QUESTIONS`. #58 vẫn giữ nguyên response singleton theo catalog dù flow/path là danh sách; không tự đổi thành Page. Nhóm chưa implementation-ready do support schema và UUID/int64 mapping, course relation, Mentor identity/scope, nested response projection, lifecycle/attachment rules và error middleware wiring còn `SOURCE_REQUIRED`/chưa xác nhận. Xem [macro-review tổng hợp](../61_mentor_support_resolve/PLAN_RESULT.md#macro-review-ac-24-58-61).

Không đánh dấu implementation-ready hoặc group-review complete. Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) và [PLAN_RESULT.md](./PLAN_RESULT.md).
