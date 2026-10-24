# Báo cáo kiểm chứng — API #73

- DD status: Draft — Needs Confirmation.
- Endpoint: `GET /api/v1/admin/courses`.
- Runtime status: `UNWIRED / NOT_FOUND` — router, module, Admin guard và focused test không có trong Study source.
- Direct contract: Bearer JWT/Admin; query status/mentor/category/page; `ApiEnvelope<Page<Course>>`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; errors đúng 401/403/422/500.
- Derived proposal: page 1-based/default 1, fixed size 20, order id ASC, exact filters, all-status default, empty result 200.
- Source gaps: category relation, Admin guard, CourseStatus casing, live schema và orphan mentor policy chưa xác nhận.
- Application tests: `NOT_RUN` — docs-only.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector chọn #48/#49/#50; cả ba được đọc đầy đủ. | PASS |
| Plan trước folder | Requirement/request/query/mutation/response-source matrices có trong worklog trước khi tạo DD folder. | PASS |
| Catalog/diagram | API #73, Course/Page/PageMeta, AC-32 index và mọi node/edge đối chiếu. | PASS — STATIC |
| Source/auth/schema | Route/module/test #73 absent; API #06 precedent; Student-only guard; legacy/pilot DDL tách biệt; category relation gap ghi rõ. | PASS — STATIC SOURCE REVIEW |
| Contract/error | Method/path/query/response/status/error set giữ đúng catalog; không thêm code/status. | PASS |
| Field mapping | Toàn bộ Course, UserSummary, PageMeta và envelope fields được map hoặc có source gap. | PASS |
| Template/package | Exact 11-file set; đủ front matter cho 8 sheet; appendix suffix 8/8 khớp template theo byte. | PASS |
| Markdown/JSON/links | 4/4 JSON examples parse; table widths, fences, local links/anchors, final newline và whitespace đều pass. | PASS — STATIC |
| One-line/coverage | Mỗi request field, response field, query column và error case có dòng riêng; Mutation Matrix là N/A cho GET. | PASS — STATIC REVIEW |
| Template fingerprint | Registered 8-file template pack SHA-256 xem mục fingerprint bên dưới. | RECORDED |
| Output fingerprint | 8 sheet + PLAN_RESULT + OPEN_QUESTIONS; VERIFICATION_REPORT tự loại khỏi digest để tránh self-reference. | RECORDED |
| Source conversion coverage | Không chuyển đổi business workbook; input là catalog, AC-32, DDL và current source. Template appendix được giữ nguyên. | N/A |
| Source defects preserved | Category relation absent, BIGINT/UUID split, CourseStatus casing, nullable mentor và Admin guard/error path gap được giữ rõ. | PASS |
| Introduced defects | Không thấy broken link, JSON/schema/example mismatch hoặc thay đổi source/schema/catalog/diagram trong phạm vi #73. | NONE FOUND |
| AC-32 macro-review | Đã rà nhóm #73–#77; category/counters, visibility, Admin guard, status/schema và error integration còn câu hỏi mở. | COMPLETED_WITH_OPEN_QUESTIONS |
| Application tests | Không chạy; docs-only. | NOT_RUN |
| Context validator | Không sửa context page/manifest. | NOT_APPLICABLE |

## Fingerprints

| Fingerprint | Thuật toán/phạm vi | SHA-256 |
|---|---|---|
| Registered template pack | SHA-256 trên 8 tên file template đã sort + byte nội dung từng file | `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137` |
| DD output payload | SHA-256 trên 8 sheet, `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`; không gồm chính verification report | `9c80d5eb80726531f36312dbf44f7507ad221ee08f757f388789273d22062c04` |

## Source defects preserved

- Catalog #73 khai báo `category`, nhưng legacy `courses` và V1-PILOT không có course-category relation; không tự tạo predicate vật lý.
- Legacy int64 course model và V1-PILOT UUID/version model không được ghép.
- `CourseStatus` enum/casing, missing mentor behavior và Admin permission guard vẫn là câu hỏi.
- Empty-page, default page/size và sort order là proposal `DERIVED`, không được ghi thành runtime fact.

## Giới hạn kết luận

Static verification chỉ chứng minh chất lượng và tính nhất quán của tài liệu với contract/diagram/artifacts đã đọc; không chứng minh Admin auth, category query, live schema hoặc API runtime.
## Kết quả macro-review AC-32 #73–#77

- Ranh giới giữ nhất quán: #73 list; #74 detail; #75 metadata-only update; #76 status + diagram audit; #77 policy soft-delete. Response giữ đúng wrapper catalog: Page cho #73–#76, DeleteResult cho #77.
- Deleted-course visibility ở list/detail và cách #75/#76 xử lý deleted target cần owner/schema quyết định; #73 chưa thể thêm filter vật lý khi marker chưa chọn.
- Category relation, counters, Admin authorization, CourseStatus casing, legacy-vs-pilot schema, dynamic middleware path mapping và error `data:null` so với helper `{}` còn mở.
- Rà tĩnh tài liệu; không đổi contract/source/schema/diagram và không chạy application tests.
