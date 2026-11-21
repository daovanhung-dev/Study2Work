---
task_id: "2026-10-26-implement-api81-admin-content-reject"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["AC-33 APIs #78–#80; Content lifecycle APIs #49–#53, especially #51/#52; shared Admin JWT guard and API #80 audit candidate"]
status: "VERIFIED"
---

# Worklog: Implement Study Server API #81 Admin Content rejection

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 74 coding worklogs available; selected #74, #75, #76; all three read; shortage none.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Shared ADMIN guard and raw signed-int64 parsing conventions; bind SQL; checked-in legacy schema and fake-session tests do not verify live DB; preserve dirty worktree.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: `query.py` contains SQL constants only; `view.py` owns transaction orchestration and response mapping; keep DERIVED policy explicit.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Use numeric JWT `sub` only as authenticated actor; status/audit mutations belong in one transaction; nullable/error/rollback handling and legacy BIGINT audit schema remain local candidates.
- additional_related_worklog_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api80-admin-content-approve.md`
    - carry_forward: API #80 uses active BIGINT `contents`, requires `PENDING_REVIEW`, writes `APPROVED` plus one `content_review_audit_logs` row atomically, and cannot bind action to the exact revision viewed in #79. Migration 011 is a candidate only.
- related_current_artifacts_reviewed: AC-33 index/diagram; catalog row #81 in `docs/lists/list_api.md`; API #81 DD package and prior DD creation worklog; APIs #78–#80 current source/tests and DDs; APIs #51/#52 query/view; shared ADMIN auth, response, DB, route and middleware source; legacy contents/audit DDL/migration 011 and V1-PILOT schema references.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: [AC-33 APIs #78–#80; Content lifecycle APIs #49–#53; shared ADMIN JWT guard and API #80 review-audit candidate]
```

## EXPECTED_BEHAVIOR

- AC-33 diagram: Admin reviews a pending Content, chooses the reject branch, supplies a reason, updates status to `REJECTED` with review reason, then reloads the #78 queue.
- Catalog #81: `PATCH /api/v1/admin/content/{content_id}/reject`; Bearer JWT/Admin; required signed-int64 `content_id`; required body `{reason: string}`; no query; HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<Content>`; exact errors 401/403/404/422/500 with `DESIGN_AUTHENTICATION_REQUIRED`, `DESIGN_ACCESS_DENIED`, `DESIGN_RESOURCE_NOT_FOUND`, `DESIGN_VALIDATION_ERROR`, `DESIGN_INTERNAL_ERROR`.
- Reusable Content response contains exactly `id`, `course_id`, `content_type`, `title`, `payload`, `status`, optional `parent_id`, and `order`; reason/reviewer/version/audit metadata are not response fields.
- Keep API #81 DD status `Draft — Needs Confirmation`; record chosen fallback as DERIVED and keep live-schema, moderation permission and revision continuity limitations explicit.

## CURRENT_BEHAVIOR (pre-edit)

- Current OpenAPI has 46 unique `/api/v1` path templates and 51 operations. The #80 approval PATCH is composed; #81 reject path is absent from the router, shared middleware path set, module tree and test tree.
- API #78 reads active legacy `contents` rows in `PENDING_REVIEW`; #79 returns the active eight-field Content projection without a revision token; #80 locks a pending row, transitions it to `APPROVED`, appends an audit record and commits atomically.
- API #51 archives prior snapshots and sets current `contents.status='PENDING_REVIEW'`; API #52 separately transitions `APPROVED` and `PUBLISHED`. Neither source defines rejection behavior or a reason field on `contents`.
- Checked-in legacy DDL has BIGINT `contents` with `deleted_at` and TEXT `status`, but no content reason column. Migration 011/`DB.sql` have a BIGINT `content_review_audit_logs` relation with `previous_status`, `new_status`, nullable `reason`, actor and timestamp. V1-PILOT review decisions use UUID revision/reviewer keys and do not directly map to the int64 catalog.
- Shared auth supports role `ADMIN` and returns numeric JWT `sub`; there is no dedicated moderation permission source. `error_response()` defaults to `data:null`. Current local tests use fake DB sessions; checked-in DDL does not prove live deployment.
- Worktree is extensively modified/untracked, including DDs and context; preserve all existing state and only edit API #81 plus directly affected context/worklog files.

## SOURCE_TRACE

