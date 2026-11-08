# AD-12 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

1. **Vào màn hình:** expected Admin mở route `/admin/lessons`, có thể từ vùng Admin hoặc sau khi quay lại từ AD-13/AD-14. Route/client chưa tồn tại trong checkout; HTML preview không xử lý navigation.
2. **Authentication/authorization:** client target cần session hợp lệ. Với request #82 hiện tại, shared Bearer/JWT `ADMIN` guard chạy trước parse query và DB. 401/403 là server outcomes; AC-34 permission riêng chưa được kiểm tra bởi source đã rà soát.
3. **Khởi tạo filter:** mockup trình bày keyword, course, type và status. Không có default/query state client source. Chỉ `course`/`status` có đường xử lý local; `type` hiện bị từ chối. Không giả định UI slug/alias hoặc giá trị mặc định.
4. **Gọi API:** API contract dự kiến #82 `GET /api/v1/admin/lessons`; gửi Bearer token và chỉ query đã được xác nhận. Catalog cho phép `course`, `status`, `type`; current source không nhận được một `type` hợp lệ nào. Không có body. Không có retry/timeout/idempotency/cache policy từ client source.
5. **Xử lý query:** backend parse `course` thành signed int64; bind exact optional `course_id`/`status`; SQL loại `DELETED` và áp dụng thứ tự xác định. Không pagination/count/type/search/join.
6. **Xử lý response:** local success là 200 `ApiEnvelope<Lesson[]>` với list trong `data`; map `name→title`, `sort_order→order`. Empty list là `[]`. Catalog singleton khác local response. Required projection có thể fail nếu legacy row chứa NULL ở `course_id/order/status`, tạo safe 500 + rollback.
7. **Render UI:** current HTML luôn là empty-state prototype; không bind API. Tương lai chỉ có thể render fields response-backed sau khi owner giải quyết cardinality, filter mapping, nullability, access và pagination. Empty server result không chứng minh dữ liệu đang chờ đồng bộ.
8. **Tương tác:** refresh/reset cần gọi lại #82 sau khi filter contract rõ; search/type/status mapping hiện bị chặn. CTA Add không có API. Khi có row, `Lesson.id` là dữ liệu handoff candidate tới AD-13/#83; không mô tả action ngoài contract.
9. **Rời màn hình:** expected AD-13 detail → AD-14 actions → reload #82 theo AC-34. Lịch sử, giữ filter, stale data, row action placement, back behavior và reload strategy chưa được xác nhận.

### Request/response và lỗi #82

- **Request:** `GET /api/v1/admin/lessons`; `Authorization: Bearer <token>`; query `course?: int64`, `status?: string`, `type?: string`; không body. Catalog định nghĩa các query nhưng chưa giải quyết local behavior `type`.
- **Success theo catalog:** `200 ApiEnvelope<Lesson>` (singular).
- **Success theo local source:** `200 ApiEnvelope<Lesson[]>`, direct array `data`; không metadata phân trang.
- **Local error behavior:** 401 unauthenticated, 403 role không hợp lệ; `course` sai/overflow hoặc `type` supplied → 422 `DESIGN_VALIDATION_ERROR`; query/row mapping/projection lỗi → safe 500 và rollback. Không có path param nên #82 không có 404.
- **Retry/timeout/dedup/cache:** chưa có Study Web caller hoặc policy source; để mở, không khẳng định.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| Trạng thái | Điều kiện vào | Nội dung/kết quả | Chuyển tiếp / giới hạn |
|---|---|---|---|
| `UNWIRED` | Checkout hiện không có Study Web source/router/client | Prototype tĩnh; không có runtime state | Chỉ rời trạng thái khi client được implement; hiện runtime `NOT VERIFIED`. |
| `loading` | Target gửi #82 sau auth/query chuẩn bị | Loading state cần được thiết kế; không có trong runtime | Success→`ready`/`empty`; server errors→error states. |
| `ready` | Local #82 trả 200 có Lesson rows sau khi cardinality được chốt | Map `id/course_id/title/content/video_url/order/status`; một số cột mockup không có nguồn | Row detail→AD-13/#83 bằng numeric `id`; detail route/permission còn phải xác nhận. |
| `empty` | Local response `data: []` | Empty result; không đồng nghĩa chờ đồng bộ | Filter update/refresh có thể gọi lại #82 sau khi mapping được duyệt. |
| `validation-error` | Current `course` sai/overflow hoặc có `type` | Local 422; catalog hiện không liệt kê 422 | Sửa query theo contract; type cần API/source change trước khi retry. |
| `unauthorized` | Token/authentication lỗi | Local/catalog 401 | Session/login recovery policy không được xác định trong Study Web. |
| `forbidden` | Role `ADMIN` không thỏa guard | Local/catalog 403 | AC-34 permission chi tiết còn mở; không bypass bằng client check. |
| `service/network-error` | DB/projection lỗi (500) hoặc transport failure | Backend safe 500 + rollback; network UX chưa có client evidence | Retry/timeout/cancel policy cần contract; không hiện stale success không nguồn. |
| `pagination` (prototype-only) | Mockup hiển thị Previous/`0/0`/Next | Không có page/total từ API | Không thể chuyển thành API paging state trước khi contract thay đổi. |

**Navigation:** expected AD-01/Admin shell → AD-12 → AD-13/#83 → AD-14/#84/#85/#86 → reload #82 theo AC-34. Các route/action là design linkage. Không có current frontend route. Browser back, query preservation, post-mutation refresh, duplicate-row handling và stale list policy chưa được quy định.

**Responsive/accessibility:** áp dụng target `.agents/web-study/design.md` khi implementation design được triển khai; prototype sizing/type/tokens không đồng nhất. Tài liệu không khẳng định đã kiểm tra keyboard, screen reader, responsive layout, focus, hover hay contrast trong app runtime.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #82; catalog singleton `Lesson` khác local `Lesson[]`; course cần int64 nhưng mockup dùng slug, type trả 422, status exact raw string, không có pagination; CTA Add chưa có API.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [AD-12](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
