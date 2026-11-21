---
task_id: "2026-10-25-implement-api63"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #63

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 56 available; selected and read all three; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Reuse the application-level auth/access patterns; local BIGINT DDL and fake DB tests do not prove live schema or Object Storage.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: `query.py` contains SQL constants only; `view.py` owns query parameters and transactions; numeric `content` can map to decimal text only as an explicit local decision.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Trace producer/consumer persistence before coding; preserve checked-in legacy versus V1-PILOT schema boundary and existing dirty changes.
- related_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api62.md`
    - carry_forward: API #62 now returns distinct Student `UserSummary[]` IDs from ACTIVE legacy enrollments; #63's CSV IDs can use those numeric IDs. The exact course ID is not in #63's direct body.
  - path: `.agents/worklog/2026-10-25/implement-api61-mentor-support-resolve.md`
    - carry_forward: Preserve the shared MENTOR guard, signed numeric identity, safe errors, caller-owned commit/rollback and derived local DDL boundary.
- related_designs_reviewed:
  - `apps/study-server/docs/dd/64_mentor_notifications_status/PLAN_RESULT.md` and `OPEN_QUESTIONS.md`: #64 takes `notification_id:int64`; its current Operation response and delivery aggregation are unresolved.
  - `apps/study-server/docs/dd/18_operations/PLAN_RESULT.md` and `OPEN_QUESTIONS.md`: Operation UUID/physical persistence/lifecycle are unresolved; Work Server operations are not a Study source.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement `POST /api/v1/mentor/notifications` for AC-25 using the direct catalog method, path, body field names/types, response schema, HTTP status and exact error set.
- Direct contract: Mentor Bearer JWT; body `recipients:string!`, `title:string!`, `content:int64!`, `channels:string!`; HTTP 202 `DESIGN_OPERATION_ACCEPTED`; `ApiEnvelope<Operation>`; errors 401/403/422/503/500 only.
- Diagram flow: API #62 roster → recipient/title/content selection → API #63 creates Notification + recipients → Push/Email delivery → API #64 reads delivery status. A 202 records acceptance, not completed delivery.
- Local schema boundary: choose the checked-in legacy BIGINT `notifications` table because API #62 supplies BIGINT Student IDs and the Mentor source uses numeric IDs. Do not mix the V1-PILOT UUID learner/delivery model or claim live schema availability.

## CURRENT_BEHAVIOR (PRE-EDIT)

- Source/config: No API #63 route/module/test or notification dispatch provider exists in Study. `DESIGN_CONTRACT_PATHS` lacks the path. The existing email-verification stub only handles API #02 and does not persist jobs.
- Local DDL: `notifications` is BIGINT, one nullable `user_id` per row, `sender_id`, title, text content, optional type, read flag and created timestamp. There is no recipient-group, operation or delivery-status relation. The separate V1-PILOT `notifications`/`notification_deliveries` use UUID learners and IN_APP/EMAIL, so they do not match APIs #62–#64.
- Runnable tests: `.agents/server-study/tests.md` records 615 current full-suite tests after API #62; that is a prior verification snapshot and has not been rerun for API #63.
- Runtime wiring: API #62 is the last wired Mentor endpoint. API #64 and API #18 are design-only; no notification worker/provider is available.

## SOURCE_TRACE (PLANNED)

```text
POST /api/v1/mentor/notifications
  -> FastAPI strict body / shared MENTOR JWT guard
  -> parse CSV Student IDs and channels
  -> verify every recipient is an ACTIVE Student in one course directly owned by Mentor
  -> one legacy BIGINT notification row per recipient, grouped by Operation UUID
  -> one durable QUEUED outbox delivery row per notification/channel
  -> commit all writes atomically
  -> HTTP 202 ApiEnvelope<Operation> + meta.notification_ids for API #64
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Selected local fallback / impact |
|---|---|---|---|
| `recipients` encoding | #62 returns numeric Student IDs; catalog declares only string and no delimiter. | `DERIVED` | Parse ordered, comma-separated positive int64 User IDs; collapse duplicate IDs while preserving first occurrence. |
| Course scope absent from body | AC-25 requires recipients belong to a Mentor-managed course; #63 body has no `course_id`. | `DERIVED` | Preserve direct body and require the entire recipient set to share at least one ACTIVE roster of a directly owned course. Reject a set with no such course as 403; do not add an undocumented body field. |
| `content:int64` versus notification text | Diagram depicts entered content; reusable Notification and legacy DDL use text. | `DERIVED` | Keep the direct int64 request type and store its base-10 representation as notification text; record that free-form message text remains a contract discrepancy. |
| `channels` encoding | Diagram names Push/Email; body is string; no enum values are approved. | `DERIVED` | Parse comma-separated `PUSH` and/or `EMAIL` tokens, case-sensitive, unique, preserving order. |
| Grouping and durable delivery queue | Diagram requires Notification + recipients and asynchronous Push/Email; legacy table is one notification per user and has no queue/status table. | `DERIVED_LOCAL_DDL` | Store one notification row per recipient, group rows with a UUID `operation_id`, and persist per-channel `QUEUED` rows in a new BIGINT delivery-outbox relation. This is a checked-in local migration only, not live schema approval. |
| Operation persistence/status | Reusable Operation is UUID with undefined kind/status enums; no Study Operation table or worker exists. | `DERIVED` | Build `Operation` from the committed batch: UUID id, kind `NOTIFICATION_DISPATCH`, status `QUEUED`, Mentor owner and DB created timestamp. Outbox records enable later polling; no worker is present, so no sent/failed claim is made. |
| API #64 handoff | #64 accepts one BIGINT notification ID; Operation response has UUID and no notification ID. | `DERIVED_RESPONSE_META` | Keep `ApiEnvelope<Operation>` and expose created per-recipient notification IDs in envelope `meta.notification_ids`; #64 can be called per ID. Do not change #64 runtime in this session. |
| Live database and external delivery | Only checked-in DDL and fake-session tests are available; no Push/Email worker/provider exists. | `NOT_VERIFIED_HERE` | Verify endpoint acceptance and durable outbox behavior locally; do not claim live migration, queue worker or provider delivery. |

