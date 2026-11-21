# ST-03 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### Luồng dự kiến theo inventory và AC-11

1. Student mở route đề xuất từ ST-02 hoặc Student navigation. Không truyền PII trong URL; route và session handoff chưa có source client để xác minh.
2. Client cần kiểm tra trạng thái đăng nhập và token theo auth/session contract dùng chung. Đây là phụ thuộc SH-02; không suy ra từ tên mẫu “Nguyễn Văn A” trên mockup.
3. Client gọi GET #04 bằng Authorization: Bearer token để lấy dữ liệu profile an toàn. Response hiện tại không có bio.
4. Khi thành công, client phải chờ quyết định mapping cho các field. Full name/email/phone/avatar_url có mặt trong #04 (phone/avatar_url nullable); bio không có. Mockup chưa phải loaded-state đã xác minh.
5. Khi người dùng chọn avatar, luồng dự kiến gọi POST #13 trước. API nhận JSON body {image: Data URL}; sau kiểm tra ảnh, ghi object storage theo avatars/{user_id} và trả data.avatar_url. API #13 không ghi DB.
6. Khi người dùng lưu, luồng dự kiến gọi PUT #14 với các trường body đã được chốt. Inventory hiện yêu cầu #04 lần nữa sau PUT, trong khi current #14 đã trả UserProfile trực tiếp. Không chọn một trong hai cách trước khi contract owner quyết định.
7. Sau thành công, UI dự kiến phản ánh profile và cho phép quay lại ST-02. Hành vi giữ dữ liệu, thông báo thành công, cache và lịch sử quay lại chưa được triển khai/đặc tả.
8. Lỗi 401/403/422/500 của backend cần được ánh xạ sang UI/SH-05 theo policy đã duyệt; Study Web hiện không có error mapping.
9. Nếu #13 thành công nhưng #14 lỗi, object đã upload không rollback theo transaction DB. Cùng user dùng cùng object key nên lần upload mới ghi đè object hiện có. Không tự retry hoặc xóa object khi chưa có policy được duyệt.

### Hành vi hiện có trong asset và source

- screen.png là ảnh thiết kế tĩnh 1418×1600. SHA-256 trước/sau cần giữ nguyên: acd143a1a7d5dae4936f9bc8a3d51d015ba1fb501998a5434e96b57942d77fdc.
- code.html là HTML trình bày tĩnh. Firefox headless render tạm ở cùng viewport đã được xem để so sánh layout/copy; render không phải runtime capture và không phải tài sản thay thế ảnh gốc.
- Các chi tiết `href="#"`, `data-path` và inline `onsubmit` trong hai bullet dưới đây mô tả Stitch `code.html`, không mô tả Angular runtime hiện tại.
- In Angular source, `/student/profile/edit` calls #04 through StudentApiService and binds response-backed profile fields. Full name and phone are editable; email is read-only; Bio stays disabled because the source schema omits it.
- Selecting an avatar reads a Data URL and checks MIME/size; the explicit upload action calls #13. A successful URL is held for the subsequent #14 update. The page then calls #04 and navigates to ST-02 only after that refresh succeeds.
- StudentSessionService supplies the Bearer token for all three requests. The page uses separate loading, validation, upload, save, and saved-but-refresh-pending states; no client profile cache is added.
- The remaining Bio note describes the API/DB source gap. Header/footer route gaps remain unchanged; live API/database/object-storage and browser runtime are not verified.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| State | Điều kiện / evidence | UI outcome / ranh giới |
|---|---|---|
| Static gate | Screenshot/HTML source state. | Current page retains a concise Bio limitation note; other supported controls are active. |
| Loading | GET #04 or saved-profile refresh is pending. | Status message; edit/upload/save actions are disabled while profile data is loading. |
| Profile loaded | #04 success with a valid UserProfile envelope. | Bind profile data, show only a valid HTTP(S) avatar URL, and initialize editable values. |
| Dirty | Supported profile value differs from loaded value or a new avatar was uploaded. | Enables Save after validation; unsupported Bio does not become dirty or enter the request. |
| Uploading | File reading or POST #13 is active. | Status message; save is disabled until upload completes. |
| Saving | PUT #14 is active. | Duplicate submit is blocked and editable controls are disabled. |
| Validation error / 422 | Client field validation or API #13/#14 error. | Show an inline error; do not claim the profile changed. |
| Request error | API #04/#13/#14 returns an error or cannot be reached. | Show retry for profile reads; never auto-repeat the profile mutation. |
| Saved / refresh pending | #14 succeeds but follow-up #04 has not succeeded. | Keep returned profile data and expose a GET #04 retry; do not resend #14. |
| Return | Follow-up #04 succeeds or user follows an ST-02 link. | Successful save routes to ST-02; route navigation does not include PII. |

### Điều hướng

- ST-02 → ST-03: route `/student/profile/edit` is source-wired; ST-02's current edit entry remains disabled.
- ST-03 → ST-02: successful #14 followed by #04 navigates to `/student/profile`; visible return RouterLinks also lead there; no user ID or PII is included in the URL.
- SH-02/session handoff: StudentLayout and StudentSessionService provide the current in-memory Student Bearer; API enforces the Student role. Live session persistence/refresh remains unverified.
- Header/footer destinations: chưa xác định từ app router. Không thêm route giả định.
- No profile cache, dirty-state confirmation, or returnTo behavior is added. Post-save refresh uses #04; a failed refresh can retry #04 without repeating #14.

## 4. Luồng đọc (Read)
- Orchestration hiện tại: GET #04 → nếu đổi avatar thì POST #13 → PUT #14 với full_name/phone/avatar_url → GET #04 để đồng bộ → ST-02. Bio không được gửi; nếu upload thành công nhưng PUT lỗi thì object storage không rollback.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ST-03](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/ST-03.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
