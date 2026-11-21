---
task_id: "2026-11-07-design-study-screen-ad04"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AD-04 Study Web /admin/users/:userId/edit ↔ APIs #69/#70; AC-31 handoff from AD-03 and return to AD-03 after edit/cancel"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-04

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 209; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Preserve expected/current separation; verify Study Web route each session; do not map mockup controls to API without evidence; keep API contracts and runtime source distinct.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: AC-31's user-management permission is not proven by the local `ADMIN` claim fallback; keep PII/lifecycle/live-schema policy open and use selected numeric ID for the next detail screen.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: AD-03/#69 is locally source-backed but API DD remains Draft; legacy schema, `ADMIN` mapping, PII and lifecycle decisions remain open. AD-03 edit handoff is disabled; #70 body/role rules belong to this screen. Study Web is `UNWIRED`.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-04 only in this session; inspect inventory, AC-31, API #69/#70 contract and current source; write `AD-04_PLAN.md` before markers/annotation/DD; preserve source assets; create ordered one-to-one markers and annotated image; author A–F DD with field mapping, validation, events/API/errors, states/navigation and unresolved decisions; update `list_screen.md`, `dd_screens/PLAN.md`, and this worklog; distinguish DD readiness, implementation block and runtime verification.
- Inventory row 62: AD-04 “Chỉnh sửa người dùng”, proposed `/admin/users/:userId/edit`, AC-31, APIs #69/#70; edit allowed fields/role, dirty state and cancel; `GET #69 → PUT #70 → GET #69`; linked back to AD-03; states loading/dirty/saving/validation-error; P1; existing gate says API #70 body not specified.
- Direct API #70 contract: `PUT /api/v1/admin/users/{user_id}`, Bearer JWT/Admin, required signed-int64 path, `ApiEnvelope<UserProfile>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, errors 401/403/404/422/500. Catalog/AC omit request-body schema. Current source exposes a strict full-replacement body as `DERIVED`; inspect exact fields/rules and do not treat them as owner-approved.

## CURRENT_BEHAVIOR

- Source assets: `screen.png` 1280×1271 RGBA, SHA-256 `a2057daddda59b1767edafa6287b3cd50d98609f7f3fe49a2515c76e6628e647`; `code.html` SHA-256 `2d81ba068bfdb052d57b6ebc3ddc71218c4fefd7898b4c04ea78da962f3da90a`.
- Prototype shows a static locked form: disabled name/email/role/status/admin-note controls and disabled Save; a Cancel link goes to `/admin/users`; the top back link uses `/admin/users/USR-9281-VN/details`; a “Gửi yêu cầu” button and API-doc button have no handler. HTML has no fetch/XHR/client API call; the form's inline submit only calls `preventDefault()`.
- Prototype record ID `USR-9281-VN`, role option `lecturer`, status options `active/locked/pending`, email/status/adminNotes, audit claims, SSO/compliance/sync progress and body-gate copy do not map directly to #69/#70. #70 expects path int64 and a locally derived strict body with required `full_name`, nullable `phone`, nullable `avatar_url`, and role `STUDENT|MENTOR|ADMIN`.
- Study Web root rechecked: only `dist/`, `docs/`, `node_modules/` and `tsconfig.tsbuildinfo`; editable app source/package/router/API client absent (`UNWIRED`).
- API #70 route/module/query/model/validation/test source and Draft DD reviewed. Local view updates only `full_name`, `phone`, `avatar_url`, `role`, and `updated_at`; it preserves email/status, returns safe `UserProfile`, commits after projection validation, and rolls back failures. Focused test source has 19 cases per context; tests were not run and use fake DB sessions.

## SOURCE_TRACE

