# PLAN_RESULT — API #91 Xem thống kê quiz

## Kết quả
- Output: `apps/study-server/docs/dd/91_admin_quizzes_statistics/`.
- API: `GET /api/v1/admin/quizzes/{quiz_id}/statistics`.
- DD status: `Draft — Needs Confirmation`.
- Scope: API #91 runtime, tests, DD và Study context; không sửa schema/catalog/diagram.
- Package: 8 sheet + 3 report; Study giao Markdown, không ZIP.
- Runtime: `SOURCE_BACKED` locally; route, module và HTTP tests #91 đã được thêm.

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
6. Wire `GET /api/v1/admin/quizzes/{quiz_id}/statistics`, shared ADMIN guard, positive int64 parser và một aggregate query read-only trên legacy BIGINT candidate — verified locally; live schema chưa xác minh.
7. Chạy HTTP tests, linked #87–#91 regression, full Study suite, Ruff, OpenAPI và DD/context checks — kết quả trong VERIFICATION_REPORT.md.

## Candidate reads
- `quizzes`: id, passing_score; status chỉ được nhắc trong tombstone discussion.
- `quiz_attempts`: id, quiz_id, submitted_at, score; không filter status.
- `quiz_answers`: không đọc.
- Query/test dùng candidate legacy DDL; live DB chưa xác minh.

## Assumptions and conflicts
Metric names/definitions, path parse fallback, tombstone visibility và DTO riêng là DERIVED. AC-35 intent conflicts với direct `ApiEnvelope<Quiz>` trong diagram/catalog. Passing-score nullability, rounding, Admin policy và live schema còn cần xác nhận. Hard-delete/no-row dự kiến 404; soft-delete giữ history. DD vẫn Draft.
