# Báo cáo kiểm chứng — API #79

- DD status: `Draft — Needs Confirmation`.
- Endpoint: `GET /api/v1/admin/content/{content_id}`.
- Runtime status: `SOURCE_BACKED_LOCALLY / WIRED` — route, module, shared ADMIN guard, middleware path template và focused HTTP tests nằm trong Study source hiện tại.
- Direct contract: Bearer/Admin; path `content_id:int64!`; không body/query; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, response `ApiEnvelope<Content>`; đúng bốn lỗi catalog 401/403/404/500.
- AC-33 sequence: #78 queue → #79 detail reads `content/version/author` → #80 approve hoặc #81 reject → reload queue.
- Main discrepancy: diagram yêu cầu version/author reads nhưng response Content không có field đó. Runtime trả đúng tám Content fields; không truy vấn snapshot version hoặc suy luận author.
- Local source mapping: active row trong checked-in legacy `contents` candidate, bind theo ID; soft-deleted/missing rows trả 404. Checked-in DDL/current source không chứng minh live schema/deployment.
- Query/projection failure trả safe 500 và rollback. API #79 không commit/mutate.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Deno selector chọn #74/#75/#76; đọc cả ba và thêm API #78 worklog trước source review. | PASS |
| Plan trước implementation | Classification, source trace, discrepancy và detailed plan được ghi trong worklog trước sửa code/DD/context. | PASS |
| Catalog/diagram/schema/source | Đối chiếu catalog #79/reusable Content, toàn bộ AC-33 flow, legacy DDL/migrations 006/007, APIs #49–#53/#69/#78 và #80/#81 boundary. | PASS — STATIC |
| Direct contract/error set | Giữ singleton `ApiEnvelope<Content>`, đúng path/auth/input và đúng 401/403/404/500. | PASS |
| Content projection | Đủ tám field; current status được trả như đã lưu; version/author không được thêm. | PASS_WITH_OPEN_QUESTIONS |
| Focused API #79 tests | `13 passed`; auth order, path, row mapping, rollback, read-only, route precedence và OpenAPI. | PASS |
| Linked regression | #49–#53/#78/#79: `149 passed`. | PASS |
| Full Study suite | `946 passed`; một upstream Starlette/httpx deprecation warning. | PASS |
| Ruff | `ruff check app tests` — all checks passed. | PASS |
| OpenAPI | 45 unique `/api/v1` path templates / 50 operations; #78 static route và #79 dynamic detail đều hiện diện. | PASS |
| Package | Đúng 11 Markdown files: 8 template sheets + 3 reports; không có ZIP. | PASS — STATIC |
| Template appendices | 8/8 appendix suffix giữ nguyên byte so với registered template. | PASS — STATIC |
| JSON/tables/fences | 2/2 JSON examples parse; 165 authored Markdown tables ngoài appendix/report; 5 code fences cân bằng. | PASS — STATIC |
| Links/anchors/whitespace | 32 local links và 16 anchors resolve; final newline có mặt, không trailing whitespace. | PASS — STATIC |
| Fingerprints | Template pack và DD payload SHA-256 được ghi bên dưới; payload không gồm report này. | RECORDED |
| Context manifest/pages | Thêm 6 required source paths; route/runtime/database/security/module/test/workflow/status pages cập nhật cho API #79. | PASS — STATIC |
| Context validator | `deno run -A scripts/validate-agent-context.mjs --skip-drift`; chỉ báo các entry/source root DB Admin thiếu trong checkout, không báo lỗi Study Server. | BLOCKED_OUT_OF_SCOPE_BASELINE |

## Fingerprints

| Fingerprint | Phạm vi | SHA-256 |
|---|---|---|
| Registered template pack | 8 tên file đã sort + NUL + raw bytes + NUL | `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137` |
| DD output payload | 8 sheets + `OPEN_QUESTIONS.md` + `PLAN_RESULT.md`; không gồm report này | `93b3b470233c1087ac8c322b1e4e24a83f1766b229300c6025ee2b12c1b28195` |

## Giới hạn kết luận

Kiểm tra source và fake-DB HTTP tests xác nhận local route, contract projection và transaction/error handling. Chúng không xác minh live PostgreSQL schema, migration deployment, Admin moderation policy hoặc việc API #80/#81 quyết định trên cùng một revision. AC-33 version/author projection và revision identity vẫn cần product/schema owner xác nhận.
