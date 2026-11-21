---
task_id: "2026-10-24-create-study-api61-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #61

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` (`node` không có trong PATH)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Tách DIRECT contract khỏi candidate schema; không bịa bảng, cột, enum hoặc asset projection; giữ source/runtime boundary.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ nguyên contract catalog dù AC có ý nghĩa khác; dùng matrices và ghi `SOURCE_REQUIRED` cho Content/schema/identity gaps.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: AC-22/AC-33 đã dùng `PENDING_REVIEW` và placement như đề xuất DERIVED; không áp dụng suy đoán của nhóm khác vào AC-24.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo một API DD tiếng Việt cho #61 trong phiên này; lập plan trước khi tạo DD; đọc AC-24 diagram và DD #58–#60; kiểm tra DD ngay sau authoring; sau đó macro-review toàn nhóm #58–#61.
- Canonical contract: `docs/lists/list_api.md` row #61: `PATCH /api/v1/mentor/support/{request_id}/resolve`; Bearer JWT, role Mentor; `request_id:int64!`; không body/query; HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<SupportRequest>`; exact errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-24 direct behavior: `AC_03_MENTOR_TEACHING.drawio` page AC24 places #61 on the YES branch after #60 inserts a SupportMessage; the node says `UPDATE request status = RESOLVED`. The NO branch skips #61 and says keep OPEN. Both branches converge on thread/status refresh.
- Deliverables: one folder `apps/study-server/docs/dd/61_mentor_support_resolve/` with eight registered sheets plus `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md`. Study workflow requires Markdown only; do not create ZIP.

## CURRENT_BEHAVIOR

- Source/config: Current `apps/study-server/app/api/v1.py` has no #58–#61 routes; no support/mentor modules or focused tests exist. Shared auth guard is Student-only. API #61 is `UNWIRED / NOT_FOUND`.
- Schema: Legacy Study DB guide/ERD and `infra/postgres/study-server/DB.sql` have no support request/message model. Checked-in V1-PILOT `support_tickets` has UUID `id`, `status`, `assigned_to_subject_id`, and nullable `resolved_at`; it has no `course_id`. Its statuses are `OPEN`, `IN_PROGRESS`, `WAITING_LEARNER`, `RESOLVED`, `CANCELLED`. V1-PILOT is not proof of live or approved API mapping; `request_id:int64` conflicts with UUID. `support_messages` is a separate immutable candidate and must not be updated by #61.
- Transaction/helper: Current request DB session closes without implicit commit; query helpers do not commit. Caller-owned transaction is a convention for a future write use case, not current API #61 behavior.
- Error envelope: API Guidelines expect `data:null` on error; current helper defaults omitted error data to `{}`. The support path is not wired into `DESIGN_CONTRACT_PATHS`; this is a future wiring discrepancy, not current API behavior.
- Runnable tests: No focused API #61 tests; no tests run because this is a docs-only task.

## SOURCE_TRACE

```text
AC-24 YES decision -> PATCH #61 -> validate Bearer/Mentor and request_id -> verify request belongs to Mentor scope -> read current request/status -> logical UPDATE request status to RESOLVED -> candidate resolved_at timestamp -> reload SupportRequest using the shared #59/#60 projection -> return 200 DESIGN_RESOURCE_UPDATED; AC-24 NO branch does not call #61 and keeps OPEN
```

## PLAN BEFORE DD AUTHORING

