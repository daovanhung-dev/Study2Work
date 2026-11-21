# SH-02 — Đăng nhập · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `SH-02` |
| Module | Shared / Auth / System |
| Route | `/login` — wired qua SharedLayout tới SH02Page; browser/runtime chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | SH-02 hoàn thiện 100% theo rubric tĩnh UI/UX/logic/API; API #03 reconciled và role-home flow source-wired; browser/live runtime chưa xác minh |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.4 / 2026-11-21 |
| Nguồn đối chiếu | [SH-02.md](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02.md), [SH-02_PLAN.md](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02_PLAN.md), [SH-02_markers.json](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Đăng nhập email/password, lỗi an toàn, xác thực hồ sơ Student và điều hướng theo role.
- In-scope: POST #03 theo HTTP 200 current Study Server response; credentials ở session memory theo role; gọi #04 chỉ cho Student; điều hướng mặc định `/student`, `/mentor` hoặc `/admin`.
- Out-of-scope: `returnTo`, lưu token bền vững, quên mật khẩu và live deployment/API verification.

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
| Current source | SH02Page, SH02LoginService, role session managers and API callers | Form submits #03 once; role-specific session in tab memory; #04 only for Student; role routes; runtime unverified |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [SH-02 source screen.png](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/screen_annotated.png))
- Luồng hiện tại: POST #03 once → accept only the exact HTTP 200 `DESIGN_RESOURCE_RETRIEVED` profile+token envelope into the matching role session; Student then calls #04 and checks Student role/email; route to the role home. No `returnTo`.
- Priority: P0; scope-level contract/routing/session checks are covered by focused tests. Browser, live API, DB and deployment remain unverified.

## 7. Reconciliation and implementation evidence — 2026-11-21

- Người dùng chọn current Study Server API #03 làm contract cho SH-02. `docs/lists/list_api.md` và API #03 DD hiện khai báo HTTP 200 `DESIGN_RESOURCE_RETRIEVED` với `LoginData` profile+tokens; reusable `UserProfile` không đổi.
- UI submit/error/password-visibility states, role-session handoff, Student-only #04 verification and default role destinations are implemented and covered by focused SH-02/API tests.
- Không có `returnTo`. Refresh/replay của API #04 được xử lý đúng một lần trong `StudentApiService`; nhánh này có test riêng.
- SH-02 đạt 100% theo rubric tĩnh UI/UX/logic/API của repository. Runtime/browser và môi trường deploy vẫn `NOT VERIFIED`.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-16 — Historical: added Shared `/login` presentation page; historical tests/build covered presentation only.
- 2026-11-20 — Wired form validation/error states and #03 role dispatch; Student uses #04 verification, Mentor/Admin use existing role session managers. Catalog #03 discrepancy, `returnTo`, full Stitch acceptance and runtime remain unresolved. No tests/build/lint/browser run in this continuation.

## Trạng thái và ranh giới bằng chứng

# Tài liệu thiết kế chi tiết màn hình — SH-02 Đăng nhập

> **Trạng thái DD:** scope SH-02 reconciled to selected current-source API #03 and role-home flow · **Implementation:** SOURCE-WIRED · **Runtime:** NOT VERIFIED
> **Mã màn hình:** SH-02 · **Bề mặt:** Trang · **Tác nhân:** Khách
> **Route source hiện tại:** /login wired tới SH02Page · **AC:** AC-02 · **Độ ưu tiên:** P0
> **Nhãn phía máy chủ trong danh mục:** R cho nguồn API #03/#04; màn hình Study Web và bộ quản lý phiên phía client không có trong bản làm việc này.

## Trích đoạn tổng quan từ DD nguồn

> Các đoạn nguồn/snapshot tiếp theo giữ traceability của bản DD trước. Nếu chúng còn gọi #03/`returnTo` là blocker, ưu tiên quyết định ngày 2026-11-21 và mục Reconciliation ở đầu file.

### Trích từ DD nguồn: 1. Tổng quan

SH-02 cho phép khách gửi email và mật khẩu, xử lý lỗi đăng nhập rồi tiếp tục tới route Study đã xác thực sau khi xác định vai trò/hồ sơ. Luồng đích trong danh mục là đăng nhập bằng API #03, sau đó gọi API #04 lấy người dùng hiện tại **chỉ cho học viên**. API #04 không phải endpoint hồ sơ dùng chung: nguồn hiện tại yêu cầu vai trò STUDENT; người hướng dẫn/quản trị viên bị chặn bởi G-02.

**Điều kiện trước:** Người dùng mở route công khai `/login`; không cần token để hiển thị form. **Điều kiện sau hiện tại:** lỗi hiển thị tại form; success #03 được chuyển vào session manager theo role; Student phải qua #04 trước khi tới `/student`; Mentor/Admin tới role shell tương ứng. Không có `returnTo`. Runtime chưa xác minh.

**Lý do DD BLOCKED:** hợp đồng thành công API #03 trong danh mục (201, chỉ UserProfile) khác AC-02/nguồn hiện tại (200, hồ sơ và token); chính sách lưu/refresh phiên và route theo vai trò cũng chưa được duyệt. Tài liệu giữ rõ các nhánh bằng chứng nhưng chưa thể làm hợp đồng triển khai duy nhất. Source API có mặt không chứng minh Study Web hoặc môi trường runtime đã nối.

DD này tách riêng ba loại bằng chứng:

1. list_screen.md và AC-02 mô tả luồng màn hình/nghiệp vụ kỳ vọng.
2. Mã nguồn Study Server hiện tại mô tả route thực tế cùng hành vi yêu cầu/phản hồi.
3. screen.png hiện tại trống; code.html là bản mẫu thiết kế thẻ đăng nhập có tham chiếu bộ xử lý nội tuyến. Ảnh sạch trong DD là ảnh dựng từ HTML đã ghi nguồn, không phải ảnh chụp khi chạy.

### 1.1 Trạng thái tài sản và triển khai

| Bằng chứng | Phát hiện hiện tại | Trạng thái |
|---|---|---|
| Angular Study Web source/package | Có Angular 22 app, package manifest và Admin/Student/System routes | SOURCE_PRESENT |
| SH-02 route/page | `/login` qua SharedLayout tới SH02Page; unit spec 3/3 và app route spec 6/6 pass | SOURCE_WIRED; BROWSER_RUNTIME_NOT_VERIFIED |
| SH-02 API/session | Submit calls #03; role session accepts returned credentials in memory; Student additionally calls #04; no persistent token storage or `returnTo` | SOURCE_WIRED_PARTIAL; API #03 contract discrepancy and runtime remain open |
| .agents/web-work/study/AGENTS.md và INDEX.md | Context pages hiện tại được khai báo trong context map/manifest; runtime deploy chưa xác minh | CONTEXT_VERIFIED; DEPLOYMENT_NOT_VERIFIED |
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
