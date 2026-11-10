# AD-15 — Navigation

## 1. Route definition
- Current route in inventory: `/admin/quizzes`
- Status: candidate/design route; Study Web `UNWIRED` unless source code proves otherwise.
- Route params/types: Không có route param được biểu diễn trong inventory string; route runtime vẫn chưa xác minh.
- Query params/defaults: preserve the inventory route string; detailed parsing rules only from source DD.
- Route guards: see source DD/API contract; do not create role policy.

## 2. Điểm vào
| From screen/route | Trigger | Params | Guard / fallback |
|---|---|---|---|
| [AD-16](../AD-16-TaoChinhSuaQuiz/00-overview.md), [AD-17](../AD-17-ThongKeBaiKiemTra/00-overview.md), [AD-18](../AD-18-XacNhanXoaBaiKiemTra/00-overview.md) | Theo DD nguồn/inventory | Theo source; không suy diễn | Xem source DD; route chưa xác nhận runtime |

## 3. Điểm ra
| Destination | Trigger | Params | Điều kiện |
|---|---|---|---|
| [AD-16](../AD-16-TaoChinhSuaQuiz/00-overview.md), [AD-17](../AD-17-ThongKeBaiKiemTra/00-overview.md), [AD-18](../AD-18-XacNhanXoaBaiKiemTra/00-overview.md) | Source event/inventory navigation | Theo source DD | Expected links; runtime chưa verify |

## 4. Back / refresh / deep link
- Back behavior: xem source DD; không mặc định browser history.
- Preserve filters/scroll/form state: chỉ nếu source có nêu, nếu không `CẦN_XÁC_NHẬN`.
- Refresh/direct URL: route trong inventory không chứng minh runtime.
- Invalid/missing ID: theo source DD/backend contract; không tự tạo validation.
- Not authenticated/authorized: theo source role guard; xem [Business Rules](05-business-rules.md).

## 5. Diagram
```mermaid
flowchart LR
  S0["AD-15 Danh sách bài kiểm tra"] --> S1["AD-16"]
  S0["AD-15 Danh sách bài kiểm tra"] --> S2["AD-17"]
  S0["AD-15 Danh sách bài kiểm tra"] --> S3["AD-18"]
```

## Source navigation and flow detail

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

### Trạng thái

| State | Điều kiện | Hiện tại / đích |
|---|---|---|
| `static-prototype` | Mở `code.html` như hiện có. | Có thật trong asset; không fetch. Controls có thể disabled hoặc chỉ là static. |
| `loading` | Client candidate bắt đầu #87 sau khi route/quyền/contract được duyệt. | Target; chưa có source Study Web. |
| `ready` | API trả collection có item theo response contract đã thống nhất. | Target; không được render field chưa có mapping. |
| `empty` | API trả collection rỗng hợp lệ. | Local candidate #87 trả 200/`items=[]`; không gắn nhãn sync failure. |
| `filtered-empty` | Filter được duyệt, request hợp lệ nhưng không có item. | Chưa phân biệt trong prototype/API; UI copy cần được chốt. |
| `unauthenticated` | API 401. | Error source-backed; recovery theo auth shell contract, chưa mô tả thêm. |
| `forbidden` | API 403. | Error source-backed; quyền quiz-management chưa được map vào source. |
| `validation-error` | Local parser 422 với course/page invalid. | Local behavior; catalog chưa liệt kê 422. |
| `service-error` | API 500 hoặc lỗi query/projection. | Source-backed local; retry/retention policy chưa có. |
| `network-error` | Request không có response. | Không có client source/policy; hành vi chờ contract chung. |

### Điều hướng và dữ liệu trao đổi

| Từ | Sự kiện/điều kiện | Đích | Dữ liệu candidate | Trạng thái xác minh |
|---|---|---|---|---|
| Admin shell | Mở `/admin/quizzes` | AD-15 | Session/Admin identity; route và permission guard | Route chưa tồn tại trong Study Web checkout. |
| AD-15 | Create #88 | AD-16 | Chưa có quiz ID; query/filter carry-over chưa chốt. | Expected theo AC-35, CTA hiện disabled. |
| AD-15 row | Update #89 | AD-16 | Quiz ID theo response contract đã duyệt. | Row action không hiện ở empty screenshot; GET detail/schema thiếu. |
| AD-15 row | Statistics #91 | AD-17 | Quiz ID theo response contract đã duyệt. | Expected; #91 response chưa chứng minh analytics fields. |
| AD-15 row | Delete #90 | AD-18 | Quiz ID theo response contract đã duyệt. | Expected; delete/attempt policy thuộc AD-18. |
| AD-16/17/18 | Quay lại danh sách | AD-15 | Filter/page/history preservation chưa được quy định. | Không tự đặt cache invalidation hoặc success reload. |

