# AD-09 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-09-EV-001` | `Source heading` / EV-01 — Load selected Course context | See source event detail below |
| `AD-09-EV-002` | `Source heading` / EV-02 — Select operation | See source event detail below |
| `AD-09-EV-003` | `Source heading` / EV-03 — Confirm status update (#76) | See source event detail below |
| `AD-09-EV-004` | `Source heading` / EV-04 — Confirm delete (#77) | See source event detail below |
| `AD-09-EV-005` | `Source heading` / EV-05 — Cancel, Back and reload | See source event detail below |
| `AD-09-EV-006` | `Source heading` / EV-06 — Shell, policy and footer affordances | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### EV-01 — Load selected Course context

- **Trigger/type:** Enter proposed action route; route/Load event.
- **Preconditions:** Numeric `Course.id` from AD-06 or AD-07; approved Admin authorization; Study Web route/client exists.
- **Inputs:** Path `courseId`. Target GET #74 uses `GET /api/v1/admin/courses/{course_id}`, Bearer JWT, no body/query.
- **Steps:** (1) Read numeric ID from route, never course code. (2) Request #74. (3) Validate API envelope/returned identity under confirmed contract. (4) Render only source-backed fields such as Course ID/title/current status; counters are not in local #74 projection. (5) On failure, select distinct 401/403/404/500/network state; do not show a blank placeholder as if the course loaded.
- **Current result:** No API call, target Course is not selected, current status is static “Chưa xác định”. API #74 local query has no DELETED filter, so a deleted Course can still be returned.

### EV-02 — Select operation

- **Trigger/type:** Native `change` on radio group #25–#27.
- **Input:** Current HTML values `draft`, `archive`, `delete`; default `draft` checked.
- **Current processing:** Browser updates the group's checked radio and `peer-checked` styling; change listener does nothing. No normalized state, request body, confirmation, error or API call is produced.
- **Target processing:** After owner approval, distinguish status branch #76 from delete branch #77. #76 body candidate uses uppercase `status`, not `course_action`; #77 is DELETE with no body. There is no confirmed mapping for `archive`. Do not combine status and delete in one request or choose an unselected operation by default.
- **Outcome:** Selection alone has no server side effect. Confirm remains disabled in current artifact.

### EV-03 — Confirm status update (#76)

- **Trigger/type:** Click/submit Confirm #33 after selecting an approved status choice; current button is disabled and `type=button`.
- **Preconditions:** Course loaded; action-to-status mapping, status enum/casing, transition/readiness/public visibility and suspended learner-access policies approved; AC-32 permission mapped; no status request in flight under an approved client policy.
- **Request:** `PATCH /api/v1/admin/courses/{course_id}/status`, `Authorization: Bearer <JWT>`. Catalog/AC omit body. Local strict candidate only: `Content-Type: application/json`, `{ "status": "DRAFT" | "PUBLISHED" | "SUSPENDED" }`; no reason, metadata, `archive` or delete flag.
- **Server sequence:** (1) FastAPI parses strict body; invalid enum/extra key may produce 422 before view guard. (2) Shared role `ADMIN` guard → 401/403; dedicated AC permission is not checked. (3) Parse signed-int64 path → 422 if invalid. (4) Lock existing course status; query failure → safe 500, absent row → 404. (5) Same target → skip update/audit; otherwise update status/timestamp and append actor/old/new audit row in same transaction. No transition/readiness/enrollment gate. (6) Read Course projection through #74 query and build singleton Page. (7) Commit only after valid projection; all query/audit/mapping/commit failures rollback to safe 500. (8) Return 200 `DESIGN_RESOURCE_UPDATED` with Course page.
- **UI result/errors:** Catalog errors 401/403/404/422/500. No 409 status-transition error is declared. Apply returned status and reload/navigate only according to approved UI policy; current API response Page is local singleton implementation. Same-status success may produce no audit row by current source.
- **Current result:** No status request is made; audit reason is disabled and not part of the candidate API body.

### EV-04 — Confirm delete (#77)

- **Trigger/type:** Click/submit Confirm #33 after selecting approved delete branch; current Confirm disabled.
- **Preconditions:** Course loaded; soft-delete marker, dependency coverage, repeat-delete semantics, deleted visibility/restore, audit requirement and AC-32 permission approved.
- **Request:** `DELETE /api/v1/admin/courses/{course_id}`, `Authorization: Bearer <JWT>`; no body/query. Do not send prototype reason or `permanent=true` flag.
- **Server sequence:** (1) Shared ADMIN auth before raw path/DB → 401/403. (2) Parse signed int64 → 422 invalid path. (3) Lock course excluding status DELETED → 404 missing/already deleted. (4) Check any enrollment and candidate active Content/lesson/quiz/assignment dependencies. (5) Dependency query/projection failure → rollback/500; any dependency → rollback, no mutation, 422 `DESIGN_VALIDATION_ERROR`. (6) Otherwise set `courses.status='DELETED'`, update DB timestamp, construct DeleteResult from returned ID/timestamp, validate, commit. (7) Query/projection/commit failure rolls back to safe 500. (8) Success 200 `DESIGN_RESOURCE_DELETED`, data `{id,status:"deleted",deleted_at}`.
- **Current side effects:** Local fallback is a soft marker; child rows are not changed/deleted; no audit row is written. Timestamp maps DB `updated_at` to `deleted_at`. The blocker set and timestamp/marker choices are `DERIVED`, not approved policy.
- **UI result/errors:** 401/403/404/422/500. Dependency 422 is not a 409 and its predicate/message are local fallback. Repeat DELETE returns 404 currently. After success, GET #73/#74 visibility does not hide DELETED, so exact UI disposition is open.
- **Current result:** Clicking the radio only changes selection; disabled Confirm sends no DELETE. “Permanent delete” text is not supported by local behavior.

### EV-05 — Cancel, Back and reload

- **Trigger/type:** Click Back #14 or Cancel #32; route/reload event after success.
- **Inputs:** Current route/history and numeric Course ID; possible selected action, but no reason draft exists because textarea disabled.
- **Current behavior:** Both anchors navigate to `/admin/courses`. Back label implies AD-07, but that path is AD-06 list. No unsaved guard or state restoration.
- **Target result:** Candidate return to AD-07 with same ID or AD-06 list; inventory links both and AC-32 says reload management. Decide route, whether reload #73 list or #74 detail (or both), filter/page restoration, success notice and whether to close/retain page. Cancel itself must not call mutation API.

### EV-06 — Shell, policy and footer affordances

- **Trigger/type:** Click on nav/notification/breadcrumb/footer; static render.
- **Inputs/current:** Anchor destinations `#`, notification button no handler, policy text only. No session/permission/status monitoring, compliance resource or support destination is bound.
- **Result:** No request or permission decision occurs. Do not synthesize a support/legal route, audit event, retention policy, or monitoring API from copy.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
