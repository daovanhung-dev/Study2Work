# Báo cáo kiểm chứng — API #78

- DD status: `Draft — Needs Confirmation`.
- Endpoint: `GET /api/v1/admin/content/pending`.
- Runtime status: `SOURCE_BACKED_LOCALLY / WIRED` — route, shared ADMIN guard, module, middleware contract path và focused HTTP tests hiện có.
- Direct catalog/diagram: Bearer/Admin; `type?:string`, `course?:int64`, `page?:int32`; response `ApiEnvelope<Content>`; HTTP 200 cùng lỗi 401/403/500.
- Local fallback: `ApiEnvelope<Page<Content>>`, page 1 mặc định, size 20, `id ASC`, exact filters, active rows only và empty/out-of-range Page trả 200. Các lựa chọn này là `DERIVED`; discrepancy singular-vs-collection được giữ nguyên trong DD, không sửa catalog/diagram.
- Candidate source: current checked-in legacy `contents`; không đọc `content_versions`, không thêm DDL/migration. Đây không phải xác nhận live schema hoặc migration deployment.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector `coding --limit 3` chọn và đã đọc worklog #74/#75/#76; không thiếu log. Plan chi tiết được ghi trước implementation. | PASS |
| Source order | Đọc AC-33 diagram/index → legacy DDL/migrations và current APIs #49–#53 → catalog/reusable Content → DD #78 và linked #79–#81. | PASS — STATIC |
| Focused HTTP tests | API #78: 23 passed. | PASS |
| Linked regression | APIs #49–#53, #73 và #78: 160 passed. | PASS |
| Full Study suite | 933 passed; một upstream Starlette/httpx TestClient deprecation warning. | PASS |
| Ruff | `.venv/bin/ruff check app tests` cùng các file API #78: all checks passed. | PASS |
| OpenAPI | 44 unique `/api/v1` path templates, 49 operations; #78 có GET operation. | PASS |
| DD package | 11 Markdown files: 8 template sheets và 3 reports; không có ZIP. | PASS — STATIC |
| Template appendices | 8/8 sheet có appendix suffix khớp byte-for-byte template đã đăng ký. | PASS — STATIC |
| JSON/table/markup | 3/3 fenced JSON examples parse; 21 Markdown table blocks trong phần authoring; code fences cân bằng; không trailing whitespace và có final newline. | PASS — STATIC |
| Links/anchors | 42 local Markdown links và 19 fragment references; tất cả file/anchor đích resolve. | PASS — STATIC |
| Context validator | Chỉ báo các trang/source DB Admin thiếu ngoài Study: `.agents/db-admin/*`, `apps/db-admin-web/`, `apps/db-admin-server/`. Không có lỗi Study Server trong output. | BASELINE OUTSIDE SCOPE |
| Live database | Không kết nối/kiểm chứng live PostgreSQL, schema, grants hoặc migration deployment. Tests dùng fake DB sessions. | NOT VERIFIED |

## Fingerprints

| Fingerprint | Phạm vi | SHA-256 |
|---|---|---|
| Registered template pack | 8 tên file đã sort + NUL + raw bytes + NUL | `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137` |
| DD output payload | 8 sheets + `OPEN_QUESTIONS.md` + `PLAN_RESULT.md`; không gồm report này | `a91661b098475b0a90329f5824b56d3e96cda531f9bfa2e24907989f5b9e42a0` |

## Giới hạn kết luận

HTTP tests xác minh route behavior với fake DB sessions, không chứng minh dữ liệu hoặc schema ở môi trường live. Response cardinality, pagination, filter semantics, soft-delete exclusion và 422 query validation vẫn là lựa chọn cục bộ `DERIVED`; cần owner xác nhận và đồng bộ catalog trước khi DD được chốt.
