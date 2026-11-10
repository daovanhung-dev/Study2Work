# AD-12 — Danh sách bài học quản trị · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-12` |
| Module | Admin |
| Route | `/admin/lessons` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Detailed Design:** `DD BLOCKED` · **Implementation:** `IMPLEMENTATION BLOCKED` · **Study Web runtime:** `NOT VERIFIED` (`UNWIRED` trong checkout hiện tại)<br> |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-12.md](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12.md), [AD-12_PLAN.md](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12_PLAN.md), [AD-12_markers.json](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: List lesson; mở AD-13 bằng numeric `Lesson.id`; không bật search/course/type/status/paging/action mapping khi contract chưa chốt.
- In-scope: GET #82; catalog singleton `Lesson` khác local `Lesson[]`; course cần int64 nhưng mockup dùng slug, type trả 422, status exact raw string, không có pagination; CTA Add chưa có API.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-34 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | List lesson; mở AD-13 bằng numeric `Lesson.id`; không bật search/course/type/status/paging/action mapping khi contract chưa chốt. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #82
- Liên kết màn hình dự kiến: [AD-13](../AD-13-ChiTietBaiHocQuanTri/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/ready/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-12 source screen.png](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/screen_annotated.png))
- Luồng: GET #82; catalog singleton `Lesson` khác local `Lesson[]`; course cần int64 nhưng mockup dùng slug, type trả 422, status exact raw string, không có pagination; CTA Add chưa có API.
- Priority: P1; Gate/source status: **R** local route/module/query/model/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** cardinality, filter mappings, page metadata, row projection/Add API, lesson-management permission, legacy nullability/live schema và Study Web `UNWIRED` còn mở; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-12 — Danh sách bài học quản trị

> **Detailed Design:** `DD BLOCKED` · **Implementation:** `IMPLEMENTATION BLOCKED` · **Study Web runtime:** `NOT VERIFIED` (`UNWIRED` trong checkout hiện tại)<br>
> **Screen:** AD-12 · **Actor expected:** Admin có lesson-management permission theo AC-34 · **Route đề xuất:** `/admin/lessons` · **AC:** AC-34 · **API:** #82 · **Handoff:** AD-13 / #83<br>
> **Assets:** [screen nguồn](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/screen.png) · [screen có marker](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/screen_annotated.png) · [marker map](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12_markers.json) · [kế hoạch](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12_PLAN.md) · [inventory](../../list_screen.md)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Mục tiêu và expected behavior

AD-12 là danh sách bài học trong vùng quản trị đào tạo. Inventory row 70 đề xuất route `/admin/lessons`, Admin có quyền quản lý bài học, lọc danh sách theo khóa học/trạng thái/loại, mở chi tiết AD-13 và tiếp tục sang AD-14 cho update/status/delete. AC-34 mô tả chuỗi API #82 list → #83 detail → #84 update, #85 status hoặc #86 delete → reload list. Đây là expected design; Study Web chưa có route/caller để xác minh.

Catalog #82 quy định `GET /api/v1/admin/lessons`, Bearer/Admin, query tùy chọn `course:int64`, `status:string`, `type:string`, response `ApiEnvelope<Lesson>` (singular), lỗi 401/403/500. Local route hiện trả `ApiEnvelope<Lesson[]>`; catalog cardinality cần được chủ contract giải quyết. API #82 DD vẫn `Draft — Needs Confirmation`.

### Current behavior đã xác minh

- Trong checkout hiện tại không có editable Study Web `src`, `package.json`, router hoặc API client. `code.html` là prototype tĩnh, anchor dùng `href="#"`, controls không có event handler/data binding; không tìm thấy `fetch`/XHR/API URL/timer. Trạng thái: `UNWIRED`; không có runtime evidence.
- API #82 có route/module/query/model và test source. Shared Bearer/JWT role guard chỉ xác nhận `ADMIN`, chạy trước query parsing/DB; không chứng minh lesson-management permission của AC-34.
- `course` nhận signed int64 gồm giá trị âm/0; sai kiểu/overflow trả 422. Bất kỳ `type` được gửi nào, kể cả empty string, trả 422 `DESIGN_VALIDATION_ERROR` / `UNSUPPORTED_FILTER`. `status` được dùng như chuỗi exact, không enum/normalize/whitelist.
- Query đọc candidate legacy BIGINT `lessons`, lọc equality tùy chọn `course_id`/`status`, bỏ `status='DELETED'`, sắp theo `course_id ASC NULLS LAST, sort_order ASC NULLS LAST, id ASC`; không join, type filter, total, pagination hay mutation. Empty result là HTTP 200 `data: []`.
- Local response là `ApiEnvelope<Lesson[]>`, direct `data` list. Các trường map: `id`, `course_id`, `name→title`, nullable `content`, nullable `video_url`, `sort_order→order`, `status`. DDL legacy cho phép `course_id`, `sort_order`, `status` NULL dù response yêu cầu non-null; projection không hợp lệ trở thành safe 500 + rollback.
- Checked-in DDL không xác nhận live schema/deployment. BIGINT legacy model khác V1-PILOT UUID model. API tests dùng fake DB; test source đã đọc, không chạy trong phiên này.

