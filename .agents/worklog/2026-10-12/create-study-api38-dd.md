---
task_id: "2026-10-12-create-study-api38-dd"
date: "2026-10-12"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo Study API #38 DD draft

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-12/commit-push-study-dds.md`
    - carry_forward: API DD là design-only; không suy ra runtime từ DD hoặc đẩy các thay đổi cục bộ chưa được xác thực.
  - path: `.agents/worklog/2026-10-12/create-study-api27-dd.md`
    - carry_forward: Giữ trạng thái Draft + open questions, không tự đặt schema, tiêu chí nghiệp vụ hoặc quyền truy cập; Study không tạo ZIP.
  - path: `.agents/worklog/2026-10-12/create-study-api28-dd.md`
    - carry_forward: Giữ nguyên approved catalog contract, phân loại `SOURCE_REQUIRED`/`DISCREPANCY`/`UNWIRED`, và không thêm error code ngoài catalog.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown draft cho API #38 `GET /api/v1/users/me/achievements` theo AC-18, gồm tám sheet template, ba report và worklog; không thay đổi runtime, API catalog, diagrams, DB schema hay các DD #27–#37; không tạo ZIP.
- Canonical contract/approved DD: `docs/lists/list_api.md` là `APPROVED_DESIGN_CONTRACT`. API #38 dùng Student Bearer JWT, query `course_id?:int64`, `ApiEnvelope<Page<Achievement>>`, HTTP/business codes 200/401/403/500. `Achievement` gồm `id`, `code`, `title`, `awarded_at`, `course_id?`.

## CURRENT_BEHAVIOR

- Source/config: AC-18 mô tả đọc achievements đã mở khóa; DB guide nói achievements được tính từ dữ liệu hiện có nhưng không chỉ định tiêu chí hoặc projection. ERD V1 và checked-in `DB.sql` không có achievement table; live schema chưa được xác minh. Current `app/api/v1.py` không đăng ký route API #38, và source scan không tìm thấy achievement runtime module.
- Runnable tests: Không tìm thấy API #38 test; runtime tests chưa chạy vì phạm vi docs-only.
- Runtime wiring: API #38 hiện `UNWIRED / NOT_FOUND`; không ghi nhận là runtime-verified.

## SOURCE_TRACE

```text
Student -> GET /api/v1/users/me/achievements (approved design contract)
-> AC-18: đọc achievement unlocked sau progress flow
-> DB design: achievements computed from existing data; exact criteria/projection absent
-> current Study router/module/test inventory: API #38 absent
-> documentation-only DD draft with unresolved behavior kept open
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Achievement source | DB guide says computed from existing data; no award criteria/projection or achievement table in ERD/DDL. | `SOURCE_REQUIRED / DESIGN_ONLY` | Do not invent SQL, award rules or persistence. |
| Pagination contract | Response is `Page<Achievement>` with `PageMeta`; request row only declares `course_id`. | `DISCREPANCY / SOURCE_REQUIRED` | Preserve catalog; do not invent page/size/sort inputs or defaults. |
| Course filter semantics | `course_id?` exists on request and optional Achievement schema; treatment of course-less awards and access is unspecified. | `SOURCE_REQUIRED` | Record in open questions; do not choose inclusion policy. |
| Runtime API #38 | Current router/modules/tests have no achievements endpoint. | `UNWIRED / NOT_FOUND` | DD documents design only. |

## CHANGES

- Files changed: This worklog; `apps/study-server/docs/dd/38_users_me_achievements/` with eight sheets and three reports.
- CONTEXT_UPDATES: None.
- Context pages changed: None; no runtime or canonical source contract changes.
- Assumptions: Preserve API #38 catalog contract and use `Draft — Needs Confirmation`; classify possible progress/quiz/assignment inputs as candidates only; no ZIP per Study Server workflow.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | Selected and read the three docs worklogs listed above; no shortage. | VERIFIED |
| Current source/catalog/diagram preflight | Confirmed API #38 contract, AC-18 flow, DB design note and absence of runtime route/table evidence. | VERIFIED |
| DD static validation | 8 sheets in canonical order; front matter, Markdown table widths, JSON examples, local links, exact catalog contract/error set, read-only mapping, whitespace and conflict-marker checks passed. Output hashes and template fingerprints are in `VERIFICATION_REPORT.md`. | VERIFIED |
| Runtime route/module/test scan | No achievements/API #38 matches in Study Server app or tests. | VERIFIED — UNWIRED / NOT_FOUND |
| Documentation whitespace/diff check | No trailing whitespace or conflict markers; `git diff --check` found no whitespace errors in the new DD files. | VERIFIED |
| Runtime tests | Not run; docs-only task and API #38 is not wired. | NOT_RUN |

## HANDOFF

- Remaining blockers: Award criteria, exact source/projection, filter/access semantics, pagination/sort controls and empty-result behavior remain open for DD approval or implementation.
- Next owner/action: Review `OPEN_QUESTIONS.md` and update the canonical design contract before marking the DD Ready/Final or implementing API #38.
