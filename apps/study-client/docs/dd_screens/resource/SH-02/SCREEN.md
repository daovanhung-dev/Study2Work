# SH-02 — Đăng nhập Study

**Trạng thái:** `DESIGN_TARGET / NOT_IMPLEMENTED` · **Route:** `/login` (đề xuất) · **Actor:** Guest · **AC-02** · **Priority:** P0.

## Phạm vi và ranh giới bằng chứng

Đây là design handoff, không phải UI đã implement. Checkout hiện không có Study Web source, router hay auth client. Screen catalog chỉ là baseline thiết kế. Ảnh chính hiển thị trạng thái idle, không có lỗi và không điền email/mật khẩu mẫu. Không có modal, drawer, screen con hoặc auth provider ngoài email/password trong scope.

API #03 và #04 được đối chiếu với source hiện tại. API #03 có discrepancy contract: catalog/DD #03 ghi HTTP 201 `DESIGN_RESOURCE_CREATED` với `ApiEnvelope<UserProfile>` và errors 422/500; AC-02/current route ghi HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, current source trả profile cùng access/refresh token fields và thêm errors 401/403. DD #03 còn `Draft — Needs Confirmation`; screen không quyết định thay API owner. Không thiết kế chi tiết cơ chế lưu token ở client vì source Study Web và approved persistence policy chưa có.

## Plan tóm tắt

- Art direction `premium editorial sign-in`, dùng ocean palette và brand mark cùng họ SH-01, nhưng artwork riêng. Minh họa sách/giấy/bút là PNG trong suốt tạo riêng bằng imagegen, không có chữ giả, dữ liệu hoặc logo ngoài.
- Desktop chia hai vùng: editorial panel trái, form là vùng hành động chính bên phải. Container 1120px centered trên canvas 1440×960. Card trắng viền mảnh, shadow rất nhẹ, nhịp 4px.
- Chỉ có email, mật khẩu, nút đăng nhập và link đăng ký. Không thêm quên mật khẩu, remember-me, show-password, CAPTCHA, OTP hay social login.
- Main screenshot có đúng 17 mục tiêu đánh số; error/loading/role branches mô tả ở các phần sau và không giả xuất hiện trong ảnh idle. Artwork riêng được tạo bằng imagegen, lưu kèm dạng `learning-book-hero.png`.

## Layout và responsive

| Vùng | Desktop 1440×960 | Tablet 768–1023 | Mobile 320–767 |
|---|---|---|---|
| Container/header | max-width 1120px; x=160..1280; header 96px, brand x=160 y=30 | gutter 24px; brand giữ nguyên | gutter 16px; brand hiển thị, không drawer |
| Editorial panel | x=160 y=128 w=520 h=704; radius 16; nền #E8F4FA | giảm art, copy giữ dễ đọc | xếp sau form hoặc ẩn riêng art decorative; không che action |
| Illustration | x=185 y=196 w=470 h=313; transparent PNG, centered above editorial copy | thu nhỏ theo panel | decorative; có thể thu nhỏ hoặc ẩn |
| Login form | x=736 y=176 w=544 h=608; padding 48px; inner width 448px | max-width 600px, căn giữa | full width trừ gutter 16px; input và button 100% |
| Inputs/button | email y=418 h=56; password y=532 h=56; button y=620 h=56; radius 8px | giữ cao 56px | giữ ≥56px và hit area ≥44×44px |
| Footer | không thêm footer marketing/legal ngoài scope | không đổi | không đổi |

Bounding boxes dưới đây là pixel tuyệt đối của SVG 1440×960. Font thực tế là `Noto Sans` từ system sans fallback vì Inter chưa có trên môi trường render. `N/A` nghĩa là không áp typography.

## Bản đồ 17 elements

