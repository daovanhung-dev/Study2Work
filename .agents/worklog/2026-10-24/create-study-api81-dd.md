---
task_id: "2026-10-24-create-study-api81-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #81 — Từ chối nội dung

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3
- selected worklogs:
  - .agents/worklog/2026-10-24/create-study-api48-dd.md
  - .agents/worklog/2026-10-24/create-study-api49-dd.md
  - .agents/worklog/2026-10-24/create-study-api50-dd.md
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-24/create-study-api48-dd.md
    - carry_forward: Keep catalog contracts direct; distinguish schema candidates from selected source; do not invent fields, tables or identity mappings.
  - path: .agents/worklog/2026-10-24/create-study-api49-dd.md
    - carry_forward: Keep Content as a separate domain from Lecture; retain all eight Content fields and preserve unresolved tree/schema gaps.
  - path: .agents/worklog/2026-10-24/create-study-api50-dd.md
    - carry_forward: AC-22/AC-33 Content lifecycle proposals remain DERIVED; keep physical Content persistence and Mentor/Admin identity SOURCE_REQUIRED.
- additionally reviewed: create-study-api80-dd.md, inventory-study-api-dd-counts.md, DD #78/#79/#80, #52 and #53 related pages.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Continue the one-API-per-session sequence at API #81, author Vietnamese DD, verify immediately, then macro-review connected AC-33 APIs #78–#81.
- Inventory at task start: 103 catalog IDs; 80 DD folders (#01–#80), 23 absent; 68 full 8-sheet + 3-report packages; 12 legacy core-only packs; 12 source route/view pairs and 91 without a pair.
- Canonical contract: docs/lists/list_api.md row #81 declares PATCH /api/v1/admin/content/{content_id}/reject, Bearer JWT/Admin, path content_id:int64!, body reason:string!, no query, ApiEnvelope<Content>, HTTP 200 DESIGN_RESOURCE_UPDATED, and errors 401/403/404/422/500 with corresponding DESIGN_* codes.
- AC-33 directly specifies the REJECT branch: call #81 with reason, update status to REJECTED with review reason, then reload queue #78.
- Keep DD status Draft — Needs Confirmation. Study output is Markdown only; no ZIP.

## CURRENT_BEHAVIOR

- Source/config: Current router has API route markers #01–#09 and #12–#14; there is no #81 route, module or corresponding test. Shared Study auth is Student-only and has no Admin guard. Middleware path allowlist does not include the future #81 path.
- Database artifacts: Legacy Study DDL has no generic Content/review relation. V1-PILOT content_review_decisions is an append-only UUID revision decision log with reason_codes/comment/reviewer/version fields; it is not a direct mapping to catalog Content int64, and live schema is not verified.
- Runnable tests: Not run; documentation-only. No #81 test source found.
- Runtime wiring: API #81 is UNWIRED / NOT_FOUND. Existing 12/103 route/view pairs are source wiring, not a runtime-pass total.

## SOURCE_TRACE

~~~text
Admin pending queue (#78, status=PENDING_REVIEW) -> selected Content detail (#79) -> reject branch with required reason (#81) -> logical status=REJECTED plus review reason -> reload queue (#78)
Current source: no #81 route/module/test -> no runtime persistence or response behavior.
~~~

## PLAN BEFORE DD AUTHORING

1. Preserve exact catalog method/path, Admin Bearer role, path/body fields, absent query, Content response, success and error set. Do not add fields, error codes or business codes.
2. Use the complete AC-33 diagram: queue reads PENDING_REVIEW; #79 reads content/version/author; reject branch sends reason to #81; logical update sets REJECTED and stores review reason; then reload queue.
3. Carry forward #78/#79 open questions about response cardinality, Content schema, revision selection, stale queue item and Admin policy. #81 only has content_id, so do not invent a version ID or optimistic-lock request field.
4. Keep reason:string! as a required JSON body field. No maximum length, trimming, non-empty rule, allowed values or reason taxonomy is declared; record these as unresolved rather than adding validation.
5. Treat status=REJECTED and review-reason persistence as direct logical effects. Physical relation/columns, transaction and whether rejection also appends a separate audit decision remain SOURCE_REQUIRED/open. Do not map to the UUID pilot table.
6. Preserve direct ApiEnvelope<Content> response and all eight Content fields. Do not add reason/reviewer/version/audit fields. Map returned status to REJECTED as a logical post-action projection; mark physical mapping unresolved.
7. Keep exact errors: 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 404 DESIGN_RESOURCE_NOT_FOUND, 422 DESIGN_VALIDATION_ERROR, 500 DESIGN_INTERNAL_ERROR. Required-field request validation can use the catalog 422; stale/non-pending state behavior remains unresolved.
8. Before creating the DD folder, keep the requirement, Request Usage, Query, Mutation and Response Source matrices in this worklog. Create eight registered template sheets and three reports under apps/study-server/docs/dd/81_admin_content_reject/. Use a logical mapping/gap register, no invented DB columns. No runtime/schema/catalog/diagram changes or ZIP.
9. Static-verify the exact contract/code set, all response fields, template suffixes, JSON, links/anchors, tables, fences and whitespace. Then review #78–#81 as a connected group and update their reports/worklogs with cross-API findings. Recount DD inventory after #81.

### API Requirement Matrix

| API ID | Method/path | Actor/auth | Input | Success/response | Errors | Basis/status |
|---|---|---|---|---|---|---|
| #81 | PATCH /api/v1/admin/content/{content_id}/reject | Bearer JWT; Admin | path content_id:int64!; body reason:string!; no query | HTTP 200 DESIGN_RESOURCE_UPDATED; ApiEnvelope<Content> | 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 422 DESIGN_VALIDATION_ERROR; 500 DESIGN_INTERNAL_ERROR | Catalog request/response/errors direct; AC-33 logical rejection effect direct; storage and revision behavior unresolved |

### Request Usage Matrix

| Request item | Use | Query/mutation/response use | Rule/status |
|---|---|---|---|
| Authorization | Authenticate and authorize Admin | Before Content lookup or update | Bearer/Admin direct; Admin guard/claim SOURCE_REQUIRED |
| content_id | Path target identity | Load logical Content; map data.id | Required int64 direct; physical key/revision SOURCE_REQUIRED |
| reason | Rejection explanation | Store logical review reason | Required string direct; length/blank/storage rule unresolved |
| Query | None declared | None | Direct omission |

### Query Matrix

| Query | Purpose | Logical items/condition | Physical source/status |
|---|---|---|---|
| Q1 | Load target Content | content_id, eight Content fields, current status | Logical lookup direct; physical relation/key SOURCE_REQUIRED |
| Q2 | Check review eligibility and revision | Pending state and revision shown by #79 | Pending-review precondition direct; recheck/version selector DERIVED or SOURCE_REQUIRED |
| Q3 | Resolve Admin actor | Authenticated Admin identity for permission/review trace | Role direct; principal/claim mapping SOURCE_REQUIRED |

### Mutation Matrix

| Mutation | Logical target/effect | Condition/value | Audit/transaction | Status |
|---|---|---|---|---|
| M1 | Content status update | Set REJECTED on reject branch | Physical relation/column and transaction SOURCE_REQUIRED | Logical effect direct |
| M2 | Store review reason | Use required request reason | Physical relation/column and response exposure SOURCE_REQUIRED | Logical effect direct |
| M3 | Separate audit/decision append | Not explicitly drawn for reject branch | Do not infer a separate audit write; confirm parity with #80 | SOURCE_REQUIRED/open |

### Response Source Matrix

| Response field | Contract type | Candidate logical source | Status/gap |
|---|---|---|---|
| success | boolean | Envelope branch | Common convention; route absent |
| businessCode | string | Catalog literal | Direct: DESIGN_RESOURCE_UPDATED |
| message | string | Application message | Exact text unspecified; DERIVED |
| data.id | int64 | Logical Content identity | Physical mapping SOURCE_REQUIRED |
| data.course_id | int64 | Stored Content | Physical mapping SOURCE_REQUIRED |
| data.content_type | ContentType | Stored Content | Enum/storage SOURCE_REQUIRED |
| data.title | string | Stored Content | Physical source SOURCE_REQUIRED |
| data.payload | object | Stored Content | Shape/storage SOURCE_REQUIRED |
| data.status | ContentStatus | Post-rejection Content | Logical target REJECTED direct; physical serialization SOURCE_REQUIRED |
| data.parent_id | int64? | Stored Content | Relation/null behavior SOURCE_REQUIRED |
| data.order | int32 | Stored Content | Physical mapping SOURCE_REQUIRED |
| meta | object | Envelope convention | No pagination contract; empty/null alignment unresolved |
| traceId | uuid | Request trace | Convention direct; route absent |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #81 implementation | Current router/module/test scan | UNWIRED / NOT_FOUND | DD is design-only |
| Review reason projection | Diagram stores reason; reusable Content has no reason field | DISCREPANCY / SOURCE_REQUIRED | Do not add reason to response; physical storage and client visibility need decision |
| Rejection audit | #80 explicitly says + audit; #81 says status=REJECTED + review reason | SOURCE_REQUIRED / MACRO_REVIEW | Do not assume identical audit write; confirm review-history parity |
| Revision identity | #78/#79/#81 pass only content_id while diagram reads a version | SOURCE_REQUIRED | Target revision and stale-review behavior unresolved |
| Content persistence | Legacy lacks generic Content; pilot decision log uses UUID revision identity | SOURCE_REQUIRED / NOT_EQUIVALENT_SCHEMA | No physical SQL/table mapping claimed |
| Admin authorization | Catalog requires Admin; current shared helper only supports Student | UNWIRED / SOURCE_REQUIRED | Admin guard and 403/404 policy unresolved |
| Validation/error integration | 422 exists for invalid request, trigger beyond required field is unspecified; middleware path absent | DIRECT_CODE / SOURCE_REQUIRED_RULE | Preserve exact catalog set |

## CHANGES

- Files changed: 11 Markdown files under `apps/study-server/docs/dd/81_admin_content_reject/`; AC-33 reports and corrected Data Mapping links for #78–#80; worklogs for #78–#81; inventory worklog.
- CONTEXT_UPDATES: None; no source, schema, catalog, diagram, manifest or context page changed.
- Existing dirty worktree content was preserved.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| DD package | Exact 11-file set; eight template sheet appendix suffixes match byte-for-byte. | PASS — STATIC |
| Catalog and response | API #81 request, response, success and six error codes match catalog; all eight Content fields present; no reason field added to response. | PASS — STATIC |
| Markdown checks | 4 JSON examples parse; all 37 tables have consistent columns; five fenced blocks balance; 41 local links/anchors resolve; final newline and trailing whitespace checks pass. | PASS — STATIC |
| AC-33 macro-review | #78–#81 reviewed together; group findings recorded in #81 verification report and linked from #78–#80 reports. | REVIEWED_WITH_OPEN_QUESTIONS |
| Inventory | 103 catalog APIs; 81 DD folders, 22 missing, 69 full packages, 12 source route/view pairs, 91 without pair. | PASS — STATIC |
| Application tests/runtime | Not run; documentation-only. #81 remains `UNWIRED / NOT_FOUND`. | NOT_RUN |
| Context validator | No context page or registry changed. | NOT_APPLICABLE |

## HANDOFF

- Remaining blockers: Content/reason schema, reason validation, review revision identity/stale handling, audit parity with #80, Admin guard, middleware/error integration and #52/#53 lifecycle policy.
- Next owner/action: Continue creating DD API #82 with the same plan-before-authoring workflow.

