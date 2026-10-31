# SH-02 — Plan thiết kế màn hình đăng nhập

## 1. Phân loại và phạm vi

```text
primary_task_type: docs
secondary_task_types: []
project_scopes: [web-work, server-study]
cross_scope_dependencies: [SH-02 -> Study API #03 POST /api/v1/auth/login -> API #04 GET /api/v1/users/me for STUDENT only; R-X01 refresh is source-only]
```

- Thiết kế đúng một màn hình: **SH-02 Đăng nhập**, route mục tiêu `/login`, actor Guest, AC-02, priority P0.
- Đây là `DESIGN_TARGET / NOT_IMPLEMENTED`: checkout không có Study Web source/router, chỉ có inventory và tài liệu design resource. Không tuyên bố route hoặc client auth flow đã chạy.
- Màn hình liên quan để điều hướng/trạng thái: SH-01 `/`, SH-03 `/register`, SH-05 `/forbidden`, ST-01 `/student` (route thiết kế). Không thiết kế lại các screen đó trong gói SH-02.
- Không có modal, drawer, social login, CAPTCHA, OTP, remember-me, password recovery hoặc màn hình con được chứng minh; không thêm vào giao diện.

## 2. Chứng cứ API và logic

| Nguồn | Current source | Expected / discrepancy | Tác động thiết kế |
|---|---|---|---|
| API #03 `POST /api/v1/auth/login` | Public JSON body `{email,password}`; source chuẩn hóa email bằng trim/EmailStr/max 255, từ chối password chỉ có whitespace; tìm user, xác minh hash, chỉ chấp nhận `status=ACTIVE`; lỗi credentials là HTTP 401, inactive là 403, lỗi nội bộ 500. Thành công HTTP 200 với `DESIGN_RESOURCE_RETRIEVED`, profile và access/refresh token fields. | Catalog là normative nhưng DD vẫn `Draft — Needs Confirmation`: HTTP 201 `DESIGN_RESOURCE_CREATED`, `ApiEnvelope<UserProfile>`, chỉ quy định 422/500; AC-02 lại ghi 200/401/403. Token response/persistence cũng chưa thống nhất. | Ghi source và contract tách biệt. UI field labels là Email/Mật khẩu; không hiển thị raw tokens, token trong URL hoặc nội dung lỗi nội bộ. Chỉ mô tả state đang có bằng chứng; không chọn response contract thay BA/BE. |
| API #04 `GET /api/v1/users/me` | Bearer access JWT; shared guard bắt buộc role `STUDENT`; trả profile công khai, không trả `bio`. Role khác bị 403 trước DB query. | AC-02 muốn dùng /me sau login; API #03 đã trả profile cơ bản. Không có endpoint bootstrap/profile phù hợp cho Mentor/Admin. G-02 còn BLOCK. | Chỉ gọi #04 với role STUDENT. Không gửi Mentor/Admin vào Student `/me`, không dựng dashboard role chưa được xác nhận. Role handoff là unresolved decision, không giả thành login failure hay success route. |
| Token/client session | #03 current source phát access JWT, opaque refresh token, ghi refresh-token hash; R-X01 refresh có source nhưng không có API ID/contract riêng. | Client storage/session lifecycle chưa có Study Web source hoặc quyết định approved. | Không chốt localStorage/cookie/IndexedDB, không thêm “remember me”, logout hay token persistence details; token handler được để là `SOURCE_REQUIRED` cho implementation. |
| Route return | Inventory yêu cầu giữ route đích an toàn; `list_screen.md` §6.2 yêu cầu chỉ nhận relative internal route allowlisted. | Router Study Web không tồn tại trong checkout; đích mặc định sau login chưa chốt rõ ngoài ST-01 hoặc role-shell. | Chỉ route tiếp tới `returnTo` đã allowlist sau khi session/profile pass; không nhận absolute/external URL. Default `/student` là candidate của ST-01, cần xác nhận product và không ghi như runtime fact. |

### Source trace

```text
Guest -> SH-02 form -> POST #03 -> if role STUDENT, Bearer GET #04 -> safe internal returnTo / default route pending
                                      -> Mentor/Admin: G-02 BLOCK; không gọi Student-only #04
```

### Quy tắc xử lý lỗi

