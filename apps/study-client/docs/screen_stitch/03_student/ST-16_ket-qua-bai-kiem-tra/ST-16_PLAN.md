# ST-16_PLAN — Kết quả bài kiểm tra

> **Trạng thái:** PLAN COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED

## 1. Phạm vi và phân loại

- Phiên này chỉ xử lý **ST-16 — Kết quả bài kiểm tra**; không bắt đầu ST-17.
- `primary_task_type: docs`; `secondary_task_types: []`; `project_scopes: [web-work, server-study]`.
- Cross-scope dependencies: ST-15 #31 submit → ST-16 #32 read result; AC-16 grading branches; API #32 draft; G-09; related ST-09/ST-20.
- Inventory route `/student/attempts/:attemptId/result`, actor Student, AC-16, API #32, related ST-09/ST-20, states `pending/graded/unavailable/error`. Success screen must not treat pending grading as score zero or expose answers outside policy.
- API #32 catalog: `GET /api/v1/attempts/{attempt_id}/result`, Student Bearer, required `attempt_id:int64` path only, no query/body; `ApiEnvelope<QuizAttempt>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401/403/404/500 catalog errors. API #32 DD is `Draft — Needs Confirmation`; source search finds no current Student route/module/test.
- AC-16 says both AUTO GRADED and PENDING GRADE branches reach #32, then read score + feedback/status. Response field policy, answer disclosure and feedback source remain open.
- UI-only DD has no registered canonical skill: `.agents/context-manifest.json` excludes `web-ui-only-dd` from `createDD-markdown`.

## 2. Asset baseline and current visual state

- `screen.png`: 846×1600 RGB; SHA-256 `aa6a8e5326eab69ea6d224b45be4c7d3b880ecf0e55c9ac20647bd0baa15fcb7`.
- `code.html`: 10,503 bytes; SHA-256 `ba551f83e6419b915d62d193a7ec15aade4ecd2cfe493b996514a1ccd7682237`.
- PNG is a loaded-result mockup: pass badge, quiz title, duration/submission time/attempt ordinal, next-lesson unlock claim, score ring and GPA, skill breakdown, answer-review controls/cards, answer key/mentor feedback/video links, next-module suggestion, PDF and continue actions.
- HTML is a different Guest unavailable state with login/register header and a “Quay lại khóa học” link. It has no route data/API call; script selectors `.review-tab-btn` and `.question-card` do not match any elements in the document.
- Values and claims shown in PNG (90%, 18/20, 9/10, GPA A+, attempt 2/3, 80% unlock rule, skill scores, answer key, feedback, PDF and next module) are design samples unless an approved source supplies them.
- Preserve both original files. Do not derive result state from HTML copy, screenshot values or the prior ST-15 sample.

## 3. Contract expectations, source limits and blockers

- API #32 logical response is `ApiEnvelope<QuizAttempt>`; reusable `QuizAttempt` has `id`, `quiz_id`, `status`, `started_at`, optional `submitted_at`, optional `score`, `answers[]`. `QuizAnswer` may have `question_id`, optional `choice_ids`, `text_answer`, `correct`, `score`.
- #32 DD proposes candidate `quiz_attempts`/`quiz_answers` reads, but it is `Draft — Needs Confirmation`. No runtime SQL or mapping is verified. Questions Q-32-01…06 cover owner/masked 403 vs 404; read eligibility and pending score; correctness/score disclosure; AC feedback source; answer shape/order; path validation/error mapping.
- AC-16 only names `GRADED` and `PENDING_GRADE` result branches. For pending, score may be omitted/null/partial; all nonterminal status behavior remains open. Do not equate `GRADED` alone with passing.
- The logical response contains no quiz title, passing threshold/pass result, GPA/grade label, skill taxonomy/progress, question text/options, teacher feedback, next-lesson/module, or PDF reference. The screenshot cannot be hydrated from #32 alone. Do not invent API #28/#27/#37 calls or compute unlocks in this screen without an approved flow.
- Checked-in DDL is a design artifact: `quiz_attempts.score` and `submitted_at` nullable; `status` lacks a canonical enum; `quiz_answers.is_correct` is NOT NULL and `score_received` defaults to 0; there is no feedback or text-answer column. It is not live-schema evidence.
- Current Study Web is `UNWIRED`; current Study Server has no Student #32 route/module/test. Admin quiz APIs #87–#91 are separate.

## 4. Kế hoạch element/marker

Create sequential markers `#1–#38`, each mapped exactly once to `ST16-EL-01`…`ST16-EL-38` in the DD element table. Group related subcontrols only when one marker identifies the shared control/card and the DD row names every subpart. Use small numbered badges in the left/right page gutters where possible; keep original content legible and preserve the 846×1600 source aspect inside a centered, padded annotation canvas.

