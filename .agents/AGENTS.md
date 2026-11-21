# AGENTS context index

Source snapshot gốc cho deep-context: `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4` (2026-09-18). Context phải mô tả source hiện tại; validator theo dõi drift sau snapshot.

## Scope registry

| Scope | Mode | Trạng thái tại snapshot | Entry |
|---|---|---|---|
| Mobile Work | `DEEP` | `SOURCE_BACKED` direct Neon/SQLite Flutter apps; exhaustive tracked-file inventory | `mobile-work/AGENTS.md` |
| Web Work | `DEEP` | `VERIFIED_REACT_EXPRESS_SPLIT` relative `/api/v1` client | `web-work/AGENTS.md` |
| Work server | `DEEP` | `VERIFIED_EXPRESS_JSON_API` | `server-work/AGENTS.md` |
| Study server | `DEEP` | `SOURCE_BACKED` | `server-study/AGENTS.md` |
| AI server | `DEEP` | runtime chat `VERIFIED`, copied core `UNWIRED` | `server-ai/AGENTS.md` |
| DB Admin | `DEEP` | local Angular + FastAPI deployables `VERIFIED` | `db-admin/AGENTS.md` |

Machine-readable registry: `.agents/context-manifest.json`.

Human-readable context map: [`context-map.md`](context-map.md). The map explains
the load tree and registry relationships; it does not replace the manifest.
After reading this registry, every task must read `context-map.md` before
choosing a scope or subcontext.

## Global context

Global index: `project/INDEX.md`.

**Agent Control bắt buộc cho mọi scope:** đọc và áp dụng
[`project/agent-control.md`](project/agent-control.md) cho mọi task. Tiến độ
đang hoạt động chỉ được ghi trong [`.agents/target.md`](target.md), theo đúng
ba cột đã định nghĩa. Worklog lưu bằng chứng, không thay thế target tracker.

- `project/design.md`: nguồn chuẩn design system và UX cho Work Web/Mobile.
- `project/source-status.md`: source/DD/schema/context status và blocker.
- `project/architecture.md`: ownership/deployable boundaries.
- `project/conventions.md`: convention/workflow dùng chung.
- `project/dependencies.md`: dependency map qua app/contract/external system.
- `project/database.md`: database source hiện còn trong working tree.
- `project/business-code.md`: cách tra business code/HTTP mapping.
- `project/contracts.md`: producer/consumer/status của shared và local contracts.
- `project/workflows.md`: workflow chung và verification order.
- `project/agent-control.md`: quy tắc target, thực thi im lặng, bằng chứng và
  an toàn áp dụng cho mọi scope.
- `skills/INDEX.md`: skill registry và resource của `create-dd-from-bd-mobile`
  (Mobile module DD), `createDD-markdown` (Web/API DD), và `code-review`
  (read-only review across all code scopes).
- `worklog/README.md`: worklog contract và preflight đọc các worklog cùng type bắt buộc cho mọi task.
- `db-admin/AGENTS.md`: ownership, API safety boundary và verified commands của Neon DB Admin.

Mỗi scope có `INDEX.md` làm page graph. Không tạo context agent trong `apps/`;
root router luôn trỏ về các entry dưới `.agents/`.

## Quy tắc target và giao tiếp (mọi task)

- `.agents/target.md` là nguồn tiến độ duy nhất cho target đang hoạt động. File
  chỉ chứa bảng `STT | Tên target | Tiến độ hoàn thiện`; không thêm mô tả,
  milestone, lịch sử hay cột khác.
- Mỗi target độc lập, rõ nghĩa, bắt đầu ở `0%`; cập nhật phần trăm khi bằng
  chứng xác minh làm thay đổi tiến độ. Giữ nguyên tiến độ đã xác minh khi bị
  chặn. Khi hoàn thành, ghi bằng chứng vào worklog rồi xóa hàng `100%`.
- Worklog ghi phân loại, nguồn đã đọc, thay đổi, xác minh và `TARGET_UPDATES`;
  không lưu bảng `MILESTONES` hoặc bản sao tiến độ.
- Không tự gửi tiến độ, Event receipt, milestone, tổng kết đọc/thao tác hoặc
  báo cáo hoàn tất vào chat. Chỉ phản hồi câu hỏi của người dùng, yêu cầu làm
  rõ blocker, hoặc yêu cầu bắt buộc từ quy tắc cấp cao hơn.

Quy tắc này không thể ghi đè system/developer, bảo mật, quyền hạn hoặc giới
hạn công cụ. `.agents/project/workflows.md` và
`.agents/worklog/README.md` quy định luồng thực hiện và bằng chứng.

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

Mọi task phải chạy worklog preflight sau khi xác định `primary_task_type`, đọc
các log selector trả về trước khi inspect sâu hoặc sửa file, rồi ghi bằng chứng
vào `PRIOR_WORKLOG_REVIEW`. Worklog canonical nằm dưới
`.agents/worklog/YYYY-MM-DD/`; `docs/devs/worklogs` là legacy path và không còn
là nguồn đọc mới.

Chạy:

```bash
node scripts/validate-agent-context.mjs
```

Validator kiểm tra registry, legacy conflicts và source drift của các deep scope.
Validator cũng kiểm tra skill/resource, workflow, contract, subcontext, worklog
required fields, context-map coverage và generated/cache directory exclusions.
