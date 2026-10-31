# SH-04 — Đặc tả thiết kế màn hình handoff xác thực email

> **Status:** `DESIGN_TARGET / NOT_IMPLEMENTED`. Study Web runtime/router chưa có trong checkout. Screenshot là design artifact, không chứng minh form/route/API client đang chạy.

## Tóm tắt

- **Screen:** SH-04 — Handoff xác thực email; route mục tiêu `/register/verification`; actor Guest; AC-01; API #02.
- **Canvas:** 1440×960px; header trắng cao 96px; content max-width 1120px; auth shell chia 520px + 56px + 544px.
- **Purpose:** Hiển thị riêng hai sự thật: request được provider chấp nhận và trạng thái gửi email chưa được xác nhận. Không gọi request acceptance là email delivery hoặc verified.
- **Style:** Study ocean palette; panel trái là một dark accent `#073B57`, card phải giữ light surface. Request folio riêng, không dùng phong bì/checkmark.
- **Font:** Noto Sans với fallback `Arial, sans-serif`, đã có trong design assets; không nạp font mạng.
- **Không thuộc screen:** OTP/link confirm, resend, inbox navigation, CAPTCHA, profile info, email address, token, operation polling, email verification success.

## Bố cục và tokens

| Vùng | Bounds | Thông số |
|---|---:|---|
| Header | `0,0,1440,96` | Nền `#FFFFFF`, hairline `#D4E2E9`; brand anchor trái. |
| Editorial panel | `160,176,520,608` | Ocean-deep `#073B57`, viền `#0B5F8A`, radius 16px; artwork sáng ở trên, copy trắng cuối panel. |
| Status surface | `736,176,544,608` | `#FFFFFF`, border `#D4E2E9`, radius 16px, diffuse shadow, padding 48px. |
| Status summary | `784,400,448,152` | Nền `#F6FAFC`, border `#D4E2E9`, radius 12px; hai hàng, không shadow. |
| Primary action | `784,636,448,56` | Link đến SH-02, primary ocean. |

Tokens: primary `#0B5F8A`; hover/pressed `#084968`; heading `#073B57`; accent `#43A5C5` (decorative only); soft `#E8F4FA`; page `#F6FAFC`; surface `#FFFFFF`; text `#17324D`; muted `#536A7A`; border `#D4E2E9`; error `#B42318`. Accepted không dùng success-green.

## Bản đồ element và hành vi

Mỗi marker trong `SH-04_annotated.png` khớp đúng một hàng. `SH-04_clean.png` giữ cùng screen, bỏ riêng lớp marker. Cỡ chữ ghi `font-size/line-height/weight` px.

