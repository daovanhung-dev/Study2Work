# SH-03 — Đặc tả thiết kế màn hình đăng ký học viên

> **Artifact status:** DESIGN TARGET / NOT IMPLEMENTED. `apps/study-client/` chưa có Study Web runtime/router cho screen này. Ảnh là visual handoff tĩnh, không chứng minh form đang chạy.

## Tóm tắt thiết kế

- **Screen:** SH-03 — Đăng ký học viên; route mục tiêu `/register`; actor Guest; luồng AC-01.
- **Canvas ảnh:** 1440×960px; vùng nội dung rộng 1120px, đặt giữa; header trắng cao 96px.
- **Art direction:** editorial, yên tĩnh, tạo cảm giác bắt đầu một hành trình; panel trái có minh họa giấy gấp riêng, form phải ưu tiên đọc nhanh và thao tác dễ.
- **Tham chiếu:** cùng Study ocean palette và brand với SH-02; artwork khác hình sách mở của SH-02.
- **Font:** Noto Sans; fallback `Arial, sans-serif`. Kích thước và line-height theo từng element bên dưới.
- **Màu:** primary `#0B5F8A`; hover `#084968`; deep `#073B57`; cyan `#43A5C5` (decorative); soft `#E8F4FA`; page `#F6FAFC`; surface `#FFFFFF`; text `#17324D`; muted `#536A7A`; border `#D4E2E9`; error `#B42318`; coral `#E98C72` (chỉ artwork).
- **Thành phần ngoài 19 target:** không có navigation phụ, consent checkbox, icon social, CAPTCHA, OTP, password confirmation, meter hoặc modal.

## Bố cục

| Vùng | Bounds | Cấu trúc |
|---|---:|---|
| Header | `0,0,1440,96` | Nền trắng, hairline dưới; Study brand link ở đầu trái. |
| Editorial panel | `160,128,520,704` | Nền gradient rất nhẹ `#EEF7FB`→`#E8F4FA`, radius 16px; artwork trên, copy ở nửa dưới. |
| Registration surface | `736,128,544,704` | Trắng, viền 1px, radius 16px, shadow mềm, padding 48px. |
| Form content | `784,176,448,582` | Eyebrow, H1, helper, ba cặp label/input, nút submit, sign-in link. |

## Bản đồ element

Mỗi marker trên `SH-03_annotated.png` tương ứng một hàng trong bảng; `SH-03_clean.png` là cùng layout không có marker. Cỡ chữ dưới đây tính bằng px, ghi `font-size/line-height/weight`.

