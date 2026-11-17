# GS-04 — Đề cương khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `GS-04` |
| Module | Guest / Discovery |
| Route | `/courses/:courseId?tab=curriculum` — GS03Page owns the query tab; browser runtime chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `DD BLOCKED` — approved loaded curriculum layout/access policy is still absent and API #09 returns `content`/`video_url` without a preview/access contract. **Implementation status:** `PARTIAL SOURCE / IMPLEMENTATION BLOCKED` — GS03Page mounts the GS04 panel at `?tab=curriculum`, calls #09 after #08 succeeds and renders derived title/order states; visibility/access, cache and AC-05/F02 orchestration remain open. **Runtime status:** `RUNTIME NOT VERIFIED` — Angular tests/build pass; browser/live API/DB behavior is unverified. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [GS-04.md](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/GS-04.md), [GS-04_PLAN.md](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/GS-04_PLAN.md), [GS-04_markers.json](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/GS-04_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Hiển thị danh sách lesson public theo sort_order; item private không mở bằng guest.
- In-scope: Tái dùng #8 từ cache → GET #9; phân biệt empty curriculum và lỗi.
- Out-of-scope: Xem gate bên dưới; source wiring không đóng access/design gates hoặc chứng minh browser/live runtime.

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
| Current runtime | GS03Page + GS03 focused spec/build | `?tab=curriculum` mounts GS04 panel; #09 runs after #08 succeeds; focused spec 6/6 and build pass; browser/live runtime `NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [GS-04 source screen.png](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/screen_annotated.png))
- Luồng expected: tái dùng #8 từ cache → GET #9; current source direct-entry gọi #08 rồi lazy #09, không có client cache.
- Priority: P1; Gate/source status: **R (#09 source-backed locally)**; GS03 query-tab/#09 caller source-wired. **BLOCK:** visibility `PUBLISHED` chưa được API DD duyệt; response có content/video_url nhưng không preview/access field; legacy vs V1-PILOT schema/live DB chưa xác minh; cache/#08 reuse còn thiếu; AC-05 eager vs F02 lazy discrepancy chưa được duyệt.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-17 — T015: GS04 panel được mount trong GS03; tab query gọi #09 lazy sau #08. DD/access policy và browser/live runtime vẫn blocked/unverified.

## Trạng thái và ranh giới bằng chứng

# GS-04 — Đề cương khóa học

> **DD status:** `DD BLOCKED` — source hiện không có loaded curriculum layout và API #09 trả `content`/`video_url` công khai nhưng chưa có preview/access contract.
> **Implementation status:** `PARTIAL SOURCE / IMPLEMENTATION BLOCKED` — GS03Page owns the `?tab=curriculum` view and #09 caller; the panel renders derived title/order states only. Visibility/access, cache and orchestration approval remain open.
> **Runtime status:** `RUNTIME NOT VERIFIED` — Angular focused tests/build pass; browser and live API/DB behavior are not verified.
> **Phạm vi T015:** GS-04 is mounted as a GS03-owned panel; GS-05 remains unavailable.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | GS-04 — Đề cương khóa học (tab) |
| Mục tiêu expected | Guest xem danh sách bài học công khai của một khóa học theo `sort_order`; phân biệt curriculum rỗng với lỗi. Inventory nói Guest không được mở bài học private. |
| Actor | `Guest` theo AC-05. Header có liên kết đăng nhập/đăng ký tĩnh; không có actor/session logic trong HTML. |
| Route | `/courses/:courseId?tab=curriculum`; Guest route maps `/courses/:courseId` to GS03Page, which reads the query tab. Direct entry loads #08, then #09 after #08 succeeds. Keep `courseId` as a string; #09 backend validator enforces signed-int64 bounds. |
| API | #09 `GET /api/v1/courses/{course_id}/curriculum` (`SOURCE_BACKED` trong backend source hiện có; chưa xác minh deployed runtime/schema). #08 là prerequisite từ GS-03 theo inventory, nhưng cache contract chưa được định nghĩa. |
| Màn hình liên quan | GS-03 cung cấp `courseId`; ST-10 là Student lesson-access path. Không chuyển Guest sang #22–#24/ST-10 và không tạo Guest lesson-open flow nếu chưa có approved contract. |
| Data mutation | Không có. #09 là GET/read-only; HTML không lưu cache hay dữ liệu. |
| Điều kiện access | API source kiểm tra course `PUBLISHED` rồi chọn lesson `PUBLISHED`. API DD #09 vẫn ghi `PUBLISHED` là visibility assumption; trường `content`/`video_url` hiện vẫn có trong public response và model không có `preview/access` flag. Vì vậy không coi status này là bằng chứng Guest được phép xem nội dung/media. |

### Expected behavior và current behavior

| Expected từ inventory/flow | Current evidence trong checkout |
|---|---|
| Reuse #08 course detail từ cache rồi lấy #09; hiển thị các bài học public theo thứ tự. | `code.html` remains a static asset. Current Angular GS03Page validates the course via #08 then calls #09 for `tab=curriculum`; no client cache exists. Inventory does not define cache key, freshness or invalid-cache fallback. |
| Có loading, empty, ready và error riêng; curriculum rỗng không phải lỗi. | GS03 curriculum panel maps #09 into loading/empty/ready/not-found/error; the empty copy is currently derived and has no approved loaded-state design. |
| Path `courseId` tương ứng `course_id:int64`. | #09 route annotation là `str`; validator gọi shared `parse_integer` rồi enforce signed-int64 bounds. Source test có case hai biên hợp lệ và ngoài biên; client giữ ID dạng text. |
| Guest không mở bài học private. | Không có lesson item/click target. API #09 không trả preview/access field; current public response còn chứa `content` và `video_url`. Chưa thể thiết kế hành vi preview an toàn. |
| Breadcrumb/back về chi tiết cùng khóa học. | The source HTML anchors remain `href="#"`; in the current Angular UI, the Overview tab returns to GS03 detail without another request. |
| Tab behavior theo F02. | Current code follows lazy-by-tab after #08; AC-05 describes eager #08 → #09 → #10 before render. GS-04 row also says reuse #08 cache. These design discrepancies remain open. |
