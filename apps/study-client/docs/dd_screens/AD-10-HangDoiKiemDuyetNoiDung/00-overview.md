# AD-10 — Hàng đợi kiểm duyệt nội dung · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-10` |
| Module | Admin |
| Route | `/admin/content/pending` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Detailed Design:** `DD BLOCKED` · **Implementation:** `IMPLEMENTATION BLOCKED` · **Study Web runtime:** `NOT VERIFIED` (`UNWIRED` in current checkout)<br> |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
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
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-10 source screen.png](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/screen_annotated.png))
- Luồng: GET #78 → chọn content_id mở AD-11.
- Priority: P1; Gate/source status: **R** local #78 route/module/query/model/validator/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** catalog/AC singular Content vs local Page; pagination/order/422 và type enum còn DERIVED; thiếu course title, author, submitted time, version; stale/deleted visibility, moderation permission, live schema/deployment chưa chốt; Study Web UNWIRED. **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-10 — Hàng đợi kiểm duyệt nội dung

> **Detailed Design:** `DD BLOCKED` · **Implementation:** `IMPLEMENTATION BLOCKED` · **Study Web runtime:** `NOT VERIFIED` (`UNWIRED` in current checkout)<br>
> **Screen:** AD-10 · **Actor dự kiến:** Admin theo AC-33; fine-grained moderation permission chưa xác nhận · **Route đề xuất:** `/admin/content/pending` · **AC:** AC-33 · **API chính:** #78<br>
> **Assets:** [screen nguyên trạng](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/screen.png) · [screen đánh số](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/screen_annotated.png) · [marker map](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10_markers.json) · [kế hoạch](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10_PLAN.md)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Expected behavior

Inventory đề xuất AD-10 là trang hàng đợi Content `PENDING_REVIEW`, lọc theo type/course/page, có trạng thái rỗng và mở AD-11 bằng `content_id`. AC-33 mô tả Admin mở queue → GET #78 → chọn Content → GET #79 để xem Content/version/author → approve bằng #80 hoặc reject bằng #81 kèm reason → reload queue. AC-33 là nguồn expected flow; mockup không định nghĩa permission, enum, search contract, sort hoặc chính sách revision.

API catalog và AC-33 hiện khai báo GET `/api/v1/admin/content/pending`, Bearer/Admin, query tùy chọn `type:string`, `course:int64`, `page:int32`, response `ApiEnvelope<Content>` đơn và lỗi 401/403/500. API #78 DD còn `Draft — Needs Confirmation`.

### Current behavior và trạng thái bằng chứng

| Chủ đề | Expected / contract | Current source hoặc prototype | Trạng thái |
|---|---|---|---|
| Route và quyền | Route đề xuất `/admin/content/pending`; AC-33 actor Admin. | Không có editable Study Web app/router/client source trong checkout. #78 hiện kiểm tra shared JWT role `ADMIN`; finer moderation permission không có bằng chứng. | Route `UNWIRED`; permission `OPEN`. |
| Queue và response | Queue nhiều Content; catalog/AC lại ghi singular `Content`. | Local #78 trả `ApiEnvelope<Page<ContentResponse>>`, `items` + `pagination`; đọc active rows có `status='PENDING_REVIEW'`. | `DISCREPANCY`; Page/pagination là local-derived, cần owner chốt. |
| Bộ lọc | Inventory nói type/course/page. | Local #78 hỗ trợ exact raw `type`, signed-int64 `course`, positive-int32 `page` (mặc định 1). Không có keyword. | Exact filtering/page behavior là current local source; approval/API catalog chưa đồng bộ. |
| Cột bảng | Mockup có ID, title, format, course, lecturer, submitted time, action. | #78 chỉ trả `id`, `course_id`, `content_type`, `title`, object `payload`, `status`, nullable `parent_id`, `order`. Không trả course title, lecturer/author, submitted time hoặc version. | `BLOCKER`: không thể populate đủ các cột từ #78. |
| Revision và detail | AC-33 #79 cần Content/version/author trước quyết định. | #78 đọc current logical `contents` row; local #79 cũng chỉ trả Content projection tám field, không join author/version. | `OPEN`: revision binding, stale queue và metadata source chưa được quyết định. |
| Persistence | Inventory cũ ghi Content persistence không có trong DDL. | Checked-in legacy `DB.sql` và migrations 006/007 có `contents`/`content_versions` BIGINT; V1-PILOT UUID `content_blocks`/review model là schema khác. | Inventory claim cũ không còn đúng với local files; live schema/deployment vẫn `NOT VERIFIED`. |
| Prototype/runtime | Mockup mô tả search, filter, refresh, 30 giây auto-sync và rubric. | HTML tĩnh; không có fetch/XHR/API URL/interval. Search/select không handler; refresh chỉ local spinner 700 ms; “kiểm tra nội dung mới” và pagination disabled. | `UNWIRED`; static copy không phải runtime evidence. |

