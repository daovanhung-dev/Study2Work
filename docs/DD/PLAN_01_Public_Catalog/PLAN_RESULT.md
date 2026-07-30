# Kết quả Plan 01 — Public Catalog

- Phạm vi: API 001–006.
- Hoàn thành workbook: 6/6.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 001 | GET | `/api/v1/catalog/overview` | SUY DẪN | Draft — Needs Confirmation | `API_001_GET_catalog_overview.xlsx` | Không |
| 002 | GET | `/api/v1/catalog/learning-paths` | TRỰC TIẾP | Draft | `API_002_GET_catalog_learning_paths.xlsx` | Không |
| 003 | GET | `/api/v1/catalog/learning-paths/{slug}` | SUY DẪN | Draft — Needs Confirmation | `API_003_GET_catalog_learning_paths_by_slug.xlsx` | Không |
| 004 | GET | `/api/v1/catalog/courses` | SUY DẪN | Draft — Needs Confirmation | `API_004_GET_catalog_courses.xlsx` | Không |
| 005 | GET | `/api/v1/catalog/courses/{slug}` | TRỰC TIẾP | Draft | `API_005_GET_catalog_courses_by_slug.xlsx` | Không |
| 006 | GET | `/api/v1/catalog/sample-lessons/{lesson_id}` | TRỰC TIẾP | Draft | `API_006_GET_catalog_sample_lessons_by_lesson_id.xlsx` | Không |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
