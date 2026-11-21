# AD-07 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-07-EV-001` | `Source heading` / EV-01 — Load course detail | See source event detail below |
| `AD-07-EV-002` | `Source heading` / EV-02 — Return to list | See source event detail below |
| `AD-07-EV-003` | `Source heading` / EV-03 — Navigate to edit | See source event detail below |
| `AD-07-EV-004` | `Source heading` / EV-04 — Navigate to status/delete actions | See source event detail below |
| `AD-07-EV-005` | `Source heading` / EV-05 — Navigate to lessons | See source event detail below |
| `AD-07-EV-006` | `Source heading` / EV-06 — Map successful Course response | See source event detail below |
| `AD-07-EV-007` | `Source heading` / EV-07 — Handle mockup-only metrics, curriculum and standards | See source event detail below |
| `AD-07-EV-008` | `Source heading` / EV-08 — Shell, notification, manual, PDF and footer controls | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### EV-01 — Load course detail

- **Element/trigger:** Route entry (no numbered clickable control); `Load`.
- **Preconditions:** Angular route `/admin/courses/:courseId` is declared; `courseId` is available as a path string. `AdminApiService` obtains the Admin token for the GET #74 request. Browser/deployment execution is not verified.
- **Input:** `courseId` from AD-06 `Course.id` or direct URL. Target API path is an int64 string. There is no query/body; no course code, title or owner name may substitute.
- **Processing:** Follow the target request and current API ordering in section B EV-01. Do not add frontend positive-only validation; current server parser accepts signed int64. API guard runs before path parsing/query. The independent course-management permission check is unresolved.
- **Response handling:** 200 → validate envelope and `data.items`; local current source emits one item and pagination 1/1/1/1; map only source-backed Course fields in EV-06. 401 → authentication/session state; 403 → access-denied state; 404 → invalid/unavailable detail state; 500 → service-error state. Catalog has no 422. Network errors have no agreed client policy.
- **State/result:** Enter `loading` only while an actual request is pending; on success use `ready`. Do not keep the static “waiting” text as if bound. No cache or retry policy is specified.
- **Side effects:** API is read-only. Client cache/stale time is unspecified. No mutation or idempotency key.

### EV-02 — Return to list

- **Element/trigger:** #13 or #15; click.
- **Input:** Current route and optional list-navigation state; no such state is presently stored by this prototype.
- **Processing/result:** In the HTML prototype, `href="#"` does not navigate. The current Angular page has a RouterLink to `/admin/courses`; back-stack behavior and list-state restoration remain open. No API call is inherent in the link; AD-06 owns any subsequent #73 load.
- **Errors:** If access to the destination is denied or the session has expired, shared auth handling applies; no AD-07 redirect rule is established.

### EV-03 — Navigate to edit

- **Element/trigger:** #40; click attempt.
- **Input:** Selected loaded `Course.id` plus current authorization context.
- **Processing/result:** Current button is disabled, so browser emits no click action. Target route proposal `/admin/courses/:courseId/edit` passes the numeric ID to AD-08; AC-32 orders #74 detail before PUT #75. Enablement, editable fields, validation, and return route are owned by AD-08 and remain blocked here.

### EV-04 — Navigate to status/delete actions

- **Element/trigger:** #41; click attempt.
- **Input:** Selected loaded `Course.id`; action choice and policy not established here.
- **Processing/result:** Current button is disabled. Target proposal `/admin/courses/:courseId/actions` passes ID to AD-09, where the user/policy may choose API #76 or #77 after contract approval. Do not issue either mutation from AD-07 or infer confirm/cascade/delete semantics.

### EV-05 — Navigate to lessons

- **Element/trigger:** #42; click attempt.
- **Input:** Current `Course.id` is available in target screen state. API #82 accepts optional `course:int64`; inventory route query is not explicit.
- **Processing/result:** Current button is disabled. `/admin/lessons?course=<Course.id>` is supported by current #82 filter source, but route usage must be approved. API #82 DD still has a catalog `Lesson` vs local `Lesson[]` mismatch. Once approved, AD-12 calls #82; AD-07 does not call it directly.

### EV-06 — Map successful Course response

- **Element/trigger:** Current Angular AD07Page renders after EV-01 success; prototype markers #26–30 cover related fields.
- **Input:** `data.items[0]` per current local singleton source; fields exactly as in API matrix.
- **Processing:** Current page maps title, mentor full name, exact price string, status, thumbnail URL and description from the #74 result. It displays the route's `courseId` string under `ID khóa học`; it does not map `Course.id` to a course-code field. No transformation rule is defined for currency text or status label.
- **Output:** Current page shows those read-only values in `loaded`; API code #74 projection failure is returned as 500. The original prototype's separate course-code field #27 remains unsupported.

### EV-07 — Handle mockup-only metrics, curriculum and standards

- **Element/trigger:** #31–38 and #44–50 on render.
- **Input:** No corresponding fields exist in #74 response/query.
- **Processing/result:** Current `0`, empty module list, ISO/copyright/Capstone claims are static markup. Do not calculate counts or convert those claims into acceptance/validation rules. A future data source and owner-approved definitions are required.

### EV-08 — Shell, notification, manual, PDF and footer controls

- **Element/trigger:** #1–12, #51–56; click/hover/focus where markup allows.
- **Input:** Static anchor/button only.
- **Processing/result:** Anchors point to `#`; notification has no handler. No route, PDF resource, health check, permission result or API effect occurs. Keyboard/focus behavior beyond browser defaults is not implemented in the prototype; accessible behavior belongs to the wired Study Web component.

### Current Study Web source

- `admin.routes.ts` registers `/admin/courses/:courseId`; `AD07Page` calls GET #74 via AD07ApiService/AdminApiService and uses `loading/loaded/error` UI states.
- The AD-07 page has a back RouterLink to AD-06. AD-08, AD-09 and AD-12 action buttons are disabled and have no callers from AD-07.
- `admin-detail-pages.spec.ts` covers the AD-07 request/fields/actions; the focused spec passed 2 tests after the ID label correction. Runtime remains unverified.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
