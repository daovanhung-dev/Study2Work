# ME-07 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ME-07_markers.json](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ME-07-EL-001` | `ME07-EL-01` | Logo Study2Work LMS Mentor |
| #2 | `ME-07-EL-002` | `ME07-EL-02` | Điều hướng Mentor toàn cục |
| #3 | `ME-07-EL-003` | `ME07-EL-03` | Thông báo Mentor |
| #4 | `ME-07-EL-004` | `ME07-EL-04` | Danh tính và vai trò Mentor |
| #5 | `ME-07-EL-005` | `ME07-EL-05` | Breadcrumb course và biên tập nội dung |
| #6 | `ME-07-EL-006` | `ME07-EL-06` | Icon và nhãn Hệ thống phân phối giáo trình số |
| #7 | `ME-07-EL-007` | `ME07-EL-07` | Tiêu đề Tạo và chỉnh sửa nội dung bài giảng |
| #8 | `ME-07-EL-008` | `ME07-EL-08` | Chế độ kiểm duyệt khóa học |
| #9 | `ME-07-EL-009` | `ME07-EL-09` | Trường Tiêu đề nội dung |
| #10 | `ME-07-EL-010` | `ME07-EL-10` | Select Loại nội dung |
| #11 | `ME-07-EL-011` | `ME07-EL-11` | Input Thứ tự hiển thị |
| #12 | `ME-07-EL-012` | `ME07-EL-12` | Nhãn Nội dung chi tiết và trạng thái đồng bộ |
| #13 | `ME-07-EL-013` | `ME07-EL-13` | Placeholder trình soạn thảo chuyên sâu |
| #14 | `ME-07-EL-014` | `ME07-EL-14` | Thông báo khóa nhập tài nguyên đa phương tiện |
| #15 | `ME-07-EL-015` | `ME07-EL-15` | Hủy thay đổi |
| #16 | `ME-07-EL-016` | `ME07-EL-16` | Nút Lưu bản nháp đang disabled |
| #17 | `ME-07-EL-017` | `ME07-EL-17` | Tiêu đề panel Quy chuẩn dữ liệu |
| #18 | `ME-07-EL-018` | `ME07-EL-18` | Ghi chú Bảo mật hệ thống |
| #19 | `ME-07-EL-019` | `ME07-EL-19` | Hướng dẫn tiêu đề nội dung |
| #20 | `ME-07-EL-020` | `ME07-EL-20` | Hướng dẫn loại tài nguyên |
| #21 | `ME-07-EL-021` | `ME07-EL-21` | Hướng dẫn thứ tự hiển thị |
| #22 | `ME-07-EL-022` | `ME07-EL-22` | Tiêu đề panel Trạng thái xác thực phiên |
| #23 | `ME-07-EL-023` | `ME07-EL-23` | Badge trạng thái Đang đối soát |
| #24 | `ME-07-EL-024` | `ME07-EL-24` | Thanh tiến độ xác thực phiên |
| #25 | `ME-07-EL-025` | `ME07-EL-25` | Mô tả quyền lưu và đối soát |
| #26 | `ME-07-EL-026` | `ME07-EL-26` | Ảnh minh họa không gian làm việc |
| #27 | `ME-07-EL-027` | `ME07-EL-27` | Caption Không gian sư phạm |
| #28 | `ME-07-EL-028` | `ME07-EL-28` | Footer brand và thông tin bản quyền |
| #29 | `ME-07-EL-029` | `ME07-EL-29` | Footer Quy chế Giảng viên |
| #30 | `ME-07-EL-030` | `ME07-EL-30` | Footer Tiêu chuẩn đánh giá |
| #31 | `ME-07-EL-031` | `ME07-EL-31` | Footer Hỗ trợ kỹ thuật |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 4. Element specification — 31 markers

Source coordinates and labels are in [ME-07_markers.json](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07_markers.json); every marker below maps one-to-one with the JSON, SVG and annotated image.

