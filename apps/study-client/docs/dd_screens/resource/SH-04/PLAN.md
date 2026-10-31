# SH-04 — Plan thiết kế màn hình handoff xác thực email

## 1. Phạm vi và trạng thái bằng chứng

```text
primary_task_type: docs
secondary_task_types: []
project_scopes: [web-work, server-study]
cross_scope_dependencies: [SH-03 API #01 data.id/email -> SH-04 API #02 -> SH-02]
screen: SH-04, /register/verification, Guest, AC-01, API #02
artifact_status: DESIGN_TARGET / NOT_IMPLEMENTED
```

- Thiết kế đúng một page: **SH-04 — Handoff xác thực email**. Không thiết kế lại SH-03/SH-02 và không tạo child screen.
- `apps/study-client/` hiện chỉ có inventory; không có Study Web source/router/client. Route là proposed target, không tuyên bố đã chạy.
- `.agents/web-study/design.md` là visual target canonical. Giữ Study ocean palette, Noto Sans fallback đang có trong design resource liền kề, tương phản AA, 4px rhythm và trạng thái truy cập được.
- Ảnh chính là trạng thái `202 accepted` hiện hành của default stub. Nội dung phải tách nghĩa **request accepted** khỏi **email delivery**; không dùng check xanh, “email đã gửi”, “hãy kiểm tra hộp thư”, token, OTP, verification link hay “đã xác minh”.
- SH-05/SH-06 là state view riêng; không dùng chúng làm child screen của SH-04.

## 2. Luồng, API và discrepancy

### Expected behavior

1. SH-03 thành công từ API #01 `POST /api/v1/auth/register`, lấy `data.id` và `data.email`.
2. SH-04 gọi API #02 `POST /api/v1/auth/verify-email/send` với body `{user_id, email}`.
3. HTTP `202 DESIGN_OPERATION_ACCEPTED` chỉ xác nhận provider chấp nhận request theo contract hiện tại. Điều hướng được liệt kê tiếp theo tới SH-02 (`/login`).

### Current source

| Source | Bằng chứng hiện hành | Quyết định thiết kế |
|---|---|---|
| API catalog #02 | Public/no Bearer; request `user_id:int64`, `email`; `202` `ApiEnvelope<ActionResult>` với `status` và optional `reason`; 422/500. | Chỉ dùng đúng tên field/status/code; không tự thêm `operation_id`, poll, retry hoặc response field. |
| API #02 route/model/validator/view | Route public, không resolve DB; strict raw JSON integer cho `user_id`; normalize/validate `email`; gọi provider đồng bộ. Provider exception → HTTP 500 `DESIGN_INTERNAL_ERROR`, message an toàn. | Không có màn hình nhập lại email, user ID hay mật khẩu trên SH-04; request là target handoff từ SH-03. Lỗi được hiển thị bằng state, không lộ detail provider. |
| Default provider | `StubVerificationEmailProvider` trả `status="accepted"`; không gửi email thật, không tạo token/link; không DB mutation. | Nội dung: yêu cầu được tiếp nhận, trạng thái email chưa được xác nhận là đã gửi. Dùng neutral ocean color, không dùng success-green/checkmark mang nghĩa đã xác minh. |
| API #01 connection | Current #01 chỉ log `verification_dispatch_pending`; không gọi #02. | Expected screen sequence không được mô tả như runtime đã wired. |
| Confirmation / resend | Không có OTP/link confirmation API; không có retry worker, rate-limit/idempotency hoặc resend policy được xác nhận; các điểm này nằm trong `OPEN_QUESTIONS.md`. | Không thêm OTP/link, nút resend hoặc lời khuyên vào spam/promotions. Không tự retry POST. |
| Handoff transport | Expected #02 cần `user_id/email`; hiện chưa có Study Web router/storage/transport contract. | Không đưa PII vào URL/query string và không đoán persistence. Mô tả transport là open decision. |

### Source trace

```text
Expected: SH-03 #01 201 data.id/email -> SH-04 #02 POST user_id/email -> 202 accepted -> SH-02
Current: Study Web absent; #01 does not call #02; direct public #02 -> validation -> provider.dispatch -> default stub accepted -> 202; no delivery, token, link, DB write or verification endpoint
```

## 3. Art direction và bố cục — revision 2 sau phản hồi thẩm mỹ

