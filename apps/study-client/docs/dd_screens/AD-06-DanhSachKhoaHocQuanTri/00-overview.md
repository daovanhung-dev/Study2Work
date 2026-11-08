# AD-06 — Danh sách khóa học quản trị · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-06` |
| Module | Admin |
| Route | `/admin/courses` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Detailed Design status:** `DD BLOCKED` · **Implementation:** `IMPLEMENTATION BLOCKED` · **Study Web runtime:** `NOT VERIFIED` (`UNWIRED` in checked-in workspace)<br> |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-06.md](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/AD-06.md), [AD-06_PLAN.md](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/AD-06_PLAN.md), [AD-06_markers.json](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/AD-06_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Danh sách course; search tên/mã/mentor và filter/status chỉ bật sau khi contract xác nhận; mở AD-07 bằng numeric `Course.id`.
- In-scope: GET #73 chỉ hỗ trợ raw exact `status`, signed-int64 `mentor`, category bị reject 422, page int32; size=20, `courses.id ASC`; không có search/KPI/course code/lesson count. AC-32 đi qua #74 detail trước #76 status; chưa xác nhận action trực tiếp từ row. #77 đánh dấu `DELETED`, #73 không loại status đó.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-32 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Danh sách course; search tên/mã/mentor và filter/status chỉ bật sau khi contract xác nhận; mở AD-07 bằng numeric `Course.id`. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #73
- Liên kết màn hình dự kiến: [AD-07](../AD-07-ChiTietKhoaHocQuanTri/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | initial/loading/ready/empty/out-of-range-empty/unauthorized/forbidden/validation-error/service-error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-06 source screen.png](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/screen_annotated.png))
- Luồng: GET #73 chỉ hỗ trợ raw exact `status`, signed-int64 `mentor`, category bị reject 422, page int32; size=20, `courses.id ASC`; không có search/KPI/course code/lesson count. AC-32 đi qua #74 detail trước #76 status; chưa xác nhận action trực tiếp từ row. #77 đánh dấu `DELETED`, #73 không loại status đó.
- Priority: P1; Gate/source status: **R** source/API #73; test report 2026-11-01 pass trên temporary schema; API DD Draft; **DD BLOCKED; IMPLEMENTATION BLOCKED:** search, status/DELETED visibility, category relation, mentor options, KPI, course code/lesson count, export/create/sync/policy, Admin permission mapping và Study Web UNWIRED còn mở; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-06 — Danh sách khóa học quản trị

> **Detailed Design status:** `DD BLOCKED` · **Implementation:** `IMPLEMENTATION BLOCKED` · **Study Web runtime:** `NOT VERIFIED` (`UNWIRED` in checked-in workspace)<br>
> **Screen:** AD-06 · **Actor:** Admin · **Route đề xuất:** `/admin/courses` · **AC:** AC-32 · **API chính:** #73<br>
> **Assets:** [screen nguyên trạng](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/screen.png) · [screen đánh số](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/screen_annotated.png) · [marker map](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/AD-06_markers.json) · [kế hoạch](../../screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/AD-06_PLAN.md)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Expected behavior

AD-06 là danh sách quản trị khóa học theo inventory. Admin có quyền quản trị course vào từ Admin shell, xem/lọc danh sách theo hợp đồng được duyệt, rồi mở AD-07 để xem một khóa học. AC-32 mô tả chuỗi `GET #73 → GET #74 → #75 update / #76 status / #77 delete → reload list`; thay đổi dữ liệu không thuộc thao tác trên trang danh sách này.

Inventory đề xuất tìm kiếm theo tên/mã/giảng viên, filter mentor/status, xem chi tiết và sửa trạng thái. Những yêu cầu đó chưa đồng nghĩa API hiện hành hỗ trợ tất cả. Expected behavior được kiểm soát bởi AC-32 và API catalog #73; phần chưa có contract được ghi là blocker.

### Expected behavior và current behavior

| Chủ đề | Expected / contract | Current source hoặc prototype | Trạng thái |
|---|---|---|---|
| Route/UI | `/admin/courses` theo inventory. | Không có Study Web source/router; `code.html` là mock tĩnh. | `UNWIRED` |
| Access | AC-32 yêu cầu Admin có course-management permission. API catalog ghi Bearer JWT/Admin. | #73 dùng shared JWT guard với role `ADMIN`; không kiểm tra riêng permission course-management. | Mapping `ADMIN` ↔ AC permission cần xác nhận. |
| List | GET #73 có status, mentor, category, page. | Route/module/query/view/test có trong local source. Status exact-match; mentor int64; category bị từ chối; page 1-based, 20 rows, ID tăng dần. | Source-backed; DD API vẫn Draft. |
| Search | Inventory/mockup nói tên/mã/giảng viên. | Không có search query hoặc search handler trong #73/prototype. | `BLOCKER` |
| Dữ liệu row | Tên, mentor, fee, status có thể map từ response. | #73 trả `id`, `title`, `price`, `status`, `mentor`; không trả course code hay lesson count. | Mapping một phần; code/lesson count `BLOCKER`. |
| KPI | Mockup có 4 summary cards. | Bốn số 0 là hard-coded. #73 chỉ trả pagination total theo filter hiện tại. | `BLOCKER` — không có aggregate source. |
| Category/status | Mockup khóa category và có status lowercase. | Category có giá trị hợp lệ trả 422. Status không có enum/normalization; #77 đặt `DELETED`, #73 không loại status này. | `BLOCKER` — cần relation/status/visibility policy. |
| Controls | Mockup có Export/Add/refresh/sync/manual/governance links. | Không có handler; #73 chỉ list. AC-32 không cung cấp create/export/manual-sync cho AD-06. | `BLOCKER` |
| API test evidence | Chỉ test chứng minh tình huống trên môi trường và schema đã chạy. | Report 2026-11-01 ghi focused HTTP 20/20 pass sau nullable-cast fix trên temporary test branch; focused 178 tests/full suite 1326 pass khi đó. | Không chạy lại trong phiên; không phải production evidence. |
| Status action entry | Inventory purpose nhắc sửa trạng thái; AC-32 sequence là list → #74 detail → lựa chọn #75/#76/#77. | AD-06 inventory links AD-07; mockup chỉ có một cột thao tác trống trong empty state. | Chưa xác nhận status action trực tiếp trên list; theo AC target handoff qua AD-07/AD-09. |
| Visual system | Study Web guide là target design. | Mockup cobalt palette/Plus Jakarta Sans khác ocean-blue semantic tokens/Inter-system được guide nêu. | Cần align khi Study Web được wire; screenshot không chứng minh implementation. |

