# SH-01 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: 2. Màn hình liên kết và luồng tổng quát

~~~mermaid
flowchart TD
    Entry[Trình duyệt mở route / đề xuất] --> Landing[Khung tĩnh SH-01]
    Landing -->|đọc công khai song song| Cats[GET #05 danh mục]
    Landing -->|đọc công khai song song| Courses[GET #06 khóa học đã xuất bản]
    Landing -->|tìm kiếm bằng q đã loại khoảng trắng| Search[GS-02 đề xuất /courses/search?q=]
    Landing -->|xem toàn bộ| Catalog[GS-01 đề xuất /courses]
    Landing -->|đăng nhập| Login[SH-02 đề xuất /login]
    Landing -->|đăng ký| Register[SH-03 đề xuất /register]
    Courses -->|chọn course_id trả về; chỉ là đích| Detail[GS-03 đề xuất; current #08 source, catalog D]
~~~

Yêu cầu #05 và #06 độc lập: phản hồi danh mục không lọc hoặc quyết định yêu cầu khóa học. Khung trang cùng nội dung biên tập đã duyệt có thể hiển thị trước khi hai phản hồi hoàn tất. Mỗi khu vực dữ liệu quản lý riêng trạng thái đang tải/rỗng/lỗi.

| Liên kết | Đích | Thao tác | Trạng thái hiện tại |
|---|---|---|---|
| Trang chủ/logo | SH-01 / | Liên kết trang chủ ở đầu/chân trang | Route đề xuất; chưa có router Study Web |
| Danh mục/xem tất cả khóa học | GS-01 /courses | Menu đầu trang hoặc nút “Xem tất cả” | Route đề xuất; có mã nguồn máy chủ #05/#06, chưa có màn hình client |
| Tìm kiếm | GS-02 /courses/search?q=<q đã mã hóa> | Gửi tìm kiếm không rỗng | Route đề xuất; GS-02 sở hữu API #07; SH-01 không gọi #07 |
| Đăng nhập | SH-02 /login | Menu hoặc nút kêu gọi hành động | Route đề xuất |
| Đăng ký | SH-03 /register | Menu hoặc nút kêu gọi hành động | Route đề xuất |
| Chi tiết thẻ khóa học | GS-03 /courses/:courseId | Chọn khóa học do #06 trả về | F02 chỉ định GS-03/#08; dòng SH-01 next-screen không liệt kê GS-03. Current #08 route/module source tồn tại dù catalog gắn D; chặn chờ quyết định điều hướng/client |
| Bộ lọc danh mục | Chưa có | Bấm thẻ trông giống danh mục | Tắt/chỉ để xem; #06 trả 422 với category cho tới khi G-05 được giải quyết |
| Thu thập email quan tâm | Chưa có | Nhập/bấm nút gửi trong ảnh | Không có endpoint được hỗ trợ; bỏ/tắt, không thu thập/gửi email |
| Nghề nghiệp/diễn đàn/pháp lý | Chưa xác minh đích trong task này | Liên kết đầu/chân trang | Chỉ dùng route/URL đã duyệt; href="#..." trong HTML gốc chỉ là neo, không chứng minh route thật |

### Trích từ DD nguồn: 3. Truy vết API và dữ liệu

| API | Phương thức và đường dẫn | Trạng thái nguồn | SH-01 sử dụng | Truy vết nguồn |
|---|---|---|---|---|
| #05 | GET /api/v1/categories | SOURCE_PRESENT; runtime chưa xác minh | Chỉ dải thông tin danh mục | [route](../../../../study-server/app/api/v1.py) → [view](../../../../study-server/app/modules/guest/api_05_categories/view.py) → [query](../../../../study-server/app/modules/guest/api_05_categories/query.py) → CategoryPage |
| #06 | GET /api/v1/courses | SOURCE_PRESENT; runtime chưa xác minh | Một trang thẻ khóa học đã xuất bản | [route](../../../../study-server/app/api/v1.py) → [view](../../../../study-server/app/modules/guest/api_06_courses/view.py) → [validator](../../../../study-server/app/modules/guest/api_06_courses/validate.py) → [query](../../../../study-server/app/modules/guest/api_06_courses/query.py) → [mapper](../../../../study-server/app/modules/guest/_shared/course_catalog/helpers.py) → CoursePage |
| #07 | GET /api/v1/courses/search | Có route/module source hiện tại; runtime chưa xác minh | Không gọi ở đây; GS-02 gửi yêu cầu sau điều hướng | F02, list_screen.md, API #007 và current Study route/module |
| #08 | GET /api/v1/courses/{course_id} | Có route/module source hiện tại; catalog vẫn gắn D | Không gọi ở SH-01; đích chi tiết còn mâu thuẫn điều hướng | [route](../../../../study-server/app/api/v1.py), current detail module/test source tồn tại; trạng thái inventory và next-screen cần xác nhận |

### 3.1 Chi tiết yêu cầu

**#05 danh mục**

~~~http
GET /api/v1/categories
~~~

- locale là query string tùy chọn dạng string. Nếu bỏ, phía máy chủ hiện dùng DEFAULT_LOCALE = "vi-VN"; giá trị truyền vào được đối chiếu chính xác, không trim/normalize.
- Truy vấn lấy dòng status = ACTIVE và locale khớp chính xác; sắp xếp id ASC.
- Không giả định mỗi danh mục đều có khóa học hoặc danh sách có số lượng khóa học.
- Không gửi ID/slug danh mục tới #06.

**#06 khóa học**

~~~http
GET /api/v1/courses?page=1&size=6
~~~

- page=1 và size=6 là yêu cầu hiển thị đề xuất của màn hình; size=6 nằm trong khoảng phía máy chủ hiện nhận 1..100. Mặc định phía máy chủ là trang 1, kích thước 20.
- Bỏ sort để dùng thứ tự mặc định của nguồn: created_at DESC, id ASC. Danh sách cho phép sort theo định dạng field:direction với field id, name, price, created_at và direction asc hoặc desc; nhãn ảnh như “phổ biến” không tương ứng với lựa chọn sắp xếp nào được cho phép.
- Không gửi category; bộ kiểm tra hiện trả 422 vì quan hệ/bộ lọc chưa được hỗ trợ.
- API đếm các dòng đã xuất bản, kiểm tra tính hợp lệ của người hướng dẫn và truy vấn trang PUBLISHED đã yêu cầu, ghép phần dữ liệu người hướng dẫn. Điều này không chứng minh nội dung danh mục đang chạy thật.

### 3.2 Ánh xạ phản hồi

| Trường UI | Nguồn API | Có thể rỗng / định dạng | Giới hạn |
|---|---|---|---|
| Tên danh mục | #05 items[].name | Chuỗi bắt buộc từ phản hồi | Không thay bằng tên trên ảnh nếu API không trả |
| Khóa danh mục | #05 items[].id | Số nguyên | Chỉ làm định danh UI; không phải bộ lọc đang hoạt động |
| Slug danh mục | #05 items[].slug | Chuỗi bắt buộc | Theo hành vi hiện tại, không gửi tới #06 |
| Mô tả danh mục | #05 items[].description | Chuỗi tùy chọn | Chỉ hiện nếu bố cục đã duyệt cần |
| Định danh khóa học | #06 items[].id | Số nguyên | Dùng làm định danh route ổn định; không tự tạo ID |
| Tiêu đề khóa học | #06 items[].title | Chuỗi bắt buộc | Lấy trực tiếp từ máy chủ |
| Mô tả khóa học | #06 items[].description | Có thể null | Bỏ qua khi null; không dùng câu mẫu thay thế |
| Ảnh thu nhỏ | #06 items[].thumbnail_url | URL có thể null | Thiếu thì dùng ô thay thế trung tính; không lấy ảnh khóa học giả |
| Giá | #06 items[].price | Số thập phân tuần tự hóa thành chuỗi | Không có tiền tệ; không tự thêm VND/giá giảm nếu chưa có quy tắc duyệt |
| Trạng thái | #06 items[].status | Chuỗi; truy vấn lấy PUBLISHED | Thường không cần hiển thị huy hiệu trên trang công khai |
| Tên người hướng dẫn | #06 items[].mentor.full_name | Chuỗi bắt buộc | Có trong nguồn; không thay bằng tên trên ảnh |
| Ảnh người hướng dẫn | #06 items[].mentor.avatar_url | URL có thể null | Thiếu thì dùng ảnh đại diện trung tính |
| Tổng số/trang | #06 data.pagination | page, size, total, total_pages | Chỉ hiển thị nếu hữu ích; không tạo số người học/bài học |

**Không có trong DTO #06:** tiền tệ, giá cũ/giảm, điểm đánh giá, số lượt đánh giá, thời lượng khóa học, số bài học, số ghi danh, danh mục, thứ hạng phổ biến hoặc cờ nổi bật. Đây chỉ là chi tiết của bản mẫu cho đến khi được duyệt nguồn/hợp đồng khác.

### Trích từ DD nguồn: 5. Đặc tả sự kiện và xử lý dữ liệu

Không có Study Web client/router trong checkout nên mọi sự kiện dưới đây là đặc tả có điều kiện, không phải behavior đã chạy. API response/error mapping dựa trên source hiện tại; không mô tả retry tự động, cache, debounce hoặc timeout vì chưa có client policy.

### SH01-EV-01 — Khởi tạo trang và tải dữ liệu công khai

- **Kích hoạt/loại/điều kiện:** Browser mở route đề xuất /; Page Load. Route hiện chưa được sở hữu bởi Study Web.
- **Đầu vào:** Không có auth token; locale tùy chọn nếu cấu hình locale Study được chốt. Query đề xuất: #05 không truyền locale để dùng vi-VN; #06 page=1,size=6, không truyền sort/category.
- **Xử lý:** 1) Render shell và copy đã duyệt. 2) Khởi tạo state hai vùng độc lập. 3) Gửi GET #05 và GET #06 song song sau khi có API base URL cấu hình. 4) Mỗi response đi vào mapping EV-06/07. 5) Không để lỗi một vùng xóa nội dung vùng còn lại.
- **API:** GET /api/v1/categories; GET /api/v1/courses?page=1&size=6; public, không cần Authorization theo source route. Không có request body. Retry do người dùng qua EV-11.
- **Kết quả/lỗi:** Mỗi vùng chuyển Loading → Ready/Empty/Error độc lập. Client chưa có source để xác minh timeout, cache, cancel hoặc retry tự động. TraceId chỉ dùng cho hỗ trợ lỗi nếu UI policy được duyệt.

