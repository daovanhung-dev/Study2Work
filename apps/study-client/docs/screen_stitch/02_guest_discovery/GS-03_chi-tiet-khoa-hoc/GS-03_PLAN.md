# GS-03 — Kế hoạch chi tiết

> Ngày rà soát: 2026-11-07  
> Trạng thái: `AUDIT COMPLETE`; `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.  
> Phạm vi phiên: chỉ GS-03; chưa bắt đầu GS-04.

## Re-audit plan — 2026-11-07

- Re-audit the existing GS-03 bundle only; preserve `screen.png` and `code.html`. Recheck the rendered HTML derivative and annotation provenance before deciding whether they remain usable.
- Recheck current inventory/F02/G-06/G-01, AC-05, API catalog and #08/#09/#10 DD against current route composition, validators, queries, response mapping, errors, database artifacts and focused test source. Confirm API #10's current route/module/test status with scoped source searches.
- Recheck Study Web source/runtime status, then verify the cross-screen course ID handoff from GS-02 and destination contracts for GS-04/GS-05/ST-04 without editing those screens.
- Audit the existing GS-03 DD, 10-marker map/SVG, rendered/annotated images, events, states, relative links and global 83-ID tracker. Make only source-backed corrections; retain the independent DD, implementation and runtime statuses.
- Record any new discrepancies in this plan/DD/inventory/tracker/worklog; do not start another Screen ID or run application tests/runtime.

## 1. Phạm vi và bằng chứng

- Screen ID/tên: **GS-03 — Chi tiết khóa học (Page)**; actor dự kiến `Guest`; route `/courses/:courseId` là route đề xuất trong `list_screen.md`, chưa được Study Web thực thi.
- Expected: `list_screen.md` yêu cầu course detail, mentor, giá, tabs đề cương/đánh giá, CTA ghi danh; liên kết GS-04/GS-05/GS-06/ST-04. F02 yêu cầu #08 xác định khóa học `PUBLISHED`, #09/#10 tải lười theo tab.
- Asset baseline: `screen.png` 1280×1024, SHA-256 `94360a8b1b1a9bbe0cdc110f6c243ce5aaabd8b6923331c5667421cb1c37d34d`, entropy 0.35757, 20 màu; ảnh gần như trắng, không dùng được để đọc UI. `code.html` SHA-256 `d4f4bfdb56324b7c96589af75362903a491a3f565c97152b63634573c9d69619`; đây là HTML tĩnh Guest, không có course data, route binding, API calls hay tab handlers. Bundle hiện có thêm các derivative `screen_rendered.png`, `screen_annotated.png`, marker JSON/SVG, plan và DD; không ghi đè hai asset nguồn.
- Kế hoạch hình ảnh: giữ nguyên `screen.png` và `code.html`; Firefox đã render `code.html` nguyên trạng ra `screen_rendered.png` kích thước 1440×1200 (2113 màu). Bố cục header, breadcrumb, title, tabs, empty state và footer đều hiển thị đầy đủ. Dùng ảnh render riêng này làm nền cho `screen_annotated.png`; không thay thế/xóa ảnh gốc. Đây là ảnh tĩnh của HTML nguồn, không phải ảnh runtime.
- `code.html` tải Tailwind và font từ CDN, trong khi `.agents/web-study/design.md` yêu cầu không phụ thuộc font từ xa. Bản render, nếu tạo được, chỉ là ảnh của nguồn HTML hiện có; không biến nó thành bằng chứng về UI runtime hoặc thiết kế đã được duyệt.

## 2. Source/API trace và discrepancy cần giữ nguyên

| Hạng mục | Expected/design evidence | Current source evidence | Kết luận |
|---|---|---|---|
| #08 detail | Catalog/AC-05: `GET /api/v1/courses/{course_id}`, Public; 200/404/500. Catalog contract ghi `course_id:int64`; AC cho nhánh không public 404/403. | Route trong `apps/study-server/app/api/v1.py` khai báo path là `str`; module validator dùng shared `parse_integer`, chỉ kiểm tra cú pháp integer Python, không enforce signed int64/positive range. Query chỉ lấy `PUBLISHED` course và `LEFT JOIN` mentor. Response `ApiEnvelope` với `data.items` singleton `CoursePage`, pagination page/size/total/total_pages = 1. Course gồm id/title/description?/thumbnail_url?/price/status/mentor{id/full_name/avatar_url?}. Mapper yêu cầu mentor id/name; thiếu sẽ thành mapping error rồi HTTP 500. Có test source nhưng không chạy. | API #08 **SOURCE_BACKED** trong backend checkout; API DD vẫn Draft; contract `int64` khác validator raw-string hiện tại; source `LEFT JOIN` khác API DD `INNER JOIN`; AC 404/403 khác current 404. Không suy ra route UI đã hoạt động. |
| #09 curriculum | Catalog/AC-05: `GET /api/v1/courses/{course_id}/curriculum`, Public; `course_id:int64`; 200/404/500. F02 quy định lazy theo tab. | Route khai báo `str`; module validator dùng cùng `parse_integer`, không có kiểm tra signed int64 hoặc dương. View kiểm tra PUBLISHED course rồi lấy lesson PUBLISHED, thứ tự `sort_order ASC, id ASC`. Lesson: id/course_id/title/content?/video_url?/order/status. Empty curriculum trả 200, items=[], total=0, total_pages=0; missing/unpublished trả 404; DB/mapping failure trả 500. Có test source nhưng không chạy. | API #09 **SOURCE_BACKED**; API DD còn Draft và contract `int64` khác validator raw-string hiện tại; lesson preview/access policy chưa được xác nhận. |
| #10 reviews | Catalog và `apps/study-server/docs/dd/10_courses_reviews/` khai báo public `GET /api/v1/courses/{course_id}/reviews`, page và rating filter; AC-05 có bước đọc reviews + aggregate rating. | Không có route `/courses/{course_id}/reviews`, module API #10 hoặc test API #10 trong source hiện tại. Checked-in DDL `discussions` không có `title`/rating column và không có rating table. API DD ghi `Draft — Needs Confirmation`; không có aggregate rating source và `Discussion.title` bắt buộc không có nguồn. | API #10 **DECLARED_NOT_RUNNABLE**; không gọi hoặc khẳng định rating/review UI chạy được. |
| Orchestration | `list_screen.md` F02: #08 trước; #09/#10 lazy theo tab. | AC-05 mô tả ba API calls tuần tự: #08 → #09 → #10, rồi render. | **DISCREPANCY** về thời điểm gọi; không tự chọn một luồng như thể đã được duyệt. Tab lazy là expected inventory hiện hành cho DD; cần Product/BE xác nhận với AC. |
| Enrollment CTA | Inventory liệt kê CTA và liên kết ST-04. F03 yêu cầu #15 identity contract được sửa trước khi xác nhận trạng thái ghi danh; #15 public chỉ nhận course_id nhưng trả Enrollment có user_id. | `code.html` không có CTA; không có enrollment action trong GS-03 source. API #15 không phải API đã được xác nhận ở backend runtime. | Chỉ ghi CTA là expected/missing. Không tạo event/API enrollment tại GS-03. Guest→Student/login handoff và course_id transport cần chốt; G-01 blocker chi phối ST-04. |
| Study Web | Route/UI được nêu trong inventory và HTML tĩnh. | Registered `.agents/web-work/study/INDEX.md` ghi `UNWIRED`; `apps/study-client/` hiện có docs/assets và ignored `dist`, không có editable app source hoặc package manifest. | Route trong DD vẫn là đề xuất; `RUNTIME NOT VERIFIED`. |

## 3. Sơ đồ marker dự kiến

Marker bám theo các nhóm UI có thật trong `code.html`, không đánh số phần tử vắng mặt ở trạng thái loaded. Tọa độ chốt sau khi render và xem ảnh:

| Marker | Element ID | Nhóm element trong HTML |
|---:|---|---|
| #1 | `GS03-EL-01` | Header: brand và primary navigation |
| #2 | `GS03-EL-02` | Header: đăng nhập/đăng ký |
| #3 | `GS03-EL-03` | Breadcrumb: Trang chủ / Khóa học / Chi tiết khóa học |
| #4 | `GS03-EL-04` | Tiêu đề trang “Chi tiết khóa học” |
| #5 | `GS03-EL-05` | Nhóm tab Tổng quan / Đề cương / Đánh giá; hai tab sau đang disabled |
| #6 | `GS03-EL-06` | Panel trạng thái rỗng: biểu tượng sách |
| #7 | `GS03-EL-07` | Tiêu đề và nội dung giải thích trạng thái rỗng |
| #8 | `GS03-EL-08` | CTA quay lại danh sách khóa học (`/courses`) |
| #9 | `GS03-EL-09` | Footer brand |
| #10 | `GS03-EL-10` | Footer navigation |

Không có marker cho course title/data, mentor, price, enrollment CTA, curriculum items hay review/rating vì chúng không xuất hiện trong HTML đang có. Bảng element DD phải nói rõ các phần này là expected-but-not-present/blocker, không giả chúng thuộc ảnh nguồn.

## 4. Event/state cần đặc tả trong DD

- **Initial load:** chuẩn hóa `courseId` từ route đề xuất; expected gọi #08 và chỉ render detail khi backend xác nhận PUBLISHED. HTML hiện tại không đọc route/gọi API; response singleton `data.items[0]` phải được map rõ. 404/500 và invalid path cần nêu theo current #08; 403 của AC là discrepancy. Loading UI/error replacement chưa có nguồn hình ảnh.
- **Tab curriculum:** khi được bật theo expected lazy flow, gọi #09 với đúng course ID sau khi #08 xác nhận public; map danh sách bài học theo `order`. Empty success khác lỗi API. Chưa có quy tắc preview/access cho lesson.
- **Tab reviews:** #10 chỉ là contract design; không thực hiện request cho tới khi route/module/model được wired và rating/title conflict được giải quyết. Không tính average rating từ `discussions`.
- **Enrollment CTA:** đang thiếu trong HTML; inventory liên kết ST-04, nhưng guest/auth handoff và chính sách login chưa có contract. Ghi event blocked, không invent request #15 hoặc thông báo thành công.
- **Navigation:** mô tả các href hiện có trong HTML (`/`, `/courses`, `/login`, `/register`) như thuộc tính static source; không khẳng định Study Web router thực thi chúng. Link CTA quay lại list không truyền dữ liệu.
- **States:** source HTML hiện có = empty/unavailable + tab disabled; expected states = loading, course-not-found, partial-tab-error; các state này chưa được triển khai. Tách `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.