```text
Expected: AD-03/#69 numeric user ID → AD-04 `GET #69` to populate current profile → edit approved fields → `PUT #70` → refetch #69 and return to AD-03 after confirmed success/cancel. The #70 catalog/AC omit its body, so body semantics remain unresolved at the contract layer.
Current: no Study Web route/client. Prototype values are hard-coded and form controls/save are disabled; “Cancel” links AD-02 while the top back link uses a different AD-03 path. Local #70 route takes typed strict body; view's shared `ADMIN` guard precedes custom path validation/DB; body fields and validation are DERIVED; a bound UPDATE changes only profile/role candidate columns and commits after safe UserProfile projection. Tests use fake sessions and were inspected only.
DISCREPANCY: screenshot asks for email/status/admin note and uses `lecturer`/`locked` labels; #70 body accepts only full_name/phone/avatar_url/role and has no email/status/adminNotes field. Route uses signed-int64 ID while prototype ID/path is `USR-9281-VN`. Static sync/RBAC/audit/compliance/gate claims have no #69/#70 source.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #70 body contract | Catalog/AC omit body; current strict four-field model/OpenAPI is `DERIVED`, API DD is Draft. | DISCREPANCY / BLOCKER | Do not elevate local body/role allowlist to approved contract; preserve exact implementation behavior separately. |
| Screen fields/options vs #69/#70 | Prototype ID is string code; role/status/email/adminNotes differ from required numeric path and #70 writable body; phone/avatar_url are missing from visible form. | DISCREPANCY / BLOCKER | Keep mutation disabled until body, preserved nullable-field strategy, role mapping and status ownership are approved. |
| Admin permission, PII, token and schema policy | Source uses `ADMIN`; email/phone in UserProfile; role mutation does not revoke token; legacy BIGINT schema is only a local candidate. | POLICY OPEN | Do not infer fine-grained authorization, unmasked PII display, role-transition/self-admin rules, or live DB state. |
| Request validation/auth order | API DD/context says guard before body validation; route declares typed `AdminUserUpdateRequest`, and middleware handles Pydantic 422. Focused tests cover auth-before-DB with a valid body but do not cover invalid body plus missing/invalid auth. | ORDER NOT CHARACTERIZED / DISCREPANCY | Do not state auth-before-body as verified; identify as source-level ordering question for API owner. |
| Prototype gates/audit/support claims | Static “85% sync”, API #69 verified, body mutation locked, audit note/SSO/compliance and unlock request have no mapped endpoint/source. | STATIC_ONLY / UNMAPPED | No invented gate or ticket workflow; design needs decision/source. |
| Study Web route/runtime | Current root tree lacks editable source/router/package manifest/client. | UNWIRED | No implementation/runtime claim. |

## CHANGES

- Added `AD-04_PLAN.md` before marker, annotation, or DD authoring; plan execution steps now record the completed order and blockers.
- Added `AD-04_markers.json` and `AD-04_markers.svg` with 40 ordered markers, and `screen_annotated.png` at 2× (2560×2542). Original `screen.png` and `code.html` were not modified.
- Added `AD-04.md` with sections A–F, 40 one-to-one element rows, six event specifications, API #69/#70 mapping/errors, route/state matrix and unresolved contract/policy decisions.
- Updated `list_screen.md`: AD-04 now records source-backed local #70, derived body contract, status/error states and blockers; reverse API source index #070 changed D→R. Formal API catalog/body remains unapproved and API DD remains Draft.
- Updated `dd_screens/PLAN.md` AD-04 row and session checkpoint: 57/83 core bundles; `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.
- Context pages changed: none in this session. The workspace already contained unrelated uncommitted context/document changes; they were not reverted or edited by this task.
- Assumptions: none. Current local API body is recorded as `DERIVED`, not owner-approved.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective, root router, context map, worklog contract/template reviewed; exact docs selector READY 3/209; AD-01, AD-02, AD-03 worklogs fully reviewed. | VERIFIED |
| Plan-before-authoring order | `AD-04_PLAN.md` existed before `AD-04_markers.json`, SVG, annotation and DD; 40 marker coordinates match the plan. | VERIFIED |
| Marker/DD static audit | JSON parses; SVG XML parses; IDs 1–40 are ordered/unique/in-bounds and align with 40 element rows; all plan coordinates match JSON. | VERIFIED |
| DD/link audit | A–F headings present; all local Markdown links in AD-04.md resolve. | VERIFIED |
| Image/source audit | `screen_annotated.png` is 2560×2542; annotation viewed; original `screen.png` SHA-256 `a2057daddda59b1767edafa6287b3cd50d98609f7f3fe49a2515c76e6628e647` and `code.html` SHA-256 `2d81ba068bfdb052d57b6ebc3ddc71218c4fefd7898b4c04ea78da962f3da90a` match pre-authoring hashes. | VERIFIED |
| Inventory/core-bundle audit | 83 unique Screen IDs and 83 matching folders; 57/83 have all four core artifacts after AD-04. | VERIFIED |
| Whitespace/diff audit | `git diff --check` passed on `list_screen.md` and global plan; new AD-04 authored text/JSON/SVG has no trailing whitespace; final tracker diff check passed. | VERIFIED |
| Application test/runtime | Focused test source reviewed only; no application tests or runtime verification were requested/run. | NOT RUN / NOT VERIFIED |

## HANDOFF

- Remaining blockers: API #70 body/role approval; phone/avatar preservation decision; Admin permission and role-transition rules; PII/audit/lifecycle/token policy; numeric-ID route alignment; unsaved-change navigation; gate/help/ticket source; live schema/deployment; request-validation/auth-order clarification; Study Web remains `UNWIRED`.
- Next owner/action: process AD-05 only in a separate session; AD-04 is not `DD READY`, implementation is blocked, and runtime is not verified.
