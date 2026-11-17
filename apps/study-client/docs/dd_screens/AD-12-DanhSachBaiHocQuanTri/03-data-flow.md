# AD-12 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

1. **Vào màn hình:** Admin có thể mở Angular route `/admin/lessons` đã khai báo tới `AD12Page`; browser/runtime chưa xác minh. HTML preview riêng không xử lý navigation.
2. **Authentication/authorization:** client target cần session hợp lệ. Với request #82 hiện tại, shared Bearer/JWT `ADMIN` guard chạy trước parse query và DB. 401/403 là server outcomes; AC-34 permission riêng chưa được kiểm tra bởi source đã rà soát.
3. **Khởi tạo filter:** mockup trình bày keyword, course, type và status. Angular page hiện khởi tạo query rỗng; search/course/type/status controls disabled. Service có thể serialize `course`/`status`; `type` bị backend từ chối. Không giả định UI slug/alias hoặc giá trị mặc định.
4. **Gọi API:** Angular page gọi #82 `GET /api/v1/admin/lessons` bằng Admin Bearer session, ban đầu không query. Catalog cho phép `course`, `status`, `type`; `type` supplied trả 422 theo local source. Không có body. Retry/timeout/idempotency/cache policy chưa được xác định trong source.
5. **Xử lý query:** backend parse `course` thành signed int64 rồi bind vào `course_id`; `status` dùng exact equality. SQL loại `DELETED` và áp dụng thứ tự xác định. Không pagination/count/type/search/join.
6. **Xử lý response:** local success là 200 `ApiEnvelope<Lesson[]>` với list trong `data`; map `name→title`, `sort_order→order`. Empty list là `[]`. Catalog singleton khác local response. Required projection có thể fail nếu legacy row chứa NULL ở `course_id/order/status`, tạo safe 500 + rollback.
7. **Render UI:** Angular template bind loading/error/empty/loaded states và chiếu `id/title/course_id/order/status`; không render `content` hoặc `video_url`. Catalog cardinality, filter mapping, nullability và access còn mở; không có pagination. Empty server result không chứng minh dữ liệu đang chờ đồng bộ.
8. **Tương tác:** search/course/type/status, refresh/reset, Add và pagination chưa được wire. Row “Chi tiết” điều hướng tới AD-13 khi `Lesson.id` là safe JS integer; ID không biểu diễn chính xác được sẽ có control disabled và cảnh báo. AD-13 gọi #83; browser/runtime chưa xác minh. Không mô tả action ngoài contract.
9. **Rời màn hình:** expected AD-13 detail → AD-14 actions → reload #82 theo AC-34. Lịch sử, giữ filter, stale data, row action placement, back behavior và reload strategy chưa được xác nhận.

### Request/response và lỗi #82

- **Request:** `GET /api/v1/admin/lessons`; `Authorization: Bearer <token>`; query `course?: int64`, `status?: string`, `type?: string`; không body. Catalog định nghĩa các query nhưng chưa giải quyết local behavior `type`.
- **Success theo catalog:** `200 ApiEnvelope<Lesson>` (singular).
- **Success theo local source:** `200 ApiEnvelope<Lesson[]>`, direct array `data`; không metadata phân trang.
- **Local error behavior:** 401 unauthenticated, 403 role không hợp lệ; `course` sai/overflow hoặc `type` supplied → 422 `DESIGN_VALIDATION_ERROR`; query/row mapping/projection lỗi → safe 500 và rollback. Không có path param nên #82 không có 404.
- **Retry/timeout/dedup/cache:** GET #82 caller tồn tại trong Angular source; retry/timeout/dedup/cache policy chưa có trong source và để mở.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| Trạng thái | Điều kiện vào | Nội dung/kết quả | Chuyển tiếp / giới hạn |
|---|---|---|---|
| `source-wired; runtime NOT VERIFIED` | Angular router/page/GET #82 caller tồn tại trong checkout | Prototype HTML riêng vẫn là static reference | Không khẳng định browser/deployment runtime. |
| `loading` | Angular page nhận request state qua `adminQueryState` | Loading row trong template | GET ban đầu dùng query rỗng. |
| `loaded` | Local #82 trả `Lesson[]` có rows | Chiếu `id/title/course_id/order/status`; body/video không hiển thị | Safe integer ID links tới AD-13/#83; unsafe ID không navigable. |
| `empty` | Local response `data: []` | Empty result; không đồng nghĩa chờ đồng bộ | Filter controls disabled. |
| `validation-error` | Current `course` sai/overflow hoặc có `type` | Local 422; catalog hiện không liệt kê 422 | Sửa query theo contract; type cần API/source change trước khi retry. |
| `unauthorized` | Token/authentication lỗi | Local/catalog 401 | Session/login recovery policy không được xác định trong Study Web. |
| `forbidden` | Role `ADMIN` không thỏa guard | Local/catalog 403 | AC-34 permission chi tiết còn mở; không bypass bằng client check. |
| `service/network-error` | DB/projection lỗi (500) hoặc transport failure | Backend safe 500 + rollback; network UX chưa có client evidence | Retry/timeout/cancel policy cần contract; không hiện stale success không nguồn. |
| `pagination` (prototype-only) | Mockup hiển thị Previous/`0/0`/Next | Không có page/total từ API | Không thể chuyển thành API paging state trước khi contract thay đổi. |

**Navigation:** expected AD-01/Admin shell → AD-12 → AD-13/#83 → AD-14/#84/#85/#86 → reload #82 theo AC-34. Angular source có route/page/GET #82 caller; row link dùng safe `Lesson.id` để mở AD-13, page AD-13 gọi #83. Browser back, query preservation, post-mutation refresh, duplicate-row handling và stale list policy chưa được quy định; runtime chưa xác minh.

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