## 5. Thứ tự thực hiện và acceptance checklist

1. [x] Kế hoạch này được tạo trước khi tạo ảnh render, annotation hoặc DD.
2. [x] Render HTML nguyên trạng trong Firefox ra `screen_rendered.png`; đã kiểm tra kích thước, stylesheet và nội dung. Không ghi đè nguồn.
3. [x] Tạo `GS-03_markers.json`, SVG overlay và `screen_annotated.png` theo 10 nhóm trên; marker đúng vùng, thứ tự liên tục, không che nội dung.
4. [x] Viết `GS-03.md` tiếng Việt theo các phần: tổng quan; luồng; 10 element; từng event với đầu vào/xử lý/đầu ra và API status; state/navigation matrix; blocker; acceptance checklist và trace links.
5. [x] Static audit: JSON parse; marker IDs/số thứ tự khớp bảng DD; link tương đối tồn tại; hash `screen.png`/`code.html` không đổi; 83 inventory/tracker/folder IDs match; `git diff --check`. Không chạy test hay runtime.
6. [x] Cập nhật dòng GS-03 trong `dd_screens/PLAN.md` và worklog. Kết quả `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`, vì loaded state/CTA/tab orchestration/#10 contract/UI router chưa đủ căn cứ.

### Kết quả static audit

