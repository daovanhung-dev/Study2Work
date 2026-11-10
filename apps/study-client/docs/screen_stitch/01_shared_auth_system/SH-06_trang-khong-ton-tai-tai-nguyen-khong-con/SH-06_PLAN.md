# Kế hoạch màn hình — SH-06 Trang không tồn tại / tài nguyên không còn

> **Trạng thái kế hoạch:** `REVIEWED / SOURCE_TRACE_COMPLETE` · **Phiên:** chỉ xử lý SH-06 · **Quyết định DD sau khi rà soát nguồn:** `DD BLOCKED` cho tới khi các surface recommendation/contact/footer và sai khác AC-05 được chốt. **Route inventory:** `/not-found` (đề xuất; Study Web router/source chưa có).

## 1. Mục tiêu, phạm vi và nguồn

- Đặc tả hai nguồn vào cùng state view: route không khớp (`ROUTE_404`) và tài nguyên khóa học không tồn tại/không public (`RESOURCE_404`). Không làm lộ sự tồn tại của khóa học draft/private; không đổi 500 hoặc lỗi mạng thành 404.
- Dòng SH-06 trong `../../../list_screen.md`: route `/not-found`, AC-05, API #08, liên kết GS-01/SH-01, state `route-404/resource-404`; route đích trong inventory là GS-01 `/courses` và SH-01 `/`.
- Nguồn hình: `screen.png` (1600×1425) và `code.html`. Ảnh có header, 404 hero, CTA, “Safe Scope” notice, ba course card, contact strip và footer; HTML dùng `href="#"`, dữ liệu khóa học/learner count viết cứng, không có handler/router/API trong file.
- API #08 design contract nằm trong `../../../../../../docs/lists/list_api.md` và AC-05 trong `../../../../../study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio`. Có sai khác nhãn trạng thái: dòng SH-06 trong `list_screen.md` ghi BE `D`, nhưng API index §5 cùng file ghi #008 `R`; root API contract được đánh dấu `APPROVED_DESIGN_CONTRACT` nhưng chưa runtime-verified, còn API DD #08 ghi `Draft — Needs Confirmation`. Current Study Server route, module và test source tồn tại; không coi source/test là runtime verification. AC-05 ghi `404/403` cho nhánh course không tồn tại/PUBLISHED; API contract chỉ đặc tả 404/500 và current handler trả 404 cho invalid/missing/unpublished, 500 cho lỗi nội bộ. Không tự sửa contract hoặc ánh xạ 403 của #08.
- Current UI source: `apps/study-client/src/` và package manifest không có. `dist/` có một bundle build cũ/ignored; scan không thấy route `/not-found`, `/courses`, `/login`, 404 string hay Vue Router call. Bundle này không chứng minh SH-06 UI/routing.
- Nguồn target visual: `.agents/web-study/design.md`; nguồn current API/DB: `apps/study-server/app/api/v1.py`, module #08, shared course catalog model/helper, `infra/postgres/study-server/DB.sql`, test #08. Live database chưa được xác minh.

## 2. Expected behavior và current behavior

| Hạng mục | Expected behavior theo inventory/AC/API design | Current source evidence |
|---|---|---|
| Route 404 | `/not-found` là route/state proposal; route lỗi không yêu cầu API. CTA đi GS-01 `/courses` hoặc SH-01 `/`. | Không có client source/router. `code.html` chứa `href="#"` cho mọi anchor và không có route handler. |
| Resource 404 | API #08 `GET /api/v1/courses/{course_id}`; 404 không tiết lộ draft/private. Không gửi 500/mạng sang SH-06. | Route/module source có; query lọc `status='PUBLISHED'`; invalid ID hoặc không có dòng PUBLISHED trả 404 `DESIGN_RESOURCE_NOT_FOUND`; SQL/mapping error trả 500. |
| Thành công API #08 | Published course → GS-03/course detail theo route hợp lệ. | 200 `DESIGN_RESOURCE_RETRIEVED`; `data` là `Page<Course>` có đúng 1 item và pagination 1/1. `Course` có id, title, description?, thumbnail_url?, price dạng string, status và mentor summary. |
| 403 | Không thay bằng 404 nếu API/authorization thực sự trả 403; giữ phân nhánh access denied. | API #08 hiện public, không có 403 branch; AC-05 diagram ghi `404/403` khi course không tồn tại/PUBLISHED. Đây là discrepancy; 403 từ auth/access guard thuộc SH-05, không khẳng định do #08. |
| Gợi ý khóa học | Hiển thị dữ liệu công khai có nguồn thật hoặc bỏ khối dữ liệu mẫu. | Ba card, category tags, durations, learner counts và copy trong HTML là static content; không có API mapping/ID. API #06 là public list route nhưng chưa được khai báo như dependency SH-06. |
| Liên hệ/footer | Chỉ điều hướng tới route/contact channel đã được duyệt. | CTA hỗ trợ và 4 footer links đều `href="#"`; không có route/contact contract trong SH-06. |

