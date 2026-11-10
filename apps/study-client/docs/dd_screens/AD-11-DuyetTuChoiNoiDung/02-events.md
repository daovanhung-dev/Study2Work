# AD-11 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-11-EV-001` | `Source heading` / EV-01 — Vào detail và tải Content | See source event detail below |
| `AD-11-EV-002` | `Source heading` / EV-02 — Render preview | See source event detail below |
| `AD-11-EV-003` | `Source heading` / EV-03 — Hiển thị metadata | See source event detail below |
| `AD-11-EV-004` | `Source heading` / EV-04 — Nhập lý do từ chối | See source event detail below |
| `AD-11-EV-005` | `Source heading` / EV-05 — Approve | See source event detail below |
| `AD-11-EV-006` | `Source heading` / EV-06 — Reject / request changes | See source event detail below |
| `AD-11-EV-007` | `Source heading` / EV-07 — Rubric evaluation | See source event detail below |
| `AD-11-EV-008` | `Source heading` / EV-08 — Shell, status copy, back and footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

### EV-01 — Vào detail và tải Content

- **Trigger:** route entry bằng AD-10 selection hoặc browser reload; candidate route `/admin/content/:contentId/review`.
- **Input:** numeric `Content.id` → `contentId` route param → path `content_id:int64!` cho #79. Không truyền author/version vì #78 không cung cấp; không tạo query/body ngoài catalog.
- **Expected sequence:** Admin mở item từ queue; GET #79; nhận Content; sau một decision thành công AC-33 dự kiến refresh #78. Quy tắc giữ filter/page/back link chưa được duyệt.
- **Current #79 processing:** shared Bearer/JWT `ADMIN` validation chạy trước parse path và DB. Signed-int64 path invalid/overflow hiện map 404 (catalog mapping); query active row bằng bind parameter. Response mapping kiểm tra đúng requested ID và Content shape. Không filter `PENDING_REVIEW`; không đọc `content_versions`; không commit/mutate.
- **Response:** 200 `ApiEnvelope<Content>` với direct `data`; các field đúng theo `ContentResponse`: `id`, `course_id`, `content_type`, `title`, object `payload`, `status`, nullable `parent_id`, `order`. Không `items`/pagination.
- **Errors/current boundary:** 401 unauthenticated, 403 role denied, 404 invalid/missing/soft-deleted, 500 query/mapping failure (safe envelope + rollback). Network/timeout behavior chưa có client source. Route #78 static được đăng ký trước dynamic #79; local test source có coverage route precedence.
- **State mapping:** valid response có thể cấp dữ liệu Content vào `ready`, nhưng không thể lấp metadata author/version hoặc preview. 404/malformed ID cần not-found/error state; exact UI copy/redirect chưa được định nghĩa.

### EV-02 — Render preview

- **Trigger:** #79 success và `data.payload` có dữ liệu; marker #21–#26.
- **Current behavior:** preview luôn ở empty-state prototype; không `<video>`, iframe, fetch, signed URL, file/object-storage endpoint, SCORM/PDF package parser hay route param binding.
- **API boundary:** #79 chỉ cam kết object `payload` qua Content response; không được suy ra schema media, asset locator, authorization, expiry, sandboxing, decoder hoặc Content-Disposition. Không render HTML trong payload như trusted content.
- **Output:** current UI giữ placeholder; expected behavior phải có payload schema và secure preview contract trước implementation. Loading/failure/unsupported content states chưa được chốt.

### EV-03 — Hiển thị metadata

- **Trigger:** map `data` từ #79 vào preview metadata và field cards #28–#33.
- **Mapping được hỗ trợ:** `data.id` → Content ID; `data.title` → title; `data.course_id` → numeric course ID; `data.content_type` → type nếu UI cần; `data.status` → current logical status; `data.payload`, `data.parent_id`, `data.order` thuộc Content model nhưng screenshot không có field rõ để trình bày.
- **Không mapping:** author/lecturer name, course title, submitted date, review version/revision, rubric status. Không dùng `archived_by` hoặc current user làm author; không lấy timestamp từ file hay audit candidate để giả submitted date.
- **Empty/NULL:** screenshot text `NULL`/`N/A` là literal static; không đại diện null values từ API. Nullable `parent_id` không phải Content ID. API #79 đọc active row có thể trả status không pending; client chưa có status gate.

### EV-04 — Nhập lý do từ chối

- **Trigger:** Admin focus/typing vào #37; current textarea `disabled`.
- **Input contract #81:** JSON `{ "reason": string }`; field required theo API catalog. Current Pydantic model strict `str`, `extra="forbid"`; FastAPI body validation chạy trước view auth. Thiếu field, sai kiểu hoặc extra field trả 422.
- **Current prototype:** không nhập được; label ghi “Tùy chọn”. Đây là discrepancy cần sửa sau khi contract owner chốt required/blank rule.
- **Current source semantics:** empty string được chấp nhận và preserved đúng nguyên văn; không trim, không min/max, không blank-only rule. Không tự thêm client validation/char counter/required policy mới. Catalog không định nghĩa độ dài, reason code, plain-text/HTML rules hay localization.
- **Future event boundary:** #81 chỉ gọi khi Admin xác nhận reject sau form data được phép nhập; giữ nguyên reason string khi gửi trừ khi approved contract đổi. Chống double click/in-flight state, dirty state, confirm dialog, reason validation feedback và focus behavior cần design/implementation decision.

