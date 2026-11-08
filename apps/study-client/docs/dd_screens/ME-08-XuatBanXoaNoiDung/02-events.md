# ME-08 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-08-EV-001` | `ME08-EV-01` / ME08-EV-01 — Mở ME-08 và xác định Content/course context | See source event detail below |
| `ME-08-EV-002` | `ME08-EV-02` / ME08-EV-02 — Load selected Content with GET #49 | See source event detail below |
| `ME-08-EV-003` | `ME08-EV-03` / ME08-EV-03 — Confirm publish using PATCH #52 | See source event detail below |
| `ME-08-EV-004` | `ME08-EV-04` / ME08-EV-04 — Confirm unpublish using PATCH #52 | See source event detail below |
| `ME-08-EV-005` | `ME08-EV-05` / ME08-EV-05 — Confirm deletion using DELETE #53 | See source event detail below |
| `ME-08-EV-006` | `ME08-EV-06` / ME08-EV-06 — Return to ME-06 | See source event detail below |
| `ME-08-EV-007` | `ME08-EV-07` / ME08-EV-07 — Header, breadcrumb, policy and footer links | See source event detail below |
| `ME-08-EV-008` | `ME08-EV-08` / ME08-EV-08 — Render impact, audit and protection copy | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 5. Detailed event specification

### ME08-EV-01 — Mở ME-08 và xác định Content/course context

- **Trigger:** open proposed `/mentor/content/:contentId/actions` from ME-06, or direct route entry.
- **Input:** `contentId` path; expected `courseId` and selected Content from ME-06 route/context. The proposed route only includes Content ID, and there is no current client navigation state.
- **Processing:** parse route ID as an integer candidate without treating a malformed ID as create/new; require an authenticated Mentor session before protected data is shown. Obtain the `courseId` from an agreed navigation contract. If absent, block hydration/mutation; do not guess course from an unscoped Content endpoint because no detail endpoint exists.
- **Output:** `loading` until #49 returns an exact Content; no sample title/status should appear as loaded data. Route resolution and session UX are not wired.
- **Exceptions:** malformed/missing route value and direct-link return behavior have no client contract; API #52/#53 map malformed int64 path to 404 after the shared auth guard.

### ME08-EV-02 — Load selected Content with GET #49

- **Trigger:** route has `contentId` and resolved `courseId`.
- **Request:** `GET /api/v1/mentor/courses/{course_id}/content`, `Authorization: Bearer <token>`, no body/query.
- **Steps:** (1) send course ID only to the course-scoped route; (2) current API authenticates MENTOR and direct owner before Content query; (3) read all active Content rows and validate flat tree; (4) client finds exact `id == contentId`, verifies `course_id`, then maps title/type/status/parent/order; (5) render action context and keep API-provided status raw until status labels are approved.
- **Success:** HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `data:[]` is valid as a course tree but yields `not-found` for a selected Content ID. No `canPublish/canDelete` field exists.
- **Errors:** 401 auth; 403 role/owner; 404 invalid or missing course; 500 query/projection/tree-integrity. No partial list. Exact selected Content absent from a successful collection is a UI not-found result, not a new API code.
- **Side effect/cache:** GET is read-only. Cache policy and request cancellation are not implemented.

### ME08-EV-03 — Confirm publish using PATCH #52

- **Trigger:** explicit user confirmation for publish. In current source HTML the publish button is disabled; the event is a candidate only.
- **Preconditions:** exact Content loaded; Mentor passes server access check; Content transition and readiness policy approved; destructive/public confirmation text and destination behavior agreed.
- **Request:** `PATCH /api/v1/mentor/content/{content_id}/publish`; Bearer JWT; current source body `{ "published": true }`. This body is strict/current-source DERIVED and absent from catalog/AC, so it is not an approved client contract.
- **Current processing:** guard MENTOR → parse Content ID → lock active Content/Course → direct-owner check → require current `APPROVED` (unless already `PUBLISHED`) → change only `contents.status` to `PUBLISHED` → validate Content response → commit. Source does not validate payload/assets/revision beyond status.
- **Success:** 200 `DESIGN_RESOURCE_UPDATED` + Content. Prevent duplicate UI submits while processing, then revalidate #49. The text “Hiển thị cho tất cả học viên” is not proven by the mutation source.
- **Errors:** 401; 403 role/direct owner; 404 invalid/missing/deleted Content; 422 strict-body error or unsupported current status; 500 lookup/update/projection/commit. No 409 or version selector.
- **Retry/partial failure:** repeating the same target returns current Content without another UPDATE in local source. Contract body/idempotency is unapproved. If mutation succeeds but #49 refresh fails, preserve `success-await-refresh` separately from mutation failure.

