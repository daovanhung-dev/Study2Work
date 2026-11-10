# ST-03 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-03-EV-001` | `Source heading` / Ma trận event | See source event detail below |
| `ST-03-EV-002` | `ST03-EV-01` / ST03-EV-01 — Mở trang và tải profile | See source event detail below |
| `ST-03-EV-003` | `ST03-EV-02` / ST03-EV-02 — Thay đổi họ tên | See source event detail below |
| `ST-03-EV-004` | `ST03-EV-03` / ST03-EV-03 — Email readonly | See source event detail below |
| `ST-03-EV-005` | `ST03-EV-04` / ST03-EV-04 — Phone/Bio bị khóa | See source event detail below |
| `ST-03-EV-006` | `ST03-EV-05` / ST03-EV-05 — Tải avatar | See source event detail below |
| `ST-03-EV-007` | `ST03-EV-06` / ST03-EV-06 — Lưu hồ sơ | See source event detail below |
| `ST-03-EV-008` | `ST03-EV-07` / ST03-EV-07 — Quay về ST-02 | See source event detail below |
| `ST-03-EV-009` | `ST03-EV-08` / ST03-EV-08 — Header brand/navigation | See source event detail below |
| `ST-03-EV-010` | `ST03-EV-09` / ST03-EV-09 — Footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### Ma trận event

| Event ID | Tên / loại | Element | Current behavior |
|---|---|---|---|
| ST03-EV-01 | Mở trang và tải profile — Load | Route ST-03 | Route/API call chưa có trong Study Web; expected gọi #04. |
| ST03-EV-02 | Thay đổi họ tên — Input/Change | #14 | Native input nhận text; không có dirty/validation handler. |
| ST03-EV-03 | Tương tác email — Input/Focus | #15 | Read-only; không đổi dữ liệu. |
| ST03-EV-04 | Phone/Bio bị khóa — Input/Change | #16, #17 | Disabled; browser không phát thao tác nhập. |
| ST03-EV-05 | Tải avatar — Click/Upload | #11 | Button disabled; không mở file picker hoặc gọi #13. |
| ST03-EV-06 | Lưu hồ sơ — Submit/Click | #19 | Button disabled, type button; không submit hoặc gọi #14. |
| ST03-EV-07 | Quay về hồ sơ — Click/Anchor | #7, #18 | Fragment href="#"; expected ST-02, chưa có route binding. |
| ST03-EV-08 | Header brand/navigation — Click/Anchor | #1, #2 | Fragment anchors, đích chưa map. |
| ST03-EV-09 | Footer navigation — Click/Anchor | #26 | Fragment anchors, đích chưa map. |

### ST03-EV-01 — Mở trang và tải profile

- **Input:** Route đề xuất /student/profile/edit; không có path/query/body. Token dự kiến đọc từ auth/session theo SH-02; không có Study Web session source hiện tại.
- **Tiền điều kiện:** App/router tồn tại và user có Student session. API #04, #13, #14 đều kiểm tra JWT Bearer và role STUDENT ở server; client guard chưa được xác minh.
- **Quy trình dự kiến:**
  1. Resolve route và yêu cầu session theo auth contract đã duyệt.
  2. Gửi GET #04 tới /api/v1/users/me, một header Authorization: Bearer <access-token>, không path/query/body.
  3. Backend hiện parse JWT, lấy sub numeric và roles; yêu cầu STUDENT rồi SELECT profile theo users.id.
  4. Thành công: HTTP 200, businessCode=DESIGN_RESOURCE_RETRIEVED, data=UserProfile, meta={}, có traceId. Fields hiện có: id, full_name, email, role, avatar_url nullable, phone nullable, status, created_at, updated_at. Không có bio.
  5. Chỉ map các field theo UI contract đã duyệt. Candidate mapping là full_name → #14, email → #15, phone → #16, avatar_url → #8; phone/avatar bị khóa bởi design và bio không có nguồn. Do đó không tự prefill/enable các control khi chưa có loaded-state design.
  6. Không có cache policy, duplicate request policy hoặc refresh-after-save policy được xác minh.
