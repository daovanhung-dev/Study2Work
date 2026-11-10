---
task_id: "2026-11-07-design-study-screen-st10"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-10 lesson access/start handoff ↔ AC-14/AC-15 and APIs #22/#23/#24; upstream ST-09 and downstream ST-11/ST-12"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-10

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 237; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Separate expected/current behavior; trace auth, query, response, tests and side effects; keep Study Web UNWIRED and runtime/live-schema claims limited to evidence.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Do not infer routes, fields, actions or policy from mockups; distinguish local source from Draft API contracts; preserve the UI-only DD boundary.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Keep current route/source and Draft contract status separate; preserve unresolved API/security decisions and do not claim test/runtime execution.
- additional_dependency_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-st09.md`
    - carry_forward: ST-09 exposes no lesson selection/lessonId handoff; APIs #22–#24 were NOT_FOUND in the preceding audit, and public API #09 cannot prove enrollment/access. Recheck current source before relying on these findings.
- scoped_context_reviewed:
  - project: `.agents/project/INDEX.md`, architecture, dependencies, contracts and database pages for the Study Web ↔ Study Server boundary; Study OpenAPI is registered as `NOT_FOUND`.
  - web-work: router, INDEX, Study Web router/INDEX, and `.agents/web-study/design.md`; Study Web is `UNWIRED` and the design guide is intent only.
  - server-study: AGENTS and INDEX; selected Study router/modules/tests, API #09 current source, AC/API design, and relevant database context/DDL were reviewed.
  - registry: `createDD-markdown` is explicitly excluded for `web-ui-only-dd`; Study OpenAPI is `NOT_FOUND`; no canonical UI-only DD skill is wired.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-10 only in this session. Read the screen inventory, AC-14/AC-15, API #22/#23/#24 contracts and current Study Server source; inspect existing assets; write/update `ST-10_PLAN.md` before editing DD, marker map, or annotation; preserve usable originals; ensure one-to-one numbered markers and explicit A–F DD sections; update `list_screen.md`, `dd_screens/PLAN.md`, and this worklog. Do not invent lesson selection, authorization, API behavior, retry/idempotency, payload fields, media access, or navigation policy.
- Canonical inventory details and source contract: ST-10 is row 24 in `list_screen.md`, route proposal `/student/lessons/:lessonId/start`, AC-14, #22/#23/#24, with ST-09/ST-11 links. The detailed plan now contains a dated source re-audit written before DD/marker edits.

## CURRENT_BEHAVIOR

- Source/config: AC-14 diagram sequences #22 access → enrollment/prerequisite decision → #23 start → UPSERT `lesson_progress=IN_PROGRESS` → #24 Lesson/content; denied access is `403 + reason`. AC-15 adds access and publish checks before content read. Catalog #22–#24 require Student Bearer and `lesson_id:int64!`, with no query/body. API DDs remain Draft with entitlement/JWT/reason, upsert/idempotency/transaction, and #24 authorization/publish/projection/null/path questions open.
- Runnable tests: Focused source inventory finds no Student #22/#23/#24 route/module/query/test; Admin #82–#86 lesson routes have distinct paths/permissions. API #09 route/query/view/test source exists and returns published curriculum rows including `content`/`video_url` without enrollment/auth context. No application tests were run.
- Runtime wiring: `apps/study-client` has no tracked editable source/package; ignored `dist` is a root-only bundle and serving/deployment is unverified. Study Web remains UNWIRED. ST-09 has no lesson selection/lessonId handoff; ST-11 expects `/student/lessons/:lessonId` and also lists #24, leaving request ownership unresolved.

## SOURCE_TRACE

```text
Expected: `list_screen.md` row 24 and AC-14/AC-15 plus Draft catalog/API DD contracts for #22–#24.
Current: static assets, current Study Web inventory, API route/module/test search, API #09 query, API Draft DD/open questions, and both checked-in DDL models reviewed; no runtime or test execution.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API declaration vs runtime | Catalog/AC/API DDs declare #22–#24; exact router/module/test search finds no Student implementations. | DISCREPANCY | Keep declared design separate from current behavior; Admin lesson APIs are not substitutes. |
| Access response | AC-14 has enrollment/prerequisite decision and `403 + reason`; #22 catalog success type is `ApiEnvelope<Lesson>` with no explicit allow/reason field. | OPEN CONTRACT | Do not guess an allow flag or reason shape; preserve transport branches only as declared. |
| Start/upsert model | AC-14 says UPSERT to `IN_PROGRESS`; API #23 catalog says 201 `ApiEnvelope<Lesson>`. BIGINT `lesson_progress` DDL lacks `(user_id,lesson_id)` unique; V1-PILOT UUID `lesson_progress_facts` has unique `(enrollment_id,lesson_id)` but different identity/fields. | DISCREPANCY / LIVE SCHEMA UNVERIFIED | Do not infer idempotency key, state preservation, transaction, or live schema. |
| Lesson content gate | AC-15 requires access/publish checks; #24 server predicate is absent. Existing #09 public endpoint selects PUBLISHED `content` and `video_url` without enrollment/auth context. | SECURITY CONTRACT OPEN | Client order and #09 response do not prove protected access control. |
| Screen transition | Inventory expects ST-09→ST-10→ST-11; ST-09 has no lesson selector/ID and ST-11 also lists #24. | BLOCKED | LessonId handoff and duplicate #24 read ownership need a decision. |

