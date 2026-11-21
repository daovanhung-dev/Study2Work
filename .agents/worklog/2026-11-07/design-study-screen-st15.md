---
task_id: "2026-11-07-design-study-screen-st15"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-14 → ST-15; Study API #30/#31 / AC-16; downstream ST-16 #32"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-15

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 242; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Preserve expected/current separation; trace source and API catalog separately; do not infer UI/runtime from static prototype; use exact blockers and separate DD/implementation/runtime statuses.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Current source may differ from Draft API DD; retain unsolved policy and live-schema gaps; no tests/runtime claim without execution.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Keep source-backed locally separate from owner-approved contract; preserve open lifecycle, authorization and PII rules; Study Web remains `UNWIRED` without editable routes.
- additional_dependency_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-st14.md`
    - carry_forward: AC-16 order is #28 → eligibility → #29 → #30 → #31 → #32; ST-13/ST-14 ownership of #29 remains unresolved, and ST-14 cannot restore attempt/answers. API #30 answer representation/upsert/access/retry and live schema are open; keep #31 ownership/state/submit ambiguity unresolved until current sources are checked.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-15 only in this session; read the goal objective; re-audit source/assets/contracts; record a screen plan before DD/tracker edits; preserve original assets; maintain ordered one-to-one markers and A–F DD; describe each event's input/process/output and API/error handling; update inventory/F05 or linked-flow notes as needed, global plan and worklog; keep DD, implementation and runtime statuses separate.
- Canonical contract/approved DD: AC-16 and catalog/API DD #30/#31, with ST-15 inventory route, pending-save flush, one #31 submit, and downstream ST-16 #32 handoff, subject to source/contract re-verification.

## CURRENT_BEHAVIOR

- `apps/study-client/` có tài liệu/assets và ignored `dist`, không có editable Student app/router hoặc `package.json`; `.agents/web-work/study/INDEX.md` giữ status `UNWIRED`. Không coi dist hoặc screen inventory là route/runtime proof.
- `apps/study-server/app/api/v1.py`, `.agents/server-study/apis/declared-routes.md`, `apps/study-server/app/modules/student/` và `apps/study-server/tests/modules/student/` không có API #30–#32; Student source/module/test hiện tìm thấy là API #34 uploads. Đây là source absence, không xác nhận tình trạng deployment/live service.
- Catalog #30–#32 và API #30/#31 DD là design evidence; #31 DD là Draft — Needs Confirmation, Q-31-01…06 còn mở. AC-16 XML `AC16` xác nhận GET #28 → eligibility → POST #29 → answer/#30 → submit/#31 → result/#32, cùng `SUBMITTED` và nhánh `PENDING_GRADE`/`GRADED`.
- `DB.sql` legacy dùng BIGSERIAL/BIGINT `quiz_attempts`/`quiz_answers`; V1-PILOT `02_study_db.sql` dùng UUID `assessment_attempts`, submitted snapshot và immutable answers, với state branch khác AC-16. Không có mapping được duyệt và không xác minh live schema.
- PNG là confirmation mockup; HTML là unavailable fallback, DOM không có `btn-submit-exam`, script có hash route hardcode, không có API request. Timer/count/sync/attempt/grading text là sample-only. Hai asset biểu diễn trạng thái khác nhau.

## SOURCE_TRACE

```text
```text
Requirement/flow: apps/study-client/docs/list_screen.md (ST-15 row, F05, G-09)
AC/API contract: docs/lists/list_api.md (#30–#32); apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio (diagram id=AC16); apps/study-server/docs/dd/30_attempts_answers/OPEN_QUESTIONS.md; apps/study-server/docs/dd/31_attempts_submit/{02_Overview,03_Request,04_Response,05_Data_Mapping,06_Error,OPEN_QUESTIONS}.md
Current route/source: apps/study-server/app/api/v1.py; .agents/server-study/apis/declared-routes.md; apps/study-server/app/modules/student/; apps/study-server/tests/modules/student/
Schema candidates: infra/postgres/study-server/DB.sql; infra/postgres/02_study_db.sql; apps/study-server/docs/diagrams/DB_UNICA_TABLES.md
Web/status/design: .agents/web-work/study/INDEX.md; .agents/web-study/design.md; apps/study-client/dist/
Screen assets/handoff: ST-15/{screen.png,screen_annotated.png,code.html,ST-15_markers.json,ST-15_markers_overlay.svg,ST-15_PLAN.md,ST-15.md}; ../ST-14_lam-bai-kiem-tra/ST-14.md
```
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| #30/#31/AC-16 contract and lifecycle | Catalog/AC diagram/API DD open questions; plan re-audit section 8 | `DESIGN_ONLY / BLOCKER` | Flush ordering/outcome and submit ownership/state/repeat/expiry/grading/transaction/response unresolved; do not invent or retry. |
| Route and app source | Router/route-index/student module-test scan; Study Web status index | `NOT_FOUND / UNWIRED` | No implementation or runtime claims for #30–#32 or ST-15. |
| Candidate schema mismatch | Legacy DB.sql vs V1-PILOT `02_study_db.sql` | `DISCREPANCY / NOT_VERIFIED` | Distinct IDs, answer shapes, immutability and lifecycle; live schema not inspected. |
| PNG vs HTML and sample copy | Visual review, DOM/script static search | `DISCREPANCY / DESIGN_ONLY` | Keep mock data separate from contract; HTML fallback is not a submit path. |
| Element event references | ST15-EL-17/18 table vs EV-01…07 | `FIXED` | Continue now references EV-02; Submit references EV-03. |

