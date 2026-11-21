---
task_id: "2026-10-24-create-study-api78-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #78 — pending content

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Keep exact catalog/diagram evidence separate from source status; do not use pilot UUID tables as runtime schema; preserve source-required fields.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Generic Content/tree persistence is absent; preserve singular `ApiEnvelope<Content>` as direct contract while explicitly reviewing cardinality and visibility questions.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: AC-33 queue directly reads `status=PENDING_REVIEW`; initial state for POST #50 remains `DERIVED`; no generic Content physical mapping is approved.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Create a Vietnamese Markdown DD for API #78 after recording this plan/matrices; read the full AC-33 diagram page and relevant AC-22 lifecycle page; check the package immediately after authoring. Perform the AC-33 group macro-review only after linked DDs #79–#81 exist.
- Catalog row #78: `GET /api/v1/admin/content/pending`; Bearer JWT, role Admin; optional `type:string`, `course:int64`, `page:int32`; `ApiEnvelope<Content>`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-33 direct flow: Admin opens pending queue → read Content where `status=PENDING_REVIEW` → selects item → API #79 reads content/version/author → decision → #80 approve or #81 reject with reason → reload queue.
- Reusable `Content`: `id:int64`, `course_id:int64`, `content_type:ContentType`, `title:string`, `payload:object`, `status:ContentStatus`, optional `parent_id:int64`, `order:int32`.

## CURRENT_BEHAVIOR

- Source/config: No `/api/v1/admin/content/pending` route, API #78 module, or focused test exists in current Study source. Router declares catalog IDs #01–#09 and #12–#14 only. Shared `validate_current_user_request` requires `STUDENT`, not Admin. Middleware `DESIGN_CONTRACT_PATHS` omits the endpoint; framework validation/unhandled error fallbacks use non-catalog `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR` for a future route outside the allowlist. `error_response()` serializes absent/None error `data` as `{}`.
- Schema artifacts: Legacy `DB.sql`/ERD has no generic Content table or review-queue relation. V1-PILOT `content_blocks` has UUID identity and `lesson_id`/`content_json`, while `content_review_decisions` is an append-only UUID review decision log. These artifacts do not implement the catalog's BIGINT `Content` model or prove live schema availability.
- Runnable tests: No API #78 focused test source found; no application tests run for this docs task.
- Runtime wiring: `UNWIRED / NOT_FOUND`; Admin auth, queue query, response cardinality, persistence and moderation effects are not current runtime behavior.

## SOURCE_TRACE

