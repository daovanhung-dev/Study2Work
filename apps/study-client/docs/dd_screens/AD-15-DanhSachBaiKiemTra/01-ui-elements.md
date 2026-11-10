# AD-15 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-15_markers.json](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/AD-15_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-15-EL-001` | `not supplied in marker JSON` | Study2Work Admin brand block |
| #2 | `AD-15-EL-002` | `not supplied in marker JSON` | Admin navigation: Tổng quan |
| #3 | `AD-15-EL-003` | `not supplied in marker JSON` | Admin navigation: Người dùng |
| #4 | `AD-15-EL-004` | `not supplied in marker JSON` | Admin navigation: Khóa học và Nội dung |
| #5 | `AD-15-EL-005` | `not supplied in marker JSON` | Admin navigation: Kiểm duyệt |
| #6 | `AD-15-EL-006` | `not supplied in marker JSON` | Admin navigation: Báo cáo |
| #7 | `AD-15-EL-007` | `not supplied in marker JSON` | Static SYSTEM NORMAL badge |
| #8 | `AD-15-EL-008` | `not supplied in marker JSON` | Notifications button without handler |
| #9 | `AD-15-EL-009` | `not supplied in marker JSON` | Static Admin identity and avatar |
| #10 | `AD-15-EL-010` | `not supplied in marker JSON` | Global breadcrumb: Hệ thống |
| #11 | `AD-15-EL-011` | `not supplied in marker JSON` | Global breadcrumb: Quản trị trung tâm |
| #12 | `AD-15-EL-012` | `not supplied in marker JSON` | Global breadcrumb: Không gian làm việc |
| #13 | `AD-15-EL-013` | `not supplied in marker JSON` | Static RBAC assurance copy |
| #14 | `AD-15-EL-014` | `not supplied in marker JSON` | Local breadcrumb: Quản trị khảo thí |
| #15 | `AD-15-EL-015` | `not supplied in marker JSON` | Current breadcrumb: Danh sách bài kiểm tra |
| #16 | `AD-15-EL-016` | `not supplied in marker JSON` | Static scoring-engine readiness badge |
| #17 | `AD-15-EL-017` | `not supplied in marker JSON` | Static KHẢO THÍ & ĐÁNH GIÁ category badge |
| #18 | `AD-15-EL-018` | `not supplied in marker JSON` | Static screen ID AD-15 |
| #19 | `AD-15-EL-019` | `not supplied in marker JSON` | Page title: Quản lý ngân hàng bài kiểm tra |
| #20 | `AD-15-EL-020` | `not supplied in marker JSON` | Page subtitle |
| #21 | `AD-15-EL-021` | `not supplied in marker JSON` | Disabled create quiz CTA to AD-16 |
| #22 | `AD-15-EL-022` | `not supplied in marker JSON` | Quiz name/code search input with decorative icon |
| #23 | `AD-15-EL-023` | `not supplied in marker JSON` | Course filter select with decorative icon |
| #24 | `AD-15-EL-024` | `not supplied in marker JSON` | Status filter select with decorative icon |
| #25 | `AD-15-EL-025` | `not supplied in marker JSON` | Toolbar refresh button |
| #26 | `AD-15-EL-026` | `not supplied in marker JSON` | Disabled advanced-filter button |
| #27 | `AD-15-EL-027` | `not supplied in marker JSON` | Table header: Mã bài thi |
| #28 | `AD-15-EL-028` | `not supplied in marker JSON` | Table header: Tiêu đề bài kiểm tra |
| #29 | `AD-15-EL-029` | `not supplied in marker JSON` | Table header: Khóa học |
| #30 | `AD-15-EL-030` | `not supplied in marker JSON` | Table header: Số câu hỏi |
| #31 | `AD-15-EL-031` | `not supplied in marker JSON` | Table header: Thời lượng |
| #32 | `AD-15-EL-032` | `not supplied in marker JSON` | Table header: Trạng thái |
| #33 | `AD-15-EL-033` | `not supplied in marker JSON` | Table header: Thao tác |
| #34 | `AD-15-EL-034` | `not supplied in marker JSON` | Empty-state quiz icon |
| #35 | `AD-15-EL-035` | `not supplied in marker JSON` | Empty-state heading |
| #36 | `AD-15-EL-036` | `not supplied in marker JSON` | Empty-state explanatory copy |
| #37 | `AD-15-EL-037` | `not supplied in marker JSON` | Empty-state refresh button |
| #38 | `AD-15-EL-038` | `not supplied in marker JSON` | Result-count summary: 0 of 0 quizzes |
| #39 | `AD-15-EL-039` | `not supplied in marker JSON` | Page indicator: 0 / 0 |
| #40 | `AD-15-EL-040` | `not supplied in marker JSON` | Disabled previous-page button |
| #41 | `AD-15-EL-041` | `not supplied in marker JSON` | Disabled next-page button |
| #42 | `AD-15-EL-042` | `not supplied in marker JSON` | Digital-assessment policy information icon |
| #43 | `AD-15-EL-043` | `not supplied in marker JSON` | Digital-assessment policy heading |
| #44 | `AD-15-EL-044` | `not supplied in marker JSON` | Static question-bank and activation rule copy |
| #45 | `AD-15-EL-045` | `not supplied in marker JSON` | Static exam-security V3 badge |
| #46 | `AD-15-EL-046` | `not supplied in marker JSON` | Footer copyright |
| #47 | `AD-15-EL-047` | `not supplied in marker JSON` | Footer system descriptor |
| #48 | `AD-15-EL-048` | `not supplied in marker JSON` | Footer privacy link without route handler |
| #49 | `AD-15-EL-049` | `not supplied in marker JSON` | Footer RBAC standards link without route handler |
| #50 | `AD-15-EL-050` | `not supplied in marker JSON` | Footer technical-support link without route handler |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Tọa độ là pixel trên ảnh nguồn 1600×1394; ảnh đánh số được render 2× thành 3200×2788. Trạng thái `static`, `disabled` và giá trị hiển thị mô tả HTML/screenshot hiện tại. Các trạng thái loading/ready/error là target state có điều kiện, không phải implementation evidence.

