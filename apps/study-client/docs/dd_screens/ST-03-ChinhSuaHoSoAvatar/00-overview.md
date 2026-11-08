# ST-03 — Chỉnh sửa hồ sơ/avatar · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-03` |
| Module | Student |
| Route | `/student/profile/edit` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: dd_status: "BLOCKED"; implementation_status: "BLOCKED"; runtime_status: "NOT_VERIFIED"; **Trạng thái:** DD BLOCKED · IMPLEMENTATION BLOCKED · RUNTIME NOT VERIFIED |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-03.md](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/ST-03.md), [ST-03_PLAN.md](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/ST-03_PLAN.md), [ST-03_markers.json](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/ST-03_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Form chỉnh sửa fullname/phone/bio/avatar, theo dõi upload/save riêng.
- In-scope: GET #4 → nếu đổi avatar thì POST #13 → nhận tham chiếu chưa xác định → PUT #14 → GET #4 để đồng bộ; chặn khi mapping chưa chốt.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-11 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Form chỉnh sửa fullname/phone/bio/avatar, theo dõi upload/save riêng. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #04, #13, #14
- Liên kết màn hình dự kiến: [ST-02](../ST-02-HoSoCaNhan/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | dirty/uploading/saving/422/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-03 source screen.png](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/screen_annotated.png))
- Luồng: GET #4 → nếu đổi avatar thì POST #13 → nhận tham chiếu chưa xác định → PUT #14 → GET #4 để đồng bộ; chặn khi mapping chưa chốt.
- Priority: P1; Gate/source status: **M**; **BLOCK:** API #13/#14 chưa wired; avatar, bio, phone contract xung đột

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

---
screen_id: "ST-03"
title: "Chỉnh sửa hồ sơ/avatar"
screen_type: "Page"
dd_status: "BLOCKED"
implementation_status: "BLOCKED"
runtime_status: "NOT_VERIFIED"
review_date: "2026-11-06"
---

# ST-03 — Chỉnh sửa hồ sơ/avatar

> **Trạng thái:** DD BLOCKED · IMPLEMENTATION BLOCKED · RUNTIME NOT VERIFIED  
> Tài liệu này phân biệt thiết kế mong đợi với hành vi có source hiện tại. Mockup và HTML tĩnh không chứng minh Study Web hoặc API đã hoạt động khi chạy.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-03 — Chỉnh sửa hồ sơ/avatar |
| Mục tiêu | Cho Student xem và chỉnh sửa các trường hồ sơ được duyệt; tải avatar riêng; lưu profile và quay lại hồ sơ ST-02. |
| Actor | Student đã đăng nhập theo AC-11 và guard của API #04/#13/#14. Guest, Mentor và Admin không thuộc phạm vi trang này. |
| Route đề xuất | /student/profile/edit. Inventory ghi route đề xuất; Study Web chưa có router/source để xác minh. |
| Màn trước / sau | ST-02 → ST-03 → ST-02 theo inventory. Header/footer destinations khác chưa có route map được xác minh. |
| API liên quan | #04 GET /api/v1/users/me; #13 POST /api/v1/users/me/avatar; #14 PUT /api/v1/users/me/profile. Cả ba có source backend hiện tại; Study Web không có caller. |
| Điều kiện trước | Có Student access token hợp lệ. Backend guard yêu cầu JWT có sub là ID số dương và roles chứa STUDENT. Cách client duy trì/refresh session hoặc giữ return route chưa được xác minh trong Study Web. |
| Kết quả mong đợi | Profile được cập nhật theo hợp đồng đã thống nhất, avatar phản ánh trên UI, sau đó quay lại ST-02. AC-11 nêu hậu điều kiện này nhưng các trường bio/phone/avatar và bước reload còn mâu thuẫn với API source. |
| Tài sản | [Ảnh nguồn](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/screen.png), [HTML nguồn](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/code.html), [ảnh đánh số](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/screen_annotated.png), [bản đồ marker](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/ST-03_markers.json), [SVG overlay](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/ST-03_markers_overlay.svg), [kế hoạch](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/ST-03_PLAN.md). |

### Expected behavior và current behavior

| Chủ đề | Expected/design evidence | Current source evidence | Kết luận |
|---|---|---|---|
| Trang và session | Inventory đề xuất route trên; ST-03 nhận Student từ luồng đăng nhập SH-02 và quay về ST-02. | Không có Study Web package/source/router/entrypoint hoặc API client trong checkout. | Route/session handoff chưa chạy được; không tự tạo cách redirect hoặc cache. |
| Tải hồ sơ | Inventory/AC-11 yêu cầu GET #04 trước khi điền form. | API #04 được đăng ký; xác thực Student và trả safe UserProfile. Không có client gọi API. | Server source-backed; prefill, loading/error UI và cache chưa có bằng chứng. |
| Avatar | AC-11 và catalog mô tả POST #13 upload-only, rồi dùng avatar_url ở #14. | API #13 nhận JSON Data URL, xác thực nội dung, upload object và trả AvatarUploadResult. Không cập nhật DB. | Mô tả multipart/CDN trong mockup cũ, không phải request hiện tại. Storage thật chưa được xác minh. |
| Profile | API catalog/AC-11 yêu cầu full_name, bio, phone, avatar_url. | API #14 nhận full_name, phone, avatar_url; model bỏ qua bio; phone/avatar_url nullable; trả UserProfile không có bio. | DISCREPANCY/BLOCKER: chưa được phép thiết kế body, validation và UI thành một contract thống nhất. |
| Sau khi lưu | Inventory yêu cầu GET #04 sau PUT #14 để đồng bộ. | #14 dùng UPDATE ... RETURNING, commit và trả profile trực tiếp; không gọi #04. | DISCREPANCY/BLOCKER: quyết định có dùng PUT response hay GET lại chưa được chốt. |
| G-03 / controls | Mockup hiển thị Gate G-03 và khóa upload/phone/bio/save. | Cùng trạng thái được hard-code trong HTML; không có API gate, feature flag hoặc response lỗi gắn với pill/banner. Full name vẫn nhập được nhưng không có handler. | Chỉ là design state; không phải trạng thái runtime hoặc feature flag. |
