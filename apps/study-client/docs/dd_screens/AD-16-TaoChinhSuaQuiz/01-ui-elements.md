# AD-16 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-16_markers.json](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/AD-16_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-16-EL-001` | `not supplied in marker JSON` | Study2Work brand block |
| #2 | `AD-16-EL-002` | `not supplied in marker JSON` | Admin navigation: Tổng quan |
| #3 | `AD-16-EL-003` | `not supplied in marker JSON` | Admin navigation: Người dùng |
| #4 | `AD-16-EL-004` | `not supplied in marker JSON` | Admin navigation: Khóa học & Nội dung |
| #5 | `AD-16-EL-005` | `not supplied in marker JSON` | Admin navigation: Kiểm duyệt |
| #6 | `AD-16-EL-006` | `not supplied in marker JSON` | Admin navigation: Báo cáo |
| #7 | `AD-16-EL-007` | `not supplied in marker JSON` | Static SYSTEM NORMAL badge |
| #8 | `AD-16-EL-008` | `not supplied in marker JSON` | Notifications button |
| #9 | `AD-16-EL-009` | `not supplied in marker JSON` | Static Admin identity and avatar |
| #10 | `AD-16-EL-010` | `not supplied in marker JSON` | Global breadcrumb trail |
| #11 | `AD-16-EL-011` | `not supplied in marker JSON` | Static RBAC verification indicator |
| #12 | `AD-16-EL-012` | `not supplied in marker JSON` | Local breadcrumb trail |
| #13 | `AD-16-EL-013` | `not supplied in marker JSON` | Return to AD-15 link |
| #14 | `AD-16-EL-014` | `not supplied in marker JSON` | Page title: Thiết lập và biên tập bài kiểm tra trắc nghiệm |
| #15 | `AD-16-EL-015` | `not supplied in marker JSON` | Safe Mode notice |
| #16 | `AD-16-EL-016` | `not supplied in marker JSON` | Quiz configuration section heading and part label |
| #17 | `AD-16-EL-017` | `not supplied in marker JSON` | Quiz title field group |
| #18 | `AD-16-EL-018` | `not supplied in marker JSON` | Course selector field group |
| #19 | `AD-16-EL-019` | `not supplied in marker JSON` | Duration field group |
| #20 | `AD-16-EL-020` | `not supplied in marker JSON` | Passing score field group |
| #21 | `AD-16-EL-021` | `not supplied in marker JSON` | Static local autosave notice |
| #22 | `AD-16-EL-022` | `not supplied in marker JSON` | Questions section heading and part label |
| #23 | `AD-16-EL-023` | `not supplied in marker JSON` | Static schema notice |
| #24 | `AD-16-EL-024` | `not supplied in marker JSON` | Empty-state icon |
| #25 | `AD-16-EL-025` | `not supplied in marker JSON` | Empty-state heading |
| #26 | `AD-16-EL-026` | `not supplied in marker JSON` | Empty-state description |
| #27 | `AD-16-EL-027` | `not supplied in marker JSON` | Disabled Add Question button and temporary-lock badge |
| #28 | `AD-16-EL-028` | `not supplied in marker JSON` | Static Questions Builder Gate notice |
| #29 | `AD-16-EL-029` | `not supplied in marker JSON` | Static RBAC/access status strip |
| #30 | `AD-16-EL-030` | `not supplied in marker JSON` | Cancel link/button |
| #31 | `AD-16-EL-031` | `not supplied in marker JSON` | Disabled Save button |
| #32 | `AD-16-EL-032` | `not supplied in marker JSON` | Footer brand and copyright block |
| #33 | `AD-16-EL-033` | `not supplied in marker JSON` | Privacy policy link |
| #34 | `AD-16-EL-034` | `not supplied in marker JSON` | RBAC standards link |
| #35 | `AD-16-EL-035` | `not supplied in marker JSON` | Technical support link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Tọa độ `(x,y)` là tâm marker trên ảnh nguồn 1600×1402. Tọa độ này khớp với thứ tự trong JSON, SVG và ảnh annotated. Element tĩnh được mô tả là copy/layout, không tạo data contract.

