---
task_id: "2026-11-07-design-study-screen-ad10"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-33 Admin moderation queue; Study Web AD-10 → AD-11; API #78"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-10

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 215; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Separate mockup copy from source-backed behavior; recheck Study Web wiring; don't infer route, API or profile/permission from static prototype; keep tests/runtime/schema evidence distinct.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Keep expected and current evidence separate; trace source auth/query/response/errors; don't equate shared `ADMIN` with AC permission; preserve API DD and live-schema blockers.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Preserve ID handoffs and security boundaries; avoid unsupported static audit/retention claims; distinguish local source from approved API DD and fake DB evidence from live runtime.
- additional_cross_screen_review: `.agents/worklog/2026-11-07/design-study-screen-ad09.md`
  - carry_forward: Keep Admin permission distinct from shared `ADMIN`; record API source versus Draft DD; do not infer behavior from prototype copy; Study Web remains `UNWIRED` unless current editable source proves otherwise.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-10 only in this session. Review its inventory row, AC-33, API #78, current Study Web source and relevant Study Server route/module/schema/tests. Write `AD-10_PLAN.md` before markers, annotation or screen DD; preserve source assets; create a one-to-one marker map and annotated image; author A–F DD; update the screen inventory, global screen plan and this worklog. Record unresolved decisions without inventing moderation policy.
- Inventory row 68: AD-10 “Hàng đợi kiểm duyệt nội dung”, proposed `/admin/content/pending`, AC-33, API #78; pending list by type/course/page, empty state; selecting `content_id` opens AD-11; expected `loading/empty/ready/error`; P1. Existing blocker says Content persistence is absent from DDL and must be rechecked against current source.
- AC-33: Actor Admin; precondition contains pending Content; #78 queue → #79 content detail/version/author → approve via #80 or reject with reason via #81 → reload queue. The diagram/catalog specify singular `ApiEnvelope<Content>` for #78 despite queue/page semantics.
- API #78 DD: `Draft — Needs Confirmation`; body absent; query `type?:string`, `course?:int64`, `page?:int32`; direct response `ApiEnvelope<Content>` and errors 401/403/500. Current-source-derived Page, pagination, exact-filter, active-row and 422 choices remain open.

## CURRENT_BEHAVIOR

- Assets: only `screen.png` (1600×1461, SHA-256 `32320a759dfcdec655b567be530642c988c805812e112eab2c861668e815f066`) and `code.html` (SHA-256 `72d97508568b05e5f3e698a49a0c09631fa716859ec01fc2f52beec71e841eaa`) existed at inspection; no earlier plan, markers, annotation or DD.
- HTML prototype: empty queue/table with 7 headings; search input has no name/handler, type/course selects use placeholder values and have no handler, refresh click only spins/disables locally for 700 ms; “check content” and pagination controls are disabled. No fetch/axios/XHR/EventSource/API URL or interval exists. Count `0/0`, page `1`, empty copy, `System Normal`, RBAC/policy labels and 30-second auto-sync claim are static. All nav/footer/rubric anchors use `#`; notification is no-handler.
- Study Web: current `apps/study-client/` root contains docs, ignored `dist`, `node_modules` and `tsconfig.tsbuildinfo`; editable source, package manifest and feature route/client are absent. Runtime remains `UNWIRED` / `NOT VERIFIED`.
- AC-33/catalog: Admin actor and pending Content precondition; queue → detail/version/author → approve or reject(reason) → reload. #78 direct response is singular `Content`, query `type`, numeric `course`, `page`, and 401/403/500. No distinct moderation permission is named by current screen source.
- API #78 current source: router/module/query/model/validator and focused test source exist. Shared `ADMIN` JWT guard runs before raw query validation/DB; reads active legacy `contents` where status is `PENDING_REVIEW`, applies optional exact `content_type`/signed-int64 `course_id`, counts and returns fixed-size 20 `id ASC` `Page<ContentResponse>` with 1-based page default 1. Empty/late pages return 200; invalid numeric course/page returns local 422; DB/projection failure rolls back and returns safe 500. Read-only; no author, course title, submitted timestamp, version, audit or mutation fields.
- Content sources: checked-in legacy `DB.sql` and migrations 006/007 define BIGINT `contents` and `content_versions`; API #50 and #51 current sources place/update logical rows as `PENDING_REVIEW`. The V1-PILOT UUID `content_blocks`/`content_review_decisions` model is separate and incompatible with #78's int64 Content path. Local DDL/migrations do not prove live deployment/schema.
- API #79 local detail returns the same eight-field Content projection and does not join author/course or version data; its DD leaves revision and author questions open. AC-33 expects those metadata, so the AD-10 “Giảng viên gửi”, course-name and submitted-time columns are not mapped by the #78 response.
- Historical API #78 verification report records 23 focused, 160 linked and 933 full-suite tests passed on fake DB sessions, plus Ruff/OpenAPI checks. Tests were read as evidence only and were not run in this screen session; they do not prove live schema, deployment or moderation policy.

## SOURCE_TRACE

