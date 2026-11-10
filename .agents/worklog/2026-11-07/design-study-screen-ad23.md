---
task_id: "2026-11-07-design-study-screen-ad23"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-37; APIs #98–#100; AD-22 → AD-23 moderation detail and return to queue"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-23

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 228; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current behavior separate; inspect current route/source each session; do not infer UI data or runtime from mockups; keep Admin permission distinct from local `ADMIN` and distinguish runtime/DD statuses.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Preserve original assets; trace route/auth/query/effects/response/errors; API local-source `R` does not finalize Draft API DD; no canonical skill applies to web UI-only DD; fake DB evidence does not prove live schema/runtime.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Do not infer numeric IDs, privacy policy or actions from a mockup; retain API catalog vs local-source discrepancies; keep Study Web `UNWIRED`; do not claim tests/runtime/live schema verified.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-23 only; inspect current assets, inventory, AC-37, direct API contracts and current source; write `AD-23_PLAN.md` before marker JSON/SVG, annotation or DD; preserve original assets; create ordered one-to-one markers and annotated image; author A–F DD with traceable elements/events/APIs/states/navigation/errors; update inventory/API reverse index/global plan/worklog; stop before AD-24.
- Inventory row 81: AD-23 “Điều tra/kiểm duyệt thảo luận”, candidate `/admin/discussions/:discussionId/moderate`, AC-37, APIs #98/#99/#100; read full thread/report, action hide/lock/warn/delete with reason; GET #98 → PATCH #99 or DELETE #100 → refresh #97; links back to AD-22; expected `loading/reviewing/processing/resolved/conflict`; P1; tracker D, blocker report persistence/audit.
- AC-37, catalog #98–#100, current route/module/query/validation/model/effects/errors/tests and the AD-22 handoff must be compared before defining detail fields, decision actions, confirmation, permission, audit, deletion, or return behavior.

## CURRENT_BEHAVIOR

- Original assets are `screen.png` (1505×1600 RGB, SHA-256 `2f3787dfdaab4a82b7ddf31a266f3dc0dadb3abe17eb696bfe6790c7c91070bf`) and `code.html` (SHA-256 `8e8d8fe38bbd6f5c9e5e0cd0a184acc0988a9c90732dda199e4ae2d9fd13d74b`). Folder had no plan/DD/markers/annotation.
- HTML is a static placeholder: target ID says “Chưa nạp tham số ID hợp lệ”; course/author/status show `--`; thread area shows an empty state; four disabled radio choices are hide, lock comments, warn author, and permanent delete; reason textarea and apply button are disabled. Return controls use `href="#ad-22"`; there is no form, JavaScript handler, fetch/XHR, API client or Study route.
- Current Study Web recheck: `git ls-files apps/study-client/src` returns 0; app tree has docs, ignored `dist` and no editable route/client/package source. Candidate route is UNWIRED.
- API #98 is registered at `GET /admin/discussions/{discussion_id}`. Local source checks shared `ADMIN` before raw path parsing/query, maps invalid/non-positive/overflow int64 or missing row to 404, reads a Discussion and direct child comments, derives title from normalized content, preserves all child statuses, orders comments by creation time then ID, returns a one-item `Page<Discussion>`, and does not query reports or mutate/commit. Query/projection failures return safe 500 with rollback. API DD #98 still says `UNWIRED / NOT_FOUND`, a source/DD discrepancy.
- Direct catalog #98 is Bearer JWT/Admin, path `discussion_id:int64!`, `ApiEnvelope<Page<Discussion>>`, 200/401/403/404/500. #99 is `PATCH /api/v1/admin/discussions/{discussion_id}/moderate`, required body `action:string`, `reason:string`, `ApiEnvelope<Page<Discussion>>`, 200/401/403/404/422/500. #100 is `DELETE /api/v1/admin/discussions/{discussion_id}`, path only, `ApiEnvelope<DeleteResult>`, 200/401/403/404/422/500. No #99/#100 route/module/query/model/test source was found; both DDs are Draft and record missing physical policy/audit mapping.
- AC-37 expects #98 to read Discussion/comments/reports; after a policy-violation decision it expects #99 state update + audit, optional separate #100 soft delete + preserve audit, and queue reload. The NO branch says dismiss report but no dismissal API is listed. Current #98 has no report fields; #97 response has no reason/severity/count/reporter/time; #97 report table/migration is a candidate and report writer/live deployment are unverified.
- Prototype puts permanent delete in the #99 radio set although AC separates optional deletion into #100; prototype says data is deleted “hoàn toàn” although AC/#100 say soft delete; warning copy claims an email and auto-audit persistence without source. Action tokens/state transitions, reason constraints, Admin permission/actor mapping, audit schema/atomicity, report dismissal and root/reply policy remain unapproved.
- Application tests/runtime have not been run in this task. Existing API #98 characterization test source was inspected; fake DB tests do not establish live schema/deployment.

## SOURCE_TRACE

Expected flow: AD-22 passes a valid Discussion ID → AD-23 loads #98 thread/report detail → Admin decides per AC-37 policy → #99 action with required reason and audit, then optionally separate #100 soft delete preserving audit → reload #97 / return AD-22. AC-37 “NO violation → dismiss report” has no listed endpoint. Direct API contracts do not define action tokens, response detail, authorization claims, or physical audit/delete persistence.

