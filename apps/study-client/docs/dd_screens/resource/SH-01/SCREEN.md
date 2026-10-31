# SH-01 — Public Study landing/home

**Trạng thái:** `DESIGN_TARGET / NOT_IMPLEMENTED` · **Route:** `/` · **Actor:** Guest · **AC-03** · **W0**.

## Phạm vi và ranh giới bằng chứng

Đây là bản bàn giao thiết kế, không phải màn hình đã triển khai. Study Web source/router chưa có trong checkout. Các tên chủ đề, khóa học và mentor trên hình đều là `VISUAL_SAMPLE` tĩnh, không phải dữ liệu trả về từ API. Không có screen con, modal, drawer hoặc search suggestion.

## Layout desktop và responsive

| Vùng | Hình học chính xác ở 1440×1320 | Tablet 768–1023 | Mobile 320–767 |
|---|---|---|---|
| Container | x=160–1280, max-width 1120; gutter 32 | gutter 24 | gutter 16 |
| Header | y=24–96, h=72, surface white, border-bottom 1px | một hàng, thu hẹp spacing | brand thay Trang chủ; Courses/login/register một hàng compact, không drawer; target ≥44 |
| Hero | copy x=160–758; art x=802 y=135 w=478 h=347; search y=422 | copy rồi art theo chiều dọc | ẩn art; search input rồi button full-width |
| Categories | separator y=510; heading y=519; nhãn taxonomy x=172/307, y=611–632; accent 2×16 tại x=172/307 | giữ 2 nhãn text, wrap khi cần | wrap nhãn tĩnh; không click/tap/focus |
| Courses | heading y=684; cards x=160/541/922, y=753, w=357 h=369, gap=24 | 2 cột | 1 cột; nội dung dài tự tăng chiều cao |
| Footer | separator y=1177; brand y=1200; links y=1206 | co giãn | xếp dọc, links wrap |

## Bản đồ 41 thành phần

Tọa độ `x,y,w,h` là **pixel tuyệt đối** của bản SVG desktop cuối cùng. Font Inter được cài cục bộ; không dùng font mạng. `N/A` nghĩa là không có typography. Những nhóm art trong một thumbnail là một leaf duy nhất. Các course card và nhãn taxonomy đều **không tương tác**.