## 3. Kế hoạch element và marker

Ảnh mặc định sẽ có **22 marker** theo thứ tự #1–#22. Marker khoanh các component/controls nhìn thấy; các link cùng loại trong nav group được liệt kê riêng trong thuộc tính/event của element. Các nội dung mock vẫn được đánh dấu để DD nhận diện và chặn việc dùng nhầm làm dữ liệu runtime.

| # | Element ID | Element / vùng trong ảnh | Notes |
|---:|---|---|---|
| 1 | `SH06-EL-01` | Logo + tên Study2Work ở header (`a`) | `href="#"`, chưa gắn route. |
| 2 | `SH06-EL-02` | Primary navigation group (`nav`): Trang chủ, Khóa học, Tìm kiếm | Ba anchor riêng, hiện đều là placeholder. |
| 3 | `SH06-EL-03` | Link Đăng nhập (`a`) | Route proposal `/login`; source href hiện là `#`. |
| 4 | `SH06-EL-04` | CTA Đăng ký (`a`) | Route proposal `/register`; source href hiện là `#`. |
| 5 | `SH06-EL-05` | Icon người dùng (`div` + icon) | Không có role/button/handler; không mô tả thành control đã hoạt động. |
| 6 | `SH06-EL-06` | Badge “Mã lỗi hệ thống · HTTP 404 · Resource Not Found” | Static mock; route 404 không nhất thiết có API businessCode. |
| 7 | `SH06-EL-07` | Số 404 + divider trang trí | Status illustration; H1 hiện chứa số 404. |
| 8 | `SH06-EL-08` | Heading lỗi | Nội dung tiếng Việt tĩnh trong prototype. |
| 9 | `SH06-EL-09` | Description lỗi | Không khẳng định resource đã xóa nếu nguồn chỉ cho biết không tồn tại/không public. |
| 10 | `SH06-EL-10` | Primary CTA về danh sách khóa học (GS-01) | Route đề xuất `/courses`. |
| 11 | `SH06-EL-11` | Secondary CTA về trang chủ (SH-01) | Route đề xuất `/`. |
| 12 | `SH06-EL-12` | Safe Scope notice card | Copy về draft/private được đối chiếu với API #08; nhãn “Standard Spec” là mock. |
| 13 | `SH06-EL-13` | Header/description “Khám phá các khóa học khả dụng” | Không có nguồn course recommendation hiện hành trong SH-06 contract. |
| 14 | `SH06-EL-14` | Link “Xem tất cả” | Placeholder route; target proposal GS-01 `/courses`. |
| 15 | `SH06-EL-15` | Course card 1 | Toàn bộ tên/category/duration/description/count là static mock; không có course ID. |
| 16 | `SH06-EL-16` | Course card 2 | Toàn bộ nội dung static mock; không có course ID. |
| 17 | `SH06-EL-17` | Course card 3 | Toàn bộ nội dung static mock; không có course ID. |
| 18 | `SH06-EL-18` | Help strip icon + prompt | Copy tĩnh; chưa có help service. |
| 19 | `SH06-EL-19` | Link “Liên hệ ban giáo vụ Study2Work” | `href="#"`; contact route/channel chưa được xác nhận. |
| 20 | `SH06-EL-20` | Footer brand + platform descriptor | Static label; không phải link trong source footer. |
| 21 | `SH06-EL-21` | Footer navigation group (4 anchor) | Chương trình đào tạo, Tra cứu chứng chỉ, Quy chế học vụ, Hỗ trợ học viên; routes chưa đồng bộ/được định nghĩa. |
| 22 | `SH06-EL-22` | Copyright text | Static `© 2025`; current year/legal wording chưa được xác nhận. |

Ảnh gốc chỉ có một state 404; state/loading/ready/service-error không được giả lập thành hình nguồn bổ sung. `SH06_markers.json` sẽ ghi tọa độ ảnh 1600×1425 và `visible_in="default 404 source"` cho từng marker.

