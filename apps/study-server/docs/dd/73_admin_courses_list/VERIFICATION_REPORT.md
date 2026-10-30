# Báo cáo kiểm chứng — API #73

- DD status: Draft — Needs Confirmation.
- Endpoint: `GET /api/v1/admin/courses`.
- Runtime status: `SOURCE_BACKED_LOCAL` — route, Admin module, shared role guard, query/view and focused tests exist; this does not prove deployment/live DB.
- Direct contract: Bearer JWT/Admin; query status/mentor/category/page; `ApiEnvelope<Page<Course>>`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; errors đúng 401/403/422/500.
- Derived proposal: page 1-based/default 1, fixed size 20, order id ASC, exact filters, all-status default, empty result 200.
- Source gaps: category relation, dedicated course-management permission, CourseStatus casing, live schema và orphan mentor policy chưa xác nhận.
- Category behavior: valid int64 filter returns 422 before DB as a `DERIVED` fallback; catalog directly declares the filter, so the discrepancy remains open.
- Application tests: focused API #73 `24 passed`; linked #06/#68/#73 regression `60 passed`; full Study suite `830 passed`, one upstream Starlette/httpx warning. Tests use fake DB rows.
- Static checks: Ruff passes; `git diff --check` passes; OpenAPI exposes 41 unique `/api/v1` paths and 44 operations.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector chọn #48/#49/#50; cả ba được đọc đầy đủ. | PASS |
| Plan trước folder | Requirement/request/query/mutation/response-source matrices có trong worklog trước khi tạo DD folder. | PASS |
| Catalog/diagram | API #73, Course/Page/PageMeta, AC-32 index và mọi node/edge đối chiếu. | PASS — STATIC |
| Source/auth/schema | Route/module/test #73 present; shared ADMIN guard; legacy/pilot DDL tách biệt; category relation gap ghi rõ. | PASS — SOURCE REVIEW; live schema unverified |
| Contract/error | Method/path/query/response/status/error set giữ đúng catalog; không thêm code/status. | PASS |
| Field mapping | Toàn bộ Course, UserSummary, PageMeta và envelope fields được map hoặc có source gap. | PASS |
| Template/package | Exact 11-file set; đủ front matter cho 8 sheet; appendix suffix 8/8 khớp template theo byte. | PASS |
| Markdown/JSON/links | 4/4 JSON examples parse; 34 tables, 36 local links, appendix 8/8 byte-matches template; fences, anchors, final newline and whitespace pass. | PASS — STATIC |
| One-line/coverage | Mỗi request field, response field, query column và error case có dòng riêng; Mutation Matrix là N/A cho GET. | PASS — STATIC REVIEW |
| Template fingerprint | Registered 8-file template pack SHA-256 xem mục fingerprint bên dưới. | RECORDED |
| Output fingerprint | 8 sheets + PLAN_RESULT + OPEN_QUESTIONS; VERIFICATION_REPORT excluded to avoid self-reference. | RECORDED |
| Source conversion coverage | Không chuyển đổi business workbook; input là catalog, AC-32, DDL và current source. Template appendix được giữ nguyên. | N/A |
| Source defects preserved | Category relation absent, BIGINT/UUID split, CourseStatus casing, nullable mentor and dedicated permission gap are kept explicit. | PASS |
| Introduced defects | No broken links or invalid JSON; source changes are scoped to API #73, with no schema/catalog/diagram edits. | NONE FOUND |
| AC-32 macro-review | #73 static path and shared ADMIN guard exist; counters, dedicated permission, visibility, schema/status and #74–#77 integration remain open. | COMPLETED_WITH_OPEN_QUESTIONS |
| Application tests | Focused, linked and full suites pass using fake DB; live DB/deployment not verified. | VERIFIED_LOCAL |
| Context validator | `node` is unavailable; Deno fallback reports only baseline out-of-scope DB Admin context/source paths and missing registered source commit. | BASELINE_FAILURE; Study paths pass isolation review |

## Fingerprints

| Fingerprint | Thuật toán/phạm vi | SHA-256 |
|---|---|---|
| Registered template pack | SHA-256 trên 8 tên file template đã sort + byte nội dung từng file | `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137` |
| DD output payload | SHA-256 trên 8 sheet, `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`; không gồm chính verification report | `6b611fd57ee2909b283e538c166b3c3190c107844d968fe1cb483f9ce687fbe2` |

## Source defects preserved

- Catalog #73 khai báo `category`, nhưng legacy `courses` và V1-PILOT không có course-category relation; không tự tạo predicate vật lý.
- Legacy int64 course model và V1-PILOT UUID/version model không được ghép.
- `CourseStatus` enum/casing, missing mentor recovery behavior and dedicated Admin permission remain open.
- Empty-page, default page/size, filter semantics and sort order are implemented local `DERIVED` choices, not owner-confirmed policy.

## Giới hạn kết luận

Static DD checks and fake-DB HTTP tests confirm local code and contract mapping; they do not prove live schema, production deployment, dedicated course-management permission or category filtering.
## Kết quả macro-review AC-32 #73–#77

- Ranh giới giữ nhất quán: #73 list; #74 detail; #75 metadata-only update; #76 status + diagram audit; #77 policy soft-delete. Response giữ đúng wrapper catalog: Page cho #73–#76, DeleteResult cho #77.
- Deleted-course visibility ở list/detail và cách #75/#76 xử lý deleted target cần owner/schema quyết định; #73 chưa thể thêm filter vật lý khi marker chưa chọn.
- Category relation, counters, dedicated Admin permission, CourseStatus casing, legacy-vs-pilot schema, #74–#77 route-template middleware mapping and course visibility remain open.
- API #73 runtime was changed locally; catalog/schema/diagram were not modified. Tests remain bounded to fake DB data.
