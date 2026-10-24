# Plan Result — API #89 Cập nhật quiz

## Kết quả

- Output: apps/study-server/docs/dd/89_admin_quizzes_update/
- API: PUT /api/v1/admin/quizzes/{quiz_id}
- DD status: Draft — Needs Confirmation.
- Scope: Một API DD; không sửa runtime, schema, catalog, diagram hoặc context pages.
- Package: 12 Markdown sheets (7 shared sheets + 5 mapping sheets) và 3 reports; không tạo ZIP.

## Contract được giữ

Nguồn: docs/lists/list_api.md, API #89.

- Actor/authentication: Admin, Bearer JWT; AC-35 yêu cầu quiz-management permission.
- Direct input: quiz_id:int64! trong path; catalog không khai báo body/query.
- Direct success: HTTP 200, DESIGN_RESOURCE_UPDATED, ApiEnvelope<Quiz>.
- Errors: 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 422 DESIGN_VALIDATION_ERROR; 500 DESIGN_INTERNAL_ERROR.

## Plan trước khi authoring

1. Đọc AC-35: nhánh UPDATE gọi #89; backend ghi “UPDATE quiz/question set”; #88/#90/#91 là nhánh riêng.
2. Giữ catalog path-only; không coi body proposal là direct contract.
3. Đề xuất body config:string + questions:string bằng cách reuse API #88; nested JSON cũng là DERIVED.
4. Map candidate parent UPDATE sang legacy quizzes; không đổi status/description hoặc field ngoài Quiz schema.
5. Vì child IDs không có trong body candidate, đề xuất full child replacement; history guard ngăn xóa IDs được attempts/answers tham chiếu.
6. Tách mapping file cho quizzes UPDATE, choices DELETE, questions DELETE, questions INSERT, choices INSERT.
7. Giữ QuestionType/QuizChoice, order, live DB, body, attempt policy, course move và Admin permission là open questions.
8. Macro-review AC-35 chờ DD #91.
9. Static-check manifest, template tails, contract/errors, JSON, response fields, mappings, links/anchors, tables/fences, whitespace, fingerprint và source absence.

## Sources

- Catalog API #89, reusable Quiz/QuizQuestion, API Guidelines.
- AC-35 index và page trong AC_04_ADMIN_MANAGEMENT.drawio.
- DB_UNICA_TABLES.md, DB_UNICA_ERD.drawio, legacy DB.sql và V1-PILOT 02_study_db.sql.
- API #87/#88, API #28 Quiz detail, API #84 Admin PUT precedent.
- Current Study router, middleware, auth helper, response helper và tests status.
- Registered createDD-markdown skill/template pack; Study workflow Markdown-only.

## Candidate reads/writes

- Reads: quizzes target; quiz_attempts/quiz_answers history checks.
- Writes: quizzes UPDATE; old choices/questions DELETE; replacement questions/choices INSERT.
- Physical names là legacy candidates; live DB/FK/cascade chưa xác minh.

## Assumptions and conflicts

- Catalog path-only so với AC-35 update set; config/questions body là proposal DERIVED từ #88.
- Child replacement là DERIVED vì candidate body không có child IDs; history guard chưa approved.
- Legacy quiz_questions thiếu QuestionType; quiz_choices thiếu order; Quiz response chưa map đủ.
- Admin policy, schema selection, middleware và error data serialization chưa được xác nhận.

## Verification

Xem static checks và fingerprint trong [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).

## Handoff

Tiếp theo API #90 trong phiên DD sau; macro-review AC-35 chờ #91.
