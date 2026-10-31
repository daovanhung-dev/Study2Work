# SH-03 — Plan thiết kế màn hình đăng ký học viên

## 1. Phân loại và phạm vi

```text
primary_task_type: docs
secondary_task_types: []
project_scopes: [web-work, server-study]
cross_scope_dependencies: [SH-03 -> Study API #01 POST /api/v1/auth/register -> SH-04 -> Study API #02 POST /api/v1/auth/verify-email/send; SH-02 is the existing-account route]
```

- Thiết kế đúng một screen: **SH-03 Đăng ký học viên**, route target `/register`, actor Guest, AC-01, priority P0.
- Đây là `DESIGN_TARGET / NOT_IMPLEMENTED`. `apps/study-client/` không có Study Web runtime, router hay client API; không tuyên bố route hoặc form đã chạy.
- SH-01 `/` là brand/home destination; SH-02 `/login` là đường dành cho người đã có tài khoản; SH-04 `/register/verification` là screen kế tiếp theo inventory. SH-04 là route liên kết độc lập, không phải screen con của SH-03 và không được thiết kế lại trong gói này.
- Không có child screen, modal, drawer hoặc overlay đã được xác nhận trong SH-03. Không thêm CAPTCHA, OTP, social login, password confirmation, password-strength meter hoặc checkbox điều khoản.

## 2. Evidence và logic hiện hành

| Nguồn | Expected behavior | Current source | Tác động thiết kế |
|---|---|---|---|
| Inventory SH-03 / AC-01 / F01 | Form họ tên, email, mật khẩu → API #01; `201` đưa `data.id`/`data.email` sang SH-04; `409` giữ người dùng ở form; link sang SH-02. Consent chỉ khi có contract. | Inventory là target journey, không chứng minh Study Web runtime. | Dùng 3 field đúng request; thành công chỉ xác nhận account creation và chuyển SH-04; không nói email đã gửi/verified. Không render consent vì không có contract/copy được duyệt. |
| API #01 `POST /api/v1/auth/register` | DD Draft mô tả public JSON, HTTP 201, `ApiEnvelope<UserProfile>`, lỗi 409/422/500. | Source route public, HTTP 201. Body `email`, `password`, `full_name`. Validator trim email + `EmailStr`, max 255; password chỉ reject blank/whitespace; trim full_name, 1–150. View kiểm tra trùng, băm Argon2id, INSERT `users` với role `STUDENT`, commit. Success code `DESIGN_RESOURCE_CREATED`, data profile công khai; không trả plaintext password/hash. 409 `DESIGN_STATE_CONFLICT` / “Email đã tồn tại.”; 422 có `meta.fieldErrors`; 500 `DESIGN_INTERNAL_ERROR` / “Không thể tạo tài khoản.” | Local form chỉ phản chiếu validation current-source; không thêm password complexity/minimum. Email trim/format/max; không tự lower-case hay suy diễn case-insensitive uniqueness. Không hiển thị `status`, profile `bio`, tokens hoặc DB errors. |
| API #01 post-create side effect | Expected AC-01 dispatch verification sau commit, lỗi delivery được log/retry. | Current #01 không gọi API #02; sau commit chỉ log `verification_dispatch_pending`. DD #01 `Draft — Needs Confirmation`; feature enablement, owner, account status, profile mapping và `bio` còn open questions. | Đánh dấu discrepancy. `201` chỉ xác nhận tài khoản được tạo theo response; không tự khẳng định email đã gửi hoặc tài khoản đã xác thực. |
| API #02 `POST /api/v1/auth/verify-email/send` | SH-04 gửi `user_id`/`email`, HTTP 202 là accepted theo inventory. | Route công khai trả 202 khi provider chấp nhận; provider mặc định là stub trả `accepted`, không gửi email thật, không tạo token/link. Provider exception hiện trả 500 đồng bộ; chưa có queue/retry worker. #02 không được gọi trực tiếp trong SH-03. | Chỉ mô tả #02 như bước SH-04 target; không đặt “email đã gửi”, OTP, verification link hay expiry vào SH-03. |

### Trace

```text
Expected inventory: Guest -> SH-03 -> POST #01 -> 201 data.id/email -> SH-04 -> POST #02 -> accepted/stub -> SH-02
Current source: SH-03 UI absent -> public #01 -> validate -> duplicate lookup -> Argon2id hash -> INSERT users/commit -> safe 201 profile; #01 only logs verification pending -> separate #02 invokes default stub -> 202 accepted without email delivery
```

