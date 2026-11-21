---
task_id: "2026-11-06-design-study-screen-st02"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-02 API #04 Student profile; auth/session handoff from SH-02; downstream edit route ST-03"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-02

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 167 exact-type docs worklogs available; selected 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: keep Study Web `UNWIRED`; source tests/DDL are not deployment or live-schema proof; trace API current behavior separately from catalog/AC.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: preserve source image/HTML hashes and document screenshot/HTML state mismatch without inferring client routes or loaded UI.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: use current Study API source over stale declarations while preserving `DISCREPANCY`; one Screen ID per session; no test/runtime claims from read-only test source.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Objective file was reread this turn: `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`. This session covers ST-02 only, with a per-screen plan before annotation/DD.
- Inventory: `/student/profile`, AC-11, API #04, Student actor, profile display, expected `loading/ready/401/403`, cache profile, link to ST-03. AC-02 also calls #04 after login for Student.
- AC-11 expects an authenticated Student; broader user instruction requires every profile field/API mapping/state/navigation to be traceable and unsupported decisions remain blockers.
- Next screen is selected by `list_screen.md` dependency wave: ST-02 is remaining W0/P0; after it, W1 starts at ST-03. ST-01 is assigned W3. The stale global handoff `GS-08` is invalid because there are only GS-01..GS-07 and will be corrected.

## CURRENT_BEHAVIOR

- Before edits, ST-02 directory contained only `screen.png` and `code.html`. PNG is 1280×1078, SHA-256 `d708cf38575a9ef14352ea5937379e191448bdb62341f7b1fc90f5e50144f379`; HTML SHA-256 `9969e179da65352894ac2eead28147f341b47b5fb226c6047c7b62345a265cc1`.
- Original screenshot body is blank; HTML contains heading/description and a static sign-in card with login link and disabled edit button. Header/footer links are `href="#"` with `data-path`; no API call, route handler, or Study Web app source exists. Screenshot and HTML disagree; a faithful separate HTML rendering is being prepared, leaving source files unchanged.
- API #04 current route/view/query/model are present. It uses shared Bearer/JWT guard requiring `STUDENT` before read-only query by JWT `sub`; emits profile fields `id/full_name/email/role/avatar_url/phone/status/created_at/updated_at`. No `bio`/permissions; no comparison of JWT role or status against DB. Test source has branches for 200/401/403/500 but is read only/not run.
- API #04 DD is `Draft — Needs Confirmation`; API #03 current success already returns a base profile with tokens; live database schema and Study Web runtime are not verified.

## SOURCE_TRACE

