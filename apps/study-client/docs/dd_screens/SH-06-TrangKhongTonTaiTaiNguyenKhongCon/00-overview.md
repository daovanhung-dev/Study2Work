# SH-06 — Trang không tồn tại / tài nguyên không còn · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `SH-06` |
| Module | Shared / Auth / System |
| Route | `/not-found` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái:** `DD BLOCKED` cho tới khi chốt recommendation/contact/footer surfaces và giải quyết discrepancy AC-05; `IMPLEMENTATION BLOCKED` vì Study Web router/source và các dependency đó chưa có; `RUNTIME NOT VERIFIED`. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [SH-06.md](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/SH-06.md), [SH-06_PLAN.md](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/SH-06_PLAN.md), [SH-06_markers.json](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/SH-06_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Thông báo 404 không tiết lộ draft/private, cung cấp quay về khóa học.
- In-scope: Router 404 hoặc resource 404 chuyển state; không chuyển 500 thành 404.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-05 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Thông báo 404 không tiết lộ draft/private, cung cấp quay về khóa học. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #08
- Liên kết màn hình dự kiến: [GS-01](../GS-01-DanhSachKhoaHoc/00-overview.md), [SH-01](../SH-01-TrangGioiThieuStudyVariant1/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | route-404/resource-404 |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [SH-06 source screen.png](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/screen_annotated.png))
- Luồng: Router 404 hoặc resource 404 chuyển state; không chuyển 500 thành 404.
- Priority: P0; Gate/source status: **D**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# Tài liệu thiết kế chi tiết màn hình — SH-06 Không tìm thấy trang / tài nguyên

> **Mã màn hình:** SH-06 · **Loại:** state view · **Tác nhân:** khách hoặc người dùng truy cập route/tài nguyên không khả dụng
> **Route đề xuất:** `/not-found` · **AC:** AC-05 · **API catalog:** #08 · **Route liên quan:** GS-01, SH-01
> **Trạng thái:** `DD BLOCKED` cho tới khi chốt recommendation/contact/footer surfaces và giải quyết discrepancy AC-05; `IMPLEMENTATION BLOCKED` vì Study Web router/source và các dependency đó chưa có; `RUNTIME NOT VERIFIED`.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan màn hình

SH-06 hiển thị một state 404 chung cho hai trường hợp: router không tìm thấy route (`ROUTE_404`) hoặc API #08 không tìm thấy khóa học đã publish (`RESOURCE_404`). Nội dung không phân biệt khóa học không tồn tại với khóa học chưa được publish, nhờ đó không tiết lộ draft/private. Lỗi dịch vụ, lỗi mạng hoặc quyền truy cập không được đổi thành 404.

| Thuộc tính | Đặc tả |
|---|---|
| Mục tiêu | Giải thích rằng route/tài nguyên không khả dụng và đưa người dùng tới nơi công khai tiếp theo. |
| Actor/Role | Khách hoặc người dùng bất kỳ. API #08 là public, không yêu cầu Bearer token. |
| Route | `/not-found` là đề xuất trong inventory; không có Study Web router/source để xác minh. State có thể được mở bởi route fallback hoặc bởi response resource 404. |
| API | API #08 `GET /api/v1/courses/{course_id}` khi flow từ course detail. SH-06 không tự gọi #08 khi mở route lỗi. Trạng thái được ghi khác nhau: dòng SH-06 trong inventory ghi BE `D`, API index §5 ghi #008 `R`, API contract tổng thể đã được duyệt nhưng chưa runtime-verified, còn API DD #08 ghi `Draft — Needs Confirmation`; route/module/test source hiện có. |
| Điều kiện trước | Direct route: router xác định path không khớp. Resource: request #08 từ flow GS-03 nhận HTTP 404 `DESIGN_RESOURCE_NOT_FOUND`. Không lấy 500/mạng làm điều kiện mở SH-06. |
| Điều kiện sau | Người dùng có thể tới GS-01 `/courses` hoặc SH-01 `/`. 200 từ #08 ở flow course detail phải tiếp tục GS-03; 403 đi theo state access-denied (SH-05); 500/mạng ở service-error state riêng. |
| Liên kết màn hình | [GS-01 prototype](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/code.html), [SH-01 DD](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01.md). GS-01 là target route nhưng chưa có DD trong checkout. |
| Trạng thái triển khai | `screen.png` và `code.html` là tài sản design-only. Study Web `src/` và `package.json` vắng mặt. `dist/` bundle build có trong máy nhưng không chứa route identifier SH-06 và không thay thế source có thể build/sửa. |

### 1.1 Expected behavior và current behavior

| Hạng mục | Expected behavior theo inventory/AC/API design | Current source evidence |
|---|---|---|
| Route 404 | Route đề xuất `/not-found`; cung cấp link tới GS-01 và SH-01. | Client router không có source. Prototype `code.html` có các anchor `href="#"`; không có handler navigation. |
| Resource 404 | API #08 404 không tiết lộ draft/private; route hoặc resource 404 dẫn tới SH-06. | Current query lọc `courses.status='PUBLISHED'`; invalid ID, record không có hoặc chưa publish cùng trả HTTP 404 `DESIGN_RESOURCE_NOT_FOUND`. |
| API #08 status/shape | API contract khai báo `ApiEnvelope<Page<Course>>`, 200/404/500; API DD #08 còn ở trạng thái draft. Dòng SH-06 ghi BE `D`, trong khi API index §5 ghi #008 `R`. | `app/api/v1.py`, module #08 và test source đều có. Current success envelope có `data: Page<Course>` singleton. Đây là sai khác giữa các nhãn trạng thái và source hiện hành; source không chứng minh deployment/runtime. |
| 403 | AC-05 diagram thể hiện nhánh `404/403` khi course không tồn tại/PUBLISHED; API catalog chỉ liệt kê 404/500. | #08 hiện public, không có 403 branch. Invalid/missing/unpublished là 404; query/mapping error là 500. Cần owner xác nhận/sửa AC; nếu guard khác thật sự trả 403, giữ riêng theo access-denied flow. |
| Service error | 500/mạng không bị biến thành 404. | Module #08 trả 500 `DESIGN_INTERNAL_ERROR` khi query/mapping lỗi. Inventory global yêu cầu service error riêng; Study Web service-error component chưa có source. |
| Khóa học gợi ý | Cần quyết định giữ/bỏ section và xác nhận nguồn, schema, ID, copy, thứ tự; không render dữ liệu giả. | HTML có ba card viết cứng, không có course ID/API mapping. API #06 có trong catalog nhưng chưa là dependency SH-06 và không quy định recommendation semantics. `BLOCKER`. |
| Support/footer | Cần quyết định giữ/bỏ từng control và xác nhận route/contact/legal copy trước khi ship. | Contact CTA và 4 footer links dùng `href="#"`; chứng chỉ, quy chế và hỗ trợ chưa có route/channel contract tại SH-06. `BLOCKER`. |

`code.html` là prototype. Giá trị course, category, duration, learner count, copy hợp tác doanh nghiệp, copyright year và đường dẫn `#` không phải dữ liệu/business contract. `dist/index-CfdyELOP.js` là bundle build cũ/ignored; scan string không thấy `/not-found`, `/courses`, `/login`, `404`, `createRouter` hoặc `createWebHistory`. Không thể xác nhận hoặc build lại Study Web runtime từ các tài sản hiện có.
