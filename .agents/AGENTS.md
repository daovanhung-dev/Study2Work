# AGENTS context index

Source snapshot gốc cho deep-context: `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4` (2026-09-18). Context phải mô tả source hiện tại; validator theo dõi drift sau snapshot.

## Scope registry

| Scope | Mode | Trạng thái tại snapshot | Entry |
|---|---|---|---|
| Mobile Work | `DEEP` | `SOURCE_BACKED` direct Neon/SQLite Flutter apps | `mobile-work/AGENTS.md` |
| Web Work | `DEEP` | `VERIFIED_REACT_EXPRESS_SPLIT` relative `/api/v1` client | `web-work/AGENTS.md` |
| Work server | `DEEP` | `VERIFIED_EXPRESS_JSON_API` | `server-work/AGENTS.md` |
| Study server | `DEEP` | `SOURCE_BACKED_WITH_TEST_BLOCKER` | `server-study/AGENTS.md` |
| AI server | `DEEP` | runtime chat `VERIFIED`, copied core `UNWIRED` | `server-ai/AGENTS.md` |
| DB Admin | `DEEP` | local Angular + FastAPI deployables `VERIFIED` | `db-admin/AGENTS.md` |

Machine-readable registry: `.agents/context-manifest.json`.

## Global context

Global index: `project/INDEX.md`.

- `project/design.md`: nguồn chuẩn design system và UX cho Work Web/Mobile.
- `project/source-status.md`: source/DD/schema/context status và blocker.
- `project/architecture.md`: ownership/deployable boundaries.
- `project/conventions.md`: convention/workflow dùng chung.
- `project/dependencies.md`: dependency map qua app/contract/external system.
- `project/database.md`: database source hiện còn trong working tree.
- `project/business-code.md`: cách tra business code/HTTP mapping.
- `project/contracts.md`: producer/consumer/status của shared và local contracts.
- `project/workflows.md`: workflow chung và verification order.
- `skills/INDEX.md`: skill registry và resource của `createDD-markdown`.
- `worklog/README.md`: worklog contract bắt buộc cho mọi task.
- `db-admin/AGENTS.md`: ownership, API safety boundary và verified commands của Neon DB Admin.

Mỗi scope có `INDEX.md` làm page graph. Không tạo context agent trong `apps/`;
root router luôn trỏ về các entry dưới `.agents/`.

## Nhãn trạng thái

- `VERIFIED`: đọc trực tiếp từ source hiện tại và wiring có bằng chứng.
- `DECLARED_NOT_RUNNABLE`: declaration tồn tại nhưng import/composition hiện chặn runtime.
- `UNWIRED`: implementation tồn tại nhưng runtime không đăng ký/gọi.
- `EMPTY_PLACEHOLDER`: file/module tồn tại nhưng chưa có logic.
- `SKELETON_ONLY`: chỉ router/placeholder; phải inventory source khi nhận task.
- `NOT_FOUND` / `SOURCE_REQUIRED`: thiếu nguồn, không được đoán.
- `SOURCE_CHANGED` / `CONTEXT_STALE`: tracked source đã đổi sau snapshot.
- `EXPECTED_BEHAVIOR`: requirement/canonical contract/approved DD.
- `CURRENT_BEHAVIOR`: current source, runnable tests và executable config.
- `DISCREPANCY`: expected và current behavior chưa khớp; không tự reconcile.

## Bảo trì

Sau thay đổi làm đổi architecture, endpoint, important function contract, database, external dependency, business code, convention hoặc test flow, cập nhật đúng page scope. Không copy cùng một mô tả sang nhiều page; page API/module link tới core/service dùng chung.

Chạy:

```bash
node scripts/validate-agent-context.mjs
```

Validator kiểm tra registry, legacy conflicts và source drift của các deep scope.
Validator cũng kiểm tra skill/resource, workflow, contract, subcontext, worklog
required fields và generated/cache directory exclusions.
