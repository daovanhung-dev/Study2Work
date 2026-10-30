# VERIFICATION_REPORT — Study API #29

## Phạm vi

Tài liệu DD trong apps/study-server/docs/dd/29_quizzes_attempts/. Không chạy runtime tests vì API #29 chưa được tìm thấy trong Study router/modules/tests và scope chỉ tạo tài liệu.

## Nguồn đối chiếu

- docs/lists/list_api.md — API #29 row, ApiEnvelope/QuizAttempt schemas và business-code catalog.
- apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md — AC-16 actor, precondition và postcondition.
- apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio — API #29 create flow, IN_PROGRESS state, exhausted/expired branch.
- apps/study-server/docs/diagrams/DB_UNICA_TABLES.md and DB_UNICA_ERD.drawio — candidate quiz_attempts relationships and fields.
- infra/postgres/study-server/DB.sql — checked-in design DDL; foreign-key nullability discrepancy.
- apps/study-server/app/api/v1.py, app/modules/ and tests/ — current runtime wiring scan.
- .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/ — canonical Markdown template.
- .agents/server-study/workflows/README.md — Study DD packaging policy, no ZIP.
- apps/study-server/docs/dd/28_quizzes_detail/ — adjacent DD/open-question precedent.
- contracts/api-guidelines/README.md — response envelope/error conventions.

## Template fingerprint

| Template file | SHA-256 |
|---|---|
| 00_Cover.md | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md | d17dbef29c4159a1c30b6dc67df41bce8377fba40836eaab5fafd289aa81bc54 |
| 03_Request.md | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md | 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b |
| 06_Error.md | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

## Output fingerprint

| Output file | SHA-256 |
|---|---|
| 00_Cover.md | 00bb46795312320cfcb8d6d80476723132ae0b54622f2edc38816b67f4b44680 |
| 01_Lich_su.md | fc66d33761d907ec5bfba618f7c7daf7b1fcb726b23f0cf6ae2eb12e80a4ddf8 |
| 02_Overview.md | a532504630d483e74622fb17969705fea678c76f8ecfa287f1f906981c312e91 |
| 03_Request.md | 423e06196e63c758c20b677f04b1030d12281147690451117020588e50deb6d2 |
| 04_Response.md | f7c3de6c68d7c94af42f0f2ff5850763226b218f0bd2a49f7ce0b710ef75da49 |
| 05_Data_Mapping.md | 3642d587194805d8fd77b87da92078e4c149cde78ce20bb6af06c473d4310740 |
| 06_Error.md | b12ba79bd4e4847aa75663ab1e94c115711248ad52c33d9496572accb5eb13b4 |
| 07_table.md | d21bbfc34adbe7b27c3a0b56693e2fdd0bef981b3052e2c24fd5292d1382a889 |

## Kết quả kiểm tra

| Check | Result | Status |
|---|---|---|
| Template file set/order | Đủ 8 sheet 00–07; các sheet được tạo từ canonical template và giữ thứ tự. | VERIFIED |
| Front matter/API ID/status | Cả 8 sheet có dd_id 29 và status Draft — Needs Confirmation. | VERIFIED |
| Markdown tables | 28 table blocks có số cột nhất quán và separator hợp lệ. | VERIFIED |
| JSON examples | 2 JSON examples parse thành công. | VERIFIED |
| Relative links and anchors | 25 Markdown links và các anchor Q-29 được resolve. | VERIFIED |
| Contract path/response/error-code set | Khớp API #29 catalog: POST path, Student Bearer, quiz_id:int64!, ApiEnvelope<QuizAttempt>, 201/401/403/404/422/409/500. | VERIFIED |
| Candidate mutation and source statuses | quiz_attempts INSERT/IN_PROGRESS được ghi design-only; DDL nullability conflict và eligibility/response gaps được giữ lại. | VERIFIED |
| Whitespace/conflict markers | Inline scan trên file DD mới và worklog không phát hiện lỗi. | VERIFIED |
| Runtime tests | Không chạy; API #29 UNWIRED / NOT_FOUND và task documentation-only. | NOT_RUN |
| Context validator | Không chạy vì không có agent-context page/manifest nào thay đổi. | NOT_REQUIRED |

## Kết luận

DD hoàn tất ở trạng thái Draft — Needs Confirmation. Chỉ chuyển DD sang Final sau khi các câu hỏi trong OPEN_QUESTIONS.md được giải quyết và canonical contract được cập nhật nếu cần.

## Cross-AC review — AC-35 quiz tombstone

- Review result: DERIVED proposal added after document-level AC-35 review; owner confirmation is still required.
- Cross-reference: API #90 preserves history on soft-delete when attempts exist; API #91 reads retained history.
- No runtime, catalog, diagram or schema behavior was changed or verified.
