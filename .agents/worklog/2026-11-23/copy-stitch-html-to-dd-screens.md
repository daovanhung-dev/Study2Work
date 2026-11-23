---
task_id: "2026-11-23-copy-stitch-html-to-dd-screens"
date: "2026-11-23"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Chép screen_stitch code.html vào DD packages

## READ_PLAN

| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `AGENTS.md` | Nội dung root router được cung cấp trong task context | Quy tắc phân loại, read-set, target và worklog | `READ_FROM_CONTEXT` |
| `.agents/AGENTS.md` | Global context index và quy tắc read-set/worklog | Router context bắt buộc; đã nạp ở task liền trước | `READ_FROM_CONTEXT` |
| `.agents/context-map.md` | Page graph và mapping apps/study-client → web-work/study-web | Chọn đúng scope; đã nạp ở task liền trước | `READ_FROM_CONTEXT` |
| `.agents/context-manifest.json` | Registry web-work/study-web và docs workflow | Xác nhận context wiring; đã nạp ở task liền trước | `READ_FROM_CONTEXT` |
| `.agents/project/agent-control.md` | Target, silent execution, read-set, worklog rules | Áp dụng tracking; đã nạp ở task liền trước | `READ_FROM_CONTEXT` |
| `.agents/target.md` | Bảng active target | Tracker đã là header-only trước task này; kiểm tra theo task context | `READ_FROM_CONTEXT` |
| `.agents/worklog/README.md` | Read-set, selector preflight, required order | Contract worklog; đã nạp ở task liền trước | `READ_FROM_CONTEXT` |
| `.agents/worklog/TEMPLATE.md` | Các trường worklog bắt buộc | Khởi tạo log; đã nạp ở task liền trước | `READ_FROM_CONTEXT` |
| `scripts/select-worklogs.mjs` | CLI/type match và selector output | Chọn cùng loại `docs` trước khi xử lý | `READ_FROM_CONTEXT` |
| `scripts/validate-agent-context.mjs` | Chạy validator sau cập nhật worklog/target | Kiểm tra contract context/worklog theo router | `CHECKED_BY_TOOL` |
| `.agents/worklog/2026-11-23/copy-stitch-html-to-dd-screens.md` | Nội dung worklog hiện tại | Selector có thể trả về worklog của task hiện tại | `READ_FROM_CONTEXT` |
| `.agents/worklog/2026-11-23/load-study-client-context.md` | Source summary, verification, handoff | Carry-forward context từ task vừa nạp Study Web | `READ` |
| `.agents/worklog/2026-11-21/2026-11-21-build-server-web-commands.md` | Summary, current behavior, context updates, verification, handoff | Carry-forward Study Web local command/proxy facts | `READ` |
| `.agents/worklog/2026-11-21/document-server-and-script-prompts.md` | Worklog body was not selected | Do not substitute a nonselected log | `SKIPPED` |
| `.agents/web-work/AGENTS.md` | Scope router and Study subcontext routing | Study Web ownership; đã nạp ở task liền trước | `READ_FROM_CONTEXT` |
| `.agents/web-work/INDEX.md` | Web Work page graph | Chọn Study Web pages; đã nạp ở task liền trước | `READ_FROM_CONTEXT` |
| `.agents/web-work/study/AGENTS.md` | Study Web rules | Phạm vi apps/study-client; đã nạp ở task liền trước | `READ_FROM_CONTEXT` |
| `.agents/web-work/study/INDEX.md` | Study Web page map and source status | Phạm vi apps/study-client; đã nạp ở task liền trước | `READ_FROM_CONTEXT` |
| `.agents/web-study/frontend-rules.md` | Frontend source/design separation rules | File HTML là reference; đã nạp ở task liền trước | `READ_FROM_CONTEXT` |
| `.agents/web-study/design.md` | Intended visual/interaction target | Bối cảnh UI prototype; đã nạp ở task liền trước | `READ_FROM_CONTEXT` |
| `.agents/web-work/study/workflows/screen-implementation.md` | DD and screen asset workflow | Xác nhận HTML là reference; đã nạp ở task liền trước | `READ_FROM_CONTEXT` |
| `apps/study-client/docs/screen_stitch/README.md` | Source asset location, screen group counts and variant rules | Giữ source assets; đã đọc ở task liền trước | `READ_FROM_CONTEXT` |
| `apps/study-client/docs/dd_screens/PLAN.md` | Package/source preservation and acceptance rules | Xác định việc copy không làm thay đổi source; đã đọc ở task liền trước | `READ_FROM_CONTEXT` |
| `apps/study-client/docs/dd_screens/screen-index.md` | ID → DD package mapping table | Ánh xạ 83 nguồn vào đúng folder; đã đọc ở task liền trước | `READ_FROM_CONTEXT` |
| `apps/study-client/docs/screen_stitch/**/code.html` | All 83 source files; byte-copy and hash verification only | Nguồn cần chép, giữ nguyên nội dung | `CHECKED_BY_TOOL` |
| `apps/study-client/docs/dd_screens/*/code.html` | Existing destination collision check and hash verification | Bảo toàn GS-01 untracked copy và không overwrite conflict | `CHECKED_BY_TOOL` |
| `apps/study-client/docs/screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/code.html` | Exact source bytes | Recheck existing mapped file before preserving/copying | `CHECKED_BY_TOOL` |
| `apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc/code.html` | Exact existing destination bytes | Existing user file; compare and leave unchanged if identical | `CHECKED_BY_TOOL` |

