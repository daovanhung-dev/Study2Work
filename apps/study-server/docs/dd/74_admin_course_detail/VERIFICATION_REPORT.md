# Báo cáo kiểm tra — API #74

Trạng thái: kiểm tra tĩnh tài liệu; API #74 chưa được wire.

## Phạm vi nguồn

| Nguồn | Đã đọc | Ghi chú |
|---|---:|---|
| API catalog #74 và reusable schemas | Có | Contract giữ nguyên; `Page<Course>` là singleton proposal. |
| AC-32 index và toàn bộ node/edge của diagram | Có | #73 → #74 → #75/#76/#77 → reload; counters chưa có schema. |
| Legacy DB guide/ERD/DDL | Có, phần Course/User liên quan | Mapping `DESIGN_ONLY`; live schema không xác minh; mentor nullability có discrepancy. |
| V1-PILOT DDL | Có, phần courses/course_versions | UUID/versioned model không map ngầm sang BIGINT. |
| Current API #06/#08 source và API #08 tests | Có | Chỉ dùng mapping/error/Page precedents; không áp dụng public `PUBLISHED` filter. Không chạy tests. |
| DD tham khảo #69/#73 | Có | Admin guard boundary, Course projection và AC-32 continuity. |
| Template | Có, 8/8 file mở | Fingerprint/manifests bên dưới; appendix phải khớp byte với baseline. |

## Kết quả kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Exact deliverables | Đúng 11 file: 8 sheet + 3 report; không có ZIP. | PASS |
| Front matter/template appendix | 8/8 sheet có metadata; appendix cuối khớp byte với 8 template tương ứng. | PASS |
| Catalog request/response/error contract | GET/path/auth/response và đúng success 200 + error 401/403/404/500; không thêm business code. | PASS |
| Course/Page field coverage | Có toàn bộ field Course, UserSummary và PageMeta; `category` optional được ghi SOURCE_REQUIRED/omit, counters giữ open vì chưa có field contract. | PASS_WITH_OPEN_GAPS |
| JSON examples | 2/2 JSON example parse hợp lệ. | PASS |
| Tables/fences/links/anchors/whitespace | 32 bảng có số cột nhất quán; code fence đóng; 39 link nội bộ/anchor resolve; không trailing whitespace; có final newline. | PASS |
| Output fingerprint | Digest của 8 sheet + PLAN_RESULT + OPEN_QUESTIONS; loại VERIFICATION_REPORT để tránh self-reference. | RECORDED |
| Route/module/test absence | Đã xác nhận trước authoring | VERIFIED_STATIC_ONLY |
| Runtime tests | Không chạy — docs-only | NOT_RUN |
| AC-32 macro-review #73–#77 | Đã rà cả năm DD; counters, visibility, Admin guard, schema/status và error integration vẫn mở. | COMPLETED_WITH_OPEN_QUESTIONS |

## Fingerprint

- Template manifest SHA-256 (tên file sort + SHA-256 từng file): `ffc3df52dfdfa6ff69a9c71420300fdbd5b083352255f89685dd6214a91a591b`.
- DD payload SHA-256: `8b267a0f66c8d77a7f18c7e74a46768a2f021140a254a0fe1c155509e6460ea5`; gồm 8 sheet và 2 report `PLAN_RESULT.md`/`OPEN_QUESTIONS.md`, loại trừ file report này.

## Giới hạn bằng chứng

- Tài liệu là `Draft — Needs Confirmation`, không chứng minh API #74 runtime/DB/live schema.
- Không chạy application tests; source evidence được đọc tĩnh.
- AC-32 macro-review đã hoàn tất ở mức tài liệu sau khi DD #77 có mặt.
## Kết quả macro-review AC-32 #73–#77

- Ownership: #73 list/filter, #74 detail, #75 metadata-only, #76 status + audit intent, #77 policy soft-delete. #73–#76 giữ `Page<Course>` theo catalog; #77 giữ `DeleteResult`.
- Diagram nhắc owner và counters cho detail; Course/UserSummary có owner nhưng counter definitions/fields không có trong contract. Không tự thêm counter response/query.
- Visibility sau soft-delete, behavior của update/status trên deleted target, category relation, Admin guard, CourseStatus casing, schema generation và middleware/error convention còn quyết định.
- Static document review only; không xác minh live schema/runtime và không chạy application tests.
