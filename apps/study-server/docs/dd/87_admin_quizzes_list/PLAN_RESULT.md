# Plan Result — API #87 Lấy danh sách quiz

## Kết quả

- Output: apps/study-server/docs/dd/87_admin_quizzes_list/
- API: GET /api/v1/admin/quizzes
- DD status: Draft — Needs Confirmation.
- Scope completed: Wire một API #87 gồm route, module, tests, middleware contract path, Markdown DD và đúng các context pages liên quan. Không sửa database, catalog hoặc diagram.
- Package: Tám template sheets và ba report chuẩn của Study workflow; không tạo ZIP.

## Contract được giữ

Nguồn: docs/lists/list_api.md, API #87.

- Actor/authentication: Admin, Bearer JWT.
- Query: course?:int64, status?:string, page?:int32.
- Direct success: HTTP 200, DESIGN_RESOURCE_RETRIEVED, ApiEnvelope<Quiz>.
- Errors: 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 500 DESIGN_INTERNAL_ERROR.

## Plan trước khi authoring

1. Đọc AC-35 index/diagram: #87 list query là bước mở đầu trước nhánh #88–#91.
2. Giữ nguyên direct contract và exact error set; không tạo route/schema/error code.
3. Dựng Request Usage, Query, Mutation và Response Source matrices trước khi chốt các sheet.
4. Dùng quizzes/question/choice trong legacy DB.sql như candidate only; tách riêng V1-PILOT assessments/quiz_options UUID model.
5. Ghi list cardinality/page conflict và đề xuất Page<Quiz>, page=1, fixed size=20, id ASC rõ là DERIVED, chưa duyệt.
6. Ghi schema child gap và lựa chọn metadata-only list projection; API #88 later adds a DERIVED local QuestionType/QuizChoice candidate without changing #87 query behavior.
7. Tạo/đồng bộ đúng 11 file Markdown, giữ appendix template; macro-review nhóm AC-35 đã có ở mức document review và giữ open questions.

## Implemented local fallback

- Authenticates shared `ADMIN` before raw query parsing and DB access; AC-35 quiz-management permission remains unavailable.
- Uses legacy BIGINT `quizzes` candidate only: exact optional course/status filters, hides `DELETED`, count + page, page default 1, fixed size 20, `id ASC`.
- Returns `ApiEnvelope<Page<Quiz>>`; catalog still declares `ApiEnvelope<Quiz>`, so this remains a visible DERIVED discrepancy.
- Returns metadata-only quiz items with `questions: []`; child rows are not queried in the list flow. API #88 migration 013 now supplies local DERIVED type/order candidates, but #87 keeps its list projection and does not claim that a Quiz has no questions.
- Invalid/out-of-range course/page returns 422 `DESIGN_VALIDATION_ERROR`, outside the direct catalog error set.
- Focused tests: 20 passed; linked #07/#78/#82/#86/#87 regression: 93 passed; full Study suite: 1113 passed; Ruff passed; OpenAPI: 51 path templates / 58 operations.
- These tests use fake DB rows. Live schema, migrations and deployment remain unverified.

## Sources

- API catalog reusable schemas và row #87.
- AC-35 index và AC_04_ADMIN_MANAGEMENT.drawio.
- DB_UNICA_TABLES.md, DB_UNICA_ERD.drawio, legacy DB.sql và V1-PILOT 02_study_db.sql.
- API #28 Quiz detail DD và API #82 Admin list DD.
- Current app/api/v1.py, middleware.py, auth.py, responses.py, Study context pages và API guidelines.
- Registered createDD-markdown skill/templates; template pack SHA-256: 3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137.

## Tables

- Candidate read: legacy quizzes, quiz_questions, quiz_choices.
- Write tables: none.
- V1-PILOT tables are a distinct non-selected model; live DB not verified.

## Assumptions and conflicts

- course/status exact match, page default 1, fixed size 20 and id ASC are proposals, not approved behavior.
- Catalog ApiEnvelope<Quiz> conflicts with list/page semantics.
- Quiz questions are required by reusable Quiz, while AC-35 diagram only says Query quizzes; question/choice projection needs confirmation.
- Legacy course_id nullability and physical model differ from logical Quiz/current pilot schema.
- Admin guard, nested schema, malformed query errors and error data convention remain unresolved.

## Verification

Chi tiết static checks, fingerprints, links và source boundary ở [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).

## Handoff

API #87 package is one DD session. Continue with API #88 in the next session. Perform AC-35 macro-review after #91 exists.
