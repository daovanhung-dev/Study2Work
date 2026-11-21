---
task_id: "2026-10-25-implement-api55-mentor-submissions-detail"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["API #54 submission list -> API #55 detail -> API #56 grade / API #57 feedback"]
status: "PARTIAL"
---

# Worklog: Implement API #55 Mentor submission detail

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` (`node` availability not assumed)
- selector_result: 48 matching coding worklogs; 3 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: API #34 persists legacy BIGINT UploadAsset metadata; keep read-only lookups scoped by owner, purpose and course; live DB/Object Storage are unverified.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: Use explicit shared MENTOR guard and direct `courses.mentor_id` ownership; checked-in migrations are artifacts, not live schema proof.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: For a Mentor detail GET, preserve catalog errors, parse raw signed-int64 path in the view, keep query.py SQL-only, return 404 for missing/malformed ID, detect broken parent links, and test through TestClient.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Implement `GET /api/v1/mentor/submissions/{submission_id}` for the AC-23 step after API #54 chooses one submission and before APIs #56/#57 mutate grade/feedback. Keep it read-only and return `ApiEnvelope<Submission>`.
- Canonical contract: API catalog and AC-23 diagram define Bearer JWT / Mentor, required `submission_id:int64`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, and errors 401/403/404/500 with their catalog business codes. Reusable `Submission` includes id, assignment_id, user_id, content, files, status, submitted_at, score and feedback; it has no rubric field.
- Sources read by priority: AC-23 action says read `Submission + files + rubric`; AC-23 node and catalog response say `ApiEnvelope<Submission>`. Legacy DDL has BIGINT `assignments` and `assignment_submissions` but no assignment-rubric relation. V1-PILOT rubric tables use UUID `assessments`/`rubrics` and have no relation to the legacy BIGINT submission model. Do not invent a rubric field or join.
- Derived fallbacks, explicitly not approved/live facts: use the current shared MENTOR guard and direct course owner `courses.mentor_id`; reuse API #54's exact URL + owner + `SUBMISSION` purpose + course lookup for 0/1 `UploadAsset`; preserve the shared `SubmissionResponse` shape and its current optional-field serialization; map malformed/out-of-range raw path to catalog 404 following API #48; treat null/orphan required parent relations as safe 500 per #55 DD candidate.

## CURRENT_BEHAVIOR

- Source/config: API #55 has no route, module, test or `DESIGN_CONTRACT_PATHS` template. API #54 already returns a `Page<Submission>` using shared MENTOR auth, direct-owner filters and a DERIVED constrained upload lookup. API #48 provides a raw signed-int64 path pattern and TestClient conventions.
- Runnable tests: Current context records 461 passing Study Server tests; this is historical baseline and will be rerun after implementation. API #55 has no focused tests.
- Runtime wiring: Current router includes API #54 but not API #55. Shared `error_response()` emits `data: null`; no transaction commit is needed for this read-only endpoint.

## SOURCE_TRACE

```text
GET /api/v1/mentor/submissions/{submission_id}
  -> raw path to API #55 view
  -> validate_current_user_request(role=MENTOR)
  -> parse signed-int64 path
  -> query submission + LEFT JOIN assignment/course + constrained LATERAL UploadAsset lookup
  -> distinguish missing row / broken parent / owner mismatch
  -> map the shared Submission response only after ownership passes
  -> success/error envelope + trace
  -> TestClient route/auth/access/data/error/OpenAPI/read-only checks
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Rubric projection | AC-23 action mentions rubric, but catalog/diagram response is `Submission`; reusable schema has no rubric and neither legacy assignment DDL nor the separate UUID V1-PILOT model connects it to this submission | `DISCREPANCY / SOURCE_REQUIRED` | Return only the catalog `Submission` shape; keep rubric unresolved in DD; do not invent schema/field. |
| Mentor access | AC-23 precondition says Mentor may grade course; current Mentor APIs use numeric JWT subject and direct `courses.mentor_id`; assigned-Mentor relation is absent | `DERIVED / SOURCE_REQUIRED` | Enforce direct owner, do not claim assigned-Mentor access. |
| Files association | Legacy submission has one `file_url`; `uploads` has metadata but no submission FK; API #54 already applies URL/owner/purpose/course fallback | `DERIVED / SOURCE_REQUIRED` | Return zero or one metadata asset; API #35 producer compatibility remains unverified. |
| Null/orphan relations | Logical guide/ERD and legacy DDL disagree on nullability of submission/assignment/course keys | `DISCREPANCY` | Detect missing required parent joins and return safe 500 per the DD candidate; live schema remains unverified. |
| Path parse behavior | Catalog permits only 401/403/404/500; minimum and malformed behavior are not specified | `DERIVED` | Follow API #48: raw signed-int64 path, malformed/overflow -> 404, no added 422. |
| Optional fields/time | Reusable Submission marks content/score/feedback optional; DDL fields are nullable and timestamp is zone-less | `SOURCE_REQUIRED` | Reuse current #54 serialization of optional fields and ISO JSON conversion; no live timezone claim. |

## IMPLEMENTATION_PLAN

