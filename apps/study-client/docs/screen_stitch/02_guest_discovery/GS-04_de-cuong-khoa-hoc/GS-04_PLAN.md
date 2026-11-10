# GS-04 — Kế hoạch chi tiết

> Ngày rà soát: 2026-11-07 · Trạng thái: `AUDIT COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`
> Phạm vi phiên: chỉ GS-04; chưa bắt đầu GS-05.

## Re-audit plan — 2026-11-07

- Re-audit GS-04 only. Preserve the original `screen.png` and `code.html`; verify the existing HTML render, annotation and marker provenance before making any asset changes.
- Recheck current inventory/F02/F04/G-06/G-01, AC-05, API #09 catalog/DD, current route/validator/query/model/view/tests and both checked-in DDL candidates. Test source may be read, but do not run application tests or runtime.
- Recheck the same-course ID handoff from GS-03 and the boundary to ST-10 without editing either Screen ID; recheck Study Web source/wiring.
- Audit the current GS-04 DD, all events/states, marker JSON/SVG/PNG mapping, local links and global tracker. Make only evidence-backed corrections and retain the separate DD, implementation and runtime statuses.
- Record source/contract/schema discrepancies in this plan, GS-04 DD/inventory/tracker/worklog. Do not start GS-05 in this session.

## 1. Phạm vi và nguồn

- Screen ID/tên: **GS-04 — Đề cương khóa học (Tab)**; actor `Guest`; route đề xuất `/courses/:courseId?tab=curriculum`.
- Expected theo `apps/study-client/docs/list_screen.md`: AC-05, API #09; public lesson list theo `sort_order`; private lesson không được Guest mở; reuse #08 from cache → GET #09; phân biệt empty curriculum với error. Liên kết GS-03 và ST-10.
- Current `screen.png`: 1280×1024, SHA-256 `4892375ec0fe6316e126b1eefe85ce05b0852079c6d666290e43c4a6f13b85c2`, entropy 0.134765, 1930 colors; chỉ còn nền gần trắng và footer, không đọc được phần header/body.
- Current `code.html`: SHA-256 `cb500b6794bc3336167dfce639506b99f438e789d64055717cedc1849b5be22c`; static empty curriculum page: header, breadcrumb, H1, card/icon/copy “Chưa có nội dung đề cương để hiển thị.”, back-to-detail link `href="#"`, footer. Không có lesson rows, route binding, request/API handler hoặc click logic.
- Kế hoạch ảnh: giữ nguyên `screen.png` và `code.html`; Firefox đã render HTML nguyên trạng thành `screen_rendered.png` 1440×1200, đầy đủ header, breadcrumb, title, empty panel và footer. Dùng ảnh render làm nền chú thích mà không sửa nguồn. Ghi rõ bản render không phải runtime.
- Study Web subcontext là `UNWIRED`; không có app source/router/package/entrypoint. Route trong tài liệu vẫn là proposal.

## 2. API #09 source trace và các discrepancy