### ME08-EV-04 — Confirm unpublish using PATCH #52

- **Trigger:** explicit unpublish action if Product approves one. The screenshot has no unpublish button, so there is no current element/click handler.
- **Preconditions/input:** exact Content loaded and currently PUBLISHED; user selected target state `published=false`. Do not implement as a blind toggle because path-only catalog cannot identify intent.
- **Request:** same PATCH path and strict current-source body `{ "published": false }` (DERIVED, not approved).
- **Current processing:** lock active Content/Course → direct-owner check → if already APPROVED return the same row/no-op; otherwise require PUBLISHED → update only status to APPROVED → validate response → commit.
- **Success/errors:** 200 `DESIGN_RESOURCE_UPDATED` + Content; 401/403/404/422/500 as #52. If Content is PENDING_REVIEW, DRAFT, REJECTED or another status, local view rejects 422. This is not the catalog’s finalized lifecycle.
- **Output:** refresh #49. No version is changed and no audit row is written by this handler.

### ME08-EV-05 — Confirm deletion using DELETE #53

- **Trigger:** click Delete then an explicit confirmation step if that UX is approved. Current button is disabled and no confirm dialog exists.
- **Request:** `DELETE /api/v1/mentor/content/{content_id}`, Bearer JWT, no request body/query. Do not add status, course ID, dependency list or version to the body.
- **Current processing:** guard MENTOR → parse ID → lock active Content/Course → direct-owner check → if exact status is PUBLISHED return 422 before child lookup → check for active direct Content child → if one exists return 422 → write `deleted_at=CURRENT_TIMESTAMP` → validate DeleteResult → commit.
- **Success:** 200 `DESIGN_RESOURCE_DELETED`; `data={id,status:"deleted",deleted_at}`. Do not call it a Content `status=DELETED`; current source leaves `contents.status` as-is and filters tombstone via `deleted_at`.
- **Errors:** 401; 403 role/owner; 404 malformed/missing/already-soft-deleted ID; 422 PUBLISHED or active direct child; 500 query/projection/commit. Exact eligibility of other statuses and dependencies beyond direct children is DERIVED/open.
- **After success:** use preserved `courseId` to GET #49, where the tombstone is omitted, then return to ME-06. The DeleteResult itself cannot supply course ID. If #49 refresh fails, report delete success with refresh pending; do not issue automatic DELETE retry because a repeated tombstone lookup returns 404.
- **Non-atomic sequence:** source suggests unpublish PUBLISHED via #52 before delete via #53, but those are separate commits. If delete is later blocked by an active child, Content remains APPROVED. Do not chain both mutations automatically until the lifecycle/policy is approved.

### ME08-EV-06 — Return to ME-06

- **Trigger:** click #37 or return after a completed mutation.
- **Expected input:** preserve `courseId`, route context and optionally selected node ID; refresh #49 before showing the tree after mutation.
- **Current:** CTA is `href="#"`; no router/state/cache exists. No dirty form is present, but confirmation/return semantics for a failed mutation are not defined.
- **Output:** candidate destination `/mentor/courses/:courseId/content` from ME-06 inventory; not a current route implementation.

### ME08-EV-07 — Header, breadcrumb, policy and footer links

- **Trigger:** click #1–#6, #14, #42, #44–#46.
- **Current:** all anchors target `#`; `data-path` is inert metadata in HTML and there is no click handler/router. Profile at #4 is static.
- **Expected:** destination map/course context must come from approved navigation design. These links do not call #49/#52/#53 and must not mutate Content.

### ME08-EV-08 — Render impact, audit and protection copy

- **Trigger:** screen render of #8, #11, #13, #16, #23–#29, #33, #36, #38–#41, #43.
- **Current:** each value is static. #49 returns no impact/audit/environment metrics; #52 does not write audit/version; #53 does not query student progress/submissions/assets.
- **Expected:** no API event can be specified from available contracts. Keep these regions labeled design-only or replace them with approved source-backed copy before implementation.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
