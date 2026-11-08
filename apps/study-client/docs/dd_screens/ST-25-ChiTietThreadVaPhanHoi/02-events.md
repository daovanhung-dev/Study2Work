# ST-25 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-25-EV-001` | `ST25-EV-01` / ST25-EV-01 — Mở màn hình và GET thread | See source event detail below |
| `ST-25-EV-002` | `ST25-EV-02` / ST25-EV-02 — Map response #42 lên thread | See source event detail below |
| `ST-25-EV-003` | `ST25-EV-03` / ST25-EV-03 — Hiển thị lỗi tải thread / unavailable state | See source event detail below |
| `ST-25-EV-004` | `ST25-EV-04` / ST25-EV-04 — Dùng shared header/footer navigation | See source event detail below |
| `ST-25-EV-005` | `ST25-EV-05` / ST25-EV-05 — Lưu/bookmark thảo luận | See source event detail below |
| `ST-25-EV-006` | `ST25-EV-06` / ST25-EV-06 — Like/vote topic hoặc reply | See source event detail below |
| `ST-25-EV-007` | `ST25-EV-07` / ST25-EV-07 — Copy code và mở source URL | See source event detail below |
| `ST-25-EV-008` | `ST25-EV-08` / ST25-EV-08 — Open linked course/material | See source event detail below |
| `ST-25-EV-009` | `ST25-EV-09` / ST25-EV-09 — Mở related discussion hoặc “Xem thêm” | See source event detail below |
| `ST-25-EV-010` | `ST25-EV-10` / ST25-EV-10 — Mentor Office Hour CTA | See source event detail below |
| `ST-25-EV-011` | `ST25-EV-11` / ST25-EV-11 — Đổi thứ tự reply | See source event detail below |
| `ST-25-EV-012` | `ST25-EV-12` / ST25-EV-12 — Reply to a specific comment | See source event detail below |
| `ST-25-EV-013` | `ST25-EV-13` / ST25-EV-13 — Nhập nội dung reply | See source event detail below |
| `ST-25-EV-014` | `ST25-EV-14` / ST25-EV-14 — Formatting toolbar / Markdown help | See source event detail below |
| `ST-25-EV-015` | `ST25-EV-15` / ST25-EV-15 — Gửi reply bằng API #41 | See source event detail below |
| `ST-25-EV-016` | `ST25-EV-16` / ST25-EV-16 — Reload thread sau khi POST #41 thành công | See source event detail below |
| `ST-25-EV-017` | `ST25-EV-17` / ST25-EV-17 — Quay lại ST-23 | See source event detail below |
| `ST-25-EV-018` | `ST25-EV-18` / ST25-EV-18 — Session/access/API/transport and moderation errors | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

Mọi event dưới đây mô tả `EXPECTED` flow; `CURRENT` UI/API không được wire. Catalog/API DD errors chỉ có giá trị theo nguồn đã trích; những trạng thái mẫu/handler riêng trên screenshot chưa phải runtime behavior.

### ST25-EV-01 — Mở màn hình và GET thread

- **Element / loại:** Route lifecycle; không có marker.
- **Điều kiện:** Expected Student signed in và được phép tham gia course discussion theo AC-19; permission predicate chưa có contract cụ thể.
- **Input:** Route `/student/discussions/:discussionId`; `discussionId` dự kiến là `discussion_id:int64!`; Student Bearer token nếu session layer được xây dựng. Param lấy từ route, không từ screenshot.
- **Xử lý:** (1) Route/auth guard hiện chưa tồn tại; (2) không suy user/session từ header mẫu; (3) khi contract được duyệt, kiểm tra parse/path semantics theo catalog; (4) gọi GET #42, không thêm query/body.
- **API:** `GET /api/v1/discussions/{discussion_id}`; Student Bearer; success 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401/403/404/500 theo catalog. Page detail semantics vẫn Draft.
- **Output:** Expected chuyển `loading → ready` khi hợp đồng trả thread; current route/request không tồn tại.
- **Ngoại lệ:** Invalid/missing ID mapping, expired session UX, inaccessible-vs-not-found concealment, network retry và error copy chưa được quyết định. API #42 DD đề xuất malformed ID → 404 nhưng là DERIVED.

### ST25-EV-02 — Map response #42 lên thread