| Element và nội dung | Bounding box | Visual, typography và màu | Semantic | Click/tap | Hover, focus, pressed | Validation, loading và responsive |
|---|---|---|---|---|---|---|
| **#1 — Study brand mark**<br>Open-page glyph | `x=160, y=30, w=38, h=38` px<br>Marker center `(146, 49)` in annotated PNG. | Ô vuông ocean 38×38px, radius 11px; glyph trang mở cân giữa.<br><br>**Font:** N/A; hình vector trắng, nét 2px<br>**Color:** see exact token values above and `PLAN.md`. | Ảnh trang trí trong brand link có accessible name ‘Study, Trang chủ’. | Click/tap mark hoặc wordmark #2 → `/` (SH-01). | Hover/pressed theo brand link; focus-visible 2px `#0B5F8A`, offset 2px. | **Validation/loading:** Không có; trạng thái link theo điều hướng.<br><br>**Responsive:** 38×38px; hit area brand link tối thiểu 44×44px, không ẩn ở mobile.<br><br>**Source:** STATIC_UI; nối nhận diện với SH-02. |
| **#2 — Study wordmark**<br>Study | `x=210, y=34, w=82, h=30` px<br>Marker center `(306, 49)` in annotated PNG. | Text thuần, không nền; đặt cùng baseline với mark #1.<br><br>**Font:** Noto Sans 23px/30px, 700, `#073B57`<br>**Color:** see exact token values above and `PLAN.md`. | Nội dung text của brand link tới SH-01. | Click/tap → `/` (SH-01). | Hover/pressed `#084968`; focus-visible 2px ring trên link cha. | **Validation/loading:** Không có.<br><br>**Responsive:** Giữ wordmark ở mọi breakpoint; không ép xuống dòng.<br><br>**Source:** STATIC_UI. |
| **#3 — Editorial eyebrow**<br>HỌC TẬP BẮT ĐẦU TỪ ĐÂY | `x=212, y=582, w=282, h=18` px<br>Marker center `(181, 591)` in annotated PNG. | Chữ hoa màu ocean; thanh nhấn cyan 3×18px ở x=194; không có nền.<br><br>**Font:** Noto Sans 13px/18px, 700, tracking 0.4px, `#0B5F8A`<br>**Color:** see exact token values above and `PLAN.md`. | Text tĩnh trong phần giới thiệu. | Không có tương tác. | Không hover/focus/pressed. | **Validation/loading:** Không áp dụng.<br><br>**Responsive:** Cho phép wrap có kiểm soát khi cột hẹp; nội dung vẫn là một eyebrow.<br><br>**Source:** STATIC_UI. |
| **#4 — Editorial heading**<br>Bắt đầu hành trình / học tập. | `x=212, y=618, w=408, h=88` px<br>Marker center `(197, 662)` in annotated PNG. | Hai dòng, căn trái; weight đậm, không hiệu ứng trang trí trên chữ.<br><br>**Font:** Noto Sans 36px/44px, 700, `#073B57`<br>**Color:** see exact token values above and `PLAN.md`. | H2 giới thiệu SH-03. | Không có tương tác. | Không hover/focus/pressed. | **Validation/loading:** Không áp dụng.<br><br>**Responsive:** Giữ thứ tự dòng trên desktop; giảm cỡ theo viewport và tránh tràn ở mobile.<br><br>**Source:** STATIC_UI. |
| **#5 — Editorial supporting copy**<br>Tạo tài khoản học viên với họ tên, email và mật khẩu. | `x=212, y=730, w=404, h=52` px<br>Marker center `(197, 754)` in annotated PNG. | Đoạn văn tối đa hai dòng, độ tương phản dịu, căn trái.<br><br>**Font:** Noto Sans 16px/26px, 400, `#536A7A`<br>**Color:** see exact token values above and `PLAN.md`. | Paragraph mô tả ngắn. | Không có tương tác. | Không hover/focus/pressed. | **Validation/loading:** Không áp dụng.<br><br>**Responsive:** Wrap tự nhiên; không ellipsis hoặc cắt câu ở 320px.<br><br>**Source:** STATIC_UI. |
| **#6 — Minh họa hành trình học tập**<br>Notebook ocean, máy bay giấy gấp và đường quỹ đạo; không chứa chữ. | `x=185, y=196, w=470, h=313` px<br>Marker center `(173, 196)` in annotated PNG. | Nhóm minh họa riêng 470×313px; notebook đóng ở thấp, các nếp giấy bay lên, chấm coral nhỏ; shadow mềm.<br><br>**Font:** N/A; artwork vector raster thành PNG trong suốt.<br>**Color:** see exact token values above and `PLAN.md`. | Nhóm decorative, `aria-hidden=true`. | Không có tương tác hoặc focus. | Không hover/pressed; không phải control. | **Validation/loading:** Không chứa email, token, số liệu hoặc claim.<br><br>**Responsive:** Giữ aspect ratio khi thu nhỏ; có thể ẩn trên mobile vì không mang nội dung thiết yếu.<br><br>**Source:** STATIC_UI artwork vector original; `learning-path-hero.svg/png`. |
| **#7 — Registration form surface**<br>Surface chứa form và các control #8–#19. | `x=736, y=128, w=544, h=704` px<br>Marker center `(1300, 139)` in annotated PNG. | Trắng `#FFFFFF`, border 1px `#D4E2E9`, radius 16px, shadow diffuse 0 20px 56px rgba(7,59,87,.075); padding 48px.<br><br>**Font:** N/A.<br>**Color:** see exact token values above and `PLAN.md`. | Form surface; click nền không kích hoạt hành động. | Submit chỉ qua button #17 hoặc Enter trong field. | Không có hover/pressed riêng; elevation không đổi khi focus field. | **Validation/loading:** Bên trong hiển thị lỗi/thông báo theo state, giữ đúng hierarchy.<br><br>**Responsive:** Desktop 544px; tablet max-width 600px; mobile full-width trong gutter 16px, padding 24px.<br><br>**Source:** STATIC_UI; vị trí form theo plan SH-03. |
| **#8 — Form eyebrow**<br>TÀI KHOẢN HỌC VIÊN | `x=784, y=176, w=250, h=18` px<br>Marker center `(760, 185)` in annotated PNG. | Chữ hoa nhỏ, màu muted; căn trái.<br><br>**Font:** Noto Sans 13px/18px, 700, tracking 0.5px, `#536A7A`<br>**Color:** see exact token values above and `PLAN.md`. | Text tĩnh định danh nhóm form. | Không có tương tác. | Không hover/focus/pressed. | **Validation/loading:** Không áp dụng.<br><br>**Responsive:** Không wrap trong chiều rộng form mobile.<br><br>**Source:** STATIC_UI. |
| **#9 — Tiêu đề form**<br>Tạo tài khoản | `x=784, y=212, w=360, h=48` px<br>Marker center `(760, 236)` in annotated PNG. | H1 căn trái, khoảng thở rõ với eyebrow và helper.<br><br>**Font:** Noto Sans 40px/48px, 700, `#073B57`<br>**Color:** see exact token values above and `PLAN.md`. | H1 duy nhất của screen. | Không có tương tác. | Không hover/focus/pressed. | **Validation/loading:** Không áp dụng.<br><br>**Responsive:** Co font khi card hẹp; tiếng Việt không clip.<br><br>**Source:** STATIC_UI. |
| **#10 — Form helper**<br>Điền thông tin để tạo tài khoản Study. | `x=784, y=272, w=432, h=26` px<br>Marker center `(760, 285)` in annotated PNG. | Một dòng hướng dẫn, không hiển thị policy chưa được source xác nhận.<br><br>**Font:** Noto Sans 16px/26px, 400, `#536A7A`<br>**Color:** see exact token values above and `PLAN.md`. | Paragraph liên kết ngữ cảnh với form. | Không có tương tác. | Không hover/focus/pressed. | **Validation/loading:** Không áp dụng.<br><br>**Responsive:** Có thể wrap thành hai dòng khi card thu hẹp.<br><br>**Source:** STATIC_UI. |
| **#11 — Nhãn họ và tên**<br>Họ và tên | `x=784, y=332, w=160, h=20` px<br>Marker center `(760, 342)` in annotated PNG. | Label thường, khoảng cách 8px tới input #12.<br><br>**Font:** Noto Sans 14px/20px, 600, `#17324D`<br>**Color:** see exact token values above and `PLAN.md`. | `label[for=full_name]`; bấm label đưa focus tới #12. | Click/tap label → focus input #12. | Màu giữ nguyên; focus thuộc input. | **Validation/loading:** Không có lỗi riêng trên label; lỗi nằm cạnh input/summary.<br><br>**Responsive:** Luôn hiện phía trên input; không dùng placeholder thay label.<br><br>**Source:** API #01 field `full_name`. |
| **#12 — Ô họ và tên**<br>Placeholder: Nhập họ và tên | `x=784, y=360, w=448, h=56` px<br>Marker center `(760, 388)` in annotated PNG. | Nền trắng, border 1px `#536A7A`, radius 8px, padding ngang 16px; không icon.<br><br>**Font:** Noto Sans 15px/24px, 400; placeholder `#536A7A`/70%; value `#17324D`<br>**Color:** see exact token values above and `PLAN.md`. | Required text input; `name=full_name`, `autocomplete=name`. | Click/type/paste/autofill; trim khoảng trắng; giới hạn 1–150 ký tự theo validator hiện hành. | Hover border `#084968`; focus 2px ring `#0B5F8A` offset 2px; invalid dùng border `#B42318` + thông báo có text. | **Validation/loading:** Empty/whitespace hoặc >150 ký tự bị từ chối theo client/server validator; error liên kết qua `aria-describedby`.<br><br>**Responsive:** Full width; cao 56px; bàn phím mobile phù hợp văn bản.<br><br>**Source:** API #01 current validator và `RegisterRequest.full_name`. |
| **#13 — Nhãn email**<br>Email | `x=784, y=436, w=120, h=20` px<br>Marker center `(760, 446)` in annotated PNG. | Label thường; khoảng cách 8px tới input #14.<br><br>**Font:** Noto Sans 14px/20px, 600, `#17324D`<br>**Color:** see exact token values above and `PLAN.md`. | `label[for=email]`; bấm label đưa focus tới #14. | Click/tap label → focus input #14. | Màu giữ nguyên; focus thuộc input. | **Validation/loading:** Không có lỗi riêng trên label.<br><br>**Responsive:** Luôn hiện phía trên input.<br><br>**Source:** API #01 field `email`. |
| **#14 — Ô email**<br>Placeholder: Nhập email của bạn | `x=784, y=464, w=448, h=56` px<br>Marker center `(760, 492)` in annotated PNG. | Nền trắng, border 1px `#536A7A`, radius 8px, padding ngang 16px; không thêm icon/claim.<br><br>**Font:** Noto Sans 15px/24px, 400; placeholder `#536A7A`/70%; value `#17324D`<br>**Color:** see exact token values above and `PLAN.md`. | Required `type=email`, `inputmode=email`, `autocomplete=email`. | Click/type/paste/autofill; gửi email sau khi trim; không tự lower-case. | Hover/focus như #12; 409 duplicate hiển thị `Email đã tồn tại.` cạnh trường; invalid border + text error. | **Validation/loading:** EmailStr format, nonblank và max 255 theo current validator; lỗi 422 map từ `meta.fieldErrors`.<br><br>**Responsive:** Full width 448×56px desktop; full-width theo card ở mobile.<br><br>**Source:** API #01 current `EmailStr`/validator; 409 `DESIGN_STATE_CONFLICT`. |
| **#15 — Nhãn mật khẩu**<br>Mật khẩu | `x=784, y=540, w=120, h=20` px<br>Marker center `(760, 550)` in annotated PNG. | Label thường; khoảng cách 8px tới input #16.<br><br>**Font:** Noto Sans 14px/20px, 600, `#17324D`<br>**Color:** see exact token values above and `PLAN.md`. | `label[for=password]`; bấm label đưa focus tới #16. | Click/tap label → focus input #16. | Màu giữ nguyên; focus thuộc input. | **Validation/loading:** Không có lỗi riêng trên label.<br><br>**Responsive:** Luôn hiện phía trên input.<br><br>**Source:** API #01 field `password`. |
| **#16 — Ô mật khẩu**<br>Placeholder: Nhập mật khẩu; giá trị được che | `x=784, y=568, w=448, h=56` px<br>Marker center `(760, 596)` in annotated PNG. | Nền trắng, border 1px `#536A7A`, radius 8px, padding ngang 16px; không icon reveal.<br><br>**Font:** Noto Sans 15px/24px, 400, `#17324D`<br>**Color:** see exact token values above and `PLAN.md`. | Required `type=password`, `autocomplete=new-password`. | Click/type/paste/autofill; chỉ gửi trong POST JSON khi submit. | Hover/focus như #12; invalid có text/error border; không strength meter. | **Validation/loading:** Current source chỉ reject blank/whitespace; không suy ra độ dài tối thiểu hoặc complexity.<br><br>**Responsive:** Full width 448×56px; giữ password-manager support và không lưu vào local storage.<br><br>**Source:** API #01 current validator. |
| **#17 — Nút tạo tài khoản**<br>Tạo tài khoản | `x=784, y=656, w=448, h=56` px<br>Marker center `(760, 684)` in annotated PNG. | Nền `#0B5F8A`, radius 8px, shadow nhẹ; full-width; label căn giữa.<br><br>**Font:** Noto Sans 16px/24px, 600, trắng<br>**Color:** see exact token values above and `PLAN.md`. | Submit button duy nhất của form. | Click/tap hoặc Enter → validate → `POST /api/v1/auth/register` với `{email,password,full_name}`, không Authorization. | Hover/pressed `#084968` trong 140ms; focus ring 2px; loading label `Đang tạo tài khoản…`, disabled để chống double submit. | **Validation/loading:** Client validation trước request; 201 handoff, 409 duplicate, 422 field errors, 500 safe message; không tự retry mutation.<br><br>**Responsive:** Full width, cao 56px (đạt hit target mobile).<br><br>**Source:** API #01 route/source; expected SH-03 flow từ inventory. |
| **#18 — Lời nhắc tài khoản hiện có**<br>Đã có tài khoản? | `x=872, y=736, w=150, h=22` px<br>Marker center `(850, 773)` in annotated PNG. | Văn bản tĩnh trong hàng footer; không có nền riêng.<br><br>**Font:** Noto Sans 15px/22px, 400, `#536A7A`<br>**Color:** see exact token values above and `PLAN.md`. | Text dẫn trước liên kết #19. | Không có tương tác. | Không hover/focus/pressed. | **Validation/loading:** Không áp dụng.<br><br>**Responsive:** Có thể wrap trên màn nhỏ; giữ liền ngữ nghĩa với link #19.<br><br>**Source:** STATIC_UI. |
| **#19 — Liên kết đăng nhập**<br>Đăng nhập | `x=1038, y=736, w=118, h=22` px<br>Marker center `(1175, 747)` in annotated PNG. | Text link gạch chân mảnh, không button fill.<br><br>**Font:** Noto Sans 15px/22px, 600, `#0B5F8A`<br>**Color:** see exact token values above and `PLAN.md`. | Anchor tới route target `/login` (SH-02). | Click/tap → SH-02. | Hover `#084968`, underline đậm hơn; focus-visible 2px ring; hit target mở rộng ≥44×44px. | **Validation/loading:** Không có.<br><br>**Responsive:** Không tách khỏi lời nhắc; wrap có kiểm soát ở card hẹp.<br><br>**Source:** SH-03 inventory; SH-02 linked screen. |

