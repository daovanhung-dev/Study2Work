---
task_id: "2026-11-06-design-study-screen-sh02"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-02 sign-in UI -> API #03/#04 and uncatalogued refresh R-X01; token/session and role routing contract"]
status: "VERIFIED"
---

# Worklog: Rà soát Detailed Design màn hình Study SH-02

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- selector_result: READY; selected 3 of 154 docs worklogs and read all selected files.
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-11-06/design-study-screen-sh01.md
    - carry_forward: Keep DD READY, IMPLEMENTATION BLOCKED and RUNTIME VERIFIED separate; preserve source assets; use explicit marker-to-element IDs and source-backed event traces.
  - path: .agents/worklog/2026-11-05/check-study-screen-stitch-coverage.md
    - carry_forward: Inventory covers 83 screen IDs; artifacts are design evidence only and do not prove client runtime.
  - path: .agents/worklog/2026-11-05/co-locate-study-screen-documents.md
    - carry_forward: SH-01 through SH-04 DD, plans and marker maps belong beside source assets; preserve original PNG/HTML hashes.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Complete SH-02 within this one-screen session; review/update its plan before modifying DD or generated artifacts; preserve original source PNG/HTML; verify clean preview, annotated image and one-to-one marker map; trace all events and API flows to current source; update global tracker and this worklog.
- Canonical contract: list_screen.md SH-02 row 02, AC-02, API #03/#04, F01, G-02/G-14, API catalog and current Study Server source; Study design guide is intended UI target, not runtime evidence.

## CURRENT_BEHAVIOR

- Assets: SH-02 folder contains screen.png, code.html, screen_rendered.png, screen_annotated.png, SH-02_markers.json, SH-02_PLAN.md and SH-02.md. Source PNG is 1280×1024 and visually blank; rendered HTML and annotated preview are 1280×1024 and 2560×2048 respectively.
- UI runtime: apps/study-client/src, apps/study-client/package.json, .agents/web-work/study/AGENTS.md and INDEX.md are NOT_FOUND in the current tree.
- Existing preview and annotated image were visually reviewed: the clean HTML render shows the centered login card; all eight markers are visible and do not cover important content.
- Original PNG and HTML hashes were rechecked and match the recorded values.
- API #03/#04 source and test files are present; tests will not be run unless requested. Live DB/deployment are not established by source-only review.

## SOURCE_TRACE

- Expected behavior was compared across `apps/study-client/docs/list_screen.md` (SH-02, F01, G-02/G-14), AC-02 diagram and `docs/lists/list_api.md`.
- Current #03 route is registered in `apps/study-server/app/api/v1.py` and implemented by `api_03_auth_login/{validate.py,view.py,query.py,models.py}`. It trims/validates email (max 255 after normalization), rejects blank password after a temporary strip check while preserving the original password for verification, returns generic 401 for unknown/wrong credentials, 403 for non-ACTIVE accounts, 422 validation errors, and 500 safe internal errors. Success is HTTP 200 `DESIGN_RESOURCE_RETRIEVED` with allowlisted profile plus access/opaque refresh tokens; refresh-token HMAC hash is stored transactionally.
- Current #04 route is in `app/api/v1.py`; `api_04_users_me/{view.py,query.py,models.py}` and `app/utils/auth.py` enforce Bearer/JWT claims and STUDENT role before DB lookup. Success returns the safe profile fields without `permissions`, `bio`, token or password hash; role mismatch is 403, invalid/missing JWT or missing profile is 401, and DB/model errors are safe 500s.
- R-X01 `POST /api/v1/auth/refresh` is registered in `app/api/v1.py` and implemented in the #03 auth module; it rotates opaque refresh tokens transactionally and is present in runtime source but absent from the API catalog.
- Source tests exist at `apps/study-server/tests/modules/guest/api_03_auth_login/test_auth_login.py` and `apps/study-server/tests/modules/guest/api_04_users_me/test_users_me.py`. They use fake sessions/fixtures and were not run.
- `infra/postgres/study-server/DB.sql` and `migrations/002_refresh_tokens.sql` were traced as committed candidates only; no live schema/deployment claim is made.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Source screenshot | screen.png is blank while code.html renders a login card; a derived preview exists. | SOURCE_IMAGE_INVALID_FOR_CONTENT / DERIVED_PREVIEW | Preserve blank source and mark preview provenance; do not call it runtime UI. |
| Study Web wiring | Current tree lacks Study client source/router/package and referenced Study subcontext pages. | UNWIRED / NOT_FOUND | No route, token persistence or client behavior is runtime-verified. |
| API #03 response | Canonical catalog says 201 `DESIGN_RESOURCE_CREATED`, `UserProfile` only, and 422/500; AC/current source say 200 and source returns profile+tokens with 401/403/422/500. | DISCREPANCY / DD BLOCKED | Do not choose a parser contract or combine the two shapes. |
| Session policy and frontend wiring | Study Web source/router/session manager are absent; token storage, refresh/logout policy and retry behavior are unapproved. | UNWIRED / IMPLEMENTATION BLOCKED | Do not claim runtime behavior or pick browser storage. |
| Role bootstrap | API #04 requires STUDENT while #03 can issue profiles/tokens for other roles; Mentor/Admin route/profile and permissions contract are not defined. | BLOCKED / G-02 | Do not call student profile endpoint or route Mentor/Admin to `/student`. |
| Return destination | `returnTo` allowlist and default destinations have no client router implementation/approval. | OPEN | Document as proposed safe behavior only. |

