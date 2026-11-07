# AD-12 — Kế hoạch Detailed Design

## 1. Phạm vi và kết quả cần tạo

- Phiên này chỉ hoàn thiện **AD-12 — Danh sách bài học quản trị**; không author AD-13.
- Giữ nguyên `screen.png` và `code.html`; tạo kế hoạch này trước marker, ảnh chú thích và DD.
- Tạo `AD-12_markers.json`, `AD-12_markers.svg`, `screen_annotated.png` và `AD-12.md` với A–F, mỗi marker ánh xạ tới đúng một hàng C.
- Đối chiếu AC-34, API #82, API #83 handoff tới AD-13, Study Web design guide và current Study Server source; cập nhật inventory, reverse API index, global tracker và worklog.
- Không suy ra implementation/runtime từ prototype. Các quyết định contract còn mở tiếp tục là blocker; API #82 DD giữ trạng thái `Draft — Needs Confirmation`.

## 2. Expected behavior và current behavior

### Expected behavior

- Inventory row 70: route đề xuất `/admin/lessons`, actor Admin theo AC-34 với lesson-management permission; list theo course/status/type, thao tác sửa và mở AD-13; trạng thái dự kiến loading/empty/ready/error.
- AC-34 flow: #82 list → #83 detail → #84 update, #85 status hoặc #86 delete → reload list. Detail handoff dùng ứng viên `Lesson.id` số nguyên 64-bit; chưa suy ra row action ngoài điều hướng tới AD-13.
- Catalog #82: `GET /api/v1/admin/lessons`; Bearer/Admin; query tùy chọn `course:int64`, `status:string`, `type:string`; success `ApiEnvelope<Lesson>` (singular); lỗi catalog 401/403/500.

### Current behavior đã xác minh từ source

- Study Web không có editable app source/router/package/API client trong checkout này; prototype HTML không có handler, binding, request hoặc API URL. Study Web là `UNWIRED`; runtime `NOT VERIFIED`.
- Route #82 được khai báo cục bộ với query `course`, `status`, `type`, response model `GetAdminLessonsEnvelope` (`Lesson[]`). Bearer/JWT role `ADMIN` được kiểm tra trước query parsing/DB; quyền riêng lesson-management của AC-34 chưa được chứng minh.
- `course` parse signed-int64 (âm/0 được nhận); sai kiểu hoặc overflow trả 422. `type` có mặt—even empty string—trả 422 `DESIGN_VALIDATION_ERROR/UNSUPPORTED_FILTER`. `status` là chuỗi exact, không enum/normalize/whitelist.
- SQL đọc candidate legacy BIGINT `lessons`; lọc equality tùy chọn trên `course_id`/`status`, loại `status='DELETED'`, sắp `course_id ASC NULLS LAST, sort_order ASC NULLS LAST, id ASC`. Không join course, không type, count, pagination, mutation hoặc total.
- Response map `id`, `course_id`, `name→title`, nullable `content`, nullable `video_url`, `sort_order→order`, `status`. `course_id/order/status` bắt buộc trong response nhưng có thể NULL theo checked-in legacy DDL; projection lỗi trả safe 500 + rollback. Empty list là HTTP 200 với `data: []`.
- Mockup có keyword/lesson code, course slug options, type/status choices, table columns course/format/actions, pagination, Add CTA, “API active”, “DB sync” và SCORM/xAPI/DRM claims; #82 không hỗ trợ phần lớn các dữ kiện đó. Không có create-lesson route trong AC-34/#82–#86.
- API #82 DD đang `Draft — Needs Confirmation`; live DB/deployment và V1-PILOT UUID schema không được xác minh. Test source dùng fake DB, đã đọc nhưng không chạy trong phiên này.

## 3. Discrepancies / blockers phải giữ trong DD

1. Catalog/AC mô tả `ApiEnvelope<Lesson>` đơn; local route trả collection `ApiEnvelope<Lesson[]>` không pagination.
2. Mockup keyword/lesson code không có query hoặc field tương ứng. Course options là slug trong UI, trong khi API cần int64; không có mapping/options source được duyệt.
3. UI type filter không được model/DDL/query hỗ trợ; API #82 từ chối mọi `type` đã gửi với 422. UI status `active/draft/hidden` không được map sang raw exact `status`.
4. Mockup paging/total không thể ánh xạ từ API. Bảng course chỉ có `course_id`; format không có field; thao tác row chưa có screenshot row thực. `Add lesson` không có API tạo được catalog/AC xác nhận.
5. AC-34 yêu cầu lesson-management permission; source chỉ kiểm tra role `ADMIN`. Checked-in BIGINT DDL cho phép NULL ở các cột response bắt buộc; live schema chưa xác minh.
6. “API Endpoint Active”, “Đồng bộ trực tiếp”, “System Normal”, SCORM/xAPI/DRM là copy tĩnh, không phải health/feature evidence. Empty array chỉ nghĩa là không có dòng phù hợp.
7. `.agents/web-study/design.md` là target UI; mockup cobalt/Plus Jakarta Sans/full-width lệch ocean tokens/Inter/system font và content width khoảng 1120px. Ghi nhận, không sửa nguồn ảnh.

## 4. Kế hoạch marker

Ảnh nguồn `1600×1301`; tạo 42 marker theo thứ tự đọc từ shell đến footer. Tọa độ trong JSON/SVG là tâm marker trên ảnh nguồn, mỗi marker đánh số tuần tự và giữ circle/stroke trong bounds.

