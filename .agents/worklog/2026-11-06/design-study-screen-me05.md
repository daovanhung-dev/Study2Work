---
task_id: "2026-11-06-design-study-screen-me05"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: ["test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-05 reads Mentor lecture/API #48 after AC-21 creation in ME-04 and links expected ME-03/ME-06; source access is direct-owner only"]
status: "VERIFIED"
---

# Worklog: Detailed Design Study ME-05 — Xem bài giảng Mentor

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selected 3 exact-type docs worklogs of 187; all selected worklogs read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Separate expected from current source; preserve source assets; UI-only DD has no canonical skill; source tests/DDL do not prove deployment or live DB.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Keep Study Web UNWIRED; preserve screenshot/HTML mismatch; map each action to source or explicit blocked/unwired state; do not infer routes or sample data.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: One Screen ID per session; distinguish API source-backed from DD/DB/runtime status; record AC-vs-inventory differences rather than reconciling by inference.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Handle ME-05 only in this session; plan first; preserve source image/HTML; create checked annotated image, marker map, source-traced DD; update `dd_screens/PLAN.md` and worklog; separate DD readiness, implementation block and runtime verification.
- Screen inventory: `/mentor/lectures/:lectureId`, Mentor actor, AC-21, GET #48, expected states `loading/ready/not-found`; links ME-03/ME-06; do not create an edit endpoint.
- AC-21 flow: create lecture → read by ID. ME-04 proposes redirect using #47 `data.id`, but Study Web route is not wired.
- UI-only DD skill registry: no canonical UI-only skill; `createDD-markdown` explicitly excludes `web-ui-only-dd`.

## CURRENT_BEHAVIOR

- Screen source: `screen.png` is 841×1600, SHA-256 `458ea549ae892b0825c48a62ec13655b8f631915070bd840c62bc8690c3f6a8f`. `code.html` is 43,487 bytes, SHA-256 `eb8861bb475621590248c0fe9913bafd891697e5c20717dcaf9041e2f0e2a3d2`; no inline event handlers, form, video element, fetch/XHR or meaningful route (14 anchors are `#`). The screenshot contains sample author/course/title/media/analytics/discussion/tree values outside the API #48 projection.
- Study Web source/runtime: current checkout has `dist/` and `docs/`, no editable `src/`, package manifest or router; serving/provenance of ignored dist is unverified. Web subcontext status is `UNWIRED`.
- API #48 current source: route is registered in `apps/study-server/app/api/v1.py`; shared MENTOR JWT guard runs before path parse/DB; invalid signed-int64 parse maps to 404; Q1 reads non-DELETED lesson and parent course, requires direct owner; Q2 returns ordered, scoped `lesson_uploads/uploads` metadata; success maps `LectureResponse` and is read-only. Errors are 401/403/404/500; malformed IDs have no catalog 422. `content` may be null, `assets` may be empty, and status is returned as stored except DELETED is filtered.
- API #47 current model sends `content:int64` into `lessons.content` as decimal string and creates PUBLISHED. API #48 therefore does not establish the screenshot's academic Markdown/code content or status menu.
- API #48 DD is `Draft — Needs Confirmation`; legacy DB/migrations are checked-in candidates and live DB state is unknown. V1-PILOT model differs.
- Test source `test_mentor_lecture_detail.py` covers auth, owner, malformed/missing IDs, nullable content, ordered/empty assets, parent/link integrity, query failure and OpenAPI. It was read, not run. Fake sessions are not runtime/DB proof.

## SOURCE_TRACE

```text
ME-04 expected #47 201 data.id
  -> proposed Study Web /mentor/lectures/:lectureId (UNWIRED)
  -> registered GET #48 route
  -> shared MENTOR guard
  -> signed-int64 parse (current malformed → 404)
  -> Q1 lessons LEFT JOIN courses; hide DELETED; direct owner check
  -> Q2 ordered lesson_uploads + scoped uploads projection
  -> 200 ApiEnvelope<Lecture> or safe 401/403/404/500
  -> no DB write; tests use fake DB and were not run
```

Current #48 response has `id`, `course_id`, `title`, nullable `content`, ordered `assets[]`, `order`, and `status`. It does not return author, media URL/player/chapter, analytics, discussion, outline or adjacent lessons. `error_response` source defaults error `data` to JSON null; API #48 DD prose has a stale contradictory statement saying `{}`.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study Web route | No editable source/router/package; static HTML anchors target `#`. | `UNWIRED` | No client navigation/runtime claim. |
| AC-21 access | AC allows owned/assigned course; #48 current source checks direct `courses.mentor_id`. | `DISCREPANCY` | Assignment contract unresolved. |
| Mockup projection | Author, media/player/chapter, analytics, discussions, tree and neighboring lessons absent from #48. | `DISCREPANCY` | Cannot present sample values as API data. |
| Content/status actions | #48 returns nullable content/status but does not edit; #47 content is decimal string and status PUBLISHED. | `DISCREPANCY` | Rendering, status transitions and editing remain blocked. |
| Resources | #48 returns asset URL metadata; object-storage access/reachability is unverified. | `IMPLEMENTATION BLOCKED` | Download/preview policy needs approval. |
| API/schema | Route/module/test source local; API DD Draft, migrations/live schema/identity/status semantics/path mapping open. | `SOURCE_BACKED / NOT RUNTIME VERIFIED` | Keep DD blocked; tests not run. |
| Error envelope docs | Current core helper `data=None` serializes to null; API DD #48 Overview says `{}`. | `DISCREPANCY` | Source wins for current behavior; API owner should correct DD/contract. |

## CHANGES

- Files changed: ME-05 `ME-05_PLAN.md`, `ME-05_markers.json`, `ME-05_markers_overlay.svg`, `screen_annotated.png`, `ME-05.md`; global `dd_screens/PLAN.md`; this worklog.
- Original `screen.png` and `code.html` are not modified.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none; mockup-only content/action is marked unresolved or blocked.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Worklog selector + review | 3 exact-type docs logs selected and read; no shortage. | VERIFIED |
| Current ME-05 image/HTML/API #48/test/DD/schema source review | Plan and DD trace source; focused test source read but not run. | VERIFIED_SOURCE_REVIEW |
| Static artifact audit | 33 ordered unique markers; JSON/SVG/DD map 1:1; 20 ordered events; all DD relative links resolve; coordinates within bounds and min center gap 23 source px; annotated PNG is 1682×3200; source image/HTML hashes unchanged; inventory recount 36/83, tracker matches; no trailing whitespace. | VERIFIED (12/12 checks) |
| Visual inspection | Opened annotated PNG at full page; verified marker placement/readability around header, action bar, player, panels, resource actions, course rows and footer. | VERIFIED |
| `git diff --check` | No whitespace errors. | VERIFIED |
| Tests/browser/runtime | Not run by task instruction. | NOT_RUN |
| Context validator | No context page/manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Study Web wiring; assigned-course identity/access; content serialization/null fallback; status/edit APIs; media/chapter/preview; asset URL access; analytics/discussions; course tree/neighbor source; API #48 DD and live schema confirmation.
- Next owner/action: ME-06 in a separate session. ME-05 must remain `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` until blockers are resolved.