### SH01-EV-02 — Gửi tìm kiếm hero

- **Kích hoạt/loại/điều kiện:** Element 5, Submit/Click; input #4 có q sau trim.
- **Đầu vào:** q:string từ người dùng, có thể gồm Unicode và whitespace.
- **Xử lý:** 1) Đọc giá trị hiện tại. 2) Trim whitespace đầu/cuối. 3) Nếu rỗng, giữ SH-01, không điều hướng/API; thông báo validation chưa được duyệt. 4) Nếu không rỗng, URL-encode q đúng một lần và chuyển sang route đề xuất GS-02 /courses/search?q=…. 5) Không gọi #07 tại SH-01; GS-02 sở hữu tìm kiếm.
- **API/đầu ra:** Không API ở SH-01. q là dữ liệu duy nhất đưa vào query string; không thêm email, token hoặc session data.
- **Ngoại lệ:** Không tự lowercase hoặc đặt maxlength khi chưa có contract. Lỗi route đích thuộc router/GS-02; hiện chưa có client runtime.

### SH01-EV-03 — Gửi tìm kiếm trong header của PNG

- **Kích hoạt/loại/điều kiện:** Element 1, Submit/Click nếu giữ lại control search trong thiết kế cuối.
- **Đầu vào/xử lý:** Chưa có input tương ứng trong code.html; nếu Product xác nhận cùng chức năng hero search, dùng trim/empty-check/encode của EV-02 và một route đích GS-02.
- **API/đầu ra/lỗi:** Không có API riêng; không tạo #07 request kép. Nếu không được xác nhận là input thật, bỏ control khỏi thiết kế triển khai. Asset hiện không thống nhất nên event chưa được bật.