### Contract discrepancies to retain

- API #01 DD remains `Draft — Needs Confirmation`; source response omits `bio` although DD schema lists it. The DD asks product/backend to resolve account status, profile, password/email normalization and verification dispatch.
- Local DDL is not proof of live schema/status. Current INSERT omits `status`; do not display or promise ACTIVE/pending state.
- API #01 → #02 is not wired by current #01 source. The user inventory expects SH-04 to call #02 after account creation. Preserve both expected and current behavior.
- API #02 DD is also Draft. No token/link, expiry, delivery, retry worker, ownership check or final email-verification endpoint is source-backed.

## 3. Art direction và bố cục

- Hướng **editorial registration / quiet optimism**: liên kết trực quan với SH-02 bằng cùng brand, ocean tokens, spacing và form geometry; tạo hình minh họa riêng cho SH-03 thay vì lặp sách mở ở SH-02.
- Desktop frame `1440×960`; content max width 1120px, centered (`x=160..1280`), header 96px. Main starts 32px below header.
- Header: Study mark/wordmark ở x=160, y=30; giữ link trang chủ. Không thêm navigation ngoài brand.
- Left editorial panel: x=160, y=128, w=520, h=704, radius 16px, nền `#E8F4FA`. Minh họa transparent PNG riêng ở khoảng x=185, y=196, w=470, h=313; copy ở nửa dưới. Không có số liệu, text giả hoặc logo bên ngoài.
- Right form card: x=736, y=128, w=544, h=704, padding 48px, content width 448px; white surface, viền 1px `#D4E2E9`, radius 16px, diffuse shadow rất nhẹ. Card và panel chung trục dọc.
- Field height 56px, radius 8px, border `#536A7A`; label luôn hiện phía trên. Primary action full width 448×56px.
- Typography `Noto Sans` (system fallback đang có), 4px rhythm; H1 40/48/700, editorial H2 36/44/700, body 16/26/400, label 14/20/600, input 15/24/400.
- Palette: page `#F6FAFC`; surface `#FFFFFF`; primary `#0B5F8A`; hover/pressed `#084968`; deep `#073B57`; accent `#43A5C5` decorative only; soft `#E8F4FA`; text `#17324D`; muted `#536A7A`; border `#D4E2E9`; error `#B42318` only with text/icon.
- Custom art brief gửi ChatGPT: transparent horizontal editorial soft-3D/paper-sculpture illustration; một quyển notebook màu ocean ở thấp, 2–3 máy bay giấy/paper forms bay theo cung hướng lên, một coral dot nhỏ, vài thin orbit strokes; tông `#073B57/#0B5F8A/#43A5C5/#E8F4FA/white` + coral điểm nhỏ. Không text, số, logo, UI, watermark, panel nền đục, dark glow hoặc childish cartoon. Dùng như một decorative group, `aria-hidden=true`.
- Screenshot idle không hiển thị lỗi, loading, mẫu user, consent, password meter hoặc email success notice.

## 4. Main-state element map (19 targets)

Bounding box là tọa độ pixel dự kiến trên 1440×960; marker xuất hiện trong ảnh annotated và không che text/control.