## LEAF_TARGET_PLAN

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Chép 7 prototype Shared/Auth/System vào DD package | Chép các `SH-01`–`SH-07` HTML theo ID | Mỗi nguồn có đúng một DD đích với byte/hash giống nguồn; nguồn giữ nguyên |
| Chép 7 prototype Guest/Discovery vào DD package | Chép các `GS-01`–`GS-07` HTML theo ID | 7 đích khớp nguồn; GS-01 copy có sẵn giống nguồn và không bị ghi lại |
| Chép 26 prototype Student vào DD package | Chép các `ST-01`–`ST-26` HTML theo ID | Mỗi nguồn có đúng một DD đích với byte/hash giống nguồn; nguồn giữ nguyên |
| Chép 18 prototype Mentor vào DD package | Chép các `ME-01`–`ME-18` HTML theo ID | Mỗi nguồn có đúng một DD đích với byte/hash giống nguồn; nguồn giữ nguyên |
| Chép 25 prototype Admin vào DD package | Chép các `AD-01`–`AD-25` HTML theo ID | Mỗi nguồn có đúng một DD đích với byte/hash giống nguồn; nguồn giữ nguyên |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-23/load-study-client-context.md`
    - carry_forward: Study Web is owned by `web-work/study-web`; the prior task found context-page discrepancies unrelated to copying reference HTML. App source was not inspected there.
  - path: `.agents/worklog/2026-11-21/2026-11-21-build-server-web-commands.md`
    - carry_forward: Historical note records local Study Web `/api/v1` proxy to `127.0.0.1:3003`; no transfer-specific behavior.
- selector also returned the new current task worklog; it is not a prior task.
- shortage: `none` (295 matching docs worklogs available; 3 selected)

## EXPECTED_BEHAVIOR

- Requirement: Chuyển các `screen_stitch/**/code.html` vào DD package cùng screen ID.
- Clarification: Chép vào DD và giữ nguyên originals theo lựa chọn của người dùng; không di chuyển hoặc xóa file nguồn.
- Canonical docs: `screen_stitch/README.md` giữ `code.html` làm source asset; `dd_screens/screen-index.md` ánh xạ screen ID sang package; `dd_screens/PLAN.md` yêu cầu không sửa source assets.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Chép 7 prototype Shared/Auth/System vào DD package | `0% → 100%` | Đã chép 7 file và xác minh hash đích trùng nguồn trong nhóm SH. |
| Chép 7 prototype Guest/Discovery vào DD package | `0% → 100%` | Đã chép 6 file; file GS-01 có sẵn giữ nguyên; xác minh đủ 7 hash đích trùng nguồn. |
| Chép 26 prototype Student vào DD package | `0% → 100%` | Đã chép 26 file và xác minh hash đích trùng nguồn trong nhóm ST. |
| Chép 18 prototype Mentor vào DD package | `0% → 100%` | Đã chép 18 file và xác minh hash đích trùng nguồn trong nhóm ME. |
| Chép 25 prototype Admin vào DD package | `0% → 100%` | Đã chép 25 file và xác minh hash đích trùng nguồn trong nhóm AD. |

## CURRENT_BEHAVIOR

- Source/config: Fresh inventory/hash preflight found 83 unique `screen_stitch` IDs, 83 matching DD folders, 82 missing destination files, and one existing destination (`GS-01-DanhSachKhoaHoc/code.html`) that is byte-identical to source. There are no destination conflicts.
- Runnable tests: No app tests are in scope; this is a documentation asset copy.
- Runtime wiring: These HTML files are visual/prototype references, not Angular runtime source.

## SOURCE_TRACE

```text
screen_stitch/<group>/<ID>_<slug>/code.html -> screen-index.md row for <ID> -> dd_screens/<ID>-<Name>/code.html
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Existing GS-01 destination | Current `git status` shows the DD file is untracked; pre-copy SHA-256 check confirms it is identical to the Stitch source. | `VERIFIED` | Preserve it; do not overwrite. |

