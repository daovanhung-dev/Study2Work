# AD-16 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

```mermaid
flowchart TD
  A[AD-15: chọn tạo hoặc sửa Quiz] --> B[AD-16 candidate route]
  B --> C{Create hay Edit?}
  C -->|Create #88| D[Form prototype rỗng]
  C -->|Edit #89| E[BLOCK: không có GET detail; #87 không có questions]
  D --> F[Questions Builder hiện disabled]
  F --> G[Save hiện disabled]
  G --> H{Contract và UI đã được duyệt/wire?}
  H -->|Create| I[POST #88 theo direct catalog]
  H -->|Update| J[PUT #89: catalog chưa khai báo body]
  I --> K[Quiz created; đích sau save chưa chốt]
  J --> L[Quiz updated; đích sau save chưa chốt]
  D --> M[Hủy → hash #/admin/quizzes; route chưa xác minh]
```

1. **Entry:** AD-15 là luồng trước theo AC-35. Inventory đề xuất create/edit route; hiện không có Study Web route để resolve hoặc kiểm tra session.
2. **Authentication/authorization:** API catalog yêu cầu Bearer JWT/Admin. AC-35 dùng `quiz management permission`; source local chỉ kiểm tra shared `ADMIN`. UI chưa có guard. Khi thiếu auth, catalog liệt kê 401; thiếu quyền, 403. Client response/navigation chưa được thiết kế.
3. **Khởi tạo:** Screenshot hiện render config rỗng và Questions rỗng. Không có API options/load. Course select chỉ có placeholder. Create default ngoài dữ liệu rỗng chưa được xác định. Edit cần Quiz detail nhưng endpoint không tồn tại; không được dựng data từ URL hoặc #87.
4. **Nhập liệu:** Các input không có event listener/validation. Question/Choice controls không tồn tại; Add Question và Save disabled. Giao diện không thể tạo request chứa Question set.
5. **Mutation:** Khi contract và UI được duyệt, create dùng #88; update cần chốt request body trước khi dùng #89. Direct catalog và current local handler có khác biệt; xem EV-05/EV-06. Hiện không có request được gửi.
6. **Response:** Catalog thành công trả `ApiEnvelope<Quiz>`. Local code sinh ID Quiz/Question/Choice và response Admin có `is_correct`; mapping frontend, cache, retry, idempotency, toast và route sau save chưa có. Không được gửi answer key qua Student API.
7. **Lỗi và trạng thái:** Catalog #88/#89 nêu 401/403/422/500; #89 thêm 404. Local #89 dùng 422 cho history conflict. Prototype không thể biểu diễn loading, field errors, permission errors, save success hoặc conflict hiện hành.
8. **Rời màn hình:** Hủy có hash `#/admin/quizzes`; hash đích không chứng minh route có runtime. AD-17 được mở từ nhánh statistics của AD-15, không có nút/điều hướng trực tiếp từ prototype AD-16. Bảo toàn draft/filter/page hoặc cảnh báo thay đổi chưa lưu không được xác nhận.

### Trích từ DD nguồn: D. Đặc tả sự kiện và xử lý dữ liệu

### EV-01 — Khởi tạo mode tạo (Load)

- **Element/kích hoạt:** Route candidate `/admin/quizzes/new`; hiện chưa có client route.
- **Đầu vào:** URL, session/auth state và permission cần có theo AC-35; form values ban đầu không nhận từ màn trước ngoài mode create.
- **Quy trình:** (1) Resolve route và mode; hiện không có router. (2) Kiểm tra Bearer/session và quiz-management permission; chưa có UI guard. (3) Nếu quyền hợp lệ, cần tải course options và defaults, nhưng không có API/source được chỉ định cho options/defaults. (4) Không gọi #87 để lấy course options trừ khi contract và mapping được duyệt. (5) Render blank config/questions như prototype chỉ làm trạng thái mẫu. (6) Chỉ enable builder/save sau khi schema/validation/permission/UI được duyệt.
- **API/output:** Không có request hiện tại. #88 chỉ chạy khi submit hợp lệ; create entry không tự POST. Destination sau create chưa xác định.
- **Ngoại lệ/trạng thái:** Loading, unauthorized, forbidden, error và empty course option chưa có UI implementation. Không thể đánh dấu create `ready` từ screenshot.

### EV-02 — Khởi tạo mode chỉnh sửa (Load)

