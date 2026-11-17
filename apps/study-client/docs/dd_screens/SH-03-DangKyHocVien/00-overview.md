# SH-03 — Đăng ký học viên · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `SH-03` |
| Module | Shared / Auth / System |
| Route | `/register` — route unit test pass; local Chrome headless đã render sau hydration ở desktop/mobile; deployment/deep-link chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); DD nguồn `DD READY`; current source có presentation, route và API #01 caller; local render đã xác minh; SH-04 handoff/account lifecycle còn `BLOCKED`; deployment/runtime tích hợp chưa xác minh |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.2 / 2026-11-16 |
| Nguồn đối chiếu | [SH-03.md](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/SH-03.md), [SH-03_PLAN.md](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/SH-03_PLAN.md), [SH-03_markers.json](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/SH-03_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Nhập tên/email/password và xác nhận điều khoản nếu có contract; không tự thêm CAPTCHA/OTP.
- Expected flow: POST #1 → nhận user_id,email → SH-04; 409 email trùng trở lại form.
- Current implementation: form công khai trim tên/email, kiểm tra email sớm, gọi API #01 qua `StudyApiService`, và không gọi API #02. Chỉ 201 `DESIGN_RESOURCE_CREATED` có `data.id` nguyên dương và `data.email` không rỗng mới hiện tài khoản đã tạo/xóa mật khẩu; SH-04 handoff vẫn blocked do transport và account lifecycle chưa được chốt.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-01 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Nhập tên/email/password và xác nhận điều khoản nếu có contract; không tự thêm CAPTCHA/OTP. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #01
- Liên kết màn hình dự kiến: [SH-04](../SH-04-HandoffXacThucEmail/00-overview.md), [SH-02](../SH-02-DangNhap/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | validating/submitting/409/422/201 |
| Current source | `shared.route.ts`, `SH03/pages/*`, `SH03/data-access/*`, app-route/component specs | `/register` và API #01 caller được wire; component/route tests pass; local Chrome headless direct-route render verified desktop/mobile |
| Browser runtime | Worklog T018 | Local route render verified; form submit, live API and deployed runtime remain unverified |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [SH-03 source screen.png](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/screen_annotated.png))
- Luồng: POST #1 → nhận user_id,email → SH-04; 409 email trùng trở lại form.
- Priority: P0; Gate/source status: **R**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-16 — Thêm presentation Angular và route `/register`; unit test xác nhận route/form và không gọi API. (Ghi nhận trạng thái trước đó; được cập nhật bởi mục triển khai API #01 bên dưới.)

## Trạng thái và ranh giới bằng chứng

# Tài liệu thiết kế chi tiết màn hình — SH-03 Đăng ký học viên

> **Trạng thái DD:** DD READY · **Trạng thái triển khai:** API #01 WIRED / SH-04 HANDOFF BLOCKED · **Focused tests:** VERIFIED · **Local route render:** VERIFIED desktop/mobile · **Live API/deployment:** NOT VERIFIED · **Mã màn hình:** SH-03 · **Bề mặt:** Trang · **Tác nhân:** Khách · **Đường dẫn:** `/register` · **Tiêu chí:** AC-01 · **Ưu tiên:** P0.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan

SH-03 thu thập họ tên, email và mật khẩu để tạo tài khoản học viên. Theo luồng F01 trong [danh mục màn hình](../../list_screen.md), màn hình gửi API #01; khi tạo tài khoản thành công, chuyển sang SH-04 để xử lý bước yêu cầu gửi email. Liên kết cuối thẻ mở SH-02 cho người đã có tài khoản.

Tài liệu tách riêng thiết kế đích và hiện trạng mã nguồn:

1. `list_screen.md` xác định màn hình, đường dẫn đề xuất, tiêu chí AC-01, thứ tự SH-03 → SH-04 và các trạng thái cần thể hiện.
2. Mã nguồn Study Server xác nhận đường dẫn đăng ký và hành vi API #01. API #02 là đường dẫn riêng, dùng bộ gửi thư giả lập mặc định; API #01 không gọi API #02.
3. `screen.png` và `code.html` là tài sản thiết kế. Angular page/route `/register` và caller API #01 có focused unit tests; Chrome headless xác nhận route local render ở desktop/mobile. Không submit form; live API/deployment chưa xác minh. Caller không nối tiếp sang SH-04/API #02.

**Căn cứ DD READY:** hành vi thuộc màn SH-03 (nhập ba trường, gọi #01, ánh xạ 201/409/422/500, giữ kết quả không rõ, và output `data.id`/`data.email` cùng đích SH-04 hoặc SH-02) đã được nêu rõ. Cơ chế chuyển tạm `id/email` sang SH-04 chưa được chọn; đây là blocker nối liên màn/implementation ghi tại §10, không phải field/API được tự suy đoán trong DD.

### 1.1. Bằng chứng và trạng thái

| Bằng chứng | Phát hiện | Trạng thái |
|---|---|---|
| Context Study Web | `.agents/web-work/study/AGENTS.md` và `INDEX.md` hiện có, được khai báo trong context map và manifest; chúng mô tả Angular app source. | `CONTEXT VERIFIED` |
| Mã giao diện Study Web và bộ định tuyến | `features/shared/SH03/pages/*` render form; `data-access/sh03-registration.service.ts` gọi API_001; `shared.route.ts` đăng ký `/register`; focused specs pass; Chrome headless render local desktop/mobile. | `API #01 WIRED`; live API/deployment chưa xác minh |
| Ảnh mẫu | [Ảnh gốc](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/screen.png), 1280×1056, hiển thị thương hiệu, tiêu đề, ba trường, nút tạo tài khoản và liên kết đăng nhập. | `PRESENT` / CHỈ LÀ THIẾT KẾ |
| Mã HTML mẫu | [HTML gốc](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/code.html) dựng được nội dung tiếng Việt; `onsubmit` chỉ gọi `event.preventDefault()`. | `DESIGN_SOURCE_ONLY` |
| API #01 | Có đường dẫn, mô hình dữ liệu, bộ kiểm tra, lớp điều phối, câu truy vấn và mã kiểm thử trong Study Server. | `SOURCE_BACKED`; không xác nhận môi trường triển khai hoặc cơ sở dữ liệu đang chạy thực tế |
| API #02 | Có đường dẫn và bộ gửi thư mặc định `StubVerificationEmailProvider`, chỉ trả `accepted`. | `STUB`; không gửi thư thật, không xác minh địa chỉ |
| Nối #01 → #02 | API #01 sau commit chỉ ghi `verification_dispatch_pending`; AC-01 vẽ bước #02 sau khi tạo user, còn F01 đặt #02 tại SH-04. | `DISCREPANCY`; #01 hiện không gọi #02 |
| Sai khác mật khẩu | Trợ giúp ẩn trong HTML mẫu yêu cầu tối thiểu 8 ký tự; API #01 không thực thi mức tối thiểu đó. | `DISCREPANCY` |
| Trạng thái người dùng | Lệnh chèn API #01 không gán `status`; tệp DDL `DB.sql` khai báo default `ACTIVE`; API #03 yêu cầu `status == "ACTIVE"`. Live schema/verification gate chưa xác nhận. | `DISCREPANCY` / `IMPLEMENTATION BLOCKED` |
| `UserProfile.bio` | Catalog khai báo `bio?`; response từ `INSERT_USER` hiện không trả `bio`. | `DISCREPANCY`; SH-03 chỉ cần `id`/`email`, không tạo `bio` |

### 1.2. Tài sản ảnh và quy tắc thị giác

- [Ảnh có đánh số](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/screen_annotated.png) được tạo từ chính ảnh gốc, ở kích thước gấp đôi. Số trên ảnh khớp bảng phần tử tại §4 và [bản đồ marker](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/SH-03_markers.json).
- Ảnh gốc và HTML gốc được giữ nguyên. Vì ảnh gốc đã hiển thị đầy đủ giao diện, không tạo ảnh dựng thay thế.
- Ảnh/HTML sử dụng nền `#F6FAFC`, điểm nhấn xanh biển `#0B5F8A`, thẻ trắng và Plus Jakarta Sans. Đây là mô tả tài sản hiện có, không phải bằng chứng về giao diện khi chạy.
- [Hướng dẫn Study Web](../../../../../.agents/web-study/design.md) là đích giao diện chuẩn: ưu tiên `Inter` có sẵn hoặc sans-serif hệ thống, không thêm phông chữ tải từ xa, lề và điều khiển phải thích ứng, chiều cao điều khiển tối thiểu 44px. `DESIGN.md` tham khảo có các giá trị màu khác nhau giữa phần YAML, văn xuôi và HTML; không sao chép nguyên các giá trị mâu thuẫn đó.

### 1.3. Tác nhân, quyền và đường dẫn

- SH-03 là trang công khai dành cho Khách; API #01 không yêu cầu `Authorization`.
- `/register` là route hiện hành trong `features/shared/shared.route.ts`; unit test xác nhận cấu hình route và Chrome headless render direct route local ở desktop/mobile. Deep-link deployment chưa được xác minh.
- **Điều kiện trước:** người chưa đăng nhập mở trang công khai; không cần token hay request khởi tạo. Các trường bắt đầu rỗng theo ảnh mẫu.
- **Điều kiện sau:** 201 cho phép bàn giao `data.id`/`data.email` tới SH-04 theo F01; cơ chế truyền/khôi phục state chưa được duyệt. 409/422/500 hoặc kết quả mạng chưa rõ giữ người dùng ở SH-03; không tuyên bố email đã gửi/xác minh.
- **Current implementation:** form gửi đúng `{email, password, full_name}` tới API #01; trim email/tên, kiểm tra email sớm sau trim, giữ nguyên mật khẩu; xử lý 409/422/500/network an toàn. Chỉ 201 `DESIGN_RESOURCE_CREATED` có `data.id` nguyên dương và `data.email` không rỗng mới báo tài khoản đã tạo/xóa mật khẩu; malformed success giữ form và báo kết quả chưa xác định. Không gọi #02 hoặc chuyển sang SH-04. Focused tests pass; local route render desktop/mobile verified, live API/deployment chưa xác minh.
- Vai trò `STUDENT` do SQL API #01 gán ở phía máy chủ. Phía giao diện không gửi `role` hoặc `status`.
- Không thêm lựa chọn điều khoản, CAPTCHA, OTP, đăng nhập mạng xã hội hoặc trường khác: chưa có hợp đồng cho chúng.
