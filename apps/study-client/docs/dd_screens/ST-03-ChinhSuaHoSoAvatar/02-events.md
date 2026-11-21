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
| ST03-EV-01 | Mở trang và tải profile — Load | Route ST-03 | `/student/profile/edit` requests #04 via StudentApiService; binds profile fields and shows loading/error/retry states. |
| ST03-EV-02 | Thay đổi họ tên — Input/Change | #14 | Editable `full_name`, trimmed and validated before save; no separate dirty indicator. |
| ST03-EV-03 | Tương tác email — Input/Focus | #15 | Read-only; không đổi dữ liệu. |
| ST03-EV-04 | Chỉnh phone / Bio bị khóa — Input/Change | #16, #17 | Phone editable; Bio remains disabled because API/DB source has no bio field. |
| ST03-EV-05 | Tải avatar — Click/Upload | #11 | File picker validates MIME/size, previews the Data URL, and calls #13 after explicit upload. |
| ST03-EV-06 | Lưu hồ sơ — Submit/Click | #19 | Explicit submit calls #14 with supported fields, then #04; successful refresh returns to ST-02. |
| ST03-EV-07 | Quay về hồ sơ — Click/Anchor | #7, #18 | Angular page uses RouterLink to ST-02 at `/student/profile`; browser runtime is unverified. |
| ST03-EV-08 | Header brand/navigation — Click/Anchor | #1, #2 | Home, progress, discussions and notifications map to declared routes; “Khóa học của tôi” remains noninteractive because ST-08 has no route. |
| ST03-EV-09 | Footer navigation — Click/Anchor | #26 | Legal/help destinations remain text because no route/content mapping is available. |

### ST03-EV-01 — Mở trang và tải profile

- **Input:** Route `/student/profile/edit`; không có path/query/body. StudentApiService gets the access token from StudentSessionService; server validates the Student role.
- **Tiền điều kiện:** App/router tồn tại và user có Student session. API #04, #13, #14 đều kiểm tra JWT Bearer và role STUDENT ở server; client guard chưa được xác minh.
- **Quy trình dự kiến:**
  1. Resolve route và yêu cầu session theo auth contract đã duyệt.
  2. Gửi GET #04 tới /api/v1/users/me, một header Authorization: Bearer <access-token>, không path/query/body.
  3. Backend hiện parse JWT, lấy sub numeric và roles; yêu cầu STUDENT rồi SELECT profile theo users.id.
  4. Thành công: HTTP 200, businessCode=DESIGN_RESOURCE_RETRIEVED, data=UserProfile, meta={}, có traceId. Fields hiện có: id, full_name, email, role, avatar_url nullable, phone nullable, status, created_at, updated_at. Không có bio.
  5. Chỉ map các field theo UI contract đã duyệt. Candidate mapping là full_name → #14, email → #15, phone → #16, avatar_url → #8; phone/avatar bị khóa bởi design và bio không có nguồn. Do đó không tự prefill/enable các control khi chưa có loaded-state design.
  6. Không có cache policy, duplicate request policy hoặc refresh-after-save policy được xác minh.
- **Response/error:** 401 DESIGN_AUTHENTICATION_REQUIRED khi thiếu/sai Bearer hoặc user row không tồn tại; 403 DESIGN_ACCESS_DENIED nếu JWT thiếu role STUDENT; 500 DESIGN_INTERNAL_ERROR khi query/mapping/token configuration lỗi. API #04 không lọc DB status hoặc so DB role với JWT role.
- **Kết quả UI:** Current Angular page calls #04, binds `full_name`, `email`, nullable `phone`, and a safe HTTP(S) avatar URL; loading/error/retry states are present. Browser/API/DB runtime remains unverified.

### ST03-EV-02 — Thay đổi họ tên

- **Input:** Editable `full_name` field, prefilled from #04; HTML sets `required` and `maxlength=150`.
- **Current:** Input updates component state. On submit the page trims the value, rejects blank or over-150 values, and sends the normalized value only when the user saves.
- **API mapping:** #14 server also trims, rejects blank and limits the value to 150 characters. Client validation matches those source rules; it does not add a name format rule.
- **Output:** Dirty profile state enables the save action; validation errors remain on the page and do not call #14.

### ST03-EV-03 — Email readonly

- **Input:** Không có giá trị nhập được; readonly=true.
- **Quy trình:** Focus/copy (nếu browser cho phép) không sửa trường; không gọi API. data.email của #04 là nguồn server candidate, placeholder hiện tại là mẫu tĩnh.
- **Output:** Không thay đổi state. Chính sách copy-to-clipboard hoặc email update ngoài màn này không được định nghĩa.

### ST03-EV-04 — Chỉnh phone / Bio bị khóa

- **Input:** Phone is editable; Bio textarea remains disabled.
- **Quy trình:** Phone is trimmed; blank becomes `null`; values longer than 20 characters are rejected before #14. The request always includes `phone`.
- **Current API evidence:** #14 accepts nullable phone and normalizes blank to null, with a 20-character maximum. Bio is ignored by the request model and absent from #04/DB; the client never submits it.
- **Output:** Phone changes become part of the next explicit profile save. Bio remains visible but cannot be edited or persisted.

