# Plan Result — Study API #65

## Kết quả theo plan

| Plan item | Kết quả |
|---|---|
| Giữ direct catalog evidence | Giữ GET /api/v1/mentor/courses/{course_id}/progress, Mentor Bearer JWT, course_id:int64!, không query/body, direct ApiEnvelope<Page<Course>>, HTTP 200 DESIGN_RESOURCE_RETRIEVED, errors 401/403/404/500. Runtime Page<MentorStudentProgress> là local DERIVED discrepancy để đáp ứng AC-26, không phải catalog approval. |
| Bám AC-26 | Tách API #65 class progress khỏi #66 learning-event analytics và #67 student detail. Không tạo server-to-server calls. |
| Giữ source boundary | Runtime dùng checked-in legacy BIGINT candidate; V1-PILOT UUID/versioned schema được tách riêng; không claim live schema. |
| Phân tách direct/derived | Catalog response Page<Course> được giữ là direct evidence; local progress response, formula, paging, access, eligibility và latest-row policy đều ghi DERIVED. |
| Read-only mapping | 07_table.md ghi N/A — READ-ONLY API; local SELECT relations và columns được liệt kê riêng, không thêm schema/migration. |
| Deliverables | Tám sheet template và ba reports được reconcile; API module, route, middleware, HTTP tests và server-study context/manifest được cập nhật. |
| Verification | 20 API #65 tests, 47 linked #65/#62/#9 tests, full Study suite 680 passed, Ruff pass; DD/context/static checks được ghi ở VERIFICATION_REPORT.md. |

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

`VERIFIED_WITH_OPEN_QUESTIONS` after local API #65 wiring and review of DD #66/#67. #65 roster summary, #66 event aggregate and #67 selected-Student progress remain separate responsibilities; #66/#67 are still unwired. Runtime #65 uses the DERIVED PUBLISHED denominator/floor formula and latest-row policy. Direct `Page<Course>` contract and unbounded no-input pagination remain catalog/owner decisions. Local direct-owner auth, active enrollment, empty behavior, error envelope and middleware mapping are covered by HTTP tests. Live schema and business approval remain open. See [API #67 report](../67_mentor_student_progress/VERIFICATION_REPORT.md).