### EV-05 — Approve

- **Trigger:** click #39 sau khi owner policy mở khóa. Hiện button disabled; không có JS handler.
- **Request:** `PATCH /api/v1/admin/content/{content_id}/approve`, Bearer/Admin, numeric signed-int64 path; không body, không query. Không gửi `reason`, `status`, version ID, expected version hay idempotency key ngoài contract.
- **Current server processing:** shared `ADMIN` auth → path validation (#80 malformed/overflow→422) → lock active row → require current status `PENDING_REVIEW` → update sang `APPROVED` → validate direct Content projection → append one audit row with JWT numeric `sub`, previous/new status, `reason=NULL` → commit. Error pada query/update/audit/projection/commit rolls back and returns safe 500; missing/deleted 404; non-pending 422.
- **Response/output:** HTTP 200 `ApiEnvelope<Content>`; direct eight-field Content. AC-33 diagram says `APPROVED/PUBLISHED`; local #80 writes only `APPROVED`. Mentor #52 separately changes `APPROVED ↔ PUBLISHED` under Mentor/course-owner path. Do not report published on #80 success or silently call #52 from Admin UI.
- **Concurrency/retry:** lock protects current row at call time; #79 and #80 have no shared revision token. After successful transition, retry may return 422 because status is no longer pending; API has no idempotency contract. Client retry policy and stale message open.
- **Post-success:** AC-33 expects queue reload. Whether AD-11 stays, returns to AD-10, or preserves filters/history is not source-backed.

### EV-06 — Reject / request changes

- **Trigger:** click #40 after valid required `reason`; currently disabled. “Request changes” and “Reject” are visually one control.
- **Request:** `PATCH /api/v1/admin/content/{content_id}/reject`, Bearer/Admin, path `content_id:int64!`, strict JSON `{reason:string!}`; no other request fields.
- **Current processing:** FastAPI validates JSON model before view; for a valid body shared `ADMIN` auth runs before raw path parsing/DB. Path invalid/overflow→422; active row lock; require `PENDING_REVIEW`; update to `REJECTED`; insert one reason-bearing `content_review_audit_logs` candidate row with numeric JWT `sub`, old/new status and exact body reason; validate direct Content response; commit. Missing/deleted→404; non-pending→422; query/update/decision/projection/commit failure→safe 500 + rollback.
- **Response/output:** 200 `ApiEnvelope<Content>` with Content projection; response does not return reason. Audit physical mapping to migration 011 and pending-state gate are DERIVED; live schema/deployment unverified. #78’s local pending filter will exclude the now rejected row on reload, but AC/catalog queue cardinality still differs from local Page behavior.
- **Semantics:** API represents `REJECTED`, not a separate “revision requested” state. No notification/mentor inbox/correction workflow exists in #81 contract. Do not promise that the author is notified or can resubmit as an effect of this endpoint.
- **Retry/stale:** no revision token/idempotency key; current logical row is evaluated at mutation time. Repeat after success may return 422. UX for 404/422 conflict and preserving entered reason is undecided.

### EV-07 — Rubric evaluation

- **Trigger:** view criteria #44–#47; no user-triggered interaction exists in HTML.
- **Current UI:** three check icons appear selected, while progress says `0/3 tiêu chí được nạp`; bar is static. No rubric fetch, state model, score, checkbox semantics or handler.
- **API boundary:** #79–#81 do not return rubric, criterion result or quality score. No evidence that these criteria are a required approval gate or that Full HD/stereo is an approved rule for every Content type.
- **Outcome:** treat labels as prototype copy, not verified checks. Before implementation decide whether rubric is informational or decision-enforcing, source/version, criterion applicability by `content_type`, authoring/edit permissions and what progress means. Do not block/allow approval based on static ticks.

### EV-08 — Shell, status copy, back and footer navigation

- **Trigger:** shell/breadcrumb/back/notification/footer link click, or display of status badges #7/#11/#16/#20.
- **Current behavior:** five top nav links, back link and footer anchors use `href="#"`; notification has no handler. Breadcrumb/status/RBAC/portal copy is static; no monitoring/auth/rubric/support call.
- **AC navigation:** AC-33 expects queue reload after successful decision, and inventory links AD-11 back to AD-10. Exact success route, history/back fallback, query preservation, focus return, refresh/cache behavior and browser refresh/deep-link behavior remain unspecified/unwired.
- **Errors:** 401/403 route treatment (login vs access denied), session refresh, unauthorized button gating, network retry, trace display and return-to-queue timing have no Study Web source. Do not infer from visible RBAC badge.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
