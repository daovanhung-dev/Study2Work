# PLAN_RESULT — Study API #59

## Plan gate

- `primary_task_type`: `coding`; secondary: `docs`, `test`; scope: `server-study`; no cross-scope dependency.
- Coding preflight: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`; 52 matching, 3 selected/read; no shortage.
- Prior patterns reviewed: API #34 UploadAsset, #47 Mentor create, #48 Mentor detail, #55 submission detail, and API #58 support list/current migration.
- User's priority order applied: AC-24 diagram → checked-in infrastructure/current API #58 source → catalog. Unresolved local behavior uses a documented DERIVED fallback under the user's overall task rule.
- Template gate: the registered `DD_API_Template_MD` folder contains all 8 expected sheets; its SHA-256 values are recorded in the prior DD baseline and were re-read for this update.
- Scope is API #59 detail only. API #60/#61 writes remain out of scope; Study DD output remains Markdown-only, with no ZIP.

## API Requirement Matrix

| Item | Contract | Basis/status |
|---|---|---|
| Method/path | `GET /api/v1/mentor/support/{request_id}` | Catalog + AC-24; DIRECT |
| Actor/auth | Bearer JWT; role Mentor | Catalog + AC-24; DIRECT |
| Path | required int64 `request_id` | Catalog; DIRECT |
| Body/query | none | Catalog; DIRECT |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<SupportRequest>` | Catalog/diagram; DIRECT |
| Errors | 401, 403, 404, 500 with catalog business codes | Catalog/diagram; DIRECT |
| Mutability | read-only | GET/detail flow; DIRECT |

## Conflict resolution and selected fallback

| Conflict | Higher-priority evidence | Local resolution/status |
|---|---|---|
| Legacy vs V1-PILOT support model | API #58 now has checked-in legacy BIGINT DDL/migration; pilot uses UUID and no course FK. | Reuse API #58 schema; DERIVED local contract, not live DB proof. |
| Mentor scope | AC-24 scope requirement and current API #58 direct `courses.mentor_id` source. | Shared MENTOR auth plus direct course owner; DERIVED. |
| Missing vs other owner | Catalog exposes 404 and 403; APIs #48/#55 use missing-first then owner check. | Missing → 404, extant other owner → 403; DERIVED. |
| Message visibility/order/bound | #58 selected schema has no `is_internal`; #58 returns full chronological thread; no page/limit in #59 contract. | Return all stored rows, `created_at ASC, id ASC`, full thread, empty `[]`; DERIVED. |
| User/asset projection | API #58 legacy mapping and API #34 upload metadata are now local source. | Reuse numeric users and ordered, scoped UploadAsset resolver; DERIVED. |
| Invalid path | #59 catalog omits 422; API #48 maps malformed int64 path to 404. | Preserve catalog and map malformed/out-of-range ID to 404; DERIVED. |
| Null handling | API #58 response models exclude None. | Omit null `avatar_url`/`resolved_at`; current runtime convention. |

## Query and Mutation Matrix

| Query | Source | Predicate/order | Status |
|---|---|---|---|
| Q1 request detail + Student | `support_requests`, LEFT JOIN `courses` and `users` | `request.id = :request_id`; validate required projections; then check `course.mentor_id = :mentor_id`. | `SOURCE_BACKED_WITH_DERIVED_POLICY`; migration 008/live DB unverified. |
| Q2 conversation + author + assets | `support_messages`, `users`, `support_message_uploads`, `uploads` | request ID and direct owner repeated; asset owner/course/purpose/status restrictions; messages asc by time/id; assets asc by position. | `SOURCE_BACKED_WITH_DERIVED_PROJECTION`; live DB unverified. |
| Mutation | None | API #59 is read-only; no commit. | `N/A`; #60/#61 own writes. |

## Response Source Matrix

| Response group | Source/mapping | Status |
|---|---|---|
| Envelope and trace | shared `success_response`/`error_response`, middleware trace | Current runtime convention |
| Request fields | `support_requests` BIGINT row | DERIVED from API #58 schema |
| Student/author | `users.id/full_name/avatar_url` | DERIVED from API #58 fallback and legacy user table |
| Message fields | `support_messages.id/author_id/content/created_at` | DERIVED from API #58 schema |
| Attachments | `support_message_uploads` → `uploads` public metadata | DERIVED, constrained by API #58 rules |
| Optional fields | omit NULL avatar/resolved timestamp | Current API #58 serialization behavior |

The field-by-field contract remains in [04_Response.md](./04_Response.md); execution order and predicates remain in [05_Data_Mapping.md](./05_Data_Mapping.md).

## Linked API review

- #58 collection uses the same support tables and full-thread projection; #59 uses the single request ID and returns the existing object shape.
- #60 inserts a reply message; #59 performs no write and does not invent the later request attachment payload.
- #61 sets resolution state; #59 only reads and returns the current state/timestamp.
- No #60/#61 implementation or contract change is part of this session.

## Implementation plan

1. Reconcile API #59 DD with API #58's selected local schema and write every unresolved choice as DERIVED before runtime changes.
2. Add response/query models and a raw signed-int64 path parser with catalog-compatible 404 handling.
3. Add SQL-only request and thread/asset constants; use LEFT JOINs to surface broken required relations safely.
4. Implement shared Mentor auth, 404/missing then 403/other owner, full mapping, safe 500 rollback, and read-only response in `view.py`.
5. Wire thin route and exact error-contract template; preserve response and error codes from catalog.
6. Add focused TestClient coverage, then update only affected server-study context/manifest/worklog.
7. Run focused/full suite, Ruff, OpenAPI, source/manifest checks, `git diff --check` and context validator; make no live DB calls.

## Verification boundary

Checked-in DDL, local query source, fake-session HTTP tests and OpenAPI prove local implementation behavior only. They do not prove live schema, migration application, deployed endpoint behavior, private-message policy beyond this fallback, or live asset URL reachability.
