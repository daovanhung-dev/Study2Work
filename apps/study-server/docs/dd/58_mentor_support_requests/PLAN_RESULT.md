# PLAN_RESULT — Study API #58

## Trạng thái trước authoring

- Plan được lập trước các sheet DD: `VERIFIED`.
- API: #58 — Lấy support requests.
- Output: `58_mentor_support_requests/`.
- Status DD dự kiến: `Draft — Needs Confirmation`; source/schema và list cardinality còn gap.
- Loại: read-only; không có mutation DB.
- Phạm vi: thiết kế API #58 thuộc AC-24. Không tạo code, test, schema, migration, catalog edit, diagram edit hoặc ZIP.

## API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #58 | Method/path | `GET /api/v1/mentor/support/requests` | Catalog + AC-24; DIRECT |
| #58 | Actor/auth | Bearer JWT; role Mentor | Catalog + AC-24; DIRECT |
| #58 | Query | `course_id?:int64`, `status?:string` | Catalog + AC-24; DIRECT; không có default/range/enum |
| #58 | Request body | Không có | Catalog; DIRECT |
| #58 | Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<SupportRequest>` | Catalog + diagram; DIRECT, nhưng list cardinality mâu thuẫn |
| #58 | Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR` | Catalog + diagram; DIRECT; không thêm 404/422/409 |

## Source và template manifest

| Nguồn | Định dạng | Đã đọc | Dùng để |
|---|---|---:|---|
| `docs/lists/list_api.md` | Markdown | Có | Contract #58 và schemas SupportRequest, SupportMessage, UserSummary, UploadAsset |
| `AC_UNICA/00_AC_API_INDEX.md` | Markdown | Có | Actor, pre/postcondition, thứ tự API AC-24 |
| `AC_UNICA/AC_03_MENTOR_TEACHING.drawio`, page AC24 | Draw.io XML | Có; node/edge parse | Luồng list → thread → reply → optional resolve |
| `DB_UNICA_TABLES.md`, `DB_UNICA_ERD.drawio` | Markdown/Draw.io | Có | Legacy V1 ERD/table coverage; không có support table |
| `infra/postgres/study-server/DB.sql` | SQL | Có | Legacy DB schema; không có support table |
| `infra/postgres/02_study_db.sql` | SQL | Có; đọc các table liên quan | V1-PILOT candidate support_tickets/messages, learner_profiles, file_objects; không phải runtime proof |
| Current Study router/auth/middleware/tests | Python | Có; source scan | Xác nhận API #58 chưa có route/module/test và ghi giới hạn Mentor/error wiring |
| API Guidelines | Markdown | Có | Envelope và X-Trace-Id convention |
| DD #54 và worklogs #48–#50 | Markdown | Có | Cách ghi gaps, matrices, template và macro-review |

Template `DD_API_Template_MD` đã được registry đăng ký, gồm đúng 8 file theo thứ tự. SHA-256 baseline:

| Template | SHA-256 |
|---|---|
| `00_Cover.md` | `fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63` |
| `01_Lich_su.md` | `d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e` |
| `02_Overview.md` | `c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6` |
| `03_Request.md` | `37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa` |
| `04_Response.md` | `5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8` |
| `05_Data_Mapping.md` | `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b` |
| `06_Error.md` | `e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b` |
| `07_table.md` | `4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356` |

Study workflow requires Markdown only. The read-only prototype remains as `07_table.md` with `N/A — READ-ONLY API`; project workflow overrides the skill ZIP requirement.

## Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT; require Mentor role | Candidate principal for scope check | Role DIRECT; Mentor claim/subject binding SOURCE_REQUIRED |
| `course_id` | Optional query int64 | Intended course filter | DIRECT field; no compatible course relation in pilot support_tickets |
| `status` | Optional query string | Candidate exact status filter | DIRECT field; SupportStatus values/default/casing are SOURCE_REQUIRED |
| `X-Trace-Id` | Optional API Guidelines header | Propagate request trace into envelope/response header | Shared convention; endpoint not wired |
| Body/path | None | N/A | DIRECT from catalog |

## Query Matrix

| Query | Type | Candidate source/fields | Predicate/order | Status |
|---|---|---|---|---|
| Q1 — list requests | SELECT | No approved physical table. V1-PILOT `support_tickets` has UUID id, learner_id, status, assigned_to_subject_id, created_at, resolved_at; lacks course_id and uses incompatible IDs. | Logical Mentor scope; optional exact status; course_id cannot be expressed from this table. No pagination/order contract. | SOURCE_REQUIRED; candidate table is not direct mapping |
| Q2 — request messages | SELECT | V1-PILOT `support_messages` has UUID ticket_id/id, author_subject_id/type, body, attachment_file_ids, sent_at. | Candidate by ticket_id; chronological `sent_at,id` is DERIVED only. | SOURCE_REQUIRED; required nested projection has incompatible IDs/authors |
| Q3 — student/asset projections | SELECT/JOIN | Candidate `learner_profiles` and `file_objects`; UUID IDs and no approved signed URL resolver for this endpoint. | No approved join to numeric UserSummary or UploadAsset. | SOURCE_REQUIRED |

