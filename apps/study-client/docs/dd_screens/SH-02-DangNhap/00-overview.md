# SH-02 — Đăng nhập · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `SH-02` |
| Module | Shared / Auth / System |
| Route | `/login` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái DD:** DD BLOCKED · **Trạng thái triển khai:** IMPLEMENTATION BLOCKED · **Runtime:** RUNTIME NOT VERIFIED |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [SH-02.md](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02.md), [SH-02_PLAN.md](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02_PLAN.md), [SH-02_markers.json](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Email/password, lỗi tại trường, nhớ route đích, tách thông báo 401 và tài khoản bị chặn.
- In-scope: POST #3 → lưu token ở client an toàn → #4 CHỈ cho Student; Mentor/Admin chưa có /me phù hợp.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-02 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Email/password, lỗi tại trường, nhớ route đích, tách thông báo 401 và tài khoản bị chặn. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #03, #04
- Liên kết màn hình dự kiến: [ST-01](../ST-01-TongQuanHocVien/00-overview.md), [SH-03](../SH-03-DangKyHocVien/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | idle/validating/submitting/401/403/network-error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [SH-02 source screen.png](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/screen_annotated.png))
- Luồng: POST #3 → lưu token ở client an toàn → #4 CHỈ cho Student; Mentor/Admin chưa có /me phù hợp.
- Priority: P0; Gate/source status: **R**; **BLOCK:** Role bootstrapping Mentor/Admin chưa hoàn chỉnh

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# Tài liệu thiết kế chi tiết màn hình — SH-02 Đăng nhập

> **Trạng thái DD:** DD BLOCKED · **Trạng thái triển khai:** IMPLEMENTATION BLOCKED · **Runtime:** RUNTIME NOT VERIFIED
> **Mã màn hình:** SH-02 · **Bề mặt:** Trang · **Tác nhân:** Khách
> **Route đề xuất:** /login · **AC:** AC-02 · **Độ ưu tiên:** P0
> **Nhãn phía máy chủ trong danh mục:** R cho nguồn API #03/#04; màn hình Study Web và bộ quản lý phiên phía client không có trong bản làm việc này.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan

SH-02 cho phép khách gửi email và mật khẩu, xử lý lỗi đăng nhập rồi tiếp tục tới route Study đã xác thực sau khi xác định vai trò/hồ sơ. Luồng đích trong danh mục là đăng nhập bằng API #03, sau đó gọi API #04 lấy người dùng hiện tại **chỉ cho học viên**. API #04 không phải endpoint hồ sơ dùng chung: nguồn hiện tại yêu cầu vai trò STUDENT; người hướng dẫn/quản trị viên bị chặn bởi G-02.

**Điều kiện trước:** Người dùng mở route công khai `/login`; nếu được chuyển từ route cần bảo vệ, chỉ nhận `returnTo` sau khi chính sách allowlist/role được duyệt. Không cần token để hiển thị form. **Điều kiện sau:** lỗi thì ở lại SH-02 với trạng thái an toàn; thành công chỉ được coi là hoàn tất sau khi contract #03, session policy và role/profile flow được duyệt. Hiện chưa có client route/runtime để thực hiện chuyển tiếp.

**Lý do DD BLOCKED:** hợp đồng thành công API #03 trong danh mục (201, chỉ UserProfile) khác AC-02/nguồn hiện tại (200, hồ sơ và token); chính sách lưu/refresh phiên và route theo vai trò cũng chưa được duyệt. Tài liệu giữ rõ các nhánh bằng chứng nhưng chưa thể làm hợp đồng triển khai duy nhất. Source API có mặt không chứng minh Study Web hoặc môi trường runtime đã nối.

DD này tách riêng ba loại bằng chứng:

1. list_screen.md và AC-02 mô tả luồng màn hình/nghiệp vụ kỳ vọng.
2. Mã nguồn Study Server hiện tại mô tả route thực tế cùng hành vi yêu cầu/phản hồi.
3. screen.png hiện tại trống; code.html là bản mẫu thiết kế thẻ đăng nhập có tham chiếu bộ xử lý nội tuyến. Ảnh sạch trong DD là ảnh dựng từ HTML đã ghi nguồn, không phải ảnh chụp khi chạy.

### 1.1 Trạng thái tài sản và triển khai

| Bằng chứng | Phát hiện hiện tại | Trạng thái |
|---|---|---|
| Mã Study Web, router, client API/phiên | Không có trong apps/study-client/ | UNWIRED / SOURCE_REQUIRED |
| .agents/web-work/study/AGENTS.md và INDEX.md | Hai trang hiện có, được khai báo trong context map và đăng ký trong manifest; chúng xác nhận editable Study Web source/package manifest không có và runtime chưa xác minh | CONTEXT_VERIFIED; APP UNWIRED |
| screen.png gốc | 1280×1024; nhìn thấy ảnh trống | PRESENT_BUT_BLANK |
| code.html gốc | Có bố cục đăng nhập, biểu mẫu và điều khiển; tải Tailwind/Google assets từ xa | DESIGN_SOURCE_ONLY |
| Bản dựng sạch | Dựng từ code.html hiện tại ở 1280×1024 | DERIVED_PREVIEW, không phải ảnh gốc/khi chạy |
| Ảnh chú thích | Lớp đánh số trên bản dựng sạch, xuất ở độ phân giải 2× | PRESENT; marker #1–#8 ánh xạ SH02-EL-01..08 |
| API #03 và #04 | Có route, view, validator/model và mã kiểm thử nguồn | RUNTIME_SOURCE; không khẳng định DB thật/triển khai |
| R-X01 refresh | POST /api/v1/auth/refresh có trong mã nguồn nhưng không có ID API trong danh mục | SOURCE_BACKED_UNCATALOGUED |

### 1.2 Ảnh và nguồn gốc

- [Ảnh gốc được cung cấp](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/screen.png) được giữ nguyên; không có biểu mẫu nào hiển thị để chú thích.
- [Bản xem dựng sạch](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/screen_rendered.png) được Chrome headless dựng từ HTML tương ứng ở 1280×1024 và tải tài nguyên Tailwind/font ngoài mà HTML tham chiếu. Đây là bản xem thiết kế phát sinh, có phụ thuộc tài nguyên ngoài được ghi trong nguồn gốc.
- [Ảnh đánh số](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/screen_annotated.png) chú thích lên bản xem sạch; không được xem là bản PNG nguồn trống đã sửa.
- [HTML gốc](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/code.html), [kế hoạch màn hình](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02_PLAN.md) và [bản đồ marker](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02_markers.json) vẫn được giữ riêng. Hash PNG/HTML nguồn được ghi trong worklog.

### 1.3 Vai trò và quyền route

- /login là route công khai cho Khách. Không thêm chặn xác thực để đẩy người chưa đăng nhập khỏi trang này.
- Khi API #03 thành công, nguồn hiện có thể cấp token cho vai trò không phải học viên. API #04 hiện chỉ chấp nhận học viên. Không gọi endpoint #04 dành cho học viên với token người hướng dẫn/quản trị viên và không đưa tài khoản đó tới bảng điều khiển học viên.
- Nếu guard route cần bảo vệ cung cấp returnTo, giá trị phải là đường dẫn tương đối cùng miền trong danh sách cho phép của vai trò đã xác minh. Từ chối URL tuyệt đối, //host và đường dẫn không được duyệt. Không đưa token, mật khẩu hay email vào returnTo.
- Đích mặc định học viên /student chỉ là đề xuất route, chưa có trong client hiện tại. Đích người hướng dẫn/quản trị viên và chính sách lưu token còn chưa quyết định.
