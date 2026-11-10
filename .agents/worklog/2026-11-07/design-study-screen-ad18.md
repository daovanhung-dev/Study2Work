---
task_id: "2026-11-07-design-study-screen-ad18"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-35; API #90; AD-15 → AD-18; quiz deletion vs attempts/history policy"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-18

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 223; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Separate expected/current source; no UI runtime claims from mockups; preserve API source vs contract status and record auth/data blockers.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Keep Study Web `UNWIRED`; trace backend effects and response; don't invent filter, permission or action semantics from the mockup.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Keep Admin authorization/PII/lifecycle rules open until sourced; tests/fake DB don't prove deployment/schema; preserve original assets and one-screen-per-session scope.
- additional handoff reviewed: `.agents/worklog/2026-11-07/design-study-screen-ad17.md` — AD-17 completed; next Screen ID is AD-18; Study Web remains unwired; API #90 delete/attempt policy is a dependency to verify from current source and DD.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-18 only in this session. Inspect row 76, AC-35, API #90 direct catalog/Draft DD and current backend source/tests; write `AD-18_PLAN.md` before markers/annotation/DD; preserve original screenshot/HTML; create one-to-one markers and A–F DD; update screen inventory, reverse API index, G-11/global plan/checkpoint and this worklog; run static audit; stop before AD-19.
- Inventory row 76 describes an Admin confirmation dialog at candidate route `/admin/quizzes/:quizId/delete`, API #90, returning to AD-15. The expected copy asks to review effect on attempts and confirm deletion; flow says DELETE #90 then invalidate #87 and keep the screen on conflict. These are requirements to verify, not proof that current API has a conflict policy.
- AC-35 actor/precondition is Admin with quiz-management permission. Direct catalog #90 and current source authorization/error behavior must be kept separate. AC-35 node n10 calls for soft delete when attempts exist; it gives no no-attempt rule. Do not infer a conflict code.

## CURRENT_BEHAVIOR

- Source folder `apps/study-client/docs/screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/` contains only `screen.png` (1600×1442, 288,952 bytes, SHA-256 `62411399c66e1a90efa1554232388cd7ec8bffdb8946a07b8f834fe94a67a776`) and `code.html` (17,607 bytes, SHA-256 `8e99ddbb2df1dc64ba8e258c1d7f22c6a1555bddf8d6908baf81fff984cbf955`). PNG visually reviewed; HTML has static `href="#"` anchors, disabled textarea/confirm button, no listener or network call.
- Study Web checkout has no editable app source/router/API client; it remains `UNWIRED` / `NOT VERIFIED` (docs/dist/node_modules and build metadata only).
- AC-35 diagram `apps/study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio` says quiz-management permission; API #90 DELETE path-only, `ApiEnvelope`, 200 `DESIGN_RESOURCE_DELETED`, errors 401/403/404/422/500; node n10 says soft delete if attempts exist.
- Direct API catalog #90 matches those method/path/statuses and `DeleteResult{id:int64,status:"deleted",deleted_at:date-time}`; it has no 409 and no no-attempt deletion rule. API #90 DD remains `Draft — Needs Confirmation` and lists open questions on tombstone timestamp, no-attempt hard delete, #29 create-attempt race, visibility in #87/#89/#91, and permission policy.
- Current Study Server route is registered and path-only. Module validates shared `ADMIN` before positive signed-int64 parsing, locks Quiz then questions/choices, checks attempts and linked answers, soft-deletes with `status='DELETED'` preserving children/history when either exists, otherwise hard-deletes choices/questions/quiz in one transaction. Repeated tombstone DELETE returns the prior timestamp; local response maps DB `updated_at` or hard-delete `CURRENT_TIMESTAMP` to `deleted_at`. This local branch/timestamp policy is derived and not owner-approved.
- Current API #87 list excludes `status='DELETED'`; API #89 rejects changes when attempts/answers exist with a local 422 and rejects tombstone (404). API #91 query includes tombstoned quizzes and preserves attempt history in statistics. Catalog #90 has no conflict response. No current #29 attempt-create route/module was found in `apps/study-server/app/api/v1.py` or `app/modules`; cross-API race remains unresolved.
- Existing source docs record 18 focused #90 HTTP tests, linked #86–#90 100-test regression, and 1,178 full-suite tests for the 2026-11-01 run. Tests were not run in this session; existing test-source/report evidence does not verify live production schema/deployment or #29 race.
- Inventory row 76 initially marks #90 `D`; global AD-18 plan row initially says `CHƯA_BẮT_ĐẦU`; G-11 presently covers AD-16/#88–#89 and AD-17/#91 gaps, not #90 delete policy.

## SOURCE_TRACE

