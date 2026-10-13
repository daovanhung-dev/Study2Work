# VERIFICATION_REPORT — Study API #28

## Phạm vi

Tài liệu DD trong apps/study-server/docs/dd/28_quizzes_detail/. Không chạy runtime tests vì API #28 chưa được tìm thấy trong Study route/module/tests và yêu cầu chỉ tạo tài liệu.

## Nguồn đối chiếu

- docs/lists/list_api.md — API #28 row, ApiEnvelope/Quiz/QuizQuestion schemas và business-code catalog.
- apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md — AC-16 actors/preconditions/postconditions.
- apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio — AC-16 activity flow.
- apps/study-server/docs/diagrams/DB_UNICA_TABLES.md, DB_UNICA_ERD.drawio và infra/postgres/study-server/DB.sql — candidate schema/relations only.
- apps/study-server/app/api/v1.py, app/modules/ và tests/ — runtime wiring scan.
- contracts/api-guidelines/README.md — envelope/error format.

## Template fingerprint

| Template file | SHA-256 |
|---|---|
| 00_Cover.md | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md | c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6 |
| 03_Request.md | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md | 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b |
| 06_Error.md | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

## Output fingerprint

SHA-256 checksums cover the eight template-derived DD sheets; reports and worklog are excluded from this checksum table.

| Output file | SHA-256 |
|---|---|
| 00_Cover.md | 3771d28375c64e34a519578e93fba1c5fb115b8f68c60492910c0d97420dae9f |
| 01_Lich_su.md | 5e23217786cda76e60bfc923610c67b419cf05bc317a17da781162805da88e23 |
| 02_Overview.md | 836f64dd320f58afea02895acb1f2e01c3f32b0f1e95faa8805d7f0fb80b4c0b |
| 03_Request.md | cfcf002f6768e041c5f777846ba7b68ac4d6e59f68e392cee2b0eb0267d7c09f |
| 04_Response.md | d43309c853960c58cab917f9d24b332819a445b3186d3e56f1641679882a263e |
| 05_Data_Mapping.md | fc7c971f1e96a55722c7eead2bf1fdc7291374f10d2950731265bb004d2a6e48 |
| 06_Error.md | a77a7503fd48b351b028eafc1d2baa4f2ba541bb7dfc0429e9d850603e7c358c |
| 07_table.md | 0c0c0ba4f2a2e6c99d332c0da8ef2a187fa3bc26ba76805e7cd4f6b6bfe642e5 |

## Kết quả kiểm tra

| Check | Result | Status |
|---|---|---|
| Template file set/order | Đủ 8 sheet, đúng tên và thứ tự 00–07 theo template. | VERIFIED |
| Front matter/API ID/status | Cả 8 sheet có front matter, `dd_id: "28"`, order 0–7 và status Draft — Needs Confirmation. | VERIFIED |
| Markdown tables | Các bảng Markdown có số cột nhất quán và separator hợp lệ. | VERIFIED |
| JSON examples | Parse thành công 2 JSON fence trong sheet Response. | VERIFIED |
| Relative links and anchors | Tất cả link nội bộ và fragment trong DD resolve được. | VERIFIED |
| Contract path/response/error code set | Khớp catalog: GET path, Student Bearer, `quiz_id:int64!`, `ApiEnvelope<Quiz>`, 200/401/403/404/500; không thêm 409. | VERIFIED |
| Student response answer-key exclusion | Cả hai JSON response example không chứa key `is_correct`. | VERIFIED |
| Whitespace/conflict markers | Xác nhận qua `git diff --check` và quét toàn bộ file mới. | VERIFIED |
| Runtime tests | Not run; documentation-only task and route is not wired. | NOT_RUN |

## Open discrepancy

AC-16 activity diagram mentions 403/409 for quiz eligibility, attempt limit or expiry. API #28 catalog lists 401/403/404/500 and has no 409. This DD follows the catalog and records the conflict; it does not add DESIGN_STATE_CONFLICT.

## Kết luận

Chỉ chuyển DD khỏi Draft — Needs Confirmation sau khi owner xác nhận các câu hỏi trong OPEN_QUESTIONS.md và canonical contract được cập nhật nếu cần.