```text
Admin Bearer principal -> authorize Admin -> parse optional type/course/page -> read logical Content with status=PENDING_REVIEW -> apply optional content-type/course filters and approved pagination -> map catalog Content/list response -> 200 DESIGN_RESOURCE_RETRIEVED -> UI selects item -> API #79 reads content/version/author -> #80 approve or #81 reject -> reload queue
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| List cardinality | API name and `page` query imply a collection; catalog success type is singular `ApiEnvelope<Content>`. API #68 has the same catalog mismatch; #73 explicitly uses `Page<Course>`. | `DIRECT CONTRACT / DISCREPANCY` | Keep direct type in contract tables; document `Page<Content>` only as a proposal requiring catalog correction. |
| Pending state | AC-33 diagram reads `status=PENDING_REVIEW`; #50 initial create and #51 new revision use this state only as a derived proposal. | `DIRECT QUEUE FILTER / DERIVED PRODUCER TRANSITION` | #78 filters the literal pending state; whether every producer/revision enters it remains open. |
| Physical Content source | Legacy schema has no generic Content relation; pilot content blocks/review decisions use UUID/version-specific relations. | `SOURCE_REQUIRED / NOT_VERIFIED` | No executable SQL or physical column mapping can be asserted. |
| Query/pagination rules | `type/course/page` are direct inputs, but enum/casing, page default/size/order and empty-list contract are not fully defined. | `DIRECT INPUT / DERIVED PROPOSAL` | Candidate exact filters, page 1/default, fixed size 20, id ASC and empty page 200 remain provisional. |
| Moderation metadata | AC-33 assigns version/author read to #79 and decisions to #80/#81; Content schema has no author/version/review fields. | `DIRECT BOUNDARY` | Keep #78 projection limited to reusable Content; do not duplicate detail or decision behavior. |
| Deleted/stale queue items | AC-33 does not specify filtering; #53 proposes soft-delete and queue exclusion but remains a draft. | `SOURCE_REQUIRED / DERIVED PROPOSAL` | Queue visibility and revision selection remain open. |
| Admin/error integration | Current guard is Student-only; path absent from design-code allowlist; error helper data defaults to `{}` despite guideline `null`. | `DISCREPANCY / UNWIRED` | Future wiring needs Admin-specific authorization and error-contract integration. |

## PLAN BEFORE DD AUTHORING

1. Preserve exact catalog method/path, Bearer/Admin role, optional query keys/types, `ApiEnvelope<Content>`, HTTP 200 and only the listed 401/403/500 errors. Do not add body, query key, error code or response field.
2. Use full AC-33 page flow: #78 queue → fixed `PENDING_REVIEW` read → #79 content/version/author detail → #80 approval or #81 rejection with reason → reload. #78 is read-only and does not write review/audit state.
3. Map `type` to a candidate exact-match filter on logical `content_type`, and `course` to a candidate exact match on `course_id`; values, casing and physical mapping remain open.
4. Keep query parameter `page` direct. Candidate `page=1`, fixed page size 20, stable `id ASC`, and empty collection 200 may be proposed only for an approved collection response. Do not add `size` or silently wrap the direct `Content` contract.
5. Record the cardinality conflict in Overview, Response, Data Mapping, Error/open questions, with two explicit options: retain singular contract and clarify its list/page semantics, or update catalog to `ApiEnvelope<Page<Content>>`. Recommend Page only as `DERIVED`; do not apply it as direct contract.
6. Use `status=PENDING_REVIEW` as the AC-33 logical predicate. Keep #50 initial-create and #51 revision-to-pending behavior as related proposals, not facts. Do not infer version selector, review author fields or soft-delete marker.
7. Do not write physical SQL against guessed Content/content_blocks tables. Mark logical Q1 and its fields `SOURCE_REQUIRED`; identify pilot UUID tables as incompatible design artifacts and live schema as not verified.
8. Map only reusable Content fields. Author/version/review decision details belong to #79–#81; #78 has no mutation and `07_table.md` must state `N/A — READ-ONLY API`.
9. Keep Admin role as the direct actor requirement; no invented claim, permission table, or reuse of the Student guard. Record current allowlist/error-envelope differences as integration discrepancies.
10. Create the 8 registered template sheets and 3 reports in `apps/study-server/docs/dd/78_admin_content_pending/`, preserve appendix suffixes, and do not create ZIP or edit runtime/schema/catalog/diagram.
11. Requirement, Request Usage, Query, Mutation and Response Source matrices are recorded below before the DD folder is created. Verify the exact 11-file pack, codes, fields, JSON, links/anchors, tables/fences, whitespace and fingerprints; leave AC-33 macro-review pending until #79–#81 exist.

### API Requirement Matrix

| API ID | Contract item | Value | Basis/status |
|---|---|---|---|
| #78 | Method/path | `GET /api/v1/admin/content/pending` | Catalog; DIRECT |
| #78 | Actor/auth | Bearer JWT; Admin | Catalog + AC-33; DIRECT requirement, guard SOURCE_REQUIRED |
| #78 | Query | `type?:string`, `course?:int64`, `page?:int32` | Catalog; DIRECT fields/types, semantics partly open |
| #78 | Body | None declared | Catalog + diagram; DIRECT |
| #78 | Pending predicate | Content `status=PENDING_REVIEW` | AC-33 node n3; DIRECT logical filter |
| #78 | Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Content>` | Catalog; DIRECT, cardinality discrepancy |
| #78 | Errors | 401/403/500 with exact catalog codes | Catalog; DIRECT |
| #78 | Group sequence | Queue → #79 detail → #80 approve or #81 reject → reload | AC-33 nodes/edges; DIRECT |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT; Admin role | Authorize before queue read | Role DIRECT; claim/guard SOURCE_REQUIRED |
| `type` | Optional query string | Candidate filter `Content.content_type = :type` | Field DIRECT; exact match/casing/type values DERIVED/SOURCE_REQUIRED |
| `course` | Optional int64 query | Candidate filter `Content.course_id = :course` | Field DIRECT; physical relation SOURCE_REQUIRED |
| `page` | Optional int32 query | Intended page selection | Field DIRECT; default/size/order depend on response-cardinality decision |
| Body | None | None | DIRECT absence |
| `size`/`sort` | Not declared | No request usage | Do not add to contract; fixed size/order only proposals |