- **Element/kích hoạt:** Candidate `/admin/quizzes/:quizId/edit`, truy cập từ action của một Quiz trong AD-15.
- **Đầu vào:** `quizId` route param. Catalog #89 khai báo `int64!`; format/positive check phía UI chưa được contract hóa.
- **Quy trình:** (1) Parse route ID theo contract đã chốt; (2) kiểm tra auth/permission; (3) cần GET admin Quiz detail để lấy config, Questions, Choices; (4) endpoint này không tồn tại. #87 list không phải detail và source local trả `questions=[]`; (5) không render dữ liệu giả, không gửi PUT, giữ edit state `blocked` và yêu cầu contract detail + question schema.
- **API/output:** Không có GET detail. #89 là mutation, không thể dùng làm read. Không tự dùng #87 để prefill.
- **Ngoại lệ/trạng thái:** Quiz missing/deleted và permission response chỉ có thể xác định sau khi có endpoint/load flow; catalog #89 404 chỉ áp dụng lúc mutation. Current screenshot không có ID/value.

### EV-03 — Thay đổi cấu hình chung (Input/Change)

- **Element:** #17–#20. Hiện không có listener, local UI state, error rendering hoặc submit path.
- **Đầu vào:** `title` text; course selector hiện chỉ có placeholder; duration optional number; passing score number. Phía server local #88/#89 fallback nhận `course_id` strict int64, `title` strict string, `duration_minutes` optional strict int/null, `passing_score` strict string. Đây là local derived request shape.
- **Quy trình:** (1) Nhận giá trị đã nhập. (2) Các native HTML `min/max` hiện hữu là hint prototype; không suy ra business validation. (3) Chưa có quy tắc normalize whitespace, required title, chọn course, decimal separator, rounding, bỏ trống duration hoặc đổi `%` thành request string. (4) Không gọi API khi field thay đổi. (5) Dirty/invalid state chưa implement; không claim autosave.
- **Kết quả/ngoại lệ:** Không có state change observable ngoài HTML control. Cần owner chốt required/range/precision, course ID source và mapping trước khi lập trình validator. Local fallback hiện kiểm tra title max 200, duration int32, score numeric fit; các checks này không xác nhận UI business policy.

### EV-04 — Thêm câu hỏi (Click)

- **Element:** #27 disabled Add Question. No event handler; không có question/choice inputs.
- **Tiền điều kiện:** Questions schema/type, editor behavior, answer-choice constraints, ordering, validation, source options và persistence semantics cần được xác nhận. Local #88 fallback shape có `questions[]`, từng item có `text`, `type`, `choices[]`, và Choice có `text`, `is_correct`.
- **Quy trình hiện tại:** (1) Browser không phát click cho disabled button. (2) Không tạo Question/Choice object. (3) Không cập nhật `questions` state/cache. (4) Không gọi API. (5) Gate/temporary-lock copy giữ nguyên.
- **Kết quả:** Empty state tiếp tục hiện. Không thể hoàn tất payload tạo/sửa; đây là blocker chính cho Save.

### EV-05 — Lưu Quiz mới (#88)

