# Báo cáo kiểm chứng — API #71

- DD status: `Draft — Needs Confirmation`.
- Endpoint: `PATCH /api/v1/admin/users/{user_id}/status`.
- Runtime status: `SOURCE_BACKED_WITH_DERIVED_CONTRACT` — route, shared ADMIN guard, module và focused HTTP tests đã được wire trong Study source.
- Direct contract: Bearer JWT/Admin, `user_id:int64`, `ApiEnvelope<UserProfile>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`; đúng errors 401/403/404/422/500.
- Body `{status}`, ACTIVE/SUSPENDED allowlist, current-state gate, legacy target và conditional refresh-token revoke là fallback `DERIVED`; live schema và policy chưa được xác minh.
- Access JWT đã phát hành có thể còn hiệu lực đến expiry vì shared access-token guard không đọc `users.status` hoặc token revocation.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Coding worklog preflight | Selector chọn/đã đọc đủ #34/#47/#48; không thiếu worklog. | PASS |
| Plan trước code | Source trace, discrepancies và transaction/route/test plan được ghi trong worklog trước runtime edits. | PASS |
| Catalog, diagram và linked source | Đối chiếu API #71, AC-31 STATUS branch, API #03 login/refresh, API #04 `UserProfile`, APIs #68–#70, middleware, legacy và V1-PILOT DDL. | PASS — SOURCE REVIEW |
| Focused API #71 suite | 21 HTTP tests passed; fake DB session và một upstream Starlette/httpx TestClient deprecation warning. | PASS |
| Linked API #03/#68–#71 regression | 80 tests passed; một upstream deprecation warning. | PASS |
| Full Study suite | 791 tests passed; một upstream Starlette/httpx TestClient deprecation warning. | PASS |
| Ruff | `./.venv/bin/ruff check app tests` — all checks passed. | PASS |
| OpenAPI/import | 40 `/api/v1` path templates, 42 operations; API #71 declares required int64 path, Authorization, required body and exact 200/401/403/404/422/500 response set. | PASS |
| DD package | 9 sheets (8 template sheets plus separate `refresh_tokens` mapping) and 3 reports; 8 original Excel appendix suffixes retained. | PASS — STATIC |
| DD Markdown/JSON/links | 12 Markdown files; JSON examples parse, relative links resolve, fences cân bằng, không có trailing whitespace; 8 appendix suffixes khớp các sheet API #70. | PASS — STATIC |
| AC-31 macro-review | #68–#72 have local route/module/focused HTTP tests; #72 uses a DERIVED soft-delete marker. Mutation boundaries and unresolved policy/schema questions are retained. | VERIFIED_WITH_OPEN_QUESTIONS |
| Context manifest | Sáu API #71 module/test paths đã đăng ký và đều tồn tại; JSON parse thành công. | PASS — STATIC |
| Context validator `--skip-drift` | Exit 1 với 43 diagnostics thiếu context/source/links của DB Admin ngoài scope; không có lỗi Study riêng. | BASELINE_INVALID — OUT OF SCOPE |
| Context validator mặc định | Exit 1 với cùng 43 diagnostics DB Admin và `CONTEXT_STALE` ở 7 scope do source/worktree drift hiện có; không đổi `sourceCommit` để che drift. | BASELINE_INVALID_AND_STALE |
| `git diff --check` | Không có diagnostics. | PASS |
| Live DB/deployment | Không kiểm tra; fake DB tests và checked-in DDL không chứng minh live schema hoặc migration deployment. | NOT_VERIFIED |

## AC-31 group macro-review

Status: `VERIFIED_WITH_OPEN_QUESTIONS` — document-level review of APIs #68–#72.

- #68 list trả `ApiEnvelope<Page<UserProfile>>`; #69 đọc một `UserProfile`; #70 cập nhật profile/role; #71 cập nhật status và có conditional refresh-token effect; #72 giữ delete/anonymization intent. Các mutation không overlap.
- #68–#72 có route/module/focused HTTP tests local. #72 dùng fallback `status=DELETED`, response `updated_at` alias và 404 khi lặp; đây là behavior DERIVED, chưa có owner approval hoặc live schema evidence.
- Body/status policy của #71, dedicated Admin permission/tenant/MFA, live schema, PII/audit, lifecycle visibility, immediate access-token invalidation và delete persistence vẫn là câu hỏi mở.
- Legacy user-linked relations chỉ là DDL context; không suy ra cascade, blanket dependency block hoặc hard-delete rule.
- Fake-session tests không xác minh PostgreSQL/live schema, migration deployment hoặc policy ngoài ứng dụng.

## Open status

Các quyết định fallback và câu hỏi approval còn lại nằm trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md). Runtime có bằng chứng local; DD không được nâng thành approved contract.
