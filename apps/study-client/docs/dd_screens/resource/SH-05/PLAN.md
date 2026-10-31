# SH-05 — Plan thiết kế state view không đủ quyền / session hết hạn

## 1. Scope và bằng chứng

```text
primary_task_type: docs
secondary_task_types: []
project_scopes: [web-work, server-study]
cross_scope_dependencies: [SH-05 -> API #04 GET /users/me; runtime R-X01 refresh; SH-02 login; SH-01 public fallback]
screen: SH-05, /forbidden, State view, AC-02/AC-11, API #04
artifact_status: DESIGN_TARGET / NOT_IMPLEMENTED
```

- Thiết kế một screen state view. Các trạng thái 403, 401 và refresh không khôi phục được phiên là ba biến thể trong cùng folder; chúng không phải screen con hay route mới. Dùng cùng 12 element IDs trong mọi ảnh annotated.
- `.agents/web-study/design.md` là visual target. SH-05 là trạng thái hệ thống bảo vệ truy cập; không biến thành trang lỗi toàn màn hình, form login thứ hai, dashboard hoặc màn hình khóa tài khoản.
- Source hiện tại có `GET /api/v1/users/me` và runtime `POST /api/v1/auth/refresh`. Không có Study Web `src`, router, auth interceptor hay client persistence; toàn bộ route, điều hướng và screenshot dưới đây là design target.

## 2. Luồng và quy tắc trạng thái

### Expected flow từ inventory

1. User mở route được bảo vệ; app nạp API #04 với access token.
2. Nếu API #04 trả 401, app có thể thử R-X01 tối đa một lần, đồng bộ nhiều request 401; khi refresh thành công, retry request ban đầu tối đa một lần.
3. Nếu thiếu/hết hạn access token và refresh không thành công, render biến thể `SESSION_REQUIRED` hoặc `TOKEN_REFRESH_FAILED`, cung cấp link SH-02 và giữ lại chỉ safe relative internal destination.
4. Nếu API #04 trả 403, render biến thể `ACCESS_DENIED`; tuyệt đối không gọi lại refresh theo nhánh này. Hành động quay lại dùng previous-safe-route, không đi tới URL ngoài.
5. Route direct-entry hoặc previous path không an toàn phải có public fallback SH-01 `/`.

### Current source trace

| Request/result | Current source behavior | UI decision |
|---|---|---|
| API #04 `GET /api/v1/users/me` 401 | Thiếu/sai Bearer, JWT invalid/expired, `sub`/`roles` thiếu/sai, hoặc current query không tìm thấy user. Message/business code an toàn. | Dùng copy tổng quát “Phiên đăng nhập cần được xác thực lại”; không hiển thị nguyên nhân account/claim cụ thể. |
| API #04 403 | JWT hợp lệ nhưng role không chứa `STUDENT`; shared guard trả trước profile query. | “Bạn chưa có quyền truy cập”; không refresh, không lộ role/permission. |
| API #04 500 | Lỗi decoder/config không phải 401, database hoặc model mapping. | Không render thành hết hạn/không đủ quyền; generic service error thuộc error boundary chung, ngoài 3 ảnh chính SH-05. |
| R-X01 refresh 200 | Refresh token opaque hợp lệ cho active account; old row revoke + new token hash insert + commit; trả token pair mới. | Client kỳ vọng retry request gốc một lần; không lộ token trong URL/log/UI. |
| R-X01 refresh 401 | Refresh token thiếu/hết hạn/đã dùng/không hợp lệ; code `DESIGN_AUTHENTICATION_REQUIRED`. | Terminal `SESSION_REQUIRED`; về SH-02, không retry refresh. |
| R-X01 refresh 403 | Current refresh view từ chối account không active với `DESIGN_ACCESS_DENIED`. | Dùng copy access denied chung, không khẳng định cụ thể tài khoản bị khóa/xóa. |
| R-X01 refresh 500/network | Runtime có safe 500 branch; client mapping/network response sau rotation chưa source-backed. | `TOKEN_REFRESH_FAILED` nói rõ chưa thể khôi phục phiên, không tuyên bố token chắc chắn hết hạn; không lặp refresh. CTA đăng nhập lại là design target. |

### State matrix

| State | Trigger | Headline/body | Primary action | Secondary action |
|---|---|---|---|---|
| `ACCESS_DENIED` | API #04 trả 403; hoặc refresh trả 403 | **“Bạn chưa có quyền truy cập”** · “Tài khoản hiện tại không thể mở trang này. Bạn có thể quay lại nơi vừa đến hoặc về trang chủ.” | **Quay lại** → previous-safe-route được allowlist; nếu không có route an toàn thì `/` (SH-01). | **Về trang chủ** → `/` (SH-01). |
| `SESSION_REQUIRED` | Thiếu/invalid/expired access, refresh absent/rejected (R-X01 401) | **“Phiên đăng nhập cần được xác thực lại”** · “Đăng nhập lại để tiếp tục từ trang bạn đang mở. Nếu đường dẫn còn hợp lệ, bạn sẽ được đưa trở lại.” | **Đăng nhập lại** → SH-02 `/login`, giữ relative `returnTo` chỉ khi allowlisted. | **Về trang chủ** → `/` (SH-01). |
| `TOKEN_REFRESH_FAILED` | Refresh không khôi phục được phiên, kể cả safe 500/network mapping do client quyết định | **“Chưa thể khôi phục phiên đăng nhập”** · “Không thể xác nhận phiên hiện tại. Đăng nhập lại để tiếp tục an toàn.” | **Đăng nhập lại** → SH-02, safe `returnTo` nếu hợp lệ. | **Về trang chủ** → `/` (SH-01). |

