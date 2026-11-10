# ST-06 — Thực hiện thanh toán · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-06` |
| Module | Student |
| Route | `/student/pay/:orderId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái thiết kế:** `DD BLOCKED` · **Trạng thái triển khai:** `IMPLEMENTATION BLOCKED` · **Runtime:** `NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-06.md](../../screen_stitch/03_student/ST-06_thuc-hien-thanh-toan/ST-06.md), [ST-06_PLAN.md](../../screen_stitch/03_student/ST-06_thuc-hien-thanh-toan/ST-06_PLAN.md), [ST-06_markers.json](../../screen_stitch/03_student/ST-06_thuc-hien-thanh-toan/ST-06_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Theo dõi trạng thái thanh toán và điều hướng ngoài nếu gateway xác nhận; retry chỉ khi có quy tắc an toàn được duyệt.
- In-scope: POST #17 → nhận operation_id → GET #18 theo điều kiện chốt; client callback không phải bằng chứng đã paid.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-12 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Theo dõi trạng thái thanh toán và điều hướng ngoài nếu gateway xác nhận; retry chỉ khi có quy tắc an toàn được duyệt. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #17, #18
- Liên kết màn hình dự kiến: [ST-07](../ST-07-KetQuaDangKyKhoaHoc/00-overview.md), [SH-07](../SH-07-TheoDoiTacVuBatDongBo/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | pending/running/failed/cancelled/succeeded |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-06 source screen.png](../../screen_stitch/03_student/ST-06_thuc-hien-thanh-toan/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-06_thuc-hien-thanh-toan/screen_annotated.png))
- Luồng: POST #17 → nhận operation_id → GET #18 theo điều kiện chốt; client callback không phải bằng chứng đã paid.
- Priority: P2; Gate/source status: **#17/#18 D; DD BLOCKED**; **BLOCK:** Order/provider handoff, gateway/payment verification, Operation UUID/int64 + owner policy/lifecycle/polling, retry/idempotency chưa chốt; Study Web và #17/#18 UNWIRED; prototype không có payment action, return link thiếu ID

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-06 — Thực hiện thanh toán

> **Trạng thái thiết kế:** `DD BLOCKED` · **Trạng thái triển khai:** `IMPLEMENTATION BLOCKED` · **Runtime:** `NOT VERIFIED`
>
> Phạm vi, thứ tự authoring, nguồn ảnh và blocker được ghi tại [ST-06_PLAN.md](../../screen_stitch/03_student/ST-06_thuc-hien-thanh-toan/ST-06_PLAN.md). `screen_annotated.png` được tạo từ [screen_rendered_from_html.png](../../screen_stitch/03_student/ST-06_thuc-hien-thanh-toan/screen_rendered_from_html.png); ảnh gốc `screen.png` được giữ nguyên.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-06 — Thực hiện thanh toán |
| Mục tiêu dự kiến | Trong flow paid của AC-12, khởi tạo payment theo Order, theo dõi Operation nếu contract cho phép và chỉ chuyển sang kết quả ghi danh sau khi server/gateway xác minh thanh toán thành công. |
| Actor / quyền | Student đã đăng nhập theo AC-12 và API #17. API #18 yêu cầu Bearer JWT; quyền owner-only hay owner/Admin chưa thống nhất. |
| Route | `/student/pay/:orderId` là route đề xuất trong inventory; chưa có router Study Web để xác minh hoặc thực thi. |
| Đầu vào | `orderId` từ ST-05 là route candidate. API #17 nhận body `order_id:int64`; API #18 nhận path `operation_id` nhưng kiểu `int64` trong API row mâu thuẫn UUID của reusable Operation schema và AC diagrams. |
| Điều kiện trước | ST-05 phải có Order hợp lệ; Student session hợp lệ; Order ownership/eligibility, provider, gateway policy và Order ID mapping phải được chốt. API #16 hiện chưa wired nên không có Order runtime được xác minh. |
| Kết quả sau | Payment confirmed bởi trusted server/gateway → chuyển ST-07 để tiếp tục kết quả enrollment theo AC-12. Failed/cancelled → dừng flow. HTTP 202 của #17 chỉ xác nhận Operation được accepted, không xác nhận paid. |
| Màn hình liên quan | Trước: ST-05. Sau: ST-07 và SH-07 operation tracking. Prototype CTA quay về checkout nhưng dùng route placeholder literal, không truyền ID hợp lệ. |
| API liên quan | #17 `POST /api/v1/payments` — catalog/Draft, `DESIGN_ONLY`. #18 `GET /api/v1/operations/{operation_id}` — catalog/Draft, `DESIGN_ONLY`; AC-12 có node #18 nhưng không nối vào sequence. |
| Hiện trạng | HTML là trang tĩnh báo không có thông tin thanh toán; không có order/operation data, payment action, polling, gateway callback, API client hoặc event handler. `screen.png` 1280×1024 gần như trống; ảnh HTML render được lưu riêng. |

