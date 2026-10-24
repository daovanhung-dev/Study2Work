# PLAN_RESULT — Study API #60

## Kết quả plan trước authoring

- Task: `docs`; scope `server-study`; không có dependency cross-scope.
- API: #60 — Gửi phản hồi Mentor vào support request.
- Output: `60_mentor_support_reply/`.
- Trạng thái DD: `Draft — Needs Confirmation`; physical support model, attachment registry, Mentor identity và ref encoding chưa được xác nhận.
- Loại: POST có logical INSERT SupportMessage; không phải API upload file hay resolve request.
- AC-24 group-review #58–#61 còn pending đến khi #61 có DD.

## Source inventory và contract

| Source | Bằng chứng dùng | Trạng thái |
|---|---|---|
| `docs/lists/list_api.md` row #60 | Method/path, Mentor Bearer, request fields, response và exact status/error set | `DIRECT` |
| `docs/lists/list_api.md` reusable schemas | SupportRequest, SupportMessage, UserSummary, UploadAsset fields | `DIRECT` |
| AC-24 API index + `AC_03_MENTOR_TEACHING.drawio` | #58 list → #59 detail/thread → #60 insert reply → decision: #61 resolve or keep OPEN | `DIRECT` |
| AC-17 `AC_02_STUDENT_LEARNING.drawio` | API #34 upload precedes submission; request uses opaque `file refs:string!` | `DIRECT`; encoding unresolved |
| AC-21 `AC_03_MENTOR_TEACHING.drawio` | API #34 upload precedes lecture create; request uses `asset refs:string!` | `DIRECT`; encoding unresolved |
| DD #34 | UploadAsset ID, persistence, ownership, status and URL are unresolved | `Draft / SOURCE_REQUIRED` |
| DD #35 | `file refs` wire key, representation, cardinality and binding to #34 remain open | `Draft / SOURCE_REQUIRED` |
| DD #47 | `asset_refs` is explicitly DERIVED wire-key candidate; reference string remains opaque | `Draft / DERIVED` |
| DD #58/#59 | AC-24 support model, int64/UUID, Mentor scope, message/asset projection blockers | `Draft / SOURCE_REQUIRED` |
| Legacy DB.sql/ERD | No support request/message physical model | `DESIGN_ONLY / NOT_FOUND` |
| `infra/postgres/02_study_db.sql` | V1-PILOT support_tickets/support_messages and file_objects use UUIDs; not runtime proof | `PILOT_CANDIDATE` |
| Current Study router/modules/tests/middleware | No #60 route/module/test; path absent from `DESIGN_CONTRACT_PATHS` | `CURRENT_SOURCE / UNWIRED` |
| Current DB helper/context | Request Session closes without implicit commit; caller owns transaction | `CURRENT_SOURCE` |

## API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #60 | Method/path | `POST /api/v1/mentor/support/{request_id}/reply` | Catalog + AC-24; DIRECT |
| #60 | Actor/auth | Bearer JWT; role Mentor | Catalog + AC-24; DIRECT |
| #60 | Path | `request_id:int64!` | Catalog; DIRECT |
| #60 | Body | `message:string!`; `attachment refs:string!` | Catalog + diagram; DIRECT labels/types, exact wire key/encoding unresolved |
| #60 | Query | None declared | Catalog; DIRECT |
| #60 | Success | HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<SupportRequest>` | Catalog + diagram; DIRECT |
| #60 | Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR` | Catalog + diagram; DIRECT |
| #60 | Logical mutation | `INSERT SupportMessage` | AC-24 diagram; DIRECT effect, physical mapping unresolved |

## AC-24 flow and API boundaries

```text
#58 mở danh sách → #59 đọc request/thread → Mentor nhập phản hồi → #60 INSERT SupportMessage
→ quyết định “Vấn đề đã được xử lý?”
   ├─ YES → #61 cập nhật request status = RESOLVED
   └─ NO  → giữ OPEN
→ cập nhật thread/trạng thái
```

- API #60 chỉ tạo reply. Không UPDATE request status, không đóng request, không tạo notification hoặc upload bytes.
- Success `SupportRequest` phải phản ánh message vừa gửi; cách rehydrate response cần cùng model/schema được duyệt.
- Không thêm `IN_PROGRESS`/`WAITING_LEARNER` transition theo suy đoán. Nếu request đã RESOLVED/CANCELLED thì cho reply, từ chối hay reopen còn là câu hỏi riêng.

## Request Usage Matrix