## Luồng tương tác và trạng thái

| State | Kích hoạt | Kết quả thiết kế |
|---|---|---|
| `IDLE` | Guest mở `/register` | Ảnh clean thể hiện ba trường rỗng, label rõ, button khả dụng; không có error, sample account hoặc claim email. |
| `FOCUS / TOUCHED` | Tập trung/blur field | Focus ring 2px `#0B5F8A`, offset 2px; không layout shift. Sau blur chỉ hiển thị lỗi khi dữ liệu không hợp lệ. |
| `CLIENT_VALIDATION` | Submit dữ liệu trống/sai | Họ tên trim 1–150; email trim/format/max 255; password nonblank. Gắn lỗi qua `aria-describedby`; lỗi nhiều trường có summary liên kết và focus được. |
| `SUBMITTING` | Form hợp lệ, request #01 đang chờ | Đổi label button thành `Đang tạo tài khoản…`, disable nút và chặn submit lặp; không tự retry. |
| `REGISTER_201_HANDOFF` | #01 trả HTTP 201 | Target flow chuyển SH-04 bằng `data.id`/`data.email`. Chỉ xác nhận tạo account theo response; không nói email đã gửi/verified. Cách vận chuyển state sang SH-04 còn cần quyết định. |
| `EMAIL_CONFLICT_409` | #01 trả 409 `DESIGN_STATE_CONFLICT` | Hiện `Email đã tồn tại.` ở field email và alert gọn; giữ họ tên/email, bỏ giá trị password sau response; cho phép sửa hoặc sang SH-02. |
| `VALIDATION_422` | #01 trả 422 `DESIGN_VALIDATION_ERROR` | Map `meta.fieldErrors` vào field; summary nếu nhiều field; không tự thêm chính sách mật khẩu. |
| `SERVER_500` | #01 trả `DESIGN_INTERNAL_ERROR` | Hiện câu an toàn `Không thể tạo tài khoản.`; giữ dữ liệu không nhạy cảm; không render stack/SQL/hash. |
| `NETWORK_UNKNOWN` | Không nhận HTTP response | Báo rằng chưa xác nhận hoàn tất; không retry mutation tự động; không khẳng định account được tạo. Giữ họ tên/email, không lưu password lâu dài. |

