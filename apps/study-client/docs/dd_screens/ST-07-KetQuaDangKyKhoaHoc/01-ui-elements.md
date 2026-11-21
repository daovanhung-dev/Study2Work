# ST-07 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-07_markers.json](../../screen_stitch/03_student/ST-07_ket-qua-dang-ky-khoa-hoc/ST-07_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-07-EL-001` | `ST07-EL-01` | Study2Work brand link (href="/") |
| #2 | `ST-07-EL-002` | `ST07-EL-02` | Trang chủ, Khóa học, Khóa học của tôi, Tiến độ |
| #3 | `ST-07-EL-003` | `ST07-EL-03` | Đăng nhập link (href="/login") |
| #4 | `ST-07-EL-004` | `ST07-EL-04` | Đăng ký link (href="/register") |
| #5 | `ST-07-EL-005` | `ST07-EL-05` | Trang chủ, Khóa học, Kết quả đăng ký khóa học |
| #6 | `ST-07-EL-006` | `ST07-EL-06` | H1 “Kết quả đăng ký khóa học” |
| #7 | `ST-07-EL-007` | `ST07-EL-07` | Centered status-card container |
| #8 | `ST-07-EL-008` | `ST07-EL-08` | Static Material Symbol assignment_turned_in |
| #9 | `ST-07-EL-009` | `ST07-EL-09` | H2 “Chưa thể xác nhận kết quả đăng ký.” |
| #10 | `ST-07-EL-010` | `ST07-EL-10` | Static explanation that activation is not recorded |
| #11 | `ST-07-EL-011` | `ST07-EL-11` | “Về khóa học của tôi” link (href="/student/courses") |
| #12 | `ST-07-EL-012` | `ST07-EL-12` | Static Study2Work mark |
| #13 | `ST-07-EL-013` | `ST07-EL-13` | Trang chủ, Khóa học, Đăng nhập, Đăng ký |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Tọa độ dưới đây là DOM bounds CSS px tại viewport 1280×1024; ảnh render/annotation 2× (2560×2048). JSON đầy đủ gồm bounds và marker centers ở [ST-07_markers.json](../../screen_stitch/03_student/ST-07_ket-qua-dang-ky-khoa-hoc/ST-07_markers.json). Tất cả element đều thuộc static HTML prototype; không có Enrollment/payment binding.

| ID | Tên / loại / vị trí | Thuộc tính, nguồn và điều kiện | Trạng thái / event |
|---|---|---|---|
| #1 `ST07-EL-01` | Header brand link; top-left (`x=32,y=14,w=149.281,h=36`). | Text/mark Study2Work; `href="/"`; static. | Default/hover CSS. EV-07; root route unverified. |
| #2 `ST07-EL-02` | Header primary navigation group (`x=213.281,y=18,w=364.75,h=28`). | Trang chủ `/`, Khóa học `/courses`, Khóa học của tôi `/student/courses`, Tiến độ `/student/progress`; literal links. | Default/hover; `hidden md:flex` with no visible mobile replacement in HTML. EV-07. |
| #3 `ST07-EL-03` | Sign In link (`x=1047.516,y=12,w=105.375,h=40`). | “Đăng nhập”; `href="/login"`; static. | Default/hover. EV-07; does not establish session. |
| #4 `ST07-EL-04` | Sign Up link (`x=1160.891,y=12,w=87.109,h=40`). | “Đăng ký”; `href="/register"`; static. | Default/hover. EV-07. |
| #5 `ST07-EL-05` | Breadcrumb nav (`x=32,y=96,w=1216,h=20`). | Links Trang chủ `/`, Khóa học `/`; current page “Kết quả đăng ký khóa học” as text. No course/result ID. | Default/hover for links. EV-07. |
| #6 `ST07-EL-06` | Page H1 (`x=32,y=140,w=1216,h=38`). | Hard-coded “Kết quả đăng ký khóa học”. | Static. No event. |
| #7 `ST07-EL-07` | Centered result-card surface (`x=304,y=202,w=672,h=389.5`). | White surface/layout only; not an Enrollment/payment/Operation object; contains icon, result headline, paragraph and CTA. | Static prototype; no loading/disabled state. No event. |
| #8 `ST07-EL-08` | Assignment/check Material Symbol (`x=617.984,y=285,w=44.016,h=44`). | Literal `assignment_turned_in`; decorative icon, no state/data binding. | Static. Must not be read as enrollment success. No event. |
| #9 `ST07-EL-09` | Result headline H2 (`x=456.609,y=371,w=366.766,h=30`). | Literal “Chưa thể xác nhận kết quả đăng ký.”; no API/error mapping. | Static copy, neither `awaiting-confirmation` nor `failure` evidence. No event. |
| #10 `ST07-EL-10` | Supporting paragraph (`x=384,y=405,w=512,h=45.5`). | Literal copy that activation is not recorded and suggests checking course list; no Enrollment lookup. | Static. No retry/result detail. No event. |
| #11 `ST07-EL-11` | My Courses CTA (`x=541.656,y=482.5,w=196.688,h=44`). | Anchor “Về khóa học của tôi”; literal `/student/courses`; no courseId/status payload. | Default/hover CSS. EV-06; route/auth unverified. |
| #12 `ST07-EL-12` | Footer brand group (`x=32,y=968,w=148.875,h=32`). | Static Study2Work logo/text, not an anchor. | Static. No event. |
| #13 `ST07-EL-13` | Footer navigation group (`x=950.484,y=976,w=297.516,h=16`). | Links Trang chủ `/`, Khóa học `/courses`, Đăng nhập `/login`, Đăng ký `/register`. | Default/hover. EV-07. |

## 4. Conditional UI & state variations
- States theo inventory: awaiting-confirmation/enrolled/conflict/failure
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-07_ket-qua-dang-ky-khoa-hoc/ST-07.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
