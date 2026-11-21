# SH-05 — Không đủ quyền / session hết hạn · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `SH-05` |
| Module | Shared / Auth / System |
| Route | `/forbidden` — đã khai báo trong `shared.route.ts`; runtime chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | SH-05 hoàn thiện 100% theo rubric tĩnh UI/UX/logic/API trong phạm vi #04 401/403 recovery và safe return; focused tests pass; browser/runtime is not verified. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.4 / 2026-11-21 |
| Nguồn đối chiếu | [SH-05.md](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05.md), [SH-05_PLAN.md](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05_PLAN.md), [SH-05_markers.json](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Phân biệt 401 (hết hạn/thiếu token), 403 (không đủ quyền), bảo toàn redirect an toàn.
- In-scope: For Student API #04 only, HTTP 401 triggers one R-X01 refresh and one #04 retry; 403 does not refresh; a second 401 ends the local session and routes through SH-05. Preserve only a validated internal return route, with `/` fallback.
- Out-of-scope: Automatic refresh/replay for other APIs, persistence of credentials and live deployment/runtime verification.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-02,AC-11 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Phân biệt 401 (hết hạn/thiếu token), 403 (không đủ quyền), bảo toàn redirect an toàn. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #04
- Liên kết màn hình dự kiến: [SH-02](../SH-02-DangNhap/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | 401/403/token-refresh-failed |
| Current source | Worklog/context Study Web | `/forbidden` route, #04 error handoff, 401/403 rendering and trace display are source-wired; runtime not verified |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [SH-05 source screen.png](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/screen_annotated.png))
- Luồng hiện tại: #04 401 → R-X01 once → retry #04 once; refresh or retry failure ends the session and routes to SH-05. #04 403 skips refresh and routes to SH-05. Safe return is an internal path only; invalid values fall back to `/`.
- Priority: P0; source behavior and safe-return branches are covered by focused tests; runtime not verified.

## 7. Reconciliation and implementation evidence — 2026-11-21

- SH-05 static implementation is complete under the repository's UI/UX/logic/API rubric. The policy is limited to the Student #04 read; no refresh occurs for 403 or unrelated APIs.
- Tests cover one refresh plus one retry, no refresh for 403, second-401 session end, safe return and fallback. Browser/deployment runtime remains `NOT VERIFIED`.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-16 — Cập nhật source status: Study Web Angular/router và SH-02/SH-03 tồn tại; SH-05 route, error-context handoff và Shared/Student session vẫn chưa được wire.
- 2026-11-20 — SH-05 `/forbidden` route và #04 401/403 error handoff được wire; cập nhật current-source state và các recovery/fallback gaps.

## Trạng thái và ranh giới bằng chứng

# Tài liệu thiết kế chi tiết màn hình — SH-05 Không đủ quyền / phiên hết hạn

## Current source implementation (2026-11-21)

- Source status: `PARTIAL SOURCE-WIRED / RUNTIME NOT VERIFIED`. `/forbidden` is registered under `shared.route.ts`. `StudentApiService` routes only `GET /users/me` (API #04) HTTP 401/403 responses with an allowlisted, serializable error state. Other statuses and malformed/mismatched envelopes are not sent to this page.
- `StudentSessionService` keeps credentials in memory and proactively refreshes when local access-token expiry is reached before a request. For exact API #04 only, a server-issued 401 triggers one R-X01 refresh and one #04 replay. Refresh/replay failure ends the Student session and routes to SH-05. A 403 never refreshes.
- `SH05Page` validates route state, shows distinct 401/403 headings, renders only a safe message and non-conflicting body/header trace ID, and provides a safe internal back destination or `/` fallback. A 401 also offers `/login`. Direct entry without valid state shows a neutral no-context state.
- Focused tests cover the refresh/replay limit, 403 behavior, terminal 401 and safe destinations. Browser/deployment runtime remains unverified.

The source DD excerpts below retain their original target requirements and source snapshot. Current behavior is listed above and should not be inferred from older `IMPLEMENTATION BLOCKED` statements in those excerpts.

> **Mã màn hình:** SH-05 · **Loại:** state view · **Tác nhân:** khách chưa xác thực hoặc người dùng đã xác thực nhưng không có quyền phù hợp
> **Route đề xuất:** `/forbidden` · **AC:** AC-02, AC-11 · **API catalog:** #04 · **Runtime hỗ trợ:** R-X01
> **Trạng thái nguồn gốc:** At conversion time, `DD BLOCKED` because 401 recovery and prototype composition were unresolved, and SH-05 had no route/error-context integration. Current implementation status is recorded above.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan

SH-05 là state view dùng cho lỗi xác thực (`401`) hoặc từ chối quyền (`403`). View không tự gọi API hồ sơ để dựng trang, không render dữ liệu được bảo vệ và không tự chuyển người dùng sang một vai trò khác. API #04 dùng cùng `401 DESIGN_AUTHENTICATION_REQUIRED` cho JWT/access token không hợp lệ và profile không tồn tại; response không phân biệt hai nguyên nhân, nên UI không được mặc định nói “phiên hết hạn”. Route `/forbidden` hiện được khai báo trong `shared.route.ts`.

| Thuộc tính | Đặc tả |
|---|---|
| Mục tiêu | Giải thích trạng thái xác thực/quyền bằng thông điệp an toàn, cung cấp bước tiếp theo phù hợp và giữ trace ID thật để hỗ trợ. |
| Tác nhân | Khách chưa đăng nhập; người có credential hết hạn/không hợp lệ; người dùng có danh tính nhưng không qua được kiểm tra quyền Student của API #04. |
| Quyền truy cập | Có thể hiển thị như trang lỗi không cần quyền; bản thân view không cấp quyền. Không hiển thị profile hoặc payload được bảo vệ. |
| Điều kiện trước | API #04 trả 401/403 theo contract và `StudentApiService` chuyển state đã chuẩn hóa tới route; direct navigation không có error context sẽ hiển thị trạng thái trung tính. |
| Điều kiện sau | Sau khi recovery policy xử lý 401, có thể đưa người dùng tới SH-02 nếu cần đăng nhập; 403 giữ trạng thái từ chối quyền và chỉ cho quay về route nội bộ an toàn đã xác nhận. Không có token trong URL. Điều kiện sau 401 khi profile thiếu chưa được chốt. |
| Liên kết màn hình | [SH-02 Đăng nhập](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02.md), [SH-01 Trang giới thiệu](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01.md), [GS-01 prototype](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/code.html). GS-01 chưa có DD trong checkout. `/login` (SH-02), `/` (SH-01) và `/courses` (GS-01) là route proposal từ inventory; chưa có route nào được chọn làm fallback mặc định cho SH-05. Login handoff còn phụ thuộc G-14: API #03 catalog và current source có status/response shape khác nhau; SH-02 sở hữu việc chốt parser contract. |
| Sự kiện | `SH05-EV-01` đến `SH05-EV-07`; mục 6. |
| API | API #04 `GET /api/v1/users/me`; R-X01 `POST /api/v1/auth/refresh` (runtime source, chưa có ID API trong catalog); xem mục 5. |
| Trạng thái nguồn | Angular Study Web source có route/error handoff SH-05, `StudentSessionService` in-memory/proactive refresh và API #04 caller qua `StudentApiService`. `AdminSessionService` chỉ chấp nhận ADMIN và không được tái sử dụng cho SH-05. Runtime chưa xác minh. |

### 1.1 Tách hành vi kỳ vọng và hiện trạng

| Hành vi | Kỳ vọng theo `list_screen.md` / AC | Hiện trạng theo source |
|---|---|---|
| Phân nhánh lỗi | Phân biệt 401 và 403; inventory cho phép thử R-X01 tối đa một lần sau 401, không refresh sau 403. | #04 trả 401 `DESIGN_AUTHENTICATION_REQUIRED` cho auth không hợp lệ **và** profile không tồn tại; 403 `DESIGN_ACCESS_DENIED` cho role mismatch. `StudentApiService` chuyển đúng 401/403 envelope tới SH-05; không suy nguyên nhân 401. |
| Refresh | Shared auth rule cho phép tối đa một refresh/retry cho flow 401; không refresh sau 403. | Server xoay token trong transaction. `StudentSessionService` giữ token trong memory và refresh proactive khi local expiry tới trước request; `StudentApiService` hiện không refresh/replay sau HTTP 401 từ server mà xóa local session rồi route SH-05. Không có 403 refresh. Server-401 retry, persistence/security và ambiguous outcome vẫn còn gate. |
| 403 | Không refresh để đổi quyền; giữ thông báo an toàn và đường lui. | #04 yêu cầu role `STUDENT`; role mismatch trả 403. Server không phát ra reason code nội bộ trong error envelope. |
| Lỗi khác | 5xx/mạng/timeout không bị đổi thành 403. | Inventory và shared state guide tách service error khỏi unauthorized/forbidden. Prototype hiện chỉ mô phỏng hai mã 401/403. |
| Trace | Dùng `traceId` response thật; không tự dựng ID/time. | SH-05 chỉ hiển thị trace ID body/header khi không mâu thuẫn; không có trace thì ẩn trace card. |
| Điều hướng | Login theo SH-02; 403 quay về route an toàn trước đó nếu được phép. | 401 handoff có `/login` không kèm `returnTo`; 403 safe-back chưa được wire do fallback chưa duyệt. |

`code.html` là prototype. Nó dùng mã lỗi, reason, trace ID, timestamp và envelope mẫu khác API hiện tại; hàm `executeRuntimeRefresh()` chỉ dùng `setTimeout` và không gửi HTTP. Prototype không phải bằng chứng client runtime.

**DISCREPANCY:** AC-02/AC-11 không định nghĩa cách phân biệt 401 do auth không hợp lệ với 401 do profile không tồn tại. The current route/view/error handoff is source-wired, but refresh after server 401, safe fallback and final copy remain unresolved.
