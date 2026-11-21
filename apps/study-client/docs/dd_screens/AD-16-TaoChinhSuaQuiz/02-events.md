# AD-16 — Events (đặc tả xử lý)

## Current Angular implementation snapshot (2026-11-16)

- `/admin/quizzes/new` và `/admin/quizzes/:quizId/edit` được đăng ký trong `admin.routes.ts` và cùng render `AD16Page`; `/admin` lazy-load admin routes. `AdminLayout` điều khiển hiển thị shell theo phiên đăng nhập. Runtime navigation chưa được xác minh.
- Ở create mode, page giữ `title`, `duration` và `passing score` trong component memory qua input handlers. Course select vẫn disabled. Ở edit mode, các input cấu hình bị khóa vì không có nguồn GET detail.
- Create mode tải Course page từ #73, Question Builder/Add Question và Save gọi được nhánh #88 theo current source. Edit vẫn khóa; page chưa gọi #89, không autosave và không có kiểm tra `quiz management permission` riêng. Embedded schema và catalog gaps vẫn mở.
- Prototype trong Stitch vẫn là ảnh/HTML tĩnh; mô tả prototype bên dưới chỉ áp dụng cho artifact đó, trừ khi ghi rõ Angular source.

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-16-EV-001` | `Source heading` / EV-01 — Khởi tạo mode tạo (Load) | See source event detail below |
| `AD-16-EV-002` | `Source heading` / EV-02 — Khởi tạo mode chỉnh sửa (Load) | See source event detail below |
| `AD-16-EV-003` | `Source heading` / EV-03 — Thay đổi cấu hình chung (Input/Change) | See source event detail below |
| `AD-16-EV-004` | `Source heading` / EV-04 — Thêm câu hỏi (Click) | See source event detail below |
| `AD-16-EV-005` | `Source heading` / EV-05 — Lưu Quiz mới (#88) | See source event detail below |
| `AD-16-EV-006` | `Source heading` / EV-06 — Cập nhật Quiz hiện hữu (#89) | See source event detail below |
| `AD-16-EV-007` | `Source heading` / EV-07 — Hủy/quay về AD-15 (Click) | See source event detail below |
| `AD-16-EV-008` | `Source heading` / EV-08 — Safe Mode, autosave, schema và builder gate copy | See source event detail below |
| `AD-16-EV-009` | `Source heading` / EV-09 — Admin shell, breadcrumb và footer links (Click) | See source event detail below |
| `AD-16-EV-010` | `Source heading` / EV-10 — Validation, auth và API failure states | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện và xử lý dữ liệu

### EV-01 — Khởi tạo mode tạo (Load)

- **Element/kích hoạt:** Route `/admin/quizzes/new` có trong Angular source; runtime chưa xác minh.
- **Đầu vào:** URL, session/auth state và permission cần có theo AC-35; form values ban đầu không nhận từ màn trước ngoài mode create.
- **Quy trình:** (1) Angular router đăng ký create/edit route và resolve cùng `AD16Page`; runtime chưa xác minh. (2) `AdminLayout` xử lý phiên; fine-grained `quiz management permission` chưa có source. (3) Create gọi #73 theo page và chỉ nhận response nếu `pagination.page` khớp trang đã yêu cầu; backend source echo trang đã validate. Trang ngoài `total_pages` vẫn hợp lệ khi backend trả `items=[]`, để page recovery hiện có xử lý. Edit không gọi #73 và vẫn khóa do thiếu GET detail. (4) Tạo giữ config/questions trong bộ nhớ tới khi submit; danh sách/câu hỏi có thể sửa trước khi lưu.
- **API/output:** Create gọi GET #73 với `page` rồi POST #88 khi submit hợp lệ; không tự gọi POST lúc vào trang. Save success hiển thị thông báo và link AD-15; đích/navigation sau save vẫn chưa được định nghĩa.
- **Ngoại lệ/trạng thái:** Có loading/error/empty cho Course options và saving/success/error cho #88. Runtime chưa xác minh; embedded shape vẫn `DERIVED`.

### EV-02 — Khởi tạo mode chỉnh sửa (Load)

- **Element/kích hoạt:** Candidate `/admin/quizzes/:quizId/edit`, truy cập từ action của một Quiz trong AD-15.
- **Đầu vào:** `quizId` route param. Catalog #89 khai báo `int64!`; format/positive check phía UI chưa được contract hóa.
- **Quy trình:** (1) Parse route ID theo contract đã chốt; (2) kiểm tra auth/permission; (3) cần GET admin Quiz detail để lấy config, Questions, Choices; (4) endpoint này không tồn tại. #87 list không phải detail và source local trả `questions=[]`; (5) không render dữ liệu giả, không gửi PUT, giữ edit state `blocked` và yêu cầu contract detail + question schema.
- **API/output:** Không có GET detail. #89 là mutation, không thể dùng làm read. Không tự dùng #87 để prefill.
- **Ngoại lệ/trạng thái:** Quiz missing/deleted và permission response chỉ có thể xác định sau khi có endpoint/load flow; catalog #89 404 chỉ áp dụng lúc mutation. Current screenshot không có ID/value.

### EV-03 — Thay đổi cấu hình chung (Input/Change)

- **Element:** #17–#20. Stitch prototype không có listener. Angular create page có input handlers cho title/duration/score và giữ giá trị trong component memory; edit fields bị khóa. Validation/error rendering và submit path chưa có.
- **Đầu vào:** `title` text; Course được chọn từ #73; duration optional; passing score là chuỗi thập phân. Phía server local #88 fallback nhận `course_id` int64, `title` string tối đa 200 ký tự, `duration_minutes` optional int32/null, `passing_score` decimal string biểu diễn được bằng NUMERIC(5,2). Nested shape vẫn `DERIVED`.
- **Quy trình:** (1) Nhận giá trị đã nhập. (2) Kiểm tra chính xác các giới hạn hiện có trong #88 validator; không thêm required/minimum hay quy tắc đáp án. (3) Giữ leading/sign semantics số nguyên bằng cách chuẩn hóa embedded integer mà không qua JS Number với course ID. (4) Không tự lưu khi field thay đổi; chỉ POST khi submit.
- **Kết quả/ngoại lệ:** Draft config ở bộ nhớ; lỗi validation cục bộ hiển thị trong form. Course ID vượt safe-integer không được đưa vào select để tránh gửi sai giá trị. API DD còn Draft và chưa có owner sign-off cho embedded schema.

### EV-04 — Thêm câu hỏi (Click)

- **Element:** Nút Add Question và Add Choice trong create mode.
- **Tiền điều kiện:** UI dùng current #88 fallback `questions[]`, question `text/type/choices[]`, choice `text/is_correct`; các field/type vẫn `DERIVED`, không phải catalog-approved schema.
- **Quy trình hiện tại:** (1) Thêm/xóa Question và Choice trong local signal state. (2) Question type giới hạn theo current source enum `SINGLE_CHOICE`, `MULTIPLE_CHOICE`, `TRUE_FALSE`. (3) Không áp đặt số lựa chọn hoặc số đáp án đúng tối thiểu; current validator không có các giới hạn này. (4) Không gọi API cho đến khi nhấn Save.
- **Kết quả:** UI tạo được payload shape hiện tại; API DD, owner approval và live schema vẫn chưa xác minh.

### EV-05 — Lưu Quiz mới (#88)

- **Element/kích hoạt:** Nút Save submit form trong create mode; edit vẫn disabled.
- **Tiền điều kiện current:** Create mode, Admin access token, Course option từ #73, trường cấu hình hợp lệ theo current #88 validator. AC-35 fine-grained permission chưa được source hỗ trợ.
- **Đầu vào/candidate request:** Direct catalog quy định body top-level `{config:string!, questions:string!}`. Catalog không định nghĩa JSON fields bên trong. Local #88 fallback yêu cầu hai chuỗi JSON và nested shape trong §A.2; shape này `DERIVED`.
- **Quy trình hiện tại:** (1) Validate course ID int64, title length, duration int32 và passing-score decimal theo current #88 validator. (2) Serialize nested `config/questions` thành đúng hai string outer body như direct catalog. (3) Gửi POST #88 bằng Admin Bearer token; không thêm field/header/idempotency key. (4) Chỉ coi success khi envelope có `success=true`, `DESIGN_RESOURCE_CREATED` và Quiz response shape. (5) Trong khi gửi khóa control; sau success khóa form và hướng dẫn mở AD-15, không tự navigate. (6) Kết quả mạng không rõ hoặc success envelope sai shape yêu cầu kiểm tra AD-15 trước khi submit lại.
- **Lỗi:** 401/403/422 hiển thị lỗi tương ứng; 500/network error hiển thị generic state. Admin API transport xóa local session khi nhận 401.
- **Đầu ra hiện tại:** Create mode gọi API #88. Embedded schema vẫn `DERIVED`; mapping UI sau save không có quy tắc owner-approved.

### EV-06 — Cập nhật Quiz hiện hữu (#89)

- **Element/kích hoạt:** #31 Save trong edit mode; disabled và edit mode không hydrate được.
- **Tiền điều kiện expected:** Edit route có ID đã xác minh, Quiz data/question set đã load, permission hợp lệ, dirty state có thay đổi và #89 body contract được phê duyệt. Hiện thiếu GET detail/body contract.
- **Đầu vào:** Direct catalog chỉ khai báo `quiz_id:int64!` trong path; không khai báo request body. Không thể xác định cập nhật config/question bằng API trực tiếp này.
- **Quy trình khi có thể triển khai:** (1) Validate ID/data theo contract đã duyệt. (2) Không gửi PUT cho tới khi body được thêm/chốt trong catalog/DD. (3) Local source fallback hiện parse positive int64 và reuse body #88; đây là `DERIVED`, không phải cách gọi được phê duyệt. (4) Local source lock quiz/child rows, kiểm tra attempt/answer history trước write, xác nhận target course, update Quiz, thay toàn bộ Choices/Questions theo request order, map response rồi commit. (5) Response local 200 mapping trả Quiz admin; giữ `status` và `created_at`. (6) UI/cache/route sau success cần owner quyết định; không tự invalidation/refetch.
- **Lỗi direct catalog:** 401/403/404/422/500 với business code tương ứng trong API catalog. Local fallback: 404 nếu Quiz không tồn tại/đã `DELETED`; 422 nếu path/body/Course invalid hoặc có attempt/answer history; 500 cho query/mapping/commit lỗi và rollback. History conflict hiện dùng HTTP 422, không phải 409.
- **Đầu ra hiện tại:** Không có edit data, body hoặc request; không có UI conflict/error state.

### EV-07 — Hủy/quay về AD-15 (Click)

- **Element:** #13 và #30; anchors trỏ `#/admin/quizzes`. #13 ở header, #30 ở footer action.
- **Đầu vào/quy trình:** (1) Stitch HTML độc lập dùng anchor hash; Angular template dùng `RouterLink` về `/admin/quizzes`. (2) Không gọi API. (3) Không có dirty-state check, draft restore hoặc query/page/filter preservation. (4) Route đích có trong source; runtime navigation chưa xác minh.
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

- **Nguồn:** API catalog #88/#89 và current local handlers. Angular page gọi #88 khi tạo mới, nhưng chưa có caller #89.
- **Quy trình response candidate:** (1) Nhận HTTP status + envelope/businessCode. (2) 401 yêu cầu xử lý phiên; refresh/login/redirect policy chưa được quy định. (3) 403 hiển thị access denied; detail/masking policy chưa có. (4) 422 hiển thị field/business validation theo error payload đã thống nhất; #89 local history refusal cũng là 422. (5) 404 ở #89 biểu thị Quiz không tồn tại theo catalog/local source, local source cũng trả 404 cho tombstone. (6) 500 hiển thị lỗi tổng quát/trace ID nếu contract xác nhận; không lộ SQL/body. (7) Không retry, replay hoặc giữ form/cache nếu policy chưa có.
- **Current result:** #73 và #88 có loading/error/success feedback trong create mode. Edit conflict/404, #89 errors và fine-grained permission chưa có UI vì edit mutation vẫn gated.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