### SH01-EV-04 — Mở khu vực khám phá/danh mục

- **Kích hoạt/loại/điều kiện:** CTA “Khám phá” ở Element 6 hoặc “Xem tất cả” ở Element 12; Click/Navigation.
- **Đầu vào:** Không có input do người dùng, không truyền filter. Route contract tương lai có thể chỉ định query; hiện không có.
- **Xử lý:** 1) Kiểm tra link đích nằm trong route inventory được duyệt. 2) Điều hướng tới GS-01 /courses. 3) Không gửi thêm #05/#06 từ SH-01 trừ khi client policy quy định; GS-01 sở hữu tải catalog.
- **API/đầu ra:** Không API ở sự kiện điều hướng. Đích và screen client chưa tồn tại trong checkout.
- **Ngoại lệ:** Không coi fragment của prototype là route ứng dụng. `#khoa-hoc` có thể cuộn trong chính tài liệu HTML; route không resolve thì router tương lai xử lý theo not-found contract.

### SH01-EV-05 — Mở đăng nhập hoặc đăng ký

- **Kích hoạt/loại/điều kiện:** Link header Element 1 hoặc CTA Element 6; Click/Navigation.
- **Đầu vào:** Không truyền credential hoặc email từ SH-01.
- **Xử lý:** 1) Link đăng nhập tới SH-02 /login nếu router xác nhận. 2) Link tạo tài khoản tới SH-03 /register chỉ khi CTA được xác định là đăng ký tài khoản. 3) Không gọi #01/#03 từ landing.
- **Kết quả/lỗi:** Điều hướng nội bộ; URL/query không chứa secret. CTA “đăng ký lộ trình” có thể mang nghĩa thu email, do đó bị chặn tới khi Product chọn nghĩa. Không có auth UI runtime được xác minh.