1. Preserve the exact catalog method/path, Mentor Bearer requirement, `request_id:int64!`, no body/query, HTTP 200, `ApiEnvelope<SupportRequest>`, and exact five error codes. Do not add `409`, `503`, request fields, or response fields.
2. Trace the AC-24 Draw.io page and its edges: #58 list → #59 detail/thread → #60 reply/`INSERT SupportMessage` → YES calls #61 → status becomes RESOLVED; NO bypasses #61 and keeps OPEN; both end at thread/status refresh. Keep #60 and #61 mutations separate.
3. Use V1-PILOT `support_tickets` only as an explicitly labeled candidate for status/resolved timestamp. Do not write executable SQL or cast UUID to int64. Legacy support model is absent and live schema is unverified.
4. Propose the simplest retry-safe state handling as `DERIVED`: `OPEN` → `RESOLVED`, with a server timestamp in candidate `resolved_at`; a repeated resolve of `RESOLVED` returns the current successful SupportRequest without replacing the original timestamp; a request in another non-resolvable state maps to the catalog's 422 code. Exact status enum/allowed state set remains an open question because only pilot DDL lists members.
5. Keep authorization direct at the logical level (Mentor must have this request in assigned scope); identity binding and physical predicate remain `SOURCE_REQUIRED`. Use catalog's 404 for missing request and 403 for an existing request outside scope; record the enumeration/privacy check-order question rather than choosing silently.
6. Reuse #59/#60 SupportRequest field projection. On success the logical status is RESOLVED and `resolved_at` is populated if the selected schema supports it. Do not synthesize `course_id`, student/message IDs, author profile or attachment metadata; retain the shared response-mapping blockers and refer to #59/#60 projection decisions.
7. Create Request Usage, Query, Mutation, and Response Source matrices in `PLAN_RESULT.md` before filling the eight sheets. Candidate read = one in-scope request/status; candidate write = `support_tickets.status` and `resolved_at`; no `support_messages` write; response reload remains `SOURCE_REQUIRED` pending canonical support model.
8. Use the eight registered template files; record their SHA-256 values and preserve each appendix exactly. Keep `Draft — Needs Confirmation`. No runtime, tests, schema, catalog, diagram or context edits; no ZIP.
9. After authoring, statically verify exact 11-file manifest, front matter, exact catalog request/response/error set, all SupportRequest nested response fields, JSON examples, links/anchors, tables/fences/whitespace, and `git diff --check` for relevant tracked changes plus direct whitespace checks of untracked output.
10. Macro-review #58–#61: preserve #58 list-vs-singleton response conflict; align #59 read and #60/#61 write ownership; ensure #60 only inserts a message and #61 only resolves the request; check status/timestamp semantics, shared Mentor scope, schema/ID, SupportRequest rehydration, attachments and envelope discrepancies. Update connected DD reports/worklogs with findings and keep shared blockers open.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #61 | Method/path | `PATCH /api/v1/mentor/support/{request_id}/resolve` | Catalog + AC-24; DIRECT |
| #61 | Actor/auth | Bearer JWT; role Mentor | Catalog + AC-24; DIRECT |
| #61 | Path | `request_id:int64!` | Catalog; DIRECT |
| #61 | Body/query | None | Catalog; DIRECT |
| #61 | Success | HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<SupportRequest>` | Catalog + AC-24; DIRECT |
| #61 | Errors | 401 auth required; 403 access denied; 404 resource not found; 422 validation error; 500 internal error | Catalog; exact codes DIRECT |
| #61 | Logical mutation | `SupportRequest.status = RESOLVED` | AC-24 YES branch; DIRECT |
| #61 | Timestamp | Set candidate `resolved_at` from server time | Pilot column + logical resolution; DERIVED, needs confirmation |

### Request Usage Matrix

| Request item | Source/use | Mapping/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT; require Mentor role | Principal for request-scope check | Role DIRECT; Mentor guard and subject mapping SOURCE_REQUIRED |
| `request_id` | Required path int64 | Locate one SupportRequest; map to `data.id` | Type DIRECT; pilot UUID key conflicts; malformed/int64 overflow → proposed 422 |
| Body | None | None | DIRECT |
| Query | None | None | DIRECT |
| `X-Trace-Id` | Optional shared header | Propagate/generate into response envelope/header if wired | API Guidelines convention; not an API #61 current behavior |

### Query Matrix

| Query | Type | Candidate fields/source | Predicate/purpose | Evidence/status |
|---|---|---|---|---|
| Q1 — scope/existence/state | Logical SELECT | V1-PILOT `support_tickets.id`, `status`, `assigned_to_subject_id`, `resolved_at` | Find one request, validate Mentor scope, and choose state branch | SOURCE_REQUIRED for physical query; UUID/int64 and subject mapping conflict |
| Q2 — resolve response projection | Logical read/resolver | SupportRequest, UserSummary, SupportMessage, UploadAsset projection reused from #59/#60 | Return the refreshed request/thread after resolution | SOURCE_REQUIRED; no compatible approved physical projection |

### Mutation Matrix

| ID | Operation | Candidate target/fields | Condition/value | Evidence/status |
|---|---|---|---|---|
| M1 | UPDATE SupportRequest | V1-PILOT `support_tickets.status`, `resolved_at` | `OPEN` → `RESOLVED`; server current time for `resolved_at`; repeated RESOLVED is no-op success | Logical status DIRECT; table/column/time/state guard DERIVED candidate only |
| M2 | UPDATE SupportMessage | None | #61 does not insert, alter, or delete messages | N/A by AC-24 boundary; #60 owns message INSERT |

### Response Source Matrix

