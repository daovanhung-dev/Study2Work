# ST-05 — Kiểm tra đơn hàng / checkout · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-05` |
| Module | Student |
| Route | `/student/checkout/:courseId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái thiết kế:** `DD BLOCKED` · **Trạng thái triển khai:** `IMPLEMENTATION BLOCKED` · **Runtime:** `NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-05.md](../../screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/ST-05.md), [ST-05_PLAN.md](../../screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/ST-05_PLAN.md), [ST-05_markers.json](../../screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/ST-05_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Hiển thị khoản tiền, nhà cung cấp, xác nhận mua trước khi tạo Order.
- In-scope: Revalidate #8; POST #16 một lần theo action người dùng; lưu order_id từ response.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-12 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Hiển thị khoản tiền, nhà cung cấp, xác nhận mua trước khi tạo Order. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #08, #16
- Liên kết màn hình dự kiến: [ST-06](../ST-06-ThucHienThanhToan/00-overview.md), [ST-04](../ST-04-KiemTraGhiDanhTruocDangKy/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | confirming/order-creating/422/order-error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-05 source screen.png](../../screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/screen_annotated.png))
- Luồng: Revalidate #8; POST #16 một lần theo action người dùng; lưu order_id từ response.
- Priority: P2; Gate/source status: **#08 R; #16 D; DD BLOCKED**; **BLOCK:** Order schema, provider/amount/currency policy và idempotency chưa source-backed; inventory revalidation lần hai chưa được AC-12 đặt thứ tự; Study Web UNWIRED; HTML chưa có confirm UI

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-05 — Kiểm tra đơn hàng / checkout

> **Trạng thái thiết kế:** `DD BLOCKED` · **Trạng thái triển khai:** `IMPLEMENTATION BLOCKED` · **Runtime:** `NOT VERIFIED`
>
> Phạm vi, thứ tự authoring, nguồn ảnh và blocker được ghi tại [ST-05_PLAN.md](../../screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/ST-05_PLAN.md). `screen_annotated.png` được tạo từ [screen_rendered_from_html.png](../../screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/screen_rendered_from_html.png), không phải từ ảnh nguyên trạng `screen.png`.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-05 — Kiểm tra đơn hàng / checkout |
| Mục tiêu dự kiến | Trong nhánh paid của AC-12, cho Student xem điều khoản đơn hàng đã được xác nhận, yêu cầu xác nhận tường minh, rồi tạo Order qua API #16 và chuyển tiếp sang ST-06. Contract về giá, tiền tệ, provider và Order persistence hiện chưa đủ để triển khai. |
| Actor / quyền | Student đã đăng nhập theo tiền điều kiện AC-12 và API #16. API #08 khai báo Public. Study Web hiện không có route hoặc session guard cho màn hình này. |
| Route | `/student/checkout/:courseId` là route đề xuất trong inventory; chưa có router Study Web để xác minh hoặc chạy. |
| Đầu vào | `courseId` từ route trước ST-04 là đầu vào thiết kế. API #08 và #16 cần `course_id:int64`; quy tắc parse/đổi tên route value và giữ ID qua điều hướng chưa được định nghĩa cho client. |
| Điều kiện trước | AC-12 yêu cầu Student đăng nhập, course tồn tại và đi tới nhánh trả phí. Inventory yêu cầu đọc lại API #08 ở ST-05. Thứ tự revalidation thứ hai so với bước #15 trong AC-12 và chính sách khi giá thay đổi chưa được chốt. |
| Kết quả sau | Theo inventory, sau xác nhận hợp lệ gọi #16 một lần cho mỗi thao tác người dùng và giữ `order_id`. Response #16 định nghĩa `data.id`; quan hệ `data.id` → `order_id` dùng cho #17 cần được xác nhận trước khi handoff ST-06. |
| Màn hình liên quan | Trước: ST-04 nhánh paid. Sau: ST-06 để khởi tạo/theo dõi payment; quay lại ST-04 theo inventory. Prototype hiện lại dẫn CTA về `/courses` và không giữ course ID. |
| API liên quan | #08 `GET /api/v1/courses/{course_id}` — source-backed, read-only. #16 `POST /api/v1/orders` — contract trong catalog/AC-12 và Draft DD, `DESIGN_ONLY`, chưa wired. API #17 là bước payment riêng thuộc ST-06. |
| Hiện trạng | HTML là trang tĩnh báo không thể bắt đầu thanh toán. Không có dữ liệu course/order, xác nhận, API client hoặc event handler. `screen.png` gần như trống; ảnh render HTML được lưu riêng. |

### Expected behavior và current behavior

**Expected behavior — inventory/AC-12:** Student đi vào nhánh trả phí từ ST-04; #08 được revalidate; sau khi xem thông tin Order và các điều khoản đã được phê duyệt, Student xác nhận rõ ràng; UI gửi một request #16; chỉ sau response thành công mới nhận diện Order và chuyển tới ST-06 theo contract đã được xác nhận.

**Current behavior — source/assets:** `code.html` hiển thị shell công khai, breadcrumb, card trạng thái thanh toán chưa thể bắt đầu, CTA và footer. Không có amount, currency, provider, course ID, order data, confirm control hoặc API call. HTML không có form/button/input, fetch/XHR hay event listener. `screen.png` 1280×1024 gần như chỉ có nền/dải màu; `screen_rendered_from_html.png` là ảnh dẫn xuất riêng từ HTML; hai ảnh nguồn không bị thay đổi.

**DISCREPANCY:** Inventory đòi hỏi xác nhận trước POST #16 nhưng prototype chỉ hiển thị trạng thái unavailable. AC-12 yêu cầu Student đăng nhập trong khi prototype hiển thị Đăng nhập/Đăng ký. Inventory yêu cầu revalidate #08, nhưng AC-12 chỉ đặt #08 trước #15/nhánh paid-free, không mô tả lần gọi thứ hai hoặc stale-price behavior. Các khác biệt này vẫn mở.

### Quy tắc nghiệp vụ và bảo mật

- Chỉ nhánh paid theo AC-12 được gọi #16. AC-12 bỏ qua Order/Payment cho nhánh free; API #16 cũng được catalog đánh dấu Conditional.
- #16 yêu cầu Bearer JWT và role Student. Không xem public shell hoặc route ẩn danh là xác thực.
- #08 trả `Course.price` nhưng không có currency hoặc rule xác định free/paid, eligibility hay amount cuối cùng. Không tự format giá/đổi tiền hoặc quyết định nhánh từ một giá trị cụ thể.
- `PaymentProvider` là enum type bắt buộc trong request nhưng member values và ý nghĩa chưa được phê duyệt. Không tạo danh sách provider hoặc lựa chọn mặc định.
- Logical Order tạo mới có `status=PENDING` theo AC-12. Chưa có physical `orders` table trong ERD V1/checked-in `DB.sql`; không dùng `payments` thay thế.
- API #16 không định nghĩa transaction/rollback, retry, idempotency, duplicate handling hoặc direct-call behavior cho free/unpublished/already-enrolled course. Không thêm 404/409/503.
- Không chuyển sang ST-06 dựa trên client callback. API #17/#18, payment verification và ID continuity là downstream design-only.
- API #18 catalog khai báo `operation_id:int64` trong khi node AC-12 thể hiện UUID; node #18 không nối trong sequence. Đây là downstream blocker cho ST-06, không phải dữ liệu tạo tại ST-05.
