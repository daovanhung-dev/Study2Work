# Báo cáo kiểm chứng — API #68

- DD status: Draft — Needs Confirmation; runtime implementation is source-backed with DERIVED contract/schema rules.
- Endpoint: `GET /api/v1/admin/users`.
- Response: `ApiEnvelope<Page<UserProfile>>`, synchronized in catalog and AC-31 diagram.
- Source target: checked-in legacy BIGINT `users` candidate; live schema/deployment not verified.

## Verification

| Check | Kết quả | Trạng thái |
|---|---|---|
| Coding worklog preflight | Selector found 61 coding worklogs; selected and read #34/#47/#48, plus prior API #68 DD worklog. | PASS |
| Plan before code | Source trace, discrepancies and 11-step implementation plan were written before runtime edits. | PASS |
| Focused API #68 suite | 15 TestClient tests passed; fake DB sessions, one upstream Starlette/httpx deprecation warning. | PASS |
| Full Study suite | `738 passed, 1 warning in 31.62s`. | PASS |
| Ruff | `./.venv/bin/ruff check app tests` — all checks passed. | PASS |
| OpenAPI | 38 `/api/v1` paths and 39 operations; API #68 has role/status/keyword/page query parameters, required Authorization, and 200/401/403/422/500 responses. | PASS |
| Contract synchronization | Catalog row #68 and AC-31 node specify `ApiEnvelope<Page<UserProfile>>` and 422 page validation. | PASS — SOURCE REVIEW |
| DD package | 8 numbered sheets plus 3 reports; all 8 Excel appendix suffixes match pre-edit `HEAD` byte-for-byte. | PASS |
| AC-31 sibling references | Updated stale #69–#72 statements that described the #68 response mismatch as unresolved; kept lifecycle, PII/audit and schema questions open. | PASS — STATIC REVIEW |
| `git diff --check` | No diagnostics. | PASS |
| Context validator `--skip-drift` | Study context paths passed; validation still fails on missing DB Admin context/source roots and links outside this task's scope. | PARTIAL — BASELINE |
| Context validator default | Also reports `CONTEXT_STALE` for existing tracked changes in Study and other scopes, plus the same missing DB Admin context/source paths. No source commit was changed to hide worktree drift. | PARTIAL — WORKTREE BASELINE |

## Derived behavior and limits

- Fixed page size 20, default page 1, `id ASC`, exact role/status, and case-insensitive literal substring keyword across `full_name`/`email` are DERIVED implementation choices.
- The shared `ADMIN` claim is the local authorization fallback; no Admin permission relation or tenant boundary exists in checked-in DDL.
- Runtime reuses API #04's safe profile projection, omits unsupported `bio`, and never queries `password_hash`.
- Tests use fake database rows. They do not prove the target schema, migration/deployment state, PII policy, Admin permission policy, or delete visibility in a live environment.