In the JSON map, `x/y` identify the target element in source-image coordinates and `badge_x/badge_y` identify the numbered badge center on the padded canvas; each gutter connector aligns to `y` without crossing the content.

1. Header brand/logo. 2. Search field. 3. Main navigation links. 4. Notification control. 5. Student profile control.
6. Breadcrumb trail. 7. Pass/status badge. 8. Skill/category eyebrow. 9. Quiz result title. 10. Duration, submission timestamp and attempt ordinal group.
11. Next-lesson-unlocked claim card. 12. Score summary gauge and answered denominator. 13. Points score. 14. GPA/grade label.
15. Skill analysis heading. 16. Framework/data-standardization badge. 17–19. Three individual skill cards and their level, description, correct count and bar.
20. Answer-review section heading. 21. All-questions filter. 22. Correct-answers filter. 23. Needs-review filter.
24. Question 14 card header/status/topic/difficulty. 25. Question 14 prompt. 26. Question 14 choices and selected/correct indication. 27. Question 14 instructor explanation.
28. Question 19 card header/status/topic. 29. Question 19 prompt. 30. Question 19 selected incorrect answer. 31. Correct answer and explanation. 32. Question 19 instructor feedback/video reference.
33. Next-module recommendation panel. 34. Download PDF action. 35. Review-course-outline action. 36. Continue-to-next-lesson action. 37. Footer brand/certification group. 38. Footer navigation/legal links.

The question-review controls and two question cards remain distinct; card details are subparts of their containing review element. Numeric sequence in the final map must match the DD table exactly.

## 5. Sự kiện và luồng cần đặc tả

1. **ST16-EV-01 — Open result route:** accept `attemptId` from path, require Student context, call only GET #32 per inventory. Do not use unapproved direct-entry or attempt-owner semantics.
2. **ST16-EV-02 — Map successful result:** parse `ApiEnvelope<QuizAttempt>` only under approved response schema; distinguish `PENDING_GRADE` from `GRADED`; keep score/correctness/feedback hidden or absent until field disclosure policy is resolved. No grade/pass/skill calculation is licensed by current source.
3. **ST16-EV-03 — Review-answer filters:** screenshot suggests local all/correct/unreviewed filtering, but answer correctness, question content/order and filter counts are not resolved by #32. Treat as design-only; do not activate until response projection and disclosure contract are approved.
4. **ST16-EV-04 — Continue/review/PDF/module actions:** destinations, export generation, learning progression and eligibility are not in ST-16 inventory or #32. Document visible controls; do not assign API, route, progress write or file behavior without source.
5. **ST16-EV-05 — API/auth/error handling:** preserve #32 catalog set 401/403/404/500; 403-vs-404 ownership and path parse behavior remain open; do not add 400/422/409. No retry/reconciliation policy is defined.
6. **ST16-EV-06 — Rendering and accessibility:** only show data present in an approved response; handle pending/error/empty without false score; apply Study Web design target for semantic controls, visible focus, keyboard and reduced motion, but do not claim current runtime behavior.

## 6. Trạng thái, blocker và đầu ra

- State flow: `loading → pending` or `graded`; other states `unavailable`, `error`, `access_denied`, `not_found`, `unsupported_status`. `graded` is not synonymous with passing. `PENDING_GRADE` must not display score zero. Response field policy is blocked.
- Build `ST-16_markers.json`, `ST-16_markers_overlay.svg`, `screen_annotated.png` and `ST-16.md` with sections A–F, 38 element mappings, Event IDs and API/error/state/navigation/accessibility detail.
- Record blockers: API #32 route/module/test absent; ownership/availability/state/error validation unresolved; answer/score/feedback disclosure and response projection unresolved; screenshot loaded state and HTML unavailable state conflict; result card fields/actions lack data/route contracts; candidate DB is not live evidence.
- Static audit only: verify source hashes/dimensions; annotation aspect/legibility; marker order/bounds/one-to-one DD mapping; SVG parse/count; local links; 83-ID/folder count and complete artifact count; tracker row/progress/next pointer; `git diff --check`. Do not run tests or claim runtime.

## 7. Nguồn truy vết

