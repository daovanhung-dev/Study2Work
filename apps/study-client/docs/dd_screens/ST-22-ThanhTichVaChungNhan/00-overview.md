# ST-22 — Thành tích và chứng nhận · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-22` |
| Module | Student |
| Route | `/student/achievements` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Tài liệu truy vết đủ các thành phần nhìn thấy và contract hiện có, nhưng chưa thể coi là DD READY do API #38 còn câu hỏi mở về award/projection/filter/page và các claim/chứng nhận trong mockup không có nguồn xác nhận. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-22.md](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22.md), [ST-22_PLAN.md](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22_PLAN.md), [ST-22_markers.json](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Danh sách achievement theo course; tuyệt đối không tự cấp chứng chỉ.
- In-scope: GET #38 (filter course_id optional); thành tích chỉ hiển thị khi backend xác nhận.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-18 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Danh sách achievement theo course; tuyệt đối không tự cấp chứng chỉ. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #38
- Liên kết màn hình dự kiến: [ST-20](../ST-20-TongQuanTienDo/00-overview.md), [ST-09](../ST-09-TongQuanKhoaDangHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/earned/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-22 source screen.png](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/screen_annotated.png))
- Luồng: GET #38 (filter course_id optional); thành tích chỉ hiển thị khi backend xác nhận.
- Priority: P2; Gate/source status: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** API #38 Draft còn sáu câu hỏi mở về award criteria/projection, filter/access, page/order/empty và query validation; Student route/module/query/test NOT_FOUND; Study Web UNWIRED; populated PNG có certificate/proof/GPA/metrics/competency/readiness không thuộc schema `Achievement`, còn HTML là static empty fallback; ERD/DDL chỉ có khái niệm logical/derived, không có physical registry/award table hoặc live-schema proof; AC-18 tuần tự #21→#37→#38 lệch inventory ST-20 gọi #21/#38 độc lập nên chưa suy luận timing; asset dùng remote CDN/font, 1440px và royal-blue/gradient lệch Study Web target

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-22 — Thành tích và chứng nhận

> **Trạng thái:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Tài liệu truy vết đủ các thành phần nhìn thấy và contract hiện có, nhưng chưa thể coi là DD READY do API #38 còn câu hỏi mở về award/projection/filter/page và các claim/chứng nhận trong mockup không có nguồn xác nhận.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Định danh và phạm vi

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-22 — Thành tích và chứng nhận (Page) |
| Mục tiêu | Student xem các achievement đã được backend xác nhận; không tự cấp achievement/chứng chỉ trên client. |
| Actor | Student theo inventory và API catalog #38. |
| Route trong inventory | `/student/achievements`; hiện là route thiết kế, Study Web chưa có router/runtime source để xác nhận. |
| API dự kiến | GET API #38 `/api/v1/users/me/achievements`; query tùy chọn `course_id:int64`. |
| Màn hình liên quan | ST-20 tổng quan tiến độ; ST-09 tổng quan khóa đang học. Inventory liệt kê hai màn hình này là liên kết, nhưng chưa xác nhận caller, route handoff hay dữ liệu truyền. |
| Elements / events | 46 nhóm element `ST22-EL-01…46`; 15 event `ST22-EV-01…15`. Các nhóm đánh số phản ánh các cụm nhìn thấy trong PNG, không khẳng định component/runtime đã tồn tại. |
| Trạng thái | DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. |

### A.2. Expected behavior — contract và thiết kế

- Inventory ST-22 khai báo route `/student/achievements`, AC-18, API #38, danh sách achievement theo course và state `loading/empty/earned/error`. Chỉ hiển thị thành tích backend xác nhận; không tự cấp chứng chỉ.
- API catalog #38 định nghĩa Student Bearer JWT, GET `/api/v1/users/me/achievements`, query tùy chọn `course_id:int64`, response `ApiEnvelope<Page<Achievement>>`; các logical fields của `Achievement` là `id:int64`, `code:string`, `title:string`, `awarded_at:datetime`, `course_id?:int64`. Catalog quy định 200 `DESIGN_RESOURCE_RETRIEVED`, 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-18 và API #38 DD mô tả đọc achievement đã mở khóa; không có tiêu chí unlock, bảng/registry nguồn, projection, thu hồi, ý nghĩa lọc course hoặc ordering được phê duyệt. API #38 DD đang `Draft — Needs Confirmation` với sáu câu hỏi mở.
- **DISCREPANCY về thứ tự gọi:** inventory ST-20 yêu cầu #21 và #38 độc lập, trong khi AC-18 tuần tự #21 → #37 → #38. Giữ trách nhiệm #38 và các liên kết màn hình theo inventory; chưa suy luận thời điểm vào ST-22 hoặc thứ tự orchestration.
- API #38 là GET chỉ đọc, không tạo award/chứng chỉ và không có side effect mutation được khai báo.

### A.3. Current behavior và tài sản