| Element / nội dung | Bounds + marker | Visual, typography, màu | Semantic | Click/tap | Hover/focus/pressed/state | Validation/loading/responsive/source |
|---|---|---|---|---|---|---|
| **#1 — Study brand mark**<br>Glyph trang mở trong brand link. | `x=160, y=30, w=38, h=38` px<br>Marker center `(146, 49)`. | Ô ocean 38×38px, radius 11px; glyph trang mở cân giữa.<br><br>**Font:** N/A; vector trắng, stroke 1.8px | Ảnh trang trí trong anchor có accessible name ‘Study, Trang chủ’. | Click/tap link → `/` (SH-01). | Hover/pressed theo anchor; focus-visible ring 2px `#0B5F8A`, offset 2px. | **Validation/loading:** Không có.<br><br>**Responsive:** Giữ 38×38px; hit area của link ≥44×44px ở mọi breakpoint.<br><br>**Source:** STATIC_UI; shared auth brand SH-02/03. |
| **#2 — Study wordmark**<br>Study | `x=210, y=34, w=82, h=30` px<br>Marker center `(306, 49)`. | Text thuần bên phải mark; không nền/border.<br><br>**Font:** Noto Sans 23/30/700 `#073B57` | Nội dung anchor brand link tới SH-01. | Click/tap → `/` (SH-01). | Hover/pressed `#084968`; focus-visible 2px ring ở anchor. | **Validation/loading:** Không có.<br><br>**Responsive:** Không ẩn/không wrap ở mobile.<br><br>**Source:** STATIC_UI; style khớp SH-02/03. |
| **#3 — Editorial eyebrow**<br>STUDY · XÁC THỰC EMAIL | `x=212, y=536, w=300, h=18` px<br>Marker center `(181, 545)`. | Chữ hoa vừa phải; accent bar cyan 3×18px ở x=194.<br><br>**Font:** Noto Sans 13/18/700; tracking .4px; `#FFFFFF` | Text tĩnh, không tương tác. | Không có. | Không hover/focus/pressed. | **Validation/loading:** Không áp dụng.<br><br>**Responsive:** Wrap có kiểm soát trong cột hẹp; không làm mất nội dung.<br><br>**Source:** STATIC_UI. |
| **#4 — Editorial heading**<br>Rõ ràng ở / từng trạng thái. | `x=212, y=572, w=408, h=88` px<br>Marker center `(197, 616)`. | H2 hai dòng, căn trái, không effect trên chữ.<br><br>**Font:** Noto Sans 36/44/700 `#FFFFFF` | H2 mô tả nguyên tắc hiển thị state. | Không có. | Không hover/focus/pressed. | **Validation/loading:** Không áp dụng.<br><br>**Responsive:** Giảm font theo viewport; không tràn 320px.<br><br>**Source:** STATIC_UI. |
| **#5 — Editorial supporting copy**<br>Mỗi bước chỉ phản ánh điều hệ thống đã xác nhận. | `x=212, y=696, w=404, h=52` px<br>Marker center `(197, 722)`. | Hai dòng gọn, line-height 26px, căn trái.<br><br>**Font:** Noto Sans 16/26/400 `#E8F4FA` | Paragraph tĩnh. | Không có. | Không hover/focus/pressed. | **Validation/loading:** Không áp dụng.<br><br>**Responsive:** Wrap tự nhiên, không ellipsis/crop.<br><br>**Source:** STATIC_UI. |
| **#6 — Request-receipt artwork**<br>Request folio dạng giấy với silhouette rõ, các dòng metadata trừu tượng và vòng hình học thưa; không có chữ. | `x=185, y=220, w=470, h=270` px<br>Marker center `(173, 220)`. | Artwork Study ocean-blue tương phản rõ, paper layer có depth nhẹ; chỉ dùng token palette, không phong bì/checkmark.<br><br>**Font:** N/A; vector source, PNG alpha trong suốt. | Decorative group `aria-hidden=true`. | Không click/focus. | Không có hover/pressed. | **Validation/loading:** Không có nội dung delivery/verification hoặc dữ liệu người dùng.<br><br>**Responsive:** Giữ aspect ratio; có thể ẩn ở mobile.<br><br>**Source:** Original vector asset `request-status-hero.svg/png`. |
| **#7 — Status card surface**<br>Surface của page SH-04. | `x=736, y=176, w=544, h=608` px<br>Marker center `(1300, 187)`. | Surface trắng; border 1px `#D4E2E9`; radius 16px; shadow 0 18px 48px rgba(7,59,87,.07); padding 48px.<br><br>**Font:** N/A. | Page surface; click nền không action. | Không có event riêng. | Không hover/focus/pressed; không elevation shift. | **Validation/loading:** Chứa trạng thái response API #02, không thêm form.<br><br>**Responsive:** Desktop 544px; tablet max-width 600px; mobile full width trong gutter 16px, padding 24px.<br><br>**Source:** STATIC_UI; auth family SH-02/03. |
| **#8 — Card eyebrow**<br>TRẠNG THÁI YÊU CẦU | `x=784, y=224, w=270, h=18` px<br>Marker center `(760, 233)`. | Small uppercase label, căn trái.<br><br>**Font:** Noto Sans 13/18/700; tracking .5px; `#536A7A` | Text tĩnh định danh vùng. | Không có. | Không hover/focus/pressed. | **Validation/loading:** Không áp dụng.<br><br>**Responsive:** Không wrap tại chiều rộng mobile card.<br><br>**Source:** STATIC_UI. |
| **#9 — H1 `Trạng thái yêu cầu`**<br>Trạng thái yêu cầu | `x=784, y=260, w=448, h=48` px<br>Marker center `(760, 284)`. | Heading một dòng, hierarchy chính.<br><br>**Font:** Noto Sans 40/48/700 `#073B57` | H1 duy nhất của page. | Không có. | Không hover/focus/pressed. | **Validation/loading:** Không áp dụng.<br><br>**Responsive:** Co font khi hẹp; dấu tiếng Việt không clip.<br><br>**Source:** STATIC_UI. |
| **#10 — Helper**<br>Yêu cầu đã được tiếp nhận. | `x=784, y=320, w=448, h=26` px<br>Marker center `(760, 333)`. | Một dòng ngắn dưới H1.<br><br>**Font:** Noto Sans 16/26/400 `#536A7A` | Paragraph trạng thái. | Không có. | Sau response dùng `role=status`, `aria-live=polite`, `aria-atomic=true`; không cướp focus. | **Validation/loading:** Chỉ render như `accepted` sau HTTP 202; không biến thành delivery claim.<br><br>**Responsive:** Wrap theo card nếu cần.<br><br>**Source:** API #02 message `Yêu cầu gửi email xác thực đã được chấp nhận.`; rút gọn UI, status từ data. |
| **#11 — Status summary surface**<br>Nhóm hai hàng status và hairline divider. | `x=784, y=400, w=448, h=152` px<br>Marker center `(1300, 410)`. | Nền `#F6FAFC`, border `#D4E2E9` 1px, radius 12px; không shadow.<br><br>**Font:** N/A. | Status group có accessible label `Trạng thái yêu cầu và gửi email`. | Không tương tác. | Không hover/focus/pressed; thay nội dung theo response state. | **Validation/loading:** Hai kết quả độc lập: request accepted và email delivery chưa xác nhận.<br><br>**Responsive:** Giữ hai cặp label/value; stack label trên value ở 320px.<br><br>**Source:** API #02 `data.status`; current provider không trả delivery status. |
| **#12 — Request status icon**<br>Outline glyph phiếu nhận yêu cầu. | `x=808, y=416, w=28, h=32` px<br>Marker center `(760, 434)`. | Biểu tượng folder/tray mở, không checkmark, 28×32px.<br><br>**Font:** N/A; 1.8px vector stroke `#0B5F8A`. | Decorative cạnh label status; không thay text. | Không click/focus. | Không có. | **Validation/loading:** Không encode delivery success.<br><br>**Responsive:** Giữ 28×32px hoặc ẩn nếu layout xếp chồng.<br><br>**Source:** STATIC_UI. |
| **#13 — Request label `Yêu cầu`**<br>Yêu cầu | `x=852, y=428, w=110, h=22` px<br>Marker center `(760, 466)`. | Label căn trái trong hàng thứ nhất.<br><br>**Font:** Noto Sans 15/22/600 `#17324D` | Static status label. | Không có. | Không hover/focus/pressed. | **Validation/loading:** Không áp dụng.<br><br>**Responsive:** Stack trên value; không truncate.<br><br>**Source:** STATIC_UI. |
| **#14 — Accepted badge `Đã tiếp nhận`**<br>Đã tiếp nhận | `x=1096, y=422, w=112, h=28` px<br>Marker center `(1248, 436)`. | Pill ocean-soft, không dùng success-green.<br><br>**Font:** Noto Sans 13/20/600 `#0B5F8A` | Text status lấy từ `data.status=accepted`. | Không tương tác. | Không hover/focus/pressed. | **Validation/loading:** Chỉ xuất hiện khi response 202 có status accepted.<br><br>**Responsive:** Có thể left-align trong stacked layout.<br><br>**Source:** API #02 response, default provider source. |
| **#15 — Email label `Gửi email`**<br>Gửi email | `x=808, y=492, w=120, h=22` px<br>Marker center `(760, 503)`. | Label căn trái ở hàng thứ hai.<br><br>**Font:** Noto Sans 15/22/600 `#17324D` | Static status label. | Không có. | Không hover/focus/pressed. | **Validation/loading:** Không áp dụng.<br><br>**Responsive:** Stack trên value; không truncate.<br><br>**Source:** STATIC_UI. |
| **#16 — Email state `Chưa xác nhận đã gửi`**<br>Chưa xác nhận đã gửi | `x=1000, y=492, w=208, h=22` px<br>Marker center `(1248, 503)`. | Text muted căn phải; không dùng warning/error color.<br><br>**Font:** Noto Sans 14/20/600 `#536A7A` | Explanatory value: response không xác nhận delivery. | Không có. | Không hover/focus/pressed. | **Validation/loading:** Không suy `status=accepted` thành email sent.<br><br>**Responsive:** Stack dưới label, căn trái khi hẹp.<br><br>**Source:** Current provider/view; no delivery field in ActionResult. |
| **#17 — CTA `Đến trang đăng nhập`**<br>Đến trang đăng nhập | `x=784, y=636, w=448, h=56` px<br>Marker center `(760, 664)`. | Ocean fill phẳng `#0B5F8A`, radius 10px, shadow nhẹ, full-width.<br><br>**Font:** Noto Sans 16/24/600, trắng. | Anchor styled as primary button → `/login` (SH-02). | Click/tap → SH-02 ở accepted state; `INVALID_HANDOFF` dùng cùng CTA #17 để quay về `/register`; không tạo API call. | Hover/pressed `#084968` trong 140ms; focus-visible 2px ring; navigation luôn dùng link, không loading/disabled. | **Validation/loading:** Không khẳng định đăng nhập chắc chắn thành công; API #03 status/account gate còn là dependency.<br><br>**Responsive:** Full width; cao 56px, hit target đạt yêu cầu.<br><br>**Source:** SH-04 inventory navigation; SH-02 target route. |

