# PLAN_RESULT — Study API #58

## Plan gate

- `primary_task_type`: `coding`; `secondary_task_types`: `test`, `docs`; scope: `server-study`.
- Coding worklog selector: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`; 52 matching worklogs, 3 selected and read, no shortage.
- Prior API patterns reviewed: #34 UploadAsset, #47 create lecture, #48 lecture detail, #54 submissions list. AC-24 linked APIs #59–#61 were reviewed before implementation.
- User direction: “Bạn tự xử lý hợp lý phù hợp nhất và dễ hiểu nhất.” The unresolved items below use a documented, simple fallback.
- Scope: implement only API #58 in this session. Keep Study DD output Markdown-only; do not create ZIP.

## Source priority and conflict resolution

| Priority | Evidence | Finding and decision |
|---|---|---|
| 1. AC-24 diagram | List action and `GET /mentor/support/requests`; diagram output type is singleton `SupportRequest`. | The endpoint/action is a collection, so `SupportRequest[]` is the simplest coherent result; diagram/catalog updated to the collection type. |
| 2. Infrastructure | Legacy Study DB uses BIGINT `users`, `courses`, `uploads`; Mentor APIs use numeric JWT subject and direct `courses.mentor_id`. Legacy DDL has no support tables. Separate V1-PILOT support tables use UUID and lack `course_id`; database context says pilot does not prove runtime availability. | Add a normalized legacy BIGINT support schema and migration 008. Keep the pilot artifact unchanged and do not claim the migration is live. |
| 3. API catalog | #58 declares optional `course_id:int64`, `status:string`, a SupportRequest item, and errors 401/403/500. | Keep query fields; collection response resolves AC-24 list semantics. Add 422 for invalid typed `course_id` so the shared FastAPI validation handler has a declared business code. |
| 4. Simple fallback | No page/size, sort, message limit, or empty behavior exists. | No pagination; empty `data: []`; filters combine with AND; status exact match; request order `created_at DESC,id DESC`; full required `messages[]` in chronological order. |

## Selected API behavior

| Item | Decision | Status |
|---|---|---|
| Method/path | `GET /api/v1/mentor/support/requests` | DIRECT |
| Auth | Bearer JWT; `MENTOR`; numeric subject | DIRECT role + existing Study auth convention |
| Scope | `courses.mentor_id = :mentor_id`; optional requested course must be directly owned | DERIVED from API #46/#49/#54 patterns |
| Query | Optional positive int64 `course_id`, optional string `status`; AND/exact match | Fields DIRECT; predicates DERIVED |
| Response | `ApiEnvelope<SupportRequest[]>`; `data: []` when empty | DERIVED to resolve list conflict |
| Request ordering | `created_at DESC, id DESC` | DERIVED stable order |
| Nested messages | Include all messages; `created_at ASC, id ASC`; no hidden truncation | DERIVED from required reusable field |
| Attachments | Explicit ordered message-upload links; resolve legacy `uploads` under author/course/purpose/status constraints | DERIVED using API #34 metadata |
| Errors | 401, 403, 422, 500; no 404 for missing course filter | Catalog 401/403/500; 422 added fallback |
| Mutability | Read-only; no commit | DIRECT from GET/list behavior |

## Legacy schema fallback

- `support_requests`: BIGSERIAL id; required BIGINT `course_id` and `student_id` FKs; status check `OPEN|IN_PROGRESS|WAITING_LEARNER|RESOLVED|CANCELLED`; `created_at TIMESTAMPTZ`; nullable `resolved_at`.
- `support_messages`: BIGSERIAL id; BIGINT request/author FKs; required content and creation timestamp.
- `support_message_uploads`: message/upload FKs and unique non-negative order; supports `SupportMessage.attachments[]` without embedding URLs in message rows.
- Queries: Q1 joins support request → owning course → student UserSummary. Q2 loads messages and linked uploads in one bulk query for the same Mentor/course/status scope.
- Attachment visibility: author must own upload; upload course must equal request course; `STUDENT` uses `SUBMISSION`, `MENTOR` uses `LECTURE`; status must be `UPLOADED`. A linked but invalid asset is an internal mapping error, not a partial asset.

## Linked API review

- #59 reads one SupportRequest and its thread; it should reuse the selected support tables and the same direct-owner scope.
- #60 inserts SupportMessage and does not resolve the request; its attachment wire format remains within API #60's later implementation/DD review.
- #61 updates status to `RESOLVED` and does not insert a message; transition/idempotency rules remain for its own session.
- This session does not implement #59–#61.

## Implementation plan

1. Update #58 DD, API catalog and AC-24 diagram to record the chosen behavior before runtime changes.
2. Add legacy BIGINT support table DDL and migration 008, without applying it to a live database.
3. Implement Pydantic request/response models; query SQL constants; thin router; read-only view with explicit Mentor guard, course precheck, bulk message/asset projection, safe rollback and envelope.
4. Register exact route in `DESIGN_CONTRACT_PATHS` for design validation/internal errors.
5. Add focused HTTP tests for filters, role/scope, collection/thread/assets, empty result, validation, safe failures, no commit, trace and OpenAPI. Review API #59–#61 interaction.
6. Update server-study context and manifest with route/schema/tests. Update verification report/worklog.
7. Run focused/full Study tests, Ruff, OpenAPI/import checks, `git diff --check`, context validation; report source/migration evidence separately from live behavior.

## Implementation and verification result

- API #58 route, models, query constants, read-only view, exact-path error contract and focused HTTP tests are implemented in the Study Server.
- Full Study Server suite: 550 passed; focused API #58 suite: 12 passed; Ruff passed; OpenAPI exposes 28 API v1 path templates / 29 operations; `git diff --check` passed.
- Agent context validation still reports repository baseline issues in DB Admin and broad source drift. Running with `--skip-drift` leaves only missing DB Admin context/source errors; no Study context reference error was reported.
- The new migration was not applied. Live DB schema, endpoint behavior against a live DB and deployment remain unverified.

## Verification boundary

Checked-in DDL, migration, fake-session HTTP tests and OpenAPI prove local source behavior only. They do not prove live database compatibility, migration application, deployment or real asset URL accessibility.
