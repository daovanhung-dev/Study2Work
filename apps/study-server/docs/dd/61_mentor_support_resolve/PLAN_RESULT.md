# PLAN_RESULT — Study API #61

## Trạng thái plan

- Plan được ghi trong worklog trước khi tạo các sheet DD: `VERIFIED`.
- API: #61 — Đóng yêu cầu hỗ trợ Mentor.
- Output: `61_mentor_support_resolve/`.
- DD status: `Draft — Needs Confirmation`; support schema/ID, Mentor scope, state enum và response projection chưa được xác nhận.
- Loại: PATCH; logical UPDATE SupportRequest.status. Không INSERT message và không xử lý upload.
- Giao hàng Study: 8 sheets + 3 reports dạng Markdown; không tạo ZIP theo `.agents/server-study/workflows/README.md`.

## Source inventory và contract

| Source | Bằng chứng dùng | Trạng thái |
|---|---|---|
| `docs/lists/list_api.md` row #61 | Method/path, auth/role, path, response, success/error set | DIRECT |
| `docs/lists/list_api.md` reusable schemas | SupportRequest, SupportMessage, UserSummary, UploadAsset | DIRECT shape; enum values/mapping absent |
| AC-24 index | Actor, precondition, postcondition, API sequence | DIRECT |
| `AC_03_MENTOR_TEACHING.drawio`, page AC24 | #60 INSERT → decision; YES #61 → status RESOLVED; NO keeps OPEN | DIRECT; XML parsed |
| DD #58 | List/cardinality discrepancy and shared model/access/projection gaps | Draft; blockers retained |
| DD #59 | Detail/thread projection and Mentor scope gaps | Draft; reused projection boundary |
| DD #60 | Reply INSERT boundary; #61 owns resolve; post-resolution behavior open | Draft; cross-API boundary |
| Legacy DB guide/ERD and `infra/postgres/study-server/DB.sql` | No physical SupportRequest/SupportMessage model | NOT_FOUND in legacy source |
| `infra/postgres/02_study_db.sql` | Candidate support_tickets/support_messages, UUID IDs, status/timestamp/trigger | V1-PILOT only; not live/approved proof |
| Current router/modules/tests | No #61 route/module/test; Mentor guard absent | UNWIRED / NOT_FOUND |
| DB helper and API Guidelines | Caller-owned transaction; trace/envelope conventions | Current shared helpers, not #61 runtime |
| `createDD-markdown` and template set | Registry wires skill to `server-study`; eight templates match registered hashes | SOURCE_BACKED; Study workflow overrides ZIP packaging |

## API Requirement Matrix

| API ID | Method/path | Actor/auth | Input | Success/response | Errors | Status |
|---|---|---|---|---|---|---|
| #61 | `PATCH /api/v1/mentor/support/{request_id}/resolve` | Bearer JWT; Mentor | `request_id:int64!`; no body/query | HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<SupportRequest>` | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR` | Catalog DIRECT |

## AC-24 behavior and API boundary

```text
#58 list → #59 read request/thread → #60 INSERT SupportMessage
→ “Vấn đề đã được xử lý?”
   ├─ YES → #61 UPDATE request status = RESOLVED
   └─ NO  → không gọi #61; giữ OPEN
→ cập nhật thread/trạng thái
```

- #61 chỉ thay đổi trạng thái SupportRequest; không ghi thêm message và không sửa attachments.
- #60 response giữ trạng thái hiện tại; không chuyển status trước nhánh YES.
- Response #61 là cùng schema SupportRequest mà #59/#60 trả; projection hiện chưa implementable vì physical mapping còn thiếu.
- #58 list/cardinality mismatch vẫn là blocker riêng; #61 không đổi response shape của #58.

## Request Usage Matrix

