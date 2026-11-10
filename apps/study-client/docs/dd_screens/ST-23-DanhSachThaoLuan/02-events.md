# ST-23 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-23-EV-001` | `ST23-EV-01` / ST23-EV-01 — Mở màn hình và xác định Student context | See source event detail below |
| `ST-23-EV-002` | `ST23-EV-02` / ST23-EV-02 — Tải topic list qua API #39 | See source event detail below |
| `ST-23-EV-003` | `ST23-EV-03` / ST23-EV-03 — Parse response, map list and choose empty/ready state | See source event detail below |
| `ST-23-EV-004` | `ST23-EV-04` / ST23-EV-04 — Chọn course filter | See source event detail below |
| `ST-23-EV-005` | `ST23-EV-05` / ST23-EV-05 — Chọn sort order | See source event detail below |
| `ST-23-EV-006` | `ST23-EV-06` / ST23-EV-06 — Chuyển trang | See source event detail below |
| `ST-23-EV-007` | `ST23-EV-07` / ST23-EV-07 — Mở topic/thread sang ST-25 | See source event detail below |
| `ST-23-EV-008` | `ST23-EV-08` / ST23-EV-08 — Tạo chủ đề sang ST-24 | See source event detail below |
| `ST-23-EV-009` | `ST23-EV-09` / ST23-EV-09 — Header, breadcrumb, back and footer navigation | See source event detail below |
| `ST-23-EV-010` | `ST23-EV-10` / ST23-EV-10 — API/auth/network/parse error handling | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### ST23-EV-01 — Mở màn hình và xác định Student context

- **Trigger / loại:** route entry / Load.
- **Element:** page container; inventory route `/student/discussions`.
- **Input:** route location, session/Bearer, optional previous course context from a confirmed caller; current HTML gives none.
- **Điều kiện:** AC-19 expects logged-in Student with permission to participate; concrete course authorization policy unresolved.
- **Xử lý:** (1) resolve route only after Study Web router exists; (2) obtain session through approved auth state; (3) do not derive identity from query or prototype `data-path`; (4) do not set `course_id` without caller/filter decision; (5) initialize list to `loading` only when request begins.
- **Output:** expected ST-23 context; current runtime `UNWIRED`, so no route/session transition verified.
- **Ngoại lệ:** no token/expired token maps to 401 at API boundary if implemented; login redirect and return URL behavior are not specified by ST-23.

### ST23-EV-02 — Tải topic list qua API #39