- **Response/error:** 401 DESIGN_AUTHENTICATION_REQUIRED khi thiếu/sai Bearer hoặc user row không tồn tại; 403 DESIGN_ACCESS_DENIED nếu JWT thiếu role STUDENT; 500 DESIGN_INTERNAL_ERROR khi query/mapping/token configuration lỗi. API #04 không lọc DB status hoặc so DB role với JWT role.
- **Kết quả UI:** Current HTML không gọi request; màn hình luôn là mockup Gate G-03. Cách hiển thị 401/403/500 và điều hướng SH-05 chưa được triển khai.

### ST03-EV-02 — Thay đổi họ tên

- **Input:** Chuỗi do người dùng nhập vào fullname; HTML hiện không đặt minlength/maxlength/required hoặc giá trị ban đầu.
- **Current:** Browser cho phép nhập text, nhưng form onsubmit="return false" và không có listener. Không có dirty state, validation, debounce, API call hay persistence.
- **Khi contract được chốt:** Giá trị cần được chuẩn hóa nhất quán với API #14: server trim khoảng trắng, từ chối chuỗi rỗng, giới hạn 150 ký tự. UI có thể hiển thị field error từ response; quy tắc thời điểm validate (on blur/on submit) và dirty indicator chưa có nguồn, cần quyết định.
- **Output:** Hiện chỉ thay đổi giá trị DOM tạm thời. Không đổi cache/server và không có thông báo thành công/lỗi.

### ST03-EV-03 — Email readonly

- **Input:** Không có giá trị nhập được; readonly=true.
- **Quy trình:** Focus/copy (nếu browser cho phép) không sửa trường; không gọi API. data.email của #04 là nguồn server candidate, placeholder hiện tại là mẫu tĩnh.
- **Output:** Không thay đổi state. Chính sách copy-to-clipboard hoặc email update ngoài màn này không được định nghĩa.

### ST03-EV-04 — Phone/Bio bị khóa

- **Input:** Không có input hiện tại; cả hai controls disabled.
- **Quy trình:** Browser chặn sửa và không đưa control disabled vào form submission. Không gọi #14 từ thao tác này.
- **Current API evidence:** #14 đòi field phone có mặt nhưng cho phép null; chuỗi trim, blank → null, max 20. Bio là field extra bị bỏ qua, không được lưu. #04/DDL không có bio.
- **Output:** Không thay đổi state/server. Không tự mở khóa phone chỉ vì server hiện nhận nullable value; không gửi bio như thể được persist.

### ST03-EV-05 — Tải avatar

- **Input:** Không có file input hoặc file selection event hiện tại; #11 disabled. API #13 nhận JSON {image: Data URL} trong đó image là Data URL PNG/JPEG/WebP base64.
- **Nếu gate được mở sau khi contract được duyệt:**
  1. Lấy file theo chính sách file picker/preview/encode được chốt; hiện chưa có client policy, resize policy hoặc client-side size check.
  2. Tạo request JSON đúng body {image: <Data URL>}; không dùng multipart vì current route không nhận multipart.
  3. Gửi POST /api/v1/users/me/avatar với Authorization Bearer Student; không path/query.
  4. Backend xác thực Student, parse Data URL, giới hạn 5 MiB sau decode và đối chiếu chữ ký tối thiểu với MIME. Sau đó provider ghi bytes vào object key avatars/{user_id}.
  5. Thành công HTTP 201 DESIGN_RESOURCE_CREATED, data.avatar_url chứa public URL. #13 không cập nhật users.avatar_url/DB.
  6. Client chỉ giữ URL chờ bước profile update theo policy đã chốt; UI success/preview state hiện chưa có.
- **Lỗi:** 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; invalid Data URL/empty/base64/oversize/signature mismatch → 422 DESIGN_VALIDATION_ERROR với fieldErrors; body schema/type errors → request validation 422; provider/config failure → 500 DESIGN_INTERNAL_ERROR. Provider cấu hình từ biến môi trường; thời gian kết nối 5s, đọc 30s, một attempt.
- **Ngoại lệ:** Upload là external side effect, không có DB transaction/compensation. Cùng user key bị ghi đè. Không tự retry do không có idempotency contract. Storage live chưa được xác minh.

