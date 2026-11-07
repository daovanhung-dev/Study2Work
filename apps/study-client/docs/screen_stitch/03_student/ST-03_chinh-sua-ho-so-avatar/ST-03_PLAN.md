# ST-03 — Kế hoạch chi tiết

> Ngày rà soát: 2026-11-06
>
> Trạng thái: `PLAN COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`

## 1. Phạm vi và phân loại

```text
primary_task_type: docs
secondary_task_types: []
project_scopes: [web-work, server-study]
cross_scope_dependencies: [ST-03 APIs #04/#13/#14; authenticated Student session from SH-02; profile return to ST-02]
```

- Chỉ xử lý **ST-03 — Chỉnh sửa hồ sơ/avatar (Page)** trong phiên này.
- Inventory: route đề xuất `/student/profile/edit`; AC-11; APIs #04, #13, #14; actor Student; điều hướng quay lại ST-02.
- Inventory dự kiến GET #04 để nạp profile; nếu đổi avatar thì POST #13, PUT #14 và GET #04 để đồng bộ. Trạng thái được liệt kê gồm `dirty/uploading/saving/422/error`.
- Theo `list_screen.md` §8.1, ST-03 thuộc W1; không xử lý màn hình khác trong phiên này.
- Skill registry/manifest loại trừ `web-ui-only-dd` khỏi `createDD-markdown`; không có skill canonical cho UI-only DD. Không dùng API DD template thay cho contract màn hình.

## 2. Asset và baseline

- Trước phiên, thư mục chỉ có `screen.png` và `code.html`; giữ nguyên cả hai.
- `screen.png`: PNG hợp lệ 1418×1600, SHA-256 `acd143a1a7d5dae4936f9bc8a3d51d015ba1fb501998a5434e96b57942d77fdc`. Ảnh thể hiện trang chặn Gate G-03, form, diagnostic panel và footer.
- `code.html`: SHA-256 `a8c9ebca162d9ac677b65ede88543d9a932c85b4cffed05093f263d24de511b3`. Firefox headless render tạm ở 1418×1600 được xem để so sánh; bố cục và copy khớp asset, nhưng render chỉ là HTML tĩnh và không phải runtime.
- Annotate trực tiếp `screen.png` vào `screen_annotated.png`, giữ đủ 26 marker theo nhóm component/control. Dựng `ST-03_markers_overlay.svg` làm overlay có thể kiểm tra; không sửa HTML để biến controls tĩnh thành hoạt động.
- HTML có anchors `href="#"`; full-name input có thể nhận text natively nhưng không có handler; email `readonly`; phone, bio, upload và save `disabled`; form chỉ có inline onsubmit return false; không có handler nghiệp vụ/API, router, fetch/XHR hay session binding.

## 3. Expected behavior và current evidence

