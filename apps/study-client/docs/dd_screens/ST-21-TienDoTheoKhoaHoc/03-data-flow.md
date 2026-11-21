# ST-21 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

1. **Đi vào ST-21:** expected navigation từ ST-20 course link với route `:courseId`. Inventory/API đặt cùng định danh là course ID nhưng chưa quy định cách đổi UI param casing sang `course_id`. Current Study Web không có route/handoff.
2. **Xác thực và lấy context:** expected actor là Student có Bearer session. Route guard, token storage, current-user mapping và recovery behavior chưa có trong Study Web source/API #37.
3. **Kiểm tra path:** nhận `courseId` rồi chuẩn hóa theo catalog `course_id:int64!`. Min/max và behavior khi rỗng, âm, không parse được hoặc ngoài domain chưa có contract; không thêm 400/422.
4. **Gọi API:** với ID hợp lệ theo parser đã được quyết định, expected request là GET #37 kèm Bearer, path `course_id`; không có query/body. Không gọi API Mentor #65/#67 và không gửi user ID.
5. **Đọc response:** chỉ HTTP 200 và `DESIGN_RESOURCE_RETRIEVED` là success theo catalog. Response đang là `ApiEnvelope<UserProfile>`; payload UserProfile không cho phép lấy lesson/course progress, vì vậy UI không được map profile fields thành tiến độ.
6. **Tổng hợp và hiển thị:** AC-18 yêu cầu lesson + quiz + assignment aggregate, nhưng tập dữ liệu, selection policy, công thức và output DTO chưa có. Chỉ khi contract được duyệt mới phân loại unit, tính tỷ lệ và hiển thị thời gian; không dùng empty fallback như API result evidence.
7. **Tương tác:** expected lesson navigation phải mang `lesson_id` qua access gate của ST-10/ST-11; HTML hiện không có lesson list hoặc link. Nút/breadcrumb quay lại ST-20 có href `/student/progress` trong HTML nhưng route runtime absent.
8. **Lỗi:** catalog #37 có 401/403/404/500. Path parse, response parse, timeout/network và retry không có endpoint-specific rule. Giữ lỗi riêng; không biến `404` thành “chưa có tiến độ” nếu chưa có business decision.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

### E.1. Trạng thái

| State | Điều kiện | UI / hành động |
|---|---|---|
| Route/runtime chưa wire | Current Study Web không có ST-21 router | Không khẳng định trang có thể truy cập; status `UNWIRED`. |
| Loading | Expected GET #37 đang chờ | Inventory state; skeleton/layout chưa được thiết kế hoặc xác minh. |
| In progress | API trả progress DTO và rule cho trạng thái chưa hoàn tất được duyệt | Hiện các unit/percent/timestamp đúng mapping; hiện chưa đủ schema. |
| Completed | Contract xác định course complete và API trả evidence tương ứng | Không suy từ màu/mockup; completion rule chưa chốt. |
| Empty | API contract phân biệt course hợp lệ nhưng không có activity | Shape/code/zero-vs-empty chưa chốt; empty HTML chỉ là prototype. |
| Authentication required | HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED` | Giữ code; session recovery/redirect theo app-level policy chưa xác định. |
| Access denied | HTTP 403 `DESIGN_ACCESS_DENIED` | Không lộ progress; access predicate và masking còn mở. |
| Not found | HTTP 404 `DESIGN_RESOURCE_NOT_FOUND` | Không kết luận course absent hay progress absent vì semantics chưa chốt. |
| Internal error | HTTP 500 `DESIGN_INTERNAL_ERROR` | Safe error state; không lộ SQL/stack; retry chưa định nghĩa. |
| Path invalid | `courseId` không parse/range không hợp lệ | Q-07 open; không thêm HTTP/business code ngoài catalog. |
| Transport/parse error | Không có API response hoặc envelope invalid | Client handling chưa có screen contract; không map thành API business code. |

### E.2. Điều hướng và handoff

| From / action | Target | Data dependency | Current status |
|---|---|---|---|
| ST-20 chọn course | ST-21 `/student/progress/:courseId` | `courseId` từ selected course; API path yêu cầu `course_id:int64!` | Expected inventory; API/# route absent. |
| ST-21 chọn lesson row | ST-10 access/start → ST-11 player | `lesson_id`, course context, Student session; API #22–#24 gate theo flow học | Expected inventory; ST-21 loaded row và handoff chưa có source. |
| Breadcrumb/CTA quay lại | ST-20 `/student/progress` | Không khai báo query/body; course ID có thể chỉ thuộc browser history, policy chưa chốt | HTML prototype href; router absent. |
| Header/footer links | Trang tổng quan, courses, terms/privacy/academic/support | Route/access policy | Static `#` / labels; current Study Web destination absent. |

### E.3. Bảo vệ quyền

- API catalog yêu cầu Student Bearer; server cần xác thực principal và course access trước khi trả progress.
- `course_id` từ URL chỉ là resource selector, không chứng minh enrollment, ownership hoặc entitlement.
- Không gửi user ID trong route/query/body cho `/me`; không dùng Mentor #65/#67 để lấp authorization/payload.
- Giữ nguyên catalog 401/403/404/500 và để open câu hỏi masking; không cho browser mở lesson content trực tiếp từ progress record.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #37 theo course_id; liên kết lesson_id → ST-10/11 sau gate.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ST-21](../../screen_stitch/03_student/ST-21_tien-do-theo-khoa-hoc/ST-21.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
