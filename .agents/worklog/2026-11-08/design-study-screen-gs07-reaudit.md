---
task_id: "2026-11-08-design-study-screen-gs07-reaudit"
date: "2026-11-08"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["GS-06 resourceId and ST-12 lesson/resource context -> GS-07 -> API #12; return/error mapping may involve GS-06, ST-12 and SH-06"]
status: "VERIFIED"
---

# Worklog: Re-audit Detailed Design màn hình Study GS-07

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 263 exact-type docs worklogs available; selected three; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current behavior separate; trace API declarations to current route/query/response; do not claim a local source or fake-session test proves deployed runtime or live schema.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Preserve Study Web `UNWIRED`; keep mock controls and values separate from API behavior; trace filters and data contracts to current source.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Do not infer identity, PII, privacy policy or route behavior from a mockup; keep API DD and runtime/source statuses distinct.
- additional target handoff reviewed: `.agents/worklog/2026-11-06/design-study-screen-gs07.md`; existing artifacts are prior work to recheck, not current-source authority.
- additional dependency handoff reviewed: `.agents/worklog/2026-11-07/design-study-screen-gs06-reaudit.md`; preserve #11/#12 and AC-06 discrepancies and trace `resourceId` as an unverified UI handoff.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Continue the active 83-screen objective and re-audit GS-07 only in this session. Update the screen plan before DD/marker/tracker edits; preserve original assets; verify the existing marker map and annotation; update `GS-07.md`, `list_screen.md`, `dd_screens/PLAN.md`, and this worklog. Keep `DD READY`, `IMPLEMENTATION BLOCKED`, and `RUNTIME VERIFIED` as distinct statuses.
- Inventory row 14: GS-07 “Xem/tải tài nguyên (Page)”, proposed `/resources/:resourceId`, AC-06, API #12; preview supported metadata/media and fallback download only where URL/access is valid; linked from GS-06, with ST-12 resource context also requiring explicit handling. Inventory states include loading/ready/403-unclear/404/link-expired.
- AC-06 expected flow: public or authorized resource access; denied access has a 403 branch; private object access uses an Object Storage signed URL before open/download. This must stay separate from API catalog/current-source behavior until contracts converge.
- Canonical UI target: `.agents/web-study/design.md`; it defines design expectations, not runtime behavior. Web UI-only DD has no canonical authoring skill per registry.

## CURRENT_BEHAVIOR

- Original `screen.png` is 1588×1600, SHA-256 `11068f47467e5f5f47a074c833912a17816ce3cb4f95e34b59e5b2163b56259b`; original `code.html` SHA-256 `e6550d5ba83fa27acc9f704b7599609ded9ab549175eaaadb4d03885e8bb058b`. Both source assets remain unchanged. Existing annotated PNG was 3336×3200; initial marker JSON had #8–#10 at the same `(3308,940)` center. They have now been separated and the annotation regenerated at 3336×3200; final static mapping/visual audit passes; annotation is 3336×3200 and #8–#10 are separated and legible.
- Current API #12 route is composed in `apps/study-server/app/api/v1.py`, has no auth dependency, and calls `get_resource_detail`. Positive signed-int64 validation maps invalid paths to 404 before DB; query selects `id/lesson_id/name/type/url`; parent course gate is conditional on non-null `lesson_id`; response returns direct stored URL and omits `visibility`; source has no enrollment/visibility check or signer. Success is 200; invalid/missing/parent failures 404; SQL/mapping failures safe 500. Current test source covers these branches and was read, not run.
- Expected AC-06 requires access decision, 403/404 and a signed URL for private Object Storage. API catalog #12 is public/no Bearer with 200/404/500; API DD remains Draft and has a `DECLARED_NOT_RUNNABLE` runtime note that conflicts with current local route/test-source composition. None of this verifies production/deployment/browser runtime.
- Legacy `infra/postgres/study-server/DB.sql` has `resources` with nullable `lesson_id`, `url NOT NULL`, and no `visibility`; `infra/postgres/02_study_db.sql` has no generic `resources` table. Live schema is unverified.
- Study Web current root contains `docs`, ignored `dist`, `node_modules` and build metadata; editable `src`, package manifest and router are absent. Prototype is gated/static with disabled zoom/download, no renderer/request, six text-only state tabs and `href="#"` routes. Its Google Fonts/Tailwind CDN, Plus Jakarta Sans, cobalt palette, 1440px width, mobile-hidden nav and 32×32 controls differ from `.agents/web-study/design.md`; accessibility claims were not measured.

## SOURCE_TRACE

