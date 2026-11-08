# SH-01 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [SH-01_markers.json](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `SH-01-EL-001` | `SH01-EL-01` | Header brand, navigation and utility group |
| #2 | `SH-01-EL-002` | `SH01-EL-02` | Hero campaign badge |
| #3 | `SH-01-EL-003` | `SH01-EL-03` | Hero title and supporting copy |
| #4 | `SH-01-EL-004` | `SH01-EL-04` | Hero search input |
| #5 | `SH-01-EL-005` | `SH01-EL-05` | Hero search submit button |
| #6 | `SH-01-EL-006` | `SH01-EL-06` | Hero CTA pair |
| #7 | `SH-01-EL-007` | `SH01-EL-07` | Three marketing KPI cards |
| #8 | `SH-01-EL-008` | `SH01-EL-08` | Category section heading |
| #9 | `SH-01-EL-009` | `SH01-EL-09` | Category chip row |
| #10 | `SH-01-EL-010` | `SH01-EL-10` | Category carousel controls |
| #11 | `SH-01-EL-011` | `SH01-EL-11` | Published-course section title and subtitle |
| #12 | `SH-01-EL-012` | `SH01-EL-12` | Course sort/filter and view-all controls |
| #13 | `SH-01-EL-013` | `SH01-EL-13` | Six repeated course-card grid |
| #14 | `SH-01-EL-014` | `SH01-EL-14` | Benefits section heading and intro |
| #15 | `SH-01-EL-015` | `SH01-EL-15` | Three benefit cards |
| #16 | `SH-01-EL-016` | `SH01-EL-16` | Testimonial section heading and metric |
| #17 | `SH-01-EL-017` | `SH01-EL-17` | Three testimonial cards |
| #18 | `SH-01-EL-018` | `SH01-EL-18` | Employer logo strip |
| #19 | `SH-01-EL-019` | `SH01-EL-19` | Email CTA heading and copy |
| #20 | `SH-01-EL-020` | `SH01-EL-20` | Email input |
| #21 | `SH-01-EL-021` | `SH01-EL-21` | Email submit action |
| #22 | `SH-01-EL-022` | `SH01-EL-22` | Privacy and reassurance labels |
| #23 | `SH-01-EL-023` | `SH01-EL-23` | Footer brand and description |
| #24 | `SH-01-EL-024` | `SH01-EL-24` | Footer navigation columns |
| #25 | `SH-01-EL-025` | `SH01-EL-25` | Accreditation badges |
| #26 | `SH-01-EL-026` | `SH01-EL-26` | Copyright and platform tagline |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 4. Đặc tả các element có đánh số

Marker 1–26 ánh xạ một-một tới Element ID trong [bản đồ marker](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01_markers.json) và [ảnh chú thích](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/screen_annotated.png). Marker xác định nhóm component nhìn thấy trong PNG; component lặp được đặc tả một lần theo dạng reusable, còn số lượng instance hiện có được ghi rõ. Marker không xác nhận control đang chạy.