| Hạng mục | Expected/design source | Current source evidence | Kết luận |
|---|---|---|---|
| Route/API | Public `GET /api/v1/courses/{course_id}/curriculum`, AC-05; no query/body. | `apps/study-server/app/api/v1.py` đăng ký route #09 và gọi `get_course_curriculum` với DB dependency/trace ID. | API #09 `SOURCE_BACKED`; điều này không chứng minh Study Web gọi được endpoint hoặc live deployment. |
| Validation | Catalog/DD path `course_id:int64`. | Route khai báo `course_id:str`; `validate_course_id` dùng `parse_integer`, malformed syntax trả 404 `DESIGN_RESOURCE_NOT_FOUND`. Shared parser không enforce signed int64/positive range; tests source chỉ cover số thường và non-integer, chưa có boundary case. | `DISCREPANCY`: API contract int64 chưa khớp parser current; không invent response cho oversized ID. |
| Query/visibility/order | AC-05 muốn curriculum public theo thứ tự; inventory nói private lesson không được Guest mở. | Q1 chỉ nhận course `PUBLISHED`; Q2 chỉ lấy lesson `PUBLISHED`, `sort_order ASC, id ASC`. Read-only. | `status=PUBLISHED` là current query behavior, nhưng API DD vẫn gọi đây là visibility assumption; nó chưa chứng minh lesson an toàn để mở/xem trước. |
| Response | Declared `ApiEnvelope<Page<Lesson>>`. | Current `Lesson` gồm `id`, `course_id`, `title`, optional `content`, optional `video_url`, `order`, `status`. API trả cả `content`/`video_url` cho public callers; pagination one-page `page=1,size=total,total=total,total_pages=1` nếu có item, empty thì 0. | UI curriculum chỉ được mô tả theo dữ liệu cần thiết cho danh sách; không render/phát media/lesson content từ public response nếu chưa có preview/access rule. |
| Empty/error | Empty curriculum khác lỗi; API contract 200/404/500. | Empty là HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, `items=[]`, message `No published lessons.`. Missing/unpublished course là 404 `DESIGN_RESOURCE_NOT_FOUND`; DB/mapping error là 500 `DESIGN_INTERNAL_ERROR`; SQLAlchemy error rollback. | Map empty riêng; 404/500 riêng. Không tự tạo retry, 403, timeout hoặc cache TTL. |
| Tests | Test source hiện diện. | Fake-session tests cover invalid ID, course not found, both DB branches, success, empty and TestClient route composition. Tests chưa chạy; không kiểm tra real PostgreSQL. | Static/source-backed only; no runtime or live schema claim. |
| DDL | API source/DD map `lessons.name/content/video_url/sort_order/status`. | `infra/postgres/study-server/DB.sql` legacy BIGINT candidate khớp các field query nhưng không có preview flag. `infra/postgres/02_study_db.sql` V1-PILOT UUID/versioned lessons dùng `title/summary/position/estimated_minutes/is_preview` và relations khác; API #09 không query nó. Live schema chưa xác minh. | `DISCREPANCY`: không suy ra preview từ V1-PILOT DDL hoặc coi DDL nào là live. Cần chốt schema/API projection/access policy. |
| Orchestration/cache | GS-04 inventory: reuse #08 cache → GET #09. F02: lazy theo tab; AC-05: gọi #09 ngay sau #08 trong flow eager. | Không có Study Web cache/router implementation để kiểm tra. API #09 tự kiểm tra course PUBLISHED. Cache key/freshness/miss behavior không thấy contract. | Giữ cả ba nguồn; không invent cache TTL, fallback #08 hoặc eager/lazy policy. Direct route without #08 cache needs owner decision. |
| Lesson access | Inventory: private lesson không mở bằng Guest; F04 không dùng public #09 thay permission tree; ST-10 #22 → #23 → #24 chỉ sau allowed. | API #09 không trả preview/access flag và public response có optional `video_url`/`content`; #22–#24 là design-only theo inventory, không được gọi từ GS-04. | `BLOCKER` bảo mật/visibility: không tạo lesson-open, video, preview hoặc ST-10 action từ Guest tab. |

## 3. Marker dự kiến

Chỉ đánh số các nhóm element thật sự có trong current HTML state; không thêm marker cho loaded lesson list vắng mặt. Tọa độ chốt sau khi render:

| Marker | Element ID | Nhóm |
|---:|---|---|
| #1 | `GS04-EL-01` | Header brand và primary nav |
| #2 | `GS04-EL-02` | Header Đăng nhập / Đăng ký |
| #3 | `GS04-EL-03` | Breadcrumb Trang chủ / Khóa học / Chi tiết khóa học / Đề cương khóa học |
| #4 | `GS04-EL-04` | H1 “Đề cương khóa học” |
| #5 | `GS04-EL-05` | Empty card icon `toc` |
| #6 | `GS04-EL-06` | Empty-state heading |
| #7 | `GS04-EL-07` | Empty-state explanatory copy |
| #8 | `GS04-EL-08` | Link “Quay lại chi tiết khóa học” (`href="#"`) |
| #9 | `GS04-EL-09` | Footer brand |
| #10 | `GS04-EL-10` | Footer navigation |

Không có marker cho lesson item, private/preview indicator, play button, video/content, course title hoặc tab controls vì chúng không xuất hiện trong HTML. Mục C của DD phải ghi rõ expected-but-absent cho các yếu tố này.

## 4. Events, state và handoff cần mô tả

