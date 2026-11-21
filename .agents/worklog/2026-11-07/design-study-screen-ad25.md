---
task_id: "2026-11-07-design-study-screen-ad25"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-38; APIs #103/#18; AD-24 → AD-25 → SH-07 export-operation handoff"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-25

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 230; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current evidence separate; preserve source assets; do not infer report KPI/date/permission semantics; Study Web and #101 remain unwired unless current source proves otherwise.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Trace contract against source; do not infer navigation, filter or authorization behavior; distinguish local API evidence from Draft and runtime; no tests/runtime claim without running them.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Preserve original assets and current-source-first evidence; do not infer identity, role or handoff from mockups; fake DB/test evidence does not prove live schema/runtime.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-25 only in this session; write `AD-25_PLAN.md` before marker map, annotation or DD; preserve existing source assets; map all visible elements to ordered markers and A–F DD rows; trace export and operation lifecycle to AC-38, inventory, APIs #103/#18 and current source; update inventory, global screen plan and worklog; distinguish DD, implementation and runtime status.
- Inventory row 83: AD-25 “Xuất báo cáo và theo dõi tiến trình”, candidate `/admin/reports/export`, AC-38, APIs #103/#18; choose format and filters, track progress and download only when an operation has a result URL; expected `queued/processing/ready/failed/expired`; links AD-24 and SH-07; P2. Inventory currently marks this screen D and calls out export URL/result schema/format allowlist as unresolved.
- Cross-screen contract to verify: AD-24 inventory expects filter preservation; AC-38 has an optional export branch; SH-07/#18 must only be used with an approved operation ID/type/ownership mapping. Catalog and runtime behavior must be checked independently.

## CURRENT_BEHAVIOR

- Target folder `apps/study-client/docs/screen_stitch/05_admin/AD-25_xuat-bao-cao-va-theo-doi-tien-trinh/` initially contains only `screen.png` and `code.html`. Source image is 1368×1600; SHA-256 `5d90eabc1fcf154433771d58b91e814e6fc6a40e89933ffac9c5b0f35522b722`. HTML is 27,722 bytes; SHA-256 `0cd68b7aba2052a35cf89289241cf125c64ca1c1cce9e23d5d0187c276a861be`.
- Prototype contains format radios (`csv` selected, `xlsx`, `pdf`), dataset checkboxes (course and learner selected; community unselected), period radios (`month` selected; `week` and `custom`), a submit button, a disabled download button and a static SH-07 queue callout. `onsubmit="event.preventDefault();"` cancels form submission; no other handler, fetch/XHR, route client, timer or storage request is present. Navigation and footer anchors use `#`; the back-to-AD-24 anchor also uses `#`.
- Progress text is static: no Operation ID, “Sẵn sàng khởi tạo”, no downloadable link, and placeholder policy claims about Celery, Worker Node 04, RBAC L3, SHA-256, signed URL 120 minutes, audit logging and 24-hour deletion. These are not backed by this HTML's behavior or current Study service source.
- Study Web has no tracked `apps/study-client/src` files or editable router/client/package manifest. The screen is documentation/prototype evidence only; route/runtime remains `UNWIRED`.
- Current Study router/modules/tests have no #103 export or #18 operation path/module/query/model/test. Router composition is source-backed through #98. Study app search found no Celery/export worker/download serving implementation. No report-export Operation store or lifecycle was found in Study source.
- DB artifacts: V1-PILOT defines general `file_objects`, `report_snapshots` and separate `evidence_export_requests`; the latter is for signed learner evidence requests. None is mapped to AC-38 export or proves live schema/deployment. `file_objects` notes signed URLs up to five minutes in its generic pilot purpose metadata, which does not establish an export TTL; this differs from the mockup's unsupported 120-minute claim. `report_snapshots` is a report-data snapshot candidate, not an export job/file mapping.
- Inventory row 83/global plan show API #103/#18 D and AD-25 not started. AD-24 is the prior screen; do not start another Screen ID after AD-25.

## SOURCE_TRACE

