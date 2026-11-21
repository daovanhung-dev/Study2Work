# Plan Result — API #89 Cập nhật quiz

## Kết quả

- Output: apps/study-server/docs/dd/89_admin_quizzes_update/
- API: PUT /api/v1/admin/quizzes/{quiz_id}
- DD status: Draft — Needs Confirmation.
- Scope completed: API #89 runtime, focused tests, DD và server-study context; không sửa schema, catalog hoặc diagram.
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
7. Giữ QuestionType/QuizChoice catalog contract, live DB, body approval, attempt policy, course move policy và fine-grained permission là open questions; code dùng các fallback DERIVED được ghi nhận trong DD.
8. Macro-review AC-35 #87–#91 sau khi DD #91 có mặt; ghi kết quả document-level và giữ các proposal là DERIVED.
9. Kiểm tra focused/full tests, Ruff, OpenAPI, DDL unchanged, template tails, JSON, links/anchors, whitespace và context registry.

## Sources

- Catalog API #89, reusable Quiz/QuizQuestion, API Guidelines.
- AC-35 index và page trong AC_04_ADMIN_MANAGEMENT.drawio.
- DB_UNICA_TABLES.md, DB_UNICA_ERD.drawio, legacy DB.sql và V1-PILOT 02_study_db.sql.
- API #87/#88, API #28 Quiz detail, API #84 Admin PUT precedent.
- Current Study router, middleware, auth helper, response helper và tests status.
- Registered createDD-markdown skill/template pack; Study workflow Markdown-only.

## Local implementation reads/writes

- Reads: khóa quizzes target, current questions/choices và course target; check quiz_attempts/quiz_answers.
- Writes: quizzes UPDATE; old choices/questions DELETE; replacement questions/choices INSERT trong một transaction.
- Physical names là legacy candidates; live DB/FK/cascade chưa xác minh.

## Assumptions and conflicts

- Catalog path-only so với AC-35 update set; config/questions body là implementation proposal DERIVED từ #88.
- Child replacement và history guard là DERIVED; guard trả 422 trước write.
- Legacy quiz_questions thiếu QuestionType; quiz_choices thiếu order; Quiz response chưa map đủ.
- Fine-grained Admin policy, live schema/deployment và PostgreSQL locking chưa được xác minh; middleware/error envelope hiện theo source dùng chung.

## Verification

Xem test/static checks và fingerprint trong [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).

## Handoff

API #89 đã được triển khai và kiểm tra cục bộ; API #90 là task kế tiếp. Macro-review #87–#91 đã được ghi nhận ở mức tài liệu, các proposal vẫn chờ owner.