No physical SQL, count query, pagination, stable request ordering, or empty-list behavior is finalized. Do not choose the first matching row to hide a list/response mismatch.

## Mutation Matrix

| Operation | Target | Status |
|---|---|---|
| None | N/A | `N/A — READ-ONLY API`; #60 inserts messages and #61 resolves separately |

## Response Source Matrix

| Response field | Contract type | Candidate source | Mapping/status |
|---|---|---|---|
| `success` | boolean | Envelope branch | true on success; shared convention |
| `businessCode` | string | Catalog | Exact catalog literal |
| `message` | string | Application | Safe message; exact wording unspecified, DERIVED |
| `data.id` | int64 | No compatible approved source; pilot ticket id is UUID | SOURCE_REQUIRED |
| `data.course_id` | int64 | No course column/relation on pilot support_tickets | SOURCE_REQUIRED |
| `data.student.id` | int64 | Pilot learner_profiles.id is UUID | SOURCE_REQUIRED |
| `data.student.full_name` | string | Candidate learner_profiles.full_name is nullable | SOURCE_REQUIRED; requiredness mismatch |
| `data.student.avatar_url` | uri? | Candidate avatar_file_id/file_objects; no approved resolver | SOURCE_REQUIRED |
| `data.status` | SupportStatus | Candidate support_tickets.status varchar | SOURCE_REQUIRED; contract enum members absent |
| `data.messages[].id` | int64 | Pilot support_messages.id is UUID | SOURCE_REQUIRED |
| `data.messages[].author.id` | int64 | Candidate author_subject_id is UUID | SOURCE_REQUIRED |
| `data.messages[].author.full_name` | string | No approved identity projection for LEARNER/STAFF | SOURCE_REQUIRED |
| `data.messages[].author.avatar_url` | uri? | No approved identity/asset resolver | SOURCE_REQUIRED |
| `data.messages[].content` | string | Candidate support_messages.body | Candidate only; model/version mismatch |
| `data.messages[].attachments[].id` | int64 | file_objects.id and attachment_file_ids are UUID | SOURCE_REQUIRED |
| `data.messages[].attachments[].name` | string | Candidate file_objects.original_name | Candidate only |
| `data.messages[].attachments[].url` | uri | No stored URL; signed URL service not mapped | SOURCE_REQUIRED |
| `data.messages[].attachments[].content_type` | string | Candidate MIME fields; no selected field rule | SOURCE_REQUIRED |
| `data.messages[].attachments[].size_bytes` | int64 | Candidate file_objects.size_bytes | Candidate only |
| `data.messages[].attachments[].status` | UploadStatus | Candidate scan_status differs; enum mapping undefined | SOURCE_REQUIRED |
| `data.messages[].created_at` | date-time | Candidate support_messages.sent_at | Candidate only; timestamp normalization not confirmed |
| `data.created_at` | date-time | Candidate support_tickets.created_at | Candidate only |
| `data.resolved_at` | date-time? | Candidate support_tickets.resolved_at | Candidate only; null/omit rule open |
| `meta` | object | Envelope | No pagination contract; empty-object convention needs runtime alignment |
| `traceId` | uuid | Request trace | Shared API Guidelines convention |

## Kế hoạch authoring và review

1. Giữ nguyên contract catalog; không tự thêm query, response collection, status enum hoặc error code.
2. Ghi list-cardinality conflict và đề xuất xử lý như open question; response example chỉ minh họa đúng một SupportRequest theo schema hiện tại.
3. Trình bày filter status exact-match và kết hợp filter khi được gửi như DERIVED candidate; course_id không được gán vào quan hệ suy đoán.
4. Nêu rõ pilot schema là model khác, không phải schema runtime; mark physical projection SOURCE_REQUIRED.
5. Điền đủ Request Usage, Query, Mutation và Response Source trong các sheet; mỗi field/error/condition một dòng.
6. Dùng `07_table.md` N/A vì API read-only. Không tạo file mapping mutation.
7. Tạo OPEN_QUESTIONS cho list cardinality, physical model/ID type, course association, Mentor scope, SupportStatus, nested messages/assets và malformed query behavior.
8. Tạo VERIFICATION_REPORT sau khi chạy contract/template/Markdown checks; ghi macro-review AC-24 pending đến khi #59–#61 hoàn thành.

## Kết quả authoring

Đã tạo 8 sheet theo template đã đăng ký và giữ nguyên phụ lục template byte-for-byte. Nội dung giữ nguyên contract #58, phân tách expected/current behavior và đánh dấu blocker schema/cardinality. OPEN_QUESTIONS ghi 9 câu hỏi. Static checks trước khi thêm report đã pass; final manifest/link check được ghi trong VERIFICATION_REPORT.