- **401 #03:** dùng cùng thông báo source `Email hoặc mật khẩu không đúng.` cho email không tồn tại hoặc mật khẩu sai; không phân biệt tài khoản có tồn tại.
- **403 #03:** source trả `Tài khoản không được phép đăng nhập.` cho mọi `status != ACTIVE`, không riêng `LOCKED`. Giữ đúng wording source trong state specification và ghi rõ policy account status/privacy còn cần xác nhận.
- **422:** lỗi field nằm trong `meta.fieldErrors`; map lỗi vào field tương ứng. Local validation chỉ phản chiếu email format/trim/max-length và password nonblank theo source hiện tại, không tạo password-strength rules.
- **500:** chỉ hiện thông báo an toàn `Không thể hoàn tất đăng nhập.`; không lộ raw DB/hash/token/config details.
- **Network failure:** thông báo ngắn, cho phép người dùng submit lại chủ động; không tự retry POST và không tuyên bố đã đăng nhập.
- **API #04 401/403/500:** là lỗi sau bước login, tách khỏi 401/403 của #03; không đặt nội dung `/users/me` sai role vào state 401 credentials.

## 3. Art direction

- Hướng: **premium editorial sign-in**, yên tĩnh, gọn, chuyên nghiệp, nhiều khoảng thở; màn hình auth có nhịp riêng nhưng nhận ra cùng sản phẩm Study với SH-01.
- Dùng ocean palette từ `.agents/web-study/design.md`: page `#F6FAFC`, surface `#FFFFFF`, primary `#0B5F8A`, hover/pressed `#084968`, deep `#073B57`, accent `#43A5C5` chỉ làm chi tiết nhỏ, soft `#E8F4FA`, text `#17324D`, muted `#536A7A`, border `#D4E2E9`.
- Typography `Noto Sans` theo font fallback đang cài; 4px spacing rhythm; surface phẳng, viền mảnh, shadow khuếch tán nhẹ, radius control 8–12px và panel 12–16px.
- Header thoáng với cùng Study mark/wordmark như SH-01. Layout desktop bất đối xứng hai vùng: cụm minh họa/editorial bên trái, form đăng nhập là điểm tập trung bên phải. Căn theo container 1120px, gutter 32px.
- Vùng minh họa dùng PNG trong suốt được tạo riêng bằng imagegen: sách mở, giấy và bút trong ocean palette, một điểm nhấn coral nhỏ. Đây là decorative target; không có chữ, data/metric, logo ngoài và không lặp illustration của SH-01.
- Form nằm trên surface trắng rõ ràng; heading nổi bật, labels luôn hiện phía trên input, khoảng cách trường nhất quán, primary submit rõ nhất. Không thêm đường phân cách hoặc phụ kiện chỉ để lấp khoảng trống.
- Giữ trang ở light-first. Không gradient lớn, glass, neon, heavy shadow, emoji, floating badges hoặc decoration cạnh tranh với form.

## 4. Canvas, layout và responsive target

| Vùng | Desktop canvas 1440×960 | Tablet 768–1023 | Mobile 320–767 |
|---|---|---|---|
| Page/header | Header 96px, container max 1120, centered, gutters 32px; brand link về `/`. | Gutter 24px; không thêm nav item. | Gutter 16px; brand giữ nguyên, không drawer. |
| Main | Panel trái x=160 y=128 w=520 h=704; sign-in card phải x=736 y=176 w=544 h=608; cả hai căn giữa theo viewport. | Xếp gọn hoặc giảm bề rộng art; giữ form một cột và thứ tự đọc logic. | Một cột; form trước nội dung trang trí hoặc theo thứ tự semantic; art decorative có thể thu nhỏ/ẩn; không horizontal scroll. |
| Illustration | x=185 y=196 w=470 h=313; căn giữa phần trên của panel. | Thu nhỏ theo panel; giữ tỉ lệ ảnh. | Art decorative có thể ẩn. |
| Form | Padding 48px; input 448×56px, submit 448×56px. | Form tối đa khoảng 600px và căn giữa. | Form full width; input/button full width; nút và link có hit area tối thiểu 44×44px. |
| Footer | Không thêm footer marketing/legal nếu chưa có source; có thể bỏ footer. | Không đổi. | Không đổi. |

## 5. Main state và element map dự kiến

Ảnh chính là trạng thái `IDLE`, không có lỗi, dữ liệu credentials và profile không giả lập. Giữ 17 marker cho 17 target dưới đây; mọi element mới nếu thật sự cần phải được thêm vào map, table và screenshot trước khi đóng gói.