### Query Matrix

| Query | Type | Logical source/fields | Predicate | Purpose/status |
|---|---|---|---|---|
| Q1 | SELECT list, logical only | Content `id`, `course_id`, `content_type`, `title`, `payload`, `status`, `parent_id`, `order` | `status = 'PENDING_REVIEW'`; optional content-type/course filters | AC-33 direct logical read; physical table/columns/joins/order SOURCE_REQUIRED |
| Q1-PAGE | LIMIT/OFFSET candidate | Same logical pending set | `page` plus candidate fixed size 20 | DERIVED only if collection response is approved; singular catalog response cannot express page metadata/items |
| Q2-COUNT | COUNT candidate | Same logical pending set as Q1 | Same fixed status and optional filters | Needed only for candidate PageMeta; SOURCE_REQUIRED pending response contract/schema |

### Mutation Matrix

| Operation | Target | Condition | Fields/effect | Status |
|---|---|---|---|---|
| None | N/A | API #78 is read-only | No INSERT/UPDATE/DELETE, audit or decision write | `N/A — READ-ONLY API` |

### Response Source Matrix

| Response field | Type | Candidate source | Null/cardinality rule | Evidence status |
|---|---|---|---|---|
| `success` | boolean | Envelope branch | true on success, false on error | DIRECT envelope convention |
| `businessCode` | string | Catalog | `DESIGN_RESOURCE_RETRIEVED` or exact listed error code | DIRECT |
| `message` | string | Safe application message | Exact wording unspecified | DERIVED |
| `data` | `Content` | Pending result row(s) | Catalog says one Content; list/page semantics unresolved | DIRECT type / DISCREPANCY |
| `data.id` | int64 | Logical Content identifier | Required per reusable schema | Physical source SOURCE_REQUIRED |
| `data.course_id` | int64 | Logical Content course | Required; can correspond to optional `course` filter | Physical source SOURCE_REQUIRED |
| `data.content_type` | ContentType | Logical Content type; candidate filtered by `type` | Enum/casing unresolved | SOURCE_REQUIRED |
| `data.title` | string | Logical Content title | Required | SOURCE_REQUIRED |
| `data.payload` | object | Logical Content payload | Do not invent members/default | SOURCE_REQUIRED |
| `data.status` | ContentStatus | AC-33 pending queue row | Candidate exact value `PENDING_REVIEW` | Predicate DIRECT; enum/storage SOURCE_REQUIRED |
| `data.parent_id` | int64? | Logical Content hierarchy | Optional null/omit behavior unresolved | SOURCE_REQUIRED |
| `data.order` | int32 | Logical sibling order | Ordering of queue rows not implied | SOURCE_REQUIRED |
| `data.items[]/pagination` | `Page<Content>` candidate only | Q1/Q2 page/count | Not in catalog response | DERIVED; requires contract update |
| `meta` | object | Envelope convention | No approved pagination metadata under current response type | DIRECT envelope; helper convention |
| `traceId` | uuid | Shared trace middleware | Propagated/generated per current convention | Source-backed convention; route absent |
| Error `data` | null by API guideline | Current helper returns `{}` when omitted | Future route discrepancy | DISCREPANCY |

## CHANGES

