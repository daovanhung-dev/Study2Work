---
task_id: "2026-10-24-create-study-api91-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #91 — Quiz statistics

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Keep catalog contract separate from source; label candidate mappings `DERIVED`; do not invent asset/response fields or persistence.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Read the precise AC diagram; preserve catalog response shape and expose diagram/schema discrepancies instead of guessing payload structures.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Keep unavailable schema and access rules `SOURCE_REQUIRED`; proposals must be simple, explicit, and not silently treated as approved behavior.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Create one Vietnamese Markdown DD for API #91, plan before authoring, verify immediately after authoring, and macro-review AC-35 APIs #87–#91 as one group.
- Canonical contract/approved DD: `GET /api/v1/admin/quizzes/{quiz_id}/statistics`; Bearer JWT, role Admin; path `quiz_id:int64!`; response `ApiEnvelope<Quiz>`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR` (catalog row #91). AC-35 diagram requires Admin quiz-management permission and an aggregate of attempt statistics but only types output as generic `ApiEnvelope`; it does not define statistics fields or aggregation rules.

## CURRENT_BEHAVIOR

- Source/config: No API #91 route/path/module marker was found under `apps/study-server/app` or `apps/study-server/tests`; current router declares only #01–#09 and #12–#14 with matching views. The latest inventory reports 90 DD folders (#01–#90), 13 missing (#91–#103), and 12 source-wired API IDs.
- Runnable tests: Not run; no API #91 test source exists in current Study tests. This is source evidence only, not an app runtime result.
- Runtime wiring: `UNWIRED / NOT_FOUND` for API #91. Study has no Admin quiz guard/route; legacy DDL is a design candidate and V1-PILOT assessment schema is a distinct UUID/versioned model. Live schema is not verified.

## SOURCE_TRACE

```text
Admin Bearer + quiz-management permission -> GET #91 by quiz_id -> verify quiz exists -> aggregate related quiz_attempts (score/submitted_at; status enum remains unresolved) -> return the direct catalog Quiz envelope, while exposing the statistics/result-shape conflict and an explicitly proposed statistics DTO -> Admin UI display.
```

## PLAN BEFORE DD AUTHORING

1. Load the registered `server-study` workflow and `createDD-markdown` skill; follow the Markdown-only Study deliverable rule.
2. Read the exact API #91 catalog row and reusable response schema; preserve the direct contract, including its declared response type and error set.
3. Read the full AC-35 index entry and diagram page, including nodes, decision branches and connected API #87–#91 order. Read AC-16/API #29–#32 only where needed to establish the source/history of attempts and answers.
4. Review DD #87–#90 and relevant DB table guide/ERD/DDL separately from current runtime source; do not merge legacy and V1-PILOT schema models or claim live-schema proof.
5. Build requirement, request-usage, query, mutation and response-source matrices before authoring. Keep the direct `ApiEnvelope<Quiz>` contract in its own matrix. Because the user authorizes simple inferences outside the diagram, include a separate `DERIVED` proposal for a minimal `QuizStatistics` DTO and explicit definitions: all attempts; submitted rows by non-null `submitted_at`; scored rows by non-null `score`; average over scored rows; pass count by `score >= passing_score`; pass rate = passed/scored, null when no scored rows. Do not silently change catalog or represent the proposal as approved; retain the response-shape conflict and null passing-score policy as open questions.
6. Write the implementation plan in this worklog before creating the DD folder. Create the required sheet/report set from registered templates under `apps/study-server/docs/dd/91_admin_quizzes_statistics/`; no ZIP or runtime/schema/catalog/diagram edits.
7. Immediately validate exact catalog contract, every response field, diagram trace, example JSON, template appendix parity, Markdown links/tables/fences/whitespace and exact file set.
8. Macro-review #87–#91 for consistent list/create/update/delete/statistics semantics, quiz visibility, attempt retention/history, aggregate definitions and error/access behavior. Update connected DDs/worklogs only where needed, then refresh the inventory worklog and record open questions without implying approval.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #91 source | Current router, module and tests have no #91 marker/path; route/view inventory still ends at #14 for implemented API IDs. | `UNWIRED / NOT_FOUND` | DD is design-only; no runtime behavior is claimed. |
| Statistics result definition | AC-35 says aggregate attempt statistics; catalog returns `ApiEnvelope<Quiz>` and reusable Quiz has no aggregate fields. | `DISCREPANCY / SOURCE_REQUIRED` | Keep direct contract and a separate unapproved `QuizStatistics` proposal; do not silently change the catalog. |
| Attempt status/persistence | AC-16 names `IN_PROGRESS`, `PENDING_GRADE`, and `GRADED`; legacy status is VARCHAR with incomplete enum; V1-PILOT uses UUID assessment tables. | `DERIVED / DISCREPANCY` | Aggregate by candidate timestamps/scores; do not merge schemas or assume a complete status enum. |

## API REQUIREMENT MATRIX

| API ID | Method/path | Actor/auth | Input | Response/success | Errors | Basis/status |
|---|---|---|---|---|---|---|
| #91 | `GET /api/v1/admin/quizzes/{quiz_id}/statistics` | Admin; Bearer JWT; AC-35 quiz-management permission | `quiz_id:int64!`; no body/query | `ApiEnvelope<Quiz>`; 200 `DESIGN_RESOURCE_RETRIEVED` | 401/403/404/500 with catalog `DESIGN_*` codes | Catalog DIRECT; diagram asks for aggregate statistics but has no result schema. |

## PLAN BEFORE DD AUTHORING — REFINED AFTER CATALOG/DIAGRAM READ

1. AC-35 #91 is selected from the Statistics branch after #87 list; the diagram node says “Aggregate attempt statistics” then display result.
2. AC-16 connects #29 attempt creation (`IN_PROGRESS`), #30 answer saves, #31 submit/autograde and possible `PENDING_GRADE`/`GRADED`, and #32 result read. Avoid counting status labels as a canonical enum; use persisted timestamps/scores only as candidate aggregate signals.
3. The legacy candidate relations are `quizzes`, `quiz_attempts`, and optionally none of `quiz_answers`; `quiz_attempts` contains `quiz_id`, `user_id`, `started_at`, nullable `submitted_at`, nullable `score`, and `status`. V1-PILOT instead uses UUID `assessments`/`assessment_attempts`/`assessment_answers`; never combine the two models.
4. Preserve #91 catalog response type `ApiEnvelope<Quiz>` as the direct expected contract. Add an explicitly unapproved `ApiEnvelope<QuizStatistics>` proposal only to make the statistics purpose implementable; record that the catalog/reusable schemas currently have no `QuizStatistics` schema and `Quiz` has no aggregate fields.
5. Proposed minimal metrics and definitions: `attempt_count=COUNT(*)`; `submitted_attempt_count=COUNT(submitted_at IS NOT NULL)`; `graded_attempt_count=COUNT(score IS NOT NULL)`; `average_score=AVG(score)` over scored rows; `passed_attempt_count=COUNT(score >= passing_score)` over scored rows; `pass_rate=passed_attempt_count/graded_attempt_count*100`, null when denominator is zero. All metrics are `DERIVED`, not direct contract. Passing-score nullability, scale/rounding and soft-deleted quiz visibility remain confirmation points.
6. Review DD #87–#90 for aligned Admin permission, quiz status/visibility, quiz attempt retention, updates after attempts and deletion branches. Macro-review after authoring #91; keep statistics available for retained history as a proposal consistent with #90, while hard-deleted/no-longer-existing quizzes map to catalog 404.
7. Create template-based Markdown sheets and reports only; do not edit runtime, schema, catalog or diagrams. Validate the DD and macro-review report immediately after authoring.


## CURRENT SESSION — FINAL PLAN BEFORE DD AUTHORING

- Classification: `primary_task_type: docs`; `project_scopes: [server-study]`; no cross-scope dependencies.
- Current evidence rechecked before creating DD files:
  - `docs/lists/list_api.md` row #91: `GET /api/v1/admin/quizzes/{quiz_id}/statistics`, Admin Bearer, `quiz_id:int64!`, direct `ApiEnvelope<Quiz>`, 200 `DESIGN_RESOURCE_RETRIEVED`, and exact 401/403/404/500 codes.
  - AC-35 index and `AC_04_ADMIN_MANAGEMENT.drawio` page: `STATISTICS` branch #91 → “Aggregate attempt statistics” → display result; no metric or output schema is defined.
  - AC-16 index and `AC_02_STUDENT_LEARNING.drawio`: #29 creates `IN_PROGRESS`; #31 submits and branches to `PENDING_GRADE` or `GRADED`; #32 displays score/status. These labels do not define the complete AttemptStatus enum.
  - `DB_UNICA_TABLES.md`, `DB_UNICA_ERD.drawio`, and legacy `infra/postgres/study-server/DB.sql`: candidate `quizzes` 1:N `quiz_attempts`; attempt fields include `quiz_id`, `started_at`, nullable `submitted_at`, nullable `score`, and `status`. The schema is design-only and quiz foreign-key nullability differs between guide and DDL. V1-PILOT `assessment_attempts` uses UUID and a separate versioned model.
  - DD #87–#90 and #29–#32 reviewed. #90 already proposes hiding tombstones in #87 by default, rejecting update/new attempt after tombstone, retaining #30–#32 history, and allowing #91 to read retained history; all remain DERIVED pending owner confirmation.
  - Current Study router/module/tests contain no #91 route/view/test. This remains `UNWIRED / NOT_FOUND`; no runtime tests will be claimed.
  - Registered template pack digest recheck: `7189c554124ab319598d946e6a3b8b51ea312b25156b5c7dcaad9923c7f8a863`, matching the previously reviewed eight-template pack.

### Final authoring plan

1. Preserve the catalog contract exactly in the direct-contract matrices: GET path-only, Admin Bearer, int64 path ID, `ApiEnvelope<Quiz>`, HTTP 200, and exact four errors.
2. State the AC-35 statistics intent and the response-shape conflict. In a separate, clearly unapproved `DERIVED` proposal, define `QuizStatistics` with quiz ID; total, submitted, and scored attempt counts; average score; passed count; and pass-rate percent. Do not add it to `Quiz` or represent it as a catalog schema.
3. Use one legacy candidate aggregate over `quizzes LEFT JOIN quiz_attempts`; count all linked attempt rows, `submitted_at IS NOT NULL`, and `score IS NOT NULL`; average non-null scores; compare scored rows with `passing_score`; do not read `quiz_answers` or filter by incomplete attempt-status enum. Missing quiz maps to catalog 404. Mark every table/column as candidate; live schema is not verified.
4. For the proposal, return null average when no scored attempts; pass count/rate are null if the threshold is null; rate is null if no scored attempts. Keep exact rounding/scale and nullable threshold behavior open.
5. Integrate the AC-35/AC-16 deletion proposal without approving it: soft-deleted quiz history remains available to #91; hard-deleted/no-row quiz returns 404. Record #87 default tombstone exclusion, #89 update rejection, #29 new-attempt rejection and #30–#32 history retention as one DERIVED group proposal.
6. Create eight registered Markdown sheets plus `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md` under `91_admin_quizzes_statistics/`; no ZIP, runtime, schema, catalog, or diagram edits.
7. Verify exact contract/errors, every proposed response field and query source, valid JSON examples, template appendix byte parity, internal links/anchors, Markdown table widths, fences, final newline and whitespace; then complete macro-review #87–#91 and update connected reports/worklogs with the shared proposal and unresolved confirmations.

## CHANGES

- Files changed: This initial worklog only.
- CONTEXT_UPDATES: None planned; no runtime/schema/catalog/diagram changes are in scope.
- Context pages changed: None planned.
- Assumptions: API #91 is the next missing DD after #90 according to the inventory worklog; verify against current filesystem and catalog before authoring.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Selected #48/#49/#50 and read all three in full. | `VERIFIED` |
| Current DD/API inventory | 103 catalog IDs; #01–#90 folders and #91–#103 absent; source pair is #01–#09 and #12–#14. | `VERIFIED_STATIC_ONLY` |
| Catalog and diagrams | Read API #91 row, Quiz/QuizAttempt schemas, full AC-35 branch and AC-16 attempt/grading flow. | `VERIFIED_STATIC_ONLY` |
| DB/schema and source | Read design table guide/ERD, legacy quiz DDL, V1-PILOT assessment attempt DDL, current router/tests and error/middleware boundary. | `VERIFIED_STATIC_ONLY` |
| Skill/template gate | Registry wires `createDD-markdown`; read full skill and all eight template files. Template manifest SHA-256: `7189c554124ab319598d946e6a3b8b51ea312b25156b5c7dcaad9923c7f8a863`. No ZIP archive found in the in-scope diagram/template paths. | `VERIFIED_STATIC_ONLY` |
| API #91 authoring and static validation | 11-file package, 8 template appendices, JSON, links, tables, fences and whitespace passed static validation. | `VERIFIED` |
| AC-35 macro-review #87–#91 | Shared tombstone/attempt proposal reconciled across #87–#91 and #29–#32; unresolved decisions retained. | `VERIFIED_WITH_OPEN_QUESTIONS` |

## HANDOFF

- Remaining blockers: response shape/metrics, Admin policy, live schema, tombstone value and timestamp, hard-delete branch, in-flight attempt policy, races and error integration need owner/source confirmation.
- Next owner/action: Create the API #92 DD in a separate work session; keep AC-36 macro-review pending until #96 exists.


## CURRENT SESSION — FINALIZE #91 AND REVIEW AC-35 GROUP

- Current filesystem check: DD #91 exists with the exact 11-file Study package. Initial static validation found trailing Markdown spaces in `OPEN_QUESTIONS.md`; removed those spaces and will rerun all checks before marking the package verified. The previous verification report/worklog still says `PENDING` and is stale.
- Macro-review scope: AC-35 APIs #87–#91 plus the directly connected AC-16 attempt lifecycle #29–#32. Preserve each catalog contract; label cross-API lifecycle rules `DERIVED`, not approved behavior.
- Plan before updates: (1) validate #91 contract/examples/template parity/links/tables/whitespace; (2) reconcile #87 list visibility, #88 creation/model, #89 history updates, #90 delete branches, and #91 retained-history statistics; (3) inspect AC-16 precondition and #29–#32 attempt/save/submit/result flow; (4) record one consistent, unapproved tombstone proposal in affected DDs/reports/worklogs; (5) run document-only static checks and update this worklog. No runtime, schema, catalog or diagram changes; no application tests.

## CURRENT SESSION — FINALIZE #91 AND AC-35 REVIEW

- Current package check: API #91 contains the exact 11-file set; eight template appendix suffixes match byte-for-byte. Five JSON blocks parse; 33 tables / 444 table lines are consistent; eight fences balance; 24 local links and anchor targets resolve; no trailing whitespace; all files end with newline.
- AC-35 review: #87–#91 reports and overviews now use `VERIFIED_WITH_OPEN_QUESTIONS`; obsolete “pending until #91” statements were corrected. The shared lifecycle proposal is explicitly DERIVED and coordinated with AC-16 #29–#32. Owner decisions and runtime/source gaps remain open.
- Files changed in this finalization: #87–#91 verification reports, #29–#32 overview/open-question/report cross-references, #87–#90 worklogs, and this worklog. No runtime/schema/catalog/diagram changes.
- Tests: no application tests run. `git diff --check` is recorded after the final documentation edits.
- Next DD: #92 `GET /api/v1/admin/notifications`; AC-36 macro-review stays pending until #92–#96 exist.
