# ST-02 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-02_markers.json](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/ST-02_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-02-EL-001` | `ST02-EL-01` | Header brand Study2Work link |
| #2 | `ST-02-EL-002` | `ST02-EL-02` | Primary navigation group: home, courses, my courses and profile |
| #3 | `ST-02-EL-003` | `ST02-EL-03` | Header login link |
| #4 | `ST-02-EL-004` | `ST02-EL-04` | Page title and supporting description |
| #5 | `ST-02-EL-005` | `ST02-EL-05` | Profile card surface and account icon |
| #6 | `ST-02-EL-006` | `ST02-EL-06` | Profile card heading and sign-in explanation |
| #7 | `ST-02-EL-007` | `ST02-EL-07` | Profile card login call to action |
| #8 | `ST-02-EL-008` | `ST02-EL-08` | Disabled edit-profile button |
| #9 | `ST-02-EL-009` | `ST02-EL-09` | Footer Study2Work brand link |
| #10 | `ST-02-EL-010` | `ST02-EL-10` | Footer navigation group |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết element

Marker IDs #1–#10 có một hàng tương ứng trong `ST-02_markers.json` và ảnh chú thích. `screen.png` là asset gốc nhưng không có body; `screen_rendered.png` là render thứ cấp thuần của `code.html`; `screen_composite.png` giữ header/footer gốc và chèn body từ bản render để đủ vùng nhìn thấy cho cả 10 marker. Composite không phải runtime capture và không ghi đè hai asset nguồn.

| Marker / Element ID | Tên, loại, vị trí và mục đích | Thuộc tính, dữ liệu, hiển thị và trạng thái | Sự kiện |
|---|---|---|---|
| #1 `ST02-EL-01` | Brand Study2Work ở đầu header, link về trang chủ theo metadata. | Anchor `href="#"`, `data-path="trang-chu"`; text `Study2Work`. Không có router binding. | `ST02-EV-02`. |
| #2 `ST02-EL-02` | Primary navigation group: Trang chủ, Khóa học, Khóa học của tôi, Hồ sơ cá nhân. | Bốn anchors `href="#"`; data-path tương ứng `trang-chu`, `khoa-hoc`, `khoa-hoc-cua-toi`, `ho-so-hoc-vien`. Profile có active style tĩnh; không phản ánh route state do router. | `ST02-EV-02`. |
| #3 `ST02-EL-03` | Login link ở góc phải header. | Anchor `href="#"`, `data-path="dang-nhap"`, min-height 44px; không gắn SH-02 route/session behavior. | `ST02-EV-03`. |
| #4 `ST02-EL-04` | Page heading “Hồ sơ cá nhân” và supporting description. | Static HTML text; không lấy từ API. Heading trong source PNG gốc không thấy; chỉ có ở HTML-derived render. | Không có event. |
| #5 `ST02-EL-05` | Profile card surface và account icon. | White card, border/rounded surface; icon `account_circle` mang tính minh họa; không phải user avatar từ #04. Card hiện ở HTML render, vắng khỏi source PNG. | Không có event. |
| #6 `ST02-EL-06` | Card heading “Thông tin hồ sơ học viên” và sign-in explanatory copy. | Static copy yêu cầu đăng nhập để tải/hiển thị profile. Đây là empty/gated copy, không phải 401 response hay actual session check. | Không có event. |
| #7 `ST02-EL-07` | Login CTA bên trong profile card. | Anchor `href="#"`, `data-path="dang-nhap"`, có icon login và visible text. Không giữ `returnTo` hoặc điều hướng thật. | `ST02-EV-03`. |
| #8 `ST02-EL-08` | Button “Chỉnh sửa hồ sơ (Tạm khóa)”. | Native button `disabled`, title “Chức năng tạm khóa”; no handler, no update request. Visual says edit unavailable. | `ST02-EV-04` — browser không phát click cho disabled control. |
| #9 `ST02-EL-09` | Footer brand link Study2Work. | Anchor `href="#"`, `data-path="trang-chu"`; static brand. | `ST02-EV-05`. |
| #10 `ST02-EL-10` | Footer navigation group: Trang chủ, Khóa học, Điều khoản sử dụng, Chính sách bảo mật. | Four anchors `href="#"`, metadata data-path; no route/terms/privacy document source associated. | `ST02-EV-05`. |

### Dữ liệu #04 hiện có và giới hạn mapping

| Response path | Current source type/nullability | Candidate use on ST-02 | Limit |
|---|---|---|---|
| `data.id` | `int`, required | Identity for client state only if needed; do not display by default. | Not listed as a visible profile field. |
| `data.full_name` | `string`, required | Likely identity label in a ready state. | No ready-state layout in source assets. |
| `data.email` | `string`, required | Inventory expects email. | No ready-state layout or masking/copy policy. |
| `data.role` | `string`, required, from DB | Inventory expects role/status. | Authorization uses JWT role instead; DB role may differ from JWT. |
| `data.avatar_url` | `string \| null` | Inventory expects avatar. | No URL display/fallback/loading policy; current card icon is static, not avatar. |
| `data.phone` | `string \| null` | No display mapping in ST-02 inventory. | Do not add field to view without approved design. |
| `data.status` | `string`, required by model | Inventory expects status. | Source returns it but does not gate access by it; candidate DDL permits null. |
| `data.created_at`, `data.updated_at` | datetime serialized to JSON strings | Not in ST-02 inventory. | Do not expose or format without design requirement. |
| `data.bio` | Optional in catalog, no current source mapping | None. | Current query/model omit; current API #14 also ignores it. |
| permissions | Mentioned by AC-02, absent in catalog response model/query | None. | No permission source/schema/endpoint in #04. |

## 4. Conditional UI & state variations
- States theo inventory: loading/ready/401/403
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-02_ho-so-ca-nhan/ST-02.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