| # | Element / content | Box x,y,w,h | Visual / typography | Semantic + event | States / responsive |
|---:|---|---|---|---|---|
| 1 | Study brand mark | 160,30,38,38 | Ocean-blue square, 11px radius; white open-page vector glyph, 2px stroke | Decorative image trong link có accessible name “Study, Trang chủ”; click/tap → `/` (SH-01). | Focus ring trên link cha; hit target cha ≥44×44; không hover riêng cho glyph. |
| 2 | Study wordmark `Study` | 210,34,82,30 | Noto Sans 23/30/700 `#073B57` | Phần text của brand link; click/tap → `/` (SH-01). | Hover/pressed `#084968`; focus-visible 2px `#0B5F8A`; luôn hiển thị. |
| 3 | Editorial eyebrow `HỌC TẬP BẮT ĐẦU TỪ ĐÂY` | 212,582,282,18 | 13/18/700 `#0B5F8A`, tracking 0.4px; accent bar 3×18px `#43A5C5` tại x=194 | Static text, không event. | Desktop single line; wrap có kiểm soát trên mobile. |
| 4 | Editorial heading `Bắt đầu hành trình` / `học tập.` | 212,618,408,88 | 36/44/700 `#073B57`; hai dòng, không giả metric. | H2, không event/focus. | Co theo container, giữ wrap cân đối và không tràn. |
| 5 | Editorial supporting copy `Tạo tài khoản học viên với họ tên, email và mật khẩu.` | 212,730,404,52 | 16/26/400 `#536A7A`; tối đa hai dòng. | Paragraph, không event/focus. | Wrap tự nhiên, không cắt ở 320px. |
| 6 | SH-03 learning illustration | 185,196,470,313 | Custom transparent PNG, paper-plane/notebook composition; art-only, no border. | Decorative group, `aria-hidden=true`; không event/focus. | Tablet scale giữ aspect; mobile có thể ẩn. |
| 7 | Registration form surface | 736,128,544,704 | White; 1px `#D4E2E9`; 16px radius; shadow blur mềm; 48px padding. | `<form>` group, không tự submit khi click nền; #17/Enter là submit. | Tablet max-width 600px; mobile full width trong gutter 16px. |
| 8 | Form eyebrow `TÀI KHOẢN HỌC VIÊN` | 784,176,250,18 | 13/18/700 `#536A7A`, tracking 0.5px. | Static text. | Không wrap ở nội dung card mobile. |
| 9 | H1 `Tạo tài khoản` | 784,212,360,48 | 40/48/700 `#073B57`. | H1, không event/focus. | Co theo viewport, tiếng Việt không clip. |
| 10 | Form helper `Điền thông tin để tạo tài khoản Study.` | 784,272,432,26 | 16/26/400 `#536A7A`. | Paragraph. | Wrap theo card; giữ meaning. |
| 11 | Full-name label `Họ và tên` | 784,332,160,20 | 14/20/600 `#17324D`. | `<label for=full_name>`; click/tap focus #12. | Luôn hiện, không placeholder-only. |
| 12 | Full-name input | 784,360,448,56 | White, 1px `#536A7A`, radius 8px, padding 16px; placeholder `Nhập họ và tên`; no icon. | Required text input, `autocomplete=name`; trim, require 1–150 chars per current validator; focus/type/paste; password-manager autofill remains available. | Hover border `#084968`; focus ring 2px `#0B5F8A` offset 2px; inline invalid/error summary after submit. |
| 13 | Email label `Email` | 784,436,120,20 | 14/20/600 `#17324D`. | `<label for=email>`; click/tap focus #14. | Always visible. |
| 14 | Email input | 784,464,448,56 | White, 1px `#536A7A`, radius 8px, padding 16px; placeholder `Nhập email của bạn`. | Required `type=email`, `inputmode=email`, `autocomplete=email`; current source trims, EmailStr-validates and caps normalized length at 255; paste allowed. | Hover/focus as #12; duplicate 409 inline at this field; no lower-case assertion. |
| 15 | Password label `Mật khẩu` | 784,540,120,20 | 14/20/600 `#17324D`. | `<label for=password>`; click/tap focus #16. | Always visible. |
| 16 | Password input | 784,568,448,56 | White, 1px `#536A7A`, radius 8px, padding 16px; masked; placeholder `Nhập mật khẩu`. | Required `type=password`, `autocomplete=new-password`; current source rejects blank/whitespace only; no strength/min-length policy beyond required. | Hover/focus as #12; allow paste and password managers; no reveal toggle or strength meter in this scope. |
| 17 | Submit button `Tạo tài khoản` | 784,656,448,56 | Fill `#0B5F8A`; white 16/24/600; 8px radius. | Submit button; click/tap or Enter → validate → single `POST /api/v1/auth/register` JSON `{email,password,full_name}`; no Authorization. | Hover/pressed fill `#084968` 140ms, focus-visible 2px ring; pending `Đang tạo tài khoản…`, disabled against duplicate submit. |
| 18 | Existing-account prompt `Đã có tài khoản?` | 872,736,150,22 | 15/22/400 `#536A7A`. | Static text. | Responsive wrap only if needed. |
| 19 | Login link `Đăng nhập` | 1038,736,118,22 | 15/22/600 `#0B5F8A`, underline; no button fill. | Link click/tap → `/login` (SH-02). | Hover `#084968`; focus-visible 2px ring; hit target ≥44×44. |

## 5. Interaction and state contract