## IMPLEMENTATION_PLAN

1. DONE — Complete same-type worklog preflight; review the selected API #34/#47/#48 logs and related #58–#62 source/worklogs; read API #63 DD, AC-25 diagram, legacy/V1-PILOT DDL, catalog, and linked #64/#18 DDs.
2. DONE BEFORE CODE — Record the explicit source conflict order and local fallback in this worklog. Preserve the direct catalog body/response/error types; mark all local interpretations `DERIVED` and keep DD status Draft.
3. DONE — Reconcile API #63 DD sheets/reports, catalog row and AC-25 node with CSV encoding, common-owned-course eligibility, int64-to-decimal-text mapping, legacy BIGINT per-recipient notification rows, UUID Operation grouping, QUEUED channel outbox and `meta.notification_ids`; preserve Excel source appendices.
4. DONE — Add one forward-only local migration and matching `DB.sql` artifact for nullable `notifications.operation_id` plus `notification_deliveries(notification_id, channel, status, queued_at, updated_at)`, with minimal FK/check/unique/index constraints. Migration was not applied.
5. DONE — Implement the API module with declarative request/Operation/envelope models, API-specific CSV validation, SQL-only query constants, shared MENTOR auth, common active-course roster check, atomic inserts, standard safe 401/403/422/503/500 responses and rollback on failed write/projection.
6. DONE — Wire only API #63 in `app/api/v1.py` and `DESIGN_CONTRACT_PATHS`; use HTTP 202 and OpenAPI request/response matching direct body/Operation plus response metadata.
7. DONE — Add TestClient coverage for success/write bindings/order, scope denial, invalid/duplicate IDs and channels, auth/role, DB/projection/commit failure, trace/envelope, outbox rows, response IDs and OpenAPI. API #62/#64/#18 runtime behavior was not changed in this task.
8. DONE — Update directly affected server-study context and manifest; review the AC-25 #62→#63→#64 handoff and API #18 boundary.
9. DONE — Run focused API #63 HTTP tests, linked #62 regression, full Study tests, Ruff, route/OpenAPI/import checks, migration/DD static checks, `git diff --check` and context validator. Report live DB/outbox worker limits and preserve existing worktree changes.

