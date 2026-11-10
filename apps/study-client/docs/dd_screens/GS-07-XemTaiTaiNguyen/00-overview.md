# GS-07 — Xem/tải tài nguyên · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `GS-07` |
| Module | Guest / Discovery |
| Route | `/resources/:resourceId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: Source status is described in the source DD. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [GS-07.md](../../screen_stitch/02_guest_discovery/GS-07_xem-tai-tai-nguyen/GS-07.md), [GS-07_PLAN.md](../../screen_stitch/02_guest_discovery/GS-07_xem-tai-tai-nguyen/GS-07_PLAN.md), [GS-07_markers.json](../../screen_stitch/02_guest_discovery/GS-07_xem-tai-tai-nguyen/GS-07_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Preview metadata/media hỗ trợ; fallback download khi URL hợp lệ và được phép.
- In-scope: GET #12 tại thời điểm mở; không cache signed URL vô hạn hoặc lộ internal storage key.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-06 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Preview metadata/media hỗ trợ; fallback download khi URL hợp lệ và được phép. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #12
- Liên kết màn hình dự kiến: [GS-06](../GS-06-TaiNguyenKhoaHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/ready/403-unclear/404/link-expired |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [GS-07 source screen.png](../../screen_stitch/02_guest_discovery/GS-07_xem-tai-tai-nguyen/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/02_guest_discovery/GS-07_xem-tai-tai-nguyen/screen_annotated.png))
- Luồng: GET #12 tại thời điểm mở; không cache signed URL vô hạn hoặc lộ internal storage key.
- Priority: P2; Gate/source status: **R (#12 source-backed locally; API DD Draft)**; **BLOCK:** current public/no-auth direct URL lacks AC-06 access check/signer; preview/MIME/URL policy, 403/404/expiry mapping, GS-06/ST-12 return context and Study Web route UNWIRED; live schema unknown; prototype differs from Study design guide and WCAG unmeasured

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# GS-07 — Xem/tải tài nguyên (Trang)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID | `GS-07` |
| Mục tiêu | Hiển thị metadata tài nguyên đã được phép truy cập; preview PDF/media nếu loại tài nguyên hỗ trợ, nếu không thì tải khi URL và quyền hợp lệ. |
| Actor | Guest theo inventory/AC-06; AC-06 cũng cho phép người dùng có quyền truy cập resource private. Chính sách quyền cụ thể chưa được thống nhất. |
| Route đề xuất | `/resources/:resourceId` — route client trong inventory; chưa có Study Web source/router để xác minh. |
| API tham chiếu | #12 `GET /api/v1/resources/{resource_id}`. |
| Màn hình liên quan | GS-06 chuyển `resourceId`; ST-12 có thể mở resource trong ngữ cảnh `lessonId`; quay lại GS-06 là ý định trên mockup, chưa có route/state handoff. SH-06 là màn hình 404 generic; việc dùng cho #12 chưa được chốt. |
| Trạng thái | `DD BLOCKED` · `IMPLEMENTATION BLOCKED` · `RUNTIME NOT VERIFIED`. Đây là ba trạng thái độc lập. |

### Tiền điều kiện và hậu điều kiện

- **Tiền điều kiện mong muốn:** nhận `resourceId` hợp lệ từ GS-06 hoặc ST-12; tải metadata bằng #12; hoàn tất policy public/private và quyền truy cập trước khi mở hoặc tải URL.
- **Hậu điều kiện mong muốn:** resource được preview nếu loại/URL được hỗ trợ; nếu không, cho tải khi được phép. Không hiển thị bucket nội bộ, metadata nhạy cảm hoặc URL chưa được cấp quyền.
- **Giới hạn hiện tại:** #12 trả URL trực tiếp từ `resources.url`, không kiểm tra visibility/enrollment và không ký URL. Không tự mở URL hoặc tuyên bố private-resource access an toàn khi AC-06 và source chưa khớp.
- Không có quy tắc cache, retry, MIME allowlist, expiry, URL origin allowlist hoặc preview/download policy đã được xác nhận.

### Expected behavior và current behavior

| Chủ đề | Expected theo inventory/AC-06 | Current evidence |
|---|---|---|
| Mở màn hình | Route `/resources/:resourceId`; nhận ID từ GS-06, có thể từ ST-12; lấy metadata. | Study Web không có app source/router/API client trong checkout. `code.html` là prototype tĩnh, hiển thị chuỗi `:resourceId` và không gửi request. `UNWIRED`. |
| API #12 | Catalog: public GET, no Bearer, `int64` path, `ApiEnvelope<Resource>`, 200/404/500. AC-06 yêu cầu resource public hoặc user có quyền; thiếu quyền có nhánh 403 và private file cần signed URL qua Object Storage. | Route hiện tại được register, không có auth dependency; query lấy direct `resources.url`; model trả `id/name/type/url/lesson_id`; không visibility, enrollment/access check hoặc signer. |
| API DD status | API DD #12 là `Draft — Needs Confirmation`; internal `RUNTIME_STATUS` ghi `DECLARED_NOT_RUNNABLE`. | Local `v1.py` compose route #12 và test source tồn tại, nên nhãn runtime trong API DD không khớp current local source composition. Đây chưa phải production/deployment/runtime verification. |
| Trạng thái | Loading, ready, 403-unclear, 404 và expired-link trong inventory; preview khi hỗ trợ, fallback download. | 6 state tab chỉ thay nội dung mô tả/code sample bằng JavaScript local; toolbar/download vẫn disabled, không có viewer hay request. API hiện chỉ xác nhận 200/404/500. |
| API card / URL | Contract đúng phải theo catalog và API source. | Mock card dùng path không có `/api/v1`, host mẫu và `Authorization: Bearer`; ready sample mô tả `signed_url`/`expires_in`. Đây là prototype-only và khác catalog/source. |
| Navigation | GS-06 là return destination; ST-12 entry context có thể gồm `lessonId`. | Back/breadcrumb/header/footer anchors dùng `href="#"` và `data-path` metadata; chưa có điều hướng hoặc giữ origin/context. |
| Design/accessibility | `.agents/web-study/design.md` là target: Inter/system, ocean tokens, no remote font, ~1120px content width, responsive reflow, focus-visible/reduced-motion, target ≥44px. | Prototype tải Google Fonts/Tailwind CDN, dùng Plus Jakarta Sans và cobalt `#004ac6/#2563eb`, max-width 1440px; nav chính ẩn dưới `md` không có menu mobile, zoom controls 32×32 và status badge `animate-pulse`. Contrast/reflow/WCAG chưa được đo. |

### Quy tắc nghiệp vụ và bảo mật

1. `resourceId` là identifier; không suy ra tên file, MIME, kích thước, URL hoặc quyền từ ID.
2. API #12 `200` hiện không chứng minh người gọi có quyền mở resource private. Không tự hiển thị/mở/tải `data.url` cho private resource cho tới khi policy được thống nhất và thực thi.
3. Không coi `resources.url` là signed URL. Current response không có `signed_url` hoặc `expires_in`; không tạo TTL, refresh hoặc retry flow bằng suy đoán.
4. Không dùng mock code/status `403`, `410`, `423`, `501`, `AUTH_RESOURCE_UNAUTHORIZED` hoặc `RESOURCE_NOT_FOUND` làm runtime mapping. #12 hiện có 404 `DESIGN_RESOURCE_NOT_FOUND` và 500 `DESIGN_INTERNAL_ERROR` ngoài success.
5. Không gắn nhãn preview được hỗ trợ chỉ từ `resource_type`; enum, MIME mapping và URL/content safety policy chưa được chốt. Không dùng `<iframe>`, `<video>` hoặc download link theo đoán.
6. Source `screen.png` và `code.html` được giữ nguyên; chúng là design hand-off, không phải runtime evidence.
