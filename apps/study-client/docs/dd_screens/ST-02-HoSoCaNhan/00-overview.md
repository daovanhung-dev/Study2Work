# ST-02 — Hồ sơ cá nhân · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-02` |
| Module | Student |
| Route | `/student/profile` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: Source status is described in the source DD. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-02.md](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/ST-02.md), [ST-02_PLAN.md](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/ST-02_PLAN.md), [ST-02_markers.json](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/ST-02_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Xem thông tin profile không lộ trường bảo mật; avatar/email/role/status.
- In-scope: GET #4 với Bearer; cache profile; profile có thể thiếu bio.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-11 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Xem thông tin profile không lộ trường bảo mật; avatar/email/role/status. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #04
- Liên kết màn hình dự kiến: [ST-03](../ST-03-ChinhSuaHoSoAvatar/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/ready/401/403 |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-02 source screen.png](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/screen_annotated.png))
- Luồng: GET #4 với Bearer; cache profile; profile có thể thiếu bio.
- Priority: P0; Gate/source status: **R**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-02 — Hồ sơ cá nhân (Page)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID | `ST-02` |
| Mục tiêu | Cho Student đã đăng nhập xem thông tin hồ sơ của chính mình mà không lộ thông tin xác thực. |
| Actor | `Student` với access JWT có role `STUDENT` theo AC-11/API #04. Mentor/Admin không được dùng endpoint Student này. |
| Route đề xuất | `/student/profile`; route chưa được triển khai trong Study Web checkout. |
| API | #04 `GET /api/v1/users/me`, current route/view/query/model source-backed. |
| Màn hình liên quan | SH-02 đăng nhập và role handoff; ST-01 có thể link tới profile; ST-03 sở hữu chỉnh sửa profile/avatar. Các liên kết là thiết kế/inventory, chưa có app router. |
| Ảnh | [Ảnh gốc](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/screen.png) · [Bản xem HTML](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/screen_rendered.png) · [Bản xem tổng hợp](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/screen_composite.png) · [Ảnh chú thích](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/screen_annotated.png). |
| Trạng thái | `DD BLOCKED` · `IMPLEMENTATION BLOCKED` · `RUNTIME NOT VERIFIED`. |

### Tiền điều kiện và hậu điều kiện

- **Tiền điều kiện mong muốn:** đã đăng nhập bằng Student; client có access token theo session contract và gọi API #04. API #04 current source tự xác minh Bearer JWT, claim và Student role trước query.
- **Hậu điều kiện mong muốn:** hiển thị trường hồ sơ an toàn do API trả về; từ ST-02 có thể đi tới ST-03 theo route được duyệt. Không đưa token, password hash hoặc PII vào URL.
- **Giới hạn:** source assets không có authenticated/ready profile state; current screenshot còn thiếu body; HTML là sign-in fallback. Không tự thiết kế loaded field layout, refresh/cache policy, status handling hoặc profile edit flow.

### Expected behavior và current behavior

| Chủ đề | Expected theo inventory/AC/API design | Current evidence |
|---|---|---|
| Actor/state | Student đã đăng nhập; `/student/profile`; expected `loading/ready/401/403`; hiển thị avatar/email/role/status. | PNG gốc chỉ có header/footer; HTML có empty sign-in card, sign-in links, edit button disabled. Hai assets không đồng nhất; chưa có Study Web source/router. |
| Profile request | GET #04 với Bearer; profile được cache theo inventory; #04 dùng trong AC-11 và sau login Student theo AC-02/F01. | Route #04 nhận một Authorization header; current view gọi shared Bearer/JWT/role guard rồi đọc profile. Study Web không gửi request. |
| Auth claims | Catalog/AC-02 yêu cầu JWT + Student role; AC-02 diagram viết `user_id`/`role`. | Current #03 phát `sub` và `roles`; #04 parse `sub` thành positive integer và yêu cầu `STUDENT` trong `roles`. Đây là discrepancy, không tự sửa diagram/catalog. |
| Response data | Catalog: `ApiEnvelope<UserProfile>`; AC-02 nói profile/role/permissions; catalog đánh dấu `bio` optional. | Current query/model trả `id`, `full_name`, `email`, `role`, nullable `avatar_url`/`phone`, `status`, timestamps; không có `bio` hoặc permissions. API #04 DD còn Draft. |
| Status/role freshness | Student role và tài khoản hợp lệ. | Current auth guard chỉ xem role trong JWT; SELECT không so `users.role` hoặc lọc `users.status`; status chỉ được trả về. DDL candidate không có `NOT NULL` cho status trong khi model bắt buộc. |
| Edit action | ST-03 là màn chỉnh sửa; AC-11 tham chiếu #13/#14. | HTML hiển thị “Chỉnh sửa hồ sơ (Tạm khóa)” với button disabled; không có handler. Không mở edit hoặc upload/save behavior từ ST-02. |
| Navigation/runtime | SH-02 role flow, ST-01/ST-03 navigation; cache/session theo approved contract. | Header/footer/login anchors `href="#"` với `data-path`; không có Study Web runtime/router/client. |

### Quy tắc nghiệp vụ và bảo mật

1. Chỉ gọi #04 cho Student; route phải được bảo vệ ở client sau khi Study Web auth/session contract tồn tại, nhưng backend #04 vẫn là ranh giới xác thực/ủy quyền thực sự.
2. Không lấy user ID từ route/query/body. Current #04 lấy subject `sub` từ access JWT đã kiểm tra, sau đó SELECT theo `users.id`.
3. Không hiển thị `password_hash`, access/refresh token, signing secret hoặc dữ liệu ngoài allowlist response. Current query không đọc password hash; current model bỏ các field extra.
4. Không kết luận quyền hiện tại từ response `data.role` hoặc `data.status`: access guard hiện tin JWT `roles`; không so với DB role/status. Chặn/đổi role, token freshness và account revocation behavior cần quyết định.
5. `bio` và `permissions` không được bịa hoặc giữ trong client như thể API #04 trả về. `phone` có trong current response nhưng chưa xuất hiện trên ST-02 inventory/UI; không tự thêm vào display layout.
6. Không enable edit button hoặc gộp APIs #13/#14 vào ST-02. Upload avatar và profile update thuộc ST-03; API #13 upload và #14 update là các side effect khác nhau.
7. Không coi `screen_rendered.png` hoặc `screen_composite.png` là runtime UI; đây là ảnh tĩnh từ HTML source và ảnh tổng hợp có ghi provenance, còn `screen.png` gốc giữ nguyên.