### ST03-EV-06 — Lưu hồ sơ

- **Input dự kiến:** full_name từ #14; phone/avatar_url từ state theo contract còn mở; bio hiện không có trường hỗ trợ server. Current save button disabled nên không có input event.
- **Sequence trong inventory:** GET #04 lúc load → nếu avatar thay đổi POST #13 → PUT #14 → GET #04 để đồng bộ.
- **Current source-backed server behavior:**
  1. API #14 là PUT /api/v1/users/me/profile, JSON body bắt buộc có full_name (string), phone (string|null), avatar_url (string|null); không có path/query; Authorization Bearer Student.
  2. Request model cho phép field extra nên body có bio không bị từ chối, nhưng bio bị bỏ qua. Không gửi bio như thể được cập nhật.
  3. Validator trim full_name, từ chối blank, tối đa 150; trim nullable phone/avatar_url và đổi chuỗi trống thành null; phone tối đa 20. avatar_url không được kiểm tra URI hay ràng buộc với object vừa upload.
  4. Query UPDATE users SET full_name, phone, avatar_url, updated_at=CURRENT_TIMESTAMP WHERE id=:user_id RETURNING các safe profile fields. Backend map UserProfile, commit và trả envelope.
  5. Thành công HTTP 200 DESIGN_RESOURCE_UPDATED; data là UserProfile trực tiếp trong response envelope. Không gọi #04 tiếp theo.
  6. Client outcome chưa có source. AC-11/inventory đòi GET #04 sau PUT; quyết định dùng PUT response hay refetch phải được chốt trước implementation.
- **Lỗi:** Thiếu/sai auth 401 DESIGN_AUTHENTICATION_REQUIRED; không đúng Student 403 DESIGN_ACCESS_DENIED; thiếu required body/type validation 422 VALIDATION_ERROR; semantic full_name/phone validation 422 DESIGN_VALIDATION_ERROR; user row không tồn tại trả 401; DB/mapping/commit lỗi 500 DESIGN_INTERNAL_ERROR và rollback DB transaction.
- **Trùng lặp/partial failure:** Không có idempotency key, FE debounce, retry policy hoặc conflict resolution được xác minh. Nếu POST #13 đã ghi object nhưng PUT #14 thất bại, object vẫn tồn tại hoặc đã ghi đè avatar cũ. Không có compensation/cleanup source. Không tự gửi request lần nữa.
- **Kết quả hiện tại:** Save không thể kích hoạt trong HTML. Không có persisted state hoặc success/error message.

### ST03-EV-07 — Quay về ST-02

- **Input:** Click #7 hoặc #18. Anchor hiện là href="#" với data-path="ho-so-ca-nhan".
- **Current:** Fragment navigation trong tài liệu tĩnh; không chuyển tới /student/profile.
- **Expected:** Inventory chỉ định quay về ST-02 (/student/profile); không có path/body/query contract. Không truyền profile PII qua URL. Việc giữ dirty data/cache hoặc reload ST-02 sau khi save thành công chưa được chốt.
- **Output:** Không có route event hoặc API call hiện tại.

### ST03-EV-08 — Header brand/navigation

- **Input:** Click #1 hoặc một mục #2.
- **Current:** Các anchor có href="#" và data-path như trang-chu, khoa-hoc-cua-toi, tien-do, thao-luan, thong-bao; metadata không phải router.
- **Expected output:** Destination Screen ID/route, session retention và active navigation state chưa được map trong inventory/source hiện có. Không tự gán destination hoặc request.

### ST03-EV-09 — Footer navigation

- **Input:** Click footer links Terms, Privacy, Help.
- **Current:** href="#"; không có tài liệu/route đích hoặc handler.
- **Output:** Không có navigation/API hiện tại. Cần route/content contract trước khi implementation; WCAG badge trong footer là static claim, chưa được audit accessibility.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