## 4. Event plan

| Event ID | Trigger / element | Input | Xử lý dự kiến / output |
|---|---|---|---|
| `SH06-EV-01` | Router resolve unknown path hoặc mở `/not-found` | URL pathname, route match result | Không gọi API; hiển thị `ROUTE_404` chung; không echo raw URL/query có thể chứa dữ liệu riêng. Router implementation chưa có. |
| `SH06-EV-02` | Nhận kết quả GET #08 từ GS-03 flow | course_id, HTTP status, businessCode, message, traceId | Parse ID theo route contract; 200 hợp lệ trả GS-03; 404 `DESIGN_RESOURCE_NOT_FOUND` → `RESOURCE_404`; 403 giữ forbidden flow; 500/network/invalid envelope → service error riêng, không dùng SH-06. Không đọc course detail từ status page thêm lần nữa. |
| `SH06-EV-03` | Click CTA #10 | Không có payload; route target GS-01 | Điều hướng tới `/courses`; request/API thuộc GS-01, SH-06 không gọi API. Route runtime chưa xác minh. |
| `SH06-EV-04` | Click CTA #11 hoặc logo #1 / Trang chủ trong nav | Route `/` theo SH-01 proposal | Điều hướng home; không gửi API từ SH-06. |
| `SH06-EV-05` | Click nav #2, login #3, register #4 | Chọn link key: `khoa-hoc`, `tim-kiem`, `dang-nhap`, `dang-ky` | Proposal mapping lần lượt `/courses`, `/courses/search`, `/login`, `/register`; validate router allowlist khi triển khai. HTML hiện `href="#"`; chưa chạy được. |
| `SH06-EV-06` | Click “Xem tất cả” #14 | Không có payload; target GS-01 | Điều hướng `/courses`; không gọi API tại SH-06. |
| `SH06-EV-07` | Click một trong card #15–#17 | Course object/ID phải đến từ nguồn public đã được duyệt | Prototype không có ID thật và href `#`. Không điều hướng bằng tên/mock. Nếu giữ cards, chỉ điều hướng GS-03 bằng ID từ nguồn đã xác nhận. |
| `SH06-EV-08` | Nạp course recommendation block #13/#15–#17 | Nguồn items và schema chưa được chọn | Không fetch hoặc render số liệu hardcoded như thật. API #06 có thể là dependency dùng lại nhưng cần Product/UX/Frontend xác nhận; đến lúc đó bỏ/ẩn block hoặc chỉ dùng nội dung biên tập đã duyệt. Không tạo API mới. |
| `SH06-EV-09` | Click contact link #19 | Địa chỉ/route support chưa có | Không thực hiện navigation giả. Chỉ bật sau khi có channel/route được duyệt; nếu chưa có thì bỏ control. |
| `SH06-EV-10` | Click footer navigation #21 | Label của anchor | Chỉ “Chương trình đào tạo” có thể map tới `/courses` proposal; ba label còn lại chưa có routes trong inventory. Không giữ `href="#"` production; Product chốt route hoặc loại link. |

## 5. API #08, database và trace dự kiến trong DD

