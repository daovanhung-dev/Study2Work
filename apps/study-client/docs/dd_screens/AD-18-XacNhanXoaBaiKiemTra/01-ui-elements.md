# AD-18 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-18_markers.json](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/AD-18_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-18-EL-001` | `not supplied in marker JSON` | Study2Work LMS/Admin brand |
| #2 | `AD-18-EL-002` | `not supplied in marker JSON` | Shell navigation — Tổng quan |
| #3 | `AD-18-EL-003` | `not supplied in marker JSON` | Shell navigation — Người dùng |
| #4 | `AD-18-EL-004` | `not supplied in marker JSON` | Shell navigation — Khóa học & Nội dung |
| #5 | `AD-18-EL-005` | `not supplied in marker JSON` | Shell navigation — Kiểm duyệt |
| #6 | `AD-18-EL-006` | `not supplied in marker JSON` | Shell navigation — Báo cáo |
| #7 | `AD-18-EL-007` | `not supplied in marker JSON` | System Normal status copy (static) |
| #8 | `AD-18-EL-008` | `not supplied in marker JSON` | Notifications button (no handler) |
| #9 | `AD-18-EL-009` | `not supplied in marker JSON` | Admin identity and avatar (static) |
| #10 | `AD-18-EL-010` | `not supplied in marker JSON` | Global breadcrumb |
| #11 | `AD-18-EL-011` | `not supplied in marker JSON` | RBAC assurance copy (static) |
| #12 | `AD-18-EL-012` | `not supplied in marker JSON` | Local breadcrumb — Quản trị khảo thí |
| #13 | `AD-18-EL-013` | `not supplied in marker JSON` | Local breadcrumb — Danh sách bài kiểm tra |
| #14 | `AD-18-EL-014` | `not supplied in marker JSON` | Current local breadcrumb — Xóa bài kiểm tra |
| #15 | `AD-18-EL-015` | `not supplied in marker JSON` | Return to AD-15 link (href #) |
| #16 | `AD-18-EL-016` | `not supplied in marker JSON` | Danger context warning icon |
| #17 | `AD-18-EL-017` | `not supplied in marker JSON` | Risk-of-learning-data-impact label |
| #18 | `AD-18-EL-018` | `not supplied in marker JSON` | Confirmation title |
| #19 | `AD-18-EL-019` | `not supplied in marker JSON` | Target record section heading |
| #20 | `AD-18-EL-020` | `not supplied in marker JSON` | Selected-record status pill (placeholder) |
| #21 | `AD-18-EL-021` | `not supplied in marker JSON` | Quiz title field and placeholder value |
| #22 | `AD-18-EL-022` | `not supplied in marker JSON` | Quiz identifier field and placeholder value |
| #23 | `AD-18-EL-023` | `not supplied in marker JSON` | Linked course field and placeholder value |
| #24 | `AD-18-EL-024` | `not supplied in marker JSON` | Attempt safety notice icon |
| #25 | `AD-18-EL-025` | `not supplied in marker JSON` | Safety policy heading |
| #26 | `AD-18-EL-026` | `not supplied in marker JSON` | Attempt/history warning paragraph (static claim) |
| #27 | `AD-18-EL-027` | `not supplied in marker JSON` | Unresolved Attempts Policy copy |
| #28 | `AD-18-EL-028` | `not supplied in marker JSON` | Hard-lock Read-Only copy |
| #29 | `AD-18-EL-029` | `not supplied in marker JSON` | Audit reason label |
| #30 | `AD-18-EL-030` | `not supplied in marker JSON` | ISO-27001 policy copy (static claim) |
| #31 | `AD-18-EL-031` | `not supplied in marker JSON` | Disabled audit reason textarea |
| #32 | `AD-18-EL-032` | `not supplied in marker JSON` | Disabled field hint |
| #33 | `AD-18-EL-033` | `not supplied in marker JSON` | Safe return link (href #) |
| #34 | `AD-18-EL-034` | `not supplied in marker JSON` | Permanent delete button (disabled; no handler) |
| #35 | `AD-18-EL-035` | `not supplied in marker JSON` | Data-protection banner copy (static claim) |
| #36 | `AD-18-EL-036` | `not supplied in marker JSON` | ED-TECH compliance badge (static claim) |
| #37 | `AD-18-EL-037` | `not supplied in marker JSON` | Copyright and system label |
| #38 | `AD-18-EL-038` | `not supplied in marker JSON` | Privacy policy footer link (href #) |
| #39 | `AD-18-EL-039` | `not supplied in marker JSON` | RBAC standards footer link (href #) |
| #40 | `AD-18-EL-040` | `not supplied in marker JSON` | Technical support footer link (href #) |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