Phiên hết hạn, back behavior, deep-link authorization, query-string persistence, duplicate click prevention và concurrent refresh behavior cần kế thừa hoặc chờ app-level contract; không có evidence để chỉ định riêng tại AD-15.

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### Luồng AC-35 và ranh giới

```mermaid
flowchart LR
  A[Admin được cấp quiz-management permission] --> B[AD-15: mở danh sách]
  B -. candidate GET #87, chưa wire .-> C{Danh sách được trả?}
  C -->|Create #88| D[AD-16]
  C -->|Update #89| D
  C -->|Statistics #91| E[AD-17]
  C -->|Delete #90| F[AD-18]
```

Sơ đồ thể hiện expected handoff theo AC-35. Route, quyền chi tiết, data mapping và các click hiện chưa có UI implementation evidence. Không gọi các mutation/statistics API từ màn hình danh sách khi chưa chuyển sang màn hình/luồng tương ứng.

### EV-01 — Mở màn hình và tải danh sách (Load, candidate)

1. **Điều kiện/input:** entry candidate từ Admin shell vào `/admin/quizzes`; session phải có Bearer JWT. AC-35 yêu cầu quiz-management permission. Route guard và cách biểu diễn permission chưa có source.
2. **Khởi tạo:** nếu owner duyệt contract và client được wire, tạo trạng thái loading. Chỉ tạo query từ filter có mapping đã duyệt. API hiện không khai báo search, size hay sort.
3. **Request candidate:** `GET /api/v1/admin/quizzes`; headers `Authorization: Bearer <JWT>`; không body. Query trực tiếp catalog: `course?:int64`, `status?:string`, `page?:int32`. Không gửi course slug hoặc giá trị search; không gửi `page=0`.
4. **Server current behavior:** shared guard kiểm tra `ADMIN` trước validate query/DB; `course` parse signed int64; `page` parse signed int32 >=1/default 1; `status` không trim/normalize/enum-check. Local count/list sử dụng exact filters, bỏ `DELETED`, size 20, `id ASC`.
5. **Success mapping:** HTTP 200 common envelope có `data.items` và `data.pagination` ở local source. Catalog lại mô tả `data: Quiz`; cho đến khi được giải quyết, không chốt DTO/state table row. Source item gồm `id`, `course_id`, `title`, `duration_minutes?`, `passing_score`, `questions=[]`.
6. **State:** request thành công với item → candidate ready; `items=[]` → empty; `total_pages=0` được local source khi không có kết quả. Prototype `0/0` không phân biệt empty và not-synced.
7. **Lỗi:** 401 yêu cầu xử lý phiên theo auth flow chung; 403 access denied; 422 có thể phát sinh từ local parser dù catalog không khai báo; 500 safe internal error; lỗi mạng/timeout chưa có policy. Không tự retry.
8. **Output:** chỉ sau contract/route approval mới render các field có nguồn. Không tạo fallback course title/code/count/status từ mockup. Runtime hiện: `UNWIRED`.

### EV-02 — Nhập tên/mã tìm kiếm (Input, chưa được hỗ trợ)

- **Trigger/input:** marker #22; chuỗi do Admin nhập. HTML hiện không gắn listener hoặc API request.
- **Validation/processing:** không có giới hạn/trim/debounce contract được tìm thấy. Không suy ra quy tắc từ placeholder.
- **API:** #87 không có query `q`, `name` hay `code`; không gửi giá trị tìm kiếm trong request.
- **Kết quả:** không đổi danh sách. Control hiện chỉ là static prototype input; muốn bật tìm kiếm cần API/query contract và UI state design được phê duyệt.

### EV-03 — Chọn khóa học (Change, mapping bị chặn)

- **Trigger/input:** marker #23; prototype option values là slug như `cs-foundations`, `frontend-eng`.
- **Validation:** #87 nhận `course` signed int64, nhưng không có source map từ slug sang numeric `course_id` hoặc options loader. Không parse slug thành ID.
- **Request/state:** không gửi request cho đến có option source/mapping; filter update/page reset/cache behavior chưa xác định.
- **Kết quả:** không lọc theo slug. Khi được wire, chỉ dùng numeric ID và response mapping đã duyệt.

### EV-04 — Chọn trạng thái (Change, enum chưa được chốt)

