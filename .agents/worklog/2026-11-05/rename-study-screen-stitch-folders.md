---
task_id: "2026-11-05-rename-study-screen-stitch-folders"
date: "2026-11-05"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Chuẩn hóa tên folder screen_stitch

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; đã đọc đủ 3 worklog trong 142 log `docs` khả dụng.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-05/check-study-screen-stitch-coverage.md`
    - carry_forward: Inventory có 83 ID, 84 folder do duplicate SH-01; giữ nguyên hai biến thể và artifact.
  - path: `.agents/worklog/2026-11-05/load-study2work-context.md`
    - carry_forward: Study Web `screen_stitch` chỉ là design artifact trong checkout; không gán runtime status.
  - path: `.agents/worklog/2026-11-05/organize-study-screen-stitch.md`
    - carry_forward: Folder đã được nhóm theo inventory; giữ nguyên category folders và nội dung 169 file đã có.
- shortage: `none` (142 worklog docs khả dụng; đã đọc đủ 3 được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Đổi tên 84 folder màn hình theo `<ID>_<slug-ASCII>` từ tiêu đề `apps/study-client/docs/list_screen.md`, bỏ hậu tố branding thừa; đổi tên folder design reference; giữ nguyên category folders và nội dung artifact.
- Canonical contract/approved DD: Inventory `list_screen.md` là nguồn tên và ID; 83 mã unique, SH-01 có hai variant. Slug bỏ dấu, `đ` thành `d`, dấu câu thành dấu gạch ngang; SH-01 variant suffix lần lượt là `__variant-1`/`__variant-2`.

## CURRENT_BEHAVIOR

- Source/config: Trước thay đổi có 84 screen folders trong 5 category folders, SH-01 có hai folder kết thúc `_1`/`_2`; reference nằm ở `90_reference/study2work_lms/DESIGN.md`. Mapping dry-run sinh 84 tên đích, không có collision. Pre-edit hash multiset cho 169 file là `f0a4a854d4bb69d053865d247f7300b51818dc825239c23f05589dd68c89d72a`.
- Runnable tests: Không chạy; không đổi runtime code.
- Runtime wiring: Không xác minh hoặc thay đổi Study Web runtime; artifact tiếp tục là design resource.

## SOURCE_TRACE

```text
list_screen.md title + stable ID -> deterministic ASCII slug -> destination inside existing actor category; SH-01 old _1/_2 -> explicit variant suffix; reference DESIGN.md -> descriptive reference folder
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Duplicate SH-01 | Two source folders have suffix `_1` and `_2`; neither is marked as preferred. | `DUPLICATE_VARIANT` | Preserve both with corresponding `__variant-1`/`__variant-2`; do not infer which is newer. |
| Existing path mentions | Current README refers to the reference folder; historical worklogs describe the previous names. | `PATH_REFERENCE` | Update active README path; retain historical worklogs as historical evidence. |

## CHANGES

- Files changed: Renamed 84 screen folders and `90_reference/study2work_lms`; updated `screen_stitch/README.md`; this worklog.
- CONTEXT_UPDATES: None; no runtime/API/architecture change.
- Context pages changed: None.
- Assumptions: Keep category directory names; use canonical title from inventory, lowercase ASCII transliteration, ID in uppercase, one underscore before slug, punctuation collapsed to one hyphen.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Worklog selector + selected worklogs | Selected and read 3 exact-type logs in 142 available. | VERIFIED |
| Rename dry-run | 84 destination names + reference destination derived; 0 collisions; pre-existing file hash multiset captured. | VERIFIED_STATIC_ONLY |
| Post-rename inventory/name audit | 83 IDs match all 84 expected folder names; no old mangled names, collisions, missing IDs, or extra IDs. Counts: SH 8 folders, GS 7, ST 26, ME 18, AD 25. | VERIFIED_STATIC_ONLY |
| Artifact/reference audit | All 84 screen folders still contain non-empty `screen.png` and `code.html`; PNG signatures pass; reference path and README are updated with no stale reference path. | VERIFIED_STATIC_ONLY |
| Content hash multiset before/after | All 169 pre-existing files are unchanged; aggregate SHA-256 matches pre-edit `f0a4a854d4bb69d053865d247f7300b51818dc825239c23f05589dd68c89d72a`. | VERIFIED_STATIC_ONLY |
| `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/validate-agent-context.mjs` | Exit 1 (`AGENT_CONTEXT_INVALID`) on pre-existing missing Study Web/DB Admin context/source paths, broken links and stale scope snapshots. | FAILED / PRE_EXISTING_CONTEXT_DRIFT |
| Tests | Not run; no runtime code changed. | NOT_RUN |

## HANDOFF

- Remaining blockers: Repository context validator remains failed on pre-existing Study Web/DB Admin path and stale-snapshot errors; folder naming and artifact checks pass.
- Next owner/action: Finish context validation and hand off the standardized folder tree.