`SESSION_REQUIRED` và `TOKEN_REFRESH_FAILED` không có nút “Thử lại refresh”: R-X01 xoay vòng token; nếu response bị mất sau commit, token cũ có thể đã bị revoke. Tránh replay tự động. Không thêm logout, “liên hệ hỗ trợ”, account-switch API, role detail, trace ID giả hoặc endpoint mới. API #04 500 không bị gom vào 401/403.

## 3. Visual thesis và bố cục

- **Visual thesis:** “Một lối rẽ bình tĩnh khi đường truy cập dừng lại.” Cấu trúc mở, không dùng dấu chấm than đỏ, ổ khóa lớn, cảnh báo toàn trang hay ngôn ngữ đổ lỗi. H1 giải thích lý do; một CTA đúng với trạng thái là điểm nhấn; minh họa cổng/đường là vector trừu tượng, không giả lập role hoặc account state.
- **Design mode:** transactional system state, light-first, Study ocean palette. Không card mosaic, không gradient lớn, không dark panel lặp SH-04, không chuyển thành marketing hero.
- **Desktop canvas:** 1440×960. Header trắng cao 96px, hairline token border; content max 1120px, `x=160..1280`. Text column bên trái, artwork độc lập bên phải; giữ whitespace quanh H1 và CTA.
- **Text column:** x=160, rộng 540px. Eyebrow `160,264,280,20`; H1 `160,312,540,104` (44/52/700, tối đa 2 dòng); paragraph `160,436,520,60` (17/28/400, tối đa 2 dòng); CTA `160,560,224,56`; secondary link hit-area `160,640,180,44`. Ba trạng thái dùng cùng bounds để không layout jump.
- **Artwork stage:** vùng phải `x=800..1296`, `y=218..720`; halo `880,275,360,360`, group ngưỡng mở `961,336,250,308`, tuyến chấm `816,623,111,3`, node `927.5,609.5,29,29`, cung trang trí `802,218,494,502`. Hình không chứa text, status code, checkmark, khóa, logo hoặc dữ liệu. Cùng art cho ba state để trạng thái do headline/copy/button nói rõ, không chỉ do màu/hình.
- **Header continuity:** mark và wordmark theo SH-01/02; header không thêm menu hoặc account controls.
- **Palette:** page `#F6FAFC`, header `#FFFFFF`, heading `#073B57`, body `#536A7A`, primary `#0B5F8A`, hover `#084968`, soft `#E8F4FA`, accent `#43A5C5` chỉ trang trí, border `#D4E2E9`. Không dùng danger red vì đây là trạng thái truy cập có recovery, không phải lỗi thao tác destructive.
- **Typography:** `Noto Sans, Arial, sans-serif` theo Study handoff; H1 44/52/700; body 17/28/400; eyebrow 13/18/700; button 16/24/600; link 15/22/600. Nếu text dài, wrap trong bounding box; không truncate tiếng Việt.
- **Mobile 390×844:** brand x=24; eyebrow baseline y=116; H1 32/38/700 từ y=142; body 16/25; CTA full width `342×54` tại y=328; home link hit-area `342×44` bên dưới; artwork co còn `209×209` và nằm cuối content. Ở 320px giữ gutter 16px, H1 28/38, body 15/25, controls ≥44px; minh họa co thêm, không ẩn copy/action, không horizontal scroll.

## 4. Element map (12 targets)

Bounds/marker là pixel ở canvas desktop 1440×960. Mỗi element có một hàng `SCREEN.md`; badge 24px trên desktop, 20px trên mobile để không cắt ở gutter. Decorative SVG có semantic `aria-hidden=true`; không focus/click.