## CURRENT_BEHAVIOR (POST-EDIT)

- API #63 is wired in the Study v1 router and `DESIGN_CONTRACT_PATHS`; focused HTTP tests exercise the route and Operation/outbox response using fake DB sessions.
- The accepted transaction writes one legacy BIGINT notification per unique Student ID and one `QUEUED` delivery row per unique channel. A shared generated UUID groups the batch; API #64 handoff IDs are exposed as `meta.notification_ids`.
- The local common-course check enforces direct Mentor ownership plus ACTIVE Student enrollment. Because request body has no course ID, it cannot bind the request to a specific UI-selected course.
- No delivery consumer/provider or live database validation is present. API #63 DD remains `Draft — Needs Confirmation`; local interpretations remain DERIVED.

## CHANGES

- Runtime source: API #63 `models.py`, `query.py`, `validate.py`, `view.py`; route and middleware contract-path wiring.
- Persistence artifacts: nullable notification `operation_id` and the new local `notification_deliveries` table/checks/index in `DB.sql` plus migration 009.
- Tests: new API #63 TestClient suite with 23 cases.
- Contract/docs: catalog #63 row, AC-25 mentor diagram node, reconciled API #63 DD sheets/reports while keeping Draft status and Excel appendices.
- CONTEXT_UPDATES: server-study context registry/pages and project source-status snapshot updated to API #63 and current local verification.
- Context pages changed: `.agents/context-manifest.json`, `.agents/server-study/AGENTS.md`, `apis/declared-routes.md`, `architecture.md`, `core/runtime.md`, `core/database-security.md`, `database.md`, `modules/README.md`, `tests.md`, `.agents/project/source-status.md`.
- Assumptions: All choices above marked DERIVED are a local implementation fallback under the task's conflict-resolution instruction, not approved business policy or evidence of deployment.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3` | 56 available; selected three; all were read. | `VERIFIED_PREFLIGHT` |
| API #63 source/DD and related API review | Diagram/catalog/legacy and pilot DDL, API #62/#64/#18 contracts, existing API #02 provider and API #62 implementation reviewed. | `VERIFIED_STATIC_PRE_EDIT` |
| `uv run pytest tests/modules/mentor/api_63_mentor_notifications_create -q` | 23 passed, one upstream Starlette/httpx TestClient deprecation warning. | `VERIFIED_LOCAL_HTTP` |
| `uv run pytest tests/modules/mentor/api_62_mentor_course_students tests/modules/mentor/api_63_mentor_notifications_create -q` | 41 passed, one upstream warning. | `VERIFIED_LINKED_HTTP` |
| `uv run pytest -q` | 638 passed, one upstream Starlette/httpx TestClient deprecation warning. | `VERIFIED_LOCAL_SUITE` |
| `uv run ruff check app tests` | All checks passed. | `VERIFIED_STATIC` |
| Router/OpenAPI import check | 33 `/api/v1` path templates, 34 operations; API #63 exposes POST in OpenAPI. | `VERIFIED_STATIC` |
| DDL/migration/diagram/DD/manifest check | Migration and DB schema contain operation/outbox artifacts; diagram XML parses; 8 DD sheets remain Draft; 3 JSON examples and relative links validate; manifest registers API #63 source/test. | `VERIFIED_STATIC` |
| `git diff --check` | No whitespace errors. | `VERIFIED_STATIC` |
| Context validator | Node executable unavailable; Deno fallback `--skip-drift` reports existing missing DB Admin context/source paths. Full Deno run reports those plus tracked-source drift from the repository source commit across existing scopes. | `BASELINE_FAILURE_OUTSIDE_SCOPE` |

## HANDOFF

- Remaining limits: API #63 contract remains Draft; local outbox is not a running worker/provider; live database and migration state are unverified. Context validation remains blocked by existing missing DB Admin paths and repository-wide source drift, which were not changed as part of this Study task.
- Next owner/action: After local API #63 verification, continue with the separate API #64 implementation session using `meta.notification_ids` and the local delivery rows as the documented candidate.