## Expected flow và current source

| Hạng mục | Expected từ inventory/catalog | Current source được đọc | Thiết kế giữ đúng ranh giới |
|---|---|---|---|
| Choreography | SH-03 gọi #01; lấy `data.id`/`data.email`; SH-04 gửi body `{user_id,email}` đến #02; sau 202 liên kết SH-02. | #01 hiện chỉ log `verification_dispatch_pending`; không gọi #02. API #02 route public, không Bearer, không DB; gọi provider đồng bộ. | Link đến SH-02 là target điều hướng; không nói transition đã chạy/wired. Handoff identity transport còn open. |
| HTTP 202 | `DESIGN_OPERATION_ACCEPTED`, `ActionResult.status`/optional `reason`. | View ánh xạ `status`, optional `reason`; default stub trả `accepted`. | Hàng `Yêu cầu` phản ánh status `accepted`; không thêm operation id, poll hay retry. |
| Email delivery | API mục tiêu gửi mã/link nếu verification được bật; F01 nhắc accepted không chứng minh sent/verified. | Stub hiện không gửi email, không tạo token/link; response không có delivery field. | Hàng `Gửi email` ghi `Chưa xác nhận đã gửi`; không chỉ dẫn inbox/spam hoặc dùng success-green. |
| Errors | API #02 422 validation, 500 provider failure. | 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR`/safe message; provider raw details không trả ra. | `SCREEN.md` mô tả error state an toàn; không thêm resend/auto retry. |
| Confirm/resend | Catalog không có endpoint xác nhận OTP/link. | Không có token lifecycle, verification endpoint, retry worker/rate-limit contract. | Không thiết kế OTP/link/resend/verified state; ghi open decisions. |
| Runtime | Page `/register/verification`, Guest, AC-01, trạng thái accepted/stub/no-delivery/error. | `apps/study-client/` không có Study Web runtime/router. API #02 DD `Draft — Needs Confirmation`. | Toàn bộ route/UI là `DESIGN_TARGET / NOT_IMPLEMENTED`. |

