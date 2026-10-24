# Báo cáo kiểm tra — API #75

Trạng thái: DD được xác minh tĩnh; API #75 chưa được wire.

## Phạm vi nguồn

| Nguồn | Đã đọc | Ghi chú |
|---|---:|---|
| API catalog #75 và reusable schemas | Có | Direct contract giữ nguyên; body không khai báo. |
| AC-32 index và toàn bộ node/edge diagram | Có | #73 → #74 → nhánh #75/#76/#77 → reload. |
| Legacy DB guide/ERD/DDL | Có | Mapping design-only; live schema không xác minh. |
| V1-PILOT DDL | Có | UUID/versioned course model không map ngầm sang API BIGINT. |
| Current router/auth/middleware/response | Có | Không có Admin route/guard; error allowlist và data shape discrepancy ghi lại. |
| DD tham khảo #70/#73/#74 và API #14 source | Có | Proposal body, Page mapping và transaction precedent. |
| Template | Có, 8/8 | Manifest fingerprint ghi sau khi kiểm tra. |

## Kết quả kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Exact deliverables | Đúng 11 file: 8 sheet + 3 report; không có ZIP. | PASS |
| Front matter/template appendix | 8/8 sheet có front matter; appendix khớp byte với template tương ứng. | PASS |
| Catalog request/response/error contract | Method/path/auth/path type/response/success và đúng 401/403/404/422/500 codes; không đưa body proposal thành direct contract. | PASS |
| Course/Page field coverage | Đủ Course, UserSummary, PageMeta fields; category không có nguồn nên được giữ `SOURCE_REQUIRED` và omit trong example. | PASS_WITH_OPEN_GAPS |
| JSON examples | Request và success response đều parse hợp lệ. | PASS |
| Tables/fences/links/anchors/whitespace | Table widths nhất quán; fences cân bằng; local links/anchors resolve; không trailing whitespace; final newline có đủ. | PASS |
| Output fingerprint | Template manifest và DD payload SHA-256 bên dưới. | RECORDED |
| Route/module/test absence | Static source scan completed | VERIFIED_STATIC_ONLY |
| Runtime tests | Not run; docs-only | NOT_RUN |
| AC-32 macro-review #73–#77 | Đã rà toàn nhóm; metadata/status/delete boundary nhất quán, các gaps chung được giữ mở. | COMPLETED_WITH_OPEN_QUESTIONS |
| Agent context validator | `node` không có trong PATH; Deno fallback chạy nhưng thất bại do context `db-admin` và source roots được registry tham chiếu đang thiếu, cùng snapshot commit `9a70eb...` không có trong Git object database. | FAIL_REPOSITORY_WIDE; không thuộc scope #75 |

## Fingerprint

- Template manifest SHA-256: `ef4e457d840129719d47303e4cd326ac4637e65f02f27b44ec91f9e925bb402f` (sorted filename + per-file SHA-256 manifest).
- DD payload SHA-256: `23f997be3b1df127bebcdf20843a725b67637b2503a7afd7425045cb04a8bfb6` (8 sheets + `PLAN_RESULT.md` + `OPEN_QUESTIONS.md`; excludes this report).

## Giới hạn bằng chứng

- DD dự kiến ở trạng thái `Draft — Needs Confirmation`; chưa xác nhận body proposal hoặc live schema.
- Không chạy app tests; source scan không chứng minh endpoint/runtime/database availability.
- Agent context validator chưa đạt do lỗi repo-wide ngoài phạm vi Study Server; xem kết quả trong bảng trên.
- Macro-review #73–#77 đã hoàn tất ở mức tài liệu; các gap chung cần owner/schema/runtime quyết định.
## Kết quả macro-review AC-32 #73–#77

- #75 chỉ cập nhật metadata theo proposal; không cập nhật CourseStatus hoặc ghi audit. #76 giữ riêng status update và audit intent. #77 giữ soft-delete, không hard-delete/cascade hoặc tự thêm audit.
- Catalog response shapes được giữ: #73–#76 là `Page<Course>`, #77 là `DeleteResult`; body #75/#76 vẫn là derived vì catalog không khai báo.
- #73/#74 visibility sau soft-delete và #75/#76 behavior trên deleted target phụ thuộc marker/policy chưa có nguồn. Category/counters, Admin guard, schema/status casing và middleware/error gaps còn mở.
- Review tĩnh tài liệu; không chạy application tests và không sửa runtime/schema/catalog/diagram.
