# PLAN_RESULT — Study API #28

## Kết quả

- Output: apps/study-server/docs/dd/28_quizzes_detail/
- API: GET /api/v1/quizzes/{quiz_id}
- DD status: **Draft — Needs Confirmation**
- Scope: Tạo tài liệu DD; không sửa runtime, API catalog, diagrams hoặc DB schema.
- Package: Không tạo ZIP theo workflow của Study Server.

## Đã tạo

| Artifact | Nội dung |
|---|---|
| 00_Cover.md | Định danh API, nguồn và design-only status. |
| 01_Lich_su.md | Lịch sử DD draft. |
| 02_Overview.md | Contract, nguồn, candidate tables, security boundary và discrepancies. |
| 03_Request.md | Student Bearer header và quiz_id:int64! path parameter. |
| 04_Response.md | ApiEnvelope<Quiz>, field mappings, business codes và JSON examples. |
| 05_Data_Mapping.md | Candidate Quiz/question/choice reads, mapping, errors và source gaps. |
| 06_Error.md | HTTP/business codes theo API catalog; không thêm 409. |
| 07_table.md | Candidate read projection; mutation ghi N/A. |
| OPEN_QUESTIONS.md | Câu hỏi về eligibility, attempt/expiry, schema, field projection, ordering và path errors. |
| VERIFICATION_REPORT.md | Kết quả structural/content/link/contract checks. |
| .agents/worklog/2026-10-12/create-study-api28-dd.md | Preflight, expected/current behavior, discrepancies và verification. |

## Contract được giữ

Nguồn: docs/lists/list_api.md, API #28.

- Actor/authentication: Student, Bearer JWT.
- Path: quiz_id:int64!.
- Success: HTTP 200, DESIGN_RESOURCE_RETRIEVED, ApiEnvelope<Quiz>.
- Errors: 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 500 DESIGN_INTERNAL_ERROR.

## Evidence và giới hạn thiết kế

- AC-16 ghi Student có quyền làm quiz và quiz đang mở; diagram đọc Quiz/rules/question set và có nhánh 403/409 khi hết lượt/hết hạn.
- Catalog API #28 không có 409. DD giữ contract catalog và ghi lệch với diagram trong OPEN_QUESTIONS.md.
- quizzes, quiz_questions và quiz_choices là candidate reads từ DB design/DDL; live schema/query chưa xác minh.
- Response không đưa quiz_choices.is_correct cho Student. API #88 migration 013 adds local type/order candidates, but QuizChoice fields and QuestionType values remain unapproved in catalog.
- Search current Study router/modules/tests không tìm thấy API #28; DD không tuyên bố runtime implementation.

## Assumption

Tiếp tục cách làm API #27: tạo draft, ghi câu hỏi mở và giữ nguyên các artifact #27 hiện có.