- **Trigger / loại:** initial load or refresh after approved route/query; GET.
- **Input:** `course_id?:int64`, `page?:int32`, `sort?:string`; `Authorization: Bearer <Student JWT>`; no path/body. Do not send `size`.
- **Xử lý:** (1) serialize only catalog query names; (2) apply parser/default values only after decisions in API #39 open questions; (3) call GET `/api/v1/discussions`; (4) no mutation; (5) retain HTTP/business code; (6) do not add retry/cache/dedupe/timeout policy without source.
- **Output:** catalog success 200 `DESIGN_RESOURCE_RETRIEVED` with `ApiEnvelope<Page<Discussion>>`. Current Student #39 route/module/query/test is `NOT_FOUND`; request is not runnable here.
- **Ngoại lệ:** 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`. Network/timeout is transport error, not new API business code. Catalog has no 400/404/422 for #39.

### ST23-EV-03 — Parse response, map list and choose empty/ready state

- **Trigger / loại:** API #39 response.
- **Input:** `ApiEnvelope<Page<Discussion>>`; `items:Discussion[]`; pagination `{page,size,total,total_pages}`.
- **Xử lý:** (1) check HTTP/business success; (2) validate envelope and page structure against final API schema; (3) use only fields in catalog; (4) do not invent title from `content` because catalog `title` has no DB column; (5) do not assume comments are included because API #39 list-vs-#42 detail boundary is open; (6) `ready` requires a success response with renderable fields; `empty` requires success `items=[]` after empty-page contract is confirmed; (7) set error distinctly for HTTP/transport/parse failure.
- **Output:** expected ready/empty list; current HTML is a static empty-state illustration and cannot be used as API outcome.
- **Ngoại lệ:** missing/invalid required Discussion fields, null course_id/user_id source, unknown status enum, inconsistent PageMeta or malformed JSON are contract/data errors; endpoint-specific client copy is unspecified.

### ST23-EV-04 — Chọn course filter

- **Trigger / loại:** Change/select; expected UI control is absent from both assets.
- **Input:** optional `course_id:int64`; the selected course ID must come from an approved Student course context/control.
- **Xử lý:** (1) do not add filter to current empty-state prototype; (2) when designed, normalize as int64 only according to approved parser; (3) define omitted-course scope and active enrollment access first; (4) send only `course_id` on #39; (5) reset page only if product/API pagination decision requires it; (6) re-render after approved response.
- **Output:** currently no course-filter interaction. API DD’s “only ACTIVE enrollments” and all-enrolled-course scope are DERIVED proposals.
- **Ngoại lệ:** invalid ID, unauthorized course, missing enrollment, global topics and course not found lack mapping; do not assign 403/404/422 without catalog decision.

### ST23-EV-05 — Chọn sort order

- **Trigger / loại:** Change; expected sort selector absent.
- **Input:** API field `sort?:string`; field/direction values unspecified by catalog.
- **Xử lý:** (1) do not send UI labels as raw sort; (2) API #39 DD proposes `created_at_desc` default or `created_at_asc` with ID tie-break, but both are DERIVED; (3) wait for approved allowlist/default; (4) once confirmed, send exact allowlisted string and update list state.
- **Output:** no sort behavior in current HTML; contract not implementable yet.
- **Ngoại lệ:** unsupported sort parse/validation behavior has no catalog 400/422; do not silently claim fallback behavior.

### ST23-EV-06 — Chuyển trang

- **Trigger / loại:** Click page control; absent from source UI.
- **Input:** optional `page:int32`; response has PageMeta `size`, but request has no size parameter.
- **Xử lý:** (1) do not fabricate page buttons/counts in current state; (2) confirm default page, allowed range, response size and out-of-range behavior; (3) serialize `page` only; (4) map server PageMeta to approved paging UI; (5) preserve filter/sort only if route/state contract specifies it.
- **Output:** current screen has no pagination. API DD’s page=1/size20/ceil formula is DERIVED, not approved.
- **Ngoại lệ:** malformed/negative/overflow/out-of-range page has no catalog validation mapping; no retry or size override is defined.

### ST23-EV-07 — Mở topic/thread sang ST-25

- **Trigger / loại:** Click a discussion row/card; no row/card exists in HTML.
- **Input:** selected `discussion_id:int64` would be required by inventory ST-25 route `/student/discussions/:discussionId`; API #39 `Discussion.id` is the logical candidate.
- **Xử lý:** (1) do not navigate from empty fallback; (2) once row design and API mapping are approved, use the returned ID only; (3) route to ST-25 with required ID; (4) ST-25 owns GET #42 and detail/comments resolution, not ST-23.
- **Output:** no current row navigation; expected target ST-25 only.
- **Ngoại lệ:** missing ID, inaccessible/moderated thread and 404/403 masking are unresolved; #39 itself does not declare 404.

### ST23-EV-08 — Tạo chủ đề sang ST-24

- **Trigger / loại:** Click create-topic CTA; CTA is expected by inventory but absent from source HTML.
- **Input:** expected destination `/student/discussions/new`; course context may be needed by ST-24, but no approved handoff contract.
- **Xử lý:** (1) do not insert a button into the static prototype; (2) when approved, navigate to ST-24 and let that screen own form submission; (3) do not call POST #40 from this list event; (4) record API #40’s `content:int64` vs rich-text body conflict for resolution before form implementation.
- **Output:** no create navigation in current UI. No topic is created by #39/ST-23.
- **Ngoại lệ:** enrollment/course selection, unauthorized course, canceled form and create error handling belong to approved ST-24 flow; not inferred here.

### ST23-EV-09 — Header, breadcrumb, back and footer navigation

- **Trigger / loại:** Click visible anchor.
- **Input:** static labels and prototype hrefs; back CTA uses `/student/courses`; header/footer mostly `#`.
- **Xử lý:** (1) treat `href="#"` as placeholder, not route; (2) inventory maps `/student/courses` to ST-08 proposal; (3) confirm Study Web route/auth/back-stack policy before wiring; (4) do not pass IDs or return query absent a contract.
- **Output:** prototype link destinations only; no runtime navigation verified.
- **Ngoại lệ:** direct deep link, missing screen and expired session behavior follow future shared router/auth policy, not this asset.

### ST23-EV-10 — API/auth/network/parse error handling

- **Trigger / loại:** API response or transport failure during EV-02 or filter/page refresh.
- **Input:** catalog statuses/business codes and local transport/parse error.
- **Xử lý:** (1) keep 401 auth failure distinct; (2) keep 403 access denied distinct; (3) keep 500 service failure distinct; (4) transport/timeout and malformed response remain client-side errors, without invented API codes; (5) do not show empty-state copy or static sample records after error; (6) retry/recovery copy waits for shared UX decision.
- **Output:** inventory `error` state; error panel/copy/recovery action not present in HTML and therefore unspecified.
- **Ngoại lệ:** no 400/404/422, retry count, timeout, cache stale policy or partial-load contract is declared by #39 catalog.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