## CHANGES

- Files changed: 82 new `code.html` files under DD packages and this worklog; `.agents/target.md` was updated for the five leaf targets then returned to header-only. Existing untracked `GS-01-DanhSachKhoaHoc/code.html` was preserved unchanged.
- CONTEXT_UPDATES: None; no source/runtime contract changes.
- Context pages changed: None.
- Assumptions: Destination filename is `code.html` at the root of each DD package; no HTML transformation or DD Markdown link update is requested.
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`; 295 available, current worklog plus two prior docs worklogs selected; both prior bodies reviewed; no shortage | `VERIFIED_PREFLIGHT` |
| Ephemeral Node inventory/hash preflight | 83 source IDs and 83 target folders; 82 destinations missing; GS-01 destination already identical; no duplicate IDs, missing folders or conflicts | `VERIFIED_STATIC` |
| Ephemeral Node copy operation | Copied 82 files; preserved one identical GS-01 destination; per-group counts: SH 7, GS 6+1 existing, ST 26, ME 18, AD 25 | `VERIFIED_STATIC` |
| Ephemeral Node post-copy hash verification | 83 sources, 83 destinations and 83 target folders; no missing IDs, mismatches or duplicate IDs | `VERIFIED_STATIC` |
| `git status --short -- apps/study-client/docs/screen_stitch` | No source changes | `CHECKED_BY_TOOL` |
| `git status --short --untracked-files=all -- apps/study-client/docs/dd_screens | wc -l` | 83 DD code files are untracked, including the pre-existing GS-01 copy | `CHECKED_BY_TOOL` |
| App tests | Not run; no application code changed | `NOT_RUN` |
| `node scripts/validate-agent-context.mjs` | Exit 1, `AGENT_CONTEXT_INVALID`; the current filtered output reports missing tracked Study Web path `apps/study-client/src/app/features/auth/.gitkeep`. No worklog/target errors were reported by the filter; repository-wide validator drift was already present in the immediately prior task. | `AGENT_CONTEXT_INVALID` |

## HANDOFF

- Remaining blockers: None for the requested copy. The global context validator remains invalid on repository context/source inventory outside this task; the Study Web missing `.gitkeep` finding is recorded above.
- Next owner/action: None.
