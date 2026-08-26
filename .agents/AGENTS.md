# AGENTS context index

Snapshot kiểm tra: **2026-08-26**. Context này mô tả working tree hiện tại,
không khôi phục nội dung đã bị xóa và không coi Git history là runtime contract.

## Trạng thái scope

| Scope | Mức context | Entry |
|---|---|---|
| Mobile Work | `SKELETON_ONLY` theo yêu cầu | `mobile-work/AGENTS.md` |
| Web Work | `SKELETON_ONLY` theo yêu cầu | `web-work/AGENTS.md` |
| Work server | source-backed, function/API level | `server-work/AGENTS.md` |
| Study server | source-backed, gồm blocker hiện tại | `server-study/AGENTS.md` |
| AI server | source-backed, runtime và unwired core tách biệt | `server-ai/AGENTS.md` |

## Global context

- `project/source-status.md`: DD/schema/context status và discrepancy cần biết.
- `project/architecture.md`: bản đồ monorepo và ownership.
- `project/conventions.md`: convention/workflow dùng chung đã xác minh.
- `project/dependencies.md`: dependency map qua app/contract/external system.
- `project/database.md`: database source hiện còn trong working tree.
- `project/business-code.md`: cách tra và bảo trì code/HTTP mapping.

## Nhãn trạng thái

- `VERIFIED`: đọc trực tiếp từ source hiện tại.
- `DECLARED_NOT_RUNNABLE`: source có declaration nhưng app không thể đi tới nó.
- `UNWIRED`: implementation tồn tại nhưng runtime không đăng ký/gọi.
- `SKELETON_ONLY`: chỉ có router/placeholder; phải inventory source khi nhận task.
- `NOT_FOUND` hoặc `SOURCE_REQUIRED`: thiếu nguồn, không được đoán.
- `SOURCE_CHANGED` / `CONTEXT_STALE`: context cũ không còn khớp source.

## Bảo trì

Sau thay đổi code làm đổi architecture, endpoint, function public, database,
business code, external service, convention hoặc test flow, cập nhật đúng page
scope trong cùng task. Không copy một mô tả sang nhiều page; page module/API nên
link tới core/service dùng chung.