### SH01-EV-06 — Nhận và ánh xạ response danh mục #05

- **Kích hoạt/loại/điều kiện:** Response GET #05; API Response.
- **Đầu vào/response thành công:** success=true, businessCode=DESIGN_RESOURCE_RETRIEVED, data.items[] gồm {id,name,slug,description?}; data.pagination={page:1,size:total,total:total,total_pages:1}; meta và traceId đi cùng envelope. Nếu items rỗng, pagination={page:1,size:0,total:0,total_pages:1}. HTTP 200; message khi rỗng là “No active categories.”
- **Xử lý:** 1) Kiểm tra HTTP success/envelope. 2) Đọc data.items theo model, bỏ trường ngoài model. 3) Ánh xạ id/name/slug/description optional; hiển thị name thôi nếu chip được giữ. 4) items=[] chuyển EMPTY_CATEGORIES, không thay bằng mockup labels. 5) Giữ chip không tương tác tới khi G-05 có contract.
- **Kết quả:** HTTP 200 với envelope/model hợp lệ đưa riêng vùng danh mục sang READY; `items=[]` đưa vùng đó sang EMPTY_CATEGORIES. Hiện chỉ `name` có thể được hiển thị trên chip; vùng khóa học giữ nguyên trạng thái độc lập.
- **Lỗi:** Query type lỗi 422 / DESIGN_VALIDATION_ERROR; DB hoặc mapping lỗi 500 / DESIGN_INTERNAL_ERROR. Error envelope có success:false,businessCode,message,data:null,meta.fieldErrors nếu có,traceId; response header X-Trace-Id. Giữ course region độc lập; không biến lỗi thành EMPTY.
- **Nguồn hiện hành:** route /api/v1/categories → view.py → ACTIVE_CATEGORIES; status ACTIVE, locale chính xác, order id ASC; locale không truyền mặc định vi-VN. DB live chưa xác minh.

### SH01-EV-07 — Nhận và ánh xạ response khóa học #06

