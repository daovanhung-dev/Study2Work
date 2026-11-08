# SH-05 — Không đủ quyền / session hết hạn · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `SH-05` |
| Module | Shared / Auth / System |
| Route | `/forbidden` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái:** `DD BLOCKED` vì chưa chốt nguyên nhân/phục hồi 401 và thành phần prototype nào là UI người dùng; `IMPLEMENTATION BLOCKED` do thiếu Study Web source cùng quyết định phiên/điều hướng; `RUNTIME NOT VERIFIED`. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [SH-05.md](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05.md), [SH-05_PLAN.md](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05_PLAN.md), [SH-05_markers.json](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Phân biệt 401 (hết hạn/thiếu token), 403 (không đủ quyền), bảo toàn redirect an toàn.
- In-scope: Khi 401 có thể thử refresh runtime R-X01 1 lần; 403 KHÔNG refresh vô hạn.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

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
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [SH-05 source screen.png](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/screen_annotated.png))
- Luồng: Khi 401 có thể thử refresh runtime R-X01 1 lần; 403 KHÔNG refresh vô hạn.
- Priority: P0; Gate/source status: **R**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# Tài liệu thiết kế chi tiết màn hình — SH-05 Không đủ quyền / phiên hết hạn

> **Mã màn hình:** SH-05 · **Loại:** state view · **Tác nhân:** khách chưa xác thực hoặc người dùng đã xác thực nhưng không có quyền phù hợp
> **Route đề xuất:** `/forbidden` · **AC:** AC-02, AC-11 · **API catalog:** #04 · **Runtime hỗ trợ:** R-X01
> **Trạng thái:** `DD BLOCKED` vì chưa chốt nguyên nhân/phục hồi 401 và thành phần prototype nào là UI người dùng; `IMPLEMENTATION BLOCKED` do thiếu Study Web source cùng quyết định phiên/điều hướng; `RUNTIME NOT VERIFIED`.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan

SH-05 là state view dùng cho lỗi xác thực (`401`) hoặc từ chối quyền (`403`). View không tự xác thực lại bằng cách gọi API hồ sơ, không render dữ liệu được bảo vệ và không tự chuyển người dùng sang một vai trò khác. API #04 dùng cùng `401 DESIGN_AUTHENTICATION_REQUIRED` cho JWT/access token không hợp lệ và profile không tồn tại; response hiện không phân biệt hai nguyên nhân, nên UI không được mặc định nói “phiên hết hạn”. Route `/forbidden` là đề xuất trong inventory, chưa được xác nhận bởi Study Web router vì checkout không có `apps/study-client/src/`.

| Thuộc tính | Đặc tả |
|---|---|
| Mục tiêu | Giải thích trạng thái xác thực/quyền bằng thông điệp an toàn, cung cấp bước tiếp theo phù hợp và giữ trace ID thật để hỗ trợ. |
| Tác nhân | Khách chưa đăng nhập; người có credential hết hạn/không hợp lệ; người dùng có danh tính nhưng không qua được kiểm tra quyền Student của API #04. |
| Quyền truy cập | Có thể hiển thị như trang lỗi không cần quyền; bản thân view không cấp quyền. Không hiển thị profile hoặc payload được bảo vệ. |
| Điều kiện trước | Một request được bảo vệ đã trả kết quả lỗi được chuẩn hóa, hoặc người dùng truy cập trực tiếp route lỗi. Nguồn và cách truyền context lỗi vào route chưa có trong Study Web source. |
| Điều kiện sau | Sau khi recovery policy xử lý 401, có thể đưa người dùng tới SH-02 nếu cần đăng nhập; 403 giữ trạng thái từ chối quyền và chỉ cho quay về route nội bộ an toàn đã xác nhận. Không có token trong URL. Điều kiện sau 401 khi profile thiếu chưa được chốt. |
| Liên kết màn hình | [SH-02 Đăng nhập](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02.md), [SH-01 Trang giới thiệu](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01.md), [GS-01 prototype](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/code.html). GS-01 chưa có DD trong checkout. `/login` (SH-02), `/` (SH-01) và `/courses` (GS-01) là route proposal từ inventory; chưa có route nào được chọn làm fallback mặc định cho SH-05. Login handoff còn phụ thuộc G-14: API #03 catalog và current source có status/response shape khác nhau; SH-02 sở hữu việc chốt parser contract. |
| Sự kiện | `SH05-EV-01` đến `SH05-EV-07`; mục 6. |
| API | API #04 `GET /api/v1/users/me`; R-X01 `POST /api/v1/auth/refresh` (runtime source, chưa có ID API trong catalog); xem mục 5. |
| Trạng thái nguồn | API #04 và R-X01 có mã Study Server cùng test source; Study Web UI/auth client chưa có source. Không có runtime UI nào được xác minh. |

### 1.1 Tách hành vi kỳ vọng và hiện trạng

| Hành vi | Kỳ vọng theo `list_screen.md` / AC | Hiện trạng theo source |
|---|---|---|
| Phân nhánh lỗi | Phân biệt 401 và 403; inventory cho phép thử R-X01 tối đa một lần sau 401, không refresh sau 403. | #04 trả 401 `DESIGN_AUTHENTICATION_REQUIRED` cho auth không hợp lệ **và** profile không tồn tại; 403 `DESIGN_ACCESS_DENIED` cho role mismatch. Cùng một response không cho biết nguyên nhân 401; HTML chỉ có preview toggle. |
| Refresh | Shared auth rule yêu cầu tối đa một refresh/retry cho flow 401 và single-flight coordination cho request đồng thời; không refresh sau 403. | Endpoint server xoay token trong transaction; client interceptor, token persistence, single-flight implementation, replay và xử lý refresh thành công nhưng request #04 tiếp tục 401 chưa có source. |
| 403 | Không refresh để đổi quyền; giữ thông báo an toàn và đường lui. | #04 yêu cầu role `STUDENT`; role mismatch trả 403. Server không phát ra reason code nội bộ trong error envelope. |
| Lỗi khác | 5xx/mạng/timeout không bị đổi thành 403. | Inventory và shared state guide tách service error khỏi unauthorized/forbidden. Prototype hiện chỉ mô phỏng hai mã 401/403. |
| Trace | Dùng `traceId` response thật; không tự dựng ID/time. | Backend error envelope và header có trace ID; HTML chứa dữ liệu mẫu `tr_403_sec_study`. |
| Điều hướng | Login theo SH-02; 403 quay về route an toàn trước đó nếu được phép. | HTML href `/sh-02-login` và `/sh-01-dashboard` không khớp route inventory `/login` và `/`. |

`code.html` là prototype. Nó dùng mã lỗi, reason, trace ID, timestamp và envelope mẫu khác API hiện tại; hàm `executeRuntimeRefresh()` chỉ dùng `setTimeout` và không gửi HTTP. Prototype không phải bằng chứng client runtime.

**DISCREPANCY:** AC-02/AC-11 mô tả các flow gọi API #04 nhưng không định nghĩa route/UI của SH-05 hoặc cách phân biệt 401 do hết hạn với 401 do profile không tồn tại. Dùng inventory SH-05 làm intent cho 401/403/refresh, nhưng giữ recovery sau lần thử #04 lặp lại ở trạng thái cần Product/Backend xác nhận.
