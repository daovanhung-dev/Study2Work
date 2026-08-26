# AGENTS context index

Source snapshot gốc cho deep-context: `5a5c2c826ddcc2931a9398115fdb61448dcb4c57` (2026-08-26). Context mô tả working tree tại snapshot này và được validator theo dõi drift sau đó.

## Scope registry

| Scope | Mode | Trạng thái tại snapshot | Entry |
|---|---|---|---|
| Mobile Work | `SKELETON_ONLY` | source phải inventory khi nhận task | `mobile-work/AGENTS.md` |
| Web Work | `SKELETON_ONLY` | source phải inventory khi nhận task | `web-work/AGENTS.md` |
| Work server | `DEEP` | `VERIFIED` foundation | `server-work/AGENTS.md` |
| Study server | `DEEP` | `DECLARED_NOT_RUNNABLE` | `server-study/AGENTS.md` |
| AI server | `DEEP` | runtime chat `VERIFIED`, copied core `UNWIRED` | `server-ai/AGENTS.md` |

Machine-readable registry: `.agents/context-manifest.json`.

## Global context

- `project/source-status.md`: source/DD/schema/context status và blocker.
- `project/architecture.md`: ownership/deployable boundaries.
- `project/conventions.md`: convention/workflow dùng chung.
- `project/dependencies.md`: dependency map qua app/contract/external system.
- `project/database.md`: database source hiện còn trong working tree.
- `project/business-code.md`: cách tra business code/HTTP mapping.

## Nhãn trạng thái

- `VERIFIED`: đọc trực tiếp từ source hiện tại và wiring có bằng chứng.
- `DECLARED_NOT_RUNNABLE`: declaration tồn tại nhưng import/composition hiện chặn runtime.
- `UNWIRED`: implementation tồn tại nhưng runtime không đăng ký/gọi.
- `EMPTY_PLACEHOLDER`: file/module tồn tại nhưng chưa có logic.
- `SKELETON_ONLY`: chỉ router/placeholder; phải inventory source khi nhận task.
- `NOT_FOUND` / `SOURCE_REQUIRED`: thiếu nguồn, không được đoán.
- `SOURCE_CHANGED` / `CONTEXT_STALE`: tracked source đã đổi sau snapshot.

## Bảo trì

Sau thay đổi làm đổi architecture, endpoint, important function contract, database, external dependency, business code, convention hoặc test flow, cập nhật đúng page scope. Không copy cùng một mô tả sang nhiều page; page API/module link tới core/service dùng chung.

Chạy:

```bash
node scripts/validate-agent-context.mjs
```

Validator kiểm tra registry, legacy conflicts và source drift của các deep scope.
