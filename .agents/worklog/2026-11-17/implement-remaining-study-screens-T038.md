---
task_id: "2026-11-17-implement-remaining-study-screens-T038"
date: "2026-11-17"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work (Study Web)", "server-study"]
cross_scope_dependencies: ["83 Study screen IDs -> existing Study Server API IDs/source; design-only or unavailable endpoints remain gated"]
status: "DONE_WITH_LIMITATION"
---

# Worklog: Implement the remaining Study screens — T038

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 148 available; T011, T012 and T013 selected and read fully; no shortage.
- prior_worklogs_reviewed:
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T011.md`: preserve AD-22/#97 report-metadata, permission, live-schema and AD-23 handoff gates; fake-session/browser evidence does not prove live runtime.
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T012.md`: overall scope is all 83 Study screens; preserve source/DD/runtime distinctions and user dirty state; do not infer API behavior from catalog alone.
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T013.md`: keep Draft API behavior gated, preserve signed int64 IDs as strings, and update process per continuation.
  - `.agents/worklog/2026-11-17/implement-study-screens-apis-T037.md`: completed AD-12 CSS-only slice; #82 caller exists but cardinality/filter/pagination/permission gates remain; tests/build pass, authenticated browser/live DB unverified.
- baseline: `git status --short apps/study-client apps/study-server` reported 664 entries before this continuation's tracker/worklog updates. `docs/tasks/process.md` is untracked; `dd_screens/screen-index.md` and many screen DD/source files are already dirty. Preserve existing changes and inspect exact target diffs before every edit.

## EXPECTED_BEHAVIOR

- User request: implement the remaining screens described by Study screen DD/inventory, associate them with their existing server API IDs, and match DD logic/UI with `screen_stitch` references where useful.
- Scope confirmed in conversation: use the 83 inventory IDs (Page, Tab, Dialog, Panel, Transition); implement only missing/partial behavior and keep already accepted work unchanged.
- API policy confirmed in conversation: wire only APIs with current source-backed behavior; screens depending on design-only, unavailable or unresolved API behavior keep a safe gate and no HTTP caller until source/contract is ready. Do not create API endpoints, schema or business rules for this continuation.
- UI policy: DD describes expected behavior; screen_stitch provides source visual/asset evidence; current Study Web architecture, semantic tokens and accessibility conventions apply. Preserve discrepancies instead of silently reconciling them.
- The overall project tracker remains approximately `20% ACTIVE`; that number is a coarse estimate, not an exact screen-completion count.

## MILESTONES

### Continuation milestones — 2026-11-17 resume

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 15% | 15% | Re-run coding preflight; read selected worklogs, scope rules/workflow; inspect actual status/routes and target DD/source. | `DONE` |
| 40% | 55% | Wire read-only API #04 in ST-02/ST-03 through `StudentApiService`; render only source-backed fields, preserve ST-03 mutation gates. | `DONE` |
| 30% | 85% | Reconcile stale ST-02/ST-03 and handoff/source-current documentation plus the 83-screen matrix against actual current callers. | `DONE` |
| 15% | 100% | Run permitted build/diff/context verification and record exact results/limits in this worklog and `task_finish.md`. | `DONE_WITH_LIMITATION` |

Continuation progress starts at 0%; it is tracked separately from the stale
historical T038 checkpoint below. The broad implementation estimate is not a
screen acceptance percentage.

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 10% | 10% | Complete coding preflight; read selected prior worklogs; inspect current continuation, task tracker and dirty-state baseline. | `DONE` |
| 15% | 25% | Finish current T037/AD-12 verification and update its worklog/process row with actual results and runtime limits. | `DONE_WITH_LIMITATION` |
| 60% | 85% | Build a source-backed gap crosswalk for all 83 IDs and implement each missing/partial screen through waves W0–W4; keep unsupported API-dependent behavior gated. | `DONE_WITH_LIMITATION` |
| 15% | 100% | Run scoped final verification; synchronize screen DD/index/context/process/worklogs; record remaining gates and runtime limits. | `DONE_WITH_LIMITATION` |

**Current T038 progress: 100% implementation/closeout. Overall project objective: `20% ACTIVE` (coarse tracker estimate). Remaining product/API gates and browser/live API/DB validation are outside the completed source-backed slice and remain explicitly unverified.**

## EVENT_LOG

| Event ID | Operation / target | Result |
|---|---|---|
| S01.A01.E01 | RUN `node scripts/select-worklogs.mjs --type coding --limit 3` | `READY`; selected T011, T012 and T013. |
| S01.A02.E01 | READ T011–T013 worklogs | Loaded carry-forward constraints for gates, dirty state and runtime evidence. |
| S01.A03.E01 | READ T037 and process continuation state | Confirmed AD-12 M0/M1 complete and M2 was the current open continuation. |
| S01.A04.E01 | INSPECT baseline/AD-12 target paths and package scripts | 664 dirty entries across Study client/server; AD-12 HTML/TS/spec already dirty; T037 stylesheet was the owned CSS slice. |
| S01.A05.E01 | RUN focused AD-12 Angular and API #82 tests | Angular 4/4; API #82 FakeSession 15/15 with one upstream deprecation warning. |
| S01.A06.E01 | RUN production build and scoped style/diff checks | Build passed with three existing Student CSS budget warnings; Prettier/no-hex/diff checks passed. |
| S01.A07.E01 | INSPECT CUA browser inventory | No browser/app surfaces available for visual verification. |
| S01.A08.E01 | RUN local `/admin/lessons` smoke check | HTTP 200; Angular dev server was stopped after the check. |
| S01.A09.E01 | UPDATE T037 completion and start T038 | T037 marked `DONE_WITH_LIMITATION`; broad 83-screen continuation opened at 25%. |
| S02.A01.E01 | READ 83-ID inventory/index and route/page/caller source | Generated [the source gap matrix](T038-screen-gap-matrix.md), with route/page structure, assigned API IDs, numbered server route evidence and feature-local FE callers for all 83 IDs. The matrix is structural, not acceptance evidence. |
| S02.A02.E01 | READ ST-02 DD package and Stitch sources | Read all eight DD pages, both PNGs, image README, source HTML, plan, markers and source DD. Confirmed clean PNG body is blank while HTML-derived reference contains a sign-in gate; profile-ready UI is not specified. |
| S02.A03.E01 | TRACE ST-02 route/API/auth | API #04 currently reads Student profile by Bearer JWT; client has no Student session/token provider. Keep #04 assigned but do not call it or fabricate profile-ready fields. |
| S02.A04.E01 | IMPLEMENT ST-02 gate route and screen | Added `/student/profile`, page and four-folder screen package; route metadata assigns #04; edit stays disabled. Added a `custom` Student shell mode and host-scoped CSS. |
| S02.A05.E01 | UPDATE ST-02 source status and context | Updated the inventory, DD index/package, Study Web context and architecture note to distinguish the route gate from an authenticated/API-backed profile. |
| S02.A06.E01 | RUN focused ST-02 checks | Angular 2/2, Prettier and scoped diff check pass; production build passes with only the three pre-existing Student CSS budget warnings. Browser/authenticated rendering not available. |
| S02.A07.E01 | READ ST-03 DD and Stitch package | Read the eight DD pages, image README, clean/numbered PNGs, Stitch HTML, plan and markers. Confirmed G-03 is the only designed UI state and upload/save/phone/bio remain gated. |
| S02.A08.E01 | TRACE ST-03 server API and client auth source | #04 returns safe profile without bio; #13 accepts JSON Data URL, uploads to object storage and returns `avatar_url`; #14 updates `full_name`/`phone`/`avatar_url`, ignores `bio`, and returns the updated profile. Study Web has no Student session/token provider. |
| S02.A09.E01 | IMPLEMENT ST-03 gate page and route mapping | Added `/student/profile/edit`, four-folder page package, responsive host-scoped UI, API #04/#13/#14 route metadata, and ST-02 RouterLinks. No API caller was added; upload/save and conflicting fields remain disabled. |
| S02.A10.E01 | UPDATE ST-03 DD/index/context/worklog | Updated current-source notes, gap matrix, Study Web context, architecture source status, and tracker to label the screen `GATE_ONLY / PARTIAL`, not authenticated/API-backed. |
| S02.A11.E01 | VERIFY ST-03 slice | Focused route/page tests 4/4; production build pass with only the three existing Student CSS budget warnings; Prettier and scoped `git diff --check` pass. No browser/authenticated API runtime was available. |
| S02.A12.E01 | RUN context validator | `AGENT_CONTEXT_INVALID`, exactly the prior baseline: 1,431 lines, SHA-256 `7496126958d348bb35ec8a7df9ca7228326ba4735b79536b28119e6d26afe9e0`; no ST-03/T038 findings. |
| S02.A13.E01 | RE-READ current API #15 route/module/query/model/test source | Found current #15 route and tests despite stale DD/catalog status. A valid Student Bearer selects that user; absent or invalid Authorization falls back to the latest enrollment for any user in the course. Kept #15 uncalled and recorded the security discrepancy. |
| S02.A14.E01 | IMPLEMENT ST-04 route/page and #08 integration | Added `/student/enroll/:courseId`, route metadata #08/#15, and a #08 caller reused from GS-03. A published course reaches the Stitch gate; #08 404/error states remain distinct; no #15 request or enrollment branch is enabled. |
| S02.A15.E01 | VERIFY ST-04 | Focused ST-04/Student route tests passed 5/5; production build passed with the same three existing Student CSS budget warnings. |
| S02.A16.E01 | UPDATE ST-04 DD/index/context and gap matrix | Updated current-source status, marked #15 `R` but unsafe optional-token fallback, recorded ST-04 as partial, and refreshed Web/Study Server context. Structural counts became 54 route/page and 25 not started. |
| S02.A17.E01 | READ ST-05 DD/Stitch/server sources | Read its eight DD files, source plan/markers/HTML-derived render and current #16 route/model/validator/query/view. #16 source validates Student auth but writes to `orders`, absent from checked-in DDL; no focused #16 tests were found. |
| S02.A18.E01 | IMPLEMENT ST-05 route/page and #08 integration | Added `/student/checkout/:courseId`, metadata #08/#16, responsive Stitch-derived unavailable state and #08 revalidation. #16 remains uncalled because its descriptor is `UNWIRED` and persistence/provider/amount contract is unverified. |
| S02.A19.E01 | VERIFY ST-04/ST-05 slice | Focused tests passed 8/8; production build passed with the same three existing CSS budget warnings. |
| S02.A20.E01 | UPDATE ST-05 DD/index/context and gap matrix | Recorded #16 as partial route source with missing checked-in table/tests, updated screen/index/context/process notes, and changed structural counts to 55 route/page and 24 not started. |
| S03.A01.E05 | READ agent-control and active T038 worklog plan | Confirmed 10/15/60/15 milestone weights, current progress 25%, and that the log's handoff predates the current Student/Mentor source changes. |
| S03.A01.E06 | READ T038 implementation/current behavior sections | Confirmed Mentor plan exists but Student ST11–ST26 and Mentor implementation are absent from recorded changes; current-behavior and handoff summaries need synchronization. |
| S03.A02.E08 | UPDATE Student route/model/layout | Added ST13 API metadata #28/#29; made ST16 answer DTO required; removed redundant Student portal width declaration. |
| S03.A02.E09 | SPLIT Student API stylesheets | Split common/learning/community styles and assigned them to ST11–ST26 components; corrected parser boundaries after the first build reported malformed CSS. |
| S04.A01.E11 | RUN Study Web production build | TypeScript/templates compiled; build reported malformed CSS split and budget warnings. |
| S04.A01.E12 | READ split CSS boundaries and dirty-file status | Identified `result-failed` split and duplicate media opener; no files restored from Git. |
| S04.A01.E13 | APPLY exact CSS patch | First patch context did not match because table cells shared a selector; no file changed. |
| S04.A01.E14 | READ exact CSS selector blocks and screen usage | Confirmed unused table/h3 rules and cross-screen icon class usage. |
| S04.A01.E15 | REPAIR CSS rules and remove unused selectors | Restored full learning/community rules and moved common icons to the shared base style. |
| S04.A01.E16 | RUN Study Web production build | Exit 0; CSS parses, new shared styles have no budget warnings; existing bundle/layout/static/Mentor/ST22 warnings remain. |
| S03.A03.E17 | READ inventory, screen index, DD and Web context status | Found ST11–26 source-status text and Web context stale; DD expects/current behavior must remain separated. |
| S03.A03.E18 | READ precise inventory/matrix rows | Confirmed stale `NOT_FOUND` descriptions in current inventory and empty FE caller column in structural matrix. |
| S03.A03.E19 | READ representative ST API DDs and source matrix | Confirmed DD API excerpts are historical relative to current Student source; matrix source/test states need refresh. |
| S03.A03.E20 | INVENTORY Student/Mentor API wrappers and routes | Found screen-local wrappers for Student ST11–25 and Mentor routes/pages; wrappers alone do not prove enabled UI calls. |
| S03.A03.E21 | READ current API source/test status and inventory schema | Confirmed #31 and #35–45 have no focused server tests; #34 test is in Shared; Mentor source ledger was stale. |
| S03.A03.E22 | INVENTORY focused server test packages and current descriptors | #34 and #32/#33 test packages exist; #31/#35–45 do not; #43–45 are SOURCE_ONLY in the client. |
| S03.A03.E23 | TRACE Mentor source routes and FE call gates | Current `app/api/v1.py` has #46–67 route source; #46–67 descriptors are WIRED; ME04 and ME14 remain UI-gated. |
| S03.A03.E24 | INVENTORY Mentor focused test packages | Focused Mentor test files exist for #46–67. |
| S03.A03.E25 | READ current list-screen summary and row structure | Found stale statements that ST routes/Mentor group are absent and that Student #13+ is design-only. |
| S03.A03.E26 | READ structural matrix counts and known gaps | Baseline is 61 route+page, 3 tabs, 1 page-only, 18 not-started; the latter are ME01–18. |
| S03.A03.E27 | READ Mentor gated-action templates with wrong path | Wrong paths returned file-not-found; no source changed. |
| S03.A03.E28 | READ exact Mentor action templates and handlers | ME04 #34/#47 and ME14 #63 are disabled; ME07 #50/#51 follow current request model; ME08 actions have explicit confirmation and server checks. |
| S03.A03.E29 | UPDATE inventory and 83-ID matrix rows | Updated ST11–26 and ME01–18 current caller/gate descriptions; structural counts now 79 route+page, 3 tabs, 1 page-only, 0 not-started. |
| S03.A03.E30 | READ updated inventory/matrix rows | Rows and delimiters are valid; inventory overview paragraph and some matrix known-gap text remain stale due an in-memory writer issue. |
| S03.A04.E31 | READ current ST01/ST08/ST09/ST10 pages | Confirmed all four remain static; ST10's expected API sequence exists only as explanatory copy. |
| S03.A04.E32 | TRACE #20/#22–#24 and frontend course DTO/service patterns | #20 is paged CourseSummary; Student course fields match the response subset; further route/query review needed. |
| S03.A04.E33 | TRACE #22/#23/#24 route/module/model/view source | #22 is Student/auth + course/enrollment check; #23 is Student/auth + enrollment + progress upsert; #24 checks published lesson/course and enrollment. |
| S03.A04.E34 | TRACE #22/#23 query predicates and UI styles | #22 query does not itself filter lesson status; #23 is an upsert but lacks its own publication check. Client must gate on #22's returned `status` before explicit Start; backend discrepancy remains noted. |
| S05.A01.E35 | RE-RUN coding selector and READ selected logs | Selector `READY`, 149 available; T038/T011/T012 selected and read. No shortage. |
| S05.A02.E36 | READ ST-02/ST-03 DD, Stitch images, FE session/transport and #04 source | Confirmed #04 allowlisted profile and Student Bearer path; implementation scope is read-only; preserve ST-03 mutation gate. |
| S05.A03.E37 | IMPLEMENT ST-02/ST-03 #04 callers | Added screen services/shared DTO and loading/error/retry; rendered only `full_name`/`email`; ST-03 #13/#14 remain uncalled. |
| S05.A04.E38 | UPDATE inventory, architecture, DD, context and matrix | Removed stale no-session/no-caller claims from current-source notes; expected DD and runtime blockers remain separate. |
| S05.A05.E39 | RUN permitted final verification | Production build, source Prettier, and `git diff --check` pass with recorded bundle/CSS budget warnings; tests not run. |
| S05.A06.E40 | RUN context validator and closeout | Standard and `--skip-drift` remain invalid on repository-wide baseline findings; no static Study Web/ST02/ST03 findings under `--skip-drift`. Updated progress to 100% implementation/closeout and recorded remaining gates in `task_finish.md`. |

## CURRENT_BEHAVIOR

- Screen inventory: `apps/study-client/docs/list_screen.md` and `docs/dd_screens/screen-index.md` describe 83 screen surfaces; surfaces are not equivalent to independent routes. All 83 DD packages exist, but package existence does not establish implementation completeness.
- Structural source gap matrix: [T038-screen-gap-matrix.md](T038-screen-gap-matrix.md) maps all 83 IDs to page/route structure, inventory API IDs, numbered server route-source status and feature-local FE callers. It shows 79 route/page surfaces, 3 parent tabs, 1 page-only component and 0 IDs without a page/route; these counts are structural, not acceptance.
- StudentLayout now authenticates a Student through API #03, checks the role and retains tokens in tab memory. ST-02 calls #04 read-only through `StudentApiService`, displays `full_name`/`email`, and retains disabled edit behavior.
- ST-03 calls #04 read-only and binds `full_name`/`email` in readonly fields. It remains the G-03 write gate: #13/#14 have route metadata but no caller; upload/save and phone/bio are disabled. Avatar/bio/phone/reload discrepancies remain.
- ST-04 is source-wired at `/student/enroll/:courseId`. It calls public #08 and maps published/not-found/error states; route metadata assigns #08/#15. It does not call #15 because current server code falls back to any course enrollment when Authorization is absent or invalid. Student auth and enrollment branching remain gated.
- ST-05 is source-wired at `/student/checkout/:courseId`. It calls #08 then renders the Stitch unavailable checkout state; route metadata assigns #08/#16. It sends no #16 request because the client descriptor is UNWIRED, checked-in DDL lacks `orders`, no focused #16 tests were found, and Student/provider/amount/persistence behavior remains unverified.
- Existing implementation footprint: 88 Angular `pages/*.ts` files were found before ST-02; route declarations and API callers vary. Current worktree is highly dirty, so page-file counts are not used as completion evidence.
- Study Server: the project exposes a 103-ID API catalog, but some IDs are design-only or unresolved; #99–#103 currently have no local route source. Mentor routes exist for #46–#67. API ID references alone do not prove a screen caller or live runtime.
- T037/AD-12: current source route/page/#82 caller exists; API DD/catalog cardinality, unsupported filters/paging, fine-grained permission and live schema remain gated. Angular 4/4, API #82 fake-session 15/15, production build passed with three pre-existing Student CSS budget warnings, and `/admin/lessons` returned HTTP 200. Authenticated visual/runtime and live DB were not verified.
- T038 implemented source-supported callers for Student ST-01–ST-25 and Mentor ME-01–ME-18, with unsupported actions gated. ST-02/ST-03 call #04 read-only; ST-04/ST-05 call public #08 while #15/#16 remain gated. No Study Server code/API/schema was changed in this task.

## SOURCE_TRACE

```text
83-screen inventory and screen-index
  -> [83-ID structural gap matrix](T038-screen-gap-matrix.md)
  -> per-ID DD + matching screen_stitch source/plan/markers/HTML/PNG
  -> existing Angular route/page/data-access/UI and API descriptor/caller
  -> Study Server route/module/query/model/test source where available
  -> source-backed caller or explicit gated state; no invented API behavior
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Screen count vs route count | Inventory has 83 Page/Tab/Dialog/Panel/Transition IDs; routes are only one possible implementation for a Page. | `VERIFIED_INVENTORY` | Build the gap matrix by stable screen ID, not by URL/page-file count. |
| API catalog vs implementation | Some API IDs lack current route source; #99–#103 are absent; Mentor #46–#67 routes are present. | `DESIGN_ONLY / UNWIRED` | Do not create callers for missing APIs; keep dependent screens gated. |
| API DD vs current source | Several screen/API DDs are Draft or disagree with local response/permission behavior. | `DISCREPANCY` | Use current source for current behavior; preserve expected behavior and gate unsupported actions. |
| ST-02 API assignment vs caller | Current FE route metadata assigns #04; `ST02ProfileService` calls GET #04 and the page renders only `full_name`/`email` with loading/error/retry. | `PARTIAL SOURCE / READ_ONLY WIRED` | Edit stays disabled; no avatar, role/status authorization, bio or permissions are rendered. Visual acceptance beyond the supplied profile-safe fields remains limited by the blank clean design reference. |
| ST-03 API assignment vs caller | Current FE route metadata assigns #04/#13/#14; `ST03ProfileService` calls GET #04 and binds only `full_name`/`email` as readonly. #14 ignores bio, phone/avatar are nullable, and #13/#14 upload/update consistency remains open. | `PARTIAL SOURCE / READ_ONLY WIRED` | #13/#14 remain uncalled; upload/save/phone/bio stay gated until data contract decisions are resolved. |
| ST-04 API #15 route vs contract | Current Study Server has #15 route/module/query/model/test. Valid Student token binds user, but absent/invalid token falls back to latest course enrollment for any user; FE descriptor remains UNWIRED. | `DISCREPANCY / SECURITY GATE` | ST-04 calls only public #08; never branch from #15 until identity/selection is corrected and approved. |
| ST-05 API #16 route vs persistence | Current Study Server has #16 route/module/query/model but no focused tests; code writes to `orders`, absent from checked-in DB DDL. FE descriptor remains UNWIRED. | `PARTIAL_SOURCE / SCHEMA GATE` | ST-05 revalidates with #08 and renders unavailable checkout; no order mutation until storage/auth/provider/amount contract is verified. |
| ST-10 API #22/#23 publication checks | #22 verifies published course/enrollment but does not filter lesson status; #23 checks enrollment and upserts progress but has no publication predicate. | `DISCREPANCY / CLIENT GATE` | Client requires `status=PUBLISHED` from #22 before explicit #23; ST-11 revalidates through #24. This does not repair the server-side discrepancy. |
| Existing dirty state | 664 short-status entries were present in the two application scopes; process and screen-index files already have user-owned changes. | `PRESERVE` | Inspect and edit only exact gap files; do not clean, reset or overwrite unrelated changes. |
| Runtime evidence | Tests use fake sessions for many APIs; CUA inventory currently has no browser surface; live schema/deployment is unverified. | `NOT_VERIFIED` | Do not claim deployed or authenticated visual behavior based on unit tests/local HTTP 200. |

## IMPLEMENTATION_PLAN

### Continuation plan — read-only profile API slice and handoff reconciliation

1. Keep the existing StudentLayout/API #03 session and use `StudentApiService`
   for protected calls. Add typed #04 profile response access in ST-02 and
   ST-03 screen-local data-access services; share only the response type under
   Student shared models.
2. ST-02 requests #04 at page entry and renders loading, service-error/retry,
   and a read-only profile card using only `full_name` and `email`. Do not
   render `avatar_url` as an image, `role`/`status` as authorization state,
   `bio`, `permissions`, or sample identity. Keep the edit control disabled as
   specified by the source screen asset.
3. ST-03 requests #04 and binds `full_name`/`email` into read-only controls.
   Keep #13 upload, #14 save, phone, bio and all G-03 diagnostic gates closed;
   no profile write or avatar side effect is introduced.
4. Update inaccurate current-source statements that claim there is no Student
   session or no #04 caller, while retaining the DD's design/schema blockers and
   distinguishing caller source from browser/live API runtime evidence.
5. Reconcile the current handoff and screen/API matrix/docs. Run the Study Web
   production build, `git diff --check`, and the context validator because
   canonical context pages are expected to change. Do not run tests in this
   continuation unless requested.

### Reuse check

- Reuse existing Student role/session and Bearer transport at
  `core/auth/student-session.service.ts` and
  `core/http/student-api.service.ts`.
- No existing profile API screen caller or neutral profile presentation
  component exists; keep request orchestration screen-local and share only the
  exact API #04 response type.

1. Enumerate all 83 stable IDs from the inventory/index and compare each against current route, page/component, data-access caller, API descriptor/source, DD, and prior worklog. Record `COMPLETE`, `PARTIAL`, `GATE_ONLY` or `NOT_STARTED` only from source-backed evidence; do not use the coarse 20% estimate as a count.
2. Execute remaining items in the inventory's W0–W4 order. Within a wave, implement parent Page before its dependent Tab/Dialog/Panel/Transition, and skip screens that meet acceptance.
3. For each screen, read the full eight-page DD package and matching screen_stitch source, plan, markers, HTML and visual assets; trace the current API route/view/query/model/tests before adding a caller. Follow the four-folder Study Web feature convention for page features; embed non-route surfaces under their parent route.
4. Use an existing source-backed API only for the exact behavior it currently supports. Keep unsupported filters, mutations, permissions, fields and unavailable APIs disabled/gated with honest copy; add no server endpoint, schema migration or invented response shape.
5. Match screen structure and visual intent to DD/Stitch while using current Study tokens, responsive layout, focus states and accessible controls. Preserve original Stitch assets.
6. Build the Study Web app after implementation waves; do not run test suites unless requested. Perform visual comparison when a browser is available. Update only relevant DD/current-source index/context/tracker/worklog. Use `git diff --check`; run the context validator after canonical context pages change and compare with the repository baseline.

### Mentor implementation plan — W3

- Scope: `ME-01..ME-18`; proposed routes and API assignments are from
  `apps/study-client/docs/list_screen.md` and the 18 screen DD packages.
- Reuse check: no Mentor route, layout, session, API adapter, or shared Mentor
  shell exists. Reuse `StudyApiService` and the verified API #03 login/refresh
  response contract; create a Mentor-only ephemeral `MentorSessionService` and
  `MentorApiService` rather than weakening the Admin role check. Reuse existing
  `StudyIcon`; do not import Admin/Student feature code.
- Group wiring: add `features/mentor/mentor.route.ts` and
  `layouts/mentor/mentor-layout.*`; keep a Mentor role sign-in form in the
  group shell, session tokens in tab memory, and server-side role/owner checks
  authoritative. Never put IDs/tokens in query strings.
- API mapping: ME-01 #46/#54/#58; ME-02 #46; ME-03 #49/#65; ME-04 #46/#34/#47;
  ME-05 #48; ME-06 #49; ME-07 #49/#50/#51; ME-08 #49/#52/#53; ME-09 #54;
  ME-10 #55/#56/#57; ME-11 #58; ME-12 #59/#60/#61; ME-13 #46/#62;
  ME-14 #63; ME-15 #64 only (not #18); ME-16 #65; ME-17 #67; ME-18 #66.
- Per-screen shape: create exactly `data-access/`, `models/`, `pages/`, and
  `ui/` direct folders; route API IDs are recorded on the route data. Pages own
  loading/error/empty/success state and events; screen services call the
  Mentor API adapter; typed models mirror current source projections.
- Safe behavior: implement only source-backed response fields and current
  request schemas. Keep ME-04 lecture create, ME-07/#51 update, ME-08 transition
  actions, ME-14 dispatch and ME-15 batch handoff blocked wherever DD/API
  mismatches remain; show exact blocker copy. Do not render Stitch sample
  identities, KPIs, dates, SLA, ratings, chart series, or operation/notification
  ID conflations. Use ME-13 selected course/recipient IDs only for the in-app
  next-screen handoff; server remains authoritative.
- Visual plan: use the Stitch clean/numbered image pairs and matching
  `screen_stitch/04_mentor/*/code.html` as layout references, preserving the
  Study design tokens, responsive reflow and accessible controls. Dashboard,
  list, detail/editor, dialog, recipient, status and analytics surfaces remain
  screen-specific; omit/gate unsupported prototype panels instead of inventing
  data.
- Test plan: cover Mentor login role acceptance/rejection, API Bearer and refresh
  behavior, all 18 route screens, per-screen API request/response mapping,
  empty/error states, and enabled/disabled actions. No DB seed/demo is planned;
  browser surface and live DB availability will be checked before runtime claims.

### Student implementation plan — W4

- Scope: finish API-backed data flows for `ST-11..ST-25` and retain an explicit
  gate for `ST-26`; retain existing ST-01..ST-10 behavior. Follow the Student
  route/layout and screen-local `data-access/`, `models/`, `pages/`, `ui/`
  structure, use typed DTOs from current Study Server projections, and keep
  route-level API IDs aligned with caller/intent.
- Session: use API #03 only for Student login, verify the returned Student
  role, keep access/refresh tokens in tab memory, use source-only `R-X01` for
  refresh, and clear the session on protected 401. Do not persist tokens or
  change the SH-02 screen contract.
- API gates: keep #21 off ST-20 progress because it returns `UserProfile`;
  #25 cannot save DD's position field; #26 resource URL access and #27
  terminal/order semantics are unresolved; do not claim a player/progress/
  next-lesson action. For #35, send only source request fields and avoid
  automatic retry when the outcome is unknown. Keep #43–45 uncalled because
  their SQL depends on `notification_recipients`, absent from checked-in DDL.
- Current-source mapping: #20 supports ST-24's enrolled-course picker; #24
  lesson detail; #28–32 quiz/attempt; #33–36 assignment/submission; #37
  aggregate course progress; #38 achievements; #39–42 discussions. #40's
  current source accepts text `course_id,title,content`, which differs from
  the stale catalog request projection.
- Styling: use the Student Stitch output and DD for screen structure, preserve
  their original assets, and keep new shared component CSS under the Angular
  per-component style budget by splitting common, learning, and community
  rules. Do not use rendered fixture values as live data.
- Verification: production build, `git diff --check`, and context validator
  after context edits. No test suite is planned in this continuation unless
  explicitly requested; browser/live DB behavior remains unverified.

## CHANGES

- T037: completed its existing AD-12 CSS slice verification; updated only its worklog and the T037/T038 rows in `docs/tasks/process.md`.
- T038: generated the 83-ID structural matrix and implemented ST-02/ST-03 pages; this continuation adds read-only API #04 callers and displays only `full_name`/`email` through StudentApiService. ST-03 mutation controls remain gated.
- T038: implemented ST-04 and ST-05 partial routes/pages using public #08, while keeping unsafe/unverified #15/#16 behavior gated. Updated source status and cross-scope context.
- Context/source docs updated: `.agents/web-work/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/context-manifest.json`, `apps/study-client/gui/architech.md`, `docs/list_screen.md`, `docs/dd_screens/screen-index.md`, ST-02–ST-05 DD/status and T038 matrix. No Study Server source changed.

## VERIFICATION

| Command / evidence | Result | Status |
|---|---|---|
| T037 Angular spec | 4 tests passed. | `PASS` |
| API #82 focused suite | 15 passed; one upstream deprecation warning; fake-session only. | `PASS_WITH_WARNING` |
| Study Web production build | Passed; three existing Student CSS budget warnings. | `PASS_WITH_EXISTING_WARNINGS` |
| AD-12 CSS/diff checks | Prettier, no-literal-hex and scoped `git diff --check` passed. | `PASS` |
| Local route smoke | `/admin/lessons` returned HTTP 200; dev server stopped. | `HTTP_PASS` |
| Browser visual verification | No browser/app available in CUA; authenticated state not used. | `NOT_VERIFIED` |
| ST-02 focused Angular specs | `npm test -- --include=src/app/features/student/ST02/pages/st02-page.spec.ts --include=src/app/features/student/student.route.spec.ts`; 2 tests passed. | `PASS` |
| ST-02 Angular production build | `npm run build`; passed with three existing Student CSS budget warnings, no new ST-02 warning. | `PASS_WITH_EXISTING_WARNINGS` |
| ST-02 formatting/diff | Prettier on touched client targets and scoped `git diff --check` passed. | `PASS` |
| ST-02 API/live visual | No #04 request was added; no browser surface or authenticated Student session was available. | `GATED / NOT_VERIFIED` |
| ST-03 focused Angular specs | 4 tests passed across the ST-03 page and Student route specs. | `PASS` |
| ST-03 production build | `npm run build` passed; only the three existing Student CSS budget warnings remain, with no new ST-03 warning. | `PASS_WITH_EXISTING_WARNINGS` |
| ST-03 formatting/diff | Prettier on touched client files and scoped `git diff --check` passed. | `PASS` |
| Study Agent Context validator | Same repository-wide baseline as T037; no ST-03/T038 findings. | `BASELINE_INVALID / NO_NEW_FINDING` |
| ST-03 API/live visual | #04 read-only caller is implemented; #13/#14 remain uncalled. Authenticated Student/browser runtime is unavailable. | `PARTIAL / NOT_VERIFIED` |
| ST-04 focused Angular tests | Student routes + ST-04 page: 5 passed, including public #08 success, #08 404, and no #15 request. | `PASS` |
| ST-04 production build | Passed; same three pre-existing Student CSS budget warnings, no new ST-04 budget warning. | `PASS_WITH_EXISTING_WARNINGS` |
| ST-05 focused Angular tests | Student routes + ST-04/ST-05 pages: 8 passed, including #08 success/404 and no #16 request. | `PASS` |
| ST-05 production build | Passed; same three pre-existing Student CSS budget warnings, no new ST-05 budget warning. | `PASS_WITH_EXISTING_WARNINGS` |
| ST-04/ST-05 API/live UI | #08 callers are source-wired and tested with HTTP fakes; #15/#16 remain uncalled. Authenticated Student, live DB and deployed browser state are not verified. | `PARTIAL / NOT_VERIFIED` |
| T038 continuation Angular tests | Not run in this continuation; no test execution was requested. | `NOT_RUN` |
| T038 continuation production build | `npm run build` passed. Initial bundle 538.02 kB (38.02 kB above 500 kB); existing warnings: Student layout CSS +3.98 kB, Mentor shared CSS +17 B, Student static CSS +202 B, ST22 CSS +2.21 kB. No ST-02/ST-03 CSS budget warning. | `PASS_WITH_BUDGET_WARNINGS` |
| T038 continuation formatting/diff | Prettier check passed for touched TypeScript/HTML/CSS/DTO files; `git diff --check` passed. Markdown-wide Prettier check flags 16 long DD/inventory documents, so no whole-document reformat was applied. | `PASS_WITH_DOC_FORMAT_LIMIT` |
| Study Agent Context validator (standard) | Exit 1, 1,784 lines, SHA-256 `c6c5872c6bb77736ce9409bb5c99eab6a07b322f989765c993b4beb4488e4314`; `AGENT_CONTEXT_INVALID`, including pre-existing missing db-admin pages and `CONTEXT_STALE` scopes against old manifest sourceCommit. | `BASELINE_INVALID / DRIFT` |
| Study Agent Context validator (`--skip-drift`) | Exit 1, 77 lines, SHA-256 `ea02781d98736eb3cdace354980ddd115272a4276a0294db25e99c819ef9e80e`; remaining static findings are db-admin missing pages/orphan resources; no `study-web`/ST-02/ST-03 finding. | `BASELINE_INVALID / NO_NEW_STUDY_FINDING` |
| ST-02/ST-03 authenticated browser/live API | Not exercised; no browser session/live backend evidence. | `NOT_VERIFIED` |

## HANDOFF

- Remaining T037 gates: API #82 cardinality/filter/pagination and fine-grained permission, live schema and authenticated visual/runtime verification.
- T038 implementation/closeout is complete for this source-backed slice. Remaining product/API gates include ST-03 #13/#14, unsafe #15, order/payment/result, lesson/resource/notification contract gaps, absent #99–#103 and authenticated live API/DB/browser verification. Context validator remains invalid on repository-wide baseline findings; do not call it a pass. Do not count a route or disabled gate as full acceptance.