## CHANGES

- Files changed: `SH-02_PLAN.md` reviewed first and updated with plan status, stable Element IDs, Event ID inventory, and acceptance checks; `SH-02.md` updated with DD/implementation/runtime statuses, stable Element/Event IDs, complete event metadata, source trace links, and explicit blockers; `SH-02_markers.json` updated with `SH-02`, `SH02-EL-01..08`, and coordinate provenance; global `dd_screens/PLAN.md` updated with SH-02 status and SH-03 handoff; this worklog completed.
- Original `screen.png` and `code.html` were not changed. Existing derived clean/annotated previews were retained after visual review; no image was regenerated.
- CONTEXT_UPDATES: None; no context pages changed. Current source/context discrepancies are recorded in the SH-02 DD and this worklog.
- Context pages changed: None.
- Assumptions: UI-only DD is not covered by createDD-markdown, which is registered for Web/API DD and explicitly excludes web-ui-only-dd.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| node scripts/select-worklogs.mjs --type docs --limit 3 | Selected 3 exact-type worklogs of 154; read all three. | VERIFIED |
| Static marker/event/link/image audit | JSON valid; numbers 1–8 map one-to-one to SH02-EL-01..08; SH02-EV-01..13 each has trigger/type, precondition, input and API/output metadata; all local links resolve; PNG sizes are 1280×1024, 1280×1024 and 2560×2048. | VERIFIED |
| SHA-256 source integrity | `screen.png` = `5c3cb8e59c1b645c4338ce527d5fd2c7a2288568fc04982481865d422ec4e323`; `code.html` = `6e848c7bbab66b13f0486eb397b9da8a0e2059f3d9b169287b8359b8c1aad595`. | VERIFIED |
| git diff --check | Removed trailing whitespace from the DD status line; final repository diff check reports no whitespace errors. | VERIFIED |
| Final SH-02 static audit | All 8 markers/element IDs align; all 13 Event IDs are ordered and include required metadata; all relative Markdown links resolve; rendered image dimensions and source hashes match. | VERIFIED |
| Tests/runtime/context validation | Project tests and runtime not run; context pages unchanged, so context validator not applicable. | NOT_RUN |

## HANDOFF

- Remaining blockers: #03 contract reconciliation; safe token/session and refresh/logout policy; Mentor/Admin role bootstrap; approved `returnTo`/default route; Study Web implementation; blank original screenshot acceptance; missing HTML handlers; missing web-study context pages.
- Final screen status: DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED.
- Next owner/action: SH-03 is the next W0 screen; this session handled SH-02 only.
