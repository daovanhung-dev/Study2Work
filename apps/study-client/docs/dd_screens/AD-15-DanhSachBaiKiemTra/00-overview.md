# AD-15 — Danh sách bài kiểm tra · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-15` |
| Module | Admin |
| Route | `/admin/quizzes` — registered in `features/admin/admin.routes.ts`; route spec covers `AD15Page` |
| Actor/role | Admin session; local #87 requires `ADMIN`. AC-35 quiz-management permission remains unresolved. |
| DD status | **DD BLOCKED** · **IMPLEMENTATION PARTIAL SOURCE** · **RUNTIME NOT VERIFIED** · Angular route/page/API caller/spec and local #87 route/module/query/model/tests exist; API DD remains Draft and live schema/deployment is unverified.<br> |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-15.md](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/AD-15.md), [AD-15_PLAN.md](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/AD-15_PLAN.md), [AD-15_markers.json](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/AD-15_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: List theo course/status; Create/Update → AD-16, Statistics → AD-17, Delete → AD-18 theo AC-35.
- In-scope: Current Angular page calls GET #87 with `course`, `status`, and `page`; it renders only the local Page projection fields and exposes the safe-ID statistics handoff. Catalog `ApiEnvelope<Quiz>` still differs from local `ApiEnvelope<Page<Quiz>>`; code/course title/question count/status are absent, and search is not supported.
- Out-of-scope: No API #88–#91 mutation/statistics request is issued from this list page; do not treat source/tests as live DB or browser verification.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-35 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | List theo course/status; Create/Update → AD-16, Statistics → AD-17, Delete → AD-18 theo AC-35. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #87
- Liên kết màn hình dự kiến: [AD-16](../AD-16-TaoChinhSuaQuiz/00-overview.md), [AD-17](../AD-17-ThongKeBaiKiemTra/00-overview.md), [AD-18](../AD-18-XacNhanXoaBaiKiemTra/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/ready/error/unauthorized/forbidden/validation/service-error |
| Current source | Angular route/page/service/spec and local API source | `loading` / `loaded` (including empty rows) / `error`; API/browser/live-DB runtime remains `NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-15 source screen.png](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/screen_annotated.png))
- Luồng hiện tại: `/admin/quizzes` → `AD15Page` → `AD15ApiService` → Admin Bearer client → GET #87. The local client consumes `Page<Quiz>`; this remains a derived local shape, not an approved change to the catalog's singleton `Quiz` response.
- Priority: P1; **DD BLOCKED; IMPLEMENTATION PARTIAL SOURCE; RUNTIME NOT VERIFIED:** response cardinality/projection, AC-35 permission vs `ADMIN`, legacy BIGINT vs V1-PILOT UUID/live schema, and live/browser behavior remain unresolved.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-16 — Reconcile current Angular route/page/API caller and focused specs; retain Draft API and live-runtime gates.

## Trạng thái và ranh giới bằng chứng

### Current-source addendum — 2026-11-16

- `/admin/quizzes` is registered to `AD15Page` in `apps/study-client/src/app/features/admin/admin.routes.ts`; `admin.routes.spec.ts` covers the route.
- On entry the page requests #87 with default `page=1`; submitted filters use exact `course` and `status` text, and page controls use returned pagination. `AD15ApiService` calls `AdminApiService`, which attaches the Admin Bearer token. The local #87 implementation returns `Page<Quiz>`; the direct catalog/AC contract still says `Quiz`.
- The page renders only `id`, `title`, `course_id`, nullable `duration_minutes`, and `passing_score`. It does not show quiz code, course title, question count, quiz status, or nested question content. It does not expose search, edit, or delete actions. Create and safe-ID statistics links are navigation only; the page sends no mutation/statistics request.
- Current UI states are loading, loaded rows/empty rows, and error. Shared Admin error handling maps authentication, access, validation and connection errors; no retry/cache policy is declared here.
- Numeric identifiers are labelled as IDs. The existing open questions remain: response cardinality, dedicated quiz-management permission, live schema, tombstone/status rules and local derived 422 behavior. Status: `DD BLOCKED`, `IMPLEMENTATION PARTIAL SOURCE`, `RUNTIME NOT VERIFIED`.
- Verification on 2026-11-16: focused Angular spec 5/5 passed; focused API #87 tests 20 passed with fake DB sessions; Study Web production build passed with three existing Student CSS budget warnings. Browser UI and live DB remain `NOT VERIFIED`.

> The source excerpt below preserves the 2026-11-08 prototype/DD snapshot. Its `UNWIRED` statements describe that historical snapshot and are superseded for current source status by this addendum.

# AD-15 — Danh sách bài kiểm tra

> **Screen:** AD-15 · **Actor theo thiết kế:** Admin có quyền quản lý quiz theo AC-35 · **Route đề xuất:** `/admin/quizzes` · **API chính:** #87 · **Liên quan:** AD-16 tạo/sửa, AD-17 thống kê, AD-18 xác nhận xóa.<br>
> **Trạng thái màn hình:** `DD BLOCKED` · `IMPLEMENTATION BLOCKED` · `RUNTIME NOT VERIFIED` · **API source:** route/module/query/model/test source #87 có trong checkout; API DD còn Draft; live schema/deployment chưa xác minh.<br>
> **Tài sản:** [ảnh nguồn](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/screen.png) · [ảnh đánh số](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/screen_annotated.png) · [bản đồ marker](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/AD-15_markers.json) · [kế hoạch](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/AD-15_PLAN.md) · [inventory](../../list_screen.md)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Mục tiêu và trạng thái chứng cứ

AD-15 là trang quản trị danh sách bài kiểm tra, dự kiến giúp Admin lọc danh sách theo khóa/trạng thái, mở AD-16 để tạo hoặc chỉnh sửa, AD-17 để xem thống kê, và AD-18 để xác nhận xóa. Inventory đề xuất `/admin/quizzes`; đây chưa phải route đã được xác minh trong Study Web.

| Thuộc tính | Expected behavior | Current evidence |
|---|---|---|
| Actor/quyền | Admin có `quiz management permission` theo AC-35. | Local API #87 chỉ kiểm tra role `ADMIN`; chưa có policy source cho permission riêng. |
| Route | `/admin/quizzes` theo inventory. | Study Web hiện không có editable source/router/API client; route chưa được wire (`UNWIRED`). |
| Dữ liệu danh sách | Quiz theo khóa học/trạng thái; AC-35 gọi #87 trước khi chọn thao tác. | Catalog #87 khai báo `ApiEnvelope<Quiz>`; local source trả `ApiEnvelope<Page<Quiz>>` với metadata hạn chế. |
| Tìm/lọc/phân trang | Prototype có ô tìm, khóa học, trạng thái và trang. | Search không có trong #87; course option là slug nhưng API nhận `int64`; status option chưa có mapping; local page cố định size 20. |
| Handoff | Create/Update → AD-16 (#88/#89), Statistics → AD-17 (#91), Delete → AD-18 (#90). | Đây là luồng AC-35/danh mục. Các thao tác không hiện trên ảnh empty state và chưa có client handler. |
| Trạng thái triển khai | Tài liệu có thể mô tả contract candidate và chặn rõ chỗ thiếu. | Source UI không có; không có runtime evidence cho màn hình. |

### API #87 — contract đối chiếu

| Thành phần | Catalog/API DD trực tiếp | Local source #87 | Quyết định cho AD-15 |
|---|---|---|---|
| Request | `GET /api/v1/admin/quizzes`; Bearer JWT/Admin; query tùy chọn `course:int64`, `status:string`, `page:int32`; không body. | Route chuyển raw query đến module. Shared `ADMIN` guard chạy trước query validation và truy vấn DB. | Chỉ các query có nguồn và mapping được owner xác nhận mới được gửi. Không tự thêm search/code/size/sort. |
| Response | Catalog khai báo `ApiEnvelope<Quiz>`; API DD #87 còn `Draft — Needs Confirmation`. | Envelope thành công gồm `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; `data` là `Page<Quiz>` với `items` và `pagination`. `businessCode=DESIGN_RESOURCE_RETRIEVED`; message phụ thuộc có item hay rỗng. | Cardinality catalog/AC và source chưa thống nhất; client không được chốt mapping list trước khi có quyết định. |
| Local query | Không nêu page size/default/order hay status enum trong catalog. | `course` là signed int64; `page` signed int32 >=1, mặc định 1; `status` giữ nguyên chuỗi; count và list dùng cùng exact filters; loại `DELETED`; size cố định 20; `id ASC`; không commit. | Đây là hành vi local source, chưa được coi là API contract đã duyệt. |
| Local projection | Catalog gọi kiểu `Quiz` nhưng chưa giải quyết yêu cầu page/list. | Mỗi item có `id`, `course_id`, `title`, nullable `duration_minutes`, `passing_score` dạng decimal string, `questions=[]`. | Không có quiz code, course title, question count, status; không suy ra các giá trị này. |
| Lỗi | Catalog: 401/403/500. | 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, lỗi query/projection 500 `DESIGN_INTERNAL_ERROR`; invalid `course`/`page` local trả 422 `DESIGN_VALIDATION_ERROR` trước DB. | 422 là local derived behavior chưa có trong catalog; UI mapping vẫn chờ contract. |
| Empty/page | Catalog không quy định chi tiết. | Empty hoặc page vượt tổng trả 200; `total_pages=0` khi total=0; message `No quizzes found.` | Không đồng nhất `0/0` của prototype với trạng thái lỗi hoặc “chưa đồng bộ”. |

### Discrepancy và điều kiện chặn

1. **Response shape/cardinality:** catalog trực tiếp `ApiEnvelope<Quiz>` khác AC/list intent và local `ApiEnvelope<Page<Quiz>>`; cần owner duyệt trước khi wire UI.
2. **Thiếu cột:** ảnh có mã bài thi, khóa học, số câu hỏi và trạng thái nhưng #87 không trả các trường này. `questions=[]` là projection chưa hydrate, không phải số câu hỏi bằng 0.
3. **Search/course/status:** tìm theo tên/mã chưa có query; course select dùng slug, #87 cần numeric ID; `draft/active/closed` không có enum/mapping đã duyệt trong khi source lọc status theo raw exact text.
4. **Permission:** AC-35 yêu cầu quiz-management permission; source chỉ kiểm tra `ADMIN`. Không coi role Admin tương đương permission nghiệp vụ riêng.
5. **Schema:** source truy vấn legacy bảng `quizzes` với ID BIGINT; `DB.sql` cho phép một số cột cần projection là nullable. V1-PILOT dùng UUID `assessments`/question/options model khác. Không có bằng chứng live schema/deployment.
6. **UI/runtime:** Study Web không có source/router/client; controls/anchors trong prototype không được wire. “System normal”, scoring-engine ready, “chưa đồng bộ”, RBAC assurance và security V3 là copy tĩnh, không phải kết quả đo từ server.
7. **Visual target:** prototype rộng 1600px, cobalt và font kiểu Plus Jakarta; `.agents/web-study/design.md` hướng tới ocean-blue, Inter/system và bố cục centered/responsive. Cần áp dụng design target khi có implementation, không coi prototype là runtime.

Không có retry, timeout, deduplication, cache invalidation hay stale-response rule được #87/catalog xác định. Không có client/runtime behavior nào được xác minh trong phiên này.
