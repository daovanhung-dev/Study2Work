# PLAN_RESULT — API #91 Xem thống kê quiz

## Kết quả
- Output: `apps/study-server/docs/dd/91_admin_quizzes_statistics/`.
- API: `GET /api/v1/admin/quizzes/{quiz_id}/statistics`.
- DD status: `Draft — Needs Confirmation`.
- Scope: một DD và macro-review AC-35 #87–#91; không sửa runtime/schema/catalog/diagram.
- Package: 8 sheet + 3 report; Study giao Markdown, không ZIP.
- Runtime: `UNWIRED / NOT_FOUND`; không có route/view/test #91.

## Contract được giữ
Nguồn: catalog row #91.
- Admin Bearer; quiz-management permission theo AC-35.
- `quiz_id:int64!`; không body/query.
- Direct success: 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Quiz>`.
- Exact errors: 401/403/404/500 với `DESIGN_*` codes của catalog.

## Plan và kết quả
1. Đọc AC-35/AC-16 diagrams và liên kết attempt lifecycle — DONE.
2. Tách direct Quiz response khỏi statistics DTO proposal — DONE.
3. Dùng legacy quiz/attempt model làm candidate; Pilot UUID model được giữ riêng — DONE.
4. Định nghĩa metric từ attempts/submitted_at/score; không đọc answer rows hoặc filter incomplete status enum — DONE.
5. Macro-review tombstone cùng #87–#90/#29–#32; approval vẫn OPEN — DONE.
6. Tạo 8 sheets + 3 reports và chạy static checks — xem VERIFICATION_REPORT.md.

## Candidate reads
- `quizzes`: id, passing_score; status chỉ được nhắc trong tombstone discussion.
- `quiz_attempts`: id, quiz_id, submitted_at, score; không filter status.
- `quiz_answers`: không đọc.
- Live DB chưa xác minh.

## Assumptions and conflicts
Metric names/definitions và tombstone visibility là DERIVED. AC-35 intent conflicts với direct ApiEnvelope<Quiz>. Passing-score nullability, rounding, Admin policy và live schema còn cần xác nhận. Hard-delete/no-row dự kiến 404; soft-delete giữ history.