| # | Element / state text | Desktop bounds | Style | Semantics / action | Hover/focus/responsive |
|---:|---|---:|---|---|---|
| 1 | Study brand mark | `160,30,38,38` | Ocean square, radius 11; white line glyph. | Anchor tới SH-01 `/`. | Link hit area ≥44px; 2px focus-visible; mobile x=24. |
| 2 | Wordmark `Study` | `210,34,82,30` | Noto Sans 23/30/700 `#073B57`. | Cùng brand anchor, tới SH-01. | Hover/pressed `#084968`; không wrap. |
| 3 | Eyebrow theo trạng thái | `160,264,280,20` | Noto Sans 13/18/700, tracking 0.5px, `#0B5F8A`. | Static section label. | No interaction; stack unchanged on mobile. |
| 4 | H1 state headline | `160,312,540,104` | Noto Sans 44/52/700 `#073B57`; state-specific text from matrix. | H1 duy nhất; no interaction. | 401/403/refresh variants giữ cùng max width; mobile 32/38. |
| 5 | Supporting paragraph | `160,436,520,60` | Noto Sans 17/28/400 `#536A7A`; state-specific. | Paragraph; no API payload/raw detail. | Natural wrap; mobile 16/25, full column. |
| 6 | Primary CTA | `160,560,224,56` | Ocean `#0B5F8A`, white 16/24/600, radius 10px. | 403=`Quay lại`→safe previous route (fallback SH-01); 401/refresh failed=`Đăng nhập lại`→SH-02 with safe `returnTo`. No API mutation. | Hover/pressed `#084968` 140ms; focus ring 2px; mobile width 100%. |
| 7 | Secondary link `Về trang chủ` | `160,640,180,44` | Noto Sans 15/22/600 `#0B5F8A`, underline on hover. | Navigate to SH-01 `/`; no API request. | 44px minimum hit box; visible focus; no layout shift. |
| 8 | Illustration halo | `880,275,360,360` | `#E8F4FA` circle with one diffuse shadow, no gradient. | Decorative, in #12 illustration group. | No input state; scales to about `209×209` at 390px. |
| 9 | Open threshold frame | `961,336,250,308` | 5px arch line `#0B5F8A`, layered paper-white inner plane and ground ellipse. | Decorative; must not look like a locked account. | No hover/focus; scales proportionally. |
| 10 | Interrupted route line | `816,623,111,3` | 3px dotted `#43A5C5`; accent is decorative only. | Decorative route metaphor; not progress/status control. | No hover/focus. |
| 11 | Route stop node | `927.5,609.5,29,29` | Open-circle node with ocean border, soft fill; no check/error glyph. | Decorative end point before threshold. | No hover/focus. |
| 12 | Orbit/accent arcs | `802,218,494,502` | Four sparse line arcs and three small dots in `#43A5C5` at low opacity. | Decorative vector group with halo/frame/path/node. | No hover/focus; scales proportionally at 320px. |

## 5. State, navigation và security

| Event/source | Transition | Screen behavior |
|---|---|---|
| Protected request returns 401 | Expected one coordinated refresh R-X01 | No visible intermediate error if refresh succeeds; retry original request once. |
| Refresh returns 200 | Token rotation succeeds | Return to originally requested safe route; no SH-05 flash. |
| Refresh returns 401 / no usable refresh | `SESSION_REQUIRED` | Render 401 variant; CTA SH-02 carries only allowlisted relative `returnTo`. |
| Protected request returns 403 | `ACCESS_DENIED` | Render 403 variant; do not refresh; CTA returns to safe previous route, fallback SH-01. |
| Refresh returns 403 | Access denied | Use generic 403 wording; no refresh loop or claim about account status. |
| Refresh 500/network/uncertain rotation | `TOKEN_REFRESH_FAILED` design mapping | No automatic repeat; user can proceed to SH-02 or public SH-01. Exact client mapping is `OPEN_DECISION`. |
| User activates brand or home link | Public navigation | SH-01 `/`; do not preserve token in URL. |

Safe-return rules: accept only relative internal routes in the approved allowlist; reject protocol-relative `//`, absolute/external URLs, auth-loop paths (`/login`, `/forbidden`) and malformed values; never include access/refresh token or PII in query. The exact client allowlist and token store are not implemented/source-backed. API #04/refresh 500 branches and API #04 user-missing semantics are not silently converted to 401 in the screen copy.

## 6. Accessibility và quality gates

- H1→paragraph→primary action→secondary link reading and tab order. The illustration is `aria-hidden`; no automatic focus or refresh retry after entering state view.
- H1/copy/status describe the state in text; color and illustration never carry the only meaning. No role, status, token, raw response or trace ID on the page.
- Text contrast ≥4.5:1; meaningful icon/boundary ≥3:1; CTA/link hit area ≥44px; focus ring visible and not clipped; reduced motion removes nonessential entrance effects.
- Export a clean and annotated image for each desktop state; each annotated image has exactly markers #1–#12. Also render mobile 390×844 variants to check all three headlines/body/controls without clipping.
- Final review checks: state copy accuracy, safe navigation labels, token palette, exact bounding boxes, marker overlap, Vietnamese glyph rendering, desktop/mobile reflow, duplicate refresh prevention wording, and ZIP member integrity.

## 7. Related screens and open decisions

| Related screen/route | Link condition |
|---|---|
| SH-02 `/login` | 401 or terminal refresh failure; preserve safe relative return only. |
| SH-01 `/` | Explicit secondary public escape and fallback when no previous safe route exists. |
| Previous safe route | 403 primary action only; use app router history/allowlist after implementation, not arbitrary `window.location` target. |

Open: Study Web auth persistence/interceptor/allowlist are absent; R-X01 is outside API catalog; SH-05 mapping for refresh 500/network is not specified; Mentor/Admin role bootstrap is blocked because API #04 only accepts Student. No child screens are listed; state variants stay at SH-05 root.