| Chủ đề | Expected/design source | Current evidence | Tác động |
|---|---|---|---|
| Actor/route | AC-11: Student đã đăng nhập; route đề xuất `/student/profile/edit`, quay về ST-02. | Study Web không có app source/package/router/entrypoint. HTML links đều `href="#"`; route chưa chạy được. | Không khẳng định session guard, route history hay navigation runtime. |
| Load profile | Inventory/AC-11: GET #04 với Student Bearer để có dữ liệu form. | #04 current route/view/query/model có source; guard yêu cầu role `STUDENT`, đọc theo numeric JWT `sub`, trả safe profile; không có UI caller. | Prefill, loading và client cache chưa được xác minh. |
| Avatar upload | AC-11 gọi POST #13 trước khi lưu profile; inventory để response reference chưa khóa. | #13 current route nhận JSON Data URL `image`; kiểm tra PNG/JPEG/WebP, chữ ký và tối đa 5 MiB sau giải mã; upload Object Storage tại `avatars/{user_id}`; response `AvatarUploadResult.avatar_url`, không query/update DB. | Screenshot gọi nhầm multipart/CDN và mô tả #13 halted; đó là diagnostic tĩnh cũ, không khớp current API source. Storage thật chưa được xác minh. |
| Profile update | Catalog/API contract yêu cầu `full_name`, `bio`, `phone`, `avatar_url`. | #14 current route/model chỉ nhận `full_name`, `phone`, `avatar_url`; `bio` là extra bị bỏ qua. Phone/avatar URL có thể null; full name trim/nonblank/max 150, phone trim/blank→null/max 20; avatar URL chỉ trim, không kiểm URI. | G-03 vẫn là `DISCREPANCY`; không giả định bio được lưu hoặc avatar URL được ràng buộc với kết quả #13. |
| Persistence/result | AC-11 mô tả update rồi load lại profile. | #14 làm một `UPDATE users ... RETURNING` theo user ID từ JWT, cập nhật full_name/phone/avatar_url/updated_at; validate `UserProfile`, commit rồi trả profile trực tiếp. Không gọi #04. | Quyết định có cần GET #04 thứ hai sau PUT còn mở; external #13 và DB #14 không cùng transaction. |
| Current UI state | Design page cho biết Gate G-03 blocked và vô hiệu hóa upload/phone/bio/save. | Full name input vẫn active nhưng không có submit handler; email readonly, phone/bio/upload/save disabled. Nút/link quay về đều fragment-only. Không có dữ liệu/API/network state. | Đây là prototype/design state, không phải response lỗi hoặc gate runtime. |

### Discrepancies cần giữ nguyên

- `list_screen.md` còn ghi API #13/#14 `not wired`; current `app/api/v1.py` hiện đăng ký cả hai route và module/test source tương ứng tồn tại. Đây là discrepancy giữa inventory và current backend source; Study Web vẫn `UNWIRED`.
- API #13 `list_api.md`/DD #13 và current source dùng JSON Data URL, `AvatarUploadResult`; G-03 và diagnostic card trên màn hình còn mô tả multipart/CDN và `UserProfile`/schema mismatch.
- API #14 contract yêu cầu bio và phone không nullable, avatar URL dạng URI; current source bỏ bio, nhận phone/avatar_url nullable, và không validate URI. Current response cũng không có bio.
- `infra/postgres/study-server/DB.sql` cho `users.phone` nullable và không có `users.bio`; `users.status` cũng nullable trong DDL trong khi `UserProfile.status` required. DDL là candidate, live schema `NOT_VERIFIED`.
- AC-11/inventory yêu cầu GET #04 sau PUT; current #14 trả `UserProfile` trong cùng response `UPDATE RETURNING`, không tự gọi #04. API DD #14 vẫn ghi runtime module absent, trái với source hiện tại.
- Nếu #13 upload thành công rồi #14 lỗi, Object Storage side effect không rollback theo DB transaction; cùng user ID dùng cùng object key, upload mới ghi đè key đó. Không có cleanup/idempotency policy riêng được source xác nhận.

## 4. Planned marker và event coverage

Tạo 26 marker theo thứ tự đọc từ trên xuống, mỗi marker có đúng một hàng element trong DD:

1. Brand/logo link; 2. primary navigation; 3. account identity/avatar; 4. breadcrumb; 5. Gate G-03 status pill; 6. warning banner/title/copy; 7. back link trong banner; 8. avatar preview/lock overlay; 9. account/source label; 10. Avatar Asset Pipeline diagnostic; 11. disabled upload button; 12. safe-mode notice; 13. profile form surface/title/description; 14. full-name field/help/API #04 badge; 15. readonly email field/help; 16. disabled phone field/badge/schema warning; 17. disabled bio field/badge/schema warning; 18. back link dưới form; 19. disabled save button; 20. API #14 mapping note; 21. Developer Hand-off heading/route context; 22. API #13 diagnostic; 23. API #14 diagnostic; 24. proposed-next-step notice; 25. copyright/accessibility footer; 26. footer navigation.

Event IDs dự kiến:

