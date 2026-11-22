# AD-06 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite và không tự chứng minh implementation/runtime. Current executable evidence is recorded separately below.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-06-TC-001` | Planning ref / not run | `AC-32` | See source acceptance section | P1 |

## 2. Test planning references

### AD-06-TC-001 — Acceptance planning reference (AC-32)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-06](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/AD-06.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-32`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/AD-06.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

### Tài liệu và traceability

- [x] Source `screen.png`/`code.html` được giữ nguyên, có hash kiểm tra trước/sau.
- [x] Mỗi marker 1–44 có đúng một mô tả ở mục C; marker map và annotated image đồng bộ.
- [x] API #73 được đối chiếu catalog, AC, route, validate/query/view, shared model, tests/report và database candidate.
- [x] Expected behavior, current source behavior, isolated test evidence và deployment/runtime status tách riêng.
- [x] Search, category, status enum, KPI, code/lesson count, export/sync/policy và permission mapping được ghi blocker/open; create được tách thành API #104 user-approved extension thay vì suy ra từ AC-32.
- [x] Error, empty/out-of-range, auth, pagination và AD-07 handoff được mô tả có truy vết.
- [x] Không ghi AD-06 UI là implemented hoặc RUNTIME VERIFIED.

### Completion decision

- **DD:** `BLOCKED` — source mapping không thể khép kín search, category, KPI, course code/lesson count, status/visibility, export/sync/policy; quyền AC-32 ↔ `ADMIN` chưa duyệt. Create được bổ sung riêng theo user-approved API #104.
- **Implementation:** `PARTIAL SOURCE` — route/page/#68/#73/#104 callers, create dialog, DRAFT write flow and pagination/detail links exist; unresolved features and policy gates remain in [AD-06_PLAN.md](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/AD-06_PLAN.md). Authenticated browser/live API/DB runtime is `NOT VERIFIED`.
- **Runtime:** `NOT VERIFIED` — current focused API #104 and Angular tests use fake DB/client behavior; they do not establish Study Web runtime or live schema/deployment.
- **Next Screen ID:** AD-07 trong một phiên riêng sau khi hoàn tất AD-06.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 2. Bằng chứng đã rà soát

