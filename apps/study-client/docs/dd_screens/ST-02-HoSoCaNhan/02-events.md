# ST-02 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-02-EV-001` | `Source heading` / Ma trận sự kiện | See source event detail below |
| `ST-02-EV-002` | `ST02-EV-01` / `ST02-EV-01` — Mở route và nạp profile | See source event detail below |
| `ST-02-EV-003` | `ST02-EV-02` / `ST02-EV-02` — Header brand/navigation | See source event detail below |
| `ST-02-EV-004` | `ST02-EV-03` / `ST02-EV-03` — Login links | See source event detail below |
| `ST-02-EV-005` | `ST02-EV-04` / `ST02-EV-04` — Edit profile disabled button | See source event detail below |
| `ST-02-EV-006` | `ST02-EV-05` / `ST02-EV-05` — Footer navigation | See source event detail below |
| `ST-02-EV-007` | `Source heading` / API #04 contract/source matrix | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

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

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