- Mandatory routing/preflight read: `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`; selector `node scripts/select-worklogs.mjs --type docs --limit 3`; selected GS-01, GS-02 and GS-03 logs read individually.
- Cross-scope context: `.agents/project/INDEX.md`, `architecture.md`, `dependencies.md`; `.agents/web-work/AGENTS.md`, `INDEX.md`, Study `AGENTS.md`/`INDEX.md`, `.agents/web-study/design.md`; `.agents/server-study/AGENTS.md`, `INDEX.md`, `apis/declared-routes.md`, core runtime/auth/database, database, module and tests pages; `.agents/skills/INDEX.md`, `.agents/context-manifest.json`.
- Inventory and flow: `apps/study-client/docs/list_screen.md` ST-02, F01, G-02/G-03, §8.1 W0/W1/W3; AC source `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` AC-02/AC-11 and `AC_02_STUDENT_LEARNING.drawio`.
- Assets: `apps/study-client/docs/screen_stitch/03_student/ST-02_ho-so-ca-nhan/{screen.png,code.html}`; screenshot visually inspected; controls/anchors parsed; hashes/dimensions recorded above.
- API declaration/current chain: `docs/lists/list_api.md`; `apps/study-server/docs/dd/04_users_me/{02_Overview,03_Request,04_Response,05_Data_Mapping,06_Error,OPEN_QUESTIONS}.md`; `apps/study-server/app/api/v1.py`; `app/modules/guest/api_04_users_me/{view,query,models}.py`; `app/utils/auth.py`; shared token decoder; API #03 auth view/helper.
- Test source (read only): `apps/study-server/tests/modules/guest/api_04_users_me/test_users_me.py`; tests not run.
- DB candidate: `infra/postgres/study-server/DB.sql` `users` definition; `.agents/server-study/database.md` reports pilot DDL checked in and live schema `NOT_VERIFIED`.
- Related screens/dependencies: SH-02, ST-01, ST-03 inventory; global `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`.
- Registry explicitly excludes `web-ui-only-dd` from `createDD-markdown`; no canonical UI-only DD skill is available, so no API-DD authoring skill is invoked.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Screenshot vs HTML | PNG shows header/footer only; HTML includes profile heading and sign-in card. | `DISCREPANCY` | Preserve both; annotate a separately rendered HTML variant only if visually faithful; no screenshot body claim. |
| Authenticated actor vs current static UI | AC-11 requires signed-in Student; HTML asks user to log in and disables edit. | `DISCREPANCY` / `UNWIRED` | Loaded profile/authorized view is not designed or implemented. |
| #04 claims and permissions | AC-02 diagram says `user_id`/`role`, current #03/#04 source uses `sub`/`roles`; AC-02 mentions permissions absent from catalog response/model/query. | `DISCREPANCY` | Token/bootstrap and permission UI contract unresolved. |
| Profile fields | Catalog has optional `bio`; current #04 excludes it; AC-11 edit includes it. | `DISCREPANCY` | Do not invent/store/display bio in ST-02. |
| Role/status freshness | Current guard trusts JWT `roles`; SQL does not compare `users.role` or filter `users.status`; returned status is required by model but candidate DDL allows null. | `BLOCKER` / `NOT_VERIFIED` | Account lock/role-change and nullable status semantics unresolved; live schema unknown. |
| Duplicate profile fetch/cache | Current #03 returns base profile and F01/AC-02 then calls #04 for Student; cache behavior unspecified. | `OPEN` | No cache TTL/invalidation or reason for second fetch can be inferred. |
| UI routing | All anchors use `#`; Study Web has no source/router. | `UNWIRED` | Login, nav, ST-03 route and refresh/back behavior unverified. |

## CHANGES

- `ST-02_PLAN.md` is written before creating the DD or marker artifacts.
- Firefox headless rendered `code.html` to `screen_rendered.png` (1280×1078); visual inspection confirmed the static HTML content. Its viewport-bound main minimum height leaves the footer outside that capture.
- Added `screen_composite.png`, retaining the original screenshot header/footer and placing the body crop (x=0, y=64, 1280×536) from the HTML render. `screen.png` and `code.html` remain unchanged. Rebuilt the 10-marker SVG/PNG against the composite and aligned footer markers to the visible labels.
- Updated `ST-02.md` and `ST-02_PLAN.md` with composite provenance and static artifact review; updated the global tracker to 15/83 complete bundles, 68 remaining, ST-02 blocked statuses, and ST-03 as next. Corrected the stale GS-08 pointer.
- No Study API, Study Web app code, context registry/page, test or database file changed.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Source and image hash audit | Original `screen.png` and `code.html` hashes match the pre-edit plan; `screen_rendered.png` is 1280×1078, `screen_composite.png` is 1280×1078, and `screen_annotated.png` is 2720×2156. Composite input/output hashes match marker JSON provenance. | VERIFIED |
| Static marker/DD/SVG audit | Marker JSON IDs #1–#10 are ordered; 10 IDs match 10 DD element rows; SVG has exactly 10 numbered circles/text labels and embeds the composite hash. | VERIFIED |
| Relative DD links and tracker audit | All relative Markdown links resolve; tracker says 15/83 complete artifact bundles, 68 remaining, ST-02 separate blocked statuses, and ST-03 next; no GS-08 pointer remains. | VERIFIED |
| `git diff --check` and changed-text whitespace scan | No whitespace errors in tracked diff or the five updated text files. | VERIFIED |
| API tests / UI runtime / live schema | Test source was read only; no tests, UI runtime, or live-schema verification were performed. | NOT_RUN / NOT_VERIFIED |

## HANDOFF

- This session covered ST-02 only. Continue with ST-03 in a separate session; keep the overall 83-screen goal active.