- PASS: `list_screen.md`, master tracker và 83 thư mục nguồn có cùng 83 ID; GS-03 có đủ source, render, annotated image, marker map, plan và DD.
- PASS: JSON marker có #1–#10 duy nhất; bảng element DD ánh xạ đủ 10 ID; event IDs liên tục #01–#06; mọi Markdown link tương đối trong DD resolve.
- PASS: source hashes giữ nguyên; PNG là 1280×1024 (source), 1440×1200 (rendered), 3040×2400 (annotated); SVG có 10 circle/leader và embed đúng ảnh render.
- PASS: master tracker cập nhật GS-03 và next screen GS-04; `git diff --check` không báo lỗi.
- Tests và Study runtime không chạy/không xác minh.

### Điều kiện DD READY chưa đạt

- Chưa có visual contract cho loaded course detail, mentor/price blocks, curriculum/review states hoặc enrollment CTA.
- AC-05 và inventory khác nhau về thứ tự eager/lazy API calls.
- API #10 chưa có runtime source; rating/title thiếu source/schema.
- Guest CTA sang ST-04 cần policy identity/authentication/route handoff giải quyết.
- Study Web/router chưa được nối.

## Re-audit result — 2026-11-07

- Re-traced API #08/#09 routes, validators, view/query/model mapping and focused test source; source remains local and tests were not run. Both route signatures accept `str`; shared `parse_integer` validates integer syntax but does not enforce catalog `int64` or a positive-only range. This new contract discrepancy is recorded in the DD and GS-03 inventory/tracker rows.
- #08 query uses `LEFT JOIN` although the Draft API DD specifies `INNER JOIN`; `mentor.id` and `mentor.full_name` are required by the current mapper, so missing mentor data becomes a safe 500 mapping error. The checked-in courses DDL allows nullable `mentor_id`; no live data was inspected.
- #08 current source returns a singleton `Page<Course>` and 404 for invalid/missing/unpublished course; AC-05's 403 alternative remains a conflict. #09 current source gates on PUBLISHED course, returns PUBLISHED lessons sorted by `sort_order ASC, id ASC`, and treats empty curriculum as HTTP 200. API #08/#09 DDs remain Draft and do not establish deployed behavior.
- Scoped search found no executable #10 route/module/test; checked-in `discussions` DDL has no title or rating source. No live DB was inspected.
- GS-02 passes `course.id` as the expected GS-03 route input; GS-04/GS-05 expect the same `courseId`; ST-04 proposes the same route parameter but still has the Student/#15 identity blocker. These are design handoffs, not wired navigation.
- Static re-audit: source hashes unchanged; PNG dimensions 1280×1024, 1440×1200 and 3040×2400; 10 ordered unique marker IDs map to 10 DD element rows, with 10 SVG circles/labels; all 6 event sections have input/process/outcome or an explicit blocked outcome; 11 local DD links resolve; 83 inventory IDs match tracker IDs and screen folders.
- Tests, Study Web runtime and live database were not run or verified. Keep `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. GS-04 remains the next Screen ID for a separate session.
