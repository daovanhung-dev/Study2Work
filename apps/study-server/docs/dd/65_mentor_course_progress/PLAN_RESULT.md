# Plan Result — Study API #65

## Kết quả theo plan

| Plan item | Kết quả |
|---|---|
| Giữ exact catalog contract | Giữ GET /api/v1/mentor/courses/{course_id}/progress, Mentor Bearer JWT, course_id:int64!, không query/body, ApiEnvelope<Page<Course>>, HTTP 200 DESIGN_RESOURCE_RETRIEVED, đúng errors 401/403/404/500. |
| Bám AC-26 | Tách API #65 class progress khỏi #66 learning-event analytics và #67 student detail. Không tạo server-to-server calls. |
| Giữ source boundary | API #65 là UNWIRED / NOT_FOUND; DDL legacy và V1-PILOT được tách riêng; không claim live schema. |
| Phân tách direct/derived | Contract response Page<Course> được giữ; learner progress response/formula/paging/access đều đánh dấu DERIVED hoặc SOURCE_REQUIRED. |
| Read-only mapping | 07_table.md ghi rõ N/A — READ-ONLY API; query relations chỉ là candidate. |
| Deliverables | Tám sheet template và ba reports Markdown; không tạo ZIP, code, test, schema, catalog, diagram hoặc context edits. |
| Verification | Static-only check xác nhận manifest, template appendices, contract, JSON, links, tables, fences, whitespace và fingerprints; kết quả chi tiết ở VERIFICATION_REPORT.md. |

## Template source fingerprints — SHA-256

| Sheet | Template |
|---|---|
| 00_Cover.md | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md | c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6 |
| 03_Request.md | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md | 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b |
| 06_Error.md | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

## Fingerprint interpretation

The template files were fingerprinted before authoring. Verification compares each output suffix beginning at the template appendix heading byte-for-byte with its registered template suffix. Output file SHA-256 values are recorded in VERIFICATION_REPORT.md after static validation.

## Macro-review AC-26 after DD #67

`VERIFIED_WITH_OPEN_QUESTIONS` at document level. #65 roster summary, #66 event aggregate and #67 selected-Student progress are separate responsibilities. The #65/#67 candidate lesson denominator and formula match; #66 event-active count is not enrollment count and must use an approved event source. Direct `Page<Course>` contracts and pagination gaps remain unchanged and require owner decision. Shared Mentor authorization, live schema, progress row uniqueness, empty behavior and error envelope remain open. See [API #67 report](../67_mentor_student_progress/VERIFICATION_REPORT.md).