| # | Tên/nội dung | x,y,w,h (px) | Typography | Background / border / radius / alignment | Semantics | Event / target | Hover, focus, pressed | Responsive | Source |
|---|---|---|---|---|---|---|---|---|---|
| #1 | Biểu tượng Study | 160,43,34,34 | N/A | fill #0B5F8A; white line icon; radius 9px; border none; left | brand link | đến `/` | hover 140ms đổi màu #084968 hoặc underline; focus 2px #0B5F8A offset 2px; pressed #084968 | mobile: giữ cùng wordmark | STATIC_UI |
| #2 | Study wordmark | 207,45,77,29 | Inter 24px/29px/700 #073B57 | nền none; border none; left | brand link | đến `/` | hover 140ms đổi màu #084968 hoặc underline; focus 2px #0B5F8A offset 2px; pressed #084968 | mobile: giữ | STATIC_UI |
| #3 | Trang chủ | 656,48,76,34 | Inter 15px/22px/600 #0B5F8A | underline #0B5F8A 2px; background none; border none | navigation link | đến `/` | hover 140ms đổi màu #084968 hoặc underline; focus 2px #0B5F8A offset 2px; pressed #084968 | mobile: ẩn vì brand dẫn về `/` | STATIC_UI |
| #4 | Khóa học | 780,48,75,24 | Inter 15px/22px/600 #17324D | background none; border none | navigation link | đến `/courses` (GS-01) | hover 140ms đổi màu #084968 hoặc underline; focus 2px #0B5F8A offset 2px; pressed #084968 | mobile: giữ trên cùng hàng compact | STATIC_UI |
| #5 | Đăng nhập | 1002,48,91,24 | Inter 15px/22px/600 #17324D | background none; border none | navigation link | đến `/login` (SH-02) | hover 140ms đổi màu #084968 hoặc underline; focus 2px #0B5F8A offset 2px; pressed #084968 | mobile: giữ trên cùng hàng compact | STATIC_UI |
| #6 | Đăng ký | 1139,36,141,48 | Inter 15px/22px/600 #FFFFFF | fill #0B5F8A; border none; radius 10px; centered | navigation link | đến `/register` (SH-03) | hover 140ms đổi màu #084968 hoặc underline; focus 2px #0B5F8A offset 2px; pressed #084968 | mobile: giữ, compact target ≥44px | STATIC_UI |
| #7 | HỌC ĐIỀU BẠN QUAN TÂM | 176,139,295,18 | Inter 13px/18px/600 #0B5F8A | accent stripe x160 y143 4×17 #43A5C5; border none | static text | không có | không áp dụng | mobile: giữ; xuống dòng nếu cần | STATIC_UI |
| #8 | Bắt đầu hành trình / học tập của bạn | 160,174,580,116 | Inter 48px/58px/700 #073B57 | background none; border none; left | h1 | không có | không áp dụng | tablet/mobile: reflow theo bề rộng, giữ 48/58 desktop | STATIC_UI |
| #9 | Hero supporting paragraph | 160,310,565,52 | Inter 16px/26px/400 #536A7A | background none; border none | paragraph | không có | không áp dụng | mobile: tự wrap theo 320px | STATIC_UI |
| #10 | Tìm kiếm khóa học | 160,388,188,20 | Inter 14px/20px/600 #17324D | background none; border none | visible input label | không có | không áp dụng | mobile: giữ trên input | STATIC_UI |
| #11 | Bạn muốn học điều gì? | 160,422,401,56 | Inter 15px/22px/400 #536A7A | fill white; border 1px #D4E2E9; radius 11px; left padding 51px | search textbox | typing lưu q; Enter submit | idle border #D4E2E9; focus 2px #0B5F8A offset 2px; typing cập nhật q; submitting chuyển route | mobile: full width | STATIC_UI |
| #12 | Biểu tượng kính lúp | 178,442,19,19 | N/A | outline #536A7A 1.9px; background none; border none | decorative icon | không có | không áp dụng | mobile: trong input | STATIC_UI |
| #13 | Tìm khóa học | 573,422,185,56 | Inter 15px/22px/600 #FFFFFF | fill #0B5F8A; border none; radius 11px; centered | submit button | trim q; q khác rỗng → `/courses/search?q=${encodeURIComponent(q)}` (GS-02); rỗng → `/courses` (GS-01) | hover 140ms đổi màu #084968 hoặc underline; focus 2px #0B5F8A offset 2px; pressed #084968 | mobile: full width dưới input | STATIC_UI |
| #14 | Editorial learning desk illustration | 802,135,478,347 | N/A | vector grouped: background #E8F4FA radius 26; laptop/paper; border none | decorative group | không có | không áp dụng | tablet: sau copy; mobile: ẩn | STATIC_UI |
| #15 | Khám phá theo chủ đề | 160,519,402,38 | Inter 30px/38px/600 #073B57 | background none; border none | h2 | không có | không áp dụng | desktop: giữ nguyên; tablet: co giãn; mobile: xếp theo luồng | STATIC_UI |
| #16 | Một vài chủ đề để tham khảo khi khám phá nội dung học. | 160,566,560,20 | Inter 14px/20px/400 #536A7A | background none; border none | paragraph | không có | không áp dụng | desktop: giữ nguyên; tablet: co giãn; mobile: xếp theo luồng | STATIC_UI |
| #17 | Lập trình | 172,611,71,21 | Inter 14px/20px/500 #17324D | background transparent; border none; radius 0px; text left at x184 baseline y631; decorative accent x172 y616 2×16px #43A5C5 | static label | không có | không áp dụng (không hover/focus/pressed) | tablet: inline, mobile: wrap; không pointer/hover | #05 GET /api/v1/categories; VISUAL_SAMPLE |
| #18 | Thiết kế | 307,611,66,21 | Inter 14px/20px/500 #17324D | background transparent; border none; radius 0px; text left at x319 baseline y631; decorative accent x307 y616 2×16px #43A5C5 | static label | không có | không áp dụng (không hover/focus/pressed) | tablet: inline, mobile: wrap; không pointer/hover | #05 GET /api/v1/categories; VISUAL_SAMPLE |
| #19 | Một số khóa học | 160,684,340,38 | Inter 30px/38px/600 #073B57 | background none; border none | h2 | không có | không áp dụng | desktop: giữ nguyên; tablet: co giãn; mobile: xếp theo luồng | STATIC_UI |
| #20 | Xem tất cả | 1181,697,78,28 | Inter 15px/22px/600 #0B5F8A | underline 1px #0B5F8A; background none; border none | navigation link | đến `/courses` (GS-01) | hover 140ms đổi màu #084968 hoặc underline; focus 2px #0B5F8A offset 2px; pressed #084968 | mobile: giữ bên phải nếu đủ rộng; ngược lại xuống dòng | STATIC_UI |
| #21 | Cover minh họa: Xây dựng ứng dụng Web | 176,769,325,169 | N/A | vector editorial #1; nền #E7F2F7; radius 10px; border none | decorative image | không có | không áp dụng | tablet: 2 cột; mobile: 1 cột | #06 GET /api/v1/courses; VISUAL_SAMPLE; thumbnail_url nullable |
| #22 | Xây dựng ứng dụng Web | 180,952,317,26 | Inter 18px/26px/600 #073B57 | background white; border none; left | static course title | không có | không áp dụng | tablet: 2 cột; mobile: 1 cột | #06 title; VISUAL_SAMPLE |
| #23 | Tìm hiểu cách tạo giao diện và kết nối các phần của website. | 180,982,317,42 | Inter 14px/20px/400 #536A7A | background white; border none; left; two lines | static course description | không có | không áp dụng | mobile: wrap; null description → hide | #06 description nullable; VISUAL_SAMPLE |
| #24 | Avatar mentor | 180,1063,38,38 | N/A | fill #E8F4FA; border 1px #D4E2E9; circular 38px; placeholder vector | decorative avatar | không có | không áp dụng | mobile: giữ 38px | #06 mentor.avatar_url nullable; VISUAL_SAMPLE |
| #25 | Nguyễn Minh Anh | 229,1068,246,22 | Inter 14px/20px/500 #17324D | background white; border none; left | static mentor name | không có | không áp dụng | mobile: wrap nếu cần | #06 mentor.full_name; VISUAL_SAMPLE |
| #26 | Cover minh họa: Thiết kế giao diện số | 557,769,325,169 | N/A | vector editorial #2; nền #EDF4F7; radius 10px; border none | decorative image | không có | không áp dụng | tablet: 2 cột; mobile: 1 cột | #06 GET /api/v1/courses; VISUAL_SAMPLE; thumbnail_url nullable |
| #27 | Thiết kế giao diện số | 561,952,317,26 | Inter 18px/26px/600 #073B57 | background white; border none; left | static course title | không có | không áp dụng | tablet: 2 cột; mobile: 1 cột | #06 title; VISUAL_SAMPLE |
| #28 | Làm quen với bố cục, màu sắc và trải nghiệm người dùng. | 561,982,317,42 | Inter 14px/20px/400 #536A7A | background white; border none; left; two lines | static course description | không có | không áp dụng | mobile: wrap; null description → hide | #06 description nullable; VISUAL_SAMPLE |
| #29 | Avatar mentor | 561,1063,38,38 | N/A | fill #E8F4FA; border 1px #D4E2E9; circular 38px; placeholder vector | decorative avatar | không có | không áp dụng | mobile: giữ 38px | #06 mentor.avatar_url nullable; VISUAL_SAMPLE |
| #30 | Trần Hải Nam | 610,1068,246,22 | Inter 14px/20px/500 #17324D | background white; border none; left | static mentor name | không có | không áp dụng | mobile: wrap nếu cần | #06 mentor.full_name; VISUAL_SAMPLE |
| #31 | Cover minh họa: Nhập môn Python | 938,769,325,169 | N/A | vector editorial #3; nền #E6F1F5; radius 10px; border none | decorative image | không có | không áp dụng | tablet: 2 cột; mobile: 1 cột | #06 GET /api/v1/courses; VISUAL_SAMPLE; thumbnail_url nullable |
| #32 | Nhập môn Python | 942,952,317,26 | Inter 18px/26px/600 #073B57 | background white; border none; left | static course title | không có | không áp dụng | tablet: 2 cột; mobile: 1 cột | #06 title; VISUAL_SAMPLE |
| #33 | Bắt đầu với tư duy lập trình qua những bài tập thực tế. | 942,982,317,42 | Inter 14px/20px/400 #536A7A | background white; border none; left; two lines | static course description | không có | không áp dụng | mobile: wrap; null description → hide | #06 description nullable; VISUAL_SAMPLE |
| #34 | Avatar mentor | 942,1063,38,38 | N/A | fill #E8F4FA; border 1px #D4E2E9; circular 38px; placeholder vector | decorative avatar | không có | không áp dụng | mobile: giữ 38px | #06 mentor.avatar_url nullable; VISUAL_SAMPLE |
| #35 | Lê Thu Hà | 991,1068,246,22 | Inter 14px/20px/500 #17324D | background white; border none; left | static mentor name | không có | không áp dụng | mobile: wrap nếu cần | #06 mentor.full_name; VISUAL_SAMPLE |
| #36 | Footer brand symbol | 160,1200,29,29 | N/A | fill #0B5F8A; white line icon; radius 8px; border none | brand link | đến `/` | hover 140ms đổi màu #084968 hoặc underline; focus 2px #0B5F8A offset 2px; pressed #084968 | mobile: footer stack | STATIC_UI |
| #37 | Footer Study wordmark | 202,1203,67,25 | Inter 20px/25px/700 #073B57 | background none; border none | brand link | đến `/` | hover 140ms đổi màu #084968 hoặc underline; focus 2px #0B5F8A offset 2px; pressed #084968 | mobile: footer stack | STATIC_UI |
| #38 | Một không gian để khám phá và bắt đầu học tập. | 160,1241,460,20 | Inter 13px/20px/400 #536A7A | background none; border none | static paragraph | không có | không áp dụng | mobile: wrap | STATIC_UI |
| #39 | Footer Khóa học | 989,1206,79,24 | Inter 14px/20px/500 #17324D | background none; border none | navigation link | đến `/courses` | hover 140ms đổi màu #084968 hoặc underline; focus 2px #0B5F8A offset 2px; pressed #084968 | mobile: footer links wrap | STATIC_UI |
| #40 | Footer Đăng nhập | 1091,1206,94,24 | Inter 14px/20px/500 #17324D | background none; border none | navigation link | đến `/login` | hover 140ms đổi màu #084968 hoặc underline; focus 2px #0B5F8A offset 2px; pressed #084968 | mobile: footer links wrap | STATIC_UI |
| #41 | Footer Đăng ký | 1207,1206,73,24 | Inter 14px/20px/500 #17324D | background none; border none | navigation link | đến `/register` | hover 140ms đổi màu #084968 hoặc underline; focus 2px #0B5F8A offset 2px; pressed #084968 | mobile: footer links wrap | STATIC_UI |

