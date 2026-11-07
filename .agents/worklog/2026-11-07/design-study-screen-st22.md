---
task_id: "2026-11-07-design-study-screen-st22"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-22 achievements → API #38 and AC-18; navigation from ST-20/ST-09"]
status: "PARTIAL"
---

# Worklog: Re-audit ST-22 achievements and certificates DD

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`, 248 exact-type worklogs available, 3 selected, no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Separate expected behavior from current source; do not infer product behavior or API fields from screenshots; keep UI-only DD outside API-DD skill.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Preserve static-prototype claims as such; trace source for current routes/API; maintain design-system discrepancies and independent readiness/runtime statuses.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Do not invent routes, identities, mappings or policies from a mockup; tests/fake DB evidence does not prove live runtime/schema.
  - path: `.agents/worklog/2026-11-07/design-study-screen-st20.md` (supplemental)
    - carry_forward: Inventory links ST-20/ST-22; API #38 award/filter/pagination semantics are unresolved, and AC-18 sequencing must remain distinct from inventory orchestration.
  - path: `.agents/worklog/2026-11-06/design-study-screen-st22.md` (supplemental, prior ST-22 session)
    - carry_forward: ST-22 already has plan, 46-marker assets and A–F DD; re-audit existing artifacts before changing anything, preserve PNG/HTML sources and retain API #38 blockers.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Re-audit ST-22 only; preserve source assets; verify ordered marker/DD mapping, event details, A–F, API #38/AC-18 trace, navigation and current visual target; update inventory, global plan and dated worklog.
- Canonical contract/approved DD: inventory ST-22 `/student/achievements`, AC-18, API #38; catalog GET `/api/v1/users/me/achievements`, optional `course_id:int64`, `ApiEnvelope<Page<Achievement>>`, 200/401/403/500. Only backend-confirmed awards may display; no client-side award/certificate issuance.

## CURRENT_BEHAVIOR

- Source/config: Preserved `screen.png` (803×1600; SHA-256 `cf11ec7d3e064b689c90853e275fcd65dcb828e644c495e1d9b004d58b974b4f`) and `code.html` (SHA-256 `abde69d2bc108b1b5bc9004896fff0ec016a61a7ec14a3a9e2b9f63ae10a5439`). HTML is a static empty fallback with Tailwind CDN/config and three remote Google Font imports; it has no app API/data binding/auth/form/input/event handler. Study Web remains `UNWIRED`; Study Server API #38 route/module/query/test is `NOT_FOUND` in checked source. Current DB artifacts support only logical/derived achievements, not a live-schema claim.
- Runnable tests: Not run; this is a documentation task.
- Runtime wiring: Not verified; no runtime or live DB/deployment claim is made.

## SOURCE_TRACE

```text
ST-20/ST-09 → ST-22 (inventory navigation only)
ST-22 → API #38 catalog/Draft DD
AC-18 → login → progress/course flow → read unlocked achievements
DISCREPANCY: ST-20 inventory calls #21 and #38 independently; AC-18 sequences #21 → #37 → #38
Current Study Web route → UNWIRED; Student API #38 route/module/query/test → NOT_FOUND
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #38 award projection | Catalog describes `Page<Achievement>`; Draft DD has six open questions; Study Server route/module/query/test search is empty. | `DECLARED_NOT_RUNNABLE`; Draft; `NOT_FOUND` | Do not invent award criteria, certificate/proof fields, or pagination semantics. |
| Loaded PNG vs empty HTML | Populated PNG versus static empty fallback; HTML includes Tailwind CDN/config and remote Google Fonts, but no app handlers/data binding. | `DISCREPANCY` | Keep assets and runtime state distinct; note visual target mismatch. |
| Cross-screen call order | ST-20 inventory requires #21/#38 independently; AC-18 sequences #21 → #37 → #38. | `DISCREPANCY` | Keep ST-22 #38 responsibility; do not infer page-entry timing/orchestration. |
| Study Web / API wiring | Current Study Web has no editable route source; API #38 route/module/query/test absent. | `UNWIRED` / `NOT_FOUND` | No runtime claim. |

## CHANGES

- Files changed: `ST-22.md`, `ST-22_PLAN.md`, `apps/study-client/docs/list_screen.md`, `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`, this worklog. Source PNG/HTML and marker/annotation images were preserved.
- DD updates: clarify static HTML dependencies and design-system mismatch; add explicit inventory-vs-AC-18 ordering discrepancy; ensure all 15 event rows identify element/lifecycle, type, and precondition.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: None; missing policy remains an explicit blocker.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| PNG/hash audit | Source 803×1600 and annotated 907×1640; source hashes match DD/plan and remain unchanged. | `PASS` |
| Marker/DD/event audit | 46 sequential unique markers = 46 element rows; 15 ordered events have Trigger, Element/precondition, Input, Xử lý, Output, Ngoại lệ; A–F present. | `PASS` |
| JSON/SVG/link audit | Marker JSON parses; SVG XML parses at 907×1640; local Markdown links in DD and plan resolve. | `PASS` |
| Inventory audit | 83 IDs/folders; 82/83 have all four core artifacts; ST-01 is the only incomplete bundle. | `PASS` |
| Whitespace | Scoped `git diff --check` and authored-file trailing-whitespace scan. | `PASS` |
| Application tests/runtime/live DB | Not requested/performed. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: API #38 award/projection, `course_id` access/filter, page/order/empty and query validation remain open; populated screenshot claims still lack approved projection; Study Web route and Student #38 runtime source are absent; AC-18 ordering conflicts with independent inventory calls.
- Next owner/action: ST-22 re-audit is complete for this session with status `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`. ST-01 is the only Screen ID lacking a complete core artifact bundle; handle it in a separate session.