Tọa độ marker được lưu bằng source pixels trong [AD-18_markers.json](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/AD-18_markers.json); ảnh hiển thị 2×. Các giá trị `--`/`Chưa chọn bản ghi`, trạng thái disabled và security/policy claims dưới đây là giá trị tĩnh của mockup, không phải dữ liệu runtime.

| ID | Tên và loại | Vị trí/mục đích | Tọa độ marker (x,y; source px) | Thuộc tính, nguồn và validation | Hiển thị/trạng thái | Event |
|---:|---|---|---|---|---|
| 1 | Brand Study2Work/Admin — brand group | Header trái; nhận diện hệ thống | (`16,36`) | Static text/logo; không nhận data | Visible; static | — |
| 2 | Tổng quan — navigation link | Header nav | (`355,61`) | HTML `href="#"`; destination chưa có | Visible; no route behavior | EV-06 |
| 3 | Người dùng — navigation link | Header nav | (`490,61`) | HTML `href="#"`; destination chưa có | Visible; no route behavior | EV-06 |
| 4 | Khóa học & Nội dung — navigation link | Header nav | (`660,61`) | HTML `href="#"`; destination chưa có | Visible; no route behavior | EV-06 |
| 5 | Kiểm duyệt — navigation link | Header nav | (`856,61`) | HTML `href="#"`; destination chưa có | Visible; no route behavior | EV-06 |
| 6 | Báo cáo — navigation link | Header nav | (`983,61`) | HTML `href="#"`; destination chưa có | Visible; no route behavior | EV-06 |
| 7 | System Normal badge — status copy | Header phải | (`1152,61`) | Literal mockup; không nối health API | Visible; không chứng minh hệ thống normal | — |
| 8 | Notifications — button | Header phải | (`1295,60`) | `button`, `aria-label=Notifications`; không listener | Visible; clickable-looking, no handler | EV-06 |
| 9 | Admin identity/avatar — profile group | Header phải | (`1584,61`) | Static “TS. Quản Trị Viên”/`ADMIN`; không đọc session | Visible; không chứng minh identity/permission runtime | — |
| 10 | Global breadcrumb — navigation text | Shell row | (`18,95`) | Static hierarchy; không có route handler trong HTML | Visible; static | — |
| 11 | RBAC assurance badge — claim | Shell row phải | (`1585,95`) | Static copy “Chuẩn xác thực RBAC”; không có guard evidence | Visible; static claim | — |
| 12 | Quản trị khảo thí — breadcrumb text | Local navigation rail | (`130,171`) | Current label; không link destination | Visible; static | — |
| 13 | Danh sách bài kiểm tra — breadcrumb link | Local navigation rail | (`333,171`) | `href="#"`; intended AD-15, no route | Visible; no navigation runtime | EV-02 |
| 14 | Xóa bài kiểm tra — current breadcrumb | Local navigation rail | (`508,171`) | Static current section | Visible; static | — |
| 15 | Quay lại danh sách bài kiểm tra (AD-15) — anchor/button style | Rail phải | (`1547,247`) | `href="#"`; intended AD-15. Filter/page handoff unspecified | Visible; no handler | EV-02 |
| 16 | Danger warning icon — decorative icon | Main panel header trái | (`346,390`) | Icon only; no independent action | Visible; decorative | — |
| 17 | Risk-of-learning-data-impact — eyebrow text | Main panel header | (`880,328`) | Static warning label | Visible; copy does not prove actual policy | — |
| 18 | Xác nhận gỡ bỏ bài kiểm tra khỏi hệ thống — heading | Main panel header | (`985,393`) | Static H1 | Visible | — |
| 19 | Thông tin bản ghi mục tiêu — section heading | Target record card | (`390,462`) | Static heading | Visible | — |
| 20 | Chưa chọn bản ghi — status pill | Target card right | (`1218,462`) | Static placeholder; no selected-record state source | Visible; placeholder | — |
| 21 | Tên bài thi — label/value card | Target card, column 1 | (`640,606`) | Current value `--`; potential source #87 `title`, only after approved handoff | Visible; mockup value unresolved | EV-01 |
| 22 | Mã định danh khảo thí — label/value card | Target card, column 2 | (`920,606`) | Current “Chưa chọn bản ghi”; candidate `quizId` / #87 `id`; map/format must be approved | Visible; placeholder | EV-01 |
| 23 | Khóa học liên kết — label/value card | Target card, column 3 | (`1200,606`) | Current `--`; #87 returns `course_id`, not course title | Visible; no valid display mapping | EV-01 |
| 24 | Attempt safety icon — decorative icon | Warning card left | (`350,770`) | Icon only; no data/action | Visible; decorative | — |
| 25 | Chính sách bảo toàn kết quả & Khóa an toàn — heading | Warning card | (`900,715`) | Static claim | Visible; not API policy | — |
| 26 | Attempt/history warning paragraph — warning text | Warning card body | (`1215,803`) | Static claim that delete is blocked and manual DB action is needed; conflicts with local #90 branches and unapproved policy | Visible; no data binding | — |
| 27 | Unresolved Attempts Policy — rule badge | Warning card bottom left | (`760,878`) | Static English copy; not a resolved policy enum | Visible; unsupported as runtime policy value | — |
| 28 | Khóa cứng (Read-Only) — status badge | Warning card bottom right | (`1160,878`) | Static copy; no UI state source beyond disabled elements in mockup | Visible; static | — |
| 29 | Lý do kiểm toán hệ thống — label | Audit region | (`625,927`) | Associates to `textarea#audit-reason`; whether required is not in #90 contract | Visible | EV-05 |
| 30 | ISO-27001 (Bị khóa theo chính sách) — policy copy | Audit label right | (`1217,927`) | Static claim, no policy source or server data | Visible; static | — |
| 31 | Audit reason — textarea | Audit region | (`380,1066`) | `disabled`; placeholder says reason required. #90 has no body; do not send value. No length/validation contract | Visible; Disabled/Readonly in mockup | EV-05 |
| 32 | Trường dữ liệu vô hiệu hóa — disabled hint | Textarea lower-right | (`1221,1095`) | Static hint with lock icon | Visible; static | — |
| 33 | Quay lại an toàn — anchor/button style | Bottom action row | (`685,1138`) | `href="#"`; no route behavior | Visible; enabled appearance, no handler | EV-03 |
| 34 | Xác nhận xóa vĩnh viễn — destructive button | Bottom action row | (`1225,1138`) | `disabled`, `aria-disabled="true"`; no click handler. API #90 has only path input | Visible; Disabled | EV-04 |
| 35 | Data protection auto-activated — footer copy | Inner panel footer left | (`735,1252`) | Static statement; no runtime control/system evidence | Visible; static claim | — |
| 36 | ED-TECH COMPLIANCE • SAFE-GUARD ENABLED — badge | Inner panel footer right | (`1254,1252`) | Static copy; no compliance/API state source | Visible; static claim | — |
| 37 | Copyright and central-admin label — footer text | Global footer left | (`468,1390`) | Literal © 2025 Study2Work LMS/system text | Visible; static | — |
| 38 | Quy chế bảo mật dữ liệu — footer link | Global footer | (`1090,1390`) | `href="#"`; destination unknown | Visible; no handler | EV-06 |
| 39 | Tiêu chuẩn phân quyền RBAC — footer link | Global footer | (`1368,1390`) | `href="#"`; destination unknown | Visible; no handler | EV-06 |
| 40 | Hỗ trợ kỹ thuật hệ thống — footer link | Global footer | (`1584,1390`) | `href="#"`; destination unknown | Visible; no handler | EV-06 |

### Quy tắc dùng chung cho elements

- Design source is the supplied static Admin prototype. No shared runtime component/theme behavior was found in Study Web source because app source is absent. Do not present prototype copy as Design System implementation.
- Disabled confirm and textarea do not accept keyboard, pointer or pasted input in the current HTML. A future enablement requires explicit approved state/policy; do not infer enablement from a selected row.
- Use semantic heading/labels and accessible disabled state when implementation is designed. Preserve a visible focus target and announce asynchronous result/errors; exact live regions/keyboard behavior are not defined by current source.
- Responsive layout is present only through Tailwind classes in the mockup; it is not tested in a running client. Narrow-screen order and sticky-shell behavior remain unverified.

## 4. Conditional UI & state variations
- States theo inventory: confirm/deleting/deleted/unauthorized/forbidden/not-found/validation-error/service-error/unknown-outcome/unwired; `conflict` unsupported
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/AD-18.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
