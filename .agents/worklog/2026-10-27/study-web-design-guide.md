---
task_id: "2026-10-27-study-web-design-guide"
date: "2026-10-27"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Tạo design guide cho Study Web

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/load-study-server-context.md`
    - carry_forward: Tách current source khỏi contract/tài liệu; không coi kiểm tra tĩnh hoặc kết quả test lịch sử là xác minh runtime hiện tại.
  - path: `.agents/worklog/2026-10-24/commit-push-study-dd.md`
    - carry_forward: Không suy diễn trạng thái giao nhận/remote từ worklog cũ; giới hạn file sửa đúng scope.
  - path: `.agents/worklog/2026-10-24/complete-study-api01-dd-package.md`
    - carry_forward: Giữ requirement kỳ vọng tách khỏi current behavior; không thêm logic hoặc mapping khi source/contract chưa có bằng chứng.
- shortage: `none` (131 worklog docs khả dụng; đã đọc đủ 3 worklog được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Tạo `.agents/web-study/design.md` làm design target riêng cho Study Web; Study Web UI/UX/graphic-design/FE coding task phải đọc tài liệu này trước khi làm.
- Canonical contract/approved DD: Yêu cầu người dùng và plan đã duyệt; chỉ tạo một design artifact mới, cập nhật context graph cần thiết, không sửa mã trong `apps/`.

## CURRENT_BEHAVIOR

- Source/config: Context Study Web hiện nằm dưới `.agents/web-work/study/`; chưa có `.agents/web-study/`. Context entry chưa bắt buộc đọc design page; manifest subcontext `web-work.study-web` chưa đăng ký page này. `.agents/project/design.md` chỉ áp dụng Work Web/Mobile. Checkout hiện không có `apps/study-client/`; architecture context ghi nhận màu xanh lá từ snapshot cũ.
- Runnable tests: Không áp dụng cho tài liệu thiết kế; không chạy FE tests.
- Runtime wiring: Study Web là subcontext của web-work; root router → web-work AGENTS → study subcontext. Chưa có route/API contract Study OpenAPI; design guide chỉ là target visual/UX.

## SOURCE_TRACE

```text
AGENTS.md -> .agents/context-map.md -> .agents/web-work/AGENTS.md -> .agents/web-work/study/AGENTS.md + INDEX.md -> Study Web source/context pages
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study Web source | Manifest yêu cầu các source paths dưới `apps/study-client/`, nhưng checkout hiện thiếu source root; Study Web architecture context còn ghi nhận visual baseline xanh lá. | `SOURCE_REQUIRED / DISCREPANCY` | Design guide xác định intended future direction; không mô tả hoặc tuyên bố giao diện hiện hành. |
| Context validator baseline | Lượt preflight hiện tại báo thiếu DB Admin context/source và thiếu Study Web source; snapshot Git `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4` không có trong local object database. | `CONTEXT_BASELINE_INVALID` | Sau sửa phải kiểm tra không phát sinh lỗi mới liên quan page/link/registry; không sửa scope ngoài yêu cầu. |

## CHANGES

- Files changed: `.agents/web-study/design.md`, `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/context-manifest.json`, `.agents/context-map.md`, và worklog này. Không sửa file trong `apps/`.
- CONTEXT_UPDATES: Đăng ký design page vào `web-work.study-web.pages`, thêm link trong Study Web index/context map, và thêm chỉ thị bắt buộc đọc trong Study Web AGENTS.
- Context pages changed: `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/context-map.md`, `.agents/context-manifest.json`.
- Assumptions: Study-specific custom ocean palette; giao diện sáng trước; không thêm font/dependency; "chỉ design.md" nghĩa là không sửa FE source, trong khi minimal context wiring vẫn được phép theo yêu cầu #4.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `git status --short --branch` | `develop...origin/develop`; worktree sạch trước khi bắt đầu. | VERIFIED |
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Chọn 3/131 worklog cùng type; đã đọc đủ. | VERIFIED |
| Manifest/page/link and palette check (Python, read-only) | JSON hợp lệ; design page đã đăng ký và được index/map/AGENTS tham chiếu; các link mới resolve; Markdown mới không có trailing whitespace/final newline issue; primary/text/status colors kiểm tra trên trắng đều đạt >=4.5:1. | VERIFIED_STATIC_ONLY |
| `git diff --check` | Không có whitespace errors trong tracked changes. | VERIFIED |
| `deno run --allow-read --allow-env scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID` còn các lỗi baseline: thiếu DB Admin context/source, thiếu 10 Study Web source paths và snapshot Git gốc. Không có lỗi mới cho `.agents/web-study/design.md`, page registry hoặc context links. | CONTEXT_BASELINE_INVALID |
| Study Web FE tests/build | Không chạy vì không thay đổi FE source; `apps/study-client/` không có trong checkout. | NOT_RUN_BY_SCOPE |

## HANDOFF

- Remaining blockers: Context validator toàn repo vẫn không xanh vì các path DB Admin/Study Web và Git snapshot nền bị thiếu; không sửa các scope này ngoài yêu cầu.
- Next owner/action: Đọc `.agents/web-study/design.md` trước mọi task Study Web UI/UX/đồ họa/FE. Khi source Study Web được khôi phục, đối chiếu implementation với design target này; chưa có UI code được sửa trong task hiện tại.
