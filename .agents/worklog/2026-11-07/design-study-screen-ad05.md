---
task_id: "2026-11-07-design-study-screen-ad05"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AD-05 Study Web /admin/users/:userId/actions ↔ APIs #69/#71/#72; AC-31 handoff from AD-02/AD-03 and return to AD-02/AD-03"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-05

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 210; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current behavior separate; inspect current Study Web boundary; distinguish catalog from source; do not imply mockup actions, tests, or runtime are wired.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: AC-31 user-management permission is not proven by local `ADMIN`; do not infer role/status values from lowercase UI aliases; keep PII/lifecycle/live schema policy open.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: AD-03/#69 hands off numeric user ID; audit/sync claims are unsupported; API #69 is local source only and Study Web remains `UNWIRED`.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-05 only in this session; inspect inventory, AC-31, APIs #69/#71/#72 and current source; create `AD-05_PLAN.md` before markers, annotation, or DD; preserve original assets; create ordered one-to-one marker map/annotation; author sections A–F with traceable fields/events/APIs/errors/states/navigation and blockers; update `list_screen.md`, `dd_screens/PLAN.md`, and this worklog; distinguish DD readiness, implementation block and runtime verification.
- Inventory row 63 currently describes account status/lock/unlock/delete from AD-02/AD-03 using #69/#71/#72. The proposed route and action policy are not yet verified against current source.
- API catalog/AC body, action eligibility, status transition and deletion policy must be compared with local source. Do not infer irreversible delete semantics, confirmation, audit, or undo behavior from the screenshot.

## CURRENT_BEHAVIOR

- Assets: `screen.png` is 1600×1428, SHA-256 `eef9a7e9da0be16b76b519885424aae269486f2a0cc2c4529488b00872a89c82`; `code.html` SHA-256 `cc4dbe123f674d3903838790d806c70116941936383167d73a1b521bdd635adb`.
- Prototype has no selected account; current status is “Không xác định”; permission is “Bị khóa bởi chính sách”; “Read-Only protocol” is displayed. Action tabs are Lock/Unlock/Permanent Delete; first tab is selected. Audit reason textarea and confirm action are disabled. Two back links use `/admin/users`. Header/footer/navigation, audit, ISO, RBAC, gate and API-handler claims are static.
- DOM inspection: 10 anchors, 5 buttons, 1 disabled textarea, no input/select/form, 2 external Tailwind scripts, no `fetch`, XHR, event listener or inline action handler. Back links have `/admin/users`; nav/footer anchors use `#`; buttons have no handlers.
- Study Web root rechecked: only `dist/`, `docs/`, `node_modules/` and `tsconfig.tsbuildinfo`; editable app source/package/router/API client are absent (`UNWIRED`).
- Direct contract: AC-31 Admin with user-management permission chooses status or delete action; #71 `PATCH /api/v1/admin/users/{user_id}/status`, path int64, `ApiEnvelope<UserProfile>`, 200 updated and 401/403/404/422/500; catalog/diagram omit its body. #72 `DELETE /api/v1/admin/users/{user_id}`, path int64 with no body/query, `ApiEnvelope<DeleteResult>`, 200 deleted and the same error set.
- Local #71 source: typed strict required body `{status: "ACTIVE"|"SUSPENDED"}` is `DERIVED`; FastAPI validates typed body before entering endpoint/view guard. The view guard then requires shared `ADMIN`, parses signed-int64 path, locks user status, allows only current `ACTIVE`/`SUSPENDED`, updates status and `updated_at`, and when target is `SUSPENDED` revokes unrevoked/unexpired refresh-token rows in the same transaction. Same-state request still updates timestamp and repeats eligible refresh-token revoke; target `ACTIVE` does not restore revoked rows. Other current states (including `DELETED` and `PENDING_EMAIL_VERIFICATION`) map to 422. Success returns safe UserProfile; query/projection/revoke/commit failures rollback to safe 500.
- Local #72 source: DELETE has no request body; view requires shared `ADMIN` before raw signed-int64 parse, then conditionally sets candidate legacy `users.status='DELETED'` and `updated_at=CURRENT_TIMESTAMP`. Any existing non-DELETED state can be marked; missing/already-DELETED return 404. Response `DeleteResult{id,status:"deleted",deleted_at}` aliases the mutation's `updated_at`; no separate delete timestamp, hard delete, anonymization, dependency check, audit write or refresh-token revoke. Commit follows result validation; failures rollback/safe 500.
- API #03 login and refresh require account status `ACTIVE`; shared access JWT guard checks token claims/roles without reading current account status. Existing access JWTs may remain usable until expiry after either action. #68/#69 queries do not filter `DELETED`, so a deleted user remains list/detail visible with a status marker in local source.
- API #71 and #72 DDs are `Draft — Needs Confirmation`. Test source/context records 21 focused #71 cases and 11 #72 cases, including token side effect, raw-path/auth/errors/rollback and OpenAPI. Tests are read only, not run; fake sessions do not verify live schema/deployment or owner policy.

## SOURCE_TRACE

