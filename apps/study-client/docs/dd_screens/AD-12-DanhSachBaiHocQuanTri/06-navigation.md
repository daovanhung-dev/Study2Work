# AD-12 — Navigation

## 1. Route definition
- Current route in inventory: `/admin/lessons`
- Status: Angular router source khai báo `/admin/lessons` → `AD12Page`; browser/runtime `NOT VERIFIED`.
- Route params/types: Route không có param; browser/runtime vẫn chưa xác minh.
- Query params/defaults: preserve the inventory route string; detailed parsing rules only from source DD.
- Route guards: see source DD/API contract; do not create role policy.

## 2. Điểm vào
| From screen/route | Trigger | Params | Guard / fallback |
|---|---|---|---|
| [AD-07](../AD-07-ChiTietKhoaHocQuanTri/00-overview.md), [AD-14](../AD-14-SuaDoiTrangThaiXoaBaiHoc/00-overview.md) | Theo DD nguồn/inventory | Theo source; không suy diễn | Xem source DD; route chưa xác nhận runtime |

## 3. Điểm ra
| Destination | Trigger | Params | Điều kiện |
|---|---|---|---|
| [AD-13](../AD-13-ChiTietBaiHocQuanTri/00-overview.md) | Source event/inventory navigation | Theo source DD | Expected links; runtime chưa verify |

## 4. Back / refresh / deep link
- Back behavior: xem source DD; không mặc định browser history.
- Preserve filters/scroll/form state: chỉ nếu source có nêu, nếu không `CẦN_XÁC_NHẬN`.
- Refresh/direct URL: route trong inventory không chứng minh runtime.
- Invalid/missing ID: theo source DD/backend contract; không tự tạo validation.
- Not authenticated/authorized: theo source role guard; xem [Business Rules](05-business-rules.md).

## 5. Diagram
```mermaid
flowchart LR
  S0["AD-12 Danh sách bài học quản trị"] --> S1["AD-13"]
```

## Source navigation and flow detail

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| Trạng thái | Điều kiện vào | Nội dung/kết quả | Chuyển tiếp / giới hạn |
|---|---|---|---|
| `source-wired; runtime NOT VERIFIED` | Angular router/page/GET #82 caller có trong checkout | Prototype HTML chỉ là static reference | Không khẳng định browser/deployment runtime. |
| `loading` | Angular page nhận request state qua `adminQueryState` | Loading row trong template | Request ban đầu không có query. |
| `loaded` | Local #82 trả Lesson rows | Chiếu `id/title/course_id/order/status`; content/video không hiển thị | Safe integer ID links tới AD-13/#83; unsafe ID không navigable. |
| `empty` | Local response `data: []` | Empty result; không đồng nghĩa chờ đồng bộ | Filter controls disabled. |
| `validation-error` | Current `course` sai/overflow hoặc có `type` | Local 422; catalog hiện không liệt kê 422 | Sửa query theo contract; type cần API/source change trước khi retry. |
| `unauthorized` | Token/authentication lỗi | Local/catalog 401 | Session/login recovery policy không được xác định trong Study Web. |
| `forbidden` | Role `ADMIN` không thỏa guard | Local/catalog 403 | AC-34 permission chi tiết còn mở; không bypass bằng client check. |
| `service/network-error` | DB/projection lỗi (500) hoặc transport failure | Backend safe 500 + rollback; network UX chưa có client evidence | Retry/timeout/cancel policy cần contract; không hiện stale success không nguồn. |
| `pagination` (prototype-only) | Mockup hiển thị Previous/`0/0`/Next | Không có page/total từ API | Không thể chuyển thành API paging state trước khi contract thay đổi. |

**Navigation:** expected AD-01/Admin shell → AD-12 → AD-13/#83 → AD-14/#84/#85/#86 → reload #82 theo AC-34. Angular source có route/page/GET #82 caller; row link mở AD-13 cho safe `Lesson.id`, rồi AD-13 gọi #83. Browser back, query preservation, post-mutation refresh, duplicate-row handling và stale list policy chưa được quy định; runtime chưa xác minh.

