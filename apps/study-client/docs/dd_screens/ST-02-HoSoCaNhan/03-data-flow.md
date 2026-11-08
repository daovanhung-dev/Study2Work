# ST-02 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### Luồng dự kiến theo AC-02/AC-11 và inventory

1. User tới route `/student/profile` sau SH-02 hoặc qua Student navigation. Route/query/user ID chưa có app source; không cho route tự mang PII.
2. Client xác nhận session có token và role Student theo auth state đã được duyệt. Role guard client chưa tồn tại để xác minh; backend guard vẫn bắt buộc.
3. Hiển thị loading state cho profile area và gọi #04 `GET /api/v1/users/me` với đúng một header `Authorization: Bearer <jwt>`, không body/path/query. Catalog lặp ký hiệu auth nhưng route thực tế chỉ nhận một header.
4. Backend decode access JWT theo thuật toán/key/issuer/audience/expiry hiện hành; yêu cầu claims bắt buộc, `type=access`, `sub` dạng chuỗi ID dương và `roles` là list string có `STUDENT` sau chuẩn hóa. Guard chạy trước DB access.
5. Backend query một row `users` theo `id` từ `sub`, lấy safe profile columns. Không lọc account status, không so role từ row với JWT role. Nếu row không có, current source trả 401.
6. Nếu thành công, map `UserProfile`, serialize datetime và trả envelope. Dự kiến UI chỉ map trường được duyệt; inventory nêu avatar/email/role/status nhưng chưa có loaded layout. `bio`/permissions không có trong current response. Không thể xác nhận cache, TTL, merge với profile từ login hoặc invalidation.
7. Chỉ điều hướng sang ST-03 sau khi user activate edit action có contract; hiện button disabled và chưa được mở. Chi tiết route/form/upload/save thuộc ST-03, không nằm trong ST-02 scope.

### Luồng hiện tại có thể xác nhận

- Study Web không có application source, package, router, entrypoint hoặc API client trong checkout.
- `screen.png` là trang gần như trống: header/footer hiện diện, body không có profile/card. `code.html` có page heading và static sign-in card, dùng prompt “Vui lòng đăng nhập...”, login links `href="#"`, và edit button disabled.
- HTML không có fetch/XHR/Axios, không có route binding, session read, data mapping, loading/error transition hay event handler. Header/footer `data-path` là metadata string, không phải điều hướng runtime.
- API #04 có current source; test source hiện hữu được đọc nhưng không chạy. Không có UI/API end-to-end, browser production hay live-schema verification.

### Trích từ DD nguồn: D. Đặc tả sự kiện và xử lý dữ liệu

### Ma trận sự kiện

| Event ID | Tên / loại | Phần tử kích hoạt | Hiện trạng |
|---|---|---|---|
| `ST02-EV-01` | Mở route và nạp profile — `Load` | `/student/profile` route, không có DOM handler | Expected GET #04; current Study Web không route/fetch. |
| `ST02-EV-02` | Header brand/navigation — `Click/Anchor` | #1–#2 | `href="#"`; chỉ fragment navigation, không chuyển Screen ID. |
| `ST02-EV-03` | Mở đăng nhập — `Click/Anchor` | #3 hoặc #7 | `href="#"`; không có SH-02 route/session state. |
| `ST02-EV-04` | Chỉnh sửa hồ sơ — `Click` | #8 | Disabled; thao tác không được browser phát; ST-03 không được mở. |
| `ST02-EV-05` | Footer brand/navigation — `Click/Anchor` | #9–#10 | `href="#"`; destinations chưa được map. |

### `ST02-EV-01` — Mở route và nạp profile