```text
Expected: AD-02/AD-03 selects a user under AC-31 permission → AD-05 reads current profile via #69 → Admin confirms a supported #71 status action or #72 delete action → response and downstream list/detail refresh follow the approved lifecycle/visibility contract.
Current: AD-05 source is static/unwired. #71 catalog/AC omit body while local code derives strict ACTIVE/SUSPENDED target status, revokes active refresh credentials only on suspend, and leaves existing access JWTs usable until expiry. #72 performs a local soft status marker DELETED, preserves linked rows and refresh tokens, and returns updated_at as deleted_at; login/refresh reject non-ACTIVE while stateless access JWTs may remain usable. #68/#69 still expose DELETED rows. User-management permission, status vocabulary, delete/anonymization/session policy, audit reason, self/last-admin safeguards, route/runtime and live schema remain unresolved.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| #71 body/status | Catalog/AC path-only; strict `{status: ACTIVE|SUSPENDED}` exists only in local source and Draft DD. | DISCREPANCY / DERIVED | Do not present target literals/body as approved contract. |
| #71 session effect | Local suspend revokes eligible refresh tokens; access JWT guard is stateless; unlock does not restore tokens. | SOURCE-BACKED LOCALLY / POLICY OPEN | The prototype claim that all active sessions/access end immediately is unsupported. |
| #72 delete semantics | AC says logical delete/anonymize per policy; local query sets `status='DELETED'` and retains PII/relations/tokens; no persistent delete timestamp. | DISCREPANCY / DERIVED | “Permanent delete” UI label is not the implemented physical/anonymizing behavior; owner decision required. |
| Visibility after delete | #68/#69 read paths do not filter status; #71 rejects DELETED; #72 repeat/missing maps 404. | SOURCE-BACKED LOCALLY / POLICY OPEN | Refresh may leave the user visible with DELETED status; no hide/redirect rule is approved. |
| Audit reason and audit claims | Prototype requires a reason and claims audit/compliance; #71 only accepts status, #72 has no body, neither writes audit. | STATIC_ONLY / UNMAPPED | No audit reason can be persisted by these APIs. |
| Authentication ordering | #71 route has typed request body; framework can return 422 before the view checks ADMIN. Existing auth-order tests use a valid body; mixed invalid-body/missing-auth is not characterized. | ORDER NOT CHARACTERIZED | Do not promise auth-before-body validation. |
| Study Web route/runtime | App tree lacks editable source/router/client. | UNWIRED | No implementation/runtime claim. |

## CHANGES

- Created `AD-05_PLAN.md` before marker/DD authoring; completed its plan, sources, discrepancy, event, blocker and execution notes.
- Created/updated target bundle: `AD-05.md`, `AD-05_markers.json`, `AD-05_markers.svg`, and `screen_annotated.png`. Corrected #12/#14/#27 marker placement and aligned footer marker labels/coordinates (#31 API claim on the right, #32 audit/ISO claim on the left); reviewed final annotated image directly.
- Updated `apps/study-client/docs/list_screen.md`: AD-05 states/flow and blockers now reflect sourced behavior; reverse API source rows #071/#072 changed `D→R`; backend snapshot mentions route/module/test source #68–#72.
- Updated `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` with AD-05 checkpoint and current 58/83 core-artifact count.
- Updated this worklog with completion and static verification results.
- CONTEXT_UPDATES: none. No `.agents` context page changed.
- Original assets retained unchanged. No app tests or runtime checks were run; test source only was read.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Exact-type docs selector `READY` 3/210; AD-01, AD-02, AD-03 worklogs fully read. Manifest confirms `createDD-markdown` excludes `web-ui-only-dd`; no canonical screen-UI DD skill applies. | VERIFIED |
| AC/catalog/API context and source review | AC-31, #69/#71/#72 catalog and Draft DDs, #71/#72 route/model/validation/query/view, shared auth, API #03 login/refresh, #68/#69 query, focused test source/context and Study Web tree reviewed. No tests run. | VERIFIED_SOURCE_REVIEW |
| Marker/static DD audit | 34 JSON markers sequential, unique and in bounds; SVG IDs/coordinates and plan coordinates match JSON; 34 element rows map 1:1; A–F sections present; all 26 local Markdown links resolve. | VERIFIED |
| Source/annotation audit | `screen.png` 1600×1428 and `code.html` hashes match recorded originals; annotated PNG is 3200×2856. Final image visually reviewed; all key text remains legible and footer IDs map to the correct text blocks. | VERIFIED |
| Inventory/checkpoint | 83 distinct inventory IDs and 83 folders; 58/83 have all four core artifacts; AD-05 is included. | VERIFIED |
| Whitespace/static consistency | Generated text files have no trailing whitespace; `git diff --check -- apps/study-client/docs/list_screen.md apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` passes. | VERIFIED |
| Application tests/runtime | Not run by instruction; this documentation session does not verify deployed API, live DB, route or UI runtime. | NOT_RUN / NOT_VERIFIED |

## HANDOFF

- AD-05 artifacts and tracker updates are complete. Remaining product/API blockers are recorded in `AD-05.md`; this is not `DD READY`.
- Next Screen ID for a separate session: AD-06. Do not continue another Screen ID in this session.