- **Kích hoạt/loại/điều kiện:** Response GET #06; API Response.
- **Đầu vào/response thành công:** Envelope {success:true,businessCode:DESIGN_RESOURCE_RETRIEVED,data:{items:[{id,title,description?,thumbnail_url?,price,status,mentor:{id,full_name,avatar_url?}}],pagination:{page,size,total,total_pages}},meta,traceId}. HTTP 200; empty thành công, total_pages=0 khi total=0.
- **Xử lý:** 1) Kiểm tra envelope/model. 2) Ánh xạ tối đa 6 items theo thứ tự trả về. 3) Dùng id làm key; hiển thị title, optional description/thumbnail, price giữ nguyên decimal, mentor.full_name và avatar optional. 4) Chỉ render status PUBLISHED mà server query trả; không tính ranking. 5) items=[] chuyển EMPTY_COURSES.
- **Kết quả:** HTTP 200 với model hợp lệ đưa riêng vùng khóa học sang READY; `items=[]` đưa vùng đó sang EMPTY_COURSES; `items` có dữ liệu hiển thị tối đa sáu course theo thứ tự response. Vùng danh mục giữ nguyên trạng thái độc lập.
- **Lỗi:** Invalid page/size/sort và category đều 422 / DESIGN_VALIDATION_ERROR; category có message “Bộ lọc category chưa được hỗ trợ.”. DB, lỗi mapping, giá/mentor thiếu hoặc orphan mentor trả 500 / DESIGN_INTERNAL_ERROR; error envelope dùng meta.fieldErrors nếu có, traceId và X-Trace-Id. Không biến lỗi thành rỗng và không xóa categories region.
- **Yêu cầu hiện tại đề xuất:** page=1,size=6, bỏ sort/category. Runtime server defaults page=1,size=20; size phải 1..100; sort allowlist id/name/price/created_at với asc/desc; default created_at DESC,id ASC. Client không thêm filter.

### SH01-EV-08 — Chọn chip danh mục

- **Kích hoạt/loại/điều kiện:** Element 9, Click; hiện bị khóa theo G-05.
- **Đầu vào:** Category item từ response #05 có id:int, slug:string.
- **Xử lý hiện tại:** Không cập nhật selected state, không điều hướng, không gửi #06. Source #06 từ chối bất kỳ category nào với HTTP 422 vì chưa có quan hệ filter được hỗ trợ.
- **Kết quả/ngoại lệ:** Chip phải là informational/disabled hoặc bị ẩn. Chỉ sau khi có contract/backend mapping mới xác định id hay slug, query param, pagination reset và trạng thái lỗi; không tự suy đoán.

### SH01-EV-09 — Điều khiển carousel, sort hoặc filter

- **Kích hoạt/loại/điều kiện:** Element 10 carousel arrows hoặc Element 12 tabs; Click.
- **Đầu vào:** Direction/filter/sort label từ prototype; không có enum/state contract hiện hành.
- **Xử lý hiện tại:** Không thay đổi danh sách, không thay URL và không gọi API. #06 chỉ chấp nhận sort id/name/price/created_at theo asc/desc; carousel behavior và filter mapping không có nguồn.
- **Kết quả/ngoại lệ:** Ẩn/disabled các control chưa được duyệt. “Xem tất cả” là link riêng EV-04. Không ánh xạ “phổ biến” thành sort khác.

### SH01-EV-10 — Chọn thẻ khóa học

- **Kích hoạt/loại/điều kiện:** Element 13, Click trên card sau khi #06 trả item.
- **Đầu vào:** course_id:int lấy đúng từ item.id; không dùng title/slug làm khóa.
- **Xử lý/đầu ra hiện tại:** F02 mô tả GS-03/#08 là trang kế tiếp; list_screen dòng SH-01 chỉ liệt kê GS-01, SH-02, SH-03 trong next screens. Current #08 route/module/test source tồn tại, trong khi catalog vẫn đánh #08 là D. Đây là discrepancy chưa quyết định. Không mở detail giả; giữ card không click hoặc chờ quyết định giữa GS-01 và GS-03.
- **API/lỗi:** SH-01 không gọi #08. Khi quyền route được chốt, màn GS-03 sở hữu GET /api/v1/courses/{course_id}; không thêm API behavior vào SH-01. Card không được báo thành công khi chưa navigate.

### SH01-EV-11 — Thử lại vùng danh mục hoặc khóa học lỗi

