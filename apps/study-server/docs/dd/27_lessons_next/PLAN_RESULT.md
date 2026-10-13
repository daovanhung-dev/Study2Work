# PLAN_RESULT — Study API #27

## Kết quả

- Output: apps/study-server/docs/dd/27_lessons_next/
- API: GET /api/v1/lessons/{lesson_id}/next
- DD status: **Draft — Needs Confirmation**
- Scope: Tạo tài liệu DD; không đổi runtime, API catalog, diagrams hoặc DB schema.
- Package: Không tạo ZIP theo workflow của Study Server.

## Đã tạo

| Artifact | Nội dung |
|---|---|
| 00_Cover.md | Thông tin DD, nguồn và trạng thái design-only. |
| 01_Lich_su.md | Lịch sử và trạng thái cập nhật. |
| 02_Overview.md | Contract, nguồn, phạm vi đọc candidate và discrepancy. |
| 03_Request.md | Header Student Bearer JWT và path lesson_id:int64!. |
| 04_Response.md | ApiEnvelope<Lesson> và ví dụ contract. |
| 05_Data_Mapping.md | Candidate read flow, request/query/response mapping và gaps. |
| 06_Error.md | HTTP/business-code mapping theo catalog và các điều kiện chưa chốt. |
| 07_table.md | Candidate lessons projection; mutation được ghi N/A vì GET. |
| OPEN_QUESTIONS.md | Câu hỏi cần xác nhận về entitlement/publish, ordering/tie-break, not-found, payload/schema và path. |
| VERIFICATION_REPORT.md | Kết quả rà soát cấu trúc, contract, links, JSON và diff. |

Worklog: .agents/worklog/2026-10-12/create-study-api27-dd.md.

## Contract được giữ

Nguồn: docs/lists/list_api.md, mục API #27.

- Actor/authentication: Student, Bearer JWT.
- Path: lesson_id:int64!.
- Success: HTTP 200, DESIGN_RESOURCE_RETRIEVED, ApiEnvelope<Lesson>.
- Errors: HTTP 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 500 DESIGN_INTERNAL_ERROR.

## Evidence và giới hạn thiết kế

- AC-15 xác nhận mục tiêu hiển thị điều hướng bài kế tiếp và activity diagram ghi bước đọc thứ tự curriculum; diagram không chốt predicate, tie-break hoặc hành vi bài cuối.
- DB diagrams và checked-in DDL là evidence thiết kế cho cột lessons; chúng không xác nhận live schema hoặc API #27 query.
- API #9 curriculum DD được trích làm precedent lân cận, không nâng thành rule API #27.
- Source scan không tìm thấy route/module/test API #27 trong Study Server. Runtime hiện tại được ghi UNWIRED / NOT_FOUND.
- Không tự chọn SQL, quyền publish/enrollment, trạng thái được phép, cách xử lý trùng sort_order hoặc ý nghĩa cụ thể của 404. Xem OPEN_QUESTIONS.md.
