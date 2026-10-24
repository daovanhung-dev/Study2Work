---
task_id: "2026-10-24-create-study-api53-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #53 — Xóa nội dung Mentor

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `available:73`, `selected:3`, `status:READY`, shortage `none`.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Preserve contract/source separation; Mentor identity and assignment remain SOURCE_REQUIRED; keep Content separate from Lecture; use Markdown-only Study output.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: AC-22 tree endpoint returns singular Content in catalog; Content schema and physical mapping remain unresolved; do not guess children response shape.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Create Content body uses course_id/content_type/title/payload; PENDING_REVIEW and root/order are DERIVED proposals; no compatible generic Content table is present.
  - path: `.agents/worklog/2026-10-24/create-study-api51-dd.md` (related API)
    - carry_forward: AC-22 update says Content + version; request body/version lifecycle remain derived or source-required; preserve version history unless approved otherwise.
  - path: `.agents/worklog/2026-10-24/create-study-api52-dd.md` (related API)
    - carry_forward: Publish/unpublish input and transitions remain DERIVED; AC-33 approval versus publication is ambiguous; #52 must remain the publication-state owner.
  - path: `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`
    - carry_forward: Catalog contains 103 IDs; after #52, #53 is the next DD; source implementation remains 12/103.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Create a Vietnamese, source-traceable API #53 DD after recording this plan; then static-verify the DD and macro-review linked APIs #49–#53 against AC-22/AC-33.
- Canonical contract: `docs/lists/list_api.md` row #53: `DELETE /api/v1/mentor/content/{content_id}`, Mentor Bearer JWT, `path{content_id:int64!}`, no declared body/query, `ApiEnvelope<DeleteResult>`, HTTP 200 `DESIGN_RESOURCE_DELETED`, and exactly 401/403/404/422/500 with their catalog `DESIGN_*` codes. `DeleteResult` is `id:int64`, `status:"deleted"`, `deleted_at:date-time`.
- Diagram: AC-22 requires Mentor permission to manage the course and shows DELETE/soft delete Content followed by reload of the content tree. It does not define dependency criteria, physical tombstone fields, status gate, cascade behavior, or idempotency. AC-33 reads PENDING_REVIEW content/version/author, sets APPROVED/PUBLISHED + audit on approval, or REJECTED + reason; approval/publication relation remains ambiguous.

## CURRENT_BEHAVIOR

- Source/config: No `/api/v1/mentor/content` route, API #53 module, or API #53 test exists in current Study source. Current source search returned no match under `apps/study-server/app` or `apps/study-server/tests`.
- Schema: Legacy `infra/postgres/study-server/DB.sql` has no generic Content table. V1-PILOT `content_blocks` uses UUID `id`, `lesson_id`, `block_type`, and `content_json`; it is not the catalog BIGINT Content model. No compatible Content soft-delete field or dependency table is source-backed; live schema is unverified.
- Runnable tests: No API #53 tests exist; this is documentation-only and application tests will not be run.
- Runtime wiring: API #53 is `UNWIRED / NOT_FOUND`; Mentor principal/assignment mapping is not present in the Study runtime.

## SOURCE_TRACE

```text
Mentor Bearer principal -> DELETE content_id -> load logical Content and course permission -> check supported direct-child dependency -> soft-delete eligible leaf Content -> return DeleteResult -> AC-22 client reloads content tree
```

Physical tables, soft-delete columns, Mentor identity, full dependency graph and review-audit storage remain `SOURCE_REQUIRED`.

## PLAN BEFORE DD AUTHORING

