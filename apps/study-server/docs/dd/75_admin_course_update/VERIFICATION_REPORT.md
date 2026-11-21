# Báo cáo kiểm tra — API #75

Trạng thái: API được wire và kiểm tra local; DD vẫn `Draft — Needs Confirmation` vì request body, policy chi tiết và schema/live state chưa được owner xác nhận.

## Phạm vi nguồn

| Nguồn | Đã đọc | Ghi chú |
|---|---:|---|
| API catalog #75 và reusable Course/Page schemas | Có | Direct contract giữ nguyên; catalog không khai báo body. |
| AC-32 index/activity diagram | Có | #75 là metadata update giữa #74 detail và #76 status/#77 delete. |
| Legacy Study DDL / table guide | Có | BIGINT `courses`, `name VARCHAR(200)`, `price NUMERIC(12,2)` là checked-in candidate; không xác nhận live schema. |
| V1-PILOT Study DDL | Có | UUID/versioned course model không được dùng cho API int64 candidate. |
| API #70/#73/#74 và shared Course mapper/auth/middleware/response | Có | Strict request/auth/transaction precedent, Course projection và middleware route-template behavior. |
| Current router/module/tests | Có | API #75 route/module/test được thêm; PUT dùng cùng path template với GET #74. |
| DD template | Có, 8/8 sheets | Excel appendix suffix được giữ nguyên trong các sheet được chỉnh. |

## Kết quả kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Focused API #75 HTTP tests | 27 passed; một upstream Starlette/httpx deprecation warning. | PASS |
| Linked Course/Admin regression | #06/#08/#70/#73/#74/#75: 113 passed; cùng warning upstream. | PASS |
| Full Study suite | 872 passed; một upstream Starlette/httpx deprecation warning. | PASS |
| Ruff | `.venv/bin/ruff check app tests`: all checks passed. | PASS |
| Import/OpenAPI | 42 `/api/v1` path templates / 46 operations; `/admin/courses/{course_id}` có GET và PUT; PUT khai báo int64 path, strict JSON body và lỗi catalog. | PASS |
| DD static checks | 11 Markdown deliverables; 8 sheet files giữ Draft + appendix; relative links và fenced JSON parse. | PASS |
| `git diff --check` | Không có whitespace errors sau khi sửa newline cuối context pages. | PASS |
| Agent context validator | Deno `--skip-drift` chỉ báo thiếu DB Admin context/source roots và links ngoài scope; không báo thiếu API #75 path. | BASELINE_FAIL_OUT_OF_SCOPE |
| Live DB/schema/migration/deployment | Không truy cập hoặc áp dụng. | NOT_VERIFIED_HERE |

## Giới hạn bằng chứng

- Body full replacement, field validation, legacy BIGINT mapping, singleton Page, role-only Admin gate và transaction order là lựa chọn `DERIVED`; DD vẫn Draft.
- Tests dùng fake Session/rows; không chứng minh live table, constraints, grants, dedicated course-management permission, migration state hoặc deployment.
- Không sửa API catalog, AC-32 diagram, DDL hay migration.

## Kết quả macro-review AC-32 #73–#77

- #75 chỉ cập nhật metadata theo proposal; không cập nhật CourseStatus hoặc ghi audit. #76 giữ riêng status update và audit intent. #77 giữ soft-delete, không hard-delete/cascade hoặc tự thêm audit.
- Catalog response shapes được giữ: #73–#76 là `Page<Course>`, #77 là `DeleteResult`; body #75/#76 vẫn là derived vì catalog không khai báo.
- #73/#74 visibility sau soft-delete và #75/#76 behavior trên deleted target phụ thuộc marker/policy chưa có nguồn. #73 hiện có category 422 fallback và shared `ADMIN` guard cục bộ; #75 body/validation policy, dedicated permission, counters, schema/status casing và soft-delete visibility còn mở. API #75 route hiện đã wired qua template chung với #74.
- Review tĩnh tài liệu; không chạy application tests và không sửa runtime/schema/catalog/diagram.
