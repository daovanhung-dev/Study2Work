# VERIFICATION_REPORT — Study API #30

## Phạm vi

DD-only cho PUT /api/v1/attempts/{attempt_id}/answers tại apps/study-server/docs/dd/30_attempts_answers/. Không chạy runtime tests vì API #30 chưa được wire và yêu cầu chỉ tạo tài liệu.

## Nguồn đối chiếu

- docs/lists/list_api.md — API #30 contract, ApiEnvelope, QuizAttempt, QuizAnswer và business codes.
- contracts/api-guidelines/README.md — envelope và error conventions.
- apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md và AC_02_STUDENT_LEARNING.drawio — actor và AC-16 UPSERT AttemptAnswer.
- apps/study-server/docs/diagrams/DB_UNICA_TABLES.md, DB_UNICA_ERD.drawio và infra/postgres/study-server/DB.sql — candidate answer persistence; đây là design evidence, không xác minh live schema.
- apps/study-server/app/utils/auth.py — helper xác thực Student hiện có; API #30 chưa được xác nhận sử dụng helper.
- apps/study-server/app/api/v1.py, apps/study-server/app/modules/ và tests/ — scan trạng thái wiring hiện tại.
- .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/ — canonical template Markdown.
- .agents/server-study/workflows/README.md — quy tắc không tạo ZIP cho Study DD.
- apps/study-server/docs/dd/27_lessons_next/, 28_quizzes_detail/, 29_quizzes_attempts/ và worklogs liên quan — draft precedent.

## Template fingerprint

| Template file | SHA-256 |
|---|---|
| 00_Cover.md | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md | 5fbf83eaf2f69705c3cc7ffe7dc43c4cbbb70c0649eda7c41ffd5cb1cb58a12e |
| 03_Request.md | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md | 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b |
| 06_Error.md | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

## Output fingerprint

| Output file | SHA-256 |
|---|---|
| 00_Cover.md | a3cc62d7a7fb2bccf1963a6ededc498a1ade5e38b40c31b1d329db69043b6537 |
| 01_Lich_su.md | 1b68986efdd251d554a4d0a50cd8d11e5bd0c2334c5697e25de46ef51431f85b |
| 02_Overview.md | 1777aa4499efc680520734a7c94343e05ad7ed8cb33f9ac3b1409f933eb100fb |
| 03_Request.md | 6ff73ec44a3bb4efbc7ca507b1f7d76852337ab5ac0bd02e7fc0edd0bd1728a6 |
| 04_Response.md | 465f337716ced25bc86752757ef62ca3ab30c8ab49ac132665d5b7c862266f1c |
| 05_Data_Mapping.md | 56c967682c5039e4416c18d8cf89cb3d2ddec555d20e6c6e55de8fee73ca2b88 |
| 06_Error.md | 10c7dc688fa00b8461d2043b6d7fd7fb77ab677c6c41e34db4624b8ef2a2f83a |
| 07_table.md | dc235f07b98be8666ff66fb3b8563a981a5dd3210c6f2cb867c5ca69fc77a240 |

## Kết quả kiểm tra

| Check | Result | Status |
|---|---|---|
| Template file set/order | Đủ 8 sheet 00–07; metadata, API ID và status đồng nhất; appendix của từng sheet khớp canonical template. | VERIFIED |
| Markdown tables | 392 hàng bảng có số cột nhất quán. Các field request/response được ghi riêng từng hàng. | VERIFIED |
| JSON examples | 3 request/response examples parse thành công. | VERIFIED |
| Relative links and anchors | 23 Markdown links cùng anchor nội bộ được resolve. | VERIFIED |
| Contract path/response/error codes | Giữ PUT /api/v1/attempts/{attempt_id}/answers, Student Bearer JWT, attempt_id:int64!, body question_id:int64! và answer(s):string!, ApiEnvelope<QuizAttempt>, success 200 và đúng 5 error codes catalog; không thêm 409. | VERIFIED |
| Candidate mapping and open questions | quiz_answers được ghi design-only; giữ mâu thuẫn answer shape, choice_id, is_correct NOT NULL, thiếu unique upsert key, ownership/state và response projection trong draft/open questions. | VERIFIED |
| Runtime wiring | Không tìm thấy route/module/query/test API #30 trong current scan. | UNWIRED / NOT_FOUND |
| Whitespace/conflict markers | Static scan trên DD và worklog sạch; git diff --check thành công. | VERIFIED |
| Runtime tests | Không chạy; scope DD-only và API chưa được wire. | NOT_RUN |
| Context validator | Không cần chạy vì không sửa context page hoặc manifest. | NOT_REQUIRED |

## Kết luận

DD hoàn tất ở trạng thái Draft — Needs Confirmation. Chỉ chuyển sang Final hoặc triển khai runtime sau khi các câu hỏi trong OPEN_QUESTIONS.md được owner xác nhận.

## Cross-AC review — AC-35 quiz tombstone

- Review result: DERIVED proposal added after document-level AC-35 review; owner confirmation is still required.
- Cross-reference: API #90 preserves history on soft-delete when attempts exist; API #91 reads retained history.
- No runtime, catalog, diagram or schema behavior was changed or verified.