- **Load curriculum:** parse `courseId` từ route proposal; expected reuse #08 cache theo đúng ID rồi gọi #09. Cache availability/freshness chưa có contract. Current #09 tự gate course PUBLISHED, nhưng không giải quyết lesson preview/access. Map `data.items` theo `order`; không show `content`/`video_url` hoặc status badge như access token.
- **Empty:** map `items=[]` 200 thành empty state; static HTML có copy gần với empty case nhưng không chứng minh nó được hiển thị theo API.
- **Back to GS-03:** HTML có breadcrumb `Chi tiết khóa học` và CTA quay lại với `href="#"`; expected route giữ nguyên `courseId` và tab/course context theo proposal. Router/back destination chưa wired.
- **Lesson selection:** hiện không có lesson card. Không tạo link/event mở lesson cho Guest. Nếu sản phẩm muốn preview, cần API field/endpoint + visibility/access contract; ST-10 là Student path với #22–#24, không phải Guest action.
- **Header/footer navigation:** giữ đúng literal href hiện có `/`, `/courses`, `/login`, `/register`; route resolution không verified.
- **States:** source hiện có static empty state; expected loading/empty/ready/error. 404/500 từ API có thể phân biệt theo source, nhưng visual error/loading state chưa có asset. No retry/timeout/cache semantics.

## 5. Thứ tự và acceptance checklist

1. [x] Kế hoạch này được ghi trước khi tạo render/annotation/DD.
2. [x] Render `code.html` trong Firefox thành `screen_rendered.png`; layout đã kiểm tra. Không ghi đè source.
3. [x] Tạo `GS-04_markers.json`, SVG overlay và `screen_annotated.png` với 10 marker đúng vùng và không che nội dung; preview đã được kiểm tra.
4. [x] Viết `GS-04.md` theo objective: overview; flow; 10 elements; event input/processing/output/error; #09 contract; state/navigation; security/access blockers; trace links.
5. [x] Static check JSON/order/ID mapping, local links, image dimensions/visual layout, original hashes, marker bounds/gutters, `git diff --check`, 83 ID count and total artifacts. Không chạy tests.
6. [x] Cập nhật tracker GS-04/progress và worklog sau kiểm tra. Do source/design còn thiếu access/preview policy, DDL discrepancy, cache rule, loaded list design và Study Web runtime: `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`.

### Điều kiện DD READY chưa đạt

- Không có visual design cho loaded list, lesson hierarchy/preview affordance hoặc curriculum error/loading variants.
- API #09 trả lesson content/video URL công khai nhưng không có preview/access field; status filter là assumption trong DD #09.
- Hai checked-in DDL sources khác nhau; live schema chưa được xác minh.
- #08 cache freshness/miss behavior và AC-05 eager vs F02 lazy orchestration chưa chốt.
- Study Web/router chưa wired; route/back link hiện chỉ là proposal/`#` placeholder.

## Re-audit result — 2026-11-07

- API #09 route, validator, query/model/view and focused test source were re-read. Current route is public GET; query gates on PUBLISHED course, selects PUBLISHED lessons sorted by `sort_order ASC, id ASC`, and maps a no-lesson result to HTTP 200 with an empty page. Query/mapping errors return safe 500; SQLAlchemy query errors roll back. Tests use fake sessions and were not run.
- New discrepancy recorded: catalog says `course_id:int64`, but the route annotation is `str` and shared `parse_integer` has no signed-int64/positive bound. Existing test source has no range-boundary case.
- The current `status='PUBLISHED'` filter is present in runtime source, while API #09 Draft DD still calls it an assumption; public response includes `content` and `video_url` but no preview/permission field. Keep the Guest lesson-open/media action blocked.
- The legacy BIGINT DDL matches the queried `name/content/video_url/sort_order/status` columns but has no preview flag. The V1-PILOT UUID/versioned schema uses different lesson fields/relations and includes `is_preview`; current API #09 does not query that model. Server database context marks live schema unverified.
- F02 lazy-by-tab, AC-05 eager calls, and inventory #09 reuse of #08 cache remain distinct expected sources; cache key/freshness/miss/direct-entry behavior is absent. GS-03 handoff preserves the same courseId; ST-10 #22–#24 is a separate Student path and is not wired as a Guest action.
- Visual review confirmed `screen.png` remains near blank and unchanged; its HTML-derived render is legible, and the 10 gutter markers are ordered and do not cover content. Final static audit passed: all eight bundle files are present; source hashes match; image dimensions are 1280×1024, 1440×1200 and 3040×2400; ten ordered unique markers map to ten DD rows and ten SVG labels and remain within the annotation canvas; the SVG embeds the exact rendered PNG; all six events specify input/trigger, processing and output; local links resolve; and 83 inventory IDs match tracker rows and screen folders. Scoped `git diff --check` passed.
- Keep `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. No tests, browser app runtime or live database were run.