- `ST03-EV-01` mở trang và nạp profile qua #04 (expected); current UI không gọi API.
- `ST03-EV-02` nhập full name; native field hoạt động trong HTML nhưng không gắn dirty/save logic.
- `ST03-EV-03` email readonly; không nhận chỉnh sửa.
- `ST03-EV-04` phone/bio disabled; browser không sửa được và không phát save.
- `ST03-EV-05` upload avatar; button disabled, không có file picker/action hiện tại. Expected sequence #13 Data URL → lấy `avatar_url` chỉ để gửi sang #14.
- `ST03-EV-06` lưu hồ sơ; save button disabled. Expected sequence khi gate được quyết định: validate body theo contract đã chốt → tùy avatar có đổi hay không gọi #13 → PUT #14 → xử lý response và quy tắc reload #04 chưa chốt. Current endpoint/test source được mô tả riêng, không tuyên bố UI thực hiện.
- `ST03-EV-07` quay về ST-02 qua hai link `href="#"`; hiện chỉ fragment navigation.
- `ST03-EV-08` header brand/navigation; anchors static, không map Screen IDs trong app runtime.
- `ST03-EV-09` footer navigation; anchors static, không có destination binding.

## 5. Output, acceptance và verification

- Đã tạo `ST-03_PLAN.md` trước DD/annotation; giữ nguyên hai source assets và đối chiếu hash trước/sau.
- Đã tạo `ST-03_markers.json`, SVG overlay, `screen_annotated.png`, và `ST-03.md`; marker order/Element ID ánh xạ 1:1. Không đánh dấu data-only text thành event hoặc disabled controls thành hoạt động.
- `ST-03.md` bao gồm overview, expected/current flow, 26 elements, 9 events, current API #04/#13/#14 mapping/errors/effects, state/navigation matrix, security/privacy, discrepancies và acceptance checklist.
- Đã đọc test source #13/#14 nhưng không chạy test theo yêu cầu; ghi rõ test fake storage/session và DDL không chứng minh live S3, DB schema/deployment hay Study Web runtime.
- Đã cập nhật global tracker: ST-03 có trạng thái DD/implementation/runtime riêng; 16/83 artifact bundles, còn 67; điểm tiếp tục W1 là ST-08. Không bắt đầu Screen ID tiếp theo trong phiên này.
- Giữ `DD BLOCKED` vì bio/phone/avatar mapping và reload contract chưa khóa; `IMPLEMENTATION BLOCKED` vì Study Web không có app runtime và thiết kế gate giữ thao tác save/upload disabled; `RUNTIME NOT VERIFIED` vì không chạy client/live S3/production DB.

## 6. Preflight record

- Đọc `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`; selector `node scripts/select-worklogs.mjs --type docs --limit 3` trả `READY`, chọn 3/168, không thiếu.
- Đọc riêng GS-01, GS-02, GS-03 worklogs đã chọn; ghi carry-forward trong worklog ST-03.
- Đọc project index/architecture/dependencies, web-work và Study Web subcontext, Study Server entry/index và các page module/auth/database/tests/workflow liên quan, skill registry và `context-manifest.json`.

## 7. Kết quả static audit

- `ST-03_markers.json`: 26 ID tuần tự; `ST-03.md`: 26 hàng element khớp ID; SVG có 26 circle và 26 số.
- `screen.png` giữ nguyên hash `acd143a1a7d5dae4936f9bc8a3d51d015ba1fb501998a5434e96b57942d77fdc`; `code.html` giữ nguyên hash `a8c9ebca162d9ac677b65ede88543d9a932c85b4cffed05093f263d24de511b3`.
- Ảnh nguồn 1418×1600; ảnh chú thích 2996×3200. Link tương đối trong DD đều tồn tại; xem lại ảnh chú thích cho thấy marker ở gutter và không che giao diện. `git diff --check` sạch.
- Không chạy test, không xác minh app runtime, live DB hoặc Object Storage.