- Files changed: 11 Markdown files under `apps/study-server/docs/dd/78_admin_content_pending/`; this worklog and `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md` updated.
- CONTEXT_UPDATES: None; no runtime/schema/catalog/diagram changes.
- Context pages changed: None.
- Assumptions: `PENDING_REVIEW` is a direct queue predicate; filter equality, page defaults/size/order and `Page<Content>` remain `DERIVED`; physical Content persistence remains `SOURCE_REQUIRED`.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Deno selector selected #48/#49/#50; all three worklogs were read. | `VERIFIED` |
| Context/registry/skill | Root/global/scope router, context map, docs workflow, manifest, skill and relevant source pages were read; `createDD-markdown` and `docs-dd` are wired to `server-study`. | `VERIFIED_STATIC_ONLY` |
| Catalog/diagrams | #78–#81 catalog rows and reusable Content/Page; AC-33 entire page nodes/edges and AC-22 lifecycle page read. | `VERIFIED_STATIC_ONLY` |
| Related DDs | #49–#53 Content lifecycle and #68 list-response mismatch read; relevant #73 list response pattern checked. | `VERIFIED_STATIC_ONLY` |
| Current source/schema | No #78 route/module/test; Student-only guard; allowlist/error helper behavior; legacy/pilot Content mismatch inspected. Live DB not verified. | `VERIFIED_STATIC_ONLY` |
| Plan-before-authoring | Requirement, Request Usage, Query, Mutation, Response Source matrices recorded above before DD folder creation. | `VERIFIED` |
| Static DD validation | Exact 11-file package; 8/8 appendix parity; 3 JSON examples; 24 core tables; balanced code fences; 38 local links/17 anchors; contract codes and Content fields checked; fingerprints recorded; whitespace clean. | `VERIFIED_STATIC_ONLY` |
| Application tests | Not run; docs-only. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Catalog response cardinality versus list/page intent, Content/version physical schema, page defaults/size/order, enum/type matching, deleted/stale queue visibility, Admin guard and middleware/error integration.
- Next owner/action: Continue with API #79; leave AC-33 #78–#81 macro-review pending until #79–#81 are created.

## CURRENT RECHECK AFTER API #78 — 2026-10-24

- API #78 DD: exact 11-file Markdown package; direct catalog response/cardinality discrepancy retained; runtime remains `UNWIRED / NOT_FOUND`.
- Static validation: 8/8 template appendix suffixes byte-match; 3 JSON examples parse; 24 core tables and six fenced blocks are structurally balanced; 38 local links and 17 anchors resolve; no trailing whitespace. Template SHA-256 `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`; payload SHA-256 `78b54d242f51a2a2c16b415f50715b73b379b6a14de72a394356d20cac9847a6`.
- Application tests not run; no live DB or runtime behavior was verified. AC-33 macro-review remains pending until #79–#81 DDs exist.
- Current catalog/DD totals: 103 unique APIs; 78 DD folders with core sheets, 66 complete 11-file packages, 25 APIs without DD folders (#79–#103), and #01–#12 still lack the three standard reports.
- Programming criterion remains route declaration in `apps/study-server/app/api/v1.py` plus matching `app/modules/**/api_*/view.py`: #01–#09 and #12–#14 (12) match; 91 do not. This is source wiring, not runtime verification.
- Next DD: API #79.

## POST-AUTHORING AC-33 GROUP REVIEW — 2026-10-24

- Reviewed DD #78–#81 together after API #81 was created. The review is document-level; no API contract, source, schema or diagram was changed.
- Group findings: #78 list/page intent conflicts with `ApiEnvelope<Content>` cardinality; #79 version/author read intent is absent from the Content response; #80 `APPROVED/PUBLISHED` and audit intent need reconciliation with separate #52; #81 records `REJECTED` plus reason without an explicit audit append; revision identity, Admin guard, Content persistence and #53 lifecycle policy remain unresolved.
- The fixed `PENDING_REVIEW` predicate means a matching row with updated `REJECTED` state will no longer appear after queue reload, but shared revision identity is not established.
- Corrected local Data Mapping anchors in #78 that did not match the headings; all local links/anchors in #78–#81 now resolve.
- Full findings: `apps/study-server/docs/dd/81_admin_content_reject/VERIFICATION_REPORT.md`.
- API #78 documentation verification is complete; application tests/runtime were not run. Next DD: API #82.