### State matrix

| State | Trigger | Hành vi |
|---|---|---|
| `HANDOFF_LOADING` | Có `user_id/email`, request #02 đang chờ | Announce polite status, chỉ gửi một request; CTA #17 vẫn là link navigation, không khóa khi dispatch đang chờ; không hiển thị PII trong URL, không gửi duplicate. |
| `ACCEPTED_STUB` | HTTP 202, `data.status=accepted` | State trong ảnh chính; request `Đã tiếp nhận`, email `Chưa xác nhận đã gửi`; không auto retry/poll. |
| `UNMAPPED_PROVIDER_STATUS` | HTTP 202 có `status` ngoài tập UI được duyệt | Hiện trạng thái trung tính “Trạng thái chưa được xác định”; không render raw `reason` hoặc suy ra delivery. |
| `INVALID_HANDOFF` | Thiếu context hoặc 422 | Không call lại; message an toàn; CTA #17 đổi nhãn/đích về SH-03 chỉ trong state này. |
| `DISPATCH_ERROR` | 500 hoặc không có response | “Chưa thể tiếp nhận yêu cầu lúc này.”; không suy đoán delivery outcome; không auto retry. |
| `NO_DELIVERY_CONFIRMATION` | Default stub accepted, không gửi thư | Giữ status email rõ ràng; không gợi ý kiểm tra inbox/spam; không resend. |

