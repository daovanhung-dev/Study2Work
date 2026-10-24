# VERIFICATION_REPORT — Study API #67

## Kết quả

- DD status: Draft — Needs Confirmation; response-shape, authorization and schema decisions remain open.
- Deliverables: đúng 8 template sheets và 3 reports, tổng cộng 11 Markdown files.
- Runtime API #67: UNWIRED / NOT_FOUND; không có route/module/focused test.
- AC-26 macro-review #65–#67: `VERIFIED_WITH_OPEN_QUESTIONS` ở mức tài liệu/source tĩnh.
- Runtime tests: không chạy; docs-only.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Deno selector chọn #48/#49/#50; cả ba worklog đã đọc đầy đủ; không thiếu. | PASS |
| Plan-before-authoring | Requirement, current behavior, source trace, plan và năm ma trận được ghi trong worklog trước khi tạo DD folder. | PASS |
| Catalog/diagram | Exact contract #67 và thứ tự AC-26 #65 → #66 → chọn Student → #67 đã đối chiếu. | PASS — STATIC |
| Source/schema | #65–#67 đều không có route/module/focused test; API #9 source lọc PUBLISHED course/lesson và sort `sort_order,id`; legacy và V1-PILOT progress schema vẫn khác nhau. | PASS — STATIC SOURCE REVIEW |
| Manifest/front matter | Exact 11-file set; cả 8 sheet có dd_id 67 và Draft — Needs Confirmation. | PASS |
| Contract/error set | GET path, Bearer JWT/Mentor, hai path int64, no query/body, `ApiEnvelope<Page<Course>>`, HTTP 200; đúng 4 direct errors 401/403/404/500. | PASS |
| Direct/candidate response | Course/PageMeta/envelope fields được liệt kê; `StudentCourseProgress` và mọi progress fields/formula tách riêng, gắn DERIVED. | PASS |
| Template appendix | 8/8 output appendix suffix trùng registered template byte-for-byte. | PASS |
| JSON/Markdown | JSON parse; relative links/anchors resolve; table widths nhất quán; fences cân bằng; không trailing whitespace. | PASS |
| AC-26 macro-review | Tách class progress (#65), event analytics (#66), detail hiện trạng theo Student (#67); xác nhận shared #65/#67 candidate formula, response/page gaps, access/schema/error blockers. | VERIFIED_WITH_OPEN_QUESTIONS |
| `git diff --check` | Chạy sau khi cập nhật reports và worklogs. | PASS |
| Runtime tests | Không chạy; docs-only và endpoint chưa wired. | NOT_RUN |
| Context validator | Không áp dụng; không thay đổi context page hoặc manifest. | NOT_APPLICABLE |

## Output fingerprints — SHA-256

| Sheet | SHA-256 |
|---|---|
| 00_Cover.md | 346e49bcdef381bca0cb5020e19533f860884f07caacdeacce891075a41a4869 |
| 01_Lich_su.md | 05c87e96b29c7aeaf275facc5b65f5430a010e1c2ae4c1a4413a0c7f5bde873d |
| 02_Overview.md | 77d4aa51846a0507039c4a77d50264f982165d8c6d87586bb74375d4ae94be0a |
| 03_Request.md | 29ccbb954c36036388a9ae46edb4907707db68b58dabd885f679f0dfd0170b51 |
| 04_Response.md | 9c832cf62ab9dc2228261e2d55db7153b08b85749942e6d0c0caf9a16a870206 |
| 05_Data_Mapping.md | 6f6cd598dc7d70946619219211eea3fd5e061331ca6696ee80ccdc38a7c40b0c |
| 06_Error.md | 5dd4b00989e47490ddb230e0258ecb88a4fec53cac6ec1f730d9cf34a73d6b20 |
| 07_table.md | 31a24ccdfc0464423abfc4a21303f420d31780ba90a23f78afed0aa9ca4b3262 |

## Macro-review findings

- AC-26 sequence is UI orchestration; no server-to-server request is specified.
- #65 is class roster progress, #66 is course-wide learning-event analytics, and #67 is current lesson progress for one selected Student.
- #65 and #67 candidate calculations share the PUBLISHED lesson set and floor-average formula. Both are still DERIVED. #66 `students_with_learning_events` is distinct from #65 enrollment count; progress state and `last_accessed_at` are not an approved event source.
- All three direct responses are `Page<Course>` with no page/size request; they do not express the AC-26 data and provide no paging policy.
- Mentor course access, Student roster eligibility, live schema, duplicate progress rows, formula/empty rules, error envelope and middleware allowlist remain unresolved.