Current source flow: no Study Web caller; #98 route/module/query/model/test source exists locally, but its response contains only one Discussion and direct comments, not report data. It uses a local `ADMIN` guard and local `Page<Discussion>` projection, with read-only DB behavior. #99/#100 exist only in catalog/AC/API DD, with no current route/module/test. The HTML’s ID is unresolved and all decision/reason/apply controls are locked; return anchors stay on fragment `#ad-22`.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Report detail in #98 | AC-37 expects reports; #98 direct `Page<Discussion>` and current projection have no report fields or report query. | DISCREPANCY / BLOCKER | Do not fabricate report reason/severity/reporter/time/count in the panel. |
| #98 DD runtime status | DD says `UNWIRED / NOT_FOUND`; route/module/query/test source is currently registered. | SOURCE/DD DISCREPANCY | Document current local source without treating it as approved/final API DD. |
| #99 moderation/audit | Catalog provides generic required `action`/`reason`; no current route; exact tokens, status transition, actor and physical audit source/atomicity unresolved. | DRAFT / UNWIRED / BLOCKER | Keep controls locked; do not claim an audit record or action success. |
| #100 delete | Direct contract is separate DELETE, AC says soft delete + preserve audit; no route/source and no approved state/timestamp/audit mapping. Prototype says permanent delete. | DRAFT / UNWIRED / DISCREPANCY | Do not put delete through #99 or claim hard/soft delete has runtime behavior. |
| Report dismissal branch | AC-37 NO-violation branch says dismiss report; catalog lists only #98–#100, no dismissal route. | NOT_FOUND / BLOCKER | Do not add a dismiss action to the screen or use #99 without an approved mapping. |
| Target ID/thread scope | #98 accepts Discussion int64; AC/#97 do not decide report-on-root vs reply; child/thread visibility and report target grain open. | OPEN / BLOCKER | Do not infer root/reply transition or relation from the page route. |
| Authorization | AC/catalog actor Admin; current #98 uses local `ADMIN`; #99/#100 have no current policy source or actor mapping. | PARTIAL SOURCE / OPEN QUESTION | Keep Admin role/permission and audit actor identity separate. |
| Study Web/runtime | Editable Study Web source/router/client absent. | UNWIRED | Candidate route and interactions are not runtime verified. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/AD-23_PLAN.md`, `AD-23.md`, `AD-23_markers.json`, `AD-23_markers_overlay.svg`, `screen_annotated.png`; `apps/study-client/docs/list_screen.md`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; this worklog. Original `screen.png` and `code.html` were preserved unchanged.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none. Unresolved decisions are recorded as blockers in the DD and do not drive invented behavior.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Router/context/worklog preflight | `.agents/AGENTS.md`, `.agents/context-map.md`, worklog README/template read; exact docs selector READY 3/228; AD-01/02/03 read in full. | VERIFIED_PREFLIGHT |
| Initial assets/trackers | AD-23 folder only has `screen.png`/`code.html`; inventory/global plan D; API reverse-index #098–#100 D; source hashes and image dimensions recorded. | VERIFIED_INITIAL |
| AD-23 source/contract review | AC-37, direct catalog #98–#100, #98 local route/module/query/validator/view/model/test source, API DDs, candidate migration/DDL and Study Web tree/context reviewed; expected/current discrepancies documented. | VERIFIED_SOURCE_REVIEW |
| DD and artifacts | Plan saved before markers/DD; A–F DD has 45 elements and EV-01…EV-09; marker JSON/SVG #1–#45; annotated PNG visually reviewed. | VERIFIED_ARTIFACTS |
| Static marker/link audit | JSON parsed; SVG XML parsed; 45 IDs sequential/unique/in-bounds, no marker center pairs closer than 22 source px; plan/JSON/SVG/DD mapping aligned; local Markdown links resolve. | PASS |
| Image/source preservation | `screen.png` 1505×1600; `screen_annotated.png` 3010×3200; original SHA-256 values for `screen.png` and `code.html` unchanged. | PASS |
| Inventory/core assets | 83 unique inventory IDs, 83 screen folders; 76/83 have all four core DD artifacts. | PASS |
| Tracked diff and authored files | `git diff --check` clean for changed tracker files; new plan/DD/JSON/SVG have no trailing whitespace. A whole-file whitespace scan of the pre-existing inventory stopped at unrelated trailing whitespace on `list_screen.md:3`; that line was left unchanged. | PASS_SCOPED |
| Application tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining work: none for AD-23 documentation/artifact audit. AD-24 is a separate session.
- Remaining blockers: report details/persistence and writer; #98 API DD/runtime-status discrepancy; #99 action tokens/state/audit/authorization; no-violation dismissal endpoint; #100 soft-delete persistence/audit/eligibility/retention; report root/reply target; AC Admin vs local `ADMIN`; Study Web and #99/#100 routes are unwired. See `AD-23.md` §F.
- Final statuses: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Static DD artifacts and checks are verified; this does not mean runtime implementation is ready.
- Stop after AD-23; AD-24 is a separate-session screen.