| ID / tọa độ | Tên và loại | Vị trí, thuộc tính, dữ liệu và trạng thái hiện tại | Event |
|---|---|---|---|
| 1 `(276,18)` | Study2Work brand block — branding | Header trên cùng bên trái; logo “S”, Study2Work, LMS, ADMIN PORTAL. HTML là div tĩnh, không phải link. | — |
| 2 `(336,13)` | Tổng quan — navigation link | Header top nav; anchor `href="#"`, không có route handler. | EV-09 |
| 3 `(455,13)` | Người dùng — navigation link | Header top nav; anchor `href="#"`; destination không xác minh. | EV-09 |
| 4 `(599,13)` | Khóa học & Nội dung — navigation link | Header top nav; anchor `href="#"`; destination không xác minh. | EV-09 |
| 5 `(817,13)` | Kiểm duyệt — navigation link | Header top nav; anchor `href="#"`; destination không xác minh. | EV-09 |
| 6 `(959,13)` | Báo cáo — navigation link | Header top nav; anchor `href="#"`; destination không xác minh. | EV-09 |
| 7 `(1085,13)` | SYSTEM NORMAL — status badge | Copy/pulse tĩnh; không có health check/API nguồn. Không coi là backend health. | — |
| 8 `(1276,14)` | Notifications — button | Icon bell và chấm đỏ; button không có listener, không có notification request. | EV-09 |
| 9 `(1357,15)` | Admin identity/avatar — identity block | Tên “TS. Quản Trị Viên”, role copy và avatar tĩnh; không chứng minh session/current user. | — |
| 10 `(37,76)` | Global breadcrumb trail — navigation region | Hệ thống > Quản trị trung tâm > Không gian làm việc; spans/copy, không có href/router. | EV-09 |
| 11 `(1520,76)` | Chuẩn xác thực RBAC — status copy | Header góc phải; icon/copy tĩnh. Không chứng minh policy/authorization. | — |
| 12 `(40,134)` | Local breadcrumb trail — breadcrumb | Quản trị khảo thí > Danh sách bài kiểm tra > Thiết lập bài kiểm tra; copy prototype, không có router evidence. | EV-09 |
| 13 `(1176,167)` | Quay lại danh sách bài kiểm tra (AD-15) — link/button | Góc phải cạnh title; anchor `#/admin/quizzes`. Handoff mong đợi AD-15; route chưa được xác minh. | EV-07 |
| 14 `(40,170)` | Page title — heading | “Thiết lập và biên tập bài kiểm tra trắc nghiệm”; copy tĩnh, không thay đổi theo mode/ID. | — |
| 15 `(54,262)` | Safe Mode — alert/information banner | Dải xanh dưới title, gồm icon, nhãn, mô tả hạn chế edit sâu. Static copy; không có server read/feature gate evidence. | EV-08 |
| 16 `(66,421)` | Cấu hình chung bài thi — section heading | Card trái, nhãn “PHẦN 1 / 2”; chỉ là cấu trúc trình bày. | — |
| 17 `(55,513)` | Tên bài kiểm tra — text input group | Label có dấu `*`, copy “Bắt buộc”, text placeholder và helper. Input `id=quiz-title`, type text; không có `required`, maxLength hoặc listener. Local #88 nested fallback nhận strict string, max 200 theo candidate storage; không có min. Value hiện rỗng; `dirty/error` chưa wire. | EV-03 |
| 18 `(55,647)` | Khóa học áp dụng — select group | Label có dấu `*`/“Bắt buộc”; select `id=course-select` chỉ có placeholder disabled/selected, chưa có option/value. Local fallback yêu cầu `course_id:int64` và kiểm tra Course tồn tại; slug→ID/options source chưa có. | EV-03 |
| 19 `(54,797)` | Thời gian làm bài — number input group | Nhãn phút, placeholder `-- phút`, helper “Để trống nếu không giới hạn”; HTML `min=1,max=300`, không `required`. Local fallback nullable strict int, int32 range; 1–300 chưa phải business rule. | EV-03 |
| 20 `(640,798)` | Điểm đạt yêu cầu — number input group | Nhãn `%`, placeholder `-- %`, helper ngưỡng hoàn thành; HTML `min=0,max=100`, không `required`. Local fallback yêu cầu `passing_score` strict string biểu diễn được NUMERIC(5,2); map number→decimal string và 0–100 chưa duyệt. | EV-03 |
| 21 `(612,942)` | Tự động lưu bản ghi nháp — information card | Card xanh trong cấu hình; copy khẳng định lưu cục bộ. Không có localStorage, state persistence hoặc request trong HTML; chỉ là claim tĩnh. | EV-08 |
| 22 `(706,421)` | Ngân hàng câu hỏi & Đáp án — section heading | Card phải, nhãn “PHẦN 2 / 2”; không có dữ liệu câu hỏi. | — |
| 23 `(1512,502)` | Schema notice — information banner | Copy nói schema câu hỏi/thang điểm đang chờ chuẩn hóa. Là prototype notice, không phản ánh live schema/deployment. | EV-08 |
| 24 `(1095,641)` | Empty-state icon — decorative icon | Icon ballot ở giữa khung Questions; không có action/data. | — |
| 25 `(734,752)` | Empty-state heading — heading | “Chưa có câu hỏi nào được thêm vào bài kiểm tra”; empty state hiện trên prototype, không phải API result. | — |
| 26 `(1502,796)` | Empty-state description — supporting text | Copy mô tả chưa ghi nhận câu hỏi và chờ đồng bộ schema; không phải trạng thái backend. | — |
| 27 `(903,888)` | Thêm câu hỏi mới — disabled button | Button `disabled`, `aria-disabled=true`, có badge “Chức năng tạm khóa”; không có question/choice editor hay click handler. | EV-04 |
| 28 `(1511,1045)` | Questions Builder Gate — information notice | Notice lock ở cuối card; copy claim gate an toàn. Không có runtime gate/service evidence. | EV-08 |
| 29 `(55,1206)` | Trạng thái xác thực/RBAC — status strip | Dải cuối form khẳng định đã ghi nhận quyền Admin khảo thí; static text/icon, không phải auth result. | — |
| 30 `(1138,1208)` | Hủy bỏ — link/button | Anchor `#/admin/quizzes`. Không có dirty-state prompt, draft cleanup hoặc route runtime xác minh. | EV-07 |
| 31 `(1515,1208)` | Lưu bài kiểm tra — disabled button | Button `disabled`, `aria-disabled=true`; tooltip child ẩn khi không hover ghi “Vui lòng hoàn thiện cấu trúc câu hỏi hợp lệ”. Không có submit handler. | EV-05, EV-06 |
| 32 `(24,1334)` | Footer brand/copyright — footer text | “© 2025 Study2Work LMS. Hệ thống quản trị trung tâm.” Copy tĩnh. | — |
| 33 `(882,1347)` | Quy chế bảo mật dữ liệu — footer link | Anchor `href="#"`; destination/content không được cấu hình. | EV-09 |
| 34 `(1116,1347)` | Tiêu chuẩn phân quyền RBAC — footer link | Anchor `href="#"`; không phải bằng chứng policy hoặc tài liệu đã link. | EV-09 |
| 35 `(1382,1347)` | Hỗ trợ kỹ thuật hệ thống — footer link | Anchor `href="#"`; không có support handler. | EV-09 |

## 4. Conditional UI & state variations
- States theo inventory: blank/draft/loading/ready/dirty/invalid/saving/created/updated/not-found/conflict/unauthorized/forbidden/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/AD-16.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
