# SH-01 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `SH-01-EV-001` | `SH01-EV-01` / SH01-EV-01 — Khởi tạo trang và tải dữ liệu công khai | See source event detail below |
| `SH-01-EV-002` | `SH01-EV-02` / SH01-EV-02 — Gửi tìm kiếm hero | See source event detail below |
| `SH-01-EV-003` | `SH01-EV-03` / SH01-EV-03 — Gửi tìm kiếm trong header của PNG | See source event detail below |
| `SH-01-EV-004` | `SH01-EV-04` / SH01-EV-04 — Mở khu vực khám phá/danh mục | See source event detail below |
| `SH-01-EV-005` | `SH01-EV-05` / SH01-EV-05 — Mở đăng nhập hoặc đăng ký | See source event detail below |
| `SH-01-EV-006` | `SH01-EV-06` / SH01-EV-06 — Nhận và ánh xạ response danh mục #05 | See source event detail below |
| `SH-01-EV-007` | `SH01-EV-07` / SH01-EV-07 — Nhận và ánh xạ response khóa học #06 | See source event detail below |
| `SH-01-EV-008` | `SH01-EV-08` / SH01-EV-08 — Chọn chip danh mục | See source event detail below |
| `SH-01-EV-009` | `SH01-EV-09` / SH01-EV-09 — Điều khiển carousel, sort hoặc filter | See source event detail below |
| `SH-01-EV-010` | `SH01-EV-10` / SH01-EV-10 — Chọn thẻ khóa học | See source event detail below |
| `SH-01-EV-011` | `SH01-EV-11` / SH01-EV-11 — Thử lại vùng danh mục hoặc khóa học lỗi | See source event detail below |
| `SH-01-EV-012` | `SH01-EV-12` / SH01-EV-12 — Nhập và submit email CTA | See source event detail below |
| `SH-01-EV-013` | `SH01-EV-13` / SH01-EV-13 — Điều hướng header/footer | See source event detail below |
| `SH-01-EV-014` | `SH01-EV-14` / SH01-EV-14 — Render nội dung tĩnh marketing/footer | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

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

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