| ID | Thành phần / vị trí (x,y) | Thuộc tính, nguồn và trạng thái hiện tại | Event |
|---:|---|---|---|
| 1 | Khối brand Study2Work Admin `(15,22)` | Nhãn/nhận diện tĩnh; không có dữ liệu tenant hoặc session binding. | EV-12 |
| 2 | Admin nav “Tổng quan” `(350,64)` | Anchor `href="#"`; không có destination handler. | EV-12 |
| 3 | Admin nav “Người dùng” `(475,64)` | Anchor `href="#"`; route chưa được wire. | EV-12 |
| 4 | Admin nav “Khóa học và Nội dung” `(675,64)` | Active style tĩnh; không chứng minh route content đang hoạt động. | EV-12 |
| 5 | Admin nav “Kiểm duyệt” `(850,64)` | Anchor `href="#"`; không có route handler. | EV-12 |
| 6 | Admin nav “Báo cáo” `(1000,64)` | Anchor `href="#"`; không có route handler. | EV-12 |
| 7 | Badge “SYSTEM NORMAL” `(1155,64)` | Copy tĩnh; không có health probe/API. | — |
| 8 | Nút Notifications `(1285,64)` | Button tĩnh, không có click listener hoặc notification source. | EV-12 |
| 9 | Admin identity/avatar `(1550,64)` | Tên/role/avatar tĩnh; không lấy từ JWT/profile API. | — |
| 10 | Breadcrumb toàn cục “Hệ thống” `(45,118)` | Nội dung breadcrumb tĩnh; route không được gắn. | EV-12 |
| 11 | Breadcrumb toàn cục “Quản trị trung tâm” `(205,118)` | Nội dung tĩnh; không có destination handler. | EV-12 |
| 12 | Breadcrumb “Không gian làm việc” `(380,118)` | Nội dung tĩnh; không có destination handler. | EV-12 |
| 13 | Copy bảo đảm RBAC `(1535,118)` | Copy tĩnh; không phải kết quả authorization/policy service. | — |
| 14 | Breadcrumb cục bộ “Quản trị khảo thí” `(65,197)` | Static label/link; route đích không có trong source. | EV-12 |
| 15 | Breadcrumb hiện tại “Danh sách bài kiểm tra” `(285,197)` | Nhãn trang hiện tại, không có route behavior. | EV-12 |
| 16 | Badge trạng thái scoring engine `(1440,197)` | Trạng thái “sẵn sàng” tĩnh; không có readiness API. | — |
| 17 | Badge nhóm “KHẢO THÍ & ĐÁNH GIÁ” `(125,255)` | Badge tĩnh, chỉ phân loại nội dung. | — |
| 18 | Screen ID `AD-15` `(235,255)` | Text tĩnh; không gắn tracker/build version. | — |
| 19 | Tiêu đề “Quản lý ngân hàng bài kiểm tra” `(610,284)` | Heading tĩnh, không tạo data contract. | — |
| 20 | Subtitle trang `(890,320)` | Copy tĩnh; không phải trạng thái backend. | — |
| 21 | CTA tạo bài kiểm tra `(1535,340)` | Button disabled; expected handoff AD-16, không gọi #88 từ trang này. | EV-07 |
| 22 | Ô tìm tên/mã quiz `(300,450)` | Text input; prototype không có listener/debounce/validation. Search/code không nằm trong #87. | EV-02 |
| 23 | Select khóa học `(770,450)` | Option hiện là slug; #87 nhận `course:int64`; không có map/options source. | EV-03 |
| 24 | Select trạng thái `(1085,450)` | Options `draft/active/closed`; chưa có enum mapping được duyệt. | EV-04 |
| 25 | Nút refresh toolbar `(1285,450)` | Chỉ xoay icon 800 ms; không fetch/cache update. | EV-05 |
| 26 | Nút bộ lọc nâng cao `(1470,450)` | Disabled; không có panel/event/query contract. | EV-06 |
| 27 | Header bảng “Mã bài thi” `(115,491)` | Cột được mockup đặt ra; #87 không trả quiz code. Không render giá trị suy đoán. | — |
| 28 | Header bảng “Tiêu đề bài kiểm tra” `(365,491)` | Candidate mapping `title` từ local response; catalog cardinality chưa chốt. | EV-01 |
| 29 | Header bảng “Khóa học” `(740,491)` | Local response chỉ có `course_id`, không có title; không có course lookup contract tại màn này. | EV-01 |
| 30 | Header bảng “Số câu hỏi” `(1035,491)` | #87 trả `questions=[]` chưa hydrate; không suy ra count bằng độ dài mảng. | EV-01 |
| 31 | Header bảng “Thời lượng” `(1180,491)` | Candidate `duration_minutes?`; nullable theo local projection; đơn vị hiển thị cần contract/UI mapping. | EV-01 |
| 32 | Header bảng “Trạng thái” `(1350,491)` | Local projection không trả status; prototype option không xác nhận row status. | EV-01 |
| 33 | Header bảng “Thao tác” `(1510,491)` | Header tĩnh; không có row actions trong screenshot empty state. | EV-09 / EV-10 / EV-11 |
| 34 | Icon empty state `(862,707)` | Icon trang trí; không chứng minh empty hay synchronization state. | — |
| 35 | Heading empty state `(1028,790)` | Copy tĩnh; source không tự tải danh sách để xác nhận empty. | EV-01 |
| 36 | Copy giải thích empty state `(1110,844)` | Nội dung prototype; “chưa đồng bộ” không phải trạng thái API #87. | EV-01 |
| 37 | Nút refresh trong empty state `(975,930)` | Chỉ xoay icon 800 ms; không fetch. | EV-05 |
| 38 | Tóm tắt số kết quả `(340,1110)` | Hiển thị `0 of 0` tĩnh; local API có `total`, nhưng chưa có binding. | EV-01 |
| 39 | Chỉ báo trang `0 / 0` `(1080,1045)` | Hiển thị tĩnh; source candidate page bắt đầu từ 1; empty local response có `total_pages=0`. | EV-08 |
| 40 | Nút trang trước `(1300,1166)` | Disabled trong ảnh; không có page state/event. | EV-08 |
| 41 | Nút trang sau `(1460,1166)` | Disabled trong ảnh; không có page state/event. | EV-08 |
| 42 | Icon thông tin chính sách `(46,1200)` | Icon trang trí; không có policy API. | — |
| 43 | Heading chính sách đánh giá số `(340,1200)` | Copy tĩnh; không chứng minh cấu hình quiz. | — |
| 44 | Copy question-bank/activation `(1145,1270)` | Quy tắc hiển thị chưa truy vết tới API #87/AC contract cụ thể; không dùng làm validation. | — |
| 45 | Badge “Exam security V3” `(1450,1200)` | Copy tĩnh; không phải security/version response. | — |
| 46 | Footer copyright `(125,1312)` | Nội dung tĩnh, không có event/API. | — |
| 47 | Footer mô tả hệ thống `(370,1312)` | Copy tĩnh; không phải trạng thái vận hành. | — |
| 48 | Footer Privacy `(950,1312)` | Anchor `href="#"`; chưa có destination. | EV-12 |
| 49 | Footer chuẩn RBAC `(1220,1312)` | Anchor `href="#"`; chưa có destination; không thay thế permission check. | EV-12 |
| 50 | Footer Technical Support `(1480,1312)` | Anchor `href="#"`; chưa có destination/ticket handler. | EV-12 |

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/ready/error/unauthorized/forbidden/validation/service-error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/AD-15.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
