---
task_id: "2026-11-09-add-study-frontend-rules"
date: "2026-11-09"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Thêm bộ rule bắt buộc cho Study Web

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 269 worklog cùng loại; đã chọn và đọc đủ 3.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-09/code-review-skill-pack.md`
    - carry_forward: Xác minh wiring qua registry; giữ lỗi validator nền riêng biệt với lỗi do thay đổi mới.
  - path: `.agents/worklog/2026-11-09/load-study-client-context.md`
    - carry_forward: DD/assets không phải bằng chứng runtime; giữ Study Web ở trạng thái `SKELETON_ONLY` và đối chiếu source hiện tại.
  - path: `.agents/worklog/2026-11-09/translate-study-architecture-vietnamese.md`
    - carry_forward: Giữ tài liệu kiến trúc bằng tiếng Việt; phân biệt cấu trúc dự kiến với wiring runtime hiện có.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo rule tiếng Việt bắt buộc cho Study Web Angular, nêu rõ trách nhiệm từng lớp, ranh giới UI/nghiệp vụ/data-access, chiều phụ thuộc, vai trò từng feature và trạng thái DD/API so với runtime. Đăng ký và bắt buộc nạp rule qua Study Web agent context; đồng bộ `architech.md` với `domain/` tùy chọn.
- Canonical contract/approved DD: Kế hoạch đã được người dùng duyệt trong hội thoại. Không sửa mã Angular, không tạo feature/API hay thay đổi public interface.

## CURRENT_BEHAVIOR

- Source/config: App hiện là scaffold Angular 22; root component và tuyến gốc tối thiểu, feature directories chỉ có `.gitkeep`. Study Web context đăng ký design guide nhưng chưa có trang rule frontend chuyên biệt. `architech.md` chưa nêu `domain/`.
- Runnable tests: Không chạy test/build theo phạm vi tài liệu.
- Runtime wiring: Màn hình nghiệp vụ, auth, Study API và deployment chưa được nối/xác minh; status giữ `SKELETON_ONLY`.

## SOURCE_TRACE

```text
Study Web agent router -> frontend-rules.md -> layer/feature boundary rules -> Angular scaffold and verified DD/API sources
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Rule UI/nghiệp vụ | Context hiện có design guide và kiến trúc tổng quát nhưng chưa có rule bắt buộc cho ranh giới lớp. | `CONTEXT_RULE_MISSING` | Tạo trang rule riêng và wire bắt buộc vào subcontext. |
| Lớp domain | Feature template trong `architech.md` chưa có `domain/`. | `ARCHITECTURE_DOC_NEEDS_ALIGNMENT` | Thêm `domain/` dạng tùy chọn; không tạo thư mục nguồn khi chưa có nghiệp vụ. |

## CHANGES

- Files changed: `.agents/web-study/frontend-rules.md`, `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/context-manifest.json`, `.agents/context-map.md`, `apps/study-client/gui/architech.md`, worklog này.
- CONTEXT_UPDATES: Đăng ký rule frontend Study Web và nêu rõ lúc agent bắt buộc phải nạp.
- Context pages changed: Thêm rule page tiếng Việt; nối vào Study Web router, index, manifest và context map; đồng bộ feature template/runtime flow trong architecture doc.
- Assumptions: Rule chỉ áp dụng cho `apps/study-client`; nội dung rule viết tiếng Việt; các ví dụ feature/DD không khẳng định runtime đã triển khai.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` và đọc các log được chọn | `READY`; 3 log `docs` đã được đọc; không thiếu log. | VERIFIED |
| Context manifest JSON và Study Web page wiring | JSON parse thành công; rule nằm trong `web-work/study-web.pages`; các trang mục tiêu tồn tại. | VERIFIED_STATIC_ONLY |
| Kiểm tra liên kết rule | Liên kết từ Study Web AGENTS, INDEX, context map và `architech.md` đều trỏ tới `frontend-rules.md`. | VERIFIED_STATIC_ONLY |
| Kiểm tra nội dung/whitespace Markdown | Sáu file liên quan có newline cuối, không có trailing whitespace; rule nêu trách nhiệm page/ui/domain/data-access/models/shared/core/layouts và dependency boundaries. | VERIFIED_STATIC_ONLY |
| `git diff --check` | Không có whitespace error. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | Exit 1, `AGENT_CONTEXT_INVALID` với 83 finding nền: thiếu DB Admin context/source, orphan resources `create_dd_screen`, broken DB Admin links và `CONTEXT_STALE` ở scope khác. Study Web-specific finding duy nhất là context snapshot cũ trỏ tới các đường dẫn Vue/Vite đã cũ; không finding nào nhắc `frontend-rules.md` hoặc wiring mới. | BASELINE_INVALID_UNRELATED |
| Test/build ứng dụng | Không chạy theo phạm vi tài liệu. | NOT_RUN |

## HANDOFF

- Remaining blockers: Context validator toàn repo vẫn invalid do drift nền nêu trên; không có lỗi mới cho trang rule/wiring.
- Next owner/action: Hoàn tất; không có thay đổi mã Angular hoặc API.