### Expected behavior và current behavior

**Expected behavior — inventory/AC-12:** từ Order của ST-05, thực hiện API #17 với `order_id` và provider đã được phê duyệt; nhận Operation; chỉ poll API #18 nếu ID, ownership và polling contract được thống nhất; dùng kết quả tin cậy của server/gateway để phân biệt paid với pending, failed hoặc cancelled; chỉ sau đó mới chuyển tiếp ST-07. Inventory nêu trạng thái `pending/running/failed/cancelled/succeeded` và yêu cầu retry an toàn, nhưng không có nguồn xác nhận các tên trạng thái API, trạng thái retryable hay idempotency.

**Current behavior — source/assets:** `code.html` hiển thị public header, breadcrumb, page title, card có icon `credit_card`, title, thông báo “Chưa có thông tin thanh toán để hiển thị.”, copy nói chưa tìm thấy giao dịch hoặc giao dịch đã kết thúc, CTA và footer. Không có ID, amount, provider, payment status từ server, operation ID, transaction code hay payment result. HTML có 15 anchor tĩnh nhưng không có control, fetch/XHR, event attribute hoặc listener. CTA dùng literal `/student/checkout/:courseId`; breadcrumb “Kiểm tra đơn hàng” dùng `/student/checkout` không có ID. Original PNG không hiển thị HTML; ảnh render và annotation tách riêng.

**DISCREPANCY:** Static page không chứng minh payment thất bại, cancelled hay đã kết thúc; đó chỉ là prototype copy. Inventory muốn status tracking/retry, còn HTML chỉ có unavailable state. AC-12 requires Student authentication, trong khi prototype hiện Sign In/Sign Up công khai. Route/payment behavior của Study Web chưa được wire.

### Quy tắc nghiệp vụ và bảo mật

- API #17 cần Bearer JWT, role Student, body `{order_id:int64!, provider:string!}`. Không thêm `user_id` hoặc field khác.
- API #17 trả 202 `DESIGN_OPERATION_ACCEPTED`, không phải payment success. Không chuyển ST-07 hoặc đánh dấu paid chỉ từ HTTP 202, URL return, browser event hay client callback.
- Provider field của #17 là `string`; #16 dùng `payment_provider:PaymentProvider`. Giá trị enum, case/allowlist, truyền tiếp và adapter chưa được xác nhận.
- API #18 ID conflict: catalog row `operation_id:int64`; global convention, reusable `Operation.id` và AC-12 đều UUID. Không parse/convert/synthesize ID trước khi contract owner chốt một kiểu.
- API #18 access conflict: owner-only theo API row/AC diagrams, owner/Admin theo operation tracking summary. Không query hoặc hiển thị Operation cho người khác khi policy chưa chốt.
- `OperationKind`, `OperationStatus`, PaymentStatus, result fields per job, Study storage, retention, polling and terminal rules are unresolved. `Operation.result` optional Payment does not establish a payment result for this flow.
- Inventory “safe retry” chưa được hỗ trợ bởi idempotency key, duplicate policy hoặc retryable-status contract. Không tự retry #17 hoặc cho phép repeat thao tác.
- Checked-in DDL có `payments` nhưng không có `payments.order_id`, `orders` hay `operations`; SQL cho `payments.user_id/course_id` nullable trong khi bảng thiết kế nói bắt buộc. Không coi DDL là live database evidence.
- Study Web guide yêu cầu Inter/system font, không thêm remote imports; prototype dùng Plus Jakarta Sans, Google Material Symbols và Tailwind CDN. Không có ngoại lệ thiết kế được ghi nhận.