```text
PATCH /api/v1/admin/content/{content_id}/reject
  -> typed required {reason:string} body; raw path/header passed to view
  -> shared ADMIN Bearer/JWT guard -> signed-int64 parse -> catalog 422 on malformed/overflow ID
  -> SELECT active legacy contents row FOR UPDATE
  -> missing/soft-deleted -> catalog 404; current status other than PENDING_REVIEW -> catalog 422 (DERIVED)
  -> conditional UPDATE contents.status=PENDING_REVIEW -> REJECTED RETURNING the eight Content fields
  -> INSERT one content_review_audit_logs row with numeric JWT sub, old/new status and request reason
  -> validate Content projection; commit after status and reason/audit writes; rollback failures to safe 500
  -> HTTP 200 DESIGN_RESOURCE_UPDATED with direct reusable Content data; reason remains absent from response
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Planned handling |
|---|---|---|---|
| Reason persistence | Diagram requires status `REJECTED` plus review reason; legacy `contents` has no reason field; migration 011 offers nullable reason in the #80 audit candidate. | `DIRECT LOGICAL EFFECT / DERIVED PHYSICAL MAPPING` | Store the submitted reason in the same decision/audit row written for the rejection. Do not add a new column/table or response field. |
| Audit semantics | #80 diagram explicitly says “+ audit”; #81 says “+ review reason” but does not separately specify audit. | `DISCREPANCY / DERIVED` | Use one row in the shared audit relation as the physical reason store and decision record; do not add a second audit write. Keep this selection Draft/open for owner review. |
| Eligible state | AC-33 precondition and #78 queue use `PENDING_REVIEW`; catalog #81 permits 422 but gives no trigger. | `DIRECT PRECONDITION / DERIVED` | Require current active status `PENDING_REVIEW`; otherwise return catalog 422 and do not write. |
| Request reason rules | Catalog requires string only; no length, normalization, blank, code or locale rule. | `DIRECT / SOURCE_REQUIRED` | Use strict string type and reject unknown fields; preserve string bytes/value, including empty string, without invented trim/length checks. |
| Admin permission/actor | Catalog says Admin; shared guard implements role `ADMIN` and numeric `sub`; finer permission absent. | `CURRENT SOURCE / DERIVED` | Require shared ADMIN before path parsing/DB; bind JWT subject as audit actor; do not claim dedicated moderation permission. |
| Revision continuity | #79 and #81 carry only content_id; #51 can create a newer pending current row. | `SOURCE_REQUIRED / OPEN` | Lock and act on the active row at call time; no claim that it is the revision viewed in #79; do not invent version input. |
| Status/response | Diagram says REJECTED; catalog returns reusable Content without reason. | `DIRECT` | Return the eight-field Content projection with resulting status `REJECTED`; omit null parent_id according to current response convention. |
| Transaction | Diagram describes status+reason outcome; #80 and #76 demonstrate caller-owned atomic mutation/audit; #81 DD had transaction TBD. | `DERIVED` | Lock, update, insert reason-bearing decision/audit, validate response and commit once; rollback any DB/projection/commit failure. |
| Live schema | Migration 011 and `DB.sql` are checked-in candidates; local tests use fakes. | `NOT_VERIFIED_HERE` | Make no claim that the relation, FK, grants or migration exist in deployed DB. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Preserve the existing dirty worktree. Complete conflict-source order: AC-33 diagram/index → current legacy/V1-PILOT DDL, DB guide and migration 011 → API catalog row #81. Then trace #78/#79/#80, #51/#52, shared auth/error/DB/middleware and their tests.
2. Keep direct contract exact: PATCH route, path int64, required JSON string `reason`, no query, direct Content response, exact catalog 200/401/403/404/422/500 set. Retain DD Draft status.
3. Add `api_81_admin_content_reject/models.py` with strict `reason: str`, forbidden extras, and an envelope reusing API #49 `ContentResponse`; keep models declarative only.
4. Add SQL constants only in `query.py`: active-row `SELECT ... FOR UPDATE`; conditional `PENDING_REVIEW` → `REJECTED` `UPDATE ... RETURNING` the eight Content fields; parameterized insert into migration 011's existing `content_review_audit_logs` with actor, old/new status and reason.
5. Add `validate.py` for shared ADMIN guard and raw signed-int64 path parse after auth; malformed/overflow ID maps to catalog 422. Rely on strict request model and common RequestValidation handler for missing/wrong/extra body fields.
6. Implement `view.py` transaction: authorize, parse, lock, map absent row to 404 and non-pending state to 422; update and insert one reason-bearing decision row atomically; validate projection before commit; rollback query/audit/projection/commit failures and return safe catalog 500. Do not mutate `content_versions`, publish, notify, add reason to Content, alter #52/#53 or add a revision field.
7. Wire the PATCH endpoint in `app/api/v1.py` after #80 with explicit int64 path/header/body schema and exact catalog responses. Add the unique path template to `DESIGN_CONTRACT_PATHS` so automatic validation/unhandled errors use DESIGN envelope.
8. Add focused TestClient coverage for success and audit bindings; ADMIN ordering; malformed/overflow path; required/type/extra body handling and preservation of empty reason; missing/deleted and non-pending rows; query/update/audit/projection/commit failures and rollback; response/trace/OpenAPI; and reachability regression for #78/#79/#80.
9. Update the API #81 DD package through registered `createDD-markdown`: mark the physical mapping/atomicity/pending guard as DERIVED; align Data Mapping/Table/Error/Overview/Open Questions/Plan/Verification and current `data:null`; retain response/body contract, all template appendix bytes and Draft status. Keep dedicated permission, exact revision, live schema and blank-reason owner policy open.
10. Update server-study route/architecture/runtime/security/database/module/tests/workflow/source-status and context manifest with API #81 runtime/test paths and recount current operations/tests. No schema or diagram change is planned; the existing candidate migration is reused.
11. Run focused API #81 tests, linked #49–#53/#78–#81 tests, full Study suite, Ruff, OpenAPI/import inspection, DDL candidate/reference checks, DD links/JSON/appendix checks, `git diff --check`, and context validation with documented DB Admin baseline separated.
12. Review only scoped diffs plus full `git status` preservation boundary. Do not stage or commit. Report DERIVED choices, fake DB/live schema and revision limitations, and next API #82.

## PRE-CODE CHECKPOINT

- Read root/global routing instructions, `context-map.md`, worklog contract, complete Study Server entry/index, coding worklogs #74/#75/#76 and relevant API #80 worklog.
- The selector's exact `coding` result was #74/#75/#76; all three were read in full and recorded above, with no shortage.
- Read the AC-33 index and full Admin diagram before schema; then read legacy content tables and migration 011; then catalog row #81. The catalog path is `docs/lists/list_api.md` at repository root.
- Reviewed API #81 DD, #79 revision questions, #80 approval mapping, #51 snapshot/PENDING_REVIEW logic, #52 publication transitions, current ADMIN guard, `error_response`, DB helpers, route and middleware conventions, and API #80 focused HTTP tests.
- The implementation plan and selected DERIVED fallback are recorded above before API #81 runtime, tests, DD or context edits.

## CHANGES

- Added API #81 models, SQL constants, validation and transaction/view orchestration in `apps/study-server/app/modules/admin/api_81_admin_content_reject/`.
- Wired `PATCH /api/v1/admin/content/{content_id}/reject` into `app/api/v1.py` and added the route to `DESIGN_CONTRACT_PATHS` in `app/core/middleware.py`.
- Added focused TestClient coverage for request/auth/path/state handling, database/commit failures, response contract, OpenAPI and adjacent API reachability.
- Updated API #81 DD implementation mapping and verification while retaining `Draft — Needs Confirmation` and exact template appendix suffixes.
- Corrected directly affected API #80 DD notes that called #81 unwired or described API #81 response route as absent; kept owner-review/live-schema limits explicit. Historical #80 worklog was not changed.
- Updated Study Server scope/source/runtime/database/security/module/test/workflow pages and context manifest; source snapshot now records 47 paths, 52 operations and 997 passing Study tests.
- No diagram, SQL, migration, staging or commit was created for API #81. Migration 011 remains the checked-in candidate selected as a DERIVED physical mapping.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Focused API #81 TestClient | 29 passed; one upstream Starlette/httpx deprecation warning. | PASS — LOCAL |
| Linked regression APIs #49–#53, #78–#81 | 200 passed; same warning. | PASS — LOCAL |
| Full Study Server suite | 997 passed; same warning. | PASS — LOCAL |
| Scoped Ruff | API #81 route, middleware, module and tests passed. | PASS — STATIC |
| OpenAPI | 47 unique `/api/v1` paths, 52 operations; required body, int64 path/header and catalog 200/401/403/404/422/500 responses. | PASS — LOCAL |
| DD package | 11 Markdown files; 8 template appendix suffixes byte-exact; 4 JSON examples parse; 41 relative links resolve. | PASS |
| Context manifest | Valid JSON; all 6 API #81 required paths exist among 288 required paths. | PASS |
| `git diff --check` | Clean after final report/worklog synchronization. | PASS |
| Context validator | `--skip-drift` reports absent DB Admin scope files/roots and dependent links only; no Study API #81 finding. | BASELINE_FAIL_OUT_OF_SCOPE |
| Live database/deployment | Not accessed; checked-in migration 011 is a candidate only. | NOT_VERIFIED_HERE |

One warning is from the upstream Starlette/httpx TestClient dependency, not an API #81 assertion failure. Fake DB sessions do not establish live transaction behavior.

## HANDOFF

API #81 is implemented and locally verified. Remaining owner/live confirmations: dedicated moderation permission; reason blank/length/retention/visibility policy; relation/migration/FKs in deployed DB; exact #79 revision continuity; and rejected-content lifecycle. The runtime acts on the active row locked at request time and stores reason in the same reason-bearing decision row. Next API in sequence: #82.