| Request item | Source/use | Validation/use | Status |
|---|---|---|---|
| Authorization | Bearer JWT; role Mentor | Candidate principal cho scope request và upload refs | Role DIRECT; Mentor guard/subject mapping `SOURCE_REQUIRED` |
| `request_id` | Required path int64 | Logical request lookup và scope check | Type DIRECT; pilot ticket ID UUID không tương thích |
| `message` | Required string body field | Đề xuất reject empty/whitespace bằng 422; giữ nguyên text sau khi chỉ dùng trim để kiểm tra | Required/type DIRECT; nonblank rule `DERIVED`, length limit không đặt |
| `attachment refs` | Required string catalog notation | Đề xuất wire key `attachment_refs`; chuỗi comma-separated `UploadAsset.id` int64 từ #34; `""` nghĩa không có attachment | Proposal `DERIVED`; key/encoding/empty semantics cần chốt chung #35/#47 |
| Query | None | N/A | DIRECT |
| `X-Trace-Id` | API Guidelines optional header | Propagate/generate when wired | Shared convention; route absent |

### Attachment-reference proposal

Để client upload từng file qua #34 rồi gửi reply đơn giản, proposal là một chuỗi như `"81001,81002"`, chứa các `UploadAsset.id` contract int64; chuỗi rỗng biểu thị không đính kèm. Đây là `DERIVED`, chưa được catalog/diagram xác nhận. Khuyến nghị dùng cùng encoding cho API #35 `file refs` và #47 `asset refs` khi macro-review. Không thể triển khai lookup/ownership dựa trên proposal này cho đến khi #34 có asset ID và metadata registry được duyệt; V1-PILOT `file_objects.id` là UUID.

## Query Matrix

| Query | Type | Candidate source/fields | Predicate/purpose | Status |
|---|---|---|---|---|
| Q1 — SupportRequest scope/existence | Logical SELECT | No approved support table. V1-PILOT `support_tickets` has UUID id, learner_id, status and assigned_to_subject_id; no course_id. | Locate one request by int64 path ID and enforce Mentor scope before mutation. | `SOURCE_REQUIRED`; no physical SQL |
| Q2 — attachment ref resolution | Logical lookup | No approved UploadAsset registry. #34 has no database write in its DD; pilot `file_objects` uses UUID IDs and metadata fields. | Verify every referenced asset exists, is usable, belongs to allowed uploader/purpose and can be attached to this request. | `SOURCE_REQUIRED`; no physical query |
| Q3 — updated response projection | Logical SELECT/resolver | SupportRequest, SupportMessage, UserSummary and UploadAsset projections | Re-read the request/thread after the insert so the new message is included in `data`. | `SOURCE_REQUIRED`; response cardinality is direct, source mapping is not |

## Mutation Matrix

| ID | Operation | Physical candidate | Candidate fields | Value source/rule | Evidence/status |
|---|---|---|---|---|---|
| M1 | INSERT SupportMessage | V1-PILOT `support_messages` only | `id`, `ticket_id`, `author_subject_id`, `author_type`, `body`, `attachment_file_ids`, `is_internal`, `sent_at` | Path ID, authenticated Mentor, message, resolved refs and server timestamp | Logical INSERT DIRECT; table is not approved/live and uses UUID |
| M2 | UPDATE SupportRequest | None | None | No status update in #60; #61 owns RESOLVED transition | N/A by AC-24 sequence |
| M3 | Object Storage write | None | None | Files upload separately through #34 | N/A for reply operation |

### Candidate insert mapping details

| Candidate column | Candidate assignment | Status / discrepancy |
|---|---|---|
| `id` | Generated message identifier | Pilot UUID primary key has no default; contract response requires int64; generator/type unresolved. |
| `ticket_id` | Related SupportRequest identifier | Pilot UUID FK cannot directly consume contract int64 request_id. |
| `author_subject_id` | Authenticated Mentor subject | JWT/DB identity mapping unresolved. |
| `author_type` | `STAFF` proposal for Mentor | Candidate pilot enum permits `LEARNER/STAFF`; Mentor→STAFF is DERIVED. |
| `body` | `message` request value | Candidate alias; reject whitespace-only by DERIVED 422 proposal; no length limit. |
| `attachment_file_ids` | Resolved refs from `attachment_refs` proposal | Pilot UUID[] conflicts with #34 UploadAsset int64 and has no approved lookup. |
| `is_internal` | `false` proposal for a learner-visible reply | Pilot default is false; public-reply interpretation is DERIVED. |
| `sent_at` | Server-generated time | Pilot is NOT NULL with no default; timezone/clock rule must be confirmed. |

### Transaction proposal

- Candidate: check request scope and attachment refs; insert message; read updated SupportRequest/thread and finish response mapping; commit only after the complete success projection is available.
- Any DB/projection failure before commit rolls back the insert. This follows current caller-owned transaction convention, but API #60 has no runtime code and the physical transaction is not established.
- No storage write happens in this transaction. API #34 owns upload side effects separately; orphan/failed-reference cleanup needs the #34 design owner.