## CHANGES

- Files changed so far: this worklog, `ST-10_PLAN.md`, `ST-10.md`, `list_screen.md`, and `dd_screens/PLAN.md`. Existing marker JSON/SVG/annotated PNG and source PNG/HTML were verified and retained.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none; unresolved behavior remains explicitly blocked rather than inferred.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Goal objective, root router, context map, worklog README/template and selected exact-type AD-01/AD-02/AD-03 worklogs reviewed; ST-09 dependency worklog reviewed. | VERIFIED |
| Scoped context/registry review | Project boundary pages, Web/Study Web and Server Study entries reviewed; manifest excludes API DD skill for UI-only DD and marks Study OpenAPI `NOT_FOUND`. | VERIFIED |
| Scoped source and contract review | `list_screen.md`; AC API index and extracted AC-14/15 diagram; API catalog rows #22–#24 and API DD/open questions; Study Server router/modules/tests search; API #09 query/view/router; ST-09/ST-11 DD; both Study DDLs/database context; Study Web source inventory; ST-10 static assets. | VERIFIED |
| ST-10 artifact audit | 21 ordered JSON markers ↔ 21 DD rows; SVG has 21 circles/numbers/leaders with geometry matching JSON; embedded source PNG SHA-256 matches original; annotated dimensions 3372×3200; source image 1566×1600 and source HTML hashes unchanged; visually reviewed. | VERIFIED |
| DD and link audit | Explicit A–F sections; 10 sequential event IDs; local Markdown links resolve; JSON/XML parse; current inventory/folders 83/83 and core artifacts 82/83 (ST-01 incomplete). | VERIFIED |
| Whitespace and scope check | `git diff --check` passes for tracked `list_screen.md` and `dd_screens/PLAN.md`; authored-text scan found no trailing whitespace in ST-10 DD/plan/worklog or global plan. Four trailing-space lines at start of `list_screen.md` predate and are outside changed hunks. No application tests/runtime/live DB check. | VERIFIED |

## HANDOFF

- Remaining blockers: #22 entitlement/JWT/reason/404; #23 approved schema/upsert/idempotency/transaction/response; #24 direct-call entitlement/publish/projection/error/null semantics; ST-09 lessonId handoff; #24 ownership across ST-10/ST-11; Study Web route/source.
- Next owner/action: ST-10 remains DD BLOCKED / IMPLEMENTATION BLOCKED / RUNTIME NOT VERIFIED. Stop this session; ST-11 may be processed only in a separate session.