### Actor, điều kiện và dữ liệu

- **Actor expected:** Admin trong AC-33. API catalog yêu cầu Bearer JWT/Admin; current #78 guard kiểm tra role `ADMIN` trước khi parse query và đọc DB. Không suy ra permission riêng cho moderation từ role chung.
- **Điều kiện vào:** Người dùng đã xác thực và được phép vào màn theo policy sẽ được duyệt; route là đề xuất vì Study Web chưa wire. Queue lấy Content `PENDING_REVIEW` theo AC-33.
- **Dữ liệu danh sách local:** Item #78 hiện có `id:int64`, `course_id:int64`, `content_type:string`, `title:string`, `payload:object`, `status:string`, `parent_id:int64|null`, `order:int32` theo reusable Content projection. Không có mapping cho tên khóa học, người gửi, thời điểm gửi hoặc revision.
- **Sau khi chọn:** Candidate handoff là `data.items[].id` làm `content_id` của AD-11/#79. Đây là nối kỹ thuật từ local Page và route #79; AC-33 chưa chốt version token/revision hoặc hành vi khi item đã stale.
- **Sau quyết định:** AC-33 yêu cầu reload queue sau #80/#81; submit, reason, success/error UI thuộc AD-11. Màn này chỉ nhận queue state khi có route/client được wire.
- **Empty state:** Mockup hiện empty. Local #78 có thể trả Page rỗng hợp lệ với 200; catalog cardinality chưa thống nhất.

### Nguồn truy vết

- [Screen inventory](../../list_screen.md) · [Global screen plan](../../screen_stitch/dd_screens/PLAN.md) · [AC-33 Admin flow](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) · [API catalog](../../../../../docs/lists/list_api.md)
- [API #78 route](../../../../study-server/app/api/v1.py) · [#78 model](../../../../study-server/app/modules/admin/api_78_admin_content_pending/models.py) · [#78 validator](../../../../study-server/app/modules/admin/api_78_admin_content_pending/validate.py) · [#78 view](../../../../study-server/app/modules/admin/api_78_admin_content_pending/view.py) · [#78 query](../../../../study-server/app/modules/admin/api_78_admin_content_pending/query.py)
- [#78 focused test source](../../../../study-server/tests/modules/admin/api_78_admin_content_pending/test_admin_content_pending.py) · tests are source evidence only; none were run for AD-10.
- [#78 overview](../../../../study-server/docs/dd/78_admin_content_pending/02_Overview.md) · [request](../../../../study-server/docs/dd/78_admin_content_pending/03_Request.md) · [mapping](../../../../study-server/docs/dd/78_admin_content_pending/05_Data_Mapping.md) · [errors](../../../../study-server/docs/dd/78_admin_content_pending/06_Error.md) · [open questions](../../../../study-server/docs/dd/78_admin_content_pending/OPEN_QUESTIONS.md)
- [API #79 route and model](../../../../study-server/app/api/v1.py) · [#79 Content model](../../../../study-server/app/modules/admin/api_79_admin_content_detail/models.py) · [legacy candidate DDL](../../../../../infra/postgres/study-server/DB.sql) · [migration 006 contents](../../../../../infra/postgres/study-server/migrations/006_contents.sql) · [migration 007 content versions](../../../../../infra/postgres/study-server/migrations/007_content_versions.sql)
- [Study Web design target](../../../../../.agents/web-study/design.md) · [Study Web scope index](../../../../../.agents/web-work/study/INDEX.md)