### ST03-EV-05 — Tải avatar

- **Input:** File picker accepts PNG/JPEG/WebP. Client rejects empty files and files larger than 5 MiB, then reads a Data URL for preview.
- **Quy trình:** Explicit “Tải ảnh lên” sends only `{ image: <Data URL> }` to POST #13 with Student Bearer. No multipart fields or extra body keys are sent.
- **Backend:** #13 checks Student auth, decodes the Data URL, enforces the 5 MiB decoded limit and MIME signature, writes `avatars/{user_id}`, and returns HTTP 201 `DESIGN_RESOURCE_CREATED` with `data.avatar_url`. It does not update the profile DB row.
- **Output:** On success the returned URL is staged and shown in preview; the next explicit save uses it in #14. On failure the page shows an error and does not claim the profile was saved.
- **Lỗi:** 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; invalid Data URL/empty/base64/oversize/signature mismatch → 422 DESIGN_VALIDATION_ERROR với fieldErrors; body schema/type errors → request validation 422; provider/config failure → 500 DESIGN_INTERNAL_ERROR. Provider cấu hình từ biến môi trường; thời gian kết nối 5s, đọc 30s, một attempt.
- **Ngoại lệ:** Upload là external side effect, không có DB transaction/compensation. Cùng user key bị ghi đè. Không tự retry do không có idempotency contract. Storage live chưa được xác minh.

### ST03-EV-06 — Lưu hồ sơ

- **Input:** Explicit form submit after profile load; current value set is `full_name`, `phone`, and current or newly returned `avatar_url`. Bio is excluded.
- **Sequence trong inventory:** GET #04 lúc load → nếu avatar thay đổi POST #13 → PUT #14 → GET #04 để đồng bộ.
- **Current source-backed server behavior:**
  1. API #14 là PUT /api/v1/users/me/profile, JSON body bắt buộc có full_name (string), phone (string|null), avatar_url (string|null); không có path/query; Authorization Bearer Student.
  2. Request model cho phép field extra nên body có bio không bị từ chối, nhưng bio bị bỏ qua. Không gửi bio như thể được cập nhật.
  3. Validator trim full_name, từ chối blank, tối đa 150; trim nullable phone/avatar_url và đổi chuỗi trống thành null; phone tối đa 20. avatar_url không được kiểm tra URI hay ràng buộc với object vừa upload.
  4. Query UPDATE users SET full_name, phone, avatar_url, updated_at=CURRENT_TIMESTAMP WHERE id=:user_id RETURNING các safe profile fields. Backend map UserProfile, commit và trả envelope.
  5. Thành công HTTP 200 DESIGN_RESOURCE_UPDATED; data là UserProfile trực tiếp trong response envelope. Không gọi #04 tiếp theo.
  6. Client checks the response envelope and profile shape, then calls GET #04 again as the inventory requires. It navigates to ST-02 only after that read succeeds.
- **Lỗi:** Thiếu/sai auth 401 DESIGN_AUTHENTICATION_REQUIRED; không đúng Student 403 DESIGN_ACCESS_DENIED; thiếu required body/type validation 422 VALIDATION_ERROR; semantic full_name/phone validation 422 DESIGN_VALIDATION_ERROR; user row không tồn tại trả 401; DB/mapping/commit lỗi 500 DESIGN_INTERNAL_ERROR và rollback DB transaction.
- **Trùng lặp/partial failure:** Không có idempotency key, FE debounce, retry policy hoặc conflict resolution được xác minh. Nếu POST #13 đã ghi object nhưng PUT #14 thất bại, object vẫn tồn tại hoặc đã ghi đè avatar cũ. Không có compensation/cleanup source. Không tự gửi request lần nữa.
- **Kết quả hiện tại:** A successful #14 followed by #04 navigates to ST-02. If #14 fails, the update is not auto-retried. If #04 fails after #14 succeeds, the page keeps the returned profile, offers a #04-only retry, and does not resend #14.

### ST03-EV-07 — Quay về ST-02

- **Input:** Click #7 hoặc #18.
- **Current:** Angular RouterLink chuyển tới `/student/profile`; không chuyển profile PII qua URL.
- **Expected:** Inventory chỉ định quay về ST-02 (/student/profile); không có path/body/query contract. Không truyền profile PII qua URL. Việc giữ dirty data/cache hoặc reload ST-02 sau khi save thành công chưa được chốt.
- **Output:** Không có route event hoặc API call hiện tại.

### ST03-EV-08 — Header brand/navigation

- **Input:** Click #1 hoặc một mục #2.
- **Current:** Angular header links to source-declared home, progress, discussions and notifications routes. “Khóa học của tôi” is text because ST-08 remains unrouted.
- **Expected output:** Session retention and active-navigation design remain unresolved; navigation does not trigger profile API requests.

### ST03-EV-09 — Footer navigation

- **Input:** Click footer links Terms, Privacy, Help.
- **Current:** Footer destinations are static text because no destination routes/content are mapped.
- **Output:** Không có navigation/API hiện tại. Cần route/content contract trước khi implementation; WCAG badge trong footer là static claim, chưa được audit accessibility.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