- **Input:** không có request input từ user; expected `Authorization` header lấy từ auth/session state. Không có `userId` route/body/query; current page không có input control.
- **Precondition:** route/client được triển khai và session có Student access token. Nếu chưa có token hoặc không phải Student, expected 401/403 handling theo catalog; Study Web session guard chưa tồn tại.
- **Xử lý phía client dự kiến:** resolve route → xác nhận session/role bằng contract đã duyệt → tạo GET #04 một lần theo cache policy đã chốt → chờ response → map approved fields và state. Inventory nói cache profile nhưng không cho TTL, nguồn invalidation hay xử lý duplicate call; không phát minh các giá trị này.
- **Request:** `GET /api/v1/users/me`, header `Authorization: Bearer <jwt>`, không query/path/body. Catalog lặp notation auth nhưng current route nhận một header.
- **Current server sequence:** shared decoder kiểm JWT theo configured algorithm/key, issuer/audience, expiration và required claims; helper kiểm `sub` là user ID số dương, `roles` là list string và role Student; role denial xảy ra trước DB. Query `CURRENT_USER_PROFILE` SELECT `users.id/full_name/email/role/avatar_url/phone/status/created_at/updated_at` theo `id=:user_id`, `LIMIT 1`. Không lấy password_hash; không filter `status` hoặc compare row role. `UserProfile` extra-ignore, `avatar_url`/`phone` nullable, `status` bắt buộc.
- **Success:** HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, message `Profile retrieved.`, `data=UserProfile`, `meta={}`, `traceId`; model dumps timestamps as JSON datetime strings. No server-side mutation. UI field mapping/ready layout is blocked because no authenticated design state exists.
- **Errors:** missing/malformed Bearer, invalid/expired token, invalid claims, or missing user row → HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`; valid claims without `STUDENT` → 403 `DESIGN_ACCESS_DENIED`; JWT configuration/query/model mapping failure → 500 `DESIGN_INTERNAL_ERROR`. SQLAlchemy query error rolls back; missing row and model mapping failure do not run rollback. Error data uses common response helper defaults; no raw DB/token detail is exposed.
- **Unsupported/contract gaps:** catalog/AC-02 claim wording `user_id`/`role` differs from source `sub`/`roles`; AC-02 permissions absent; optional `bio` absent; missing-user 401 current mapping is not separately explained by catalog; role/status DB freshness is not enforced. Do not create an alternate response mapping or UI fix here.
- **Current UI result:** there is no request/event. Rendered HTML displays static sign-in card; source PNG contains a blank body. A login copy does not establish that the user is unauthenticated, and no 401/403 response is rendered.

### `ST02-EV-02` — Header brand/navigation

- **Input:** click logo or one of four navigation anchors.
- **Precondition/current DOM:** link exists; all use `href="#"`; active profile class is static.
- **Sequence/output:** browser fragment navigation only; `data-path` is not bound to a router; no request or profile state mutation. Destination screen, role guard and history behavior cannot be inferred.

### `ST02-EV-03` — Login links

- **Input:** click header login (#3) or card login CTA (#7).
- **Current behavior:** both anchors use `href="#"` and `data-path="dang-nhap"`; no API call, login route, `returnTo` or session transition exists in HTML.
- **Expected:** could hand off to SH-02 under an approved safe-return contract, but route preservation and post-login redirect are not wired here. Do not claim login succeeded or call API #03 from this static page.

### `ST02-EV-04` — Edit profile disabled button

- **Input:** attempted click on #8.
- **Current behavior:** native disabled button with no event handler; browser does not activate it, call API #13/#14 or navigate to ST-03.
- **Expected ownership:** enable/edit flow belongs to ST-03 only after profile/avatar request-response mapping is resolved. No upload/update action is part of this event.

### `ST02-EV-05` — Footer navigation

- **Input:** click footer brand or one of four footer links.
- **Current behavior:** anchors use `href="#"`, `data-path` values `trang-chu`, `khoa-hoc`, `dieu-khoan-dich-vu`, `chinh-sach-bao-mat`; no route/document destinations or app link behavior exist.
- **Output:** no backend action; browser fragment navigation only.

### API #04 contract/source matrix

| Hạng mục | Catalog/AC/API DD | Current source |
|---|---|---|
| Endpoint/auth | GET `/api/v1/users/me`; Bearer JWT; role Student; no path/body/query. | Registered GET route accepts one Authorization header; `validate_current_user_request(..., role="STUDENT")`; no path/query/body. |
| Input claims | Catalog does not fix JWT claims; AC-02 diagram says `user_id`/`role`. | #03 creates claims `sub`, `roles`, `type`, `jti`, `iat`, `exp`, `iss`, `aud`; #04 consumes `sub` and `roles`. |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<UserProfile>`. | HTTP 200, safe profile fields listed in §C, no permissions or bio; direct current source-backed. |
| Auth errors | Catalog/diagram: 401 and 403. | 401 for missing/bad token or absent user row; 403 for no Student token role. Role denial occurs before query. |
| System error | 500 `DESIGN_INTERNAL_ERROR`. | Decoder configuration, DB query, or model validation failures map to safe 500; SQLAlchemy exception rolls back. |
| DB effect | Read current user profile. | Single `users` SELECT by `users.id`; no joins/writes/external service. Candidate schema is not live verification. |
| Missing profile fields | `bio` optional at catalog; AC-02 says permissions. | Neither is selected, modeled or serialized by API #04. |