- **Visual thesis:** “Một biên nhận rõ ràng, không phóng đại kết quả.” Đây là màn hình dịch vụ sau đăng ký; trạng thái phải được quét trong vài giây, CTA đăng nhập luôn nổi bật, hình minh họa chỉ neo cảm giác có một yêu cầu đang được ghi nhận.
- **Design mode:** transactional service, light-first, theo chuẩn Study Web. Cá tính đến từ typography có nhịp, minh họa vector riêng và một lớp status được phân nhóm gọn; không biến trang thành landing page hoặc dashboard.
- **Canvas/grid:** giữ canvas 1440×960px, header trắng cao 96px, content centered 1120px; hai cột tại `(160,176,520,608)` và `(736,176,544,608)`. Giữ 56px gutter để hai vùng thở đều và không đổi thứ tự đọc.
- **Auth continuity:** dùng cùng Study mark, Noto Sans và palette đã duyệt như SH-02/03. Giữ radius 16px, viền mảnh và một bóng ambient thấp. Không thêm nav, progress step, badge kỹ thuật, số HTTP hoặc nội dung không có trong inventory.
- **Editorial panel:** một mảng ocean-deep `#073B57` có viền primary `#0B5F8A`, chữ trắng và copy `#E8F4FA`; đây là một dark accent duy nhất trên canvas light-first. Artwork riêng tại `(185,220,470,270)` vẽ lại thành “request folio” có tờ giấy lớn, silhouette rõ, nét ocean đậm hơn, chi tiết giấy/metadata trừu tượng và vòng hình học thưa. Tăng tỷ lệ chủ thể trong vùng tranh, phân biệt rõ khỏi nền, giữ nhiều khoảng trống. Chỉ dùng `#073B57`, `#0B5F8A`, `#43A5C5`, `#D4E2E9`, `#E8F4FA`, `#FFFFFF`; không phong bì, máy bay giấy, checkmark, text giả, logo giả, dữ liệu cá nhân hoặc watermark. Copy ở nửa dưới giữ ba tầng: eyebrow trắng, H2 trắng, body `#E8F4FA`; thanh accent `#43A5C5` chỉ để trang trí.
- **Status card:** white, viền `#D4E2E9`, radius 16px, bóng ambient thấp, padding 48px. Tạo nhịp rõ theo 3 cụm: eyebrow/H1/helper; status summary hai hàng với divider; CTA. Bỏ cảm giác card trống bằng cách cân lại khoảng cách theo chiều dọc, không thêm nội dung. Summary vẫn tách request acceptance khỏi email delivery; icon line-art không mang nghĩa verified. CTA dùng fill phẳng `#0B5F8A`, không gradient, tương phản cao và full-width.
- **Typography:** `Noto Sans, Arial, sans-serif`; H1 40/48/700, H2 36/44/700, body 16/26/400, label 14–15/20–22/600, status 14/20/600. Giữ câu ngắn, không all-caps dài, không đổi wording trạng thái thành delivery claim.
- **Palette:** chỉ dùng token Study: `#0B5F8A` primary/link; `#084968` hover/pressed; `#073B57` heading; `#43A5C5` decorative only; `#E8F4FA` informational surface và soft copy trên dark panel; `#F6FAFC` page; `#FFFFFF` card; `#17324D` primary text; `#536A7A` secondary text; `#D4E2E9` boundary; `#B42318` paired error only. Không dùng success green cho `accepted`, không thêm coral hoặc màu ngoài token.
- **No extra functionality:** không checkbox, password field, email edit, confirmation code/link, resend, support chat, external inbox button, timer, HTTP badge hoặc operation polling.
- **Quality gates:** bản clean giữ đúng 17 element; bản annotated có đúng 17 marker không che nội dung; copy/API boundary không đổi; render desktop và xem lại ảnh ở kích thước gốc; kiểm tra clipping, contrast, khoảng cách, thứ tự đọc và độ chính xác từng số marker trước khi đóng ZIP.

## 4. Element map (17 targets)

Bounding boxes là pixel trên canvas 1440×960. Các marker được đặt ở khoảng trống cạnh target, không phủ chữ/icon/control.

