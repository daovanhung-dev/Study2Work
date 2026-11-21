# Kết quả plan — API #72

## Phạm vi

Triển khai `DELETE /api/v1/admin/users/{user_id}` theo catalog/AC-31, với fallback đơn giản nhất có thể thực hiện từ source local mà không thêm schema: soft-delete bằng `users.status='DELETED'`. Đồng bộ API #72 DD, current-state review của #69/#70, canonical server-study context, manifest và worklog. Không sửa catalog, diagram, DDL hoặc migration; giữ tất cả dirty changes có trước task.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Phân loại/context | `coding`, secondary `test/docs`, scope `server-study`; đọc root/context map, scope pages và preflight worklog trước inspect sâu. |
| Worklog preflight | Deno selector tìm thấy 65 coding logs; đọc đủ #34/#47/#48 trước khi lập plan. |
| Source trace | Đối chiếu API #72 DD/catalog, AC-31, legacy BIGINT DDL, V1-PILOT UUID model, API #03, #53, #68–#71, middleware, response helper và test conventions. |
| Plan trước code | Ghi expected/current behavior, discrepancy/fallbacks và 10 bước implementation trong worklog trước runtime edit. |
| Implementation | Tạo module API #72, wire DELETE trên path hiện có, ADMIN guard trước parse/DB, strict signed-int64 validation, transactional soft-delete và safe `DeleteResult`. |
| Focused/regression | API #72: 11 passed. API #03 + Admin #68–#72 linked regression: 95 passed. |
| Full verification | Full Study suite: 806 passed; Ruff sạch; OpenAPI introspection: 40 unique `/api/v1` paths, 43 operations. |
| Documentation/context | Cập nhật 8 DD sheets, 3 reports, sibling macro-review, server-study context, project source status, manifest và worklog. Excel appendix suffixes của 8 sheets được giữ nguyên byte-for-byte. |

## Quyết định triển khai

- `DELETE` dùng một conditional UPDATE trên legacy `users`: đặt `status='DELETED'`, `updated_at=CURRENT_TIMESTAMP`, trả `id` và `updated_at AS deleted_at`.
- Marker, response timestamp alias và 404 cho lần lặp là fallback `DERIVED`; không có migration/cột mới hoặc hard delete/anonymization/cascade.
- Giữ tất cả user-linked rows. API #03 chặn login/refresh cho non-ACTIVE; access JWT đang tồn tại không bị revoke.
- Shared `ADMIN` guard được dùng theo API #68–#71. Self/last-admin, tenant/MFA, PII retention/anonymization, audit và live schema policy vẫn cần owner xác nhận.
- DD giữ `Draft — Needs Confirmation`; không gọi local fallback là policy đã duyệt.

## AC-31 macro-review

**Status: VERIFIED_WITH_OPEN_QUESTIONS — document/source review; live policy/schema chưa xác nhận.**

- #68 list, #69 detail, #70 profile/role update, #71 ACTIVE/SUSPENDED transition và #72 soft-delete là các handler riêng; #72 không sửa sibling mutation.
- #68/#69 hiện không filter DELETED; #70 giữ nguyên status; #71 từ chối current status ngoài ACTIVE/SUSPENDED. API #03 login/refresh từ chối DELETED; access JWT chưa hết hạn có thể còn dùng.
- Shared ADMIN JWT mapping là local fallback; dedicated permission, tenant/MFA, PII/audit và self/last-admin policy còn mở.
- Legacy BIGINT candidate và V1-PILOT UUID schema giữ tách biệt. Fake DB tests không chứng minh live schema, migration deployment hoặc production authorization.

## Trạng thái

Local implementation và test evidence đã hoàn tất. DD vẫn `Draft — Needs Confirmation` cho tới khi owner xác nhận policy, timestamp persistence, dependency/retention, retry, session revocation và Admin safeguards trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