| Nhóm | Nguồn | Kết luận cho AD-06 |
|---|---|---|
| Inventory/dependency | `list_screen.md` row 64; `dd_screens/PLAN.md` | AC-32, #73, route đề xuất `/admin/courses`; từ AD-01/Admin shell, mở AD-07 bằng course ID. Mô tả tìm kiếm/filter/detail/status là expected design, cần đối chiếu source. |
| AC-32 | `apps/study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio` | Actor Admin, precondition có quyền course management; GET #73 → GET #74 → #75 update / #76 status / #77 delete theo policy → reload list. AC không cấp cho AD-06 API create/export/sync và không khóa danh sách status. |
| User-approved extension | `docs/lists/list_api.md`, API #104 source and AD-06 create tests | API #104 `POST /api/v1/admin/courses` is an explicit extension outside AC-32/AC_UNICA. It creates `DRAFT` and returns Course; it does not change what AC-32 specifies. |
| API catalog #73 | `docs/lists/list_api.md` | `GET /api/v1/admin/courses`; Bearer JWT/Admin; optional `status:string`, `mentor:int64`, `category:int64`, `page:int32`; success 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401/403/422/500. Catalog không có search, size, sort hay KPI endpoint. |
| API #73 route/source | `apps/study-server/app/api/v1.py`; `modules/admin/api_73_admin_courses_list/{models,validate,query,view}.py`; shared `shared/course_catalog/{models,helpers}.py` | Shared role `ADMIN` guard xảy ra trước query validation/DB; status raw exact-match; mentor/category signed int64; valid category bị từ chối 422 vì relation chưa source-backed; page default 1, range 1..2,147,483,647, fixed size 20, `courses.id ASC`. Read-only count/page dùng cùng filter. |
| API #73 projection | Query/view + shared Course response model | `items[]`: `id`, `title`, nullable `description`, nullable `thumbnail_url`, exact decimal-string `price`, `status`, `mentor{id,full_name,avatar_url?}`; `pagination{page,size,total,total_pages}`. Search, code, lesson count, category, KPI aggregates và counters không có. Out-of-range page trả 200/empty items, giữ total; orphan mentor/count/projection failures trả safe 500 và rollback. |
| API #77 visibility | `modules/admin/api_77_admin_course_delete/query.py` | Local delete viết `status='DELETED'`; #73 không lọc status, nên unfiltered list có thể chứa bản ghi đó. Đây là current source behavior, không phải phê duyệt visibility/lifecycle policy. |
| Database | `infra/postgres/study-server/DB.sql`; `.agents/server-study/database.md` | Legacy candidate `courses` có numeric id, `mentor_id`, `name`, `price`, `status`; không có course-category FK. `categories` tồn tại nhưng không liên kết. V1-PILOT DDL khác mô hình; live schema/deploy chưa kiểm chứng. |
| Test evidence | API #73 report; API #104 focused server test; AD-06 Angular spec | API #104: 6/6 focused server tests. AD-06: 8/8 focused Angular specs. Tests cover auth/validation/active Mentor/DRAFT/transaction and UI mentor query/success/failure/route safety. Fake DB/client tests do not verify live schema/deployment/browser acceptance. |
| API DD | `apps/study-server/docs/dd/73_admin_courses_list/{02_Overview,03_Request,04_Response,05_Data_Mapping,06_Error,OPEN_QUESTIONS}.md` | `Draft — Needs Confirmation`; còn câu hỏi category, permission, status enum/casing, page/order, orphan mentor, response fields, schema và macro flow #73–#77. |
| Prototype | `screen.png`, `code.html` | 1600×1514, empty state; 9 `href="#"` anchors, 8 buttons, one text input, two selects; chỉ Reset có listener nội bộ; không request/navigation. Bốn KPI đều zero hard-coded; status option lowercase; table có course code/lesson count; export/add/manual sync/policy controls không có handler. |
| Study Web/design | Current Angular source, router and API client exist; AD-06 page uses #73. T031 AD-06 spec 5/5; production build pass. Shared browser unavailable, so authenticated route rendering remains `NOT VERIFIED`; live API/DB remain unverified. | `SOURCE WIRED; RUNTIME NOT VERIFIED` |

## 4. Current executable verification — 2026-11-22

- Server command: `uv run --project apps/study-server pytest apps/study-server/tests/modules/admin/api_104_admin_courses_create/test_admin_courses_create.py` — **6 passed**, one upstream Starlette deprecation warning.
- Angular command: `PATH=/home/daovanhung/.local/opt/node-v22.23.4/bin:$PATH npm test -- --include='src/app/features/admin/AD06/pages/ad06-page.spec.ts'` from `apps/study-client/` — **8 passed**.
- These focused tests use fake DB/session and mocked HTTP/navigation. No live database schema, deployed API, authenticated browser session, or end-to-end deployment was verified.

### Trích từ DD nguồn: 7. Execution and verification order

1. [x] Complete docs worklog preflight; read three exact-type docs worklogs and prescribed context/source pages.
2. [x] Inspect current inventory, prototype/image, AC-32, API catalog/DD/source/test, DB candidate and Study Web boundary; record expected/current and discrepancies in worklog.
3. [x] Write this plan before marker map, annotation and DD.
4. [x] Create ordered marker JSON/SVG and 2× annotated image; preserve original hashes.
5. [x] Author A–F DD with one C row per marker, source-traced event/API/error/state/navigation behavior, and visible blockers.
6. [x] Update AD-06 inventory/reverse API source index and global tracker/checkpoint.
7. [x] Verify hashes, dimensions, marker sequence/coordinates/1:1 C rows, local links, 83 screen IDs/folders, core artifact count, whitespace and scoped diff. Do not run app tests/runtime.
8. [x] Update worklog with final verification; do not process another Screen ID.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