| Request item | Source/use | Mapping/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT; require Mentor | Principal dùng cho request scope | Role DIRECT; guard/subject mapping SOURCE_REQUIRED |
| `request_id` | Required path int64 | Logical SupportRequest lookup, maps to `data.id` | Type DIRECT; pilot key UUID; parse/overflow → catalog 422 |
| Body/query | None | None | DIRECT |
| `X-Trace-Id` | Optional API Guidelines header | Propagate/generate when wired | Shared convention; not current #61 runtime |

## Query Matrix

| Query | Type | Candidate source/fields | Predicate/purpose | Status |
|---|---|---|---|---|
| Q1 request/scope/state | Logical SELECT | Pilot `support_tickets`: `id`, `status`, `assigned_to_subject_id`, `resolved_at` | Locate request, check Mentor assignment and read current state | SOURCE_REQUIRED; UUID/int64 and principal mapping conflict |
| Q2 response reload | Logical read/resolver | SupportRequest + nested Student/messages/attachments projection from #59/#60 | Return updated SupportRequest after mutation | SOURCE_REQUIRED; no compatible approved relation/resolver |

No executable SQL is specified because the physical key and Mentor predicate are unresolved.

## Mutation Matrix

| ID | Operation | Candidate target | Fields/condition | Status |
|---|---|---|---|---|
| M1 | UPDATE | Pilot `support_tickets` | OPEN → status RESOLVED; candidate resolved_at = server timestamp | Logical status DIRECT; target/column/time DERIVED candidate |
| M1 retry | No-op success | Existing request already RESOLVED | Keep resolved_at unchanged | DERIVED idempotency proposal |
| M1 invalid state | No write | Status outside OPEN/RESOLVED | 422 `DESIGN_VALIDATION_ERROR` | DERIVED; enum/allowed states need approval |
| M2 | No message mutation | `support_messages` | No INSERT/UPDATE/DELETE | N/A; #60 owns message INSERT |

## Response Source Matrix

| Field group | Contract | Candidate source/transform | Gap/status |
|---|---|---|---|
| Envelope | `ApiEnvelope<SupportRequest>` | Shared envelope and trace convention | Direct contract; current error `data` serialization differs from guideline |
| `data.id` | int64 | Support request key | SOURCE_REQUIRED; pilot UUID mismatch |
| `data.course_id` | int64 | Course relation | SOURCE_REQUIRED; pilot ticket has no course_id |
| `data.student.*` | UserSummary | Learner identity resolver | SOURCE_REQUIRED; numeric IDs/profile fields unresolved |
| `data.status` | SupportStatus | `RESOLVED` on first success | Logical value DIRECT; persisted enum unresolved |
| `data.messages[]` | SupportMessage[] | Existing thread via #59/#60 projection | SOURCE_REQUIRED; no message mutation in #61 |
| `data.created_at` | date-time | Request creation time | SOURCE_REQUIRED; pilot candidate only |
| `data.resolved_at?` | date-time? | Candidate `support_tickets.resolved_at` | Optional field DIRECT; assignment/null/omit rule DERIVED/open |
| Nested author and UploadAsset fields | UserSummary/UploadAsset | Existing resolver/projection | SOURCE_REQUIRED; UUID IDs and URL/status mapping unresolved |

## State handling proposal

- `OPEN`: write `RESOLVED` and server time to candidate `resolved_at`.
- `RESOLVED`: return the current resource without updating timestamp (idempotent retry).
- Other status: return the catalogued 422 code without mutation.
- The diagram directly identifies OPEN and RESOLVED, while pilot DDL lists other statuses. The complete SupportStatus enum and allowed transition set need owner confirmation.

## Template fingerprints

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

## Kế hoạch authoring và review

1. Tạo tám sheets theo thứ tự template; front matter thống nhất `dd_id=61`, `Draft — Needs Confirmation`.
2. Hoàn thành Data Mapping/state proposal và candidate table mapping trước khi chốt Request/Response; Request/Response chỉ giữ contract trực tiếp.
3. Giữ đúng năm error codes; không thêm HTTP 409, 503, error field hoặc body field.
4. Tạo OPEN_QUESTIONS cho schema/ID, Mentor scope, enum/transitions, idempotency, timestamp, full response projection, 403/404 privacy order và envelope discrepancy.
5. Kiểm tra JSON, links/anchors, table/fence/whitespace, template appendices và exact package manifest; runtime tests không chạy.
6. Macro-review #58–#61 sau khi #61 được tạo; giữ list cardinality, schema/ID, identity, message/attachment projection và lifecycle blockers ở trạng thái open.

