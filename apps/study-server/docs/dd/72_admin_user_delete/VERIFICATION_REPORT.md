# Báo cáo kiểm chứng — API #72

- DD status: `Draft — Needs Confirmation`.
- Endpoint: `DELETE /api/v1/admin/users/{user_id}`.
- Runtime status: `SOURCE_BACKED_WITH_DERIVED_CONTRACT` — route, module, ADMIN guard và focused HTTP tests có trong local Study source.
- Direct contract: Bearer JWT/Admin, path `user_id:int64!`, `ApiEnvelope<DeleteResult>`, HTTP 200 `DESIGN_RESOURCE_DELETED`; errors 401/403/404/422/500.
- Local fallback: conditional soft-delete bằng `users.status='DELETED'`, `updated_at=CURRENT_TIMESTAMP`, response `deleted_at` lấy từ timestamp update; không thêm schema, không hard-delete/anonymize/cascade. Đây là lựa chọn DERIVED, chưa được policy owner xác nhận.
- Session boundary: API #03 login/refresh từ chối non-ACTIVE; access JWT đã cấp có thể còn hiệu lực đến expiry. Live schema, migration deployment, Admin policy và production behavior chưa xác minh.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector `coding --limit 3` tìm 65 logs; đã đọc đủ #34/#47/#48. | PASS |
| Plan trước code | Source trace, discrepancies và implementation plan được ghi trong worklog trước runtime edit. | PASS |
| Catalog/diagram/schema | API #72, DeleteResult, AC-31, legacy BIGINT DDL và tách biệt V1-PILOT UUID được đối chiếu. | PASS — STATIC |
| Focused API #72 | 11 HTTP tests passed; success, missing/repeat 404, validation, auth order, safe projection, rollback và OpenAPI. | PASS |
| Linked regression | API #03 + Admin #68–#72: 95 tests passed. | PASS |
| Full Study suite | 806 passed; một upstream Starlette/httpx TestClient deprecation warning. | PASS |
| Ruff | `./.venv/bin/ruff check app tests` — All checks passed. | PASS |
| OpenAPI | 40 unique `/api/v1` path templates, 43 operations; DELETE shares `/admin/users/{user_id}` with GET/PUT and declares expected path/header/error contract. | PASS — LOCAL IMPORT |
| DD package | 8 sheets + 3 reports; Excel appendix suffixes of 8 sheets preserved byte-for-byte. | PASS — STATIC |
| DD Markdown/JSON/links | Static checks recorded after authoring; JSON examples parse, relative links resolve, fences balance and no trailing whitespace. | PASS — STATIC |
| AC-31 macro-review | #68–#72 source/DD boundaries updated; outstanding approval questions retained. | VERIFIED_WITH_OPEN_QUESTIONS |
| Context validator `--skip-drift` | Expected existing DB Admin context/source/link diagnostics remain outside server-study scope. | PARTIAL — BASELINE |
| Context validator default | Also reports tracked worktree/source snapshot drift; snapshot commit was not changed to conceal it. | PARTIAL — BASELINE |
| Live DB/deployment | Not checked; local fake-session tests and checked-in DDL do not prove runtime metadata or deployment. | NOT_VERIFIED |

## AC-31 group macro-review

Status: `VERIFIED_WITH_OPEN_QUESTIONS` — local source and document review of APIs #68–#72.

- #68 list and #69 detail use safe profile projections; both currently include rows regardless of status.
- #70 owns profile/role update; #71 owns ACTIVE/SUSPENDED account status and conditional refresh-token revocation; #72 owns the DERIVED DELETED marker. These remain separate operations.
- API #03 blocks new login/refresh for DELETED; access-token guard does not query current status or revoke existing access JWTs.
- #72 preserves linked rows, does not anonymize PII, and maps response `deleted_at` to update timestamp without a dedicated deletion column. These are implementation fallbacks, not approved retention policy.
- Admin permission/tenant/MFA/self/last-admin/audit policy, live schema and deployment remain unverified.
- #68–#72 local route/module/HTTP evidence uses fake DB sessions; it does not confirm PostgreSQL behavior or deployed API behavior.

## Open status

Owner decisions remain in [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md). The endpoint is locally wired and tested; DD and policy remain Draft pending approval.
