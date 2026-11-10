# SH-04 — Handoff xác thực email · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `SH-04` |
| Module | Shared / Auth / System |
| Route | `/register/verification` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái DD:** DD BLOCKED · **Trạng thái triển khai:** IMPLEMENTATION BLOCKED · **Runtime:** RUNTIME NOT VERIFIED · **Mã màn hình:** SH-04 · **Đường dẫn đề xuất:** `/register/verification` · **Tác nhân:** Khách · **Quyền gọi API:** Công khai, không cần `Authorization` · **Loại:** Trang · **Tiêu chí:** AC-01 · **Đợt:** W0 · **Ưu tiên:** P1 · **Tình trạng danh mục màn hình:** `S`. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [SH-04.md](../../screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/SH-04.md), [SH-04_PLAN.md](../../screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/SH-04_PLAN.md), [SH-04_markers.json](../../screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/SH-04_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Hiển thị trạng thái yêu cầu gửi email; chưa có API xác nhận OTP/link.
- In-scope: POST #2 với user_id/email sau đăng ký, chỉ xác nhận accepted (stub), không tuyên bố email đã gửi hoặc đã verify.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-01 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Hiển thị trạng thái yêu cầu gửi email; chưa có API xác nhận OTP/link. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #02
- Liên kết màn hình dự kiến: [SH-02](../SH-02-DangNhap/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | accepted/stub/no-delivery/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [SH-04 source screen.png](../../screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/screen_annotated.png))
- Luồng: POST #2 với user_id/email sau đăng ký, chỉ xác nhận accepted (stub), không tuyên bố email đã gửi hoặc đã verify.
- Priority: P1; Gate/source status: **S**; **BLOCK:** Email provider mới là stub, chưa có confirm endpoint

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# Tài liệu thiết kế chi tiết màn hình — SH-04 Bàn giao xác thực thư điện tử

> **Trạng thái DD:** DD BLOCKED · **Trạng thái triển khai:** IMPLEMENTATION BLOCKED · **Runtime:** RUNTIME NOT VERIFIED · **Mã màn hình:** SH-04 · **Đường dẫn đề xuất:** `/register/verification` · **Tác nhân:** Khách · **Quyền gọi API:** Công khai, không cần `Authorization` · **Loại:** Trang · **Tiêu chí:** AC-01 · **Đợt:** W0 · **Ưu tiên:** P1 · **Tình trạng danh mục màn hình:** `S`.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan

SH-04 là bước tiếp nhận yêu cầu gửi thư điện tử sau khi Khách đăng ký ở SH-03. Theo danh mục màn hình, màn hình gọi API #02 rồi cho người dùng quay lại SH-02. API hiện tại chỉ xác nhận bộ gửi thư giả lập đã tiếp nhận yêu cầu; nó không gửi thư, không tạo OTP hoặc liên kết và không xác minh địa chỉ thư điện tử. Vì vậy, mọi thông báo phải diễn đạt “đã được bộ thử nghiệm tiếp nhận”, không được nói thư đã được gửi hoặc tài khoản đã xác minh.

Tài liệu phân biệt ba loại căn cứ:

1. `list_screen.md` là thiết kế đích: SH-04, đường dẫn đề xuất, AC-01, API #02, trình tự SH-03 → SH-04 → SH-02 và điều kiện chặn về thư điện tử.
2. Mã nguồn Study Server hiện có khai báo API #02 cùng bộ gửi thư mặc định giả lập. Đây là bằng chứng hành vi mã nguồn, không chứng minh giao diện, dịch vụ gửi thư thật, cơ sở dữ liệu thật hoặc triển khai môi trường chính thức.
3. `screen.png` và `code.html` là tài sản thiết kế. Bản làm việc không có mã nguồn Study Web để xác nhận đường dẫn trang, lời gọi API, điều hướng hay trạng thái trình duyệt.

**Lý do DD BLOCKED:** F01 đặt API #02 sau đăng ký, nhưng catalog chỉ mô tả gửi khi verification được bật và API DD chưa chốt feature gate, component sở hữu dispatch, trigger tự động hay thao tác rõ ràng, hoặc kênh chuyển `data.id`/`data.email` từ SH-03. API contract cũng để mở semantics của `ActionResult.status`/`reason` và miền `user_id:int64` chưa khớp validator. Nhánh kế tiếp SH-02 kiểm tra `status=ACTIVE`, trong khi API #01 bỏ qua `status`, DDL không xác nhận live schema và chưa có endpoint xác nhận email cập nhật trạng thái. Các điểm này ảnh hưởng flow và mapping nên không tự chọn trong DD. Luồng dự kiến và các response hiện có vẫn được ghi đầy đủ dưới đây.

### 1.1. Bằng chứng và tình trạng

| Hạng mục | Phát hiện | Tình trạng |
|---|---|---|
| Mã nguồn Study Web và bộ định tuyến | `.agents/web-work/study/AGENTS.md` và `INDEX.md` hiện tồn tại, được khai báo trong manifest; nhưng không có `apps/study-client/src`, router, `package.json` hoặc kiểm thử giao diện. `dist`/`node_modules` không xác nhận source/runtime cho màn hình này. | Context `VERIFIED`; app `UNWIRED` |
| Đường dẫn trang | `/register/verification` có trong danh mục màn hình và ảnh mẫu; chưa có bộ định tuyến để xác nhận hoạt động. | ĐƯỜNG_DẪN_ĐỀ_XUẤT |
| Ảnh mẫu | [Ảnh gốc](../../screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/screen.png), 1600×1280, đang thể hiện nhánh mặc định `accepted`. | CHỈ_LÀ_THIẾT_KẾ |
| HTML mẫu | [HTML gốc](../../screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/code.html), gồm các nút đổi trạng thái cục bộ và nút sao chép lệnh. Không có `fetch` hay lời gọi API. | CHỈ_LÀ_THIẾT_KẾ |
| API #02 | `POST /api/v1/auth/verify-email/send` có route/model/validator/view/provider/test. Public, không mở DB; validator yêu cầu raw JSON integer, chuẩn hóa email; view map `status` và `reason` tùy chọn. Catalog yêu cầu `user_id:int64`, nhưng source không kiểm tra miền int64. | SOURCE-BACKED LOCALLY; CONTRACT DISCREPANCY |
| Bộ gửi thư mặc định | Bỏ qua `user_id`, `email`, `trace_id`; trả `status="accepted"` không kèm `reason`; không gửi thư, không xếp hàng và không tạo token. Các provider khác có thể trả status/reason tùy ý theo interface hiện tại; enum/semantics chưa được duyệt. | STUB SOURCE-VERIFIED; STATUS/REASON OPEN |
| Chủ sở hữu/trigger API #02 | F01 đặt POST #02 tại SH-04 sau đăng ký, nhưng API DD Q-02-01 để mở dispatch owner/feature gate; design không chốt tự gọi khi vào trang hay thao tác riêng. | `DISCREPANCY` / `DD BLOCKED` |
| Handoff SH-03 → SH-04 | API #01 source trả `data.id`/`data.email`; không có route-state/channel trong Study Web source. | `NOT_FOUND` / `IMPLEMENTATION BLOCKED` |
| Xác nhận thư điện tử | Không thấy điểm cuối API xác nhận OTP/liên kết trong danh mục API hiện tại; API #02 chỉ nhận yêu cầu gửi. | `NOT_FOUND` |
| Tài khoản và đăng nhập SH-02 | API #01 INSERT không gán `status`; checked-in DDL có default `ACTIVE`; API #03 từ chối login nếu `status != ACTIVE`. DDL không xác nhận live schema, và không có endpoint hiện tại nối verification với status. | `DISCREPANCY` / `POLICY OPEN` |
| Mã kiểm thử | Đã đọc mã kiểm thử API #02, không chạy kiểm thử trong phiên này. Mã kiểm tra endpoint công khai, không resolve cơ sở dữ liệu, 202 khi provider chấp nhận, 422 khi request sai và 500 khi provider lỗi. | CHỈ_ĐỌC_MÃ_KIỂM_THỬ |

### 1.2. Tài sản ảnh và quy tắc thị giác

- [Ảnh gốc](../../screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/screen.png) và [ảnh có đánh số](../../screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/screen_annotated.png) được giữ tách biệt. Ảnh chú thích có kích thước 3200×2560, gấp đôi mỗi chiều so với ảnh nguồn.
- Mười hai số chú thích khớp [bản đồ số](../../screen_stitch/01_shared_auth_system/SH-04_handoff-xac-thuc-email/SH-04_markers.json) và bảng phần tử ở §4. Ảnh gốc/HTML gốc không bị sửa.
- Tệp tham khảo [DESIGN.md](../../screen_stitch/90_reference/study2work-lms-design-system/DESIGN.md) có mâu thuẫn nội bộ: YAML khai báo `primary: #004ac6`, còn phần văn xuôi gọi `#2563EB` là màu chính. HTML mẫu dùng cả `#004ac6` và `#2563eb` ở các token khác nhau.
- Hướng dẫn [Study Web](../../../../../.agents/web-study/design.md) là đích giao diện Study: `ocean-primary: #0B5F8A`, ưu tiên Inter có sẵn hoặc phông chữ hệ thống, không tải phông từ xa, điều khiển tối thiểu 44px, có chỉ báo tiêu điểm bàn phím rõ, hỗ trợ bàn phím và giảm chuyển động. Không sao chép nguyên mã màu mâu thuẫn từ tài liệu tham khảo.
- HTML mẫu nạp Tailwind và Plus Jakarta Sans từ CDN. Đây là cách dựng của tài sản mẫu, không phải phụ thuộc đã được chấp thuận cho Study Web.
- Nhãn kiểm định WCAG AA ở ảnh là nội dung đồ họa; phiên này chưa đo tương phản hoặc kiểm tra khả năng tiếp cận.

### 1.3. Tác nhân, quyền và đường dẫn

- danh mục màn hình xếp SH-04 vào Shared/Auth/System, dành cho Khách, AC-01, loại Trang, ưu tiên P1, tình trạng `S`.
- API #02 được gọi công khai, không bắt buộc Bearer token. Mã kiểm thử còn xác nhận yêu cầu vẫn được chấp nhận khi gửi `Authorization: Bearer malformed-token`; màn hình không cần token cho bước này.
- `/register/verification` là đường dẫn đề xuất, chưa phải đường dẫn API đã cài đặt. Không mô tả trang này như đang chạy.
- SH-02 là màn hình tiếp theo theo danh mục màn hình. Nút quay lại chỉ thể hiện điều hướng; không cam kết đăng nhập thành công hoặc tài khoản đã được xác minh.

**Điều kiện trước:** theo F01, API #01 phải trả HTTP 201 và SH-04 cần nhận `data.id`/`data.email`; hiện chưa có client route/state hoặc kênh handoff để chuyển hai giá trị đó. Mở đường dẫn trực tiếp có thể thiếu handoff.

**Điều kiện sau:** HTTP 202 cùng `data.status="accepted"` chỉ cho phép báo provider stub đã tiếp nhận lời gọi; không chứng minh email được giao, tài khoản kích hoạt hay email được xác minh. API #02 không cập nhật tài khoản. Theo danh mục, Khách có thể quay lại SH-02. API #03 hiện từ chối user có status khác ACTIVE, nhưng API #01 không đặt status và checked-in DDL không xác nhận live schema; vì vậy chưa thể kết luận tài khoản chưa xác minh được phép hay bị chặn đăng nhập.

### 1.4. Đối chiếu cấu trúc A–F

| Mục | Nội dung bắt buộc | Vị trí trong DD |
|---|---|---|
| A | Tổng quan, actor/quyền, điều kiện trước/sau, route/liên kết, element/event/API, quy tắc và blocker | §1, §1.3, §2–§9, §12 |
| B | Luồng từ mở màn hình tới điều hướng, dữ liệu, API và lỗi | §2–§3, §6 |
| C | Mô tả 12 element, nguồn, hiển thị, trạng thái và event liên kết | §4 |
| D | Trigger/type, precondition, input, xử lý tuần tự, API, output và ngoại lệ cho từng event | §5–§6.4 |
| E | Trạng thái, điều kiện chuyển, SH-03/SH-02 handoff, quyền và route | §7–§9 |
| F | Tiêu chí nghiệm thu và kiểm tra evidence | §14 |
