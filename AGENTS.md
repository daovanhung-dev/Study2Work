# Study2Work agent router

Đây là điểm vào bắt buộc cho coding agent. File này chỉ định tuyến; context chi tiết nằm trong `.agents/`. Source hiện tại luôn phải được kiểm tra lại trước khi sửa.

## 1. Phân loại task

Trước khi đọc sâu, ghi ngắn:

```text
primary_task_type: coding | fix | docs | test
secondary_task_types:
  - <loại khác, nếu có>
project_scopes:
  - mobile-work | web-work | server-work | server-study | server-ai
cross_scope_dependencies:
  - <contract/path nối các scope, nếu có>
```

- `coding`: requirement/contract -> pattern hiện có -> implementation -> test.
- `fix`: reproduce -> trace caller/callee/effect -> root cause -> smallest fix -> regression test.
- `docs`: source -> verified tests/contracts -> tài liệu hiện có -> cập nhật.
- `test`: requirement/contract -> implementation -> edge cases -> convention test.

Một task có thể có nhiều `project_scopes`. Không ép task cross-scope vào một scope duy nhất.

## 2. Định tuyến scope

| Scope | Source chính | Đọc tiếp |
|---|---|---|
| `mobile-work` | `apps/work-client/mobile/` | `.agents/mobile-work/AGENTS.md` |
| `web-work` | `apps/study-client/`, `apps/work-client/web/` | `.agents/web-work/AGENTS.md` |
| `server-work` | `apps/work-server/` | `.agents/server-work/AGENTS.md` |
| `server-study` | `apps/study-server/` | `.agents/server-study/AGENTS.md` |
| `server-ai` | `apps/ai-server/` | `.agents/server-ai/AGENTS.md` |

Không nạp scope khác nếu chưa có dependency thật. Task qua nhiều scope phải ghi contract nối giữa chúng; ví dụ Study -> Work event dùng `contracts/events/study-work/`.

## 3. Progressive loading

```text
AGENTS.md
  -> .agents/<scope>/AGENTS.md
  -> module/API/core/service context được scope chỉ định
  -> exact source + tests + config/contract liên quan
```

Không đọc toàn repository cho task cục bộ. Chỉ mở `.agents/project/*` khi task qua nhiều app, cần ownership/global convention, hoặc đang bảo trì chính context.

## 4. Expected behavior và current behavior

Hai loại bằng chứng phải được giữ tách biệt.

### Expected behavior

1. Yêu cầu mới nhất của người dùng.
2. Canonical DD/API contract còn tồn tại.
3. Approved business rule / implementation plan.

### Current behavior

1. Runtime/source code hiện tại.
2. Test đã thực sự xác minh/runnable.
3. Executable contract/config hiện hành.

Nếu hai phía khác nhau, ghi `DISCREPANCY`; không tự reconcile bằng suy đoán. Khi mô tả hiện trạng, ưu tiên `current source > verified runnable tests > documentation`.

## 5. Luật bắt buộc

- Không tự tạo API, field, table, validation, service, business code hoặc HTTP behavior khi chưa có bằng chứng.
- Trước khi sửa function, trace caller, callee, DB/side effect, response, business code và test bị ảnh hưởng.
- Chỉ sửa file tối thiểu; không refactor ngoài phạm vi.
- Không ép architecture của một server lên server khác.
- `VERIFIED`, `UNWIRED`, `DECLARED_NOT_RUNNABLE`, `NOT_FOUND` là trạng thái có nghĩa; file tồn tại không đồng nghĩa runtime dùng file đó.
- Nếu code/contract/DB/convention thay đổi theo cách làm context sai, cập nhật đúng page `.agents/` trong cùng task.
- Trước khi kết thúc task có thay đổi context, chạy `node scripts/validate-agent-context.mjs`.
