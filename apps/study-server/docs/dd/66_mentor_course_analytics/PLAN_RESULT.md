# Plan Result — Study API #66

## Kết quả theo plan

| Plan item | Kết quả |
|---|---|
| Exact catalog contract | Giữ GET /api/v1/mentor/courses/{course_id}/analytics, Bearer JWT/Mentor, course_id:int64!, no body/query, ApiEnvelope<Page<Course>>, HTTP 200 DESIGN_RESOURCE_RETRIEVED, errors 401/403/404/500. |
| AC-26 trace | Giữ thứ tự #65 aggregate enrollment/progress → #66 learning events → #67 selected-Student progress. Không gộp endpoint hoặc tạo server-to-server call. |
| Current source evidence | API #66 UNWIRED / NOT_FOUND; không có route/module/focused test. Current Mentor guard chưa có. |
| Database evidence | Legacy DDL không có learning event history. V1-PILOT progress facts/snapshots và generic audit/outbox không được coi là learning event store. |
| Direct vs derived | Course/PageMeta direct schema được liệt kê. Ba metric, all-time scope và summary response chỉ là DERIVED proposal; physical event mapping SOURCE_REQUIRED. |
| Read-only mapping | 07_table.md nêu N/A — READ-ONLY API; không đề xuất mutation. |
| Deliverables | 8 template sheets + 3 reports; Markdown-only, không ZIP; không đổi source/schema/catalog/diagram/context. |
| Verification | Static checks được ghi trong VERIFICATION_REPORT.md; runtime tests không chạy. Macro-review #65–#67 đã được thực hiện sau khi DD #67 tồn tại; còn open questions về source/contract. |

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

Verification must compare each output suffix beginning at the template appendix heading byte-for-byte with its registered template suffix. Output sheet fingerprints will be added to VERIFICATION_REPORT.md after static checks.

## Macro-review AC-26 sau DD #67

`VERIFIED_WITH_OPEN_QUESTIONS`: #65 class progress, #66 learning-event analytics và #67 selected-Student detail được tách riêng; không tạo server-to-server call. Event-active learner count của #66 không thay enrollment roster, và current progress timestamps không thay event stream. Cả ba direct response contract vẫn là `Page<Course>` dù không khớp AC-26; pagination, Mentor access, live schema và error envelope cần quyết định trước khi wiring. Xem [API #67 report](../67_mentor_student_progress/VERIFICATION_REPORT.md).