```text
Expected: GS-06 or ST-12 supplies a verified resourceId/context -> GS-07 requests #12 -> authorization and URL policy are resolved -> allowed metadata/media is rendered or downloaded -> return preserves the source context.
Current UI: no editable Study Web route/client -> static gated HTML, disabled preview/download, no API call or resource ID hydration.
Current API: `v1.py` #12 route -> `get_resource_detail` -> positive signed-int64 validator -> Q1 `resources` row -> optional Q2 parent lesson/course check only for non-null lesson_id -> `ResourceDetail` mapping -> 200 envelope direct URL / 404 not-found / safe 500; SQLAlchemy error rolls back. No auth/visibility/enrollment/signing side effect. Tests are fake-session source only and were not run.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Resource access and signed URL | AC-06 diagram requires access decision/403/404 and Object Storage signer for private resources; catalog #12 is public/no Bearer, 200/404/500; current source has no auth/access check/signer and returns direct stored URL. | `DISCREPANCY / BLOCKER` | Do not promote mock simulator states or HTTP 200 to proof of private access. |
| API DD runtime note | API DD #12 remains Draft and says `DECLARED_NOT_RUNNABLE`; current `v1.py` composes the route and current test source exists. | `DOC/SOURCE DISCREPANCY` | Local composition/test source is not production/deployment runtime verification. |
| Schema candidates | Legacy DDL has `resources` (`lesson_id` nullable, `url` NOT NULL, no visibility); V1-PILOT DDL has no generic `resources` table. | `SCHEMA DISCREPANCY / LIVE NOT_VERIFIED` | Do not assert which schema is deployed. |
| Preview/download and source context | Prototype has no renderer/request; zoom/download disabled. MIME/type allowlist, URL safety, expiry and GS-06/ST-12 return semantics lack approved evidence. | `OPEN / BLOCKER` | Keep unsupported renderer/download/navigation policy unresolved. |
| Design/accessibility | Prototype uses CDN fonts/Tailwind, Plus Jakarta Sans, cobalt/1440px, mobile-hidden nav and 32×32 controls; guide differs. Contrast/reflow/focus/reduced motion not measured. | `DESIGN DISCREPANCY / NOT VERIFIED` | Do not repeat prototype WCAG claim as a verified outcome. |
| Study Web runtime | Editable source, package manifest and router absent; ignored `dist` is not app runtime evidence. | `UNWIRED` | No end-to-end/browser/deployment claim. |

## CHANGES

- Files changed: `GS-07_PLAN.md`, `GS-07.md`, `GS-07_markers.json`, `GS-07_markers_overlay.svg`, regenerated `screen_annotated.png`, `apps/study-client/docs/list_screen.md`, `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`, this worklog.
- CONTEXT_UPDATES: none planned unless current source reveals an agent-context page is inaccurate.
- Context pages changed: none.
- Assumptions: none; unresolved behavior remains blocked pending authoritative evidence.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Goal objective and router | Objective reread from `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`; user-provided root router, `.agents/AGENTS.md`, `.agents/context-map.md`, worklog README/TEMPLATE read. | VERIFIED |
| Docs preflight | Selector READY for three exact-type docs logs; AD-01, AD-02 and AD-03 worklogs read in full; shortage none. | VERIFIED |
| Related screen handoffs | Existing GS-07 2026-11-06 worklog and GS-06 2026-11-07 re-audit worklog read. | VERIFIED |
| Current source trace | Inventory/API/AC, route/view/query/validator/model, test source, schema candidates, Study Web tree, Study Web design target, GS-06/ST-12 links reviewed. Test source only; not run. | VERIFIED_SOURCE_REVIEW |
| Current asset/artifact audit | Original hashes preserved; regenerated annotated image visually reviewed. 26 ordered unique in-bounds markers match SVG and 26 DD element rows; SVG embeds the original PNG. Eight events have all six required fields; one relative link resolves. | VERIFIED_STATIC |
| Global inventory presence check | 83 unique IDs match 83 folders and 83 tracker rows; all six core assets/files are present for 83/83. This checks presence only, not DD readiness. | VERIFIED_PRESENCE |
| Static consistency and whitespace | Marker/SVG/DD/event/link audit passed; scoped `git diff --check` and authored-file whitespace scan passed. | VERIFIED_STATIC |
| Application tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining blockers: AC-06 access/403/private signed-URL mismatch with #12 current source; preview/MIME/URL safety and expiry policy; GS-06/ST-12 return-context contract; schema candidate mismatch/live schema unknown; Study Web UNWIRED; design/accessibility mismatch; deployment/runtime not verified.
- Next owner/action: GS-07 re-audit artifacts and tracker are complete; handle GS-08 only in a separate session.