## Source trace

```text
AC-24 -> #60 inserts reply -> YES -> #61 updates request to RESOLVED -> reload SupportRequest -> 200 updated envelope
```

<a id="macro-review-ac-24-58-61"></a>

## Macro-review AC-24 #58–#61

### Kết luận

`VERIFIED_WITH_OPEN_QUESTIONS`: luồng API và ranh giới side effect khớp AC-24; nhóm chưa implementation-ready do các contract/schema/access/projection gaps dưới đây. Không sửa catalog hoặc tự hợp nhất các proposal DERIVED thành behavior đã duyệt.

| API | Vai trò theo catalog/AC-24 | Kết quả review |
|---|---|---|
| #58 | Đọc support requests theo query filters | GET read-only; giữ nguyên response `ApiEnvelope<SupportRequest>` dạng singular trong catalog. Endpoint plural và luồng “danh sách” tạo DISCREPANCY cardinality, chưa đổi thành list/page. |
| #59 | Đọc một request và conversation | GET read-only; response thread dùng cùng SupportRequest projection nhưng physical mapping, message ordering/bounds và visibility chưa có nguồn được duyệt. |
| #60 | Gửi reply | POST chỉ INSERT SupportMessage rồi trả request/thread; không resolve request. Attachment wire key/encoding và asset ownership/lookup vẫn là proposal/open. |
| #61 | Resolve sau nhánh YES | PATCH chỉ UPDATE status thành RESOLVED rồi trả SupportRequest; nhánh NO bỏ qua #61 và giữ OPEN. Timestamp, retry và invalid-state handling vẫn là DERIVED. |

### Blockers dùng chung

1. **Response cardinality #58:** catalog khai báo `ApiEnvelope<SupportRequest>` dù path/flow là plural/list. Giữ nguyên catalog contract và mở câu hỏi; không suy ra Page/items.
2. **Persistence/ID/course:** legacy schema không có support model; V1-PILOT có `support_tickets`/`support_messages` với UUID trong khi API dùng int64, và ticket candidate không có `course_id`. Không có ánh xạ hoặc schema live/approved.
3. **Mentor access:** AC yêu cầu trong scope Mentor, nhưng principal binding, assignment predicate và 403/404 privacy order chưa được xác nhận; current Study guard là Student-only.
4. **Shared projection:** SupportRequest → student, messages/authors, UploadAsset IDs/status/URL chưa có resolver tương thích đã duyệt. #59/#60/#61 không thể tuyên bố response mapping hoàn tất.
5. **Lifecycle/attachments:** SupportStatus và transition set chưa được chốt; #60 vẫn cần thống nhất `attachment refs` với #34/#35/#47, cùng policy gửi reply sau resolve/cancel.
6. **Error wiring:** các DD giữ đúng error codes theo từng catalog row; support paths chưa có runtime allowlist. Current helper trả error `data={}` khi vắng dữ liệu, trong khi guideline kỳ vọng `null`.

### Đánh giá trạng thái

- AC-24 sequence và ownership #60 INSERT / #61 UPDATE: `VERIFIED_STATIC_ONLY` từ catalog, diagram và DDs.
- Runtime: cả #58–#61 `UNWIRED / NOT_FOUND`; không có route/module/test pair.
- Schema/access/response mapping: `SOURCE_REQUIRED`; V1-PILOT chỉ là candidate.
- DD package: mỗi API có 8 sheets và 3 reports; các DD giữ `Draft — Needs Confirmation`.
- Kết quả nhóm: `VERIFIED_WITH_OPEN_QUESTIONS`; cần quyết định các blockers trước khi implementation.