```text
Expected: AC-33 Admin opens the AD-10 pending queue → API #78 → selects a Content item → AD-11/#79 reads Content/version/author → #80 approve or #81 reject with reason → reload queue. Catalog/diagram say #78 is a singular Content envelope while inventory/queue/page imply a collection.
Current: Study Web has no editable caller/route. Static HTML renders empty `0/0`, accepts local filter input and an icon-only refresh animation, but sends no request. Current #78 local route authenticates shared role ADMIN before parse/DB; exact count/list over active legacy PENDING_REVIEW `contents` returns DERIVED Page<Content> with exact type/course filters and fixed page. Its Content fields omit author/course title/created time/version.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Queue response cardinality | Catalog/AC-33 declare singular Content; local #78 returns Page<Content>. | DISCREPANCY / DERIVED | Requires contract owner decision before frontend response mapping. |
| Search/type/course filters | Mockup search/title/lecturer and video/doc/quiz; API #78 has no keyword, raw exact type, numeric course ID; option values are synthetic slugs. | DISCREPANCY / OPEN | Do not invent keyword/author/course-option endpoints or enum mappings. |
| Table metadata | Mockup headings include course name, lecturer and submitted time; #78 Content projection has only id/course_id/type/title/payload/status/parent/order. | UNSUPPORTED / BLOCKER | Do not render those columns as populated source-backed data until contract/source is supplied. |
| Persistence/live schema | Legacy BIGINT DDL and migrations 006/007 exist; V1-PILOT uses a different UUID versioned model. | STALE INVENTORY CLAIM / LIVE NOT VERIFIED | Replace “Content persistence absent in DDL” with local candidate evidence and preserve live deployment/schema blocker. |
| Permission and queue lifecycle | Local shared ADMIN; #78 DD leaves moderation permission, deleted/stale visibility and revision selection open. | OPEN | No fine-grained permission or current-version guarantee is inferred. |
| Study Web/runtime | Editable source/router/client absent; HTML only has a local refresh timer. | UNWIRED | No screen route, API event or 30-second sync exists in current Study Web source. |

## CHANGES

- Files changed:
  - `apps/study-client/docs/screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10_PLAN.md`
  - `apps/study-client/docs/screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10_markers.json`
  - `apps/study-client/docs/screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10_markers.svg`
  - `apps/study-client/docs/screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/screen_annotated.png`
  - `apps/study-client/docs/screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10.md`
  - `apps/study-client/docs/list_screen.md` — AD-10 source status `D→R`, stale DDL blocker replaced, reverse API #078 `D→R`.
  - `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` — AD-10 checkpoint and 63/83 artifact count.
  - `.agents/worklog/2026-11-07/design-study-screen-ad10.md`
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Original `screen.png` and `code.html` preserved byte-for-byte. Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Goal objective, router, context map and worklog contract reviewed; exact docs selector READY 3/215; selected AD-01, AD-02 and AD-03 worklogs reviewed. | VERIFIED |
| Scope/context/registry | Project dependency/contracts/workflow pages; Web and Study-Web routers/index; Study Server entry/index/module/db-security/database/tests pages; design guide; registry confirms `createDD-markdown` excludes Web UI-only DD and Study OpenAPI contract is `NOT_FOUND`. | VERIFIED |
| AC/API/screen/source review | AD-10 assets/DOM, AC-33/index, API catalog and #78 DD/open questions, current #78 route/module/query/model/validator/tests, #49 Content model, #79 detail boundary, legacy DDL/migrations, V1-PILOT content model and Study Web source tree reviewed. | VERIFIED_SOURCE_REVIEW |
| Static artifact audit | Custom Python/stdlib audit: original SHA-256 unchanged; source 1600×1461 and annotated PNG 3200×2922; JSON/SVG valid and 39 ordered unique markers match coordinates/labels with stroke bounds inside image; DD sections A–F, 39 sequential C rows, EV-01…EV-08; every local Markdown link resolves; 83 unique inventory IDs and 83 source folders; 63/83 core artifact sets; authored AD-10 text has no trailing whitespace. Final annotated image visually reviewed. Initial optional Pillow import was unavailable, so dimensions were checked from PNG headers and image review used the available viewer. | VERIFIED |
| Tracker and whitespace | AD-10 inventory row and reverse API #078 row are `R`; stale “Content persistence absent from DDL” claim removed; global checkpoint says 63/83. `git diff --check -- apps/study-client/docs/list_screen.md apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` passed. | VERIFIED |
| Runtime/tests | No application tests, server runtime, or browser runtime were run; the task required static DD/artifact review only. | NOT_RUN |

## HANDOFF

- Remaining blockers: catalog/AC singular Content vs local Page; derived pagination/order/422 and type enum/search/course ID mapping; mockup course-title/author/submitted-time and AC version needs absent from #78/#79 projection; stale/deleted/revision policy and moderation-specific permission open; legacy BIGINT vs V1-PILOT UUID and live DB/deployment not verified; Study Web remains UNWIRED. Status `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.
- Next owner/action: AD-11 is next in the moderation flow, in a separate session.