- [Screen inventory, F05 and G-09](../../../list_screen.md)
- [PNG source](./screen.png), [HTML companion](./code.html)
- [ST-15 submit handoff](../ST-15_xac-nhan-nop-bai-kiem-tra/ST-15.md)
- [API catalog #32 and QuizAttempt/QuizAnswer](../../../../../../docs/lists/list_api.md)
- API #32 DD: [overview](../../../../../../apps/study-server/docs/dd/32_attempts_result/02_Overview.md), [request](../../../../../../apps/study-server/docs/dd/32_attempts_result/03_Request.md), [response](../../../../../../apps/study-server/docs/dd/32_attempts_result/04_Response.md), [mapping](../../../../../../apps/study-server/docs/dd/32_attempts_result/05_Data_Mapping.md), [errors](../../../../../../apps/study-server/docs/dd/32_attempts_result/06_Error.md), [open questions](../../../../../../apps/study-server/docs/dd/32_attempts_result/OPEN_QUESTIONS.md)
- [API #31 grading/submit open questions](../../../../../../apps/study-server/docs/dd/31_attempts_submit/OPEN_QUESTIONS.md)
- [AC-16 index](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-16 activity diagram](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio)
- [Candidate table design](../../../../../../apps/study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy candidate DDL](../../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT candidate schema](../../../../../../infra/postgres/02_study_db.sql)
- [Current route inventory](../../../../../../.agents/server-study/apis/declared-routes.md), [Study Web status](../../../../../../.agents/web-work/study/INDEX.md), [Study Web design target](../../../../../../.agents/web-study/design.md)

## 8. Re-audit trước khi cập nhật DD/tracker (2026-11-07)

- Rechecked inventory, AC-16, API catalog #32 and API #32 DD questions Q-32-01…06. The catalog still specifies only `GET /api/v1/attempts/{attempt_id}/result` with Student Bearer, required int64 `attempt_id`, `ApiEnvelope<QuizAttempt>`, and 200/401/403/404/500. The draft still leaves ownership/masked 403-vs-404, pending score/availability, answer and correctness disclosure, feedback source, answer shape/order, and path/error mapping unresolved.
- Source search still finds no Student #32 route/module/test in Study Server; Study Web has no source app/package manifest and remains `UNWIRED`. The ignored distribution checked for this audit contains no ST route or #32 path evidence. Runtime and live database were not inspected.
- Keep database candidates separate: legacy Study Server DDL uses BIGINT attempt/answer IDs, nullable score/submission time, and one selected `choice_id`; V1-PILOT instead has UUID assessment attempts and snapshot/answer storage. Neither candidate proves the live schema or an approved #32 adapter. This is an explicit model discrepancy for the DD and tracker.
- The existing screenshot is a populated result mockup while `code.html` is a Guest/unavailable state. The companion HTML loads Google Plus Jakarta Sans and Material Symbols plus Tailwind from CDNs and styles a different blue/green palette; this conflicts with `.agents/web-study/design.md`'s Inter/system stack, ocean tokens, restrained surfaces, and responsive target. Preserve both assets and treat the visual source/design-system mismatch as a blocker; do not infer current implementation from either artifact.
- Pre-edit static artifact audit: source PNG 846×1600, SHA-256 `aa6a8e5326eab69ea6d224b45be4c7d3b880ecf0e55c9ac20647bd0baa15fcb7`; HTML 10,503 bytes, SHA-256 `ba551f83e6419b915d62d193a7ec15aade4ecd2cfe493b996514a1ccd7682237`. Annotation assets contain sequential markers #1–#38; DD has 38 corresponding rows; all recorded target coordinates are in bounds and unique; the initial DD/plan link counts were 23/19. The image assets remain unchanged.
- Inventory audit found 83 Screen IDs and 83 screen folders (excluding `90_reference/study2work-lms-design-system`, which is not a screen); 82 folders currently have all six core artifacts, with ST-01 the only incomplete folder. ST-16 has all six.
- Planned edits in this session: clarify the two schema candidates and visual-system discrepancy in ST-16 DD; make the static checklist and source links precise; update only ST-16 in `list_screen.md` and the global tracker, adding F05 result/disclosure status only where supported; complete this ST-16 worklog. No other Screen ID, API DD, or DDL will be edited. Do not run application tests, the app, or live DB queries.
- Post-edit static verification: `screen_annotated.png` is 2016×3200; 38 marker badges in the SVG match JSON order and badge centers, target coordinates are unique/in bounds, and all 38 DD element rows map to `ST16-EL-01`…`38`. Final local links: DD 26 and plan 20, all resolve. Inventory has 83 unique IDs/83 screen folders and 82 complete six-artifact bundles (ST-01 incomplete; ST-16 complete). Scoped `git diff --check` passed. `node scripts/validate-agent-context.mjs` remains `AGENT_CONTEXT_INVALID` with missing db-admin context/source roots and repository-wide stale scope manifests (server-study/server-work/web-work/mobile-work/db-admin), matching the pre-existing validator baseline; no application tests/runtime or live DB check was run.
