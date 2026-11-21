---
task_id: "2026-11-07-design-study-screen-ad13"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-34; AD-12 → AD-13; API #83; AD-14/#84–#86 handoff"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-13

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 218; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Separate expected/current behavior; preserve assets; trace permission/query/response/test source; keep Study Web UNWIRED and do not claim runtime or tests.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Preserve Admin permission and data/privacy blockers; do not invent field/filter/action semantics; fake DB and catalog are distinct evidence.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Keep numeric ID handoff explicit; do not infer detail fields/actions from mockup; source-backed local API does not prove live schema or Study Web wiring.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-13 only in this session; plan before markers/annotation/DD, preserve original assets, author A–F DD with traceable API #83 and AD-12/#82 handoff, update inventory/API reverse index/global plan and worklog; stop before AD-14.
- Inventory row 71: AD-13 `/admin/lessons/:lessonId`, AC-34, API #83; inspect lesson content/status/linked progress according to contract; GET #83; links AD-14; expected loading/ready/404/error; P1.
- AC-34 sequence: AD-12/#82 list → select lesson → AD-13/#83 detail → AD-14/#84 update, #85 status or #86 delete → reload list. Use numeric lesson ID only if supported by current response/route; no extra route/query assumptions.

## CURRENT_BEHAVIOR

- AD-13 folder currently has only source `screen.png` (1600×1595, SHA-256 `3e91e4b99567c2a8bfdcedd534d1e2c0b88360010fe742ede20fd91802bfa0dd`) and `code.html` (SHA-256 `a638941b112888e0b241c487b632197a8c689cbd6ff4100554749e8e5298ead5`). Prototype shows a selected-lesson empty state, six metadata cards, resource summary cards, disabled AD-14 action, audit/concurrency claims, learner metrics, SSE disconnected and a standards notice.
- `code.html` is static: links use `href="#"`; the only button is disabled; no route-param binding, data binding, fetch/XHR, API URL, SSE/EventSource, WebSocket, timer or listener. Study Web current root contains only `dist/`, `docs/`, `node_modules/`, and `tsconfig.tsbuildinfo`; no editable source/package/router/client. Status `UNWIRED`; runtime not verified.
- API #83 route is composed at `GET /api/v1/admin/lessons/{lesson_id}`, response model `GetAdminLessonEnvelope`, path int64 metadata and catalog errors 401/403/404/500. Shared Bearer/JWT role `ADMIN` guard runs before custom raw-path parse and DB. Parse accepts signed int64 text (including sign/leading zero); invalid/overflow/overlength path maps locally to 404 (DERIVED) without query.
- #83 SQL reads one `lessons` row by bound ID and excludes `status IS DISTINCT FROM 'DELETED'`; no public `PUBLISHED` filter, join, dependency/progress query or mutation. Maps reusable #09 `Lesson`: `id`, `course_id`, `name→title`, nullable `content`, nullable `video_url`, `sort_order→order`, `status`; direct `data` object in the envelope. Missing/deleted row→404 + rollback. Query error, invalid row identity, or required projection failure→safe 500 + rollback; success does not commit. It returns `meta:{}` and trace ID via response helper.
- Focused API #83 test source covers direct Lesson response and optional nulls, auth-before-path/query, invalid int64→404, missing row→404, query failure safe 500/rollback, invalid required/null/mismatched projection→500/rollback, no mutation, and OpenAPI contract. Tests were read, not run in this session; the API DD’s historical report lists 15 focused passes and fake sessions do not verify live PostgreSQL/deployment.
- API #83 DD is `Draft — Needs Confirmation`. AC-34 says “lesson + dependencies” but #83 response has no dependency fields. Current API #86 source rechecks progress, resources, and lesson_uploads at delete time, returning 422 when any exist; it does not prove #83 should expose counts, and current source does not check quiz/discussion dependencies. API #86 mutation-time checks cannot be replaced by stale detail-time counts.
- Legacy `infra/postgres/study-server/DB.sql` uses BIGINT lessons with nullable `course_id`, `sort_order`, `status`, and nullable content/video URL; reusable Lesson requires course_id/order/status. V1-PILOT `infra/postgres/02_study_db.sql` uses UUID lesson IDs and different chapter/course-version fields. Neither checked-in artifact proves live schema/deployment.
- The mockup’s lesson type, course title, student count, completion/submission/rating metrics, resources/quizzes/discussion counts, SSE, audit level, concurrent-write guarantee, sync status, media extraction and “Admin isolation” are absent from #83. Raw `video_url` alone does not define a secure player or media authorization contract.

## SOURCE_TRACE

