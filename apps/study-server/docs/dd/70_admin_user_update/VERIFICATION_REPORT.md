# Báo cáo kiểm chứng — API #70

- DD status: `Draft — Needs Confirmation`.
- Endpoint: `PUT /api/v1/admin/users/{user_id}`.
- Runtime status: `SOURCE_BACKED_WITH_DERIVED_CONTRACT` — route, Admin guard, module và focused HTTP tests hiện có trong Study source.
- Direct contract: Bearer JWT/Admin, `user_id:int64`, `ApiEnvelope<UserProfile>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`; đúng errors 401/403/404/422/500.
- Body, full-replacement semantics, ba role label và target legacy `users` là quyết định triển khai DERIVED. Catalog/diagram chưa khai báo body; live schema và policy chưa được xác minh.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector `coding --limit 3` chọn và đã đọc đủ worklog #34/#47/#48; không thiếu worklog. | PASS |
| Plan trước runtime | Source trace, discrepancy table và implementation plan được ghi trong worklog trước khi sửa source. | PASS |
| Catalog, diagram và sibling APIs | Đối chiếu API #70, AC-31 update branch, API #14 profile precedent và ranh giới #71 status/#72 delete. | PASS — STATIC |
| Legacy schema và current source | Bound UPDATE dùng legacy BIGINT `users`; V1-PILOT UUID và live schema không được xem là tương thích/đã triển khai. | PASS — STATIC |
| Focused HTTP tests | `19 passed`; auth order, strict body, normalization, path, 404, mapping, rollback, trace và OpenAPI được kiểm tra bằng fake DB session. | PASS |
| Full Study suite | `770 passed, 1 warning` trong `.venv`; warning là upstream Starlette/httpx TestClient deprecation. | PASS |
| Ruff | `./.venv/bin/ruff check app tests` — All checks passed. | PASS |
| OpenAPI/import | App compose thành công; 39 API path templates, 41 operations. PUT dùng đúng path/body fields, Authorization và response codes 200/401/403/404/422/500. | PASS |
| DD package/static | Có đủ 11 file; fenced blocks cân bằng, JSON examples parse, relative links resolve; 8/8 appendix suffixes byte-equal với `HEAD`. | PASS — STATIC |
| AC-31 macro-review | #68–#72 hiện có route/module/focused HTTP tests; #72 fallback soft-delete và policy vẫn DERIVED/open. Các quyền, PII/audit, schema và lifecycle gaps vẫn mở. | VERIFIED_WITH_OPEN_QUESTIONS |
| `git diff --check` | Không có diagnostics. | PASS |
| Context validator `--skip-drift` | Exit 1 với 43 chẩn đoán hiện có trong scope DB Admin bị thiếu; không báo lỗi cấu trúc riêng cho Study. | BASELINE_INVALID |
| Context validator mặc định | Exit 1 với cùng lỗi DB Admin và `CONTEXT_STALE` cho server-study, server-work, web-work (kể cả hai subscopes), mobile-work và db-admin do snapshot/source drift hiện có. | BASELINE_INVALID_AND_STALE |
| Live DB/deployment | Không kiểm tra; fake DB tests và DDL trong checkout không chứng minh live schema hoặc migration deployment. | NOT_VERIFIED |

## AC-31 group macro-review

Status: `VERIFIED_WITH_OPEN_QUESTIONS` — document-level review of APIs #68–#72.

- #68 list response dùng `ApiEnvelope<Page<UserProfile>>`; page/filter semantics vẫn DERIVED.
- #69 detail và #70 update dùng safe `UserProfile` fields từ API #04 và bỏ `bio` chưa có source mapping.
- #70 cập nhật profile/role; #71 sở hữu account status/session effect; #72 sở hữu delete/anonymization. Các mutation vẫn tách biệt.
- #70 body, role transition, live schema, Admin permission, PII/audit, access-token invalidation và deleted-user visibility chưa có quyết định nguồn được duyệt.
- #72 hiện dùng `status=DELETED`, trả `updated_at` như `deleted_at`, giữ dependent rows và trả 404 khi lặp; các quyết định này DERIVED, chưa được policy owner duyệt.
- API #68–#72 có local route/module/focused HTTP tests. Fake-session tests không xác minh PostgreSQL, deployment hoặc approval của policy. Fake-session tests không xác minh PostgreSQL hoặc deployment.

## Open status

Các policy gaps tiếp tục được liệt kê trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md). Implementation giữ body/role fallback ở trạng thái DERIVED; cần xác nhận contract và live schema trước khi coi DD hoặc deployment là approved.