- **Kích hoạt/loại/điều kiện:** Nút retry được hiển thị trong vùng lỗi nếu implementation/Product duyệt; Click.
- **Đầu vào:** Vùng lỗi duy nhất, endpoint và query params cố định như EV-01.
- **Xử lý:** 1) Giữ state thành công ở vùng kia. 2) Chuyển đúng vùng sang LOADING. 3) Lặp đúng GET công khai với cùng params. 4) Ánh xạ bằng EV-06 hoặc EV-07. 5) Không retry tự động 422/query-invalid; sửa cấu hình trước khi có thao tác thủ công.
- **Kết quả/lỗi:** READY/EMPTY khi thành công, ERROR khi lại lỗi; không đổi ERROR thành EMPTY. Retry policy/limit/backoff chưa có client source nên không tự quy định.

### SH01-EV-12 — Nhập và submit email CTA

- **Kích hoạt/loại/điều kiện:** Elements 20–21, Input/Submit; form trong ảnh.
- **Đầu vào:** Email cá nhân do người dùng nhập.
- **Xử lý hiện tại:** Không validate, gửi, cache, analytics-track, lưu hay log email vì không có endpoint, purpose/consent, retention, deletion hoặc privacy contract.
- **Kết quả/lỗi:** Ẩn cả form hoặc để disabled với lý do accessible phù hợp; không hiển thị success giả. Chỉ triển khai sau khi Product/backend/privacy xác nhận endpoint, request schema, consent text, retention và error mapping.

### SH01-EV-13 — Điều hướng header/footer

- **Kích hoạt/loại/điều kiện:** Elements 1 và 24, Click/Navigation trên link cụ thể.
- **Đầu vào:** Destination ID/URL gắn với link; không có dữ liệu form.
- **Xử lý:** Chỉ điều hướng route có trong cross-screen inventory và được router Study đăng ký. Nội bộ: SH-01, GS-01, GS-02, SH-02, SH-03 theo điều kiện EV-02/04/05. Trong HTML hiện tại, `#khoa-hoc` và `#tim-kiem` khớp section ID; `#dang-nhap`, `#dang-ky`, `#dieu-khoan` không có target; bare `#` đưa trang về đầu. Legal/external link phải có URL được duyệt.
- **Kết quả/lỗi:** Chỉ fragment tới section ID thật mới có thể cuộn trong tài liệu HTML tĩnh; không có fragment nào xác nhận route SPA hoặc màn hình liên kết đang chạy. Điều hướng ứng dụng chỉ thực hiện một lần theo router đã đăng ký; route unknown xử lý bởi policy not-found tương lai. Hiện không có client để xác minh.

### SH01-EV-14 — Render nội dung tĩnh marketing/footer

- **Kích hoạt/loại/điều kiện:** Page render; Render.
- **Đầu vào:** Nội dung biên tập/brand, KPI, testimonial, logo, privacy labels, certificate, copyright trong PNG.
- **Xử lý:** Không gọi API. Render chỉ claim/copy/assets đã được Product/Marketing/legal owner xác nhận; ẩn số liệu, testimonial, partner labels, accreditation và email assurance chưa có bằng chứng. Chỉ dùng tài sản thương hiệu được phê duyệt.
- **Kết quả/lỗi:** Static content accessible, responsive; nội dung thiếu approval được lược khỏi thiết kế phát hành. Không thay bằng văn bản giả để lấp chỗ trống.

### Trích từ DD nguồn: 6. Mô hình trạng thái

