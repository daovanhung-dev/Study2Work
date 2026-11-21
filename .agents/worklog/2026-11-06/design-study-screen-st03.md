---
task_id: "2026-11-06-design-study-screen-st03"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-03 APIs #04/#13/#14; Student session from SH-02; return navigation to ST-02"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-03

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 168 exact-type docs worklogs available; 3 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep inventory/expected separate from current API and UI source; preserve static assets; Study Web remains UNWIRED; fake-session tests/DDL do not prove live schema.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Keep UI screenshots and API current source/contracts distinct; no client route/cache/navigation can be inferred; mark unsupported fields and source state conflicts.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Use current backend source over stale catalog labels while recording `DISCREPANCY`; a screen-only DD does not establish runtime; one Screen ID per session.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Objective: continue the 83-screen Study LMS DD goal; one Screen ID this session; plan before DD/annotation; trace each control/event/API; preserve source assets; update tracker/worklog; keep DD, implementation and runtime statuses separate.
- ST-03 inventory: proposed `/student/profile/edit`, AC-11, Student actor, APIs #04/#13/#14; edit full name/phone/bio/avatar; if avatar changes: #13 upload, #14 profile update, then #04 refresh; return to ST-02.
- Canonical expected sources: `apps/study-client/docs/list_screen.md` ST-03, AC-11 index/diagram, `docs/lists/list_api.md`, API #13/#14 DD. G-03 identifies bio persistence, phone nullability and avatar mapping conflicts. These remain expected/design evidence, not runtime proof.
- Skill routing: manifest/skill index excludes `web-ui-only-dd` from `createDD-markdown`; no canonical UI-only DD skill applies.

## CURRENT_BEHAVIOR

- Asset baseline: `screen.png` 1418×1600, SHA-256 `acd143a1a7d5dae4936f9bc8a3d51d015ba1fb501998a5434e96b57942d77fdc`; `code.html` SHA-256 `a8c9ebca162d9ac677b65ede88543d9a932c85b4cffed05093f263d24de511b3`. Screenshot and a temporary Firefox HTML render were visually compared; their layout/copy align. Original files remain unchanged.
- Current Study Web status is `UNWIRED`: no app source/package/router/entrypoint. HTML anchors use `href="#"`; full-name input is native but has no handler; email is readonly; phone/bio/upload/save are disabled. No fetch/XHR/API call or session binding exists.
- API #04 current source requires Bearer JWT with Student role, reads by JWT `sub`, and returns safe `UserProfile`; no `bio`. Current route/query/model source was reread.
- API #13 current source is registered and source-backed: POST JSON `{image: <Data URL>}`, Student auth, MIME/signature/decoded-size validation, S3-compatible upload at `avatars/{user_id}`, HTTP 201 `{data.avatar_url}`. It does not use DB. Storage configuration/network is not verified here.
- API #14 current source is registered and source-backed: PUT requires `full_name`, `phone`, `avatar_url`; model ignores extra `bio`; validator trims name/nullable strings, rejects blank name and enforces max 150, enforces phone max 20, but does not validate avatar URI. SQL updates safe fields/updated_at by JWT user ID with `RETURNING`, validates `UserProfile`, commits on success; failures rollback. Checked-in DDL has nullable phone, no bio and nullable status; live schema is not verified.
- API test files #13/#14 and API DD documents were read only; tests were not run. API #14 DD says source absent, contradicted by current route/module/tests. Inventory and UI diagnostic also say #13/#14 are halted/unwired; backend source exists, while UI remains unwired.

## SOURCE_TRACE

```text
proposed ST-03 route after Student session
  -> expected GET #04 /api/v1/users/me
  -> optional POST #13 /api/v1/users/me/avatar (Student JWT -> validate Data URL -> S3-compatible put avatars/{user_id} -> return avatar_url; no DB)
  -> PUT #14 /api/v1/users/me/profile (Student JWT -> normalize fields -> UPDATE users by JWT sub -> validate UserProfile -> commit/return)
  -> AC-11/inventory expects GET #04 to refresh; current #14 already returns UserProfile and does not call #04
  -> return to ST-02 by expected navigation; current HTML links are href="#" and Study Web is UNWIRED
  -> #13/#14 test source read only; no tests/runtime/live S3/live DB run
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Inventory/UI says APIs halted | Current `app/api/v1.py`, modules and tests include #13/#14; client app source is absent. | `DISCREPANCY` / UI `UNWIRED` | Keep backend source-backed status distinct from frontend wiring. |
| API #13 representation | Current `list_api.md`/API #13 DD/source use JSON Data URL and `AvatarUploadResult`; screenshot diagnostic mentions multipart/CDN and `UserProfile`. | `DISCREPANCY` | Do not describe the diagnostic text as current backend contract. |
| API #14 body/response | Catalog/AC require bio and non-null phone/URI avatar; current model ignores bio, accepts nullable phone/avatar, response has no bio, avatar URL is only trimmed. | `DISCREPANCY` / `BLOCKER` | Field persistence, phone policy and avatar reference policy remain unresolved. |
| Reload after save | AC-11/list_screen expects #04 after #14; current #14 returns profile directly and makes no #04 call. | `DISCREPANCY` | Product/FE must decide whether to consume PUT response or refetch; no client behavior exists. |
| Partial upload/update | #13 external S3 side effect precedes #14 DB update; same-user key overwrites; no compensating delete/idempotency policy. | `OPEN` | A failed #14 cannot undo #13 storage write. |
| Screenshot gate | G-03 pill/banner and disabled controls are static HTML; they are not a #13/#14 HTTP response. | `DESIGN_STATE` / `UNWIRED` | Preserve the gate as design evidence without claiming a runtime feature flag/state. |

## CHANGES

- `ST-03_PLAN.md` was written before annotation/DD, then finalized with audit results.
- Created `ST-03.md`, `ST-03_markers.json`, `ST-03_markers_overlay.svg`, and `screen_annotated.png`; kept `screen.png` and `code.html` unchanged.
- Updated `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` with ST-03 statuses, 16/83 artifact bundle count, blocker summary, and ST-08 next pointer.
- No API, Study Web app code, tests, schema, contract, or context page changed.

## VERIFICATION

| Static audit | Result | Status |
|---|---|---|
| Marker/element mapping | JSON IDs 1–26; DD has 26 matching rows; SVG has 26 circles/numbers. | VERIFIED |
| Original assets | PNG and HTML SHA-256 match baseline hashes. | VERIFIED |
| Image output | Source 1418×1600; annotated 2996×3200; visually reviewed. | VERIFIED |
| Markdown links | All relative links in ST-03.md resolve. | VERIFIED |
| `git diff --check` | No whitespace errors. | VERIFIED |
| Tests/runtime/live services | No tests run; no app runtime, live DB or Object Storage verification. | NOT RUN / NOT VERIFIED |

## HANDOFF

- This worklog covers ST-03 only. Next screen pointer in the W1 tracker is ST-08. Do not start another Screen ID in this session.
