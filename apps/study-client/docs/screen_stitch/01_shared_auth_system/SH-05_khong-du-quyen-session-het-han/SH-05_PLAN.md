# SH-05 Plan — Không đủ quyền / phiên hết hạn

> **Trạng thái kế hoạch:** `EXECUTED / RE-AUDITED / STATIC_REVIEWED` · **Phiên:** chỉ xử lý SH-05 · **Route trong inventory:** `/forbidden` (đề xuất; chưa có Study Web router trong checkout).

## 0.1. Re-audit plan — 2026-11-07

- **Expected behavior:** `list_screen.md` §1.2 requires at most one refresh/retry for a 401 flow and single-flight coordination for concurrent requests; the SH-05 row allows one R-X01 attempt and prohibits refresh after 403. Treat single-flight as a design requirement, not an unresolved product choice.
- **Current behavior:** Current Study Server source wires API #04 and R-X01, but Study Web editable source/package/router is absent. No client implementation evidence exists for single-flight, token persistence, request replay, timeout or ambiguous token-rotation outcomes. API #04 still maps invalid/missing auth and missing profile to the same 401.
- **Artifact decision:** Preserve `screen.png` and `code.html` (current SHA-256 values recorded in this session's worklog); retain the existing 11-marker annotation if mapping/bounds checks pass. No image/marker edits are planned.
- **Planned DD delta after this plan review:** Add an A–F crosswalk to the existing DD sections; make the single-flight/max-one retry requirement explicit in `SH05-EV-03`; keep its client implementation status `UNWIRED`; narrow the session blocker to missing client source, persistence/security and ambiguous-outcome decisions; keep safe-return fallback unresolved and describe any public route only as an unselected candidate. Then update the global tracker and run focused static checks. Do not begin another Screen ID.

## 1. Mục tiêu và nguồn

- Mô tả state view cho lỗi xác thực `401` và lỗi phân quyền `403`; không hiển thị dữ liệu bảo vệ và không tự gán quyền.
- Nguồn dự kiến: dòng SH-05 trong `../../../list_screen.md`; `screen.png` (1600×1280, trạng thái mặc định 403); `code.html` (prototype có bộ chuyển 401/403); AC-02, AC-11; API #04 và runtime refresh R-X01; `.agents/web-study/design.md`.
- `screen.png` và `code.html` là tài sản thiết kế. `apps/study-client/src/` không có trong checkout, nên route, auth interceptor, storage và hành vi UI hiện tại đều `NOT_FOUND`.
- `code.html` mô phỏng state bằng JavaScript cục bộ. Hàm refresh chỉ dùng `setTimeout`, không gửi HTTP; JSON, reason code và trace ID trong mock không phải response backend.

## 2. Expected behavior và current behavior

| Hạng mục | Expected behavior theo inventory/AC | Current source evidence |
|---|---|---|
| Route | `/forbidden` là route đề xuất; nhận 401/403 hoặc direct navigation an toàn. | Chưa có frontend source/router để xác minh. HTML ghi `/forbidden`; không chứng minh route chạy được. |
| 401 | Phân biệt 401 với 403; theo shared auth rule, tối đa một refresh/retry cho flow 401 và single-flight cho request đồng thời; không suy mọi 401 là token hết hạn. | API #04 trả `401 DESIGN_AUTHENTICATION_REQUIRED` cho thiếu/sai Bearer/JWT hoặc claims không hợp lệ, đồng thời cũng map profile không tồn tại thành 401. Response không phân biệt nguyên nhân. Client chưa có code để thực hiện/kiểm chứng single-flight hoặc retry. |
| 403 | Hiển thị quyền bị từ chối; không gọi refresh để đổi role; không tiết lộ dữ liệu/role nội bộ; đưa ra đường lui an toàn. | API #04 yêu cầu role `STUDENT`; role khác trả `403 DESIGN_ACCESS_DENIED`. |
| Refresh | Chỉ dùng opaque `refresh_token` còn hợp lệ; shared auth rule yêu cầu tối đa một refresh/retry mỗi flow 401, single-flight cho request đồng thời và không refresh sau 403. | R-X01 `POST /api/v1/auth/refresh` tồn tại trong `app/api/v1.py`; lookup, revoke token cũ + insert hash token mới trong một transaction. Source/test không chứng minh client single-flight, replay hay xử lý timeout; client integration chưa có. |
| Error details | Dùng HTTP status, `businessCode`, message an toàn, `traceId` thật từ body/header; không tự sinh reason/timestamp. | Backend envelope là `{success,businessCode,message,data,meta,traceId}` và header `X-Trace-Id`. Mock hiện dùng `{status,businessCode,message,traceId,timestamp}` cùng mã giả. |
| Điều hướng | Login theo SH-02; sau 403 chỉ quay về route nội bộ an toàn theo allowlist; fallback khi direct-entry phải được xác nhận. | HTML dùng `/sh-02-login` và `/sh-01-dashboard`; list_screen đề xuất `/login` và `/`. Study Web router chưa có để xác minh route, `returnTo` hay fallback. |

**DISCREPANCY quan trọng:** API #04 không cung cấp reason code phân biệt access token hết hạn với profile không tồn tại. Inventory cho phép refresh sau 401, nhưng chưa có client policy cho trường hợp refresh thành công rồi request #04 vẫn trả 401; không suy rằng refresh sẽ sửa profile thiếu.

## 3. Kế hoạch element và marker

Ảnh chú thích sẽ đánh số **11 vùng UI nhìn thấy trong ảnh mặc định 403**. Mỗi marker đặt sát mép vùng tương ứng, tránh che chữ/nút. Các controls chỉ xuất hiện trong state 401 được mô tả trong DD dưới vùng hành động động; chúng không được đánh dấu trên ảnh 403 khi đang ẩn.

| Marker | Element ID | Vùng element / loại | Vị trí dự kiến trên ảnh 1600×1280 | Ghi chú |
|---:|---|---|---|---|
| #1 | `SH05-EL-01` | Thanh metadata hand-off (`aside`) | Mép trái thanh đầu trang | Công cụ hand-off của prototype, chưa xác nhận là UI production. |
| #2 | `SH05-EL-02` | Nút chọn state `HTTP 403` (`button`, selected mặc định) | Mép trên nút tab trái | Điều khiển demo; production lấy state từ response. |
| #3 | `SH05-EL-03` | Nút chọn state `HTTP 401` (`button`) | Mép trên nút tab phải | Điều khiển demo; production lấy state từ response. |
| #4 | `SH05-EL-04` | Tóm tắt state: icon, badge HTTP/endpoint, tiêu đề, mô tả (`section`) | Góc trên trái thẻ chính | Nội dung và badge thay đổi theo 401/403. |
| #5 | `SH05-EL-05` | Banner giới hạn role API #04 (`notice`) | Góc trên trái banner xanh nhạt | Hiện API #04 chỉ nhận role STUDENT; nội dung mock phải dùng wording/backend code thực. |
| #6 | `SH05-EL-06` | Lưới chẩn đoán: reason, recovery, refresh constraint, policy (`group/card`) | Góc trên trái lưới | Các giá trị reason/strategy hiện trong HTML là mock, không phải response field. |
| #7 | `SH05-EL-07` | Vùng hành động phục hồi (`group`): link an toàn 403; login + refresh 401 | Mép trái hàng action cuối thẻ chính | 403 và 401 có actions khác nhau; refresh control đang ẩn ở ảnh gốc. |
| #8 | `SH05-EL-08` | Nút “Sao chép mã phiên hỗ trợ” (`button`) | Mép trái nút cạnh action chính | Hiện gọi `copyTraceId()`; nhãn không khớp dữ liệu thực được copy. |
| #9 | `SH05-EL-09` | Thẻ phản hồi HTTP/Trace: trace, status, envelope, ghi chú (`card`) | Góc trên trái thẻ phải phía trên | Chỉ hiển thị dữ liệu lỗi đã chuẩn hóa; không render stack trace. |
| #10 | `SH05-EL-10` | Nút icon sao chép Trace ID (`button`) | Mép phải hàng Trace Identifier | Hiện 40×40px và thiếu target tối thiểu 44×44px theo design guide. |
| #11 | `SH05-EL-11` | Thẻ quy chuẩn hand-off và ba mục policy (`card/list`) | Góc trên trái thẻ phải phía dưới | Nội dung định hướng kỹ thuật; cần xác nhận phần nào là UX production. |

## 4. Event plan

| Event ID | Trigger | Dữ liệu vào | Kế hoạch xử lý / kết quả |
|---|---|---|---|
| `SH05-EV-01` | Nhận response xác thực từ request được bảo vệ | HTTP status, `businessCode`, message an toàn, `traceId` body/header, route hiện tại | Chuẩn hóa response; 401 → kiểm tra recovery policy, giữ nguyên rằng API #04 cũng dùng code này khi profile thiếu; không tự gọi là hết phiên. `403 DESIGN_ACCESS_DENIED` → state từ chối quyền và không refresh. Không ánh xạ lỗi 5xx/mạng thành 403. |
| `SH05-EV-02` | Click hai nút chọn 403/401 trong `code.html` | `mode = 403 | 401` | Chỉ là prototype preview: đổi badge/copy/action và response mẫu. Không ghi nhận đây là runtime event; production không nhận state từ toggle. |
| `SH05-EV-03` | Auth manager xử lý 401 và phối hợp refresh giữa request đồng thời | Opaque `refresh_token` từ phiên trước; request gốc; per-flow retry marker và single-flight coordinator | `list_screen.md` §1.2 yêu cầu tối đa một refresh/retry cho flow 401 và single-flight cho request đồng thời; client source chưa có. Thiếu refresh token thì không gọi R-X01 và đi theo SH-02 flow. Thành công: cập nhật cặp token theo persistence đã duyệt rồi chỉ retry request an toàn tối đa một lần. Không kết luận 401 ban đầu luôn do access token hết hạn; 401 lặp lại từ #04 cần xử lý theo policy profile-missing. 403 không refresh; 5xx/network/timeout không chứng minh token invalid và rotation outcome có thể mơ hồ. Prototype chỉ giả lập thất bại sau 1.2 giây. |
| `SH05-EV-04` | Click “Đăng nhập lại” ở state 401 | Route login SH-02; `returnTo` nội bộ nếu có | Điều hướng đến route login đã cấu hình (inventory đề xuất `/login`), chỉ giữ relative route trong allowlist; không đưa access/refresh token hoặc PII vào URL. |
| `SH05-EV-05` | Click đường lui sau 403 | Route gọi trước đó hoặc public safe route | Điều hướng về route nội bộ an toàn nếu allowlisted; fallback public route cần được chốt. HTML `/sh-01-dashboard` chưa khớp route đề xuất `/`; không dùng path prototype như contract. |
| `SH05-EV-06` | Click copy Trace ID | `traceId` thật từ response body hoặc `X-Trace-Id` | Sao chép duy nhất trace ID; không có ID thì disable/ẩn action. Clipboard success/failure phải có status accessible; hiện prototype không bắt lỗi Promise. Đổi nhãn “mã phiên hỗ trợ” thành “Trace ID” nếu action này được giữ. |
| `SH05-EV-07` | Click refresh trong preview prototype | Biến cục bộ `refreshAttempts`; không có token hoặc HTTP request | Chỉ `code.html`: lần đầu tăng counter, disable/đổi label rồi sau 1.2 giây hiển thị kết quả giả lập hết hạn; click thêm bị giới hạn. Không gọi R-X01, không cập nhật session và không phải runtime evidence. |

## 5. API và dữ liệu cần đối chiếu khi soạn DD

### API #04 — GET `/api/v1/users/me`

- Runtime route: `apps/study-server/app/api/v1.py` → `get_current_user()` → `validate_current_user_request(role="STUDENT")` → `find_current_user()` → `CURRENT_USER_PROFILE` → `UserProfile` → response envelope.
- Request: `Authorization: Bearer <access JWT>`; không có path, query hoặc body. Role hợp lệ là `STUDENT`.
- Thành công: HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, data gồm `id`, `full_name`, `email`, `role`, `avatar_url?`, `phone?`, `status`, `created_at`, `updated_at`. `bio` không được source hiện tại trả.
- Lỗi: 401 `DESIGN_AUTHENTICATION_REQUIRED` cho thiếu/sai Bearer/JWT/claims hoặc profile không tồn tại; 403 `DESIGN_ACCESS_DENIED` khi role không phải Student; 500 `DESIGN_INTERNAL_ERROR` cho lỗi DB/mapping. Body dùng envelope chuẩn và response có `X-Trace-Id`; cùng một mã 401 được dùng cho các nguyên nhân trên.
- Side effect: read-only query; không commit. Không dùng user/profile data trong SH-05 để render nội dung được bảo vệ.

### Runtime support R-X01 — POST `/api/v1/auth/refresh`

- Route ngoài danh mục API V1: `RefreshRequest` JSON `{ "refresh_token": string }`; không gửi token qua URL. Route source không khai báo Bearer authorization.
- Thành công: HTTP 200, `DESIGN_RESOURCE_RETRIEVED`; `data` có profile allowlist và token pair mới (`access_token`, `refresh_token`, thời hạn theo payload). Server hash token lưu DB, revoke token cũ và insert token mới trong cùng transaction.
- Lỗi: 401 `DESIGN_AUTHENTICATION_REQUIRED` nếu token thiếu/không hợp lệ/hết hạn/đã dùng; 403 `DESIGN_ACCESS_DENIED` nếu tài khoản không ACTIVE; 422 body sai; 500 lỗi nội bộ an toàn.
- Đây là backend capability hiện có, chưa phải bằng chứng client gọi endpoint hoặc có secure token persistence. Chưa có client storage/CSRF/retry implementation trong checkout; không khẳng định hành vi single-flight hay replay phía client.

## 6. Blocker và điểm cần quyết định

1. **`BLOCKER: CLIENT_SOURCE_NOT_FOUND`** — không có Study Web router, auth interceptor, session storage hoặc UI runtime để xác minh route/event; `dist`/`node_modules` không chứng minh source runtime.
2. **`BLOCKER: CLIENT_SESSION_IMPLEMENTATION`** — inventory đã quy định single-flight và tối đa một lần refresh/retry; Study Web source không có để implement/verify quy tắc này. Token persistence, CSRF/XSS mitigation, safe replay eligibility, timeout/ambiguous rotation outcome handling và session cleanup vẫn cần owner decision.
3. **`BLOCKER: 401_CAUSE_AND_RECOVERY`** — API #04 map missing profile và invalid/expired auth thành cùng 401/code/message; policy sau refresh thành công nhưng #04 tiếp tục 401 chưa có.
4. **`BLOCKER: USER_FACING_CONTENT_AND_FALLBACK`** — ảnh/code gồm preview toggles, technical diagnostics, raw JSON và handoff rules; chưa có quyết định phần nào là UI người dùng. `/login`, `/`, previous-safe-route và direct-entry fallback chưa được router/product xác nhận.
5. **`DISCREPANCY: MOCK_ERROR_ENVELOPE`** — code.html dùng `AUTHZ_STUDENT_REQUIRED`, `AUTHN_TOKEN_EXPIRED`, `status`, `timestamp`; backend trả `DESIGN_ACCESS_DENIED` / `DESIGN_AUTHENTICATION_REQUIRED` theo envelope `success`, `businessCode`, `message`, `data`, `meta`, `traceId`.
6. **`DISCREPANCY: ROUTE_TARGETS`** — HTML dùng `/sh-01-dashboard` và `/sh-02-login`; inventory chỉ đề xuất `/` và `/login`.
7. **`DISCREPANCY: SYNTHETIC_DIAGNOSTICS`** — `ROLE_NOT_AUTHORIZED_FOR_STUDENT_SCOPE`, `ACCESS_TOKEN_EXPIRED_OR_INVALID`, trace ID `tr_*` và timestamp mẫu không được backend cung cấp.
8. **`UX/A11Y`** — nút copy icon hiện 40×40px; copy action trên prototype không xử lý lỗi clipboard; text reason dài bị cắt và JSON tràn ngang. `.agents/web-study/design.md` yêu cầu control 44×44px, focus visible, responsive reflow và không thêm remote font.
9. **`NOT_FOUND: BD/BRD`** — không có BD/BRD canonical trong checkout; không suy diễn wording/reason nghiệp vụ ngoài API/AC/user requirement.
10. **`DEPENDENCY: SH02_LOGIN_HANDOFF`** — inventory G-14 ghi API #03 catalog `201/UserProfile-only` khác source `200/profile+tokens`; SH-05 không được tự giải quyết response parser của SH-02.

## 7. Tiêu chí nghiệm thu SH-05

- Tạo đúng `screen_annotated.png`; giữ nguyên `screen.png` và `code.html`; ghi hash nguồn trước/sau.
- Có 11 marker nhìn rõ theo danh sách trên; mỗi marker `#n` ánh xạ một Element ID duy nhất trong SH-05.md và SH-05_markers.json; hidden 401 controls được mô tả là state-dependent, không gắn marker giả vào ảnh 403.
- DD tách riêng 401/403, prototype/current source/target behavior; mọi API field, business code, route và response bám source hoặc đánh dấu blocker/discrepancy.
- Có input → validation/permission → API/nội bộ → response mapping → state update → outcome/exceptions cho từng event; không coi HTML timer là API call.
- Có ma trận state/loading/error/refresh failure/offline/copy failure và điều kiện điều hướng; mọi `returnTo` an toàn.
- `DD BLOCKED` đến khi chốt production content/state mapping, 401 recovery policy (kể cả profile-missing/repeated 401), token persistence/refresh outcome, safe-route fallback và SH-02/G-14 login handoff; `IMPLEMENTATION BLOCKED` do thiếu Study Web source và các quyết định trên; `RUNTIME NOT VERIFIED`.

## 8. Kết quả phiên SH-05

- Tạo `SH-05.md`, `SH-05_markers.json` và `screen_annotated.png`; giữ nguyên `screen.png` và `code.html`.
- Rà soát 11 marker, 7 event, API #04 và R-X01; link/API claims tách source-backed, prototype-only và blocker.
- Static audit: source image and `code.html` hashes unchanged; original/annotated PNG both 1600×1280; 11 markers map 1:1 in order to 11 Element definitions; seven event definitions and all 26 relative Markdown links pass static checks; `git diff --check` passes for the tracked tracker update. Tests/runtime were not run.
- Trạng thái sau static review: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Phiên kế tiếp: SH-06. Không xử lý SH-06 trong phiên SH-05.

## 9. Kết quả re-audit — 2026-11-07

- Cập nhật DD để phản ánh `list_screen.md` §1.2: single-flight cho request đồng thời và tối đa một refresh/retry mỗi flow 401 là expected behavior; Study Web client vẫn `UNWIRED`, không phải đã xác minh.
- Thêm ma trận A–F; giữ blockers về nguyên nhân 401/profile thiếu, session persistence/security, ambiguous rotation outcome, safe-return fallback, production UI composition và SH-02/G-14.
- Static audit pass: 11 marker theo thứ tự, ID duy nhất, 11/11 map với element rows; center/target đều trong bounds; hai PNG khớp kích thước JSON; 7 events có trigger/input/precondition/process/outcome/exception; A–F và local links đầy đủ; visual annotation đã xem.
- SHA-256 giữ nguyên: `screen.png` `f13f4da1e7717ccafbf93155af94e526e8a5f865d63e207c21165118c16cd23f`; `code.html` `cd0f2cb849d8a39aae842c08f5602fc24718b2d34e9f446d56041c1017b8ad7a`.
- Không chạy application tests, Study Web runtime, deployment hoặc live DB checks. Kết quả SH-05: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. SH-06 là ứng viên cho phiên riêng.