1. Preserve the exact method/path/auth/path/body/query/response/status/error contract from catalog row #53 and AC-22; do not add fields or business codes.
2. Use AC-22 as direct evidence for logical DELETE/soft delete and tree reload. Use AC-33 only for the content review states/history and record that its approval node conflates APPROVED/PUBLISHED.
3. Infer only the direct child relationship made explicit by reusable `Content.parent_id`: a non-deleted Content whose `parent_id` equals the target is the supported dependency candidate. On dependency, propose catalog 422 and no mutation; do not cascade-delete or reparent children. Label the behavior `DERIVED`; physical query and deleted-record predicate are `SOURCE_REQUIRED`.
4. Propose that PUBLISHED content must first be unpublished through #52 before deletion; this keeps publication state owned by #52 and is `DERIVED`, not direct diagram behavior. Other review statuses do not gain invented transitions; deletion remains a separate soft-delete marker and preserves Content/review/version history. Confirm whether pending/rejected/approved items may be deleted and whether published deletion needs this gate.
5. Treat soft-deleted/missing targets as unavailable and map to catalog 404 as a proposal; malformed/non-positive IDs map to the declared 422 only if input validation is required. Keep exact error set and leave error precedence unresolved.
6. `DeleteResult.status` is the literal `deleted`; derive `deleted_at` from the successful soft-delete operation. Do not invent a physical `deleted_at` column, `DELETED` ContentStatus value, audit table, or SQL statement.
7. Use logical Q1 target/owner lookup and Q2 direct-child existence check; all physical Content relations remain `SOURCE_REQUIRED`. Keep legacy `courses.mentor_id` only as a derived direct-owner candidate; assigned Mentor support and identity mapping stay open.
8. Build the API Requirement, Request Usage, Query, Mutation and Response Source matrices before finishing the eight template sheets; include logical-only mutation mapping in `07_table.md` and label its physical mapping gap.
9. Create 8 registered Markdown sheets plus `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` in `53_mentor_content_delete/`; follow the Study Markdown-only workflow and create no ZIP or runtime/schema/catalog/diagram changes.
10. Immediately verify the exact 11-file set, template appendix suffixes, front matter, catalog contract/error set, all DeleteResult fields, field/matrix traceability, JSON, relative links, Markdown tables/fences/whitespace and `git diff --check`.
11. Macro-review #49–#53 for tree/read visibility, create/update/revision, review/publish/unpublish, dependency/delete, status ownership, permissions, response shape and error consistency. Update connected DD reports/open questions/worklogs and the API inventory count after review; preserve unresolved issues as `VERIFIED_WITH_OPEN_QUESTIONS`.

### API Requirement Matrix

| API ID | Contract item | Value | Basis/status |
|---|---|---|---|
| #53 | Method/path | `DELETE /api/v1/mentor/content/{content_id}` | Catalog + AC-22; DIRECT |
| #53 | Actor/auth | Bearer JWT; role Mentor | Catalog; DIRECT |
| #53 | Path | `content_id:int64!` | Catalog + diagram; DIRECT |
| #53 | Body/query | None declared | Catalog + diagram; DIRECT omission |
| #53 | Success | HTTP 200 `DESIGN_RESOURCE_DELETED`; `ApiEnvelope<DeleteResult>` | Catalog + diagram; DIRECT |
| #53 | Errors | 401 auth, 403 access, 404 missing, 422 validation, 500 internal | Catalog; DIRECT exact set |
| #53 | Logical deletion | DELETE/soft delete Content, then reload tree | AC-22; DIRECT logical effect |
| #53 | Dependency | Block deletion for direct children; no cascade | `parent_id` + catalog conditional title; DERIVED |
| #53 | Published target | Unpublish via #52 first | Coordinate with #52 lifecycle; DERIVED proposal |

### Request Usage Matrix

| Request item | Source/use | Mapping use | Rule/status |
|---|---|---|---|
| Authorization | Header; authenticate Bearer and Mentor role | Course-management authorization | Role DIRECT; principal and assignment SOURCE_REQUIRED |
| `content_id` | Required path int64 | Q1 target lookup; `DeleteResult.id` | Type DIRECT; malformed-path mapping needs confirmation |
| Request body | None declared | None | DIRECT from catalog |
| Query parameters | None declared | None | DIRECT from catalog |

### Query Matrix

| Query | Purpose | Logical source | Predicate | Status |
|---|---|---|---|---|
| Q1 | Load target and course access context | Generic Content + owning course not identified | Content ID = `content_id`; check Mentor manages parent course | Physical table/columns SOURCE_REQUIRED; direct-owner candidate DERIVED |
| Q2 | Check dependency | Generic Content relation not identified | Existing child Content has `parent_id = target.id` | Relationship DIRECT from schema field; active-row predicate DERIVED; physical source SOURCE_REQUIRED |

### Mutation Matrix

| Mutation | Logical operation | Condition | Effect | Status |
|---|---|---|---|---|
| M1 | Soft-delete Content | Target authorized; not PUBLISHED under proposal; no active direct child | Mark target logically deleted; preserve Content/version/review history | Soft delete DIRECT; eligibility/history rule DERIVED; physical fields SOURCE_REQUIRED |
| M2 | Cascade/reparent child Content | Never proposed | No child mutation | DERIVED safeguard; confirm dependency policy |
| M3 | Physical audit/schema write | Not defined | No SQL/table/column prescribed | SOURCE_REQUIRED |