- **Trigger/input:** marker #24; prototype values `draft`, `active`, `closed`.
- **Current backend:** giữ raw `status` và so khớp exact text; không trim, case-normalize hoặc validate enum ở module #87.
- **Xử lý:** không tự đổi `active` thành một giá trị khác hoặc thêm mapping từ giao diện. Không gọi API cho đến khi status enum/casing và option source được duyệt.
- **Kết quả:** behavior filter hiện không hoạt động. Quy tắc reset trang/cache sau đổi filter chưa được xác nhận.

### EV-05 — Refresh danh sách (Click, hiện chỉ là animation)

- **Trigger:** marker #25 hoặc #37. Hai control trong `code.html` chỉ xoay icon trong 800 ms; không có fetch.
- **Candidate khi wire:** có thể yêu cầu GET #87 với query hiện hành đã được duyệt. API không quy định retry, deduplication, timeout, cache hay giữ trang/filter khi refresh.
- **Success/error:** phải dùng response/error mapping được owner chốt; hiện không có UI handler để cập nhật bảng/empty/error.
- **Kết quả hiện tại:** animation cục bộ, không chứng minh dữ liệu đã được đồng bộ.

### EV-06 — Mở bộ lọc nâng cao (Click, disabled)

- Marker #26 hiện disabled; không có event handler, panel/modal hoặc query parameter tương ứng trong #87.
- Click không thực hiện hành động. Không tạo filter field hoặc endpoint bổ sung từ biểu tượng/copy trong mockup.

### EV-07 — Tạo bài kiểm tra (Click/handoff AD-16)

- Marker #21 hiện disabled, không có handler. AC-35 mô tả Create qua API #88 và builder thuộc AD-16.
- Khi route/permission/API #88 và handoff được duyệt, điều hướng candidate tới AD-16. AD-15 không gửi POST #88.
- Request body, success destination, validation và cache invalidation thuộc DD/API #88/AD-16; không được suy ra ở đây. Hiện click không đổi route.

### EV-08 — Phân trang (Click, local source có page nhưng UI chưa wire)

- **Input:** marker #40 previous, #41 next; prototype hiển thị `Trang 0 / 0` và hai nút disabled.
- **Contract/local:** catalog có `page?:int32`; source dùng page 1-based, mặc định 1, size cố định 20, `total_pages=0` khi total rỗng. Không có `size` query.
- **Validation:** không gửi page <1 hoặc vượt int32. Quy tắc cho late page là response 200 với `items=[]`, không tự lùi trang.
- **Kết quả:** hiện không có hành động. UI page indicator format và reset page sau filter chưa được quyết định.

### EV-09 — Mở quiz để cập nhật (Row action/handoff AD-16)

- AC-35 tham chiếu Update #89 → AD-16. Ảnh hiện là empty state, không có row/action button quan sát được.
- Chỉ khi có row data và action contract được duyệt mới truyền ID quiz lấy từ response đã xác nhận. Không suy ra numeric/string route ID trước khi response contract được thống nhất.
- AD-15 không gọi PUT #89; thiếu route/GET detail, request body và mapping là trách nhiệm DD AD-16/API #89.

### EV-10 — Mở xác nhận xóa (Row action/handoff AD-18)

- AC-35 tham chiếu Delete #90 → AD-18. Không có row action hoặc dialog trong ảnh empty state.
- Khi được duyệt, truyền ID từ row contract sang AD-18; việc xác nhận, dependency/attempt impact và DELETE #90 thuộc AD-18.
- Không gọi DELETE tại danh sách và không dự đoán optimistic removal, conflict behavior hoặc restore.

### EV-11 — Mở thống kê (Row action/handoff AD-17)

- AC-35 tham chiếu Statistics #91 → AD-17; không có action hiện tại trong empty state.
- Candidate handoff dùng ID quiz từ row contract. AD-15 không tính analytics từ `questions=[]` hay Quiz metadata.
- API #91 catalog/source response chưa đủ để khẳng định các KPI trong inventory; không tạo thống kê tại danh sách.

### EV-12 — Điều hướng Admin shell/breadcrumb/footer

- **Trigger:** marker #2–#6, #8, #10–#15 và #48–#50. Trong HTML, anchor destinations dùng `#`; notification control không có listener. #7/#9/#13/#16 và #45–#47 là nội dung tĩnh.
- **Processing:** không có route, profile, health, RBAC, privacy, support hay security API được nối vào các phần tử này.
- **Kết quả:** click không chuyển màn hình/không tải dữ liệu theo source hiện tại. Route đích và session-expiry/back policy cần tuân theo app shell contract khi Study Web được wire; chưa được suy diễn ở AD-15.
