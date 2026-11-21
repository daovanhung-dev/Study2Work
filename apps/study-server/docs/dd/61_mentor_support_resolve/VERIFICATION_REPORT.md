# VERIFICATION_REPORT — Study API #61

## Kết quả

- DD status: `Draft — Needs Confirmation`.
- Local runtime: `SOURCE_BACKED_WITH_DERIVED_CHOICES`; route, module and HTTP tests are present.
- Live schema/deployment: `NOT_VERIFIED`; only checked-in migration/DDL and fake DB tests were inspected.
- Scope: API #61 route/module/tests, its DD package, direct server-study context/manifest and worklog. Existing unrelated worktree changes remain untouched.

## Deliverable manifest

| Nhóm | Kết quả |
|---|---|
| Sheets | Đủ 8 file đăng ký: `00_Cover.md` đến `07_table.md`. |
| Reports | `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`. |
| Tổng | 11 Markdown files; không tạo ZIP theo Study workflow. |

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Source precedence | AC-24 diagram → migration 008/`DB.sql` → API catalog reviewed; V1-PILOT UUID conflict recorded. | PASS |
| Local fallback | BIGINT request, course owner, active-state set, retry and DB timestamp are labeled DERIVED. | PASS |
| Template appendix | All eight sheet appendices match the registered template appendix byte-for-byte. | PASS |
| API contract | PATCH path, Mentor Bearer, int64, no body/query, 200 updated, singleton SupportRequest and exact 401/403/404/422/500 retained. | PASS |
| Focused regression | #59, #60, #61: `47 passed`, one upstream Starlette/httpx deprecation warning. | PASS |
| Full Study suite | `597 passed`, one upstream Starlette/httpx TestClient deprecation warning. | PASS |
| Ruff | API #61 module/tests, router and middleware: all checks passed. | PASS |
| OpenAPI composition | 31 `/api/v1` path templates, 32 operations; #61 is PATCH, signed-int64 path and no request body. | PASS |
| Context manifest paths | Six #61 runtime/test paths are registered and exist. | PASS |
| Context validator | Node is unavailable. Deno `--skip-drift` reports only pre-existing missing DB Admin context/source; full Deno run also reports broad source drift in the already dirty workspace. | BASELINE_FAILURE_OUT_OF_SCOPE |
| DD links/JSON/markdown | Eight sheets, 28 local file links and two JSON examples checked; no errors or unclosed fences. | PASS |
| `git diff --check` | No whitespace errors. | PASS |

## Remaining boundaries

- `OPEN`, `IN_PROGRESS`, `WAITING_LEARNER` transition, resolved retry behavior, `CANCELLED` 422 and `resolved_at` timestamp are DERIVED choices, not business-owner approval.
- Migration 008 is not evidence of live schema or deployment.
- Fake-DB tests do not prove live PostgreSQL locking/concurrency or storage URL reachability.
- #58 collection-versus-singleton catalog discrepancy remains open and unchanged.

See [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) and [PLAN_RESULT.md](./PLAN_RESULT.md#macro-review-ac-24-58-61).