| # | Element / content | Bounding box x,y,w,h (px) | Typography | Surface / alignment | Semantics | Click/tap | Hover/focus/pressed | Responsive | Data source |
|---:|---|---|---|---|---|---|---|---|---|
| #1 | Study brand mark: Biểu tượng trang học mở trong brand link | 160,30,38,38 | N/A | SVG mark #0B5F8A, nền vuông bo 11px; nét trang trắng 2px; không đổ bóng | decorative image bên trong link có accessible name Study, Trang chủ | click/tap brand link → `/` (SH-01) | focus-visible 2px #0B5F8A offset 2px trên link cha; không có hover riêng cho mark | giữ 38×38px ở mọi breakpoint; hit area link cha ≥44×44px | STATIC_UI; design continuation từ SH-01 |
| #2 | Study wordmark: Study | 210,34,82,30 | Noto Sans 23px/30px/700 #073B57 | background none; border none; left aligned; thuộc cùng brand link với #1 | link text; accessible name của brand link | click/tap → `/` (SH-01) | hover 140ms đổi màu #084968; focus-visible 2px #0B5F8A offset 2px; pressed #084968 | giữ nguyên; brand link không bị ẩn ở 320px | STATIC_UI |
| #3 | Editorial eyebrow: STUDY · KHÔNG GIAN HỌC TẬP | 212,582,282,18 | Noto Sans 13px/18px/700 #0B5F8A | background none; border none; accent bar 3×18px #43A5C5 ở x=194; letter spacing 0.4px | static text | không có | không áp dụng; không hover/focus/pressed | wrap tự nhiên; không thay đổi ý nghĩa | STATIC_UI |
| #4 | Editorial heading: Chào mừng bạn / trở lại. | 212,620,400,88 | Noto Sans 36px/44px/700 #073B57 | background none; border none; hai dòng trái; khoảng dòng 0px ngoài line-height | h2 | không có | không áp dụng; không hover/focus/pressed | tablet giữ tối đa 2 dòng; mobile co cỡ theo container và không tràn ngang | STATIC_UI |
| #5 | Editorial supporting copy: Đăng nhập để mở lại không gian học tập / của bạn trên Study. | 212,736,404,52 | Noto Sans 16px/26px/400 #536A7A | background none; border none; left aligned; two lines | paragraph | không có | không áp dụng; không hover/focus/pressed | wrap theo chiều rộng cột; không cắt nội dung | STATIC_UI |
| #6 | Editorial learning illustration: PNG minh họa sách mở, giấy và bút trong suốt; không chứa chữ hoặc dữ liệu | 185,196,470,313 | N/A | PNG artwork trong suốt 470×313px, căn giữa; sách/paper ocean palette với điểm coral nhỏ; decorative, không viền | decorative group, `aria-hidden=true` | không có | không áp dụng; không hover/focus/pressed | tablet thu nhỏ; mobile có thể ẩn vì decorative | IMAGEGEN; original hero asset tạo riêng cho SH-02, file `learning-book-hero.png` |
| #7 | Login form surface: Form group chứa #8–#17 | 736,176,544,608 | N/A | surface #FFFFFF; border 1px #D4E2E9; radius 16px; shadow 0 16px 48px rgba(7,59,87,0.06) | form group; không phải link/card action | không có event riêng; submit duy nhất qua #15 hoặc Enter trong field | không áp dụng; surface không có hover/pressed | desktop 544px; tablet max-width 600px; mobile full width trong gutter 16px | STATIC_UI |
| #8 | Form eyebrow: TÀI KHOẢN STUDY | 784,226,240,18 | Noto Sans 13px/18px/700 #536A7A | background none; border none; left aligned; letter spacing 0.5px | static text | không có | không áp dụng; không hover/focus/pressed | giữ nguyên cỡ; không wrap ở 320px content width | STATIC_UI |
| #9 | Login heading: Đăng nhập | 784,262,300,48 | Noto Sans 40px/48px/700 #073B57 | background none; border none; left aligned | h1 | không có | không áp dụng; không hover/focus/pressed | co theo viewport nhỏ; không clip tiếng Việt | STATIC_UI |
| #10 | Form supporting text: Sử dụng email và mật khẩu đã đăng ký. | 784,324,432,26 | Noto Sans 16px/26px/400 #536A7A | background none; border none; left aligned | paragraph | không có | không áp dụng; không hover/focus/pressed | wrap theo form width | STATIC_UI; nội dung không thêm policy |
| #11 | Email label: Email | 784,390,100,20 | Noto Sans 14px/20px/600 #17324D | background none; border none; left aligned; liên kết input #12 | label `for=email` | click/tap label focus #12 | không có hover; focus theo input được label trỏ tới | giữ nguyên; label luôn hiển thị phía trên input | STATIC_UI; API #03 field `email` |
| #12 | Email input: Placeholder `Nhập email của bạn`; value để trống trong ảnh | 784,418,448,56 | Noto Sans 15px/24px/400 #17324D; placeholder #536A7A | input white; border 1px #536A7A; radius 8px; padding 16px; no icon | required input `type=email`, `autocomplete=username`, `inputmode=email`; label #11 | focus/type/paste/password-manager fill; trim/validate theo current source; không tự submit khi blur | hover border #084968; focus-visible 2px #0B5F8A offset 2px; invalid border + inline error; no pressed state | width 100%, min-height 56px; giữ label; không zoom/clip tại 320px | API #03 `email`; current validator EmailStr, trim, max 255; không sample account |
| #13 | Password label: Mật khẩu | 784,504,120,20 | Noto Sans 14px/20px/600 #17324D | background none; border none; left aligned; liên kết input #14 | label `for=password` | click/tap label focus #14 | không có hover; focus theo input được label trỏ tới | giữ nguyên; label luôn hiển thị phía trên input | STATIC_UI; API #03 field `password` |
| #14 | Password input: Placeholder `Nhập mật khẩu`; value để trống trong ảnh | 784,532,448,56 | Noto Sans 15px/24px/400 #17324D; placeholder #536A7A | input white; border 1px #536A7A; radius 8px; padding 16px; no visibility icon | required input `type=password`, `autocomplete=current-password`; label #13 | focus/type/paste/password-manager fill; client rejects only blank/whitespace per current source; no password-strength rule | hover border #084968; focus-visible 2px #0B5F8A offset 2px; invalid border + inline error; no pressed state | width 100%, min-height 56px; keep password manager and paste support | API #03 `password`; no sample credential or value |
| #15 | Submit button: Đăng nhập | 784,620,448,56 | Noto Sans 16px/24px/600 #FFFFFF | fill #0B5F8A; border none; radius 8px; centered; min hit target exceeds 44px | submit button | click/tap or Enter → validate fields → one `POST /api/v1/auth/login` JSON `{email,password}`; no Authorization header | hover 140ms fill #084968; focus-visible 2px #0B5F8A offset 2px; pressed #084968 without movement; pending label `Đang đăng nhập…`, disable duplicate submit | full form width; height 56px; 100% width on mobile | API #03 current source; contract status/schema mismatch documented separately |
| #16 | Signup prompt: Chưa có tài khoản? | 837,708,175,24 | Noto Sans 15px/22px/400 #536A7A | background none; border none; centered with #17 | static text | không có | không áp dụng; không hover/focus/pressed | wrap before link only when needed; no overlap at 320px | STATIC_UI |
| #17 | Signup link: Tạo tài khoản | 1018,708,130,24 | Noto Sans 15px/22px/600 #0B5F8A | background none; border none; underline 1px #0B5F8A; inline beside #16 | navigation link | click/tap → `/register` (SH-03) | hover 140ms color #084968; focus-visible 2px #0B5F8A offset 2px; pressed #084968 | preserve ≥44px hit area; wrap to next line if required | SH-03 route from screen inventory; route remains design target |