| # / Element ID | Loại, vị trí và mục đích | Thuộc tính, nguồn và điều kiện hiển thị | Trạng thái / sự kiện |
|---|---|---|---|
| 1 · SH01-EL-01 | Header; logo, nav, ô tìm kiếm rút gọn, tiện ích, auth/account | PNG có logo, menu, search summary, chuông, avatar. HTML chỉ có logo/nav/login/register. Không có profile/session contract cho khách; không dùng chuông/avatar như control khi chưa chốt. Route chỉ lấy từ inventory đã duyệt. | Default, focus, mobile menu chưa có source. EV-03, EV-05, EV-13. |
| 2 · SH01-EL-02 | Badge/campaign ở đầu hero | Nội dung đợt, ngày và claim trên PNG là editorial, không có API. Chỉ hiển thị sau Product approval; nếu không, ẩn. | Static; không có action. EV-01, EV-14. |
| 3 · SH01-EL-03 | Tiêu đề và mô tả hero | Editorial copy; HTML/PNG không đồng nhất. Không lấy nội dung bản mẫu làm claim sản phẩm đã duyệt. | Static; cần line wrap responsive và heading semantics. EV-01, EV-14. |
| 4 · SH01-EL-04 | Input tìm kiếm hero | Chuỗi UTF-8 do khách nhập; mặc định rỗng; optional. Trim hai đầu khi submit. Chưa có maxlength hoặc quy tắc chuẩn hóa chữ hoa/thường được source xác nhận; không tự đặt. | Empty, editing, focus, validation-empty. EV-02. |
| 5 · SH01-EL-05 | Nút submit tìm kiếm hero | Button liên kết với input #4; enabled khi có q sau trim theo đề xuất, nếu không thì giữ ở SH-01. Không gọi API tại SH-01. | Default, focus, disabled khi rỗng theo proposal. EV-02. |
| 6 · SH01-EL-06 | Cặp CTA hero: khám phá / đăng ký lộ trình | Ảnh có hai CTA; HTML trỏ “Khám phá” tới section `#khoa-hoc` và CTA còn lại tới `#dang-ky` nhưng không có section target. Fragment không phải route Study. CTA còn lại chỉ nối SH-03 nếu xác nhận là tạo tài khoản thay vì đăng ký email. | Default/focus. EV-04, EV-05. |
| 7 · SH01-EL-07 | Ba KPI card | 10,000+, 120+, 94% không có API/định nghĩa/nguồn hiện hành. Ẩn cho tới khi có nguồn và duyệt claim. Không tính từ #05/#06. | Suppressed; không có action. EV-14. |
| 8 · SH01-EL-08 | Tiêu đề/eyebrow phần danh mục | Nội dung editorial; không phải response #05. Chỉ giữ khi được duyệt. | Static; responsive text. EV-06, EV-14. |
| 9 · SH01-EL-09 | Hàng chip danh mục (5 instance trong PNG) | #05 cung cấp id:int, name:string, slug:string, description?:string|null. Không có count/icon/featured flag. G-05 còn mở nên chip chỉ informational hoặc bị ẩn; không gửi category tới #06. | Loading, ready, empty, error theo region; chip disabled. EV-06, EV-08, EV-11. |
| 10 · SH01-EL-10 | Nút carousel danh mục trước/sau | Hai button trên PNG; HTML/API không chỉ ra carousel, state, số bước hoặc hành vi cuộn. Để ẩn/disabled tới khi thiết kế được chọn và hành vi được duyệt. | Không có trạng thái vận hành xác nhận. EV-09. |
| 11 · SH01-EL-11 | Tiêu đề/mô tả section khóa học | Nội dung editorial; không có field featured/popular trong #06. Không gắn nhãn xếp hạng chưa có nguồn. | Static; EV-07, EV-14. |
| 12 · SH01-EL-12 | Filter/sort tabs và “Xem tất cả” | “Tất cả” có thể điều hướng GS-01 theo inventory. Sort #06 chỉ hỗ trợ id/name/price/created_at theo asc/desc; không ánh xạ nhãn phổ biến/bán chạy khi chưa duyệt. Filter không có nguồn. | Các tab chưa hỗ trợ ẩn/disabled; link “Xem tất cả” focusable khi router được triển khai. EV-04, EV-09, EV-13. |
| 13 · SH01-EL-13 | Lưới sáu course-card lặp | API #06: id:int, title:string, description?:string|null, thumbnail_url?:string|null, price:string decimal, status:string=PUBLISHED, mentor{id:int,full_name:string,avatar_url?:string|null}. Không có currency, discount, category, review, duration, lesson count hoặc enrollment count. | Loading, ready, empty, partial/error; card navigation bị chặn tới khi #08/route được quyết định. EV-07, EV-10, EV-11. |
| 14 · SH01-EL-14 | Tiêu đề và intro section lợi ích | Nội dung editorial, không có feature API hoặc claim contract. Ẩn nội dung chưa được duyệt. | Static; EV-14. |
| 15 · SH01-EL-15 | Ba benefit card lặp | Icon/text/copy từ PNG; không suy luận rằng tính năng hoặc dịch vụ có runtime. Nội dung phải được duyệt; decorative icon có alt rỗng. | Static; EV-14. |
| 16 · SH01-EL-16 | Tiêu đề testimonial và metric | Không có nguồn cho metric/tổng đánh giá; #10 nếu có là review theo course và hiện không được SH-01 gọi. | Ẩn nếu chưa xác minh; EV-14. |
| 17 · SH01-EL-17 | Ba testimonial card lặp | Quote, rating, tên, avatar, chức danh là dữ liệu cá nhân/claim không có API/consent source tại SH-01. Không render như feedback thật. | Suppressed tới khi có nguồn, quyền sử dụng và duyệt. EV-14. |
| 18 · SH01-EL-18 | Dải 5 employer/company labels | Logo/tên doanh nghiệp là claim quan hệ đối tác; không có API hoặc asset authorization trong nguồn. | Suppressed tới khi được duyệt. EV-14. |
| 19 · SH01-EL-19 | Tiêu đề và copy CTA email | Không có lead/newsletter endpoint hoặc consent contract. | Suppressed/disabled cùng form. EV-12, EV-14. |
| 20 · SH01-EL-20 | Email input | type=email chỉ là loại control nhìn thấy trong PNG, không tạo quy tắc lưu trữ. Không đọc/ghi/log giá trị trong implementation hiện tại. | Không hoạt động; EV-12. |
| 21 · SH01-EL-21 | Nút gửi email | Không có API/HTTP behavior xác nhận. Không gửi request. | Disabled hoặc toàn form bị ẩn; EV-12. |
| 22 · SH01-EL-22 | Privacy/reassurance labels dưới form | Claim không spam, quyền riêng tư và assurance không có policy/source ở tài liệu này. | Chỉ hiện sau approval; EV-14. |
| 23 · SH01-EL-23 | Footer brand/description | Tên/logo và mô tả brand tĩnh; dùng đúng asset/copy được duyệt. | Static; EV-13, EV-14. |
| 24 · SH01-EL-24 | Các cột link footer | Prototype dùng fragment: một số quay đầu trang hoặc cuộn tới `#khoa-hoc`/`#tim-kiem`; `#dang-nhap`, `#dang-ky`, `#dieu-khoan` không có phần tử target. Label/fragment không xác nhận route/URL. Chỉ bật route có trong inventory và router tương lai; external/legal URL cần phê duyệt. | Default/focus; không coi fragment là route ứng dụng. EV-13. |
| 25 · SH01-EL-25 | Huy hiệu accreditation | Không có issuer, credential ID, thời hạn hoặc bằng chứng xác thực. | Suppressed tới khi được xác minh; EV-14. |
| 26 · SH01-EL-26 | Copyright/tagline cuối trang | Năm bản quyền/tagline là nội dung ownership chưa xác nhận. | Static sau approval; EV-14. |

### 4.1 Quy tắc ánh xạ lặp

- Category row: mỗi item #05 thành tối đa một chip; key ổn định là id. Chỉ render name. Không tạo count/icon, không suy ra số course từ dữ liệu không có. Description chỉ dùng nếu thiết kế được duyệt cần.
- Course grid: mỗi item #06 thành một card, theo đúng thứ tự máy chủ; page request đề xuất size=6. Key là id. Thumbnail và avatar null dùng placeholder trung tính không mang nội dung course/person giả. Title và mentor.full_name là bắt buộc theo model. Description có thể bỏ khi null.
- Giá từ #06 là chuỗi decimal không chứa currency; giữ chuỗi chính xác hoặc chỉ format theo quy tắc tiền tệ được phê duyệt. Không cộng thuế, giảm giá hoặc ký hiệu tiền.
- Các nhóm lặp #15 và #17 có 3 instance trong ảnh; số instance này chỉ mô tả source asset, không tuyên bố số record vận hành.
- Không có input state cache/session được xác nhận cho Study Web. Quy tắc request dưới đây là thiết kế đề xuất bị chặn cho tới khi client/router được bổ sung.

## 4. Conditional UI & state variations
- States theo inventory: skeleton/list/empty/network-error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