| Marker | Phần tử được ánh xạ |
|---:|---|
| #1–#6 | Brand; nav Tổng quan, Người dùng, Khóa học & Nội dung, Kiểm duyệt, Báo cáo |
| #7–#9 | Badge System Normal; chuông thông báo; danh tính Admin/avatar |
| #10–#11 | Breadcrumb shell; copy RBAC |
| #12–#13 | Breadcrumb Quản trị đào tạo; crumb Quản lý bài học |
| #14–#17 | H1; subtitle; badge API #82; CTA Thêm bài học mới |
| #18–#19 | Tiêu đề vùng lọc; claim “Đồng bộ trực tiếp từ CSDL LMS” |
| #20–#24 | Input tìm kiếm; select khóa học; select loại bài học; select trạng thái; Làm mới |
| #25 | Header bảng gồm bảy cột: mã, tiêu đề, khóa học, định dạng, thứ tự, trạng thái, thao tác |
| #26–#30 | Icon empty; heading; mô tả; nút refresh disabled; nút reset filter |
| #31–#34 | Summary số dòng; Previous; số trang `0/0`; Next |
| #35–#38 | Icon compliance; heading; claim SCORM/xAPI/DRM; badge API 82/SCORM 2004 |
| #39–#42 | Copyright/system footer; privacy; RBAC; technical support |

DD mục C phải có chính xác một hàng cho từng marker #1–#42. Tạo overlay SVG cùng ID/tọa độ với JSON; render overlay 2× (`3200×2602`) và ghép lên ảnh gốc đã resize 2×, không chỉnh sửa `screen.png`.

## 5. Events cần đặc tả

1. **EV-01 — Load lesson list:** route entry → #82; nêu auth-first, query parsing, SQL ordering/tombstone, array mapping, empty và lỗi; không khẳng định client caller hiện có.
2. **EV-02 — Nhập tìm kiếm:** prototype không có handler/query `q`; không gửi tên bài học/mã giảng viên như thể #82 hỗ trợ; cần contract trước khi bật.
3. **EV-03 — Chọn khóa học:** UI slug không ánh xạ int64. Chỉ gửi `course=<Course.id>` sau khi có option source/approved handoff; parse/range/error hiện tại do #82.
4. **EV-04 — Chọn loại bài:** mọi `type` supplied trả 422 current source; không gửi tới #82 đến khi contract/source được bổ sung.
5. **EV-05 — Chọn trạng thái:** current query exact string, không whitelist; không gửi UI alias trước khi status mapping được duyệt.
6. **EV-06 — Refresh/reset filters:** refresh gọi lại list với filter đã được xác nhận; reset xóa client filter rồi load lại. Đây là hành vi thiết kế cần wire; prototype chỉ có nút tĩnh, empty-state refresh đang disabled.
7. **EV-07 — Mở detail từ row:** truyền numeric `Lesson.id` tới AD-13/#83 candidate; source API #83 route tồn tại, nhưng không suy ra action cell hoặc quyền truy cập detail từ dòng empty mockup.
8. **EV-08 — Add lesson CTA:** không gọi API; create route không thấy trong AC-34/#82–#86. Giữ CTA blocked/hidden đến khi có contract và màn hình đích.
9. **EV-09 — Shell, empty state, pagination/compliance/footer:** anchor/action chưa có runtime; paging không được API cung cấp; copy compliance và status badges chưa có backend evidence. Không biến static label thành trạng thái hoạt động.

## 6. Trạng thái, access và điều hướng

- Candidate UI state: `UNWIRED`, `loading`, `ready`, `empty`, `validation-error`, `unauthorized`, `forbidden`, `service/network-error`; đây là DD target state, chưa phải client implementation.
- Current server outcomes: 200 list (có thể `[]`), 401 auth, 403 role, 422 malformed/overflow `course` hoặc supplied `type`, 500 DB/projection failure; catalog #82 errors 401/403/500 chưa liệt kê local 422.
- Expected navigation: AD-11/AD-01 admin shell → AD-12 → AD-13/#83 → AD-14/#84/#85/#86 → reload #82. Các route/handoff là thiết kế; client routing chưa có.
- Chưa có row trong empty mockup để xác minh action placement. Không tạo edit/delete/activate action trực tiếp tại AD-12; danh mục đưa thao tác tiếp theo qua AD-13/AD-14.

## 7. Thứ tự thực hiện và kiểm tra

1. [x] Đọc objective, router/context, docs worklog selector và 3 worklog được chọn; tải context web-work/server-study và registry.
2. [x] Đối chiếu ảnh/HTML, inventory, AC-34, API #82 DD/catalog, route/module/query/model/DDL/test source; xác nhận API #83 handoff candidate.
3. [x] Lưu plan trước markers, annotation và DD.
4. [x] Tạo 42 marker JSON/SVG, render annotated PNG 2× và kiểm tra trực quan.
5. [x] Author A–F DD: 42 element rows; EV-01…EV-09; field mapping, validation, auth, response, errors, states/navigation và blockers.
6. [x] Cập nhật inventory AD-12 và reverse API #082 từ D sang R theo route/module/test source; cập nhật global checkpoint/worklog. Giữ API DD Draft; không sửa AD-13.
7. [x] Static audit: hash/dimensions nguồn; JSON/XML; marker order/unique IDs/coordinates/strokes; bijection C rows; links; 83 IDs/folders, core artifact count; image dimensions/readability; `git diff --check`. Không chạy application tests/runtime.
8. [x] Kết thúc AD-12; ghi rõ DD/implementation/runtime states và dừng trước AD-13.