- **Element / loại:** Load/response mapping cho ST25-EL-10…31.
- **Điều kiện:** Có HTTP 200 và response parse hợp lệ.
- **Input:** Catalog `ApiEnvelope<Page<Discussion>>`; `Discussion` và `DiscussionComment[]` reusable schema. Page một thread/direct comments/order là proposal của API #42 DD, chưa approved.
- **Xử lý:** (1) Kiểm tra success/businessCode; (2) đọc `data.items` theo Page contract; (3) ánh xạ logical `id/course_id/content/author/status/comments`; (4) không thể hoàn tất `title` mapping vì physical source thiếu; (5) không suy counts/tags/solution/votes/course/module/related topics từ API; (6) không trình bày một derived proposal như dữ liệu runtime.
- **API:** GET #42 response `Page<Discussion>`; #42 DD đề xuất root + direct ACTIVE comments, `created_at ASC,id ASC`, page metadata 1/1/1/1; các điểm này cần duyệt.
- **Output:** State thread data chưa thể là implementable do required title, visibility, author/profile và Page semantics chưa chốt.
- **Ngoại lệ:** Malformed envelope/required field/author missing mapping chưa có client error UX. API #42 DD đề xuất internal error cho integrity failure, chưa phải implementation.

### ST25-EV-03 — Hiển thị lỗi tải thread / unavailable state

- **Element / loại:** Load result/error transition; marker vùng thread/card tương ứng.
- **Điều kiện:** GET #42 trả error hoặc transport thất bại.
- **Input:** HTTP/business code theo #42: 401, 403, 404, 500; network/browser failure nếu xảy ra.
- **Xử lý:** (1) Preserve catalog code; (2) không lộ raw server detail; (3) 401/403/404/500 phải được phân biệt về data state; (4) copy, retry CTA, login return, back route và moderator messaging chưa có approval; (5) không dùng static HTML sentence như API truth.
- **API:** #42 errors: `DESIGN_AUTHENTICATION_REQUIRED`, `DESIGN_ACCESS_DENIED`, `DESIGN_RESOURCE_NOT_FOUND`, `DESIGN_INTERNAL_ERROR`.
- **Output:** Expected error/unavailable state; exact UI/state handling chưa implementable.
- **Ngoại lệ:** Mất mạng, timeout, malformed JSON và server error không có client retry/telemetry contract.

### ST25-EV-04 — Dùng shared header/footer navigation

- **Element / loại:** Click/link trên ST25-EL-01…07, ST25-EL-39 và ST25-EL-40.
- **Điều kiện:** User activates a navigation/search/profile control.
- **Input:** Screenshot labels/icons; HTML fallback chỉ link `#` trừ link quay list.
- **Xử lý:** (1) Record labels; (2) inventory chỉ xác nhận ST-23 liên quan; (3) không suy route, search, notification, menu, session sign-out hoặc history behavior; (4) link quay list được xử lý riêng EV-17.
- **API:** Không có API ST-25 nào gắn với header/footer controls trong catalog.
- **Output:** Chỉ có visual control; destinations không được xác định từ source hiện tại.
- **Ngoại lệ:** Broken `#`/unknown destinations là prototype limitation, không là runtime error contract.

### ST25-EV-05 — Lưu/bookmark thảo luận

- **Element / loại:** Click ST25-EL-09.
- **Điều kiện:** Screenshot có control; current HTML/runtime không có control.
- **Input:** Discussion ID expected; persisted saved-state source absent.
- **Xử lý:** (1) Ghi nhận visual action; (2) không tạo toggle local/persistent state; (3) không gọi API #41/#42 như mutation thay thế; (4) cần product/API quyết định trước khi viết logic.
- **API:** No catalog endpoint or request/response exists.
- **Output:** `SOURCE_REQUIRED`; no success or rollback state may be asserted.
- **Ngoại lệ:** Ownership, duplicate click, unsave and auth behavior unspecified.

### ST25-EV-06 — Like/vote topic hoặc reply

- **Element / loại:** Click ST25-EL-14 or child action ST25-EL-28.
- **Điều kiện:** Screenshot shows reaction/vote controls; no runtime handler found.
- **Input:** Expected target discussion/comment id and current user; contract not found.
- **Xử lý:** Do not mutate counts locally as canonical data; no toggle, idempotency, authorization or optimistic rollback rule is available.
- **API:** No reaction endpoint in ST-25 catalog; #41 adds a comment only.
- **Output:** Sample counts remain visual-only; action is blocked from implementation.
- **Ngoại lệ:** Repeated click, already-voted, removal and moderation cases have no contract.

### ST25-EV-07 — Copy code và mở source URL

- **Element / loại:** ST25-EL-16/17/27 copy/source controls.
- **Điều kiện:** User activates a code/source control in the populated design.
- **Input:** Visible code or sample URL in PNG; HTML fallback has neither.
- **Xử lý:** No clipboard handler, code payload source, URL allowlist, new-tab policy or external-link behavior exists. Do not treat rendered sample text as fetched course asset.
- **API:** None declared for copy/source controls.
- **Output:** No runtime action can be claimed; retain sample content solely in the visual annotation.
- **Ngoại lệ:** Clipboard permission, unsafe/missing link and copy feedback are unspecified.