| # / Element ID | Name, type, position | Data, visibility, validation | Event/output |
|---:|---|---|---|
| 1 `ME07-EL-01` | Study2Work LMS Mentor logo/link; header left | Static brand; anchor `href="#"`. | EV-10; destination not wired. |
| 2 `ME07-EL-02` | Primary Mentor navigation group; header | Tổng quan, Khóa học phụ trách, Chấm bài, Hộp thư hỗ trợ, Thông báo; all destinations `#`. | EV-10; no route source. |
| 3 `ME07-EL-03` | Notification icon/link | Static icon/red dot; `href="#"`; no unread API/count. | EV-10. |
| 4 `ME07-EL-04` | Mentor name/role/avatar | “TS. Vũ Thành Đạt” and role are mockup text; no profile API in #49–#51. | No event handler; account menu is not present. |
| 5 `ME07-EL-05` | Breadcrumb: course list → course detail → content manager → current editor | All earlier segments are anchors `#`; course ID/name is not in #49 Content response. | EV-10; exact route/return context open. |
| 6 `ME07-EL-06` | Icon + “Hệ thống phân phối giáo trình số” kicker | Static page branding; no server field. | None. |
| 7 `ME07-EL-07` | H1 “Tạo và chỉnh sửa nội dung bài giảng” | Static title shared by create/edit screenshot; does not identify route mode. | Mode comes from route proposal, not this text. |
| 8 `ME07-EL-08` | “Chế độ kiểm duyệt: Khóa học chuẩn hóa” badge | Not returned by #49–#51; approved course moderation mode source not found in this flow. | Static only; do not gate API by badge. |
| 9 `ME07-EL-09` | Title text input `content_title` | Placeholder “Nhập tiêu đề phần hoặc bài học...”; screenshot marks required. HTML input has no `required`, max length, default or error text. API requires string but accepts no defined nonempty/length rules. | EV-03; dirty + candidate required validation; exact trim/length unresolved. |
| 10 `ME07-EL-10` | Content type select `content_type` | Placeholder + values `theory`, `reading`, `practice`; visual required mark but no `required` attr. API accepts an open string; enum/schema unconfirmed. | EV-04; not ready to submit as canonical type. |
| 11 `ME07-EL-11` | Number input `sort_order` | HTML `min=1`, no explicit step/max/required; label says positive integer. #49 maps `content_order` to int32 `order`; #50 generates root order from 0 and #51 preserves order. | EV-05; unsaved/incompatible field; block editing until API/UX decision. |
| 12 `ME07-EL-12` | “Nội dung chi tiết” label + “Đang chờ kết nối giao thức” state | Label is plain text, not associated with an editor control. Sync status is hardcoded; no sync endpoint. | EV-06; placeholder only. |
| 13 `ME07-EL-13` | Rich editor panel placeholder | Static icon/title/help text says editor formats are being aligned; no textarea/editor/input, payload serialization or autosave source. | No current input event; #50/#51 payload object remains blocked. |
| 14 `ME07-EL-14` | Locked multi-media entry note | Static lock icon/text; no upload widget, asset API or rule in ME-07 inventory. | No event; do not activate upload behavior here. |
| 15 `ME07-EL-15` | “Hủy thay đổi” anchor | `href="#"`; no dirty guard, destination or undo semantics. | EV-09; target ME-06 is a candidate, requires approved route/unsaved confirmation. |
| 16 `ME07-EL-16` | “Lưu bản nháp” button | `disabled` and `aria-disabled="true"` in HTML; title says permission validation in progress. No form/submit handler. | EV-07/EV-08 when enabled only after contract; current state is disabled. |
| 17 `ME07-EL-17` | “Quy chuẩn dữ liệu” side panel heading | Static section heading; not an API response. | None. |
| 18 `ME07-EL-18` | “Bảo mật hệ thống” callout | Copy claims save is limited to a properly authorized lecturer; #50/#51 use direct course owner. Copy is not authorization evidence. | Read-only note. |
| 19 `ME07-EL-19` | Title guideline row | Static suggestion to use a concise title; not a length rule or server validator. | None. |
| 20 `ME07-EL-20` | Resource-type guideline row | Static copy asks for matching resource type; no link between content type and payload is defined. | None. |
| 21 `ME07-EL-21` | Order guideline row | Static copy says order controls tree placement; current mutation endpoints do not accept/change it. | None; discrepancy with #50/#51. |
| 22 `ME07-EL-22` | Session-validation panel heading | Static “Trạng thái xác thực phiên”; no client session-validation source is present. | None. |
| 23 `ME07-EL-23` | “Đang đối soát” status badge | Hardcoded state, not returned by #49–#51 or a separate session API in this flow. | None; do not use as auth guard. |
| 24 `ME07-EL-24` | Progress bar | Static width `2/3`; no total/step value, role, `aria-valuenow` or server progress source. | None; not a verified authorization progress metric. |
| 25 `ME07-EL-25` | Rights/reconciliation explanatory text | Hardcoded claim about course-domain assignment and automatic permission after verification. Current APIs check direct owner per request. | Read-only; copy needs product/security approval. |
| 26 `ME07-EL-26` | Pedagogy promotional image | External/static image in HTML; not Content payload, not user/course data. HTML supplies `data-alt` rather than semantic `alt`. | No event. For implementation use an approved local/managed asset and meaningful alt or mark decorative. |
| 27 `ME07-EL-27` | “Không gian sư phạm” caption | Static marketing text, no API mapping. | No event. |
| 28 `ME07-EL-28` | Footer brand/legal text | Static copy; not form result. | No event. |
| 29 `ME07-EL-29` | Footer “Quy chế Giảng viên” link | `href="#"`; target not in source. | EV-10. |
| 30 `ME07-EL-30` | Footer “Tiêu chuẩn đánh giá” link | `href="#"`; target not in source. | EV-10. |
| 31 `ME07-EL-31` | Footer “Hỗ trợ kỹ thuật” link | `href="#"`; target not in source. | EV-10. |

## 4. Conditional UI & state variations
- States theo inventory: draft/dirty/validating/saving/conflict
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
