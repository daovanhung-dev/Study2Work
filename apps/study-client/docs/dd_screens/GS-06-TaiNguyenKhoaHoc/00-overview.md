# GS-06 — Tài nguyên khóa học · Tổng quan

> **T041/current-source update (2026-11-20):** GS-03 mounts GS-06 after #08 confirms a published course. GS-06 calls #11, validates the PUBLIC `Resource[]` projection/IDs, and renders loading/error/retry/empty/list states. Selecting a row opens GS-07 with the resource ID and course return context. T041 approves #11 collection semantics (ID ascending; valid empty course returns `200 []`) and PUBLIC/PRIVATE visibility. GS-07 calls #12; PRIVATE resources require Student auth, ACTIVE enrollment and a 300-second signed URL. These are local-source claims only; live schema/API/runtime is unverified. No Study writer for `resources` is found (#47 writes `lesson_uploads`), so populated data availability remains open. This note supersedes the historical T022 gate-only statements below.

| Trường | Giá trị |
|---|---|
| Screen ID | `GS-06` |
| Module | Guest / Discovery |
| Route | `/courses/:courseId?tab=resources` — GS03 query tab is source-wired; API/runtime availability remains separate |
| Actor/role | Guest for public resource collection; Student auth is used by #12 for PRIVATE resource access |
| DD status | Draft package; T041 approved resource access decisions; implementation partial; runtime not verified. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [GS-06.md](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/GS-06.md), [GS-06_PLAN.md](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/GS-06_PLAN.md), [GS-06_markers.json](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/GS-06_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Tài nguyên public theo khóa học; open a resource only after #12 confirms metadata, URL and access.
- In-scope: #11 public collection → chọn ID → #12 metadata/access check → expose validated HTTP(S) URL.
- Private access: Student Bearer + published parent course + ACTIVE enrollment; signed URL TTL 300 seconds.
- Remaining gaps: preview/MIME-specific UI, resource producer/schema availability and live runtime verification.

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
| Current source | GS03 + GS06 | `?tab=resources` after #08 published-course response; #11 PUBLIC collection loading/error/retry/empty/list; GS-07 handoff |
| Deployed runtime | Worklog/context Study Web | `NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [GS-06 source screen.png](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/screen_annotated.png))
- Luồng: #11 → select resource → #12; PUBLIC opens direct valid HTTP(S), PRIVATE uses server-signed URL only after enrollment check.
- Priority: P2; **PARTIAL IMPLEMENTATION / RUNTIME NOT VERIFIED**. T041 approves visibility/access and #11 collection behavior; source uses #11/#12. No `resources` writer was found; #47 writes `lesson_uploads`; legacy/V1-PILOT schemas and live DB differ/are unverified. GS-06 layout only partially matches Stitch; GS-07 does not implement MIME-specific preview/expiry UI; responsive/accessibility measurement remains incomplete.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-20 — Reconciled GS-06 current source and T041-approved resource policy; #11 list and GS-07 handoff are wired; resource producer/runtime and preview gaps remain.

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

- **Tiền điều kiện:** GS-03 has a validated course route and #08 confirms PUBLISHED before #11.
- **Hậu điều kiện:** after selection, #12 confirms resource metadata and access. PUBLIC receives a validated direct URL; PRIVATE receives a signed URL after Student ACTIVE-enrollment checks.
- Signed URLs have a 300-second TTL; this client does not persist them or implement expiry renewal. Resource-list cache/freshness remains unspecified.

### Expected behavior và current behavior

| Chủ đề | Expected theo inventory/AC/design | Current evidence |
|---|---|---|
| UI và route | Expected: resource tab, list, selection and contextual return. | Current source mounts GS-06 after published #08; #11 drives loading/error/retry/empty/list; selection routes to GS-07. Runtime is unverified. |
| API #11 | T041-approved public `Resource[]`, ordered by ID; valid empty is `200 []`. | Current query filters PUBLIC rows from published lessons/courses and maps full visibility projection. |
| API #12 | PUBLIC direct URL or PRIVATE signed URL after authorization. | Current #12 applies Student/ACTIVE-enrollment/published-parent checks for PRIVATE and signs for 300 seconds; PUBLIC URL must be valid HTTP(S). |
| Schema resource | API #11/#12 cần dữ liệu resource và quan hệ lesson/course. | Legacy `infra/postgres/study-server/DB.sql` có bảng `resources` nhưng không có `visibility`; V1-PILOT `infra/postgres/02_study_db.sql` không khai báo bảng `resources`. Current API #12 query dùng tên bảng legacy. Live schema/deployment chưa xác minh. |
| Authorization | T041 approves PUBLIC/PRIVATE; PRIVATE requires Student auth and ACTIVE enrollment on a published parent course. | Current #12 enforces the access rule; unauthenticated/invalid token, no enrollment and invalid resource map to 401/403/404. |
| Expiry | PRIVATE signed URL TTL is 300 seconds. | Server signer requests 300 seconds; no 410 or automatic renewal UI exists. |
| Thiết kế và accessibility | Study Web guide là đích giao diện và yêu cầu reflow, keyboard/focus, hit area, contrast, reduced motion. | Prototype dùng Plus Jakarta Sans, remote Google Fonts/Tailwind CDN, xanh cobalt và max-width 1440px; guide yêu cầu Inter/system, ocean tokens, không thêm remote font, content width khoảng 1120px. Ảnh desktop không chứng minh responsive/accessibility; claim WCAG trong card chưa được đo. |

### Quy tắc nghiệp vụ và bảo mật

1. Không tạo resource giả, tên file, kích thước, loại hoặc URL để lấp danh sách. Tên course, mã `FE-PRO-802`, tên đơn vị hướng dẫn và trạng thái v1 trong prototype không phải response API.
2. #11 is `Resource[]`; do not map it to singleton/Page or synthesize fields.
3. Use backend-provided `visibility`; do not infer it from course status, URL or `lesson_id`.
4. Expose a PRIVATE URL only after #12 succeeds; private access requires Student ACTIVE enrollment and server signing.
5. Do not invent 410, automatic URL renewal, MIME preview, download gateway or re-sign controls; the current client does not implement those behaviors.
6. `screen.png` và `code.html` là tài sản thiết kế. PNG gốc SHA-256 `b90795438d5369466bb101e8f6730265667f8ecc45c0d047d66495410da87dcd`; HTML gốc SHA-256 `6843e2cc0f01a24e1db8100b8fec49d88e1f3fe39859b102bb9828d4905a8c31`.
7. Không coi route source hoặc DDL artifact là bằng chứng production. API #12 hiện được compose locally; endpoint-level report trên branch tạm và fake-session test source không xác nhận production schema/deployment hay GS-06 browser flow.

### Đích thiết kế và kiểm tra tiếp cận

`.agents/web-study/design.md` là đích UI cho Study Web, không phải runtime contract. Khi chuyển prototype thành UI, cần đối chiếu lại palette `ocean-primary`, `page-background`, `text-primary`/`text-muted`, typography Inter/system, content width khoảng 1120px, reflow từ 320px, keyboard order/focus-visible, control hit area tối thiểu 44px và reduced-motion. HTML hiện tải font/CSS từ Google Fonts và Tailwind CDN, đặt content max-width 1440px và ẩn nav chính dưới breakpoint `md` mà không có mobile menu trong HTML. Không tuyên bố WCAG AA đạt chỉ từ dòng chữ trong prototype; chưa có contrast/layout/accessibility measurement.
