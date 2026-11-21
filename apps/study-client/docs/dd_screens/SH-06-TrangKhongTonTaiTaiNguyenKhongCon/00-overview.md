# SH-06 — Trang không tồn tại / tài nguyên không còn · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `SH-06` |
| Module | Shared / Auth / System |
| Route | `/not-found` — explicit route được đăng ký trong Angular source; runtime chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | SH-06 hoàn thiện 100% theo rubric tĩnh UI/UX/logic/API trong phạm vi generic 404 với `/courses` và `/`; #08 404/500 are distinguished; focused tests pass; browser/static-host runtime is not verified. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.2 / 2026-11-21 |
| Nguồn đối chiếu | [SH-06.md](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/SH-06.md), [SH-06_PLAN.md](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/SH-06_PLAN.md), [SH-06_markers.json](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/SH-06_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Thông báo trang/tài nguyên không tồn tại, không tiết lộ tài nguyên riêng tư, và đưa người dùng về nơi an toàn.
- In-scope: Generic route 404 and API #08 resource 404; real links `/courses` and `/`; preserve API #08 500 as a service error.
- Out-of-scope: Unsupported recommendation/contact/footer, personalized suggestions and static-host or production HTTP behavior.

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
| Current source | `shared.route.ts`, `SH06/pages/` | Explicit `/not-found`, unknown-route wildcard and #08 detail-404 handoffs are wired |
| Runtime | Worklog/context Study Web | `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [SH-06 source screen.png](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/screen_annotated.png))
- Luồng: Router 404 hoặc resource 404 chuyển state; không chuyển 500 thành 404.
- Priority: P0; route handoff and navigation are source-wired; runtime not verified.

## 7. Reconciliation and implementation evidence — 2026-11-21

- Product scope is the intentionally minimal page with working `/courses` and `/` links. Unsupported prototype recommendation, contact and footer content are not part of the approved implementation.
- API #08 source returns 404 for missing/unpublished courses and 500 for internal failure; it has no 403 response. Access-denied handling stays on SH-05.
- SH-06 static implementation is complete under the repository's UI/UX/logic/API rubric. Focused test covers the real navigation links; browser/static-host behavior remains unverified.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# Tài liệu thiết kế chi tiết màn hình — SH-06 Không tìm thấy trang / tài nguyên

> **Mã màn hình:** SH-06 · **Loại:** state view · **Tác nhân:** khách hoặc người dùng truy cập route/tài nguyên không khả dụng
> **Route:** `/not-found` · **AC:** AC-05 · **API catalog:** #08 · **Route liên quan:** GS-01, SH-01
> **Trạng thái:** approved minimal 404 scope; explicit route, wildcard and #08 detail-404 handoffs are source-wired · **Runtime:** `NOT VERIFIED`.

## Trích đoạn tổng quan từ DD nguồn

> The source DD excerpts below are historical design evidence. The approved 2026-11-21 scope uses only the two working links and the #08 404/500 distinction documented above.

### Trích từ DD nguồn: 1. Tổng quan màn hình

SH-06 hiển thị một state 404 chung cho hai trường hợp: router không tìm thấy route (`ROUTE_404`) hoặc API #08 không tìm thấy khóa học đã publish (`RESOURCE_404`). Nội dung không phân biệt khóa học không tồn tại với khóa học chưa được publish, nhờ đó không tiết lộ draft/private. Lỗi dịch vụ, lỗi mạng hoặc quyền truy cập không được đổi thành 404.

| Thuộc tính | Đặc tả |
|---|---|
| Mục tiêu | Giải thích rằng route/tài nguyên không khả dụng và đưa người dùng tới nơi công khai tiếp theo. |
| Actor/Role | Khách hoặc người dùng bất kỳ. API #08 là public, không yêu cầu Bearer token. |
| Route | `/not-found` được đăng ký tường minh trong Shared route group; không có wildcard. GS-03/#08 404 hiện hiển thị inline, chưa chuyển sang SH-06. |
| API | API #08 `GET /api/v1/courses/{course_id}` khi flow từ course detail. SH-06 không tự gọi #08 khi mở route lỗi. Trạng thái được ghi khác nhau: dòng SH-06 trong inventory ghi BE `D`, API index §5 ghi #008 `R`, API contract tổng thể đã được duyệt nhưng chưa runtime-verified, còn API DD #08 ghi `Draft — Needs Confirmation`; route/module/test source hiện có. |
| Điều kiện trước | Direct route: router xác định path không khớp. Resource: request #08 từ flow GS-03 nhận HTTP 404 `DESIGN_RESOURCE_NOT_FOUND`. Không lấy 500/mạng làm điều kiện mở SH-06. |
| Điều kiện sau | Người dùng có thể tới GS-01 `/courses` hoặc SH-01 `/`. 200 từ #08 ở flow course detail phải tiếp tục GS-03; 403 đi theo state access-denied (SH-05); 500/mạng ở service-error state riêng. |
| Liên kết màn hình | [GS-01 prototype](../../screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/code.html), [SH-01 DD](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01.md). GS-01 là target route nhưng chưa có DD trong checkout. |
| Trạng thái triển khai | `screen.png` và `code.html` là tài sản design-only. Shared SH-06 explicit page/route đã wire; không có wildcard hoặc #08-to-SH-06 handoff. Current `/` là SH-01 và `/courses` là GS-01 theo route source. Runtime chưa xác minh. |

### 1.1 Expected behavior và current behavior

| Hạng mục | Expected behavior theo inventory/AC/API design | Current source evidence |
|---|---|---|
| Route 404 | Route `/not-found`; cung cấp link tới GS-01 và SH-01. | Shared route table registers `/not-found`; the page links to source-backed `/courses` and `/`. No wildcard or static-host fallback is established. |
| Resource 404 | API #08 404 không tiết lộ draft/private; route hoặc resource 404 dẫn tới SH-06. | API #08 current source trả 404 `DESIGN_RESOURCE_NOT_FOUND` cho invalid/missing/unpublished. GS-03 API #08 detail 404 now navigates to SH-06 without forwarding the course ID or response body. |
| API #08 status/shape | API contract khai báo `ApiEnvelope<Page<Course>>`, 200/404/500; API DD #08 còn ở trạng thái draft. Dòng SH-06 ghi BE `D`, trong khi API index §5 ghi #008 `R`. | `app/api/v1.py`, module #08 và test source đều có. Current success envelope có `data: Page<Course>` singleton. Đây là sai khác giữa các nhãn trạng thái và source hiện hành; source không chứng minh deployment/runtime. |
| 403 | AC-05 diagram thể hiện nhánh `404/403` khi course không tồn tại/PUBLISHED; API catalog chỉ liệt kê 404/500. | #08 hiện public, không có 403 branch. Invalid/missing/unpublished là 404; query/mapping error là 500. Cần owner xác nhận/sửa AC; nếu guard khác thật sự trả 403, giữ riêng theo access-denied flow. |
| Service error | 500/mạng không bị biến thành 404. | Module #08 trả 500 `DESIGN_INTERNAL_ERROR` khi query/mapping lỗi. Inventory global yêu cầu service error riêng; current Study Web routes have no shared service-error screen. |
| Khóa học gợi ý | Cần quyết định giữ/bỏ section và xác nhận nguồn, schema, ID, copy, thứ tự; không render dữ liệu giả. | HTML có ba card viết cứng, không có course ID/API mapping. API #06 có trong catalog nhưng chưa là dependency SH-06 và không quy định recommendation semantics. `BLOCKER`. |
| Support/footer | Cần quyết định giữ/bỏ từng control và xác nhận route/contact/legal copy trước khi ship. | Contact CTA và 4 footer links dùng `href="#"`; chứng chỉ, quy chế và hỗ trợ chưa có route/channel contract tại SH-06. `BLOCKER`. |

`code.html` là prototype. Giá trị course, category, duration, learner count, copy hợp tác doanh nghiệp, copyright year và đường dẫn `#` không phải dữ liệu/business contract. `dist/index-CfdyELOP.js` là bundle build cũ/ignored; scan string đó chỉ mô tả bundle lịch sử, không phải current source hay runtime evidence.

### 1.2 Current source implementation audit (2026-11-17)

- `shared.route.ts` registers the explicit `not-found` path and loads `SH06Page`; the page renders a generic 404 with internal links to `/courses` (GS-01) and `/` (SH-01). It does not echo the requested URL, course ID, API body, or private status and does not call an API.
- The root wildcard now redirects unknown routes to `/not-found` while clearing the original path/query. GS-03 API #08 detail 404 now navigates to SH-06 with `replaceUrl`; the course ID and error body are not forwarded. API #08 500/service/network errors and the GS-03 #09 curriculum 404 remain separate.
- Recommendation cards, contact/support and footer/legal surfaces remain omitted because their content and destinations are unresolved. AC-05's 403 branch remains inconsistent with API #08's source-backed 404/500 behavior.
- This is source evidence only. Focused route/GS-03 tests pass; full-suite/build/browser, deployment, live API and live DB verification are recorded separately in T024.