```text
Expected: AD-12 Lesson.id → AD-13 numeric lessonId → GET #83 → one ApiEnvelope<Lesson> → AD-14/#84/#85/#86 action branch → reload AD-12/#82.
Current: no Study Web caller → #83 shared ADMIN guard → custom signed-int64 parser (invalid -> local 404) → bound lookup in legacy lessons candidate excluding DELETED → direct Lesson data/200, missing 404, safe 500+rollback on query/projection failure. #83 is read-only and does not load resources/progress; #86 rechecks progress/resources/lesson_uploads when delete runs.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Dependencies/linked progress | Inventory and AC-34 n5 mention dependencies; #83 returns only Lesson and has no progress/resource query; #86 separately checks progress/resources/uploads at mutation time. | `DISCREPANCY / BLOCKER` | Do not display counts or let detail-time state decide delete eligibility. |
| Metadata | Mockup has course title, content type and lesson code; #83 has numeric `course_id`, `id`, title/order/status, nullable content/video_url only. | `DISCREPANCY` | No inferred course title/type/slug; raw video URL does not define preview. |
| Metrics/SSE/audit/lock/sync | Mockup provides learner/completion/submission/rating values, Realtime SSE, Audit Log Level 1, auto lock and sync status; #83 is read-only and returns none of these. | `STATIC_ONLY / UNMAPPED` | No fabricated metric, realtime, concurrency or audit assurance. |
| Authorization and live schema | AC-34 requires lesson-management permission; current guard checks only `ADMIN`. Legacy and V1-PILOT schema differ; legacy required-response columns may be null. | `OPEN / BLOCKER` | Permission policy and deployed schema/nullability need confirmation. |
| Soft-delete and status | #83 excludes `DELETED`; status string enum/casing unresolved; #86 current local source writes `DELETED`. | `SOURCE-BACKED LOCALLY / DERIVED` | Keep exact raw status and visibility policy open; API DD remains Draft. |
| Study Web wiring/design | Prototype has no API/client handlers; Study Web source/package/router absent. Mockup palette/font/full-width differs from Study design guide. | `UNWIRED / DESIGN DISCREPANCY` | No runtime claim; implementation must follow Study design target when wired. |

## CHANGES

- Lập `AD-13_PLAN.md` trước khi tạo marker map, ảnh annotation và DD; hoàn tất checklist 1–8, chỉ xử lý AD-13 trong phiên này.
- Giữ nguyên `screen.png` và `code.html`; tạo `AD-13_markers.json`, `AD-13_markers.svg` với 61 marker và `screen_annotated.png` 3200×3190 (render 2× từ 1600×1595).
- Tạo `AD-13.md` theo mục A–F, gồm 61 element rows, EV-01…EV-08, field/error/navigation mapping, evidence links và blocker/discrepancy rõ ràng.
- Cập nhật inventory row 71 và reverse API row 083 từ D→R theo local source review; thêm checkpoint AD-13 vào global DD plan. API #83 DD vẫn Draft; AD-14 không đổi.
- CONTEXT_UPDATES: none. Context pages changed: none. Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective reread; docs selector READY 3/218; AD-01/02/03 worklogs fully reviewed. | VERIFIED |
| Scope context/registry | Cross-scope, Study Web, Study Server contexts loaded; registry confirms no canonical UI-only screen-DD skill is wired. | VERIFIED |
| Source preservation and image dimensions | `screen.png` SHA-256 `3e91e4b99567c2a8bfdcedd534d1e2c0b88360010fe742ede20fd91802bfa0dd`; `code.html` SHA-256 `a638941b112888e0b241c487b632197a8c689cbd6ff4100554749e8e5298ead5`; dimensions 1600×1595 and 3200×3190. | VERIFIED |
| Marker and DD mapping | JSON/SVG valid; 61 ordered markers, labels/coordinates agree, stroke bounds are inside source dimensions, and DD section C has rows 1–61 exactly. | VERIFIED |
| Links and inventory | All 17 relative Markdown links resolve; list_screen.md has 83 unique Screen IDs matching 83 screen folders; core artifact sets are 66/83. | VERIFIED |
| Visual and whitespace review | Annotated image reviewed directly after moving markers 12–14 into the whitespace above the breadcrumb/content; no trailing whitespace in AD-13 artifacts/worklog. | VERIFIED |
| Tracker whitespace | `git diff --check -- apps/study-client/docs/list_screen.md apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` passed. | VERIFIED |
| Application tests/runtime | Not run; Study Web is UNWIRED and runtime remains unverified. | NOT_RUN |

## FINAL_STATUS

- AD-13: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Open blockers: AC-34 dependency output; missing course/type/resource/progress/metrics/SSE/audit/concurrency/media contracts; ADMIN vs lesson-management authorization; legacy vs V1-PILOT/live schema and nullable required projections; status/soft-delete policy; Study Web source/wiring.
- AD-13 deliverables and static audit are complete. No application tests or runtime verification were performed.

## HANDOFF

- Remaining work in AD-13: none. Its static documentation audit is complete; blockers remain explicit in the DD and trackers.
- Next screen for a separate session: AD-14. Do not continue it in this session.