- `screen.png` nguyên trạng 803×1600, SHA256 `cf11ec7d3e064b689c90853e275fcd65dcb828e644c495e1d9b004d58b974b4f`. Đây là mockup populated state có trust-layer/On-Chain copy, bốn metric, hai certificate card, năm competency card, next-certificate panel và footer.
- `code.html` nguyên trạng, SHA256 `abde69d2bc108b1b5bc9004896fff0ec016a61a7ec14a3a9e2b9f63ae10a5439`. HTML tĩnh mô tả empty fallback “Chưa có thành tích để hiển thị”; có Tailwind CDN/config scripts và remote Google Fonts, nhưng không có API fetch/XHR, form/input, data binding, auth guard hay app event handler. Search field và loaded-state cards/actions trong PNG không có trong HTML. PNG và HTML khác state, nội dung, header/footer và affordances.
- `screen_annotated.png` dùng PNG nguồn nguyên trạng, đặt trên canvas 907×1640 với gutter; số `#1…#46` ánh xạ một-một tới bảng C và `ST-22_markers.json`. `ST-22_markers_overlay.svg` lưu overlay vector. Ảnh nguồn và HTML được giữ nguyên.
- Study Web hiện không có editable source/package/router cho `/student/achievements`; Study Server không có route/module/query/test của API #38. Đây là trạng thái source hiện tại, không phải bằng chứng về live deployment.
- API #38 DB guide/ERD/DDL chỉ xem `achievements` là khái niệm logic/derived; không xác nhận physical table, award registry hay tiêu chí. Không có kết luận về live database.

### A.4. API #38 — contract và source status

| Thuộc tính | Giá trị được phép dùng trong DD |
|---|---|
| Method / endpoint | `GET /api/v1/users/me/achievements` |
| Authentication / actor | `Authorization: Bearer <Student JWT>` theo catalog. Mapping principal và course-level access chưa được API #38 source xác nhận. |
| Path / query | Không có path parameter. Query tùy chọn `course_id:int64`; miền, parse failure, filter semantics và access predicate chưa chốt. Không có `page`, `size` hoặc `sort` trong request catalog. |
| Body | Không khai báo request body. |
| Success | HTTP 200, `success=true`, `businessCode=DESIGN_RESOURCE_RETRIEVED`, `data: Page<Achievement>` theo catalog/guideline. `Page` có `items` và pagination metadata; nguồn/default của metadata chưa rõ khi request không có paging controls. |
| `Achievement` | `id:int64`, `code:string`, `title:string`, `awarded_at:datetime`, `course_id?:int64`. Không bao gồm file chứng chỉ, proof hash, GPA, rank, reputation, taxonomy, QR hoặc eligibility. |
| Catalog errors | HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR`. Không tự thêm 400/404/422 hoặc business code mới. |
| Current API source | API #38 DD `Draft — Needs Confirmation`; Study Server route/module/query/test `NOT_FOUND` trong source đã kiểm tra; runtime `UNWIRED / NOT VERIFIED`. |

### A.5. Discrepancy, quy tắc và bảo mật

| Vấn đề | Expected evidence | Current evidence / impact |
|---|---|---|
| Loaded state vs empty | PNG populated visual; inventory cần loading/empty/earned/error. | HTML là static empty fallback. Chưa rõ PNG là target đã duyệt hay sample/aspirational; không dùng HTML empty copy làm bằng chứng API trả rỗng. |
| Metric/certificate/proof | Mockup hiển thị 02 certificates, 14 skill badges, 850 reputation, Top 3%, GPA, issuer, proof hash, QR, PDF/social actions. | API #38 chỉ có Achievement identity/title/time/course. Không được dựng các giá trị này từ `items` hoặc tự xác nhận chứng chỉ/blockchain. |
| Competency filters | Mockup có All/Specialization/Community. | API #38 chỉ có `course_id`; taxonomy/category không có trong contract. Không chuyển các chip thành query hoặc lọc client-side chưa được phê duyệt. |
| Next credential | Mockup có readiness 72%, prerequisites và CTA. | Không có eligibility, progress, course mapping hay formula trong #38. Không tính hoặc hiển thị như dữ liệu đã xác nhận. |
| Filter/page | API có optional `course_id`, response Page. | Filter scope, global awards, ownership/access, empty shape, page/size/order/default chưa rõ; request không khai báo page controls. |
| Runtime | Route/API design có trong inventory/catalog. | Study Web route và Student #38 runtime source chưa có; không có runtime verification. |
| Visual system | `.agents/web-study/design.md` yêu cầu semantic ocean tokens, không thêm remote font/CDN, Inter/system sans-serif, khoảng 1120px content width và surfaces tiết chế. | PNG dùng royal-blue/gradient và motif blockchain; HTML tải Tailwind CDN và remote Plus Jakarta Sans, dùng `max-w-[1440px]`, primary config `#004AC6` cùng hardcoded `#0B5F8A`. Cần xác nhận alignment; DD ghi nhận discrepancy, không sửa assets gốc. |

**Bảo mật:** `/me` identity phải gắn với principal đã xác thực theo contract backend; UI không nhận `user_id` tùy ý để lấy award. Chỉ backend xác nhận `Achievement` mới có thể được hiển thị là earned. `course_id` access/enrollment policy chưa chốt. Không diễn giải logo/QR/hash/On-Chain badge như proof validity. Không cấp, sửa hoặc thu hồi award từ event phía client.

### A.6. Nguồn truy vết

- [Screen inventory và F07](../../list_screen.md) — ST-22, liên kết ST-20/ST-09, state và nguyên tắc không tự cấp.
- [API catalog](../../../../../docs/lists/list_api.md) và [API #38 overview](../../../../study-server/docs/dd/38_users_me_achievements/02_Overview.md), [request](../../../../study-server/docs/dd/38_users_me_achievements/03_Request.md), [response](../../../../study-server/docs/dd/38_users_me_achievements/04_Response.md), [open questions](../../../../study-server/docs/dd/38_users_me_achievements/OPEN_QUESTIONS.md).
- [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-18 activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- [DB table guide](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql).
- [Study Web design target](../../../../../.agents/web-study/design.md), [original screenshot](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/screen.png), [HTML companion](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/code.html), [marker map](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22_markers.json), [overlay](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22_markers_overlay.svg), [plan](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22_PLAN.md).