## CHANGES

- Files changed:
  - `apps/study-client/docs/screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15_PLAN.md` — added dated re-audit and pre-DD/tracker edit plan.
  - `apps/study-client/docs/screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15.md` — fixed element/event map; documented BIGINT vs UUID schema/lifecycle discrepancy; completed static audit checklist and source link.
  - `apps/study-client/docs/list_screen.md` — expanded ST-15 gate/status and F05 flush/submit conditions.
  - `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` — updated ST-15 tracker row and appended the final checkpoint.
  - `.agents/worklog/2026-11-07/design-study-screen-st15.md` — current session record.
- CONTEXT_UPDATES: none; no context contract/convention page changed.
- Context pages changed: none.
- Assumptions: none; unresolved decisions remain labeled as blockers.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`; read AD-01, AD-02, AD-03 above. | VERIFIED |
| Static assets/marker/link audit (Python stdlib; no app runtime) | 18 sequential/in-bounds markers, 18 DD rows, 18 SVG groups; IDs, labels and JSON/SVG coordinates match; annotated PNG is 2×; all 23 DD and 20 plan links resolve. | VERIFIED |
| `file` + `sha256sum` on source assets | PNG 1600×1280, annotated PNG 3200×2560; source hashes match plan baseline. | VERIFIED |
| HTML static scan | No fetch/XHR/axios; `btn-submit-exam` absent; script contains hardcoded sample hash route; PNG/HTML remain discrepant. | VERIFIED |
| `git diff --check` scoped to tracked inventory/tracker edits | Clean; new ST-15 DD/plan/worklog whitespace scan is also clean. | VERIFIED |
| Full-file whitespace scan on `list_screen.md` | Found four trailing-space lines (3–6) that are identical to `HEAD`; not part of this task's edits. | PREEXISTING |
| `node scripts/validate-agent-context.mjs` | Exit 1, `AGENT_CONTEXT_INVALID`: declared db-admin context/source roots/pages are reported missing and contexts are stale for server-study/server-work/web-work/mobile-work/db-admin. Filtered output has no ST-15, worklog, inventory or global plan references. | FAILED — REPO BASELINE |

## HANDOFF

- Remaining blockers: #30 flush schema/ordering/idempotency/outcome; #31 ownership/state/repeat/deadline/concurrency/grading/transaction/response; ST-14 dirty-state/summary/direct-entry handoff; legacy BIGINT vs V1-PILOT UUID mapping and active schema; Study Web wiring and Student #30–#32 implementation; mockup copy/timers/counts/policy; accessibility/error/close decisions.
- Result: ST-15 artifacts and trackers updated. `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. No app tests, browser runtime or live DB verification run.
- Next owner/action: ST-16 in a separate session, after ST-15 is complete.