| # | Element / nội dung | Box `x,y,w,h` | Style | Semantics / event | Hover, focus, state, responsive |
|---:|---|---:|---|---|---|
| 1 | Study brand mark | `160,30,38,38` | Ocean square radius 11px, glyph trang mở trắng nét 2px. | Ảnh trang trí trong brand link “Study, Trang chủ”; click/tap → SH-01 `/`. | Focus ring ở link cha; hit area ≥44px; giữ ở mobile. |
| 2 | Wordmark `Study` | `210,34,82,30` | Noto Sans 23/30/700 `#073B57`. | Text của brand link; click/tap → SH-01. | Hover/pressed `#084968`; focus-visible 2px `#0B5F8A`; không wrap. |
| 3 | Editorial eyebrow `STUDY · XÁC THỰC EMAIL` | `212,536,300,18` | 13/18/700, tracking 0.4px, `#FFFFFF`; thanh nhấn 3×18px. | Text tĩnh. | Co/wrap có kiểm soát; decorative color không mang status. |
| 4 | Editorial heading `Rõ ràng ở / từng bước.` | `212,572,408,88` | Noto Sans 36/44/700 `#FFFFFF`; hai dòng. | H2, tĩnh. | Giảm font theo viewport, không tràn 320px. |
| 5 | Editorial copy `Mỗi bước chỉ phản ánh điều hệ thống đã xác nhận.` | `212,696,404,52` | Noto Sans 16/26/400 `#E8F4FA`; tối đa hai dòng. | Paragraph, tĩnh. | Wrap tự nhiên, không cắt câu. |
| 6 | Request-receipt artwork | `185,220,470,270` | Request folio vector có paper layer rõ, nét ocean, vòng hình học thưa và metadata trừu tượng. | Decorative group `aria-hidden=true`; không click/focus. | Giữ tỷ lệ khi thu nhỏ; có thể ẩn ở mobile. |
| 7 | Status card surface | `736,176,544,608` | White, border `#D4E2E9`, 16px radius, low shadow, padding 48px. | Page surface; click nền không action. | Surface không hover; tablet max-width 600px; mobile full-width gutter 16px. |
| 8 | Card eyebrow `TRẠNG THÁI YÊU CẦU` | `784,224,270,18` | Noto Sans 13/18/700, tracking 0.5px, `#536A7A`. | Text tĩnh. | Không wrap ở card mobile. |
| 9 | H1 `Trạng thái yêu cầu` | `784,260,448,48` | Noto Sans 40/48/700 `#073B57`. | H1 duy nhất. | Co theo viewport; không clip dấu tiếng Việt. |
| 10 | Helper `Yêu cầu đã được tiếp nhận.` | `784,320,448,26` | Noto Sans 16/26/400 `#536A7A`. | Paragraph. | Một/two lines theo chiều rộng; không claim email delivery. |
| 11 | Status summary surface | `784,400,448,152` | `#F6FAFC`, border 1px `#D4E2E9`, radius 12px; hairline divider. | Group tĩnh; expose `aria-label="Trạng thái yêu cầu và gửi email"`. | Không hover/focus. Reflow hai hàng thành stacked trên narrow card. |
| 12 | Request status icon | `808,416,28,32` | Outline tray/receipt icon 1.8px `#0B5F8A`; no checkmark. | Decorative icon cạnh trạng thái; text status vẫn có. | Không focus/click; giữ contrast ≥3:1. |
| 13 | Request label `Yêu cầu` | `852,428,110,22` | Noto Sans 15/22/600 `#17324D`. | Static status label. | Không hover/focus. |
| 14 | Accepted status `Đã tiếp nhận` | `1096,422,112,28` | Pill nền `#E8F4FA`; text `#0B5F8A`, 13/20/600; no green. | Text status từ `data.status="accepted"`. | Không interactive. Mobile wrap/left-align nếu thiếu chỗ. |
| 15 | Email label `Gửi email` | `808,492,120,22` | Noto Sans 15/22/600 `#17324D`. | Static status label. | Không hover/focus. |
| 16 | Delivery state `Chưa xác nhận đã gửi` | `1000,492,208,22` | Noto Sans 14/20/600 `#536A7A`, căn phải. | Static derived disclosure: current response không xác nhận email delivery. | Không success/error color; wrap/stack trên mobile; không suy từ `accepted` thành sent. |
| 17 | CTA `Đến trang đăng nhập` | `784,636,448,56` | Button-link ocean fill `#0B5F8A`, white 16/24/600, radius 10px. | Link route `/login` → SH-02; dùng `<a>`, không mutation. | Hover/pressed `#084968` 140ms; focus-visible 2px ring; hit target 56px; không nói login chắc chắn thành công. |

## 5. State và logic screen