| # | Element | Content / semantics | Interaction |
|---:|---|---|---|
| 1 | Study brand mark | SVG mark trong brand link; decorative icon, accessible name ở link/wordmark | Click/tap → `/` (SH-01). |
| 2 | Study wordmark | Text `Study`, brand link | Click/tap → `/` (SH-01). |
| 3 | Editorial eyebrow | Nhãn tĩnh ngắn cho vùng giới thiệu | Không event/focus. |
| 4 | Editorial heading | H2 ngắn, thân thiện, không hứa hẹn thành tích/progress cụ thể | Không event/focus. |
| 5 | Supporting copy | Một câu giải thích việc đăng nhập bằng tiếng Việt | Không event/focus. |
| 6 | Learning illustration | PNG decorative, aria-hidden; không giả lập screenshot/dữ liệu | Không event/focus. |
| 7 | Login form surface/group | Container semantics `form`/`fieldset` đúng ngữ cảnh; không phải nút/card link | Không event riêng. |
| 8 | Form eyebrow | Nhãn tĩnh nhỏ, nếu có thì ngắn và có nghĩa | Không event/focus. |
| 9 | Login heading | H1 `Đăng nhập` | Không event/focus. |
| 10 | Form supporting text | Nêu email và mật khẩu là thông tin cần dùng | Không event/focus. |
| 11 | Email label | Label `Email`, gắn với input #12 | Không event/focus độc lập. |
| 12 | Email input | `type=email`, autocomplete username, inputmode email; không chứa sample account | Focus/type/paste; validate local theo current source; không prefill sample. |
| 13 | Password label | Label `Mật khẩu`, gắn với input #14 | Không event/focus độc lập. |
| 14 | Password input | `type=password`, autocomplete current-password; không show plaintext trong mockup | Focus/type/paste/password manager; không thêm show/hide nếu không được cần. |
| 15 | Submit button | `Đăng nhập`, primary button | Enter hoặc click/tap cùng submit handler → POST #03 đúng một lần; loading chặn duplicate. |
| 16 | Signup prompt | Text `Chưa có tài khoản?` | Không event/focus. |
| 17 | Signup link | `Tạo tài khoản` | Click/tap → `/register` (SH-03). |

No event for illustration/text-only labels; no hover/focus/pressed styling on static elements. Interactive states are applied only to links, fields and button.

## 6. Accessibility và interaction contract

- Semantic order: brand → email → password → submit → signup link. Reading order on responsive layout follows semantic order, not visual illustration placement.
- Visible labels; email/password inputs each have unique IDs, labels, required semantics, autocomplete values, and associated help/error text. Allow paste and password-manager fill.
- Focus-visible 2px `#0B5F8A`, offset 2px; no focus clipping. Input/control boundary contrast ≥3:1; normal text ≥4.5:1 on its actual surface. Do not use `#43A5C5` as small text/border/focus alone.
- Field errors remain inline and are programmatically associated. On multi-field validation, show a focusable error summary at the top of the form with links to each invalid field; move focus once after failed submit, not on every blur. For 401/403/500/network errors, use a form-level announced alert and preserve entered email; do not preserve/show plaintext password after a completed failure unless behavior is explicitly approved.
- Submit loading state communicates `Đang đăng nhập…`; disable only duplicate submit while request is pending. Error state restores an actionable button. Hover 140ms color/underline only; pressed feedback must not shift layout; respect `prefers-reduced-motion`.
- No color-only error indication, no secrets in URL/log/screenshot. Keep return path relative and allowlisted. No external redirect.

## 7. Acceptance review

- [ ] Image and `SCREEN.md` each describe only SH-02; no screen children/modal/drawer.
- [ ] All 17 default-state visible targets have matching, unique numbered badges and one exact table row each; no badge obscures logo, text, labels, input, button or artwork.
- [ ] Clean and annotated PNG have identical geometry/content except the marker overlay; both are 1440×960.
- [ ] Form copy is Vietnamese, email/password only; no social, forgot-password, CAPTCHA, OTP, remember-me, fake user, metric or external brand.
- [ ] API #03 current behavior and catalog/AC-02 discrepancies are documented separately; #04 is Student-only; no token-storage or role-routing decision is invented.
- [ ] 401, 403, 422, 500, network, loading, invalid-returnTo, Student handoff and Mentor/Admin blocker are described accurately.
- [ ] Typography, dimensions, colors, spacing, event, hover/focus/pressed, target and responsive rules in `SCREEN.md` are concrete and match final source geometry.
- [ ] Visual QA at full resolution and focused marker/overlap inspection completed before ZIP delivery.