### ST25-EV-08 — Open linked course/material

- **Element / loại:** Click ST25-EL-19.
- **Điều kiện:** Screenshot links a course/module lesson; inventory does not define this handoff.
- **Input:** Screenshot-only course/module labels; no `course_id`, `lesson_id` source is mapped by #42.
- **Xử lý:** Do not construct a lesson route from sample label; require a course/lesson contract and authorization policy.
- **API:** #42 returns a Discussion candidate with `course_id`, but no course/module/lesson detail projection. No ST25-linked lesson API is declared.
- **Output:** Destination and payload are `SOURCE_REQUIRED`.
- **Ngoại lệ:** Missing course/lesson/access handling is undefined.

### ST25-EV-09 — Mở related discussion hoặc “Xem thêm”

- **Element / loại:** Click ST25-EL-20 rows or see-more control.
- **Điều kiện:** Related rows exist only in screenshot.
- **Input:** No relation, ranking, discussion IDs or pagination source identified.
- **Xử lý:** Do not query #39 based only on visual placement; #39 is a list API with draft query semantics and this screen does not specify related filter/route contract.
- **API:** No related discussion API/parameter is approved.
- **Output:** Navigation is unverified and disabled from implementable DD.
- **Ngoại lệ:** Missing item, ordering, inaccessible thread and return context are unspecified.

### ST25-EV-10 — Mentor Office Hour CTA

- **Element / loại:** Click ST25-EL-21.
- **Điều kiện:** Screenshot displays booking prompt; inventory/API #41/#42 do not define booking.
- **Input:** Sample mentor/call-to-action only.
- **Xử lý:** No schedule, slot, identity, deep link or service contract exists; do not fabricate one.
- **API:** None in ST-25 catalog.
- **Output:** `SOURCE_REQUIRED`; no booking success state.
- **Ngoại lệ:** Availability, authorization and cancellation semantics undefined.

### ST25-EV-11 — Đổi thứ tự reply

- **Element / loại:** Change ST25-EL-23 sort selector.
- **Điều kiện:** Screenshot shows a selected sort label.
- **Input:** Sample label/options; API #42 catalog defines no query parameter/order.
- **Xử lý:** Do not interpret “most helpful” or selected visual text as an approved sort key; do not reorder #42 comments client-side as canonical behavior.
- **API:** GET #42 has path only; no sort query.
- **Output:** Sorting behavior is `SOURCE_REQUIRED`.
- **Ngoại lệ:** Stable order/tie handling is unresolved; API DD’s chronological proposal remains DERIVED.

### ST25-EV-12 — Reply to a specific comment

- **Element / loại:** Click ST25-EL-28/31.
- **Điều kiện:** User selects a reply action; screenshot does not establish nesting semantics.
- **Input:** Discussion/comment ID, but API #41 path may mean root topic ID or target comment; API DD Q-41-02 is open.
- **Xử lý:** Do not use a comment ID as `discussion_id` or create nested replies until root/direct-child policy is approved. If UI only scrolls/focuses composer, that behavior is not evidenced either.
- **API:** If creating a reply, candidate #41 path/body are fixed by catalog, but target semantics and content mismatch block the request.
- **Output:** Reply target/context cannot be selected from current contract.
- **Ngoại lệ:** Deleted/moderated target, nested reply and permission failures unresolved.

### ST25-EV-13 — Nhập nội dung reply

- **Element / loại:** Input/change ST25-EL-35; avatar/header ST25-EL-32/33.
- **Điều kiện:** Expected permitted Student and open topic; neither runtime auth nor topic state is present.
- **Input:** User-authored string; no API state/cache/session source has been found for current UI.
- **Xử lý:** (1) Keep text local while editing; (2) F07 disallows assumed autosave; (3) required/blank/min/max/trim/normalization rules are not set; (4) do not cast/encode string into catalog `content:int64`; (5) do not derive author from screenshot avatar.
- **API:** No request until #41 content representation is resolved.
- **Output:** Visual draft may be described, but persistence/validation cannot be specified as approved.
- **Ngoại lệ:** Refresh/loss-of-draft, empty text and character-limit errors have no contract.

### ST25-EV-14 — Formatting toolbar / Markdown help

