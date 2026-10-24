# Kết quả plan — API #84 Cập nhật lesson

- Status: Draft — Needs Confirmation.
- Output folder: apps/study-server/docs/dd/84_admin_lesson_update/.
- Basis: Catalog #84 và AC-34 diagram; body/query schema không được khai báo.
- Direct contract: PUT /api/v1/admin/lessons/{lesson_id}, Bearer JWT/Admin, path lesson_id:int64!, response ApiEnvelope<Lesson>, HTTP 200 DESIGN_RESOURCE_UPDATED, đúng errors 401/403/404/422/500 theo catalog.
- Sources reviewed: root/project router, context map, worklog preflight #48–#50, server-study entry/index/workflow/routes/runtime/database/security/tests context, manifest, createDD-markdown skill, tám templates, catalog, AC-34 index/diagram, DD #82/#83/#75, API guidelines, current router/auth/middleware/response helper, API #09 query/model/view/test, legacy và V1-PILOT DDL.
- Archive scan: không thấy archive trong apps/study-server/docs hoặc resource folder của skill.
- Template fingerprints: xem VERIFICATION_REPORT.md.
- Tables read: legacy lessons candidate; V1-PILOT lessons được so sánh để giữ schema boundary.
- Tables write: candidate legacy lessons; live target chưa xác minh.
- Candidate mutation: name/content/video_url/sort_order từ body proposal; updated_at server timestamp chỉ DERIVED nếu không có trigger/owner khác. Không sửa course_id/status.
- Assumptions: body full-replacement candidate title/content/video_url/order; null cho content/video_url có thể clear. Cần xác nhận.
- Conflicts: path-only input vs PUT update intent; legacy BIGINT vs V1-PILOT UUID/versioned; required course_id vs nullable legacy DDL; Admin guard/middleware gap; guideline error data null vs helper {}.
- Verification: static-only; không chạy application tests.