```text
Expected: AC-35 Admin with quiz-management permission selects Quiz from AD-15, reviews impact on attempts and confirms delete. AC-35 explicitly requires soft-delete when attempts exist but omits the no-attempt branch. Inventory also expects #87 invalidation and a conflict-stay state; #90 catalog has no conflict code, so that state is unsupported by the current API contract.
Current: Study Web is unwired; the prototype has no script/listener/request, links are `#`, target record is placeholder, audit-reason input and destructive button are disabled. #90 is registered and has local soft-delete-on-attempt-or-answer and hard-delete-without-history branches; these are derived, API DD remains Draft. #87 excludes tombstones, #89 rejects edits to tombstones/history, #91 includes them, and no #29 attempt-create route exists locally to close the race.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Quiz delete effect on attempts/history | AC-35 requires soft-delete when attempts exist; catalog is silent on no attempts; local code soft-deletes on attempts or answer references and physically deletes otherwise. API DD labels these implementation branches DERIVED/open. | DISCREPANCY / BLOCKER | Document branches as local source only; no approved end-user claim, reason input requirement or final delete policy. |
| API #90 response/auth/errors | Catalog/direct DD: 200 DeleteResult and 401/403/404/422/500; local route uses shared ADMIN guard and same status set. No 409. AC-35 permission differs from local role-only guard. | VERIFIED_WITH_OPEN_QUESTIONS | The inventory `conflict` state is not API-supported; invalid ID 422 is validation only. |
| Dialog actions and route | PNG/HTML reviewed. `href="#"`, disabled reason textarea and disabled confirm button; no fetch/XHR/listener. | VERIFIED_STATIC_ONLY | Preserve mockup; describe candidate actions as expected, not implemented. |
| Study Web wiring | Current client directory contains docs/dist/node_modules/build metadata, no editable source/router/API client. | UNWIRED / NOT_VERIFIED | Inventory URL remains candidate only. |
| Attempt creation race | Local #90 parent lock cannot prove cross-API safety; no local #29 attempt-create route/module. | BLOCKER | Do not claim race-safe deletion or reject active attempts. |
| Post-delete visibility | #87 excludes DELETED; #89 rejects tombstones and history edits; #91 includes tombstones/history in statistics. Local source only; behavior requires policy confirmation. | DISCREPANCY / BLOCKER | Document current local source and open owner decision separately. |

## CHANGES

- Created `AD-18_PLAN.md` after source review and before marker/annotation/DD work; plan-first order satisfied.
- Added 40 marker JSON/SVG entries, `screen_annotated.png` at 3200×2884, and `AD-18.md` A–F with 40 element rows and EV-01…EV-06.
- Updated inventory row 76, reverse API index #090 (`D`→`R`), G-11 and global plan row/checkpoint. Core artifact sets increased 70/83→71/83; inventory/folders remain 83/83.
- Original `screen.png` and `code.html` retained unchanged (SHA-256 values recorded above).
- CONTEXT_UPDATES: none; no `.agents` context pages or application source files changed.
- Assumptions: none. No-attempt/answer-only/tombstone/repeat/concurrency/visibility/permission policies remain explicitly `DERIVED` or unresolved.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective, context map, worklog contract/template and relevant project/scope context read; exact docs selector READY 3/223; AD-01/02/03 and AD-17 worklogs read. | VERIFIED_PREFLIGHT |
| AD-18 source/contract review | Row 76/reverse index, AC-35 diagram, #90 direct catalog/DD, Study Web tree, source PNG/HTML, AD-15 handoff, #87/#89/#91 lifecycle, #90 route/module/query/model/validator and test/report sources reviewed. | VERIFIED_SOURCE_REVIEW |
| Static artifact audit (final run after DD coordinate mapping) | JSON/XML parse; 40 unique sequential markers and SVG labels; JSON/SVG/DD coordinates match; all in bounds and pairwise non-overlapping; DD rows #1–#40; 8 Markdown links resolve; original image/HTML hashes unchanged; 83 IDs/folders; core artifacts 71/83. | PASS |
| Image dimensions / visual review | `magick identify`: source 1600×1442, annotated 3200×2884 (exact 2×); annotated image reviewed, markers remain legible and do not cover key copy. | PASS |
| Whitespace / repo diff | `git diff --check` passed. | PASS |
| Agent context validator | `node scripts/validate-agent-context.mjs` returned `AGENT_CONTEXT_INVALID`, reporting missing db-admin context/source paths and stale source fingerprints, including server-study/db-admin; this task changed no context page or application source. | REPOSITORY_CONTEXT_FAILURE_OUTSIDE_AD-18 |
| Application tests/runtime | Not run as the task is a screen-documentation/static-audit pass; existing #90 report evidence is historical and does not verify this UI/runtime. | NOT_RUN |

## HANDOFF

- Remaining work in this session: none. AD-18 artifacts, trackers, and static audit are complete; no application tests/runtime were run.
- Remaining blockers: owner approval for no-attempt branch, answer-only history, tombstone/timestamp/repeat semantics, #29 concurrency, post-delete visibility, permission and conflict-state alignment; API DD/live schema/deployment and Study Web wiring. Keep `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Next Screen ID for a separate session: AD-19.