- **Element / loại:** Click ST25-EL-34.
- **Điều kiện:** Toolbar visible in PNG only.
- **Input:** Current selection/cursor and action (bold, italic, inline code, link, list, Markdown help) are visual controls; exact implementation is absent.
- **Xử lý:** No supported Markdown subset, insertion syntax, preview, renderer, sanitizer, attachment rule or HTML storage format is identified. Do not claim a toolbar transforms text in a particular way.
- **API:** No formatting-specific API fields. #41 content mismatch remains.
- **Output:** Tool actions are design-only; generated string cannot be sent under current contract.
- **Ngoại lệ:** Selection loss, malformed markup, pasted unsafe HTML and unsupported syntax policy are unspecified.

### ST25-EV-15 — Gửi reply bằng API #41

- **Element / loại:** Click/Submit ST25-EL-37.
- **Điều kiện:** Expected active Student, permitted thread, valid `discussion_id`, non-empty valid content and no in-flight submit. Content/access validation contracts are still open; screenshot includes enabled-looking CTA but is not runtime evidence.
- **Input:** Path `discussion_id:int64!`; body `{content:int64!}`; Bearer JWT. UI value is a string and cannot safely populate the catalog integer field.
- **Xử lý:** (1) Read UI string without normalization rule; (2) verify no request can be formed until contract approval; (3) if approved later, one local in-flight guard can prevent concurrent double click per inventory; no idempotency key or safe retry is cataloged; (4) send POST only after a confirmed mapping exists; (5) parse exact success/error code, without inventing status codes.
- **API:** `POST /api/v1/discussions/{discussion_id}/comments`; Student Bearer; 201 `DESIGN_RESOURCE_CREATED`; 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`. Response `ApiEnvelope<Page<Discussion>>`; item/page semantics Draft.
- **Output:** Current result is `BLOCKED` before network request. If a future approved implementation receives 201, proceed to EV-16; do not take sample comments/counts as response.
- **Ngoại lệ:** Ambiguous network after server commit can duplicate if blindly retried; API has no idempotency contract. Draft retention, error copy and retry policy are unconfirmed.

### ST25-EV-16 — Reload thread sau khi POST #41 thành công

- **Element / loại:** Automatic follow-up GET #42; thread area ST25-EL-10…31.
- **Điều kiện:** API #41 returned HTTP 201 `DESIGN_RESOURCE_CREATED`; this order comes from AC-19 diagram.
- **Input:** Same `discussion_id` and current Student Bearer session; no query/body.
- **Xử lý:** (1) Issue GET #42 after POST success; (2) validate 200 `DESIGN_RESOURCE_RETRIEVED`; (3) use approved response mapping only; (4) do not increment counters locally; (5) do not resubmit #41 if this reload fails.
- **API:** `GET /api/v1/discussions/{discussion_id}`; errors 401/403/404/500. Page, title, access, visible comments and sort decisions remain open.
- **Output:** Expected latest thread replaces prior rendered data only after valid response; no Study Web query/cache exists now.
- **Ngoại lệ:** POST may have succeeded while reload fails; reconciliation, stale view marker, manual refresh and copy are not specified.

### ST25-EV-17 — Quay lại ST-23

- **Element / loại:** Click ST25-EL-08.
- **Điều kiện:** User selects back-to-discussions action.
- **Input:** Target `/student/discussions` from fallback HTML and inventory-linked ST-23; prior filter/page may be absent.
- **Xử lý:** No current router/history behavior. Expected destination is ST-23 but query/state preservation, browser back and login return are not specified.
- **API:** No mutation; a later ST-23 load could use #39 but list query/access are outside this screen and remain draft.
- **Output:** Expected leave current thread; current static link is not a wired route.
- **Ngoại lệ:** Route missing or session expired has no destination/error UI contract.

### ST25-EV-18 — Session/access/API/transport and moderation errors

- **Element / loại:** Error lifecycle affecting screen states; no dedicated visible marker.
- **Điều kiện:** GET #42/POST #41 returns catalog error, transport fails, or topic is moderated/closed.
- **Input:** Catalog statuses/codes; status enum/allowed state is not defined by API contracts. `moderated/closed` comes from inventory only.
- **Xử lý:** Keep 401/403/404/422/500 mappings as defined for the corresponding API; never add 409/410/429/503 without catalog approval. Mark moderation/closed transition as unresolved; do not infer status from screenshot badge. Preserve original draft on failure only if product approves the retention behavior.
- **API:** #42: 401/403/404/500; #41: 401/403/404/422/500. Both are design-only.
- **Output:** Error/retry/closed/moderated UI is not source-complete. Current HTML fallback alone does not implement these cases.
- **Ngoại lệ:** Timeout after POST, 401 during reload, lost course access and invalid-response behavior need product/API decisions.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