## API, validation và event flow

### API #03 — `POST /api/v1/auth/login`

- Public JSON body `{email, password}`; không gửi Authorization header.
- Current source: email trim + EmailStr validation + max 255; password phải là string và không được whitespace-only; không có password-strength policy. Source lookup user, verify stored password hash, và chỉ cho `status == ACTIVE`.
- Success hiện là HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; data profile có id/full_name/email/role/avatar_url/phone/status/timestamps và access_token/refresh_token/token_type/expires_in/refresh_expires_in. Chỉ refresh-token hash được ghi vào DB. Không vẽ/hiển thị token hoặc password hash.
- 401: credentials sai hoặc account không tồn tại; current source trả cùng message “Email hoặc mật khẩu không đúng.”.
- 403: current source từ chối mọi status khác ACTIVE với “Tài khoản không được phép đăng nhập.”; không tự diễn giải chỉ là `LOCKED` và không khẳng định rate limit/lockout.
- 422: `meta.fieldErrors` map tới field. Client có thể trim/format check theo current source; catalog validation boundaries vẫn chưa duyệt.
- 500: chỉ hiển thị thông điệp an toàn “Không thể hoàn tất đăng nhập.”, không đưa raw DB/hash/config detail vào UI.

### API #04 — `GET /api/v1/users/me`

- Chỉ gọi sau khi #03 xác thực role `STUDENT`; dùng Bearer access token. #04 shared guard chặn role khác bằng 403 trước DB.
- API #04 trả current profile; source không có `bio`. Không gọi `/users/me` cho Mentor/Admin.
- Role Mentor/Admin hiện là `G-02 BLOCK`: API #03 có thể trả role token nhưng không có bootstrap profile endpoint phù hợp. Không thể xác định destination thành công của các role này bằng current source.

### Điều hướng

- Brand #1/#2 → `/` (SH-01); link #17 → `/register` (SH-03).
- Sau Student login: gọi #04, rồi chỉ dùng `returnTo` nếu là relative internal route trong allowlist. Default ST-01 `/student` là candidate, chờ product/role-shell xác nhận. Không nhận absolute/external URL.
- API #03 success / API #04 role/source sequencing và token persistence còn discrepancy; không gộp lỗi #03 403 với #04 403.
- R-X01 `POST /api/v1/auth/refresh` có source nhưng không có API ID/contract hiện hành; screen không thêm nút refresh/logout.

## UI states