## Navigation và screen liên quan

| Element/state | Sự kiện | Đích |
|---|---|---|
| Brand #1/#2 | Click/tap | SH-01 `/`. |
| CTA #17 | Click/tap | SH-02 `/login` theo inventory. Link này không khẳng định account đã được verify hoặc login thành công. |
| CTA #17 trong `INVALID_HANDOFF` | Click/tap | Đổi nhãn thành `Quay lại đăng ký` và về SH-03 `/register`; dùng lại cùng control slot, không phải child screen. |

SH-04 không có child page/modal. SH-05/SH-06 là state view độc lập. API #18 không được gọi vì #02 không trả `operation_id`.

## Accessibility và responsive

- H1 duy nhất; tab order: brand → CTA. Static screen không trap focus.
- Sau API response, cập nhật một `role=status`, `aria-live=polite`, `aria-atomic=true`, không tự chuyển focus. Status group có accessible label và text riêng cho acceptance/delivery.
- Không dựa vào màu/icon để biểu thị status. Không dùng checkmark xanh vì có thể bị hiểu là email verified.
- Normal text ≥4.5:1; boundary ≥3:1; focus ring ≥2px và không clip; controls ≥44px; CTA 56px.
- 1440px: hai cột 520/56/544. 768–1023px: card max-width 600px; panel có thể thu/ẩn. 320–767px: gutter 16px, card padding 24px; status cặp label/value stack; CTA full-width 56px; art ẩn được; không horizontal scroll. Tôn trọng `prefers-reduced-motion`.

## Open decisions / giới hạn

1. API #02 DD còn Draft; provider thật, acceptance boundary và `status/reason` enum chưa được xác nhận.
2. API #01 không gọi #02; caller, feature gate và lỗi dispatch sau commit chưa được quyết.
3. User-email handoff/PII transport qua route và direct-entry behavior chưa có Study Web contract.
4. Verification token/link/expiry/confirmation, resend/idempotency/rate limit/abuse-control chưa có source/contract.
5. API #03 có account-status gate; CTA route tới SH-02 không hứa đăng nhập thành công.

## Asset package

- `SH-04_clean.png`, `SH-04_annotated.png` — 1440×960.
- `SH-04_clean.svg`, `SH-04_annotated.svg` — editable vector source; artwork PNG embed bên trong.
- `request-status-hero.svg`, `request-status-hero.png` — original transparent request-receipt artwork.
- `PLAN.md`, `SCREEN.md`, `build.py`, `SH-04_design_handoff_v2.zip`.