## API boundary và orchestration

- **#05** `GET /api/v1/categories`: locale mặc định `vi-VN`, exact locale, chỉ category `ACTIVE`; fields `id`, `name`, `slug`, `description` nullable. Empty với HTTP 200 là success. Chỉ hiển thị metadata read-only, không lọc khóa học.
- **#06** `GET /api/v1/courses?page=1&size=3`: chỉ `PUBLISHED`; page=1; default size=20, range 1–100. Fields `id`, `title`, `description` nullable, `thumbnail_url` nullable, `price` decimal-string, `status`, `mentor.full_name`, `mentor.avatar_url` nullable. Chỉ render title, description, thumbnail, mentor; không render giá vì không biết currency/unit, không render status.
- **Không truyền `category` vào #06** vì API hiện trả 422. Không có course.category trong response. Không tạo giả rating, review, student count, popularity, testimonial, API/route/field khác.
- Fetch categories và courses độc lập; mỗi section có state và retry riêng. Không tự quy định cache TTL. Trace ID chỉ hiển thị khi backend thực sự trả.

## Search và điều hướng

- Input có label hiển thị “Tìm kiếm khóa học”, placeholder “Bạn muốn học điều gì?”. Enter và button cùng submit handler.
- `qTrimmed = q.trim()`. Nếu khác rỗng, điều hướng **GS-02** `/courses/search?q=${encodeURIComponent(qTrimmed)}` (encode đúng một lần). Nếu rỗng, điều hướng **GS-01** `/courses` và **không gửi q rỗng**. Không có autocomplete/suggestion.
- Header/footer brand và Trang chủ → `/`; Khóa học/Xem tất cả/footer Khóa học → GS-01 `/courses`; Đăng nhập → SH-02 `/login`; Đăng ký → SH-03 `/register`.
- Card khóa học không link. Course detail **GS-03** thuộc luồng GS-01, không được mở từ SH-01. Nhãn taxonomy #17/#18 là static labels, không filter, không event.