- **Element/kích hoạt:** #31 Save; disabled trong prototype, vì vậy hiện không có Submit event.
- **Tiền điều kiện expected:** Create mode; Admin session/quiz-management permission; form config và question schema hợp lệ; course option map sang ID; Save được enable theo rule đã duyệt. Các điều kiện này chưa đạt.
- **Đầu vào/candidate request:** Direct catalog quy định body top-level `{config:string!, questions:string!}`. Catalog không định nghĩa JSON fields bên trong. Local #88 fallback yêu cầu hai chuỗi JSON và nested shape trong §A.2; shape này `DERIVED`.
- **Quy trình khi có thể triển khai:** (1) Chuẩn hóa config/question input theo contract owner duyệt. (2) Validate client-side theo cùng contract; không dùng min/max prototype như business rule nếu chưa duyệt. (3) Encode `config` và `questions` thành hai string theo catalog. (4) Gửi `POST /api/v1/admin/quizzes` với Bearer JWT; không có header/idempotency key bổ sung được quy định. (5) Đọc HTTP/business code và envelope. (6) 201 `DESIGN_RESOURCE_CREATED`: nhận `Quiz` response; direct catalog schema không nêu chi tiết nested properties. Local source response dự kiến có IDs và answer keys nhưng là derived. (7) Cập nhật UI/cache hoặc điều hướng chỉ sau khi success mapping và destination được chốt; hiện chưa có chính sách. (8) Không retry tự động hoặc dedupe khi chưa có policy.
- **Lỗi:** 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR` theo catalog. Local fallback 422 khi body/nested JSON/shape/course invalid; 500/query/mapping/commit lỗi rollback sau khi đã vào transaction. Không có runtime client error view.
- **Đầu ra hiện tại:** Không gửi request; button disabled và Questions rỗng.

### EV-06 — Cập nhật Quiz hiện hữu (#89)

- **Element/kích hoạt:** #31 Save trong edit mode; disabled và edit mode không hydrate được.
- **Tiền điều kiện expected:** Edit route có ID đã xác minh, Quiz data/question set đã load, permission hợp lệ, dirty state có thay đổi và #89 body contract được phê duyệt. Hiện thiếu GET detail/body contract.
- **Đầu vào:** Direct catalog chỉ khai báo `quiz_id:int64!` trong path; không khai báo request body. Không thể xác định cập nhật config/question bằng API trực tiếp này.
- **Quy trình khi có thể triển khai:** (1) Validate ID/data theo contract đã duyệt. (2) Không gửi PUT cho tới khi body được thêm/chốt trong catalog/DD. (3) Local source fallback hiện parse positive int64 và reuse body #88; đây là `DERIVED`, không phải cách gọi được phê duyệt. (4) Local source lock quiz/child rows, kiểm tra attempt/answer history trước write, xác nhận target course, update Quiz, thay toàn bộ Choices/Questions theo request order, map response rồi commit. (5) Response local 200 mapping trả Quiz admin; giữ `status` và `created_at`. (6) UI/cache/route sau success cần owner quyết định; không tự invalidation/refetch.
- **Lỗi direct catalog:** 401/403/404/422/500 với business code tương ứng trong API catalog. Local fallback: 404 nếu Quiz không tồn tại/đã `DELETED`; 422 nếu path/body/Course invalid hoặc có attempt/answer history; 500 cho query/mapping/commit lỗi và rollback. History conflict hiện dùng HTTP 422, không phải 409.
- **Đầu ra hiện tại:** Không có edit data, body hoặc request; không có UI conflict/error state.

### EV-07 — Hủy/quay về AD-15 (Click)

- **Element:** #13 và #30; anchors trỏ `#/admin/quizzes`. #13 ở header, #30 ở footer action.
- **Đầu vào/quy trình:** (1) Browser xử lý anchor hash; HTML không khai báo router/listener. (2) Không gọi API. (3) Không có dirty-state check, draft restore hoặc query/page/filter preservation. (4) Destination AD-15 là expected handoff theo inventory, nhưng runtime chưa xác minh.
- **Kết quả/ngoại lệ:** Prototype hash đổi theo browser behavior; không khẳng định Study app render AD-15. Unsaved-change prompt và clear/preserve draft là open decision.

### EV-08 — Safe Mode, autosave, schema và builder gate copy

- **Element:** #15, #21, #23, #28. Đây là message regions, không phải action control.
- **Đầu vào/quy trình:** Không có event, API, timer, browser storage hoặc feature flag. Copy được render tĩnh từ HTML. “Autosave locally”, “schema đang chờ”, “SYSTEM NORMAL” và “Gate active” không phải server state.
- **Kết quả:** Không có dữ liệu được lưu/tải và không đổi trạng thái khi message hiển thị. Nếu cần autosave/gate, cần định nghĩa storage scope, lifecycle, recovery, schema version và security behavior trong contract riêng.

### EV-09 — Admin shell, breadcrumb và footer links (Click)

- **Element:** #2–#6, #8, #10–#12, #33–#35.
- **Đầu vào/quy trình:** Anchor/nav click. Top nav/footer dùng `href="#"`; breadcrumb phần lớn là spans; notification button không có handler. Không có route resolver, API call hoặc auth/session transition trong HTML.
- **Kết quả:** Chỉ browser fragment/default control behavior; destination thực tế không xác minh. Không suy ra route, logout, notification panel, role change hoặc help center.

### EV-10 — Validation, auth và API failure states