| Trạng thái | Điều kiện vào | Hành vi giao diện | Khôi phục / chuyển tiếp |
|---|---|---|---|
| INITIAL | Route đang được phân giải | Khung/placeholder ổn định; không tạo nội dung giả | Bắt đầu đọc độc lập #05/#06 |
| LOADING theo khu vực | GET tương ứng đang chờ | Placeholder nằm trong chính vùng đó; vùng kia vẫn dùng được | READY, EMPTY hoặc lỗi riêng |
| READY theo khu vực | Phản hồi 200 hợp lệ | Chỉ hiển thị trường DTO đã ánh xạ | Điều hướng hoặc người dùng thử lại |
| EMPTY_CATEGORIES | #05 trả items=[] | Bỏ dải hoặc hiện trạng thái danh mục rỗng gọn | Chỉ thử lại khi người dùng yêu cầu |
| EMPTY_COURSES | #06 thành công nhưng items rỗng | Thông báo chưa có khóa học xuất bản; không có thẻ giả | Chỉ dùng liên kết danh mục/tìm kiếm nếu đích sẵn sàng |
| PARTIAL_ERROR | Một API lỗi, API kia thành công | Giữ khu vực thành công; khu vực lỗi có thông báo và nút thử lại | Thử lại GET của khu vực lỗi |
| VALIDATION_ERROR | API trả 422 | Lỗi khu vực an toàn; chỉ đưa trường/trace nếu hợp đồng lỗi dùng chung cung cấp | Sửa tham số client; không lặp yêu cầu sai |
| SERVICE_ERROR | 500/mạng/503 | Lỗi an toàn, thao tác thử lại, trace ID nếu có; không lộ chi tiết nội bộ | Người dùng chủ động thử lại |
| UNEXPECTED_AUTH_ERROR | GET công khai trả 401/403 | Lỗi an toàn; không tự chuyển trang | máy chủ/Sản phẩm điều tra; có thể hiện liên kết đăng nhập rõ ràng |
| NAVIGATING | Người dùng chọn thao tác hợp lệ | Tránh phát sự kiện điều hướng lặp khi đang xử lý | Route đích hoặc phương án dự phòng an toàn |
| BLOCKED_ACTION | Người dùng chọn tính năng danh mục/email/chi tiết chưa hỗ trợ | Giữ thao tác tắt hoặc không hiển thị, có dấu hiệu rõ | Chỉ bật sau khi hợp đồng/điều kiện tương ứng được giải quyết |

SH-01 không có cập nhật dữ liệu hay cập nhật lạc quan. HTTP 202 không liên quan tới các API hiện tại của màn hình.

### Trích từ DD nguồn: 9. Ma trận kiểm tra và rà soát (dự kiến; chưa chạy)

| Tình huống | Kết quả cần xác minh |
|---|---|
| #05 và #06 đều có dữ liệu | Mỗi khu vực ánh xạ riêng; không xuất hiện bản ghi mẫu tĩnh |
| #05 rỗng, #06 có dữ liệu | Thẻ khóa học vẫn hiện; trạng thái danh mục rỗng độc lập |
| #06 rỗng, #05 có dữ liệu | Thông tin danh mục vẫn còn; trạng thái khóa học không có thẻ giả |
| #05 lỗi, #06 thành công | Khu vực khóa học vẫn dùng được; thử lại danh mục chỉ tác động #05 |
| #06 lỗi, #05 thành công | Danh mục vẫn hiện; thử lại khóa học chỉ tác động #06 |
| #06 trả 422 vì category | Client không gửi category; ghi nhận hồi quy, không lặp mù |
| Tìm kiếm có khoảng trắng đầu/cuối | SH-01 loại khoảng trắng, chuyển q đã mã hóa tới GS-02; không gọi #07 tại đây |
| Tìm kiếm rỗng | Không gọi API; không tự đặt câu báo lỗi |
| Bấm thẻ danh mục | Không gửi bộ lọc khi G-05 còn mở |
| Chọn khóa học | Không tạo trạng thái chi tiết giả; tiếp tục chặn điều hướng cho tới khi quyết định #08/route |
| 401/403/500/lỗi mạng | Không tự chuyển đăng nhập cho GET công khai; khôi phục an toàn theo khu vực |
| Bàn phím/di động/tiếp cận | Rà soát focus, nhãn, vùng chạm 44px và bố cục 320px theo hướng dẫn chuẩn |
| Rà soát nguồn gốc | Không trình bày KPI, siêu dữ liệu khóa học, lời chứng thực, logo hoặc thu thập email chỉ có trên ảnh như dữ liệu đã xác thực |

Mã nguồn kiểm thử phía máy chủ liên quan: [API #05 tests](../../../../study-server/tests/modules/guest/api_05_categories/test_categories.py) (gồm test_categories_empty_result_is_successful_empty_page) và [API #06 tests](../../../../study-server/tests/modules/guest/api_06_courses/test_courses.py) (gồm test_courses_rejects_category_until_relation_exists cùng kiểm tra phân trang/lỗi). Đây là test source sử dụng fake session/data; chưa chạy trong phiên tài liệu. Hiện không có mã UI Study Web để kiểm thử.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: Có thể nạp một trang khóa học PUBLISHED; không tạo API hero/KPI mới.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [SH-01](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
