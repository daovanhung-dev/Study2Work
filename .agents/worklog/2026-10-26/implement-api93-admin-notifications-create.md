---
task_id: "2026-10-26-implement-api93-admin-notifications-create"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["AC-36 APIs #92–#96; Mentor notification dispatch/status #63–#64; Operation tracker #18"]
status: "COMPLETED"
---

# Worklog: Implement Study Server API #93 Admin notification create/send

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 86 coding worklogs available; selected and read all 3; shortage none.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Preserve the dirty worktree; shared ADMIN auth precedes business queries; DDL candidates and fake DB tests do not establish live schema; mark fallbacks DERIVED.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: `query.py` contains SQL constants only, views own transaction orchestration, and strict request validation must keep OpenAPI/catalog boundaries visible.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Keep legacy BIGINT separate from V1-PILOT UUID; only add schema when the approved flow requires it; do not claim checked-in migrations are deployed.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: [AC-36 #92–#96, Mentor #63/#64, Operation #18]
```

## EXPECTED_BEHAVIOR

- Direct API #93: `POST /api/v1/admin/notifications`; Bearer JWT/Admin; JSON `recipients?:int64[]`, `segment?:AudienceSegment`, `title:string!`, `content:string!`, `channels:NotificationChannel[]!`; HTTP 202 `DESIGN_OPERATION_ACCEPTED`; `ApiEnvelope<Notification>`; exact errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 503 `DESIGN_DEPENDENCY_UNAVAILABLE`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-36 diagram: CREATE/SEND → API #93 → logical INSERT Notification + recipients → Push/Email when action is Send → reload. It provides no request action/schedule field or physical audience store.
- Reusable `Notification` requires int64 ID, title/content, channels, status, and created_at; `read_at`/`scheduled_at` are optional. Catalog does not enumerate AudienceSegment, NotificationChannel, or NotificationStatus values.
- Operation tracking prose separately says Admin notification POST returns `Operation`; this conflicts with the API-specific diagram/catalog response and UUID/int64 identities.

## CURRENT_BEHAVIOR (pre-edit)

- Current source composes 54 `/api/v1` templates / 63 operations. API #92 GET exists; API #93 has no route/module/test. The exact `/api/v1/admin/notifications` path is already in `DESIGN_CONTRACT_PATHS` for #92, so POST needs no separate path-pattern entry.
- Shared `validate_current_user_request(..., role="ADMIN")` is used by Admin APIs; no source-backed fine-grained notification-management permission exists.
- Migration 009 and checked-in legacy `DB.sql` provide BIGINT `notifications` with one nullable `user_id` per row, `sender_id`, text content, and optional shared UUID `operation_id`; `notification_deliveries` stores one `PUSH|EMAIL` row per notification/channel with `QUEUED|SENT|FAILED`. This is a local candidate only, not live availability or worker proof.
- Mentor API #63 writes one legacy notification per recipient, groups a batch by UUID `operation_id`, writes one QUEUED outbox row per channel, commits atomically, and returns Operation plus `meta.notification_ids`. API #64 reads a notification ID and sender-scoped status. Do not transfer Mentor course/Student scope or int64 `content` contract to Admin.
- V1-PILOT uses a separate UUID learner notification model. No compatible Admin campaign/recipient association table, segment enum/predicate, Operation store, dispatch worker or provider is source-backed.
- Relevant regression baseline before this task: #63/#64/#92 HTTP tests `65 passed` with one upstream Starlette/httpx deprecation warning. Full suite checkpoint after #92: `1217 passed`.
- The current worktree has 637 changed/untracked entries on `develop`; preserve every prior change. No staging, commit or cleanup.

## SOURCE_TRACE (planned local fallback)

```text
POST raw body/header -> shared ADMIN Bearer/JWT guard -> strict body validation
-> require explicit positive unique recipient IDs; reject undefined segment targeting
-> validate every requested user ID exists -> create one legacy BIGINT notification per recipient
   with one shared UUID operation_id -> create one QUEUED delivery row per recipient/channel
-> validate first Notification projection and full batch metadata -> commit once
-> return HTTP 202 ApiEnvelope<Notification> using first recipient row as data and
   DERIVED meta {operation_id, notification_ids} -> safe rollback/error response
```

No provider call, live schema assumption or schema migration is included. Immediate send is a DERIVED interpretation of CREATE/SEND plus 202 and durable outbox. The returned Notification represents the first recipient row; batch IDs and operation grouping remain separately available in metadata. The generic Operation-response prose remains a recorded discrepancy.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Planned local handling |
|---|---|---|---|
| `Notification` vs `Operation` response | API #93 diagram/catalog say Notification; generic operation-tracking paragraph says Operation with UUID. | `DISCREPANCY / DERIVED_FALLBACK` | Preserve endpoint-specific `ApiEnvelope<Notification>`; return the first recipient row and include shared UUID plus all int64 row IDs in generic envelope metadata by #63 precedent. Keep owner decision open. |
| Audience selector | Both optional; no XOR/segment enum/predicate. | `DERIVED / SOURCE_REQUIRED` | Require exactly one selector. Support explicit `recipients` only; reject `segment` with 422 until its enum and expansion source exist. Reject missing/empty/duplicate recipient arrays. |
| Recipient validity/scope | Legacy `notifications.user_id` FK points to `users`; AC-36 defines no Student/ACTIVE/course rule. | `DERIVED` | Check exact user-ID existence only; do not copy Mentor #63 course roster or add role/status predicates. Unknown IDs map to generic 422 without disclosing which ID failed. |
| Channel and status values | Diagram says Push/Email; DDL/#63 encode `PUSH|EMAIL` and outbox starts `QUEUED`. | `DERIVED` | Accept nonempty unique uppercase PUSH/EMAIL values; persist per recipient/channel; return `QUEUED`. No provider mapping or delivery claim. |
| Content/title validation | Required strings; legacy title is VARCHAR(200), content TEXT; DD proposes nonblank but schema not approved. | `DERIVED` | Reject blank values; preserve submitted strings; apply 200-character title bound from the selected local DDL candidate. No content-size cap is invented. |
| Send/schedule action | Diagram dispatch is conditional on Send but body has no action or schedule. | `DISCREPANCY / DERIVED` | Accept as immediate asynchronous send after durable outbox commit; no draft/schedule path is added. |
| Persistence/grain | Legacy table is per-recipient; migration 009 has UUID grouping and delivery outbox; no Admin campaign relation. | `DERIVED / NOT_VERIFIED_HERE` | One BIGINT notification row per recipient, shared operation UUID, one outbox row per channel. Do not add a table/migration or mix V1-PILOT UUID schema. |
| Fine-grained permission | AC-36 says notification-management permission; current guard supports only ADMIN role. | `SOURCE_REQUIRED / DERIVED` | Enforce shared ADMIN role; do not claim a separate permission check. |
| 503 and acceptance boundary | Catalog includes 503; no trigger. #63 maps DB connection unavailable to 503 and queues durably before 202. | `DERIVED` | DB OperationalError/invalidated connection before commit -> 503; other SQL/projection/commit errors -> 500; rollback partial writes. Return 202 only after one batch commit. |
| Batch response handoff | Direct Notification is singular; CREATE accepts multiple recipients; #96 takes one int64 ID. | `DERIVED / SOURCE_REQUIRED` | `data` is the first created recipient Notification; `meta.notification_ids` lists all created IDs and `meta.operation_id` identifies their group. Keep #18/#96 contract bridge for owner review. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Finish required source precedence review: AC-36 diagram → legacy DB guide/ERD/DB.sql and migration 009 → exact catalog row/reusable schemas/Operation tracking → API #93 DD and connected #92/#96 DD plus Mentor #63/#64 code/tests. Keep the specific versus generic response conflict explicit.
2. Add this worklog and record the complete fallback before touching source. Preserve all current worktree changes.
3. Add API #93 declarative request/normalized/response envelope models. Reuse API #92 `AdminNotificationResponse` so #92/#93 Notification fields and channel/status types stay aligned; represent `segment` opaquely because its schema is undefined.
4. Add API-specific validation after shared ADMIN auth: strict JSON; recipients-only selector; positive signed-int64, nonempty, unique IDs; nonblank title/content; local DDL title limit 200; nonempty unique PUSH/EMAIL channels; reject unsupported/undefined segment, unknown body fields and invalid/null values with catalog 422.
5. Add SQL constants only for exact recipient existence, one legacy Notification insert, and one delivery-outbox insert. Bind all parameters; do not query enrollment, role/status, course, V1-PILOT or an invented segment table.
6. Implement the view: shared ADMIN guard; validation; exact recipient-set check; generate UUID group; loop recipients and channels in input order; validate every returned ID/timestamp; build direct Notification response from the first row plus derived `operation_id`/`notification_ids` metadata; commit only after response validation; rollback safely and map DB unavailability to catalog 503, other failures to 500.
7. Wire async `POST /admin/notifications` in `app/api/v1.py` using raw body so auth precedes JSON parsing; reuse the existing exact middleware path entry; declare body/header, 202 response and exact five catalog errors in OpenAPI.
8. Add HTTP tests for auth-before-body/DB, role denial, body/selector/segment/channel/title/content/range/duplicate cases, recipient existence, multi-recipient × channel inserts, response shape/metadata/trace, all SQL/commit failures, rollback/no early commit, and OpenAPI path/body/errors/count.
9. Update API #93 DD and AC-36 macro-review for the implemented fallback while retaining all open owner questions and `Draft — Needs Confirmation`. Preserve each existing standard/additional template appendix byte-for-byte; add a separate notification-delivery mapping file because outbox is a second table, and keep the recipient mapping explicit about one row per recipient.
10. Update only directly affected `.agents/server-study` and `.agents/project/source-status.md` current route/operation/test counts and add source/test paths to `.agents/context-manifest.json`.
11. Verify focused #93 tests, linked #63/#64/#92/#93 regression, full Study suite, Ruff check/format, exact OpenAPI contract and operation counts, DD appendix/JSON/link/whitespace checks, manifest JSON, `git diff --check`, and Deno context validator. Record any DB Admin-only validator failure without expanding scope.
12. Review the scoped diff and keep all previous dirty work intact; do not stage or commit.

## PRE-CODE CHECKPOINT

- Read root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/worklog/README.md`, and `.agents/server-study/AGENTS.md`, `INDEX.md`, route/runtime/database/security/module/test/workflow pages.
- Ran the exact coding selector and read all three selected worklogs above. No shortage.
- Read API #93's eight standard DD sheets, extra recipient mapping, open questions, plan and verification report; read the API #92/#96 DDs, AC-36 macro-review, `00_AC_API_INDEX.md`, exact AC-36 diagram page and catalog/reusable schemas/Operation paragraph.
- Reviewed legacy BIGINT table/migration 009, separate V1-PILOT boundary, current #63/#64 implementations and tests, API #88 raw-body Admin route pattern, API #92 Notification response model, shared auth/database/response helpers, and current router/middleware.
- Baseline connected #63/#64/#92 HTTP suites pass 65 tests. The plan above is recorded before any API #93 source/test/DD/context file has been edited.


## IMPLEMENTATION_RESULT

- Added the raw-body `POST /api/v1/admin/notifications` route with shared ADMIN authentication before body parsing or recipient queries. Reused API #92 Notification response/channel declarations and the existing exact middleware path pattern.
- Added strict body validation, explicit-recipient existence lookup, per-recipient legacy notification inserts grouped by one UUID, per-recipient/channel `QUEUED` delivery inserts, safe rollback/error mapping, and commit-before-202 behavior. No schema migration or provider call was added.
- Added HTTP tests for authorization order, input fallback rules, recipient lookup, batch transaction/projection/error behavior, and OpenAPI. Updated API #92's global operation-count assertion from 63 to 64 because #93 adds a POST operation to the same path.
- Updated the API #93 DD, added a separate delivery table mapping, retained all owner questions and Draft status, and updated the AC-36 macro-review. Updated only directly relevant Study Server context pages and registered the new source/test files in the manifest.
- The response to API #58 was already reflected in existing worklog/source decisions; no API #58 changes were made in this API #93 task.

## VERIFICATION_RESULT

- Focused API #93 HTTP suite: `26 passed` (one upstream Starlette/httpx deprecation warning).
- Linked #63/#64/#87/#92/#93 regression: `111 passed` (same warning).
- Full Study Server suite: `1243 passed` (same warning).
- Full Ruff lint (`app tests`): passed. Scoped Ruff format for all 8 changed Python files: passed. Repository-wide format check identifies 60 other worktree files that would be reformatted; no broad formatting was applied.
- OpenAPI: 54 `/api/v1` templates / 64 operations; #93 shares #92's path template.
- DD: 13 files; 8 standard appendix suffixes and 2 supplementary mapping suffixes match their templates (10/10); front matter, 52 local links/anchors, 2 fenced JSON examples, newline/whitespace checks pass.
- Context manifest parses and includes #93 module/test paths. `git diff --check` passes.
- `scripts/validate-agent-context.mjs` ran via Deno fallback and returned `AGENT_CONTEXT_INVALID` only for the DB Admin context/source roots missing from this checkout and unavailable baseline `sourceCommit` object. No DB Admin files were changed.
- No live DB, deployment, migration, provider, or owner approval verification was performed.

## FINAL_STATUS

API #93 is implemented and locally verified with a DERIVED fallback. Its DD remains `Draft — Needs Confirmation`; Admin model, audience/channel rules, fine-grained permission, send/schedule semantics, response/Operation bridge, live schema, and provider/worker behavior remain open. Existing worktree modifications were preserved; no files were staged or committed.