```text
Expected: inventory links AD-24 → AD-25 and says #103 returns 202; catalog row payload is `ApiEnvelope<Report>`, while the Operation-tracking paragraph says `data:Operation`. AC-38 shows #103 → generate CSV/XLSX/PDF or job → temporary storage if server-generated → show report/download; an `operation_status` #18 node exists in the AC-38 page but has no connected edge. Inventory conditionally expects #18 after an approved `operation_id`; its ID is `int64` in the API row but UUID in reusable schema/AC diagrams. #103/#18 API DDs remain Draft and enumerate unresolved filter, format, response, ID, owner, result, storage, expiry and lifecycle decisions.
Current: no Study Web caller/router/client and no #103 or #18 route/module/query/model/test; no export worker/storage-serving flow. Current prototype selection state remains local; submit is explicitly prevented with no action; download is disabled; SH-07 is non-navigating copy. No API is called and no operation/download response is mapped.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| #103 response | Catalog endpoint row says 202 `ApiEnvelope<Report>`; same catalog's Operation tracking says #103 returns `Operation`; AC-38 describes a job and poll node. | `DISCREPANCY / BLOCKER` | Do not select a response payload or claim a pollable operation ID. |
| #18 identifier, access and lifecycle | API row is `operation_id:int64`/owner; reusable schema and AC use UUID; catalog tracking says owner/Admin while AC says owner-only; status enums/storage/result schema are open. | `DISCREPANCY / BLOCKER` | Cannot bind IDs, define status transitions/terminal states, or promise SH-07 polling. |
| AC-38 poll edge | AC-38 contains an #18 `operation_status` node but its edges connect #103 → generate → temporary storage → display/download; no edge reaches #18. Inventory adds conditional #18 handoff. | `DISCREPANCY / OPEN` | Confirm whether/when AD-25 polls #18 before implementing navigation or polling. |
| Filter and format mapping | #103 only declares optional `filters:string` and `format:string`; serialization/default/enum/validation are open. Prototype uses three arbitrary dataset toggles and week/month/custom, not AD-24 `from/to/segment`; custom has no date controls. | `OPEN / BLOCKER` | Cannot serialize settings or ensure export matches dashboard; do not add 400/422 absent catalog support. |
| GET acceptance/retry | #103 is GET but semantically accepts an async job; no idempotency/retry contract or durable-acceptance source exists. | `DISCREPANCY / BLOCKER` | Repeated submit/retry semantics cannot be specified. |
| Storage, download, and policy claims | AC-38 only conditionally mentions temporary server storage; #103 DD has ExportAsset as DERIVED and no approved storage mapping. Mockup claims 120-minute links, SHA-256, audit/IP/session log and 24-hour cleanup; pilot file tables are not mapped to export. | `STATIC_ONLY / SOURCE_REQUIRED` | Do not claim checksum, signed URL, audit event, TTL, cleanup or browser cache policy as runtime behavior. |
| Study Web/API runtime | Current tracked Study Web source and local #103/#18 route/test searches found no implementation; server composition ends at #98. | `UNWIRED / NOT_FOUND` | Route, request, polling and download are not runtime verified. |

## CHANGES

- Created `apps/study-client/docs/screen_stitch/05_admin/AD-25_xuat-bao-cao-va-theo-doi-tien-trinh/AD-25_PLAN.md` before marker/DD authoring, with evidence register, source hashes, expected/current boundaries, blocker and event plans.
- Created `AD-25_markers.json` (46 ordered elements), transparent `AD-25_markers_overlay.svg`, and `screen_annotated.png` (2× render at 2736×3200). Visually reviewed the final annotated image; marker centers stay clear of the screenshot text. Original `screen.png` and `code.html` are unchanged.
- Completed `AD-25.md` sections A–F: source-backed overview, expected/current flow, 46 element rows, EV-01…EV-09, current/proposed state boundaries, navigation/accessibility/security notes, acceptance criteria and ten implementation blockers.
- Updated inventory row 83 and API dependency index rows #018/#103 in `apps/study-client/docs/list_screen.md`; #18/#103 remain `D` and are described as catalog/Draft-only without current local implementation.
- Updated the AD-25 status row and appended the 2026-11-07 AD-25 checkpoint in `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; tracker records inventory/folders 83/83 and core artifacts 78/83.
- CONTEXT_UPDATES: none. Context pages and manifest were not changed in this task.
- Assumptions: none. Report API behavior, filter/format mapping, operation lifecycle and artifact policy remain explicitly unresolved.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Goal objective, root router, context map, worklog guide and three exact-type prior docs worklogs reviewed before deep inspection. | VERIFIED_PREFLIGHT |
| Source/contract trace | AD-25 asset/HTML, AC-38, inventory/API catalog, #103/#18 Draft DDs, current Study router/auth/source/test tree, DB candidates and AD-24/SH-07 handoff reviewed; no current Study Web route/client, #103/#18 route or export worker/download source found. | VERIFIED_SOURCE_REVIEW |
| Marker and image audit | 46 markers sequential/unique/in bounds; plan/JSON/DD/SVG IDs and coordinates align; SVG XML parses; 46 circles/labels; nearest rendered marker centers 65.1 px apart for 44 px markers. `screen.png` is 1368×1600; annotated PNG is 2736×3200 and was visually reviewed. | PASS_STATIC |
| DD/link audit | A–F headings, 46 element rows and EV-01…EV-09 present; all local Markdown links in AD-25 DD/plan resolve. | PASS_STATIC |
| Inventory/artifact audit | 83 unique inventory Screen IDs and 83 screen folders; 78/83 have the four core artifacts after AD-25. API #018/#103 reverse-index source status remains D. | PASS_STATIC |
| Source preservation/whitespace | `screen.png` SHA-256 `5d90eabc1fcf154433771d58b91e814e6fc6a40e89933ffac9c5b0f35522b722`; `code.html` SHA-256 `0cd68b7aba2052a35cf89289241cf125c64ca1c1cce9e23d5d0187c276a861be`; authored text files contain no trailing whitespace; scoped `git diff --check` passed. | PASS_STATIC |
| Application tests/runtime | Not run; there is no Study Web route/client for this screen, and the task only requires static DD verification. | NOT_RUN |

## HANDOFF

- AD-25 documentation and static verification are complete. Stop after this Screen ID for the current session; do not start another Screen ID.
- Remaining implementation blockers: #103 response and GET/retry semantics, filters/formats/authorization, #18 ID/access/lifecycle/result/store and missing AC-38 poll edge, export artifact/download policy, AD-24 filter continuity, and absent Study Web/API runtime source.
