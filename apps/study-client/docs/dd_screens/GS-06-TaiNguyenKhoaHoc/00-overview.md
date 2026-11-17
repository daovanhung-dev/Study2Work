# GS-06 — Tài nguyên khóa học · Tổng quan

> **T022 current-source update (2026-11-17):** GS03 now source-wires `?tab=resources` and mounts this screen only after API #08 confirms a published course. GS06 renders an accessible contract-blocked status and makes no #11/#12 request or resource action. This supersedes older statements that the Study Web tab/caller is absent. The resource-list/open flow remains DD BLOCKED; API #11/#12 DDs remain Draft; live API/DB and browser runtime are not established by source/tests.

| Trường | Giá trị |
|---|---|
| Screen ID | `GS-06` |
| Module | Guest / Discovery |
| Route | `/courses/:courseId?tab=resources` — GS03 query tab is source-wired; API/runtime availability remains separate |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: Source status is described in the source DD. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [GS-06.md](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/GS-06.md), [GS-06_PLAN.md](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/GS-06_PLAN.md), [GS-06_markers.json](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/GS-06_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Tài nguyên public theo khóa học; thể hiện quyền mở/tải theo metadata từ BE.
- In-scope: GET #11 → người dùng chọn id → GET #12 trước khi mở URL; không suy diễn visibility.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-06 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Tài nguyên public theo khóa học; thể hiện quyền mở/tải theo metadata từ BE. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #11, #12
- Liên kết màn hình dự kiến: [GS-07](../GS-07-XemTaiTaiNguyen/00-overview.md), [GS-03](../GS-03-ChiTietKhoaHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | empty/list/forbidden/expired-link |
| Current source | GS03 + GS06 | `?tab=resources` after #08 published-course response; accessible contract-blocked panel; no #11/#12 call |
| Deployed runtime | Worklog/context Study Web | `NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [GS-06 source screen.png](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/screen_annotated.png))
- Luồng: GET #11 → người dùng chọn id → GET #12 trước khi mở URL; không suy diễn visibility.
- Priority: P2; Gate/source status: **GS06 PARTIAL PRESENTATION SOURCE; #11/#12 API DD Draft; resource flow BLOCKED**. #11 route/module/query/tests exist locally but current view returns only `rows[0]` as a singleton, contrary to the DD rule not to select a representative row; collection/empty/order/pagination remains unresolved. `visibility` has no source. AC-06 public-or-authorized/403/private signed URL conflicts with #12 current public/no-auth/direct URL and conditional parent check; no 410/TTL/signer. Legacy DDL has `resources`, V1-PILOT does not; live schema/deployment is unknown. GS06 has no list/open UI and intentionally makes no resource API calls. Prototype differs from Study design target; WCAG/layout measurement remains incomplete.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# GS-06 — Tài nguyên khóa học (Tab)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID | `GS-06` |
| Tên | Tài nguyên khóa học (Tab) |
| Mục tiêu | Trình bày các tài nguyên thuộc khóa học; chỉ mở/tải sau khi resource ID, quyền truy cập và URL được backend xác nhận. |
| Actor | `Guest` theo inventory/AC-06. Việc học viên đã đăng ký truy cập tài nguyên private là yêu cầu trong AC-06 nhưng chưa có policy/API được chốt. |
| Route đề xuất | `/courses/:courseId?tab=resources` — route trong inventory, chưa có Study Web router để xác minh. |
| API dự kiến | #11 `GET /api/v1/courses/{course_id}/resources`; #12 `GET /api/v1/resources/{resource_id}`. |
| Màn hình liên quan | GS-03 cung cấp `courseId`; GS-07 nhận `resourceId`; ST-12 cũng dùng resource flow cho bài học. Header/footer destinations khác chưa được ánh xạ thành route. |
| Trạng thái | `DD BLOCKED` · `IMPLEMENTATION PARTIAL (gated presentation)` · `RESOURCE FLOW BLOCKED` · `LIVE RUNTIME NOT VERIFIED`. Các trạng thái được theo dõi riêng. |

### Tiền điều kiện và hậu điều kiện

- **Tiền điều kiện thiết kế:** GS-03 chuyển đúng `courseId`; course phải được xác nhận tồn tại và `PUBLISHED` trước khi public content được hiển thị. AC-06 yêu cầu resource là public hoặc người dùng có quyền truy cập, nhưng cơ chế đó chưa thống nhất với API catalog.
- **Hậu điều kiện mong muốn:** sau khi người dùng chọn một resource hợp lệ, hệ thống lấy metadata mới qua #12, hoàn tất kiểm tra quyền, rồi mới mở/tải URL được cho phép. Current #12 trả URL trực tiếp và không thực hiện kiểm tra resource visibility/enrollment hoặc ký URL.
- Không cache URL được coi là signed/temporary; current source không tạo signed URL và chưa có TTL contract. Cache/freshness của resource list cũng chưa được quy định.

### Expected behavior và current behavior

| Chủ đề | Expected theo inventory/AC/design | Current evidence |
|---|---|---|
| UI và route | Expected: tab resource trên course detail; list resource; chọn item sang GS-07; empty/list/forbidden/expired-link. | Current source: GS03 owns the `resources` query tab; after #08 success it mounts GS06, which shows only an accessible contract-blocked status. There is no list, empty claim, resource action or #11/#12 request. Browser/runtime verification is recorded separately. |
| API #11 | Public `GET /api/v1/courses/{course_id}/resources`, declared to return one `Resource`; collection use remains unresolved. | Route/module/query/model/test exist locally. Current query reads all linked rows ordered by ID; view returns 404 for no rows and maps only `rows[0]` to singleton `ResourceItem`. This is a source/DD cardinality discrepancy; `ApiEnvelope<Resource>` remains Draft and no visibility field exists. |
| API #12 | Public `GET /api/v1/resources/{resource_id}`; AC-06 muốn kiểm tra access và có thể ký URL private. | Current router/view/query/validator/model và test source có mặt; API DD #12 vẫn `Draft — Needs Confirmation` nhưng câu `RUNTIME_STATUS: DECLARED_NOT_RUNNABLE` trong DD đã lỗi thời so với route/source/test/report hiện tại. Route không yêu cầu Bearer; trả direct `resources.url`, bỏ `visibility`, không gọi storage signer. Chỉ kiểm tra parent lesson/course khi `lesson_id` khác `NULL`. |
| Schema resource | API #11/#12 cần dữ liệu resource và quan hệ lesson/course. | Legacy `infra/postgres/study-server/DB.sql` có bảng `resources` nhưng không có `visibility`; V1-PILOT `infra/postgres/02_study_db.sql` không khai báo bảng `resources`. Current API #12 query dùng tên bảng legacy. Live schema/deployment chưa xác minh. |
| Authorization | AC-06 cho phép public resource hoặc user có quyền; thiếu quyền → 403. | Catalog ghi Public/no Bearer và 404/500; API #12 source không kiểm tra visibility/enrollment và không có nhánh 403. Resource không có `lesson_id` được trả success mà không kiểm tra course cha. |
| Expiry | Prototype state card nêu signed URL hết hạn và 410. | Không có signed URL, TTL hoặc 410 trong catalog hay current #12 source. Đây là yêu cầu chưa có contract. |
| Thiết kế và accessibility | Study Web guide là đích giao diện và yêu cầu reflow, keyboard/focus, hit area, contrast, reduced motion. | Prototype dùng Plus Jakarta Sans, remote Google Fonts/Tailwind CDN, xanh cobalt và max-width 1440px; guide yêu cầu Inter/system, ocean tokens, không thêm remote font, content width khoảng 1120px. Ảnh desktop không chứng minh responsive/accessibility; claim WCAG trong card chưa được đo. |

### Quy tắc nghiệp vụ và bảo mật

1. Không tạo resource giả, tên file, kích thước, loại hoặc URL để lấp danh sách. Tên course, mã `FE-PRO-802`, tên đơn vị hướng dẫn và trạng thái v1 trong prototype không phải response API.
2. Không coi `ApiEnvelope<Resource>` là danh sách. Không tự đổi thành `{ items, total }`, `Page<Resource>` hoặc chọn một item đại diện.
3. Không tự suy ra `visibility` từ course status, URL hoặc `lesson_id`; checked-in DDL `resources` không có cột visibility và current response model cũng không trả field này.
4. Không tự mở/tải `data.url` với resource private trước khi backend access policy được chốt. Current API #12 public/direct URL flow không thỏa AC-06 private-access expectation.
5. 403, 410, signed URL TTL, Bearer forwarding/download gateway và nút “Yêu cầu tạo lại liên kết tải” xuất hiện trong AC/prototype nhưng chưa có current API contract. Không xử lý như runtime behavior.
6. `screen.png` và `code.html` là tài sản thiết kế. PNG gốc SHA-256 `b90795438d5369466bb101e8f6730265667f8ecc45c0d047d66495410da87dcd`; HTML gốc SHA-256 `6843e2cc0f01a24e1db8100b8fec49d88e1f3fe39859b102bb9828d4905a8c31`.
7. Không coi route source hoặc DDL artifact là bằng chứng production. API #12 hiện được compose locally; endpoint-level report trên branch tạm và fake-session test source không xác nhận production schema/deployment hay GS-06 browser flow.

### Đích thiết kế và kiểm tra tiếp cận

`.agents/web-study/design.md` là đích UI cho Study Web, không phải runtime contract. Khi chuyển prototype thành UI, cần đối chiếu lại palette `ocean-primary`, `page-background`, `text-primary`/`text-muted`, typography Inter/system, content width khoảng 1120px, reflow từ 320px, keyboard order/focus-visible, control hit area tối thiểu 44px và reduced-motion. HTML hiện tải font/CSS từ Google Fonts và Tailwind CDN, đặt content max-width 1440px và ẩn nav chính dưới breakpoint `md` mà không có mobile menu trong HTML. Không tuyên bố WCAG AA đạt chỉ từ dòng chữ trong prototype; chưa có contrast/layout/accessibility measurement.