- **Nguồn:** API catalog #88/#89 và current local handlers; không có client runtime để map.
- **Quy trình response candidate:** (1) Nhận HTTP status + envelope/businessCode. (2) 401 yêu cầu xử lý phiên; refresh/login/redirect policy chưa được quy định. (3) 403 hiển thị access denied; detail/masking policy chưa có. (4) 422 hiển thị field/business validation theo error payload đã thống nhất; #89 local history refusal cũng là 422. (5) 404 ở #89 biểu thị Quiz không tồn tại theo catalog/local source, local source cũng trả 404 cho tombstone. (6) 500 hiển thị lỗi tổng quát/trace ID nếu contract xác nhận; không lộ SQL/body. (7) Không retry, replay hoặc giữ form/cache nếu policy chưa có.
- **Current result:** Không có loading, inline field error, auth error, API error, success toast hoặc conflict view. Trạng thái này là thiết kế candidate, chưa implement.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

### E.1. Trạng thái

| Trạng thái | Điều kiện chuyển vào | Hiển thị/đầu ra | Tình trạng chứng cứ |
|---|---|---|---|
| Prototype blank/draft | Mở ảnh hiện tại | Config trống, Questions rỗng, Save/Add disabled | `CURRENT` static screenshot; không phải persisted draft. |
| Loading | Route/API đang tải | Chưa có loading component | `EXPECTED_CANDIDATE`; chưa implement. |
| Ready/clean | Data/options tải thành công hoặc create defaults sẵn sàng | Chưa có xác định fields/options | `BLOCKER`; đặc biệt edit thiếu GET detail. |
| Dirty | User thay đổi config/question | Không có dirty tracker | `EXPECTED_CANDIDATE`; autosave claim không có source. |
| Invalid | Validation thất bại | Chưa có field-level errors | Ranges/required/precision unresolved; API local 422 is source fallback only. |
| Saving | Mutation đang gửi | Button vẫn disabled tĩnh, không loading state | `EXPECTED_CANDIDATE`; duplicate-submit policy open. |
| Created | #88 returns 201 success | Response/copy/navigation/cache undefined | `EXPECTED`; direct contract status only. |
| Updated | #89 returns 200 success | Response/copy/navigation/cache undefined | `EXPECTED`; direct body missing. |
| Not found | #89 returns 404 | No error panel | `EXPECTED` API response; local tombstone mapping derived. |
| Conflict/history blocked | Local #89 detects attempt/answer history | No conflict UI; source returns 422 | `DERIVED`; catalog does not define attempt policy. |
| Unauthorized/forbidden | 401/403 | No session/access UI | Catalog errors; client handling open. |
| Service error | 500 or network failure | No error/retry UI | API 500 catalog; network/timeout policy absent. |

Không đồng nhất `conflict` trong inventory với HTTP 409: catalog #89 không liệt kê 409 và local history rejection là 422. Cần owner/API contract chốt status và policy trước implementation.

### E.2. Điều hướng và dữ liệu trao đổi

| Từ | Điều kiện/event | Đích | Dữ liệu cần truyền | Trạng thái |
|---|---|---|---|---|
| AD-15 | Create action / #88 | AD-16 create candidate | Không có Quiz ID; course/filter state carry-over chưa quy định. | AC-35 expected; AD-15 CTA hiện disabled và Study route chưa wire. |
| AD-15 row | Update action / #89 | AD-16 edit candidate | Quiz ID theo response đã duyệt; local/catalog candidate int64. | Detail GET/question set missing; không thể populate. |
| AD-16 | Cancel/back #13/#30 | AD-15 candidate `#/admin/quizzes` | Không có form payload; dirty draft/filter/page retention chưa rõ. | Hash hiện có trong HTML, router chưa xác minh. |
| AD-16 create/update success | #88/#89 | Chưa xác định; có thể AD-15 theo quy trình list nhưng không được suy ra | `Quiz.id`/response nếu contract chuẩn hóa; update ID từ route. | Owner cần chốt success destination, refetch/cache và duplicate-submit policy. |
| AD-15 | Statistics action | AD-17 | Quiz ID theo API/list response đã duyệt. | Không có nút đi AD-17 trực tiếp từ AD-16; API #91 thuộc AD-17. |

## 4. Luồng đọc (Read)
- Orchestration từ inventory: POST #88 khi tạo; PUT #89 khi sửa. Không giả định GET admin quiz detail; #87 metadata-only và `questions=[]` local. #89 catalog không khai báo body; local fallback yêu cầu replacement body. Autosave copy trong prototype chưa có persistence source.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [AD-16](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/AD-16.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