**Responsive/accessibility:** áp dụng target `.agents/web-study/design.md` khi implementation design được triển khai; prototype sizing/type/tokens không đồng nhất. Tài liệu không khẳng định đã kiểm tra keyboard, screen reader, responsive layout, focus, hover hay contrast trong app runtime.

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

1. **Vào màn hình:** Admin có thể mở Angular route `/admin/lessons` đã khai báo tới `AD12Page`; browser/runtime chưa xác minh. HTML preview riêng không xử lý navigation.
2. **Authentication/authorization:** client target cần session hợp lệ. Với request #82 hiện tại, shared Bearer/JWT `ADMIN` guard chạy trước parse query và DB. 401/403 là server outcomes; AC-34 permission riêng chưa được kiểm tra bởi source đã rà soát.
3. **Khởi tạo filter:** mockup trình bày keyword, course, type và status. Angular current source khởi tạo query rỗng; Course ID raw text có thể Apply. Không giả định UI slug/alias hoặc giá trị mặc định.
4. **Gọi API:** API contract dự kiến #82 `GET /api/v1/admin/lessons`; gửi Bearer token và chỉ query đã được xác nhận. Catalog cho phép `course`, `status`, `type`; current source gửi `course` raw text từ Course ID, không gửi `type`/`status`/search. Không có body. Refresh lặp applied query; Reset xóa query. Không có retry/timeout/idempotency/cache policy từ client source.
5. **Xử lý query:** backend parse `course` thành signed int64; bind exact optional `course_id`/`status`; SQL loại `DELETED` và áp dụng thứ tự xác định. Không pagination/count/type/search/join.
6. **Xử lý response:** local success là 200 `ApiEnvelope<Lesson[]>` với list trong `data`; map `name→title`, `sort_order→order`. Empty list là `[]`. Catalog singleton khác local response. Required projection có thể fail nếu legacy row chứa NULL ở `course_id/order/status`, tạo safe 500 + rollback.
7. **Render UI:** Angular template bind loading/error/empty/loaded states và chiếu `id/title/course_id/order/status`; không render `content` hoặc `video_url`. Catalog cardinality, filter mapping, nullability và access còn mở; không có pagination. Empty server result không chứng minh dữ liệu đang chờ đồng bộ.
8. **Tương tác:** Apply/refresh/reset gọi lại #82 theo raw Course ID hiện hành; search/type/status mapping hiện bị chặn. CTA Add không có API. Khi có row, `Lesson.id` là dữ liệu handoff candidate tới AD-13/#83; không mô tả action ngoài contract.
9. **Rời màn hình:** expected AD-13 detail → AD-14 actions → reload #82 theo AC-34. Lịch sử, giữ filter, stale data, row action placement, back behavior và reload strategy chưa được xác nhận.

### Request/response và lỗi #82

- **Request:** `GET /api/v1/admin/lessons`; `Authorization: Bearer <token>`; query `course?: int64`, `status?: string`, `type?: string`; không body. Catalog định nghĩa các query nhưng chưa giải quyết local behavior `type`.
- **Success theo catalog:** `200 ApiEnvelope<Lesson>` (singular).
- **Success theo local source:** `200 ApiEnvelope<Lesson[]>`, direct array `data`; không metadata phân trang.
- **Local error behavior:** 401 unauthenticated, 403 role không hợp lệ; `course` sai/overflow hoặc `type` supplied → 422 `DESIGN_VALIDATION_ERROR`; query/row mapping/projection lỗi → safe 500 và rollback. Không có path param nên #82 không có 404.
- **Retry/timeout/dedup/cache:** GET #82 caller tồn tại trong Angular source; retry/timeout/dedup/cache policy chưa có trong source và để mở.