| State | Trigger | Hiển thị / hành vi |
|---|---|---|
| `HANDOFF_LOADING` | Expected navigation từ SH-03 có `user_id/email`, trước response #02 | Announce “Đang tiếp nhận yêu cầu…” qua polite status; chỉ gửi một request và chặn submit lặp. CTA #17 vẫn là link điều hướng, không khóa khi request #02 đang chờ; không hiển thị email/PII trong URL. |
| `ACCEPTED_STUB` | #02 HTTP 202 `DESIGN_OPERATION_ACCEPTED`, `data.status=accepted` | Đây là ảnh main state: row request “Đã tiếp nhận”; row email “Chưa xác nhận đã gửi”; không tự retry/poll. |
| `UNMAPPED_PROVIDER_STATUS` | #02 trả 202 nhưng `data.status` ngoài giá trị UI đã ánh xạ | Giữ trạng thái neutral “Trạng thái chưa được xác định”; không render raw provider reason hoặc suy ra delivery. |
| `INVALID_HANDOFF` | Không có context hoặc #02 trả 422 `DESIGN_VALIDATION_ERROR` | Không gửi lại tự động; thông báo “Không thể xử lý thông tin đăng ký. Hãy quay lại bước đăng ký.”; CTA #17 đổi nhãn/đích về SH-03 chỉ trong state này; map `meta.fieldErrors` nội bộ, không đưa user_id ra UI. |
| `DISPATCH_ERROR` | #02 trả 500 `DESIGN_INTERNAL_ERROR` hoặc network không có response | Copy an toàn: “Chưa thể tiếp nhận yêu cầu lúc này.”; không nói email gửi thất bại nếu chưa biết provider outcome; giữ no-auto-retry policy; CTA SH-02 vẫn là route được inventory nêu. |
| `NO_DELIVERY_CONFIRMATION` | Current default provider accepted mà không gửi thư | Giữ callout rõ “Chưa xác nhận đã gửi”; không gợi ý kiểm tra inbox/spam; không show resend. |

### Navigation và constraints

- CTA #17 → SH-02 `/login` theo inventory.
- Chỉ state `INVALID_HANDOFF` có thể cung cấp recovery về SH-03 `/register` để bổ sung context hợp lệ; đây không phải child screen.
- Không có child route/modal trong SH-04. OTP/link verification và verified-success state không tồn tại trong API catalog/source.
- Không auto-redirect sau 202; người dùng cần nhìn thấy trạng thái được chấp nhận. 202 không có `operation_id`, vì vậy không poll API #18.
- Không thêm resend cho tới khi provider, abuse control, idempotency và retry policy có contract.

## 6. Accessibility / responsive

- Tab order: brand → primary CTA. Static status uses semantic region + `role=status` after response; no focus steal. H1 order/label unique.
- Status có text riêng cho acceptance và delivery; không dùng màu/check/icon làm status duy nhất; status announcement không lặp hoặc thay layout.
- Body contrast ≥4.5:1; boundaries ≥3:1; visible focus không clip; motion feedback 140ms, tắt nonessential motion theo `prefers-reduced-motion`.
- Desktop 1440px: 520px panel + 56px gutter + 544px card.
- Tablet 768–1023px: status content centered, art/panel có thể collapse; card max-width 600px.
- Mobile 320–767px: card full width, gutter 16px, padding 24px; status matrix stack thành cặp label/value, button ≥56px; không scroll ngang; art có thể ẩn.

## 7. Open decisions

1. API #02 DD vẫn `Draft — Needs Confirmation`: status/reason enum, acceptance boundary và provider thật chưa được duyệt.
2. API #01 không gọi #02; caller/feature gate/ownership của dispatch chưa chốt.
3. Route-state transport cho `user_id/email`, bảo vệ PII và hành vi khi refresh/deep-link chưa có Study Web contract.
4. Không có API confirm OTP/link; không thể đưa verification completion vào screen.
5. Public abuse control, ownership check, resend/rate-limit/idempotency còn open; UI không tạo các hành vi đó.

## 8. Quality gate trước khi đóng gói

- [ ] Có clean/annotated PNG chính xác 1440×960, source SVG độc lập và artwork PNG trong suốt.
- [ ] Annotated có đúng 17 marker #1–#17; không marker nào phủ text/status/control.
- [ ] SCREEN.md có đúng 17 hàng; bounding boxes, marker centers, typography, color, event/state/responsive khớp ảnh/plan.
- [ ] Main screen thể hiện `accepted` nhưng không khẳng định email sent/delivered/verified; không check xanh, OTP/link, resend hoặc sample email/user.
- [ ] API 202/422/500 và discrepancy #01→#02 match current source; no invented polling/retry/operation.
- [ ] ZIP integrity/member content được kiểm tra; clean/annotated/artwork được mở xem ở full resolution và lỗi được sửa trước khi bàn giao.