- Route current: `apps/study-server/app/api/v1.py` `GET /courses/{course_id}` → `get_course_detail(course_id_raw, db, trace_id)`; API prefix `/api/v1`, không yêu cầu Bearer auth.
- Validation current: `validate_course_id` dùng `parse_integer`; ID không parse được trả HTTP 404 `DESIGN_RESOURCE_NOT_FOUND`, cùng generic message với record không tồn tại/không PUBLISHED.
- Query `FIND_PUBLISHED_COURSE_DETAIL`: `courses` + `LEFT JOIN users` qua `mentor_id`; filter `c.id=:course_id AND c.status='PUBLISHED'`. Chỉ project title/name, description, thumbnail URL, price, status và mentor id/name/avatar. Đọc-only; không commit.
- Success source: HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `data.items` chứa 1 Course và `data.pagination={page:1,size:1,total:1,total_pages:1}`. `price` serialize thành decimal string. Missing mentor ID/name, invalid price, mapping error hoặc SQL error thành 500 `DESIGN_INTERNAL_ERROR`; SQL error gọi rollback.
- Error envelope từ shared response helper: `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; `X-Trace-Id` header. #08 current 404 body message “Published course not found.”; không render message raw hay tiết lộ status draft/private.
- Database DDL có `courses`/`users` và các cột source query dùng; `courses.mentor_id` nullable trong DDL trong khi `map_course` yêu cầu mentor summary hợp lệ. Nếu thiếu mentor data, current result là 500 chứ không phải 404. DDL không chứng minh live schema.
- Test source `apps/study-server/tests/modules/guest/api_08_courses_detail/test_courses_detail.py` cover ID invalid, row missing, DB error/rollback, success mapping và route 200. Đọc, không chạy.

## 6. Blocker, discrepancy và acceptance gate

1. `BLOCKER: SH06_PRODUCTION_SURFACE_UNDECIDED` — recommendation cards, help/contact strip, footer destinations và copyright/legal copy hiện có trong prototype nhưng chưa có content/route contract. Cần quyết định giữ/ẩn/bỏ từng surface và xác nhận dữ liệu/đích; không biến `href="#"` hoặc text mẫu thành production behavior.
2. `BLOCKER: AC05_NOT_FOUND_STATUS_CONFLICT` — AC-05 vẽ `404/403` cho nhánh course không tồn tại/PUBLISHED; API catalog và handler #08 chỉ có 404 cho invalid/missing/unpublished, 500 cho internal failure. Cần chỉnh AC hoặc xác nhận ý nghĩa 403 trước khi chốt luồng giữa SH-06 và SH-05.
3. `DISCREPANCY: API_08_STATUS_LABELS_VS_SOURCE` — dòng SH-06 trong screen inventory ghi BE `D`, API index ghi #008 `R`, root API contract là approved design nhưng chưa runtime-verified và API DD #08 vẫn Draft; route/module/test source hiện tồn tại. Deployment/live DB chưa verified. #08 success trả ApiEnvelope có `data: Page<Course>` singleton; không nhầm `Page<Course>` là toàn response.
4. `IMPLEMENTATION_BLOCKER: STUDY_WEB_ROUTER_NOT_FOUND` — không có `src/`/package manifest; dist bundle cũ không chứng minh `/not-found` hoặc route actions.
5. `DESIGN_SYSTEM_DRIFT` — HTML dùng remote Google Fonts/Tailwind CDN và max-width 1440px; Study guide chỉ định system/Inter local, content width khoảng 1120px, control 44px+, responsive reflow. Cần xác nhận có hiệu lực với prototype này hay không.

Kế hoạch sau source review: cập nhật SH-06 DD với expected/current tách biệt, 22 element, 10 event, mapping #08 có trace, và blockers không suy đoán. Không gọi màn hình `DD READY` khi các surface nhìn thấy chưa có quyết định triển khai hoặc AC-05 còn mâu thuẫn. Kiểm tra tĩnh marker→element, link, ảnh và hash sau khi cập nhật; không chạy tests/runtime trong phiên tài liệu.

## 7. Kết quả phiên SH-06

- Kế hoạch được rà soát và cập nhật trước khi sửa DD; API #08 được trace từ route qua validation, query, mapping, response và test source.
- Cập nhật `SH-06.md` với trạng thái `DD BLOCKED`; giữ expected/current, AC-05 discrepancy, API #08 contract/source, 22 element, 10 event và blocker ownership tách bạch.
- Giữ nguyên `screen.png` và `code.html`; hash dự kiến phải giữ `screen.png` `b6a423005ea008e9f00de6f2328f182c6256e7ae647575f55dfa8c4ae05ecf0a`, `code.html` `ce3c9bff0e9d24630172230f2b28e3a533ad4e2be1daecfe71f3bf1db4649ce7`.
- Marker JSON/annotated image không được tái tạo; visual review thấy 22 marker có thứ tự và không che copy/control trọng yếu. Static audit đạt: 22/22 marker→element, 10 event, 27 local link trong DD resolve được, hai ảnh 1600×1425, source hashes giữ nguyên, marker trong canvas, tracker/handoff nhất quán; trailing whitespace scan và `git diff --check` đạt.
- Trạng thái mục tiêu phiên: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Tests/runtime không chạy; worklog `.agents/worklog/2026-11-06/design-study-screen-sh06.md` đã VERIFIED.
- Re-audit 2026-11-07: làm rõ sai khác nhãn `D` ở dòng SH-06 và `R` ở API index #008; API contract/DD/source status được giữ riêng, không quy đổi thành runtime verification.
- Phiên tiếp theo: SH-07, trong một phiên riêng. Không xử lý SH-07 trong phiên này.
