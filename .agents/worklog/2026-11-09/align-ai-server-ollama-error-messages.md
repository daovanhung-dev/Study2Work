---
task_id: "2026-11-09-align-ai-server-ollama-error-messages"
date: "2026-11-09"
primary_task_type: "fix"
secondary_task_types: ["test"]
project_scopes: ["server-ai"]
cross_scope_dependencies: ["AI Server -> Ollama HTTP API"]
status: "VERIFIED_LOCAL"
---

# Đồng bộ thông báo lỗi AI Server với SPEC

## PRIOR_WORKLOG_REVIEW

- selector_command: `node scripts/select-worklogs.mjs --type fix --limit 3`
- prior_worklogs_reviewed:
  - `.agents/worklog/2026-11-01/fix-study-api-null-bind-parameters.md`: giữ lỗi validator toàn repo tách khỏi lỗi cục bộ.
  - `.agents/worklog/2026-10-25/remove-unicode-encode-catch-access-token.md`: giữ nguyên HTTP mapping và response contract khi sửa lỗi.
  - `.agents/worklog/2026-10-25/remove-valueerror-study-server.md`: trace caller và test response trước khi đổi handler.
- shortage: `none` (3/3 log cùng type đã đọc).

## CLASSIFICATION

```text
primary_task_type: fix
secondary_task_types: [test]
project_scopes: [server-ai]
cross_scope_dependencies: [AI Server -> Ollama HTTP API]
```

## EXPECTED_BEHAVIOR

- Canonical contract: `docs/ai-server/ollama-client-and-error-handling/SPEC.md`, REQ-05, bảng HTTP/error code/message. Bốn message là chuỗi client nhìn thấy; giữ nguyên status, code và JSON `{error:{code,message}}`.
- Developer đưa nhận xét review về ba message sai và yêu cầu kiểm tra lại. So sánh exact string còn phát hiện `OLLAMA_BAD_RESPONSE` lệch dấu chấm cuối câu.

## CURRENT_BEHAVIOR_AND_TRACE

- Trước sửa: `app/main.py` trả đúng status/code nhưng cả bốn message không khớp nguyên văn SPEC; `tests/test_chat_api.py` chỉ assert status/code và tên field.
- Luồng: `POST /api/v1/chat_log_ai` -> `ChatLogRequest` -> `chat_log_ai` -> `ai_service.generate` -> lỗi Ollama/pool -> exception handler trong `app/main.py` -> JSON cho client. Không có DB write; không thay đổi route hay success response.
- GitHub Compare `develop...ducna_dev/featrure_AI_sever` hiện báo 2 commit ahead, 1 commit behind. Local `origin/develop` cũ hơn remote nên phép so sánh local ra 0 behind; dùng GitHub làm bằng chứng cho trạng thái remote.

## CHANGES

- `apps/ai-server/app/main.py`: đồng bộ bốn message nguyên văn theo SPEC, gồm dấu câu.
- `apps/ai-server/tests/test_chat_api.py`: với mỗi nhánh lỗi, assert `error.message` đúng chuỗi bên cạnh status/code; giữ kiểm tra không lộ prompt/body.
- Không đổi SPEC, PLAN hoặc context API vì yêu cầu và mô tả context hiện tại vẫn đúng; đây là fix implementation khớp contract đã duyệt.

## VERIFICATION

| Kiểm tra | Kết quả | Trạng thái |
|---|---|---|
| `& .venv/Scripts/python.exe -m unittest discover -s tests -q` từ `apps/ai-server` | 8 tests pass, gồm các subcase lỗi có assertion message. | `PASS` |
| `git diff --check` | Không có lỗi khoảng trắng trong hai file source/test đã sửa. | `PASS` |
| `node scripts/validate-agent-context.mjs` | Exit 1 trên baseline toàn repo: thiếu DB Admin và báo orphan context pages, gồm AI Server; không có thay đổi context page trong fix này. | `BASELINE_FAILURE` |

## HANDOFF

- Bản sửa đã xác minh cục bộ. Developer chọn commit message `fix(ai-server): align error messages with approved spec`; stage đúng hai file source/test và worklog này, rồi commit/push lên `ducna_dev/featrure_AI_sever`. Giữ các file untracked khác ngoài scope.
