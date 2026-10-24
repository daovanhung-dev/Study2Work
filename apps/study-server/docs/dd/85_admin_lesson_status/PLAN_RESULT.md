# Kết quả plan — API #85 Đổi trạng thái lesson

- Status: Draft — Needs Confirmation.
- Output folder: apps/study-server/docs/dd/85_admin_lesson_status/.
- Basis: Catalog #85 và AC-34; request body, LessonStatus members và transition policy không được khai báo.
- Direct contract: PATCH /api/v1/admin/lessons/{lesson_id}/status, Bearer JWT/Admin, path lesson_id:int64!, ApiEnvelope<Lesson>, HTTP 200 DESIGN_RESOURCE_UPDATED, exact errors 401/403/404/422/500 theo catalog.
- Direct AC-34 intent: Admin lesson-management permission; update status + audit; reload danh sách.
- Sources reviewed: root/project router, context map, worklog preflight #48–#50, server-study entry/index/workflow/routes/runtime/database/security/tests context, catalog/reusable Lesson, AC-34 index/diagram, DD #82–#84, status precedents #71/#76, current router/auth/middleware/response helper, API guidelines, legacy và V1-PILOT DDL.
- Archive scan: không có archive cần xử lý cho Markdown-only Study deliverable; không tạo ZIP theo scope workflow.
- Tables read: legacy BIGINT lessons candidate; V1-PILOT lessons/audit_events được so sánh riêng.
- Tables write: candidate status update; logical audit event. Physical audit relation chưa được xác định.
- Candidate request: body {status: LessonStatus}; DERIVED tối thiểu để nêu target cho PATCH. Không định nghĩa enum member/transition.
- Candidate mutation: đổi legacy lessons.status; updated_at timestamp chỉ DERIVED nếu schema này được chọn và không có owner/trigger khác. Atomic status+audit transaction là DERIVED proposal; không có INSERT SQL do physical mapping SOURCE_REQUIRED.
- Assumptions: validate status theo enum được owner duyệt; không áp transition/readiness/enrollment rules chưa có nguồn.
- Conflicts: catalog/diagram path-only; legacy BIGINT lesson có status nhưng không có audit; V1-PILOT UUID Lesson không có status và audit_events.resource_id UUID; Admin guard/live schema chưa xác minh; guideline error data null khác helper {}.
- Verification: static Markdown checks only; không chạy application tests.
