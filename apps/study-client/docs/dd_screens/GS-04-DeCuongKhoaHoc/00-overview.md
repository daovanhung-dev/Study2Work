# GS-04 — Đề cương khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `GS-04` |
| Module | Guest / Discovery |
| Route | `/courses/:courseId?tab=curriculum` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `DD BLOCKED` — source hiện không có loaded curriculum layout và API #09 trả `content`/`video_url` công khai nhưng chưa có preview/access contract.; **Implementation status:** `IMPLEMENTATION BLOCKED` — chưa có Study Web runtime; visibility/access, cache và orchestration còn mở.; **Runtime status:** `RUNTIME NOT VERIFIED` — Study Web được đăng ký `UNWIRED`; browser render dưới đây chỉ xác minh tài sản HTML tĩnh. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [GS-04.md](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/GS-04.md), [GS-04_PLAN.md](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/GS-04_PLAN.md), [GS-04_markers.json](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/GS-04_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Hiển thị danh sách lesson public theo sort_order; item private không mở bằng guest.
- In-scope: Tái dùng #8 từ cache → GET #9; phân biệt empty curriculum và lỗi.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-05 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Hiển thị danh sách lesson public theo sort_order; item private không mở bằng guest. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #09
- Liên kết màn hình dự kiến: [GS-03](../GS-03-ChiTietKhoaHoc/00-overview.md), [ST-10](../ST-10-KiemTraQuyenVaBatDauHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/ready/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [GS-04 source screen.png](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/screen_annotated.png))
- Luồng: Tái dùng #8 từ cache → GET #9; phân biệt empty curriculum và lỗi.
- Priority: P1; Gate/source status: **R (#09 source-backed locally)**; **BLOCK:** `course_id:int64` chưa khớp route string/parser range; visibility `PUBLISHED` chưa được API DD duyệt; response có content/video_url nhưng không preview/access field; legacy vs V1-PILOT schema/live DB chưa xác minh; cache/#08 reuse, AC-05 eager vs F02 lazy/direct-entry chưa chốt; Study Web UNWIRED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# GS-04 — Đề cương khóa học

> **DD status:** `DD BLOCKED` — source hiện không có loaded curriculum layout và API #09 trả `content`/`video_url` công khai nhưng chưa có preview/access contract.
> **Implementation status:** `IMPLEMENTATION BLOCKED` — chưa có Study Web runtime; visibility/access, cache và orchestration còn mở.
> **Runtime status:** `RUNTIME NOT VERIFIED` — Study Web được đăng ký `UNWIRED`; browser render dưới đây chỉ xác minh tài sản HTML tĩnh.
> **Phạm vi phiên:** chỉ GS-04; chưa xử lý GS-05.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | GS-04 — Đề cương khóa học (tab) |
| Mục tiêu expected | Guest xem danh sách bài học công khai của một khóa học theo `sort_order`; phân biệt curriculum rỗng với lỗi. Inventory nói Guest không được mở bài học private. |
| Actor | `Guest` theo AC-05. Header có liên kết đăng nhập/đăng ký tĩnh; không có actor/session logic trong HTML. |
| Route đề xuất | `/courses/:courseId?tab=curriculum` theo `apps/study-client/docs/list_screen.md`; chưa được Study Web router thực thi. Giữ cùng `courseId` từ GS-03; API catalog khai báo `course_id:int64`, trong khi current #09 route nhận `str` và validator không enforce signed int64/positive range. |
| API | #09 `GET /api/v1/courses/{course_id}/curriculum` (`SOURCE_BACKED` trong backend source hiện có; chưa xác minh deployed runtime/schema). #08 là prerequisite từ GS-03 theo inventory, nhưng cache contract chưa được định nghĩa. |
| Màn hình liên quan | GS-03 cung cấp `courseId`; ST-10 là Student lesson-access path. Không chuyển Guest sang #22–#24/ST-10 và không tạo Guest lesson-open flow nếu chưa có approved contract. |
| Data mutation | Không có. #09 là GET/read-only; HTML không lưu cache hay dữ liệu. |
| Điều kiện access | API source kiểm tra course `PUBLISHED` rồi chọn lesson `PUBLISHED`. API DD #09 vẫn ghi `PUBLISHED` là visibility assumption; trường `content`/`video_url` hiện vẫn có trong public response và model không có `preview/access` flag. Vì vậy không coi status này là bằng chứng Guest được phép xem nội dung/media. |

### Expected behavior và current behavior

| Expected từ inventory/flow | Current evidence trong checkout |
|---|---|
| Reuse #08 course detail từ cache rồi lấy #09; hiển thị các bài học public theo thứ tự. | Không có route parser, cache, API call, lesson list hoặc handler trong `code.html`. Inventory không định nghĩa cache key, freshness, miss/invalid-cache fallback. |
| Có loading, empty, ready và error riêng; curriculum rỗng không phải lỗi. | Tài sản HTML chỉ có một card tĩnh với copy “Chưa có nội dung đề cương để hiển thị.”; không gắn state này với response #09. |
| Path `courseId` tương ứng `course_id:int64`. | #09 route annotation là `str`; shared `parse_integer` kiểm tra cú pháp integer nhưng không enforce signed int64/positive range. Boundary behavior chưa được test/runtime xác minh. |
| Guest không mở bài học private. | Không có lesson item/click target. API #09 không trả preview/access field; current public response còn chứa `content` và `video_url`. Chưa thể thiết kế hành vi preview an toàn. |
| Breadcrumb/back về chi tiết cùng khóa học. | Breadcrumb “Chi tiết khóa học” và CTA quay lại đều có `href="#"`; không mang `courseId`. |
| Tab behavior theo F02. | F02 nói #09 tải lazy khi chọn tab; AC-05 mô tả chuỗi eager #08 → #09 → #10 trước render. GS-04 row lại nói reuse #08 cache rồi #09. Chưa có implementation để xác định lựa chọn. |