## Response Source Matrix

| Response field | Contract type | Candidate source/transform | Status |
|---|---|---|---|
| `success` | boolean | Envelope branch | Shared convention |
| `businessCode` | string | Catalog literal | `DESIGN_RESOURCE_UPDATED` on success |
| `message` | string | Safe localized application text | Exact wording unspecified; DERIVED |
| `data.id` | int64 | Request/ticket ID | SOURCE_REQUIRED; pilot UUID |
| `data.course_id` | int64 | Support request/course relation | SOURCE_REQUIRED; pilot ticket has no course relation |
| `data.student` and nested fields | UserSummary | Learner identity projection | SOURCE_REQUIRED; pilot profile UUID/name may be nullable |
| `data.status` | SupportStatus | Support request status | SOURCE_REQUIRED; #60 must not alter it |
| `data.messages[]` | SupportMessage[] | Existing thread plus newly inserted reply | New reply inclusion is implied by updated SupportRequest; source/ordering/visibility unresolved |
| `data.messages[].id` | int64 | New message ID | SOURCE_REQUIRED; pilot UUID generator conflicts |
| `data.messages[].author` | UserSummary | Mentor identity projection | SOURCE_REQUIRED; author_type STAFF is DERIVED candidate only |
| `data.messages[].content` | string | Request `message` → candidate `body` | Candidate alias; no length rule |
| `data.messages[].attachments[]` | UploadAsset[] | Resolved attachment refs | SOURCE_REQUIRED; API #34 registry/ID/resolver absent |
| `data.messages[].created_at` | date-time | Candidate `sent_at` | Source/timezone mapping unresolved |
| `data.created_at` | date-time | Support request creation source | SOURCE_REQUIRED |
| `data.resolved_at` | date-time? | Support request state source | SOURCE_REQUIRED; #60 does not resolve |
| `meta` | object | Envelope convention | Empty object candidate; no pagination |
| `traceId` | uuid | Request trace | API Guidelines convention when wired |

Success response must preserve all fields in the reusable schema; complete field-level matrix is in `04_Response.md`. Error `data:null` guideline versus current helper `{}` remains a conditional runtime discrepancy.

## Discrepancies and status

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Route/runtime | No #60 route/module/test; path absent from design error allowlist | `UNWIRED / NOT_FOUND` | DD is design-only. |
| Physical SupportMessage | Legacy schema absent; pilot table is UUID and not runtime-approved | `DISCREPANCY / SOURCE_REQUIRED` | No production INSERT can be finalized. |
| Attachment refs | #34 ID/persistence unresolved; #35/#47 representations unresolved; pilot file IDs UUID | `DERIVED / SOURCE_REQUIRED` | CSV int64 is a harmonization proposal; no confirmed lookup. |
| Mentor identity/author | Current guard Student-only; pilot author type LEARNER/STAFF | `SOURCE_REQUIRED / DERIVED` | Need approved Mentor identity and author mapping. |
| Request lifecycle | AC-24 assigns resolution to #61 and NO keeps OPEN | `DIRECT` for no status mutation in #60 | Post-resolution reply behavior remains open. |
| Message validation | Required string contract; no blank/length policy | `DERIVED / NEEDS_CONFIRMATION` | Proposal rejects whitespace-only; no min/max. |
| Middleware | Path missing from `DESIGN_CONTRACT_PATHS` | `CONDITIONAL_FUTURE_WIRING` | 422/500 design codes need route wiring update; not current API behavior. |

## Template manifest

Registered `createDD-markdown` is `SOURCE_BACKED` for `server-study`; Study workflow requires Markdown, no ZIP. Eight registered template names and current SHA-256 values:

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

## Authoring and verification plan

1. Tạo 8 template sheets tiếng Việt ở trạng thái `Draft — Needs Confirmation`; ghi `attachment_refs` CSV và nonblank message thành DERIVED proposal.
2. Dùng candidate `support_messages` trong 07 table với từng column/status tách rõ; không ghi schema/runtime đã được duyệt.
3. Bảo toàn exact catalog input, response, success và error set; không thêm status mutation, notification, 409, 503 hoặc field mới.
4. Tạo OPEN_QUESTIONS cho support IDs/model, Mentor scope, ref wire/encoding/ownership, blank/length rules, request state, author visibility và rehydrate semantics.
5. Tạo VERIFICATION_REPORT sau static checks; xác nhận exact 11-file manifest, exact appendices, JSON, relative links, tables/fences/whitespace. Runtime tests `NOT_RUN`.
6. AC-24 macro-review vẫn pending tới khi API #61 DD tồn tại; sau đó đối chiếu #58–#61 cùng phần ref flow #34/#35/#47 để thống nhất semantics trước readiness claim.
