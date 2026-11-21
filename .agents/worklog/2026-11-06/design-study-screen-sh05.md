---
task_id: "2026-11-06-design-study-screen-sh05"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-05 maps Study API #04 auth/authorization failures and runtime helper R-X01 refresh; links to SH-02 and a safe prior route"]
status: "VERIFIED"
---

# Worklog: Rà soát Detailed Design màn hình Study SH-05

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selected 3 of 157 docs worklogs; all selected logs read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh01.md`
    - carry_forward: Keep screen DD, implementation and runtime statuses distinct; map all markers and events to stable IDs; retain source assets and verify local links.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh02.md`
    - carry_forward: Auth/session flows have unresolved API #03/#04 response and role/session-policy discrepancies; do not merge design contract with current source behavior.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh03.md`
    - carry_forward: Study Web source/router is absent; API source and static tests do not prove runtime or live schema; preserve separate implementation/runtime blockers.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete SH-05 only in this session; review its screen plan before editing DD/assets; preserve original sources; verify annotated markers map one-to-one to stable DD Element IDs; trace events and API #04/R-X01 behavior to current source/contracts/tests; update tracker and this worklog.
- Canonical contract: `apps/study-client/docs/list_screen.md` SH-05, AC-02/AC-11, G-14 and R-X01; API #04 catalog/source and SH-02 session flow. `.agents/web-study/design.md` is the Study Web visual/interaction target, not runtime evidence.

## CURRENT_BEHAVIOR

- The SH-05 folder contains the original 1600×1280 `screen.png`, `code.html`, an 11-marker `screen_annotated.png`, DD, plan and marker JSON. The original image and HTML hashes were captured before editing; the annotation visually matches the 403 default state.
- `apps/study-client/src/` and `package.json` are absent; existing `dist/` and `node_modules/` do not establish a source-backed Study Web route or runtime. The context-referenced `.agents/web-work/study/AGENTS.md` and `INDEX.md` are also absent; `.agents/web-study/design.md` exists and is registered as the Study design target.
- Current #04 source maps malformed/missing auth and missing user profile to the same `401 DESIGN_AUTHENTICATION_REQUIRED`; non-STUDENT role maps to `403 DESIGN_ACCESS_DENIED`. R-X01 server route/source rotates opaque refresh tokens; no Study Web client/session implementation is present.
- DD status is assessed `DD BLOCKED`; implementation remains blocked and runtime is not verified because 401 recovery, token/session policy, safe route fallback, production UI composition and the adjacent SH-02 handoff are unresolved.

## SOURCE_TRACE