### Tác nhân, điều kiện và bảo mật

- **Actor dự kiến:** Admin có lesson-management permission theo AC-34. **Current API:** role `ADMIN`; permission chi tiết chưa có bằng chứng.
- **Precondition thiết kế:** authenticated session, authorization hợp lệ, route `/admin/lessons`; option/query mapping chỉ được bật khi contract xác nhận. Current backend chạy authorization trước parse filter và truy cập DB.
- **Postcondition:** chỉ hiển thị collection đọc được; #82 không thay đổi dữ liệu. Mở AD-13 là điều hướng thiết kế bằng numeric `Lesson.id` nếu server trả về một row.
- Không coi badge `RBAC`, `SYSTEM NORMAL`, “API #82 Endpoint Active”, “Đồng bộ trực tiếp từ CSDL LMS” là kết quả kiểm tra runtime hoặc health/DB signal.

### API và liên kết màn hình

| API | Catalog contract | Local source behavior | Tình trạng |
|---|---|---|---|
| #82 `GET /api/v1/admin/lessons` | Bearer/Admin; query `course?:int64`, `status?:string`, `type?:string`; `ApiEnvelope<Lesson>`; catalog 401/403/500 | Role `ADMIN`; `course` signed int64; `type` unsupported→422; `status` exact; trả `ApiEnvelope<Lesson[]>`; DB/projection failures safe 500 | `R` source-backed locally; contract discrepancy; tests not run |
| #83 `GET /api/v1/admin/lessons/{lesson_id}` | Handoff đến AD-13 theo AC-34; path ID là numeric int64 trong route hiện tại | Route được đăng ký; AD-13 source/response chưa được đặc tả trong phiên này | Handoff candidate; không suy diễn row action |

Liên kết thiết kế: AD-01/Admin shell → AD-12 → AD-13 → AD-14; AD-14 thành công thì AC-34 dự kiến reload AD-12. Route, client navigation, filter preservation và reload chưa được triển khai/xác minh.

### Discrepancies và blocker

| Chủ đề | Expected/design hoặc mockup | Current source | Trạng thái / ảnh hưởng |
|---|---|---|---|
| Cardinality | Catalog/AC ghi `ApiEnvelope<Lesson>` đơn. | Local #82 trả `ApiEnvelope<Lesson[]>`. | `DISCREPANCY`; owner cần chốt schema trước khi client map. |
| Search | Mockup tìm tên bài học hoặc mã bài giảng. | Không có `q`, lesson-code field hoặc search query trong #82/`Lesson`. | `BLOCKER`; không gửi query giả định. |
| Course | Mockup dùng lựa chọn slug (`fe`, `be`, `ux`, `qa`). | API nhận `course` signed int64; query dùng `course_id`; không có option/mapping source được duyệt. | `BLOCKER`; không tự ánh xạ slug hoặc gọi API khác để suy ra. |
| Type/status | Mockup có `video/reading/assignment/quiz`, `active/draft/hidden`. | Không có lesson type field trong model/query/DDL candidate; supplied `type` trả 422; status là exact string. | `BLOCKER`; không bật filter trước mapping/enum được duyệt. |
| Pagination | Mockup hiển thị số dòng và `0/0`, Previous/Next. | API không có page/size/count/total; trả toàn bộ row phù hợp. | `BLOCKER`; `0/0` chỉ là nội dung tĩnh. |
| Table/actions | Mockup có course, format, order, status, actions; empty state không có row. | API có numeric `course_id`, không có course title, format hay pagination; #82 read-only. | `BLOCKER`; không bịa giá trị hoặc thao tác row. Numeric `Lesson.id` → AD-13 là candidate. |
| Add CTA | “Thêm bài học mới”. | Không có create API trong AC-34/#82–#86. | `BLOCKER`; chưa có API hoặc destination xác nhận. |
| Authorization/schema | AC cần lesson-management permission. | Guard chỉ check `ADMIN`; legacy DDL có NULL ở cột response bắt buộc; live schema chưa xác minh. | `OPEN`; phải chốt quyền và schema trước triển khai. |
| Copy/design | DB sync/API active/SCORM-xAPI-DRM claims; mockup cobalt, Plus Jakarta Sans, full width. | #82 không cung cấp các assurance này; `.agents/web-study/design.md` hướng tới ocean tokens, Inter/system, content width khoảng 1120px. | Static-only/design discrepancy; giữ nguyên asset, không coi là runtime fact. |
