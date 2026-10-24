# Plan Result — API #88 Tạo quiz mới

## Kết quả

- Output: apps/study-server/docs/dd/88_admin_quizzes_create/
- API: POST /api/v1/admin/quizzes
- DD status: Draft — Needs Confirmation.
- Scope: Một API DD; không sửa runtime, schema, catalog, diagram hoặc context pages.
- Package: 10 Markdown sheets (7 shared sheets + 3 table INSERT mappings) và 3 reports; không tạo ZIP.

## Contract được giữ

Nguồn: docs/lists/list_api.md, API #88.

- Actor/authentication: Admin, Bearer JWT; AC-35 yêu cầu quiz-management permission.
- Direct body: config:string!, questions:string!.
- Direct success: HTTP 201, DESIGN_RESOURCE_CREATED, ApiEnvelope<Quiz>.
- Errors: 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 422 DESIGN_VALIDATION_ERROR; 500 DESIGN_INTERNAL_ERROR.

## Plan trước khi authoring

1. Đọc AC-35 index và diagram: #88 là nhánh CREATE sau #87; node ghi “INSERT Quiz + Questions”, rồi hiển thị kết quả.
2. Giữ nguyên outer body là hai string bắt buộc; không đổi thành object/array ở contract.
3. Đề xuất embedded JSON tối thiểu từ Quiz/QuizQuestion: config có course_id/title/duration_minutes?/passing_score; questions là array text/type/choices. Đánh dấu DERIVED.
4. Đối chiếu legacy BIGINT quiz/question/choice tables, ERD quan hệ 1:N và Pilot UUID schema; không trộn chúng.
5. Dựng ma trận Q0 course existence và M1/M2/M3 atomic inserts; ghi type storage gap, output QuizChoice gap, choice order và status lifecycle.
6. Tạo ba file mapping insert riêng cho quizzes, quiz_questions, quiz_choices; reuse template table appendix byte-for-byte.
7. Giữ API #87–#91 relationship và discrepancy #87 response/#89 body trong open questions; macro-review chờ #91.
8. Static-check exact 13-file package, 10 template appendix tails, direct contract/errors, outer+nested JSON, tables, fences, links, anchors, whitespace và fingerprint.

## Sources

- API catalog row #88 và reusable Quiz/QuizQuestion.
- AC-35 index và AC_04_ADMIN_MANAGEMENT.drawio nodes/edges.
- DB_UNICA_TABLES.md, DB_UNICA_ERD.drawio, legacy DB.sql và V1-PILOT 02_study_db.sql.
- API #28 Quiz detail DD và API #87 Admin quiz list DD.
- Current app/api/v1.py, middleware.py, auth.py, responses.py và API Guidelines.
- Registered createDD-markdown skill/template pack; Study workflow Markdown-only, không tạo ZIP.

## Candidate writes

- quizzes: parent configuration.
- quiz_questions: question text and order.
- quiz_choices: option text and answer-key candidate.
- Courses: existence read only.
- Persistence mappings are legacy candidates; live DB chưa xác minh.

## Assumptions and conflicts

- config/questions embedded JSON is a proposal, not part of direct catalog schema.
- Legacy quiz_questions has no QuestionType column; V1-PILOT QuestionType belongs to UUID assessment model.
- QuizChoice shape, choice order, answer validation and correct-answer exposure remain unresolved.
- Atomic three-table write and course-not-found 422 are DERIVED proposals.
- Legacy DRAFT default and timestamp requirements are candidate; quiz-open lifecycle unresolved.
- AC-35 macro-review #87–#91 remains pending until #91 DD exists.

## Verification

Static checks and package fingerprint are in [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).

## Handoff

API #88 is one DD session. Continue at API #89 next session; macro-review AC-35 after #91 exists.