| State | Điều kiện | Hiển thị và hành vi |
|---|---|---|
| `IDLE` | Mở `/login`, chưa submit | Form trống, button “Đăng nhập”, không alert; chính là ảnh bàn giao. |
| `FOCUS` | Focus field/link/button | Focus ring 2px #0B5F8A offset 2px; không layout shift. |
| `DIRTY` | Có input | Giữ nội dung; cho paste/password manager; chưa gửi request. |
| `CLIENT_VALIDATION` | Submit thiếu/sai input theo policy current source | Email local format/length; password blank/whitespace. Inline error gắn `aria-describedby`. Nếu có nhiều lỗi, summary focusable ở đầu form có link tới field; move focus một lần sau submit. |
| `SUBMITTING` | POST #03 pending | Button đổi thành “Đang đăng nhập…”, disabled để chặn duplicate; không tự retry POST. |
| `AUTH_401` | POST #03 trả 401 | Alert “Email hoặc mật khẩu không đúng.”; giữ email, không nêu field nào sai, không tiết lộ tài khoản tồn tại. |
| `ACCOUNT_INACTIVE_403` | POST #03 trả 403 | Alert dùng current source wording “Tài khoản không được phép đăng nhập.”; policy phân biệt status vẫn chưa được BA/BE chốt. |
| `VALIDATION_422` | POST #03 trả 422 | Đọc fieldErrors từ meta; liên kết field cụ thể. Không tạo password policy ngoài source. |
| `SERVER_500` | POST #03 trả 500 | Alert “Không thể hoàn tất đăng nhập.”; giữ email; không hiện raw detail. |
| `NETWORK_ERROR` | Không nhận được HTTP response | Thông báo kết nối ngắn, cho phép người dùng submit lại chủ động; không tuyên bố đã login. |
| `STUDENT_PROFILE_401/403/500` | #03 đã thành công nhưng #04 lỗi | Tách endpoint context khỏi login errors; #04 403 không được hiển thị như sai credentials. 401/403 về trạng thái SH-05/safe previous route theo router được duyệt. |
| `ROLE_BOOTSTRAP_BLOCK` | #03 success role khác STUDENT | G-02; không gọi #04, không giả dashboard hoặc login failure. Cần quyết định BE/Product trước khi hoàn tất route state. |
| `RETURN_TO_REJECTED` | returnTo là absolute/external hoặc không allowlist | Bỏ giá trị không an toàn; dùng default chỉ khi destination role được phê duyệt. Không redirect external. |

Empty state không áp dụng cho form login. Loading/error không thay đổi main idle screenshot; thông báo động là variants của form, không thêm fake alert vào ảnh mặc định.

## Accessibility và visual tokens

- Font `Noto Sans` system sans fallback; heading #9 40/48/700; editorial heading #4 36/44/700; body 16/26/400; labels 14/20/600; controls 56px.
- Palette: page #F6FAFC; panel #E8F4FA; surface #FFFFFF; primary #0B5F8A; hover #084968; deep #073B57; accent #43A5C5 only decorative; text #17324D; muted #536A7A; border #D4E2E9. Input boundary uses canonical `#536A7A` (5.66:1 against white); focus uses #0B5F8A.
- Form labels are persistent, uniquely associated with inputs. Sequence: brand → email → password → submit → signup. Decorative art `aria-hidden`; no illustration focus.
- Paste/password-manager support; `autocomplete=username` and `current-password`; no token/password in URL, logs, screenshot or visible copy.
- Text contrast ≥4.5:1, control boundary ≥3:1, focus visible and not obscured. Hover 140ms color only; `prefers-reduced-motion` disables nonessential transitions.

## Discrepancies, open decisions, review checklist

| ID | Evidence | Status / impact |
|---|---|---|
| API #03 response/errors | Catalog/DD #03 vs AC/source have status, payload, code discrepancies | `DISCREPANCY / Draft — Needs Confirmation`; UI consumes only current source in implementation, API contract owner must reconcile. |
| API #04 role | Source guard role=STUDENT only | `BLOCK G-02`; do not route Mentor/Admin to Student profile. |
| Token session | Source emits tokens and refreshes, client policy absent | `SOURCE_REQUIRED`; no client persistence assertion. |
| Login destination | returnTo allowlist is target behavior; default route is not approved | `OPEN_DECISION`; ST-01 candidate only. |
| Study Web runtime | No app/router/API consumer source in checkout | `NOT_IMPLEMENTED`; these assets are design-only. |

- [ ] 17 unique markers #1–#17, each 24×24px with white 12px/700 text and 1px white keyline.
- [ ] Clean/annotated geometry matches; only marker layer differs; both PNG 1440×960.
- [ ] Every row has a specific size, font, event, state, responsive and data source; coordinates match SVG.
- [ ] No label, placeholder, button, text, illustration or marker overlap; Vietnamese text glyphs render cleanly.
- [ ] No unsupported recovery/social/OTP/remember-me/session or role-dashboard affordance.
- [ ] Visual review at full resolution complete; no app runtime, live DB or deployment claim.