### Response Source Matrix

| Response field | Type | Candidate source | Mapping/null rule | Evidence status |
|---|---|---|---|---|
| `success` | boolean | Envelope branch | true on success; false on error | Envelope convention |
| `businessCode` | string | Catalog | Exact 200/error code | DIRECT |
| `message` | string | Application message | Text unspecified; no domain data | DERIVED |
| `data.id` | int64 | Target Content identity | Preserve target identifier | Contract DIRECT; physical source SOURCE_REQUIRED |
| `data.status` | `"deleted"` | DeleteResult literal | Exact string | DIRECT |
| `data.deleted_at` | date-time | Successful deletion time | ISO-8601 date-time; timezone/clock source to confirm | Field DIRECT; generator DERIVED |
| `meta` | object | Envelope convention | No extra deletion metadata proposed | DIRECT shape; null/empty serialization is current helper convention |
| `traceId` | uuid | Request trace | Propagate current request trace | Envelope convention; route absent |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #53 runtime | No route/module/test source | `UNWIRED / NOT_FOUND` | DD is design-only |
| Generic Content persistence | Legacy schema has no Content; pilot content_blocks is UUID/lesson-bound | `DISCREPANCY / SOURCE_REQUIRED` | No executable SQL or tombstone column can be specified |
| Dependency coverage | `parent_id` is declared, but full dependency graph is not | `DERIVED / SOURCE_REQUIRED` | Direct children are the only candidate; other dependencies remain open |
| Published deletion | #52 has separate publish/unpublish operation; AC-22 does not state prerequisite | `DERIVED / OPEN_QUESTION` | Proposal requires unpublish through #52 first |
| Delete/history behavior | AC-22 says soft delete; AC-33 reads content/version/author | `DERIVED / SOURCE_REQUIRED` | Preserve history logically; storage and audit are unknown |
| Mentor authorization | Catalog role and AC-22 course permission; no Study Mentor guard/assignment map | `SOURCE_REQUIRED` | Access query cannot be made executable |

## CHANGES

- Files changed: `apps/study-server/docs/dd/53_mentor_content_delete/` (8 sheets + 3 reports); connected DD #49–#52 plan/report/open-question updates; worklogs #49–#52; this worklog; inventory count worklog.
- CONTEXT_UPDATES: None; no runtime/schema/catalog/diagram/context page changes.
- Assumptions: Dependency, unpublish-first and history handling are simple `DERIVED` proposals. Preserve `Draft — Needs Confirmation` and all source gaps.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector and selected prior worklogs | Selector returned #48–#50; all selected worklogs reviewed; #51/#52 and inventory worklog reviewed as linked context. | `VERIFIED_STATIC_ONLY` |
| Catalog / AC-22 / AC-33 / schema / source scan | Contract and logical delete verified; no API #53 runtime route/module/test; no compatible Content schema found. | `VERIFIED_STATIC_ONLY` |
| Template and DD authoring | 11/11 manifest; all eight appendices match current registered templates; frontmatter and status checked. | `VERIFIED` |
| Markdown/contract integrity | Exact catalog method/path/input/response/status/error set; 2 JSON examples parse; relative links, table widths, fences and whitespace pass; `git diff --check` clean. | `VERIFIED` |
| Source and schema boundary | No API #53 route/module/test; endpoint absent from `DESIGN_CONTRACT_PATHS`; generic Content/tombstone storage remains unavailable. | `VERIFIED_STATIC_ONLY` |
| AC-22/AC-33 macro-review #49–#53 | Tree/read, create/update/version, review/publish/unpublish and soft-delete/dependency flows reconciled; open questions retained in linked DDs. | `VERIFIED_WITH_OPEN_QUESTIONS` |
| Application tests | Not run; docs-only and API #53 is unwired. | `NOT_RUN` |
| Context validator | Not run; no context page or registry was changed. | `NOT_APPLICABLE` |

## HANDOFF

- Remaining blockers: Physical Content model, exact dependency set, published/pending deletion policy, soft-delete storage, audit behavior, Mentor identity/assignment and AC-33 approval/publication relation.
- Next owner/action: Continue the one-API-per-session DD sequence with API #55; preserve the #49–#53 open questions until contract/schema owners resolve them.
