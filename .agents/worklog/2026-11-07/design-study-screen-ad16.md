---
task_id: "2026-11-07-design-study-screen-ad16"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-35; APIs #88/#89; AD-15 → AD-16; AD-16 → AD-17 handoff"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-16

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 221; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current separate; preserve source assets; trace route, auth, DB, response and tests; keep Study Web `UNWIRED`; no runtime claim from mockup or API source.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Do not infer body fields, permissions or behavior from screenshot; API catalog and local implementation may differ; fake DB tests do not prove schema/deployment.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Keep API and UI status distinct; preserve Admin permission and PII/security gaps; UI-only DD has no canonical skill.
- additional handoff reviewed: `.agents/worklog/2026-11-07/design-study-screen-ad15.md` — AD-15 finished; one Screen ID per session; AD-16 is next; keep #87 catalog/source discrepancy separate and do not claim runtime.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-16 only. Read `goal-objective.md`, router/context and selected docs worklogs; inspect AD-16 source assets, inventory row 74, AC-35, API #88/#89 catalog and Draft DD plus current source/tests; write `AD-16_PLAN.md` before marker map, annotation or screen DD; preserve original `screen.png`/`code.html`; produce ordered one-to-one markers, `screen_annotated.png`, A–F DD, inventory/API reverse-index/global-plan updates and this worklog; stop before AD-17.
- AD-16 is the proposed quiz builder for creation (#88) and editing (#89). Expected actor is Admin with quiz-management permission under AC-35. Inventory proposes `/admin/quizzes/new` or `/admin/quizzes/:quizId/edit`, links back to AD-15 and onward to AD-17, and expects dirty/invalid/saving/created/conflict states.
- Direct catalog #88: `POST /api/v1/admin/quizzes`, Bearer JWT/Admin, body `{config:string!, questions:string!}`, `ApiEnvelope<Quiz>`, HTTP 201 and 401/403/422/500. Direct catalog #89: `PUT /api/v1/admin/quizzes/{quiz_id}`, Bearer JWT/Admin, path `quiz_id:int64!`; catalog declares no body, direct `ApiEnvelope<Quiz>`, HTTP 200 and 401/403/404/422/500. Both API DDs remain `Draft — Needs Confirmation`.
- Do not treat #88 embedded JSON fields or #89 body/replacement/history behavior as owner-approved. Do not infer quiz detail, course options, question builder controls, autosave, route navigation or permission policy from static copy.

## CURRENT_BEHAVIOR

- Source assets: AD-16 folder `apps/study-client/docs/screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/` initially contains only `screen.png` (1600×1402; SHA-256 `d8495b7625c4668957fd54df8a500e71b31e374c99e61895e6d450cdd3f7894f`) and `code.html` (21,782 bytes; SHA-256 `adf60f52ab9e16ad71d90ba14e1deab1d1e4db1a18c5effbd403d3ea356c403d`). Prototype has a blank Quiz configuration, a course select with only its placeholder, a blank Questions section, disabled Add Question and Save buttons, a Cancel hash link and static shell/footer. No `<form>`, validation listener, fetch/XHR, API call, router or local-storage autosave exists; no control is populated from an edit ID.
- Static claims include local draft autosave, RBAC confirmation, “System Normal”, schema sync/Questions Builder Gate, and temporary question lock. These are not current API/runtime signals. Duration input advertises HTML min=1/max=300; passing grade min=0/max=100. API #88/#89 validators only apply storage limits and do not define those business ranges. Course select has no options. Question builder has no Question/Choice controls; both create and update need a question set in local implementation.
- Study Web root currently contains `docs/`, ignored `dist/`, `node_modules/` and build metadata; editable source, package manifest, router and API client are absent. Screen status `UNWIRED`; serving/runtime unverified.
- API #88 has local route/module/query/model/validator/test source. Route reads raw body; shared `ADMIN` authentication runs before body parsing/DB. Local fallback strictly requires outer strings `config` and `questions`, decodes JSON, validates a DERIVED `{course_id,title,duration_minutes?,passing_score}` + `questions:[{text,type,choices:[{text,is_correct?}]}]` shape, with QuestionType `SINGLE_CHOICE|MULTIPLE_CHOICE|TRUE_FALSE`; course must exist. It inserts Quiz and ordered Question/Choice rows, maps a full Admin Quiz response including `is_correct`, then commits; errors rollback. Embedded schema, type/order migration and business limits remain DERIVED; fake DB tests do not verify live schema/deployment.
- API #89 has local route/module/query/model/validator/test source and dynamic path registration. Shared ADMIN auth runs before raw path/body parsing and DB. Local fallback requires a positive int64 path and reuses #88 body validation; then locks active Quiz, current Questions/Choices, rejects any attempt or answer history with 422, verifies/locks target Course, updates Quiz metadata/course, replaces old Choices then Questions, inserts replacements in request order, maps response before commit. It keeps Quiz status and `created_at`; body, full replacement, course move, history guard, locks and tombstone behavior are DERIVED. Catalog #89 is path-only; no GET admin Quiz detail exists, and #87 list returns metadata-only `questions=[]`, so edit prefill cannot be established.
- Prior API test report in `.agents/server-study/tests.md`: #88 focused 21 passed, #89 focused 26 passed, linked/full-suite results recorded at their checkpoints. These fake-session tests were read/referenced, not run in this screen-design session; live PostgreSQL, migration deployment and lock/FK behavior remain unverified.

## SOURCE_TRACE

```text
Expected: AC-35 Admin with quiz-management permission → create via #88 or update via #89 → show result; AD-16 is entered from AD-15 and may hand off back to AD-15/AD-17, but post-save route is not defined.
Current: no Study Web caller/route/client → Study Server #88/#89 routes → shared ADMIN guard → raw body/path validation → legacy BIGINT Quiz/Question/Choice queries. #88 checks Course then inserts parent/children and commits; #89 locks Quiz/children, checks attempt/answer history, checks Course, updates parent, child-first replaces the set and commits. Both return Quiz projections with Admin answer keys; all validation/projection/query/commit failures follow their local 401/403/404/422/500 paths and rollback where a transaction has begun. Tests use fake DB sessions.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Edit initialization | Inventory proposes an edit route; no GET admin Quiz detail exists. #87 returns a page with empty `questions=[]` and no validated detail projection. | `BLOCKER` | Cannot safely prefill or submit an existing Quiz from an ID using current contracts. |
| API #89 request | Catalog and AC give path only; local source requires #88-style config/questions body and full child-set replacement. | `DISCREPANCY / DERIVED` | Do not represent local fallback as direct contract; owner approval needed. |
| Question builder | Screenshot/HTML has no question/choice controls and Add Question is disabled; #88/#89 current local body includes question set. | `UNWIRED / BLOCKER` | The primary nested quiz data cannot be entered; Save remains disabled in prototype. |
| Form validation | Mockup says title/course required, duration 1–300, score 0–100; API local validation has no title minimum, duration positive/max-300 rule, or passing-score business range. Course is numeric ID; UI option source is absent. | `DISCREPANCY / BLOCKER` | Do not silently adopt mockup ranges/mapping as business rules. |
| Permission/schema/answers | AC-35 fine-grained quiz-management permission is SOURCE_REQUIRED; source checks shared `ADMIN`. Legacy BIGINT/migration 013 vs V1-PILOT UUID model; live schema unverified. Admin response includes `is_correct`; Student API #28 must omit it. | `OPEN / BLOCKER` | Security and physical persistence require owner/live review; protect answer-key boundary. |
| Autosave/navigation/runtime | “Autosave”, safety, auth, readiness and gate messages are static; no local storage or client code. Cancel points to `#/admin/quizzes`, but router is absent; post-save behavior not specified. | `UNWIRED / STATIC_ONLY` | Do not claim persistence, RBAC, routing or autosave. |

## CHANGES

- Saved `AD-16_PLAN.md` before creating any marker/annotation/DD artifact. The plan records expected AC-35/create/update behavior, verified current source, marker plan, events and blockers.
- Created `AD-16_markers.json` and `AD-16_markers.svg` with 35 ordered markers and `screen_annotated.png` at 3200×2804 (2×). Source `screen.png` and `code.html` were not edited. An initial SVG rasterization was opaque white; this was corrected by rendering with transparent background and compositing over the 2× source image, then visually inspected.
- Authored `AD-16.md` with A–F, 35 marker-to-element rows, EV-01…EV-10, API catalog vs local source distinctions, states, navigation and blockers.
- Updated inventory row 74, shared blocker G-11 and API reverse index #088/#089 from D→R based on local route/module/query/model/validator/test-source existence. API DDs #88/#89 remain `Draft — Needs Confirmation`.
- Updated global screen plan AD-16 row and appended AD-16 checkpoint; static inventory audit confirms core artifact count 69/83.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none; unresolved #88/#89 proposals remain blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective path reviewed; root router, `.agents/AGENTS.md`, context map, worklog contract/template and manifest registry reviewed; exact docs selector READY 3/221; AD-01/02/03 plus AD-15 handoff read. | VERIFIED |
| AD-16 expected/current inspection | Inventory row 74, AC-35 index/diagram, API #88/#89 catalog and Draft DD, Study Web tree, PNG/HTML, route/module/query/models/validators, test sources and prior test report reviewed. | VERIFIED_SOURCE_REVIEW |
| Plan-before-authoring order | `AD-16_PLAN.md` existed before marker JSON/SVG, annotated PNG and DD authoring. | VERIFIED |
| Static artifact audit | 35 markers sequential/unique/in-bounds/non-overlapping; JSON=SVG=DD §C coordinates; SVG XML/JSON parse; source hashes unchanged; annotated PNG 3200×2804; 21 DD links resolve; inventory 83/83 unique IDs and folders, core artifacts 69/83. | PASS |
| Visual annotation review | Full annotated image inspected; source UI remains visible, numbering is legible, and no marker obscures important field/Question text. | PASS |
| Whitespace | `git diff --check` passed; new AD-16 artifacts checked for trailing whitespace. | PASS |
| Application tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining work: none for AD-16 in this session; stop before AD-17.
- Remaining blockers: #89 body/detail route, builder controls and field contract, course option mapping, validation ranges, AC-35 permission, live schema/QuestionType migration, edit history policy and Study Web wiring.
- Next screen after AD-16, in its own session: AD-17. Do not start it here.
