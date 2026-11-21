# SH-03 — Đăng ký học viên · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `SH-03` |
| Module | Shared / Auth / System |
| Route | `/register` — route unit test pass; local Chrome headless đã render sau hydration ở desktop/mobile; deployment/deep-link chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | SH-03 hoàn thiện 100% theo rubric tĩnh UI/UX/logic/API; API #01 registration, validated result and one-use SH-04 handoff are source-wired and focused tests pass; email delivery/account lifecycle and deployment remain outside verified runtime |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.3 / 2026-11-21 |
| Nguồn đối chiếu | [SH-03.md](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/SH-03.md), [SH-03_PLAN.md](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/SH-03_PLAN.md), [SH-03_markers.json](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/SH-03_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Nhập tên/email/password và xác nhận điều khoản nếu có contract; không tự thêm CAPTCHA/OTP.
- Expected flow: POST #1 → nhận user_id,email → SH-04; 409 email trùng trở lại form.
- Current implementation (2026-11-21): form công khai trim tên/email, kiểm tra email sớm, gọi API #01 qua `StudyApiService`, và không gọi API #02 trực tiếp. Chỉ HTTP 201 `DESIGN_RESOURCE_CREATED` có `data.id` nguyên dương an toàn và `data.email` không rỗng mới hiện tài khoản đã tạo/xóa mật khẩu; nút tiếp tục chuyển ID/email hợp lệ sang SH-04 bằng one-use in-memory handoff. API #02 acceptance does not prove email delivery or account verification.
- Completion evidence (2026-11-21): the repository's static UI/UX/logic/API rubric is 100%; focused tests are included in the passing 11-file/36-test Shared-flow command. Browser, live API, DB and deployment are not verified.

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
| Current source | `shared.route.ts`, `SH03/pages/*`, `SH03/data-access/*`, SH04 handoff service | `/register`, API #01 caller, validated account-created state and explicit SH-04 in-memory handoff are source-wired; prior route/component test and local render results are historical evidence only |
| Browser runtime | Worklog T018 | Local route render verified; form submit, live API and deployed runtime remain unverified |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [SH-03 source screen.png](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/01_shared_auth_system/SH-03_dang-ky-hoc-vien/screen_annotated.png))
- Current flow: POST #01 → validate HTTP 201 envelope + `data.id/email` → user-controlled in-memory handoff to SH-04; #02 is called only from SH-04. 409 email trùng trở lại form. Focused tests cover local validation, duplicate-submit protection, success projection, handoff disclaimers and safe error states.
- Priority: P0; Gate/source status: **R**

## 7. Reconciliation and implementation evidence — 2026-11-21

- SH-03 static implementation is complete under the repository's UI/UX/logic/API rubric. The targeted SH-03 spec passed after correcting its expected continuation control to match the rendered button.
- The successful registration result presents an explicit action; it never claims that API #02 sent email. Browser/live API/DB/deployment remain unverified.

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
3. `screen.png` và `code.html` là tài sản thiết kế. Prior worklog records Angular page/route tests and local Chrome render; those checks were not repeated in this task. Current source now connects the validated #01 result to SH-04 through one-use memory state; browser runtime, live API and deployment remain unverified.

**Căn cứ DD READY:** hành vi thuộc màn SH-03 (nhập ba trường, gọi #01, ánh xạ 201/409/422/500, giữ kết quả không rõ, và output `data.id`/`data.email` cùng đích SH-04 hoặc SH-02) đã được nêu rõ. Cơ chế chuyển tạm `id/email` sang SH-04 chưa được chọn; đây là blocker nối liên màn/implementation ghi tại §10, không phải field/API được tự suy đoán trong DD.

### 1.1. Bằng chứng và trạng thái

| Bằng chứng | Phát hiện | Trạng thái |
|---|---|---|
| Context Study Web | `.agents/web-work/study/AGENTS.md` và `INDEX.md` hiện có, được khai báo trong context map và manifest; chúng mô tả Angular app source. | `CONTEXT VERIFIED` |
| Mã giao diện Study Web và bộ định tuyến | `features/shared/SH03/pages/*` render form; `data-access/sh03-registration.service.ts` calls API_001; `shared.route.ts` registers `/register`; continuation stores validated `id/email` in SH04 handoff service. Prior test/render results are recorded in worklog, not repeated here. | `API #01 + SH-04 HANDOFF SOURCE-WIRED`; live API/deployment chưa xác minh |
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
- **Điều kiện sau:** 201 cho phép bàn giao `data.id`/`data.email` tới SH-04 theo F01; source dùng một lần trong-memory, không khôi phục sau refresh/direct URL. 409/422/500 hoặc kết quả mạng chưa rõ giữ người dùng ở SH-03; không tuyên bố email đã gửi/xác minh.
- **Current implementation:** form gửi đúng `{email, password, full_name}` tới API #01; trim email/tên, kiểm tra email sớm sau trim, giữ nguyên mật khẩu; xử lý 409/422/500/network an toàn. Chỉ 201 `DESIGN_RESOURCE_CREATED` có `data.id` nguyên dương và `data.email` không rỗng mới báo tài khoản đã tạo/xóa mật khẩu. Nút tiếp tục đặt ID/email vào handoff service rồi chuyển SH-04; API #02 chỉ được gọi bởi SH-04 sau một thao tác riêng. Malformed success giữ form và báo kết quả chưa xác định. Live API/deployment chưa xác minh.
- Vai trò `STUDENT` do SQL API #01 gán ở phía máy chủ. Phía giao diện không gửi `role` hoặc `status`.
- Không thêm lựa chọn điều khoản, CAPTCHA, OTP, đăng nhập mạng xã hội hoặc trường khác: chưa có hợp đồng cho chúng.