## States chi tiết

| Section | Loading | Ready | Empty | Error |
|---|---|---|---|---|
| Categories #05 | skeleton dạng dòng chữ nhỏ (không capsule), aria-busy, không tạo dữ liệu giả | hiện ACTIVE từ response | HTTP 200 empty: “Chưa có chủ đề để hiển thị.” | thông báo lỗi riêng, “Thử lại” gọi lại đúng GET #05 |
| Courses #06 | 3 skeleton card ổn định, aria-busy, không tạo data giả | render tối đa 3 course từ page=1,size=3 | “Hiện chưa có khóa học để giới thiệu.” | thông báo lỗi riêng, “Thử lại” gọi lại đúng GET #06 |
| Nullable | N/A | thumbnail/avatar null dùng placeholder kín đáo; description null ẩn và reflow | N/A | không gán URL giả |
| Search | idle: placeholder | focus: outline 2px; typing: cập nhật local q | submit blank → GS-01 | submitting: điều hướng, không giả endpoint tìm kiếm |

Các thông báo trạng thái chỉ là **state specification**, không phải thành phần hiển thị thêm trên main mockup và không nằm trong marker map.

## Accessibility / visual tokens

- Font: Inter local, fallback system sans. H1 **48/58/700** đúng guide; body **16/26/400**; section **30/38/600**; card title **18/26/600**; description **14/20/400**; mentor **14/20/500**; nav **15/22/600**; eyebrow **13/18/600**.
- Tokens: page `#F6FAFC`, surface `#FFFFFF`, primary `#0B5F8A`, hover/pressed `#084968`, deep `#073B57`, sky `#43A5C5` chỉ decorative, soft `#E8F4FA`, text `#17324D`, muted `#536A7A`, border `#D4E2E9`.
- Focus visible 2px `#0B5F8A` offset 2px; min interactive hit area 44×44; search controls 56px; button header 48px. Tương phản chữ chính được chọn theo WCAG AA; kiểm thử lại trong browser ở breakpoint thật.
- Tab order: brand → Trang chủ → Khóa học → Đăng nhập → Đăng ký → textbox → submit → Xem tất cả → footer brand → footer Khóa học → footer Đăng nhập → footer Đăng ký. Art, nhãn taxonomy, card và avatar không focus.
- Hover 140ms chỉ đổi màu/underline, không layout shift. `prefers-reduced-motion: reduce` tắt transition không thiết yếu. Decorative art `aria-hidden`; card cover minh họa không đọc như thông tin mới.

## Discrepancy và giới hạn

- Không có mismatch đã biết giữa bản render desktop và các type target chính của guide. Đây là thiết kế target, không xác nhận frontend/backend đã tích hợp.
- Chỉ desktop 1440×1320 được render; tablet/mobile là quy tắc triển khai cần QA tại 320px. Sample course/mentor/category không chứng minh dữ liệu production.

## Checklist nghiệm thu

- [x] Hai PNG 1440×1320 xuất từ cùng một SVG, clean khác annotated chỉ ở lớp marker.
- [x] 41 marker duy nhất, 24×24, primary fill, trắng 12px bold, viền trắng.
- [x] H1 48/58; course description 14/20; 3 artwork vector khác nhau; hero art học tập mới.
- [x] Không giá/rating/status/số học viên/category trên card; không card link/category filter.
- [x] API #05/#06, điều hướng, nullable, independent state, retry, accessibility và breakpoint đã đặc tả.
- [ ] QA thực tế tại tablet/mobile khi code ứng dụng.
