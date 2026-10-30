---
task_id: "2026-10-24-create-study-api80-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #80 — Phê duyệt nội dung

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` (Node không có trong PATH)
- selected: `.agents/worklog/2026-10-24/create-study-api48-dd.md`, `.agents/worklog/2026-10-24/create-study-api49-dd.md`, `.agents/worklog/2026-10-24/create-study-api50-dd.md`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Preserve the catalog contract; keep absent route/view as `UNWIRED / NOT_FOUND`; do not infer physical Content, version, author, asset or Mentor identity mappings.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Keep Content separate from Lecture; preserve `ApiEnvelope<Content>` and its eight declared fields; label tree, persistence and access proposals `DERIVED` or `SOURCE_REQUIRED`.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: AC-22 and AC-33 Content lifecycle remains unresolved; keep exact catalog error set, distinguish logical effects from physical schema, retain approval/publication ambiguity.
- additionally reviewed: `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md` (latest snapshot after #79) and DD #78, #79, #52 relevant pages.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Refresh the Study API DD/programming inventory and continue the one-API-per-session DD sequence at API #80.
- Inventory at task start: 103 catalog API IDs; 79 DD folders (#01–#79), 24 missing; 67 complete 8-sheet + 3-report packages; 12 legacy core-only folders (#01–#12); 12 source route/view pairs and 91 without a pair.
- Canonical contract/approved DD: `docs/lists/list_api.md` row #80 declares `PATCH /api/v1/admin/content/{content_id}/approve`, Bearer JWT/Admin, required `content_id:int64!`, no body/query, `ApiEnvelope<Content>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, and exactly 401/403/404/422/500 with the matching `DESIGN_*` codes.
- AC-33 directly shows the approve branch followed by `UPDATE status = APPROVED/PUBLISHED + audit`, then reload of the moderation queue. The exact meaning of `APPROVED/PUBLISHED`, relation to Mentor API #52, revision identity and physical audit mapping remain unresolved.
- DD status must remain `Draft — Needs Confirmation`; Study deliverable is Markdown only, no new ZIP.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py` has route markers #01–#09 and #12–#14; matching `view.py` files exist for all 12. There is no #80 route, module or matching test. Shared auth is Student-only; Admin authorization is not implemented. `DESIGN_CONTRACT_PATHS` does not include the #80 path. `error_response()` serializes absent error `data` as `{}`.
- DB artifacts: legacy `infra/postgres/study-server/DB.sql` has no generic Content/review/audit relation. V1-PILOT `content_review_decisions` is an append-only UUID `resource_version_id` decision log with reviewer, decision and optimistic row-version fields; it is not a direct mapping for catalog Content IDs (`int64`) and is not proof of deployed/live schema.
- Runnable tests: Not run; this task is documentation and inventory only. No API #80 test source was found.
- Runtime wiring: API #80 is `UNWIRED / NOT_FOUND`. Current source/wiring count remains 12/103, not a runtime-pass count. Existing scope context marks #08/#09 unverified after merge; #02 uses a stub email dispatcher.

## SOURCE_TRACE

```text
AC-33 Admin opens PENDING_REVIEW queue (#78) -> reads selected Content detail (#79) -> PATCH #80 with content_id -> logical approval status update + audit -> reload queue (#78)
Current Study source: API #80 has no route/module/test -> no runtime DB or response behavior.
```

## PLAN BEFORE DD AUTHORING

1. Preserve the exact catalog method/path, Admin Bearer role, required path, no body/query, `ApiEnvelope<Content>`, success and full error set. Do not add request fields, status codes or business codes.
2. Use AC-33 as direct logical flow evidence: queue reads `PENDING_REVIEW`; #80 approve branch updates `APPROVED/PUBLISHED` plus audit; then queue reload. Do not silently decide whether approval also publishes.
3. Compare AC-22 Mentor API #52, which separately changes publication status. Record the lifecycle conflict as `DISCREPANCY`; keep #52's `published:boolean` and transitions as unapproved DERIVED proposals, not #80 contract.
4. Carry forward #79/#78 unresolved Content and revision identity: the catalog path has only `content_id`, while AC-33 detail reads version/author; no revision ID or expected row version enters #80.
5. Treat logical Content status write and audit/decision append as direct effects, but leave physical relation, columns, transaction, audit payload and version lock `SOURCE_REQUIRED`. Mention V1-PILOT `content_review_decisions` only as a non-equivalent artifact; do not map it to Content BIGINT.
6. Build the API Requirement Matrix plus Request Usage, Query, Mutation and Response Source matrices before creating the DD folder. Keep all eight `Content` fields in the response matrix; no version/author/review metadata is added to the catalog response.
7. Keep errors exactly 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`. The 422 branch is catalog-direct but its trigger is not specified; mark its rule `SOURCE_REQUIRED`/open.
8. Create `apps/study-server/docs/dd/80_admin_content_approve/` with eight registered template sheets and the three standard reports. The seventh sheet is a logical mapping/gap register and must not invent a physical table or column. Preserve template appendix bytes; no runtime/schema/catalog/diagram edits and no ZIP.
9. Static-verify package, exact contract, all response fields, JSON, links/anchors, tables/fences, template suffixes, whitespace and changed-file scope. Do not run application tests. Refresh the inventory worklog to 80 folders, 23 missing, 68 full packages, 12 source-wired APIs and 91 without pairs. AC-33 macro-review remains pending until #81 exists.

### API Requirement Matrix

| API ID | Method/path | Actor/auth | Input | Success/response | Errors | Basis/status |
|---|---|---|---|---|---|---|
| #80 | `PATCH /api/v1/admin/content/{content_id}/approve` | Bearer JWT; role Admin | `content_id:int64!`; no body/query | HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<Content>` | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR` | Catalog direct; AC-33 logical status/audit direct; transition and storage unresolved |

### Request Usage Matrix

| Request item | Use | Query/mutation/response use | Rule/status |
|---|---|---|---|
| Authorization | Authenticate Bearer and require Admin role | Authorize before Content lookup/write | Role direct; Admin principal/guard `SOURCE_REQUIRED` |
| `content_id` | Required path int64 | Select logical Content/review target; map `data.id` | Type direct; physical key/version identity unresolved |
| Body | None declared | None | Direct omission |
| Query | None declared | None | Direct omission |

### Query Matrix

| Query | Logical purpose | Required items/condition | Source/status |
|---|---|---|---|
| Q1 | Load Content selected by `content_id` | Content fields needed for eligibility and response | Logical target direct; physical relation/key `SOURCE_REQUIRED` |
| Q2 | Confirm reviewable state/version | AC-33 queue precondition is `PENDING_REVIEW`; select the revision previously shown by #79 | Pending precondition direct; stale/version selector and lock `SOURCE_REQUIRED` |
| Q3 | Resolve Admin principal/audit actor | Authenticated Admin identity for authorization/audit | Admin role direct; claim mapping and audit identity fields `SOURCE_REQUIRED` |

### Mutation Matrix

| Mutation | Logical target/effect | Condition/value | Audit/transaction | Status |
|---|---|---|---|---|
| M1 | Content review/publication status update | Diagram says `APPROVED/PUBLISHED`; whether approve selects APPROVED only or also PUBLISHED is unresolved | Physical table/column and transaction `SOURCE_REQUIRED` | Logical effect direct; state transition `DISCREPANCY` with #52 |
| M2 | Append approval audit/decision | Audit follows approval branch | Physical relation, fields, revision key and atomicity `SOURCE_REQUIRED`; pilot decision log is not an approved direct mapping | Logical audit effect direct; physical mapping unresolved |

### Response Source Matrix

| Response field | Contract type | Candidate logical source | Status/gap |
|---|---|---|---|
| `success` | boolean | Envelope branch | Envelope convention; API route absent |
| `businessCode` | string | Catalog literal | Direct: `DESIGN_RESOURCE_UPDATED` |
| `message` | string | Application message | Exact text unspecified; `DERIVED` |
| `data.id` | int64 | Approved Content identity | Physical mapping `SOURCE_REQUIRED` |
| `data.course_id` | int64 | Stored Content | Physical mapping `SOURCE_REQUIRED` |
| `data.content_type` | ContentType | Stored Content | Enum/storage `SOURCE_REQUIRED` |
| `data.title` | string | Stored Content | Physical mapping `SOURCE_REQUIRED` |
| `data.payload` | object | Stored Content | Shape/storage `SOURCE_REQUIRED`; do not invent keys |
| `data.status` | ContentStatus | Result after approve | `APPROVED/PUBLISHED` meaning and transition unresolved |
| `data.parent_id` | int64? | Stored Content | Relation/null behavior `SOURCE_REQUIRED` |
| `data.order` | int32 | Stored Content | Physical mapping `SOURCE_REQUIRED` |
| `meta` | object | Envelope convention | No pagination contract; empty/null alignment unresolved |
| `traceId` | uuid | Request trace | Convention direct; route absent |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #80 implementation | Current router/module/test inventory | `UNWIRED / NOT_FOUND` | DD is design-only |
| Approve versus publish | AC-33 says `APPROVED/PUBLISHED`; AC-22 exposes separate Mentor API #52 | `DISCREPANCY` | Cannot finalize status transition or align lifecycle |
| Content/version identity | #78/#79/#80 use `content_id`; AC-33 detail reads version; no revision/expected row version in #80 | `SOURCE_REQUIRED` | Stale review may target a different revision |
| Physical Content/audit storage | Legacy DDL lacks generic Content; pilot decision log uses UUID version identity | `SOURCE_REQUIRED / NOT_EQUIVALENT_SCHEMA` | No SQL/table mapping can be claimed |
| Admin authorization | Catalog requires Admin; current helper only supports Student | `UNWIRED / SOURCE_REQUIRED` | Guard, claim mapping and 403/404 policy unresolved |
| 422 trigger and error serialization | Catalog includes 422; its condition is unspecified; middleware path is not allowlisted and helper defaults error data to `{}` | `DIRECT_CODE / SOURCE_REQUIRED_RULE / DISCREPANCY` | Preserve contract while leaving trigger and future integration open |



## CHANGES

- Files changed: eight template sheets and three reports under apps/study-server/docs/dd/80_admin_content_approve/; this worklog; the current inventory snapshot in inventory-study-api-dd-counts.md.
- CONTEXT_UPDATES: None; no context page, manifest, runtime, schema, catalog or diagram changed.
- Context pages changed: None.
- Assumptions: Keep APPROVED/PUBLISHED and revision/audit storage unresolved; the output is a draft, not an implementation contract.
- Existing dirty files from before this task were preserved.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Deno selector returned #48/#49/#50; all three selected worklogs read; no shortage. | VERIFIED |
| Source and contract review | Catalog #80, full AC-33/AC-22 pages, linked DDs, DDL, router/auth/middleware/response source and Study test context reviewed. | VERIFIED_STATIC_ONLY |
| Exact DD package | Eight sheets plus three reports; 8/8 template appendix suffixes byte-exact. | PASS |
| Catalog and schema coverage | Exact #80 method/path/auth/input/response/success/error set; all eight Content fields represented; no extra DESIGN business code. | PASS |
| Markdown static checks | 3 JSON examples parsed; 35 tables, 4 fenced blocks, 34 local links and 9 anchors validated; final newline and whitespace checks passed. | PASS |
| Template/output fingerprints | Template 3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137; output payload 785dee3860df131ab1343c69a33d0be3d8988974c2edc84f88f422ad86c1e004. | RECORDED |
| Inventory after #80 | 80 DD folders; 68 full packages; 12 legacy core-only; 23 missing (#81–#103); 12 source route/view pairs and 91 without a pair. | VERIFIED_STATIC_ONLY |
| Application tests | Not run; documentation-only and #80 is unwired. | NOT_RUN |
| Context validator | Not run; no context page or registry changed. | NOT_APPLICABLE |
| AC-33 macro-review | Review #78–#81 completed as a document review; unresolved group findings are recorded in API #81's verification report. | REVIEWED_WITH_OPEN_QUESTIONS |

## HANDOFF

- Remaining blockers: APPROVED versus PUBLISHED transition, Content/revision identity and physical audit schema, Admin guard/claim, 422 trigger, stale revision and transaction behavior.
- Next owner/action: Continue at API #81; complete AC-33 macro-review for #78–#81 when #81 DD exists.

## POST-AUTHORING AC-33 GROUP REVIEW — 2026-10-24

- Reviewed DD #78–#81 together after API #81 was created. The review is document-level; no API contract, source, schema or diagram was changed.
- Confirmed #80's state wording and audit intent remain unresolved against separate #52 publication and #81's reason-only reject effect. Revision identity, Admin guard, Content persistence and #53 lifecycle policy are shared open questions.
- Corrected local Data Mapping anchors in #80 that did not match the headings; all local links/anchors in #78–#81 now resolve.
- Full findings: `apps/study-server/docs/dd/81_admin_content_reject/VERIFICATION_REPORT.md`.
- API #80 documentation verification is complete; application tests/runtime were not run. Next DD: API #82.