API #04 DD status is `Draft — Needs Confirmation`. Checked-in `infra/postgres/study-server/DB.sql` defines `status VARCHAR(20) DEFAULT 'ACTIVE'` without `NOT NULL`, while current `UserProfile.status` requires a string. A null status therefore causes source model validation to map an otherwise found row to 500; the deployed schema is not verified.

### Trích từ DD nguồn: E. Ma trận trạng thái, điều hướng và khả năng tiếp cận

| State | Entry condition / source | Current visual or required treatment | Exit |
|---|---|---|---|
| `INITIAL` | Route resolution, before fetch | No current runtime state. | `LOADING` or auth block after implementation. |
| `LOADING` | Expected #04 request pending | Inventory expects loading; no skeleton/spinner design exists. | `READY`/`UNAUTHORIZED`/`FORBIDDEN`/`SERVICE_ERROR`. |
| `READY` | HTTP 200 and validated profile | No ready-state screenshot/layout. Only the field allowlist/source map is known. | Navigation to ST-03 if separately enabled by approved contract. |
| `UNAUTHENTICATED` | Missing/invalid/expired Bearer or missing user row (current #04 → 401) | HTML static sign-in fallback resembles this but does not prove an actual auth check. | Login/recovery route behavior unresolved; do not infinite-refresh. |
| `FORBIDDEN` | Valid token role does not include Student (current #04 → 403) | No current 403 UI. Do not treat as login success or refresh forever. | Safe prior route/SH-05 mapping requires client policy. |
| `SERVICE_ERROR` | API 500/network/timeout | API 500 exists; current mock has no error display/retry. | Retry is read-safe but retry limits/copy not specified. |
| `EDIT_DISABLED` | Static HTML initial | Edit button disabled with “Tạm khóa”. | No transition in ST-02. |

### Điều hướng và dữ liệu handoff

- **SH-02 → ST-02:** AC-02 says login returns token/profile and routes by role; F01 says Student then calls #04. Current #03 success already returns a basic profile with tokens, and #04 returns the base profile again. Purpose of second read, freshness, cache source and role routing are open. Mentor/Admin must not call Student `/users/me`; G-02 requires role profile/bootstrap policy.
- **ST-01 → ST-02:** listed as a possible dashboard link, but ST-01/API dashboard routes are not wired. No origin state can be presumed.
- **ST-02 → ST-03:** relation is listed; current edit button is disabled and no route is wired. Do not route from this screen until ST-03 authoring/contracts permit it.
- **Refresh/deep link/back:** route is only proposed; no Study Web router. Login return path must be safe relative internal route per global rule; no token or profile PII in URL. Exact history/cache behavior is unresolved.

### Accessibility, privacy and responsiveness

- `code.html` uses semantic heading, anchors and a native disabled button; button target is at least 44px high. The logo/links have text; decorative icon names are not app-level API data.
- Current screen is desktop 1280×1078. HTML contains responsive utility classes, but no tested app at mobile widths. This render is a static HTML preview only.
- Follow `.agents/web-study/design.md` for future focus-visible, keyboard order, contrast, 44×44 icon targets and 320px reflow. Do not treat classes or render as accessibility audit.
- Profile is sensitive personal data. Restrict to authenticated Student, do not expose credential fields, do not place PII/token in URL/log, and avoid confirming other-user existence through response content. Current endpoint emits generic 401 for missing user row and safe envelope errors.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #4 với Bearer; cache profile; profile có thể thiếu bio.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ST-02](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/ST-02.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
