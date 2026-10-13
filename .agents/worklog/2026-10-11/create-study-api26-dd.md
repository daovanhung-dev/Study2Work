---
task_id: "2026-10-11-create-study-api26-dd"
date: "2026-10-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD cho Study API #26

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/node-v24.21.0-linux-x64/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `available: 39; selected: 3; status: READY`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-11/create-study-api16-dd.md`
    - carry_forward: Tách expected/current behavior; không biến contract thiết kế thành runtime; không tạo mapping schema khi không có nguồn.
  - path: `.agents/worklog/2026-10-11/create-study-api17-dd.md`
    - carry_forward: Giữ source gaps và discrepancy ở Draft; không tự chọn semantics API, DB hoặc response.
  - path: `.agents/worklog/2026-10-11/create-study-api18-dd.md`
    - carry_forward: Study API DD là Markdown-only; giữ UNWIRED/NOT_FOUND và tách schema/contract khỏi runtime.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo Draft API DD #26 `GET /api/v1/lessons/{lesson_id}/resources`, gồm 8 template sheets, `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, `VERIFICATION_REPORT.md`; không tạo ZIP.
- Canonical contract: `docs/lists/list_api.md` quy định Student Bearer JWT, `path{lesson_id:int64!}`, `ApiEnvelope<Lesson>` và HTTP/business codes 200/401/403/404/500.
- AC-15 flow: Student có quyền xem lesson; hậu điều kiện hiển thị nội dung, tài nguyên và điều hướng bài kế tiếp; API diagram ghi bước đọc lesson resources.
- Scope: Chỉ tạo DD Markdown và worklog; không sửa runtime, catalog, diagram, DDL hoặc context page.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py` không đăng ký API #26; module/test inventory không có handler hoặc focused test cho endpoint. API #12 có route đọc resource theo `resource_id`, nhưng không thực hiện endpoint #26.
- Schema evidence: ERD/checked-in DDL mô tả `resources` và `resources.lesson_id`; đây là design evidence, không xác nhận live schema. DDL không đặt `lesson_id NOT NULL`, trong khi ERD ghi FK bắt buộc.
- Runtime wiring: API #26 `UNWIRED / NOT_FOUND`; giữ riêng endpoint API #12 đã tồn tại.

## SOURCE_TRACE

```text
Student -> API #26 catalog + AC-15 -> candidate resources by lesson_id
-> catalog response ApiEnvelope<Lesson> conflicts semantically with resource-list intent
Current Study route/module/query/focused test -> API #26 NOT_FOUND / UNWIRED
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #26 runtime | Router/module/test inventory omits endpoint | `UNWIRED` / `NOT_FOUND` | DD documents expected design only. |
| Response payload | Catalog and diagram say `ApiEnvelope<Lesson>`; endpoint purpose is attached resources and reusable `Resource` is separate | `DISCREPANCY` / `SOURCE_REQUIRED` | Keep catalog type and do not invent a resource array or Lesson field. |
| Resource visibility | Reusable `Resource` mentions visibility; ERD/DDL has no `resources.visibility` | `DISCREPANCY` / `SOURCE_REQUIRED` | No visibility predicate or field mapping is inferred. |
| Cardinality/order/empty result | Resource FK permits multiple resources; API #26 contract has no list/cardinality/order rule | `SOURCE_REQUIRED` | No array/page, ordering or empty-result behavior is selected. |
| Access/publish policy | AC-15 states access precondition; diagram does not give API-specific predicate | `SOURCE_REQUIRED` | Keep 403/404 conditions unresolved. |
| Signed URL behavior | API #12 design discusses signed URL, but API #26 flow does not specify it | `SOURCE_REQUIRED` | Do not claim URL signing or external storage call. |

## CHANGES

- Files changed: Added `apps/study-server/docs/dd/26_lessons_resources/` (8 template sheets and 3 reports) and this worklog.
- CONTEXT_UPDATES: None — no canonical context page or manifest changed.
- Context pages changed: None.
- Assumptions: Keep DD status `Draft — Needs Confirmation`; preserve all existing worktree changes; no ZIP per Study Server workflow.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Docs worklog selector and review | Selected and read API #16–#18 docs worklogs; shortage none. | VERIFIED |
| Contract/AC/schema/runtime comparison | API #26 catalog and AC-15 compared with resource ERD/DDL and current router/module/test inventory; API #26 is `UNWIRED / NOT_FOUND`. | VERIFIED |
| Inline static Markdown validator | 11 deliverables; front matter, code fences, table widths, whitespace, JSON examples, local links and anchors passed. | VERIFIED |
| API contract code check | Method/path/actor/request/response and exact 200/401/403/404/500 code set match API #26 catalog. | VERIFIED |
| Template/output fingerprints | SHA-256 for all eight baseline and authored sheets recorded in `VERIFICATION_REPORT.md`. | VERIFIED |
| `git diff --check` and authored-file whitespace scan | No whitespace errors reported; all new Markdown files passed trailing whitespace check. | VERIFIED |
| Study Server application tests | Not run; documentation-only scope and API #26 is not wired. | NOT_RUN |
| Context validator | Not required; no canonical context page or manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Q-26-01 through Q-26-07 in `OPEN_QUESTIONS.md` require contract/schema owner decisions before marking the DD Ready/Final or using it as an implementation contract.
- Next owner/action: Confirm response shape/cardinality, entitlement/publish behavior, visibility/URL policy, error semantics and schema constraints in canonical sources.