1. Complete the source-priority review before runtime edits: confirm the AC-23 step and API node, legacy and V1-PILOT DDL/rubric relation, catalog `Submission` contract, current #54 output, API #48 path/error behavior, and #56/#57 consumption. Record unresolved rubric and assigned-Mentor behavior instead of reconciling by assumption.
2. Add `api_55_mentor_submissions_detail` with a strict success envelope that reuses API #54's `SubmissionResponse` model; keep models declarative, query.py SQL constants only, and view.py responsible for auth, DB calls, access/integrity branches, rollback and response mapping. Add a local raw signed-int64 parser because the contract has no 422 and API #48 uses this pattern.
3. Build one SELECT by `submission_id`, using LEFT JOINs for assignments/courses so null/orphan relation state is observable, and one constrained LATERAL lookup matching API #54: exact URL, `owner_id = user_id`, `purpose='SUBMISSION'`, same course, deterministic `id ASC LIMIT 1`. Do not query a rubric table.
4. Wire `GET /api/v1/mentor/submissions/{submission_id}` with an `int64` OpenAPI path schema and shared Mentor guard; register its route template in `DESIGN_CONTRACT_PATHS` so any framework-level contract errors use the design mapping. Keep the endpoint read-only with no commit.
5. Add TestClient coverage for success and Submission shape, nullable optional fields, matched/no upload metadata, missing/malformed/out-of-range IDs, invalid auth and wrong role before DB access, direct-owner denial before response mapping, null/orphan integrity, SQL and response-mapping failures, trace ID, OpenAPI and no commit.
6. Macro-review API #54 list -> #55 detail -> #56 grade/#57 feedback: keep the reusable Submission field names/types aligned and preserve each mutation endpoint's separate ownership. Update only API #55 DD claims and the server-study route/module/database/test context and manifest needed by this new endpoint; preserve every pre-existing worktree change and Excel appendix.
7. Run focused API #55 tests, full Study suite, Ruff, route/OpenAPI assertions, DD file/link/example checks, and `git diff --check`; run the prescribed context validator using Node or Deno fallback and record unrelated repository baseline errors separately. Review final diff for scope and worklog evidence.

## CHANGES

- Runtime route/module files added under `apps/study-server/app/modules/mentor/api_55_mentor_submissions_detail/`; route added in `app/api/v1.py`; middleware route template registered in `app/core/middleware.py`.
- Added `apps/study-server/tests/modules/mentor/api_55_mentor_submissions_detail/test_mentor_submission_detail.py`.
- Updated API #55 DD sheets `01_Lich_su.md`, `02_Overview.md`, `04_Response.md`, `05_Data_Mapping.md`, `06_Error.md`, `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, and `VERIFICATION_REPORT.md`; preserved the Excel appendix suffixes.
- Updated API #54 linked `PLAN_RESULT.md` and `VERIFICATION_REPORT.md` to record the #55 handoff and remaining rubric question.
- CONTEXT_UPDATES: `.agents/server-study/AGENTS.md`, `architecture.md`, `apis/declared-routes.md`, `core/runtime.md`, `core/database-security.md`, `database.md`, `modules/README.md`, and `tests.md` now describe #55; `.agents/context-manifest.json` registers its module/test paths.
- Existing unrelated dirty worktree changes were preserved; no files were staged or committed.
- Assumptions: Keep API #55 rubric omission and direct-owner/file lookup behavior marked derived/unresolved; no schema migration is planned.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | 48 matching logs; selected three same-type logs; all three were read. | VERIFIED |
| Source/contract review | API #55 DD, AC-23 diagram, catalog, legacy/V1-PILOT schema evidence, APIs #34/#47/#48/#54, #56/#57 DD and server-study instructions reviewed. | VERIFIED_STATIC |
| `cd apps/study-server && uv run pytest tests/modules/mentor/api_55_mentor_submissions_detail/test_mentor_submission_detail.py -q` | 22 passed; one upstream Starlette/httpx deprecation warning. | VERIFIED_LOCAL |
| `cd apps/study-server && uv run pytest -q` | 483 passed; same warning. | VERIFIED_LOCAL |
| `cd apps/study-server && uv run ruff check app/modules/mentor/api_55_mentor_submissions_detail app/api/v1.py app/core/middleware.py tests/modules/mentor/api_55_mentor_submissions_detail` | Passed. | VERIFIED_LOCAL |
| OpenAPI inspection via `app.openapi()['paths']` | 26 `/api/v1` operation declarations / 25 unique path templates; #55 GET uses signed-int64 path schema and `GetMentorSubmissionEnvelope`. | VERIFIED_LOCAL |
| DD static validation | Eight sheet filenames match the registered template; appendix suffixes are byte-identical; links resolve, fenced JSON parses, and fences/whitespace are clean. | VERIFIED_STATIC |
| `git diff --check` | Passed. | VERIFIED_STATIC |
| `deno run -A scripts/validate-agent-context.mjs` | Fails with repository-wide source drift from dirty worktree and missing db-admin context. `--skip-drift` confirms structural findings are confined to db-admin pages/source roots and links. | BLOCKED_BY_REPOSITORY_BASELINE |
| Live database/schema/deployment | Not checked. | NOT_VERIFIED |

## HANDOFF

- Remaining open decisions: Rubric projection, assigned-Mentor authorization, API #35 upload URL compatibility, and live schema/nullability remain unsupported by a linked source. The DD remains `Draft — Needs Confirmation`.
- Context-validator blocker: Existing dirty source changes cause drift output across the repository, and the db-admin scope is absent from this checkout; this task did not modify those unrelated scopes.
- Next owner/action: API #55 local implementation is complete against the catalog `Submission` shape; proceed to API #56 in a separate API session after the remaining rubric/access questions are carried forward.
