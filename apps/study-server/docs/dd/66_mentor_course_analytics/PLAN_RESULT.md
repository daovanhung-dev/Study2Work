# Plan Result — Study API #66

## Kết quả theo plan

| Plan item | Kết quả |
|---|---|
| Preflight/context | Đọc 3 worklog cùng loại coding; bảo toàn worktree bẩn. |
| AC-26 trace | #65 class progress → #66 Aggregate learning events → chọn Student → #67 student progress. Không có server-to-server call. |
| Linked #67 review | DD #67 vẫn ghi Mentor guard chưa có và error helper data {}; các nhận định này stale so với shared runtime. #67 vẫn UNWIRED và cần reconciliation ở phiên riêng. |
| DDL/source audit | Legacy DDL có courses/lessons/lesson_progress current state nhưng không có learner event ledger. V1-PILOT event IDs là markers; audit/outbox là generic. |
| Local fallback | DERIVED activity proxy từ distinct Student/lesson pairs có last_accessed_at trên PUBLISHED lessons; trả pair count, distinct Student count và MAX timestamp. Không claim số event. |
| Authorization | Shared Mentor JWT guard; local direct-owner predicate courses.mentor_id = JWT sub. |
| Local response | Summary object phục vụ AC-26; direct diagram/catalog ApiEnvelope<Page<Course>> được giữ và ghi discrepancy. |
| Routing/error handling | GET route wired; raw path parse signed int64; error status set 401/403/404/500; middleware design-contract path đã đăng ký. |
| Side effects | Read-only; không mutation và không gọi #65/#67. |
| DD/context | 8 sheets + 3 reports; 8 template suffixes giữ nguyên; context pages và manifest ghi runtime/discrepancy. DD status giữ Draft — Needs Confirmation. |
| Focused HTTP | API #66: 18 passed; API #65–#66 regression: 38 passed. |
| Full Study suite | 698 passed; một Starlette/httpx TestClient deprecation warning. |
| Ruff/import/OpenAPI | Ruff pass; compileall pass; OpenAPI có 39 path templates/40 operations; API #66 responses đúng 200/401/403/404/500. |
| Static docs/diff | 11 Markdown files, links/fences/frontmatter pass, template suffixes 8/8 pass; scoped git diff --check pass. |
| Context validator | AGENT_CONTEXT_INVALID chỉ do DB Admin context/source paths thiếu ngoài phạm vi; không có lỗi server-study/API #66 được nêu. |

## Quy tắc diễn giải fallback

- tracked_lesson_accesses là số cặp hiện có, không phải lịch sử số lần mở lesson.
- students_with_activity không phải số enrollment hoặc event actors từ event stream.
- last_activity_at là timestamp hiện lưu ở lesson_progress; update/upsert có thể ghi đè các access trước.
- Không query pilot progress snapshots, last_event_id, audit_events hoặc outbox_events.
- Không sửa API catalog/diagram hoặc DDL để tạo event semantics mới.
- Fake DB HTTP tests không xác minh schema live, migration hoặc deployment.
