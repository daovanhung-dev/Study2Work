# SH-01 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `SH-01-API-001` | #05 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `SH-01-API-002` | #06 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #05, #06
- Orchestration/data notes: Có thể nạp một trang khóa học PUBLISHED; không tạo API hero/KPI mới.
- BE/source status và gate: **R**
- Contract sources and discrepancies are preserved in the source excerpts below.

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

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01.md)