## API và screen liên quan: expected / current

| Mốc | Expected từ inventory/DD | Current source được kiểm tra | Tác động lên screen |
|---|---|---|---|
| Submit #01 | `POST /api/v1/auth/register`; body `email`, `password`, `full_name`; 201 trả `data.id`, `data.email`; 409 giữ trên form. | Public route 201; trim/validate email bằng `EmailStr`, max 255; password chỉ từ chối blank/whitespace; full_name trim 1–150; duplicate trả 409; hash Argon2id; insert role `STUDENT`; success không trả password/hash. | Form chỉ có đúng ba field; không thêm complexity/strength rules; phân biệt lỗi 409/422/500 như bảng state. |
| #01 sau commit | Inventory mô tả bước xác minh tiếp theo. | Current #01 chỉ log `verification_dispatch_pending`, không gọi API #02. Account status phụ thuộc default DB; live DB chưa được xác minh. | Giữ discrepancy; không hiển thị/promise status account. |
| SH-04 / #02 | SH-04 là screen kế tiếp trong inventory; gửi `user_id`/`email`, HTTP 202 được chấp nhận. | Provider mặc định là stub `accepted`; không gửi email thật và không tạo token/link. #02 là route độc lập, không được #01 gọi. | Link/transition tới SH-04 thuộc expected journey; tuyệt đối không ghi “email đã gửi” hoặc “đã xác minh”. SH-04 được mô tả riêng, không phải child-screen trong folder này. |
| DD status | API #01/#02 DD còn Draft — Needs Confirmation. | #01 response source không có `bio` như DD liệt kê; một số account/normalization/dispatch policy còn open. | Không đưa `bio`, token, trạng thái `ACTIVE`, hoặc claim chưa có source vào UI. |