| State | Trigger | UI behavior |
|---|---|---|
| `IDLE` | Guest opens `/register` | Three empty labelled fields; idle action `Tạo tài khoản`; no fake error or delivery claim. This is the exported screenshot. |
| `FOCUS / TOUCHED` | Keyboard/pointer focus; blur after edit | 2px focus ring `#0B5F8A`, no layout shift. After blur, show a local field error only when invalid; do not interrupt valid typing. |
| `CLIENT_VALIDATION` | Submit with missing/invalid field | `full_name`: trimmed 1–150; `email`: trim/format/max 255; `password`: nonblank. Show inline field errors associated through `aria-describedby`; if multiple, place focusable linked error summary at form top and focus it once. No password-strength rules. |
| `SUBMITTING` | Valid form, #01 pending | Button label `Đang tạo tài khoản…`, native disabled; reject duplicate click/Enter. No automatic retry. |
| `REGISTER_201_HANDOFF` | #01 returns 201 `DESIGN_RESOURCE_CREATED` | Use response `data.id`/`data.email` for the target transition to SH-04; show brief neutral success/transition feedback only if needed. Do not claim email delivery or verification; do not show ID/profile data. Transport/persistence for handoff remains a source/product decision. |
| `EMAIL_CONFLICT_409` | #01 returns 409 `DESIGN_STATE_CONFLICT` | Display source-safe message `Email đã tồn tại.` inline at email and in a concise form alert. Preserve name/email, clear password after completed request, allow edit or go to SH-02. |
| `VALIDATION_422` | #01 returns 422 `DESIGN_VALIDATION_ERROR` | Read `meta.fieldErrors`, map by field and show inline. Use linked summary on multi-field error. No new backend policy or client-only error code. |
| `SERVER_500` | #01 returns 500 `DESIGN_INTERNAL_ERROR` | Show safe source message `Không thể tạo tài khoản.`; retain non-sensitive fields; never show raw SQL/hash/stack trace. |
| `NETWORK_UNKNOWN` | No HTTP response | State that completion was not confirmed; no automatic mutation retry and no “account created/email sent” claim. Keep name/email; password handling must not persist outside the current page. |
| `RETURN_TO_SH04` | The inventory flow follows successful #01 | SH-04 is a separate screen; its #02 accepted/stub response is not part of SH-03 and must not imply delivery. |

### Accessibility / responsive

- Keyboard order: brand → full name → email → password → submit → sign-in link. All fields have persistent programmatic labels; errors are associated and summarized for screen-reader/keyboard access.
- Normal text contrast ≥4.5:1; input boundary ≥3:1; visible focus not clipped. `#43A5C5` only decorative. No color-only error state.
- Hover/focus/pressed transitions use 140ms color/underline only; no layout movement. Respect `prefers-reduced-motion`.
- Desktop 1440px: 1120px centered container, 520px panel + 56px gap + 544px card.
- Tablet 768–1023px: preserve all form controls in one column; card max-width 600px; artwork may shrink/collapse without squeezing the fields.
- Mobile 320–767px: gutter 16px; card full width, padding 24px; form fields/button full width and ≥56px high; no horizontal scroll. Art may be hidden; keep form and sign-in link available without relying on a side panel.
- No child screen/modal in this scope. SH-04 route is a separate inventory item; mention its handoff only.

## 6. Acceptance checklist for ChatGPT output and visual QA

- [ ] Output has clean and annotated PNG, exact source/asset, `SCREEN.md`, this `PLAN.md` and ZIP in SH-03 folder.
- [ ] Canvas is 1440×960; visual hierarchy is polished, calm, conversion-focused and consistent with Study tokens, while the illustration is distinct from SH-02.
- [ ] Exactly 19 default-state visible targets; badge numbers #1–#19 are unique and correspond one-to-one to table rows; no badge covers text, input, button, art subject or brand.
- [ ] Image text is legible Vietnamese; no invented claims, sample account, terms consent, confirmation password, strength meter, show-password, CAPTCHA, OTP or social provider.
- [ ] API flow, 201/409/422/500, validation, database/account caveats and API #01/#02 discrepancy match the source trace above.
- [ ] Screen does not claim #02 ran from #01, email was delivered, or email/account is verified/ACTIVE.
- [ ] Every table row includes coordinate/size, font/color, semantics, click/focus/hover/pressed/loading and responsive behavior where applicable.
- [ ] ZIP integrity, member list and image dimensions verified; clean and annotated PNG visually inspected at full resolution; iterate if any mismatch remains.
