---
task_id: "2026-10-24-create-study-api73-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #73

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Ghi riêng contract trực tiếp với proposal `DERIVED`; query/schema legacy chỉ là candidate; giữ `SOURCE_REQUIRED` khi không có field/quan hệ; Study DD chỉ giao Markdown.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Đọc diagram toàn luồng; không map ngầm UUID pilot sang BIGINT contract; xử lý data mapping trước request/response và giữ code lỗi đúng catalog.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Phân biệt DDL artifact với live schema; proposal ngoài diagram phải nêu `DERIVED`, cần review nhóm khi đủ API liên quan.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD tiếng Việt cho API #73, đọc toàn bộ AC-32, tham khảo DD đã có, lập plan và các ma trận trước khi tạo folder, kiểm tra tĩnh ngay sau authoring.
- Canonical contract/approved DD: `docs/lists/list_api.md` row #73: `GET /api/v1/admin/courses`, Bearer JWT role Admin, query `status?:string`, `mentor?:int64`, `category?:int64`, `page?:int32`, response `ApiEnvelope<Page<Course>>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, errors 401/403/422/500 đúng business codes trong catalog.
- AC-32 direct flow: Admin có quyền course management → mở danh sách (#73) → query courses → chọn chi tiết (#74) → quyết định update (#75), status (#76) hoặc delete (#77) → quay lại danh sách. AC-32 nêu quản lý course theo status/nội dung và xóa theo policy.
- Reusable schemas: `Page<T> = {items:T[], pagination:PageMeta}`; `PageMeta={page:int32,size:int32,total:int64,total_pages:int32}`; `Course={id,title,description?,thumbnail_url?,price,status,mentor:UserSummary,category?:Category}`.

## CURRENT_BEHAVIOR

- Source/config: Không có API #73 hoặc `/api/v1/admin/courses` trong `apps/study-server/app/api/v1.py`; không tìm thấy module `api_73_*` hoặc test tương ứng. Router hiện có source APIs #01–#09 và #12–#14.
- Related runtime precedent: API #06 `GET /api/v1/courses` có `CoursePage`, `PageMeta`, join mentor và serialize NUMERIC price thành chuỗi; mặc định page=1,size=20. Nhưng #06 là public, chỉ lấy `PUBLISHED`, và trả 422 cho category vì chưa có quan hệ course-category source-backed. Không chuyển bộ lọc `PUBLISHED` sang Admin #73.
- Schema artifacts: Legacy `courses` có `id`, `mentor_id`, `name`, `description`, `thumbnail_url`, `price`, `status`; `categories` tồn tại riêng nhưng `courses` không có `category_id`/bảng liên kết trong DDL. `DB_UNICA_TABLES.md` đánh dấu mapping course là DESIGN_ONLY. V1-PILOT dùng UUID `courses` và versioned `course_versions`, khác contract BIGINT; không map ngầm. Live schema chưa xác minh.
- Security/integration: `app/utils/auth.py` chỉ có shared guard cho Student; AC-32 cần Admin/course-management permission. `/api/v1/admin/courses` chưa nằm trong `DESIGN_CONTRACT_PATHS`; nếu sau này wire mà không cập nhật allowlist, generic validation/system exception có thể phát code fallback thay vì `DESIGN_*`. Current error helper mặc định `data={}` còn API guideline yêu cầu `null` cho lỗi.
- Runnable tests: Không có test API #73. API #06 test source bao phủ page default, size, empty/out-of-range page, category 422, lỗi query/mapping và mentor integrity; chỉ là precedent source, không chạy test trong task docs-only.
- Runtime wiring: API #73 `UNWIRED / NOT_FOUND`; DD không được coi là implementation.

## SOURCE_TRACE

```text
Admin Bearer principal + course-management permission -> đọc query filters/page -> validate page -> Q1 chọn page Course và Q2 count bằng cùng predicates -> map Page<Course> -> trả 200 (kể cả danh sách rỗng) hoặc exact catalog 401/403/422/500 -> UI mở #74 hoặc quay lại danh sách sau #75/#76/#77
```

Không query DB trước khi authorization thành công. Predicate category chưa thể được ánh xạ vật lý từ nguồn hiện tại; không tạo quan hệ giả. Group API #74–#77 có DD sau này và macro-review AC-32 sẽ chờ tới khi #77 tồn tại.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #73 route/module/test | Search current Study router, modules and tests | `UNWIRED / NOT_FOUND` | Tài liệu không khẳng định runtime. |
| Admin authorization | AC-32 yêu cầu quyền course management; shared guard hiện chỉ hỗ trợ Student | `SOURCE_REQUIRED` | Không dùng Student guard hoặc bịa claim/policy/table Admin. |
| Course-category relation | Legacy DDL có categories nhưng courses không có FK/association; API #06 hiện từ chối category | `SOURCE_REQUIRED / DISCREPANCY` | Category filter là contract trực tiếp, nhưng physical query chưa xác định; không thêm cột/JOIN. |
| Course schema selection | Legacy BIGINT courses/users và V1-PILOT UUID course/version model khác nhau | `DISCREPANCY` | Chỉ dùng legacy DDL làm candidate; live schema chưa xác minh. |
| Status filter | Contract query nhận string; #76 gọi draft/published/suspended; legacy default DRAFT, API #06 lọc PUBLISHED | `DIRECT semantics / enum casing SOURCE_REQUIRED` | Đề xuất equality trên giá trị được gửi; không tự dựng enum/casing allowlist. |
| Pagination rules | Query chỉ có page; response PageMeta cần page/size/total/total_pages | `DERIVED` | Đề xuất page 1-based/default 1, size cố định 20 theo API #06 và DD #68; không thêm `size` query. |
| Course mentor projection | Course.mentor bắt buộc; legacy mentor_id nullable; #06 trả 500 khi thiếu mentor | `DERIVED / SOURCE_REQUIRED` | Đề xuất dùng cùng kiểm tra integrity; owner cần cân nhắc course mồ côi trong màn Admin. |
| Error envelope/path mapping | Admin path chưa allowlist; helper data mặc định `{}` trong khi guideline kỳ vọng `null` | `CONDITIONAL FUTURE DISCREPANCY` | Ghi integration gap, không mô tả là runtime API #73. |

## PLAN BEFORE DD AUTHORING

1. Giữ nguyên method/path/auth, query names/types, response `ApiEnvelope<Page<Course>>`, HTTP 200 và exact error set 401/403/422/500; không thêm body, query `size/sort`, status code hay business code.
2. Theo đúng AC-32: #73 query danh sách trước #74 detail; không trộn update #75, status #76 hay delete #77 vào side effect của GET. Không áp dụng filter public `PUBLISHED` của API #06; khi không có filter status, candidate trả mọi course status để Admin quản lý.
3. Suy diễn đơn giản và gắn nhãn `DERIVED`: status, mentor, category dùng exact match khi được truyền; `page` bắt đầu từ 1 và mặc định 1; size cố định 20 vì contract không có query size; sort mặc định `courses.id ASC` để phân trang ổn định; page<=0 dùng 422 catalog; trang vượt tổng và danh sách rỗng trả 200 với `items=[]`, `total_pages=0` khi total=0.
4. Query candidate trên legacy: `courses AS c LEFT JOIN users AS m ON m.id=c.mentor_id`. Q1 chọn allowlist course fields và mentor summary; Q2 đếm course cùng predicates status/mentor/page context. Không chọn credential hoặc PII ngoài UserSummary.
5. Không tạo predicate category vật lý. Nêu predicate logic `category id exact-match` là DIRECT/DERIVED semantics, nhưng relation/table/column hiện `SOURCE_REQUIRED`; request có category chưa thể được triển khai đúng cho đến khi owner cung cấp source mapping. Không sao chép hành vi reject của #06 sang #73 vì #73 khai báo filter này trực tiếp.
6. Map Course: `courses.id → id`, `name → title`, description, thumbnail_url, price NUMERIC thành decimal string, status giữ source value, mentor `{id,full_name,avatar_url}` từ users. Optional null fields giữ null theo precedent API #06; `category?` chỉ emit nếu relation có nguồn, hiện omit vì optional và chưa source-backed. Giá thiếu hoặc mentor thiếu là candidate data-integrity 500 theo #06; ghi rõ rủi ro Admin visibility.
7. Response PageMeta lấy effective `page`, fixed `size=20`, `COUNT(*)` với cùng filters, `ceil(total/20)` và 0 khi total=0. Count/page predicates phải đồng nhất. Nếu category filter được gửi mà physical relation chưa có, giữ đây là implementation blocker thay vì giả lập kết quả.
8. Xác thực Admin/course-management trước query; 401/403 đúng catalog. 422 chỉ cho invalid page/query parsing theo code đã khai báo; không tạo danh sách CourseStatus mới. Query/mapping lỗi trả 500 DESIGN_INTERNAL_ERROR; không lộ SQL/stack trace.
9. Tạo 8 template sheets + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` trong `73_admin_courses_list/`; `07_table.md` là `N/A — READ-ONLY API`; không tạo ZIP, sửa code, schema, catalog hoặc diagram.
10. Static-check manifest, exact contract/errors, all Course/Page fields, one-row mapping, JSON, template appendix hashes, links/anchors, table widths, fences, whitespace, no placeholders/status markers. Sau #73 giữ AC-32 macro-review pending tới khi #74–#77 có DD; cuối nhóm rà lại default/pagination, category/status, detail response, edit/status/delete policy và reload.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #73 | Method/path | `GET /api/v1/admin/courses` | Catalog + AC-32; DIRECT |
| #73 | Actor/auth | Bearer JWT; role Admin; course-management permission | Catalog + AC-32; DIRECT requirement, runtime guard absent |
| #73 | Query | `status?:string`, `mentor?:int64`, `category?:int64`, `page?:int32` | Catalog; DIRECT |
| #73 | Body | Không khai báo | Catalog; DIRECT |
| #73 | Success | `ApiEnvelope<Page<Course>>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | Catalog + AC-32; DIRECT |
| #73 | Error | 401 `DESIGN_AUTHENTICATION_REQUIRED` | Catalog; DIRECT |
| #73 | Error | 403 `DESIGN_ACCESS_DENIED` | Catalog; DIRECT |
| #73 | Error | 422 `DESIGN_VALIDATION_ERROR` | Catalog; DIRECT; exact invalid value rules partly DERIVED |
| #73 | Error | 500 `DESIGN_INTERNAL_ERROR` | Catalog; DIRECT |
| #73 | List flow | Query courses before opening detail (#74) | AC-32 diagram; DIRECT |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Header Bearer JWT | Admin/course-management principal before Q1/Q2 | Role/permission DIRECT; guard, claims, identity mapping SOURCE_REQUIRED |
| `status` | Optional query string | Candidate exact predicate on `c.status`; no filter when omitted | Filter DIRECT; exact enum/case SOURCE_REQUIRED; all-status default DERIVED |
| `mentor` | Optional query int64 | Candidate exact predicate `c.mentor_id = :mentor` | Type/filter DIRECT; principal-vs-mentor identity irrelevant to filter; DB is legacy candidate |
| `category` | Optional query int64 | Logical exact category predicate; physical query relation absent | Request DIRECT; relation SOURCE_REQUIRED; no fabricated join/rejection |
| `page` | Optional query int32 | Candidate offset `(page-1)*20` and PageMeta.page | Type DIRECT; default 1, minimum 1 DERIVED; invalid maps to direct 422 |
| Body | None | None | DIRECT |
| Query `size`/`sort` | Not declared | None | DIRECT absence; do not add |

### Query Matrix

| Query ID | Type | Candidate source | Selected fields/predicate | Purpose/status |
|---|---|---|---|---|
| Q1 | SELECT | Legacy `courses AS c` LEFT JOIN `users AS m` | Course allowlist + `m.id`, `m.full_name`, `m.avatar_url`; `m.id=c.mentor_id`; optional `c.status=:status`, `c.mentor_id=:mentor`; `ORDER BY c.id ASC LIMIT 20 OFFSET :offset` | Candidate legacy projection; live schema unknown; category predicate absent until relation source-backed |
| Q2 | COUNT | Legacy `courses AS c` | `COUNT(*)`; same status/mentor predicates as Q1 | Candidate `PageMeta.total`; category sync blocked by same schema gap |
| Q3 | N/A pending mapping | No approved legacy or pilot course-category relation | No table/column/JOIN authorized | `SOURCE_REQUIRED`; do not invent `category_id` or link table |

### Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | API #73 is read-only | No INSERT/UPDATE/DELETE | `N/A — READ-ONLY API` |

### Response Source Matrix

| Response field | Type | Candidate source/transform | Null/empty rule | Evidence status |
|---|---|---|---|---|
| `success` | boolean | Envelope branch | true on success, false on error | DIRECT envelope |
| `businessCode` | string | Catalog branch code | Exact code | DIRECT |
| `message` | string | Safe localized message | Exact text unspecified | DERIVED wording |
| `data.items[]` | `Course[]` | Q1 course rows | Empty array when no match | DIRECT type; empty behavior DERIVED from API #06 |
| `data.items[].id` | int64 | `courses.id` | Required | Legacy candidate; live schema unknown |
| `data.items[].title` | string | `courses.name` | Required; alias name→title | Legacy candidate + API #06 mapping precedent |
| `data.items[].description` | string? | `courses.description` | Null when source NULL per #06 model | Candidate |
| `data.items[].thumbnail_url` | uri? | `courses.thumbnail_url` | Null when source NULL per #06 model | Candidate |
| `data.items[].price` | decimal-string | `courses.price` NUMERIC | Exact Decimal-to-string; no float conversion | Candidate; API #06 implementation precedent |
| `data.items[].status` | CourseStatus | `courses.status` | Preserve source value | Candidate; enum/casing incomplete |
| `data.items[].mentor.id` | int64 | `users.id` through `courses.mentor_id` | Required | Candidate; missing mentor rule DERIVED/OPEN |
| `data.items[].mentor.full_name` | string | `users.full_name` | Required | Candidate |
| `data.items[].mentor.avatar_url` | uri? | `users.avatar_url` | Null when source NULL | Candidate; #06 serializes null |
| `data.items[].category` | Category? | No approved source | Omit unless relation/schema is approved | Optional DIRECT; mapping SOURCE_REQUIRED |
| `data.pagination.page` | int32 | Effective request page | 1 when omitted | DIRECT type; default DERIVED |
| `data.pagination.size` | int32 | Fixed page size | 20 | DIRECT type; fixed value DERIVED from #06/#68 precedent |
| `data.pagination.total` | int64 | Q2 count | 0 when no rows | DIRECT type; query candidate |
| `data.pagination.total_pages` | int32 | `ceil(total/20)` | 0 when total=0 | DIRECT type; formula DERIVED |
| `meta` | object | Envelope convention | `{}` candidate | Convention candidate; error data discrepancy noted |
| `traceId` | uuid | Current request trace | Propagated/generated by middleware | Source-backed convention; API #73 unwired |

## CHANGES

- Files changed: `apps/study-server/docs/dd/73_admin_courses_list/` (8 sheets + 3 reports); `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`; this worklog.
- CONTEXT_UPDATES: None; no runtime/schema/catalog/diagram change.
- Context pages changed: None planned.
- Assumptions: Simplest pagination/status/filter behavior is explicitly `DERIVED`; physical category mapping, Admin guard and live schema remain `SOURCE_REQUIRED`. Preserve existing user modifications outside API #73 scope.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Project router/context | Read root `AGENTS.md`, `.agents/AGENTS.md`, context map, server-study entry/index/workflow and registry wiring. | `VERIFIED_STATIC_ONLY` |
| Worklog preflight | Deno selector selected #48/#49/#50; all three were read in full before deep inspection. | `VERIFIED` |
| Catalog/AC-32 | API #73 row, Course/Page/PageMeta reusable schema, AC-32 index and every AC32 diagram node/edge inspected. | `VERIFIED_STATIC_ONLY` |
| Current source/tests/schema | Router/module/test absence, API #06 source/test precedent, Student-only guard, middleware allowlist, legacy and pilot course DDL inspected; live schema not verified. | `VERIFIED_STATIC_ONLY` |
| Existing DD reference | Reviewed API #68 Admin list proposal and API #06 Course mapping/readonly sheet. | `VERIFIED_STATIC_ONLY` |
| Plan-before-authoring | API Requirement, Request Usage, Query, Mutation and Response Source matrices recorded above before creating DD folder. | `VERIFIED` |
| DD package/template | Exact 11-file manifest; 8/8 core files have front matter and byte-identical template appendix suffixes. Template pack fingerprint recorded in verification report. | `VERIFIED_STATIC_ONLY` |
| Static Markdown/contract | Exact catalog code set 401/403/422/500 plus success 200; 4 JSON examples parse; tables, fences, relative links/anchors, whitespace and required fields pass. | `VERIFIED_STATIC_ONLY` |
| Output fingerprint | 10-file DD payload fingerprint recorded in `VERIFICATION_REPORT.md`, excluding the report itself. | `RECORDED` |
| Current route/module/test scan | API #73 absent from router, modules and tests; `UNWIRED / NOT_FOUND`. | `VERIFIED_STATIC_ONLY` |
| Inventory refresh | 103 catalog IDs; 73 core DD folders (61 full 11-file packages); 30 missing; 12 route-plus-view APIs. | `VERIFIED_STATIC_ONLY` |
| Git whitespace | `git diff --check` completed without diagnostics. | `VERIFIED` |
| AC-32 macro-review | #73 is one of five linked APIs; group review remains pending through #77. | `PENDING` |
| Runtime tests | Not run; this is a docs-only task. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Course-category relation/mapping, Admin course-management guard, live schema, exact CourseStatus values/casing, and orphan mentor visibility policy.
- Next owner/action: Continue with API #74 in the next API session. Keep AC-32 macro-review pending until #74–#77 DDs exist; retain category relation, Admin guard, status casing, page defaults and orphan-mentor questions.

## CURRENT GROUP REVIEW UPDATE — 2026-10-24

- AC-32 macro-review #73–#77 đã hoàn tất sau khi API #77 có DD. Đã cập nhật `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, `VERIFICATION_REPORT.md` của #73 với trạng thái `COMPLETED_WITH_OPEN_QUESTIONS`.
- Kết quả chung giữ #73 list/filter, #74 detail, #75 metadata-only, #76 status + audit intent, #77 soft-delete theo policy; Page wrapper cho #73–#76 và DeleteResult cho #77 không đổi.
- Category relation, counters, Admin guard, CourseStatus casing, live schema, soft-delete visibility/physical marker và error middleware vẫn cần quyết định. Review tài liệu-only; không chạy application tests.
- Next API DD: #78.