**Expected flow:** SH-03 → API #01 → HTTP 201 và `data.id`/`data.email` → SH-04 → API #02 → accepted theo stub hiện tại; sau đó SH-02 theo journey.  
**Current implementation:** màn Study Web chưa có runtime; API #01 đăng ký và ghi log pending nhưng không gọi #02; API #02 dùng stub mặc định. Đây là discrepancy cần giữ nguyên trong handoff.

## Liên kết screen

| Nguồn | Sự kiện | Đích |
|---|---|---|
| Brand mark #1 / wordmark #2 | Click/tap | `/` — SH-01 (route mục tiêu). |
| Submit #17 khi API #01 trả 201 | Handoff theo expected AC-01 | SH-04 `/register/verification` (screen độc lập, ngoài phạm vi package này). |
| Link #19 | Click/tap | `/login` — SH-02 cho tài khoản đã có. |

## Accessibility và responsive

- Thứ tự bàn phím: brand → họ tên → email → mật khẩu → submit → đăng nhập.
- Label cố định cho mỗi field; lỗi có text, được nối `aria-describedby`; summary nhiều lỗi có thể focus và liên kết tới field.
- Body text cần đạt contrast ≥4.5:1; boundary field ≥3:1; không dùng màu làm dấu hiệu lỗi duy nhất; focus ring không bị clip.
- Hover/focus transition chỉ đổi màu/underline trong 140ms, không dịch layout; tôn trọng `prefers-reduced-motion`.
- 1440px: layout hai cột như hình. 768–1023px: panel được thu gọn hoặc ẩn để card tối đa 600px. 320–767px: gutter 16px, card full-width, padding 24px, control 56px cao, không scroll ngang; minh họa có thể ẩn.

## Quyết định còn mở

1. API #01 DD đang Draft: xác nhận account status/default, response profile, email case-normalization và policy mật khẩu trước khi biến target thành runtime.
2. Inventory yêu cầu follow-up SH-04 nhưng source #01 không gọi #02: cần product/backend quyết định owner và điểm dispatch verification.
3. Handoff `data.id`/`data.email` qua route/state tới SH-04 chưa có contract transport trong web client.
4. Không có contract đồng ý điều khoản nên screen không render consent checkbox.

## File trong gói

- `SH-03_clean.png`, `SH-03_annotated.png`: hai ảnh canvas 1440×960.
- `SH-03_clean.svg`, `SH-03_annotated.svg`: vector source; artwork PNG được embed để mở độc lập.
- `learning-path-hero.svg`, `learning-path-hero.png`: artwork riêng, PNG nền trong suốt.
- `PLAN.md`: plan source-backed cho screen; `build.py`: script dựng và đóng zip.
- `SH-03_design_handoff_v1.zip`: archive chứa đầy đủ các file trên cùng SCREEN.md.
