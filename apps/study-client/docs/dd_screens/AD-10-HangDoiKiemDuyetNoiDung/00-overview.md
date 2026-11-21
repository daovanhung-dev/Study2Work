# AD-10 — Hàng đợi kiểm duyệt nội dung · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-10` |
| Module | Admin |
| Route | `/admin/content/pending` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Detailed Design:** `DD BLOCKED` · **Implementation:** `PARTIAL SOURCE — route/page and GET #78 caller present; filter/page and empty/error states render from the local Page projection` · **Study Web runtime:** `NOT VERIFIED`<br> |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.2 / 2026-11-20 (current-source refresh and wiring sync) |
| Nguồn đối chiếu | [AD-10.md](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10.md), [AD-10_PLAN.md](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10_PLAN.md), [AD-10_markers.json](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: List pending content theo type/course/page; có trạng thái trống.
- In-scope: GET #78 → chọn content_id mở AD-11.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-33 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | List pending content theo type/course/page; có trạng thái trống. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #78
- Liên kết màn hình dự kiến: [AD-11](../AD-11-DuyetTuChoiNoiDung/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/ready/error |
| Current source | Angular Admin router/page, API caller and screen context | Route/page/#78 caller present; page states are `loading/loaded/error`, with empty state derived from `items=[]`; the exact #78 `PENDING_REVIEW` row status displays as “Đang chờ duyệt” with an unknown-value fallback; runtime/deployment remains `NOT VERIFIED`. |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-10 source screen.png](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/screen_annotated.png))
- Luồng: GET #78 → chọn content_id mở AD-11.
- Priority: P1; Gate/source status: **R** local #78 route/module/query/model/validator/test source; Angular route/page/Admin bearer caller present; API DD Draft. **DD BLOCKED; IMPLEMENTATION PARTIAL:** catalog/AC singular Content vs local Page; pagination/order/422 and type enum remain DERIVED; course title, author, submitted time, version and stale-item policy are absent; moderation permission and live schema/deployment are unresolved. **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-10 — Hàng đợi kiểm duyệt nội dung

> **Detailed Design:** `DD BLOCKED` · **Implementation:** `PARTIAL SOURCE — route/page and GET #78 caller present; filter/page and empty/error states render from the local Page projection` · **Study Web runtime:** `NOT VERIFIED`<br>
> **Screen:** AD-10 · **Actor dự kiến:** Admin theo AC-33; fine-grained moderation permission chưa xác nhận · **Route:** `/admin/content/pending` (Angular router source-present) · **AC:** AC-33 · **API chính:** #78<br>
> **Assets:** [screen nguyên trạng](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/screen.png) · [screen đánh số](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/screen_annotated.png) · [marker map](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10_markers.json) · [kế hoạch](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10_PLAN.md)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Expected behavior

Inventory đề xuất AD-10 là trang hàng đợi Content `PENDING_REVIEW`, lọc theo type/course/page, có trạng thái rỗng và mở AD-11 bằng `content_id`. AC-33 mô tả Admin mở queue → GET #78 → chọn Content → GET #79 để xem Content/version/author → approve bằng #80 hoặc reject bằng #81 kèm reason → reload queue. AC-33 là nguồn expected flow; mockup không định nghĩa permission, enum, search contract, sort hoặc chính sách revision.

API catalog và AC-33 hiện khai báo GET `/api/v1/admin/content/pending`, Bearer/Admin, query tùy chọn `type:string`, `course:int64`, `page:int32`, response `ApiEnvelope<Content>` đơn và lỗi 401/403/500. API #78 DD còn `Draft — Needs Confirmation`.

### Current behavior và trạng thái bằng chứng

| Chủ đề | Expected / contract | Current source hoặc prototype | Trạng thái |
|---|---|---|---|
| Route và quyền | Route `/admin/content/pending`; AC-33 actor Admin. | Angular Admin router registers AD10Page and AdminLayout links to it; page calls #78 through AdminApiService. #78 checks shared JWT role `ADMIN`; finer moderation permission has no evidence. | Route/page/caller `PRESENT`; runtime `NOT VERIFIED`; permission `OPEN`. |
| Queue và response | Queue nhiều Content; catalog/AC lại ghi singular `Content`. | Local #78 trả `ApiEnvelope<Page<ContentResponse>>`, `items` + `pagination`; đọc active rows có `status='PENDING_REVIEW'`. | `DISCREPANCY`; Page/pagination là local-derived, cần owner chốt. |
| Bộ lọc | Inventory nói type/course/page. | Local #78 hỗ trợ exact raw `type`, signed-int64 `course`, positive-int32 `page` (mặc định 1). Không có keyword. | Exact filtering/page behavior là current local source; approval/API catalog chưa đồng bộ. |
| Cột bảng | Mockup có ID, title, format, course, lecturer, submitted time, action. | #78 chỉ trả `id`, `course_id`, `content_type`, `title`, object `payload`, `status`, nullable `parent_id`, `order`. Không trả course title, lecturer/author, submitted time hoặc version. | `BLOCKER`: không thể populate đủ các cột từ #78. |
| Revision và detail | AC-33 #79 cần Content/version/author trước quyết định. | #78 đọc current logical `contents` row; local #79 cũng chỉ trả Content projection tám field, không join author/version. | `OPEN`: revision binding, stale queue và metadata source chưa được quyết định. |
| Persistence | Inventory cũ ghi Content persistence không có trong DDL. | Checked-in legacy `DB.sql` và migrations 006/007 có `contents`/`content_versions` BIGINT; V1-PILOT UUID `content_blocks`/review model là schema khác. | Inventory claim cũ không còn đúng với local files; live schema/deployment vẫn `NOT VERIFIED`. |
| Prototype/runtime | Mockup mô tả search, filter, refresh, 30 giây auto-sync và rubric. | HTML mockup tĩnh. Angular source calls #78, supports exact `type/course/page`, has pagination, manual refresh and loading/empty/error states; it does not implement keyword search, auto-sync or unsupported rubric/status claims. | Source partially wired; screenshot-only claims remain unsupported; runtime not verified. |

### Actor, điều kiện và dữ liệu

- **Actor expected:** Admin trong AC-33. API catalog yêu cầu Bearer JWT/Admin; current #78 guard kiểm tra role `ADMIN` trước khi parse query và đọc DB. Không suy ra permission riêng cho moderation từ role chung.
- **Điều kiện vào:** Người dùng đã xác thực và được phép vào màn theo policy sẽ được duyệt; Angular route/page and #78 caller are source-present; browser runtime remains unverified. Queue lấy Content `PENDING_REVIEW` theo AC-33.
- **Dữ liệu danh sách local:** Item #78 hiện có `id:int64`, `course_id:int64`, `content_type:string`, `title:string`, `payload:object`, `status:string`, `parent_id:int64|null`, `order:int32` theo reusable Content projection. Không có mapping cho tên khóa học, người gửi, thời điểm gửi hoặc revision.
- **Sau khi chọn:** AD10Page links the safe Content ID to AD-11/#79. This is a technical handoff from the local Page and route #79; AC-33 chưa chốt version token/revision hoặc hành vi khi item đã stale.
- **Sau quyết định:** AC-33 yêu cầu reload queue sau #80/#81; submit, reason, success/error UI thuộc AD-11. AD-10 currently reads queue state through #78; versioned stale-row handling remains open.
- **Empty state:** Mockup hiện empty. Local #78 có thể trả Page rỗng hợp lệ với 200; catalog cardinality chưa thống nhất.

### Nguồn truy vết

- [Screen inventory](../../list_screen.md) · [Global screen plan](../../screen_stitch/dd_screens/PLAN.md) · [AC-33 Admin flow](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) · [API catalog](../../../../../docs/lists/list_api.md)
- [API #78 route](../../../../study-server/app/api/v1.py) · [#78 model](../../../../study-server/app/modules/admin/api_78_admin_content_pending/models.py) · [#78 validator](../../../../study-server/app/modules/admin/api_78_admin_content_pending/validate.py) · [#78 view](../../../../study-server/app/modules/admin/api_78_admin_content_pending/view.py) · [#78 query](../../../../study-server/app/modules/admin/api_78_admin_content_pending/query.py)
- [#78 focused test source](../../../../study-server/tests/modules/admin/api_78_admin_content_pending/test_admin_content_pending.py) · tests are source evidence only; none were run for AD-10.
- [#78 overview](../../../../study-server/docs/dd/78_admin_content_pending/02_Overview.md) · [request](../../../../study-server/docs/dd/78_admin_content_pending/03_Request.md) · [mapping](../../../../study-server/docs/dd/78_admin_content_pending/05_Data_Mapping.md) · [errors](../../../../study-server/docs/dd/78_admin_content_pending/06_Error.md) · [open questions](../../../../study-server/docs/dd/78_admin_content_pending/OPEN_QUESTIONS.md)
- [API #79 route and model](../../../../study-server/app/api/v1.py) · [#79 Content model](../../../../study-server/app/modules/admin/api_79_admin_content_detail/models.py) · [legacy candidate DDL](../../../../../infra/postgres/study-server/DB.sql) · [migration 006 contents](../../../../../infra/postgres/study-server/migrations/006_contents.sql) · [migration 007 content versions](../../../../../infra/postgres/study-server/migrations/007_content_versions.sql)
- [Study Web design target](../../../../../.agents/web-study/design.md) · [Study Web scope index](../../../../../.agents/web-work/study/INDEX.md)


### Current Study Web source re-audit — 2026-11-20

- `/admin/content/pending` is registered in the Admin router and workspace navigation. AD10Page calls API #78 through AdminApiService on entry and sends only supported `type`, `course`, and `page` query values. `course` remains a raw string so signed-int64 values are not rounded; page changes are bounded by returned pagination metadata.
- The table uses source-backed Content fields only: ID, title, course ID, type, order, status. It routes to AD-11 only when the Content ID is a JavaScript safe integer; unsupported course title, author, submitted time, version, keyword search and rubric data are omitted. Error and empty states use the current response/error state.
- Manual refresh repeats GET #78 with the currently applied filters and page, and is disabled while loading. There is no polling or 30-second sync claim. The server currently returns `Page<Content>` while catalog/AC declare singular `Content`; moderation permission, author/revision metadata, live schema and browser runtime remain unresolved. No tests/build/lint/browser were run in this continuation.

### Current Study Web source re-audit — 2026-11-21

- AD10Page now requires the #78 success business code and validates the Content Page projection, fixed page size 20, requested-page echo, and total-page arithmetic before rendering. The local backend excludes null parent_id during JSON serialization, so the client accepts that field as omitted.
- After the page-shape guard, the page compares COUNT-derived expected rows with LIST results. A mismatch keeps returned rows visible, suppresses the possibly stale total and paginator, and offers a retry for the same applied type/course/page. A valid empty page beyond total_pages has its own return-to-first-page state; matching zero-result responses remain the ordinary empty state.
- The local Page-vs-catalog Content discrepancy, moderation permission, missing author/revision metadata, live schema and browser runtime remain unresolved. AD-10 remains 50% in screen_complete.md because this recovery behavior does not complete another weighted screen axis. No tests/build/lint/browser/API runtime were run.