- Expected screen contract: `apps/study-client/docs/list_screen.md` SH-05 row and shared auth/state sections: 401 may try R-X01 once; 403 must not trigger refresh; preserve a safe redirect; route `/forbidden`, `/login` and `/` are proposals. `docs/lists/list_api.md` is the approved design catalog. AC-02/AC-11 and the API #04 DD are linked design evidence; they do not define SH-05 route/UI or distinguish 401 causes.
- API #04 route: `apps/study-server/app/api/v1.py` registers `GET /api/v1/users/me` and delegates to `api_04_users_me.view.get_current_user`. That calls `validate_current_user_request(role="STUDENT")` before reading `CURRENT_USER_PROFILE`; invalid/missing Bearer/JWT/claims → 401, other role → 403 before DB query, missing profile → 401, query/model failure → safe 500, valid profile → read-only 200. The safe `UserProfile` allowlist excludes `bio` and `permissions`.
- API #04 test source `apps/study-server/tests/modules/guest/api_04_users_me/test_users_me.py` covers missing/malformed Bearer, invalid JWT/claims, non-STUDENT before DB access, missing row, DB error, safe projection and trace. Tests were read, not run.
- R-X01 is `POST /api/v1/auth/refresh` in `app/api/v1.py`, delegated to API #03 `api_03_auth_login.view.refresh`; request body is `{refresh_token}` and route has no Bearer parameter. Current source validates nonblank token, hashes it, finds an unrevoked/unexpired refresh row joined to user, rejects missing token with 401 and inactive account with 403, then creates a token pair, revokes the old row, inserts the new hash and commits. `build_auth_payload` returns allowlisted profile fields plus access/refresh token and expiry metadata. Test source `apps/study-server/tests/modules/guest/api_03_auth_login/test_auth_login.py` covers rotation, inactive account, invalid token and route validation; tests were read, not run.
- Error responses use `{success,businessCode,message,data,meta,traceId}` and `X-Trace-Id`; `code.html` preview instead shows synthetic codes, `status` and `timestamp`, and its refresh action uses only a local timer. It does not call an endpoint.
- Cross-screen handoff: inventory G-14 records API #03 catalog `201/UserProfile-only` versus current source `200/profile+tokens`; SH-02 already owns that discrepancy. A completed SH-05 login handoff depends on SH-02 resolving its response contract.
- The Study-specific design guide `.agents/web-study/design.md` sets 44×44px icon targets, local/system font, responsive reflow and ~1120px content width; the HTML prototype uses a 40×40px icon control, remote font/Tailwind CDNs and a wider canvas.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| SH-05 assets and annotation | Original 1600×1280 screenshot plus 11 visible markers; JSON numbers/Element IDs are 1–11 and visually align with screenshot regions. | VERIFIED_STATIC | Preserve original image and HTML hashes; keep #1/#2/#3/#6/#9/#11 marked prototype/handoff pending UI scope decision. |
| Study Web route/session handling | `src/`, package manifest and expected `.agents/web-work/study/{AGENTS,INDEX}` are absent; no router/session source. | NOT_FOUND | Do not claim runtime behavior from `dist`, `node_modules` or HTML preview. |
| API #04 auth/error mapping | Current route/view/helper/test source confirms 401 for invalid auth and missing profile, 403 for role mismatch, safe 500 for DB/model; response does not distinguish 401 cause. | VERIFIED_SOURCE; TESTS_READ_NOT_RUN | Recovery cannot assume every 401 means expiry. |
| R-X01 refresh | Route and API #03 source/test source confirm server token rotation, 401/403/422/500 mappings and transaction operations. | VERIFIED_SOURCE; TESTS_READ_NOT_RUN | No client persistence, single-flight, retry or timeout policy evidenced. |
| Expected/current and linked screens | Inventory says refresh once after 401 and safe return; G-14 keeps API #03 catalog/source mismatch open in SH-02. | DISCREPANCY / BLOCKED | Need product/backend recovery decision and SH-02 login handoff contract. |

## CHANGES

- Files changed: this worklog; SH-05 plan and DD; global `dd_screens/PLAN.md`. Existing marker JSON and annotation were reviewed and retained.
- CONTEXT_UPDATES: None. The manifest/context map references missing `.agents/web-work/study/AGENTS.md` and `INDEX.md`; the available `.agents/web-study/design.md` is manifest-registered and was used for visual requirements.
- Context pages changed: None anticipated.
- Assumptions: Web UI-only DD has no canonical registered authoring skill; verify manifest boundary before authoring.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` + selected-file review | Selected and read 3 exact-type worklogs of 157; no shortage. | VERIFIED |
| SH-05 static integrity audit | Original and annotated PNGs are 1600×1280; 11 markers map in order to 11 unique Element IDs; 7 event definitions; all 26 relative Markdown links resolve; tracker row status and SH-06 handoff match. | VERIFIED |
| Source preservation | SHA-256 `screen.png`=`f13f4da1e7717ccafbf93155af94e526e8a5f865d63e207c21165118c16cd23f`; `code.html`=`cd0f2cb849d8a39aae842c08f5602fc24718b2d34e9f446d56041c1017b8ad7a`; both match pre-edit values. | VERIFIED |
| `git diff --check -- apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` and whitespace scan of SH-05/worklog files | No diff whitespace errors or trailing whitespace. | VERIFIED |
| Tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining blockers: 401 cause/recovery; token storage/concurrency/timeout policy; safe-return fallback; production UI composition/copy; adjacent SH-02 API #03 contract discrepancy G-14.
- Next owner/action: SH-05 static review is complete; handle SH-06 only in a separate session.