### Actor, điều kiện và liên kết màn hình

| Thuộc tính | Mô tả |
|---|---|
| Actor/role mục tiêu | Admin có quyền course management theo AC-32. Hiện API #73 kiểm tra claim role `ADMIN`; mapping quyền phải được owner xác nhận. |
| Tiền điều kiện | Phiên đăng nhập hợp lệ; quyền Admin/course-management được xác định; route/API client đã được nối; local API đang dùng candidate schema tương thích. Các điều kiện deploy/live chưa xác minh. |
| Hậu điều kiện đọc | Hiển thị một trang `Page<Course>` hoặc trạng thái rỗng/lỗi. GET không commit hay mutate dữ liệu. |
| Entry | Admin shell / AD-01 có link AD-06 theo inventory. Shell route hiện chưa có trong Study Web source. |
| Next | Chọn một course row/action mở AD-07 với numeric `Course.id`; AD-07 sẽ dùng API #74. Không tạo đặc tả AD-07 trong tài liệu này. |
| Related flow | Sau AD-07, AC-32 tiếp tục sang AD-08/#75 hoặc AD-09/#76/#77; sau mutation mới reload #73 theo policy. |

### Quy tắc nghiệp vụ và bảo mật

- Dùng contract API #73: `GET /api/v1/admin/courses`, Bearer JWT/Admin, query tùy chọn `status`, `mentor`, `category`, `page`. Không thêm `q`, `size`, `sort` hoặc KPI endpoint.
- Không gửi literal `status=all`; khi chưa chọn filter thì bỏ query. Với filter cụ thể, status được gửi nguyên chuỗi chỉ sau khi status vocabulary/casing được duyệt. Source không whitelist/normalize status.
- `mentor` là signed int64 trong source. Source không áp positive-only validation; option label/value list chưa có API contract. Không lấy danh sách mentor từ một trang course để coi là đầy đủ.
- Category phải giữ disabled cho đến khi quan hệ course-category và contract được xác nhận. Một category int64 hợp lệ hiện bị #73 trả 422.
- Không dùng `Course.id` thay cho “mã khóa”. Không suy ra số bài học, aggregate KPI, moderation state, sync status hoặc permission assurance.
- `SYSTEM NORMAL`, RBAC, API-path footer và governance copy là nội dung tĩnh của mockup, không phải health, authorization, source-of-truth hay moderation evidence.
- #77 source đánh dấu `status='DELETED'`, nhưng #73 không loại status này. Cách ẩn/hiện bản ghi xóa và status transition phải được chốt; không tự thêm filter ở UI.
- Giá do response cung cấp ở dạng decimal string chính xác; UI không parse sang floating point nếu cần giữ độ chính xác. Locale/currency formatting chưa được contract định nghĩa.

### Nguồn truy vết

- Inventory: [list_screen.md](../../list_screen.md), AD-06 row 64; global tracking: [dd_screens/PLAN.md](../../screen_stitch/dd_screens/PLAN.md).
- AC/API: [AC-32 Admin Management diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio), [API catalog](../../../../../docs/lists/list_api.md), [API #73 DD overview](../../../../study-server/docs/dd/73_admin_courses_list/02_Overview.md), [API #73 open questions](../../../../study-server/docs/dd/73_admin_courses_list/OPEN_QUESTIONS.md).
- Runtime source: [#73 route](../../../../study-server/app/api/v1.py), [#73 validation](../../../../study-server/app/modules/admin/api_73_admin_courses_list/validate.py), [#73 query](../../../../study-server/app/modules/admin/api_73_admin_courses_list/query.py), [#73 view](../../../../study-server/app/modules/admin/api_73_admin_courses_list/view.py), [shared response model](../../../../study-server/app/modules/guest/_shared/course_catalog/models.py), [#77 soft-delete query](../../../../study-server/app/modules/admin/api_77_admin_course_delete/query.py).
- Test evidence (read only in this session): [#73 test module](../../../../study-server/tests/modules/admin/api_73_admin_courses_list/test_admin_courses_list.py) and [2026-11-01 API test report](../../../../study-server/docs/testing/api-test-report-2026-11-01.md).
- Persistence/client boundary: [legacy candidate DB.sql](../../../../../infra/postgres/study-server/DB.sql), [Study Web design guide](../../../../../.agents/web-study/design.md), `.agents/web-work/study/` source-status context.