| Response field | Contract type | Candidate source/transform | Status |
|---|---|---|---|
| Envelope | `ApiEnvelope<SupportRequest>` | Shared envelope convention | Contract DIRECT; message text and data/error serialization need current wiring |
| `data.id` | int64 | Support request ID | SOURCE_REQUIRED; candidate ticket key UUID |
| `data.course_id` | int64 | Support-to-course relation | SOURCE_REQUIRED; pilot support_tickets has no course_id |
| `data.student.*` | UserSummary | Learner identity projection | SOURCE_REQUIRED; numeric ID/name/avatar mapping absent |
| `data.status` | SupportStatus | Set to RESOLVED on successful mutation | Logical value DIRECT; enum/type persistence mapping candidate only |
| `data.messages[]` and nested author/attachments | SupportMessage[] | Reuse #59/#60 thread projection | SOURCE_REQUIRED; #61 must not add/change messages |
| `data.created_at` | date-time | Original request creation time | SOURCE_REQUIRED; candidate pilot field only |
| `data.resolved_at` | date-time? | Candidate `support_tickets.resolved_at` | Field optional DIRECT; set-time and null/omit semantics DERIVED/open |
| `meta`, `traceId` | object, uuid | Envelope / shared trace | Convention; exact runtime projection not yet wired |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #61 runtime | No route/module/test source | `UNWIRED / NOT_FOUND` | DD is design-only. |
| Support persistence and ID | Legacy model absent; pilot uses UUID, contract uses int64 | `DISCREPANCY / SOURCE_REQUIRED` | No production update predicate can be finalized. |
| Mentor authorization | AC-24 scope direct; current auth is Student-only and pilot assignment ID is UUID | `SOURCE_REQUIRED` | Need one approved Mentor subject/scope predicate for #58–#61. |
| State enum/transition | Diagram says YES resolves and NO keeps OPEN; pilot has candidate states | `DIRECT + DERIVED / NEEDS_CONFIRMATION` | Keep OPEN→RESOLVED and idempotent retry as proposal; other state rules require approval. |
| resolved_at | Pilot has nullable timestamp; diagram only names status update | `DERIVED / NEEDS_CONFIRMATION` | Timestamp assignment is reasonable but not directly approved. |
| Response projection | Catalog requires full SupportRequest; #59/#60 mapping incomplete | `SOURCE_REQUIRED` | Cannot claim implementation-ready until shared projection is approved. |
| Error envelope/wiring | Current helper uses `{}` for absent error data; guidelines expect null; support path absent from allowlist | `DISCREPANCY / CONDITIONAL_FUTURE_WIRING` | Do not present as current API #61 behavior. |

## CHANGES

- Files changed: `apps/study-server/docs/dd/61_mentor_support_resolve/` (8 sheets + 3 reports), reports for APIs #58–#60 (macro-review result), worklogs for APIs #58–#61 and refreshed API/DD inventory worklog.
- CONTEXT_UPDATES: None; no runtime/schema/catalog/diagram/context page changed.
- Context pages changed: None.
- Assumptions: State retry and `resolved_at` behavior remain `DERIVED` proposals; unapproved schema, ID, role identity and response mapping remain unresolved.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Deno selector chose #48/#49/#50; all three read in full. | `VERIFIED` |
| AC-24 index/diagram | Parsed AC-24 cells/edges; confirms #60 INSERT → YES #61 → status RESOLVED; NO bypasses #61 and keeps OPEN. | `VERIFIED_STATIC_ONLY` |
| Catalog contract | Row #61 and reusable SupportRequest/SupportMessage/UserSummary/UploadAsset read. | `VERIFIED_STATIC_ONLY` |
| Current source/schema | Router/module/test absence checked; legacy support schema absent; V1-PILOT support tables and UUID/status/timestamp fields inspected. | `VERIFIED_STATIC_ONLY` |
| Related DDs | #58–#60 plan, open questions, responses, mappings and #60 mutation boundary reviewed. | `VERIFIED_STATIC_ONLY` |
| AC-24 macro-review | #58–#61 sequence, contracts, mutation ownership, shared blockers, and report/worklog updates reviewed. | `VERIFIED_WITH_OPEN_QUESTIONS` |
| DD package | Exact 11 Markdown files; eight registered sheet templates retained. | `VERIFIED_STATIC_ONLY` |
| Static formatting/link checks | JSON, relative links/anchors, table widths, fences, trailing whitespace and `git diff --check` checked after final edits. | `VERIFIED_STATIC_ONLY` |
| Inventory refresh | 103 catalog IDs; 61 DD folders, 42 missing, 49 full 11-artifact packs; 12 route+view source pairs, 91 without. | `VERIFIED_STATIC_ONLY` |
| Runtime tests | Not run; docs-only; API #61 is unwired. | `NOT_RUN` |
| Agent context validator | Not run; no context page changed. | `NOT_APPLICABLE` |

## HANDOFF

- Remaining blockers: Canonical support schema/ID, Mentor identity and assignment predicate, SupportStatus enum/state transitions, response projection, and error-envelope integration. #58–#61 are not implementation-ready.
- Next owner/action: Continue the authorized DD creation sequence at API #62. Do not mark the larger DD backlog complete; #62–#103 remain without DD.
