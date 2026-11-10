# AD-21 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-21_markers.json](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/AD-21_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-21-EL-001` | `not supplied in marker JSON` | Study2Work / LMS / Admin Portal brand |
| #2 | `AD-21-EL-002` | `not supplied in marker JSON` | Shell navigation — Tổng quan |
| #3 | `AD-21-EL-003` | `not supplied in marker JSON` | Shell navigation — Người dùng |
| #4 | `AD-21-EL-004` | `not supplied in marker JSON` | Shell navigation — Khóa học & Nội dung |
| #5 | `AD-21-EL-005` | `not supplied in marker JSON` | Shell navigation — Kiểm duyệt |
| #6 | `AD-21-EL-006` | `not supplied in marker JSON` | Shell navigation — Báo cáo |
| #7 | `AD-21-EL-007` | `not supplied in marker JSON` | System Normal status badge |
| #8 | `AD-21-EL-008` | `not supplied in marker JSON` | Header notification bell and unread dot |
| #9 | `AD-21-EL-009` | `not supplied in marker JSON` | Admin identity / role / avatar |
| #10 | `AD-21-EL-010` | `not supplied in marker JSON` | Global breadcrumb — Hệ thống / Quản trị trung tâm / Không gian làm việc |
| #11 | `AD-21-EL-011` | `not supplied in marker JSON` | RBAC assurance label |
| #12 | `AD-21-EL-012` | `not supplied in marker JSON` | Local notification breadcrumb |
| #13 | `AD-21-EL-013` | `not supplied in marker JSON` | Return to list AD-19 anchor |
| #14 | `AD-21-EL-014` | `not supplied in marker JSON` | Screen ID badge and candidate route |
| #15 | `AD-21-EL-015` | `not supplied in marker JSON` | Page heading |
| #16 | `AD-21-EL-016` | `not supplied in marker JSON` | Supporting description |
| #17 | `AD-21-EL-017` | `not supplied in marker JSON` | Admin permission environment badge |
| #18 | `AD-21-EL-018` | `not supplied in marker JSON` | Technical identity panel heading/icon |
| #19 | `AD-21-EL-019` | `not supplied in marker JSON` | Active protection badge |
| #20 | `AD-21-EL-020` | `not supplied in marker JSON` | Notification ID card |
| #21 | `AD-21-EL-021` | `not supplied in marker JSON` | Operation ID card |
| #22 | `AD-21-EL-022` | `not supplied in marker JSON` | Publishing status card |
| #23 | `AD-21-EL-023` | `not supplied in marker JSON` | Missing-detail / locked-actions notice |
| #24 | `AD-21-EL-024` | `not supplied in marker JSON` | Notification content panel heading/icon |
| #25 | `AD-21-EL-025` | `not supplied in marker JSON` | Static-view badge |
| #26 | `AD-21-EL-026` | `not supplied in marker JSON` | Notification title label and placeholder field |
| #27 | `AD-21-EL-027` | `not supplied in marker JSON` | Channel label / placeholder field |
| #28 | `AD-21-EL-028` | `not supplied in marker JSON` | In-App channel chip |
| #29 | `AD-21-EL-029` | `not supplied in marker JSON` | Email channel chip |
| #30 | `AD-21-EL-030` | `not supplied in marker JSON` | Content label and placeholder area |
| #31 | `AD-21-EL-031` | `not supplied in marker JSON` | Locked-content safety note |
| #32 | `AD-21-EL-032` | `not supplied in marker JSON` | Recipient label and placeholder field |
| #33 | `AD-21-EL-033` | `not supplied in marker JSON` | Disabled Update draft button |
| #34 | `AD-21-EL-034` | `not supplied in marker JSON` | Delivery progress panel heading/icon |
| #35 | `AD-21-EL-035` | `not supplied in marker JSON` | In-App channel delivery card/status |
| #36 | `AD-21-EL-036` | `not supplied in marker JSON` | In-App completion bar and 0/0 row |
| #37 | `AD-21-EL-037` | `not supplied in marker JSON` | Email channel delivery card/status |
| #38 | `AD-21-EL-038` | `not supplied in marker JSON` | Email queue bar/status row |
| #39 | `AD-21-EL-039` | `not supplied in marker JSON` | Disabled Cancel release button |
| #40 | `AD-21-EL-040` | `not supplied in marker JSON` | Cancel action safety note |
| #41 | `AD-21-EL-041` | `not supplied in marker JSON` | SH-07 operation portal card heading/icon |
| #42 | `AD-21-EL-042` | `not supplied in marker JSON` | SH-07 handoff description |
| #43 | `AD-21-EL-043` | `not supplied in marker JSON` | Disabled SH-07 portal link |
| #44 | `AD-21-EL-044` | `not supplied in marker JSON` | Footer copyright and system label |
| #45 | `AD-21-EL-045` | `not supplied in marker JSON` | Footer privacy policy link |
| #46 | `AD-21-EL-046` | `not supplied in marker JSON` | Footer RBAC standards link |
| #47 | `AD-21-EL-047` | `not supplied in marker JSON` | Footer technical support link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Ảnh chú thích có 47 marker `#1`–`#47`, ánh xạ theo bảng dưới đây. Kích thước/vị trí nhìn theo ảnh nguồn 1425×1600; tọa độ marker nằm trong [`AD-21_markers.json`](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/AD-21_markers.json). Marker đặt cạnh phần tử hoặc vùng trống. Các value/status ghi dưới đây phân biệt giá trị in sẵn với dữ liệu API.

| # / Element ID | Tên, loại, vị trí | Thuộc tính / nguồn / validation | Hiển thị, trạng thái | Sự kiện |
|---:|---|---|---|---|
| **#1 `AD21-EL-01`** | Brand `Study2Work / LMS / Admin Portal`; nhóm nhận diện ở header. | Text/icon tĩnh; HTML dùng `div`, không phải link. Không có tenant/app data. | Visible; layout desktop. | — |
| **#2 `AD21-EL-02`** | Shell nav “Tổng quan”; anchor. | `href="#"`, `data-path="tong-quan"`; không có route binding. | Visible desktop; anchor style. | EV-02 |
| **#3 `AD21-EL-03`** | Shell nav “Người dùng”; anchor. | `href="#"`, `data-path="nguoi-dung"`. | Visible desktop; không có active route. | EV-02 |
| **#4 `AD21-EL-04`** | Shell nav “Khóa học & Nội dung”; anchor. | `href="#"`, `data-path="khoa-hoc-noi-dung"`. | Visible desktop. | EV-02 |
| **#5 `AD21-EL-05`** | Shell nav “Kiểm duyệt”; anchor. | `href="#"`, `data-path="kiem-duyet"`. | Visible desktop. | EV-02 |
| **#6 `AD21-EL-06`** | Shell nav “Báo cáo”; anchor. | `href="#"`, `data-path="bao-cao"`. | Visible desktop. | EV-02 |
| **#7 `AD21-EL-07`** | “System Normal”; status badge. | Literal string + pulse dot; không có health API/source. | Visible ở header; không phải runtime health. | — |
| **#8 `AD21-EL-08`** | Header Notifications bell + unread dot; button. | `aria-label="Notifications"`; nút có `type=button`, dot tĩnh; không có count/href/handler. | Enabled-looking; thực tế no-op. | EV-03 |
| **#9 `AD21-EL-09`** | Admin identity, role text và avatar. | Literal “TS. Quản Trị Viên / ADMIN / QUẢN TRỊ VIÊN”; avatar là `div`, không có auth/session binding. | Visible; không phải bằng chứng actor đã được xác thực. | — |
| **#10 `AD21-EL-10`** | Global breadcrumb “Hệ thống > Quản trị trung tâm > Không gian làm việc”. | Text/icon; các mục là `span`, không có route. | Visible; static. | — |
| **#11 `AD21-EL-11`** | “Chuẩn xác thực RBAC”; assurance label. | Text + shield icon; no policy check/authorization result. | Visible; static claim. | — |
| **#12 `AD21-EL-12`** | Local breadcrumb “Quản trị truyền thông > Thông báo hệ thống > Chi tiết và trạng thái phát hành”. | Static text; không có href. | Visible. | — |
| **#13 `AD21-EL-13`** | “Quay lại danh sách thông báo (AD-19)”; return anchor/button style. | `href="#"`; không mang notification ID, filter, scroll position hoặc return URL. | Enabled-looking; chưa nối AD-19. | EV-04 |
| **#14 `AD21-EL-14`** | Screen badge `MÀN HÌNH AD-21` + candidate route `/admin/notifications/:notificationId`. | Literal ID/route; param chưa được nạp/validate; route candidate từ inventory. | Visible; không phải current router evidence. | EV-01 |
| **#15 `AD21-EL-15`** | Page heading “Kiểm soát và giám sát trạng thái thông báo”. | Static heading. | Visible. | — |
| **#16 `AD21-EL-16`** | Supporting description. | Static text về cấu hình, mã thực thi và giám sát thời gian thực; không có implementation. | Visible; mô tả thiết kế. | — |
| **#17 `AD21-EL-17`** | “Môi trường kiểm soát phân quyền Quản trị viên”; badge. | Static RBAC/admin copy, not a permission key or server result. | Visible. | — |
| **#18 `AD21-EL-18`** | “Đối chiếu định danh kỹ thuật độc lập”; technical panel heading/icon. | Static label describing notification/operation identity separation. | Visible. | — |
| **#19 `AD21-EL-19`** | “Cổng bảo vệ chủ động”; safety badge. | Static copy; no guard state binding. | Visible. | — |
| **#20 `AD21-EL-20`** | Notification ID card. | Static label, “Chưa nạp tham số ID hợp lệ” and REST URI hint; no ID data or parser. API #94–#96 path is `notification_id:int64`. | Visible; unresolved ID gate. | EV-01 |
| **#21 `AD21-EL-21`** | Operation ID card. | Static “Chưa liên kết”; no value/source/ID conversion. #18 type/producer conflict remains. | Visible; unresolved. | EV-07 |
| **#22 `AD21-EL-22`** | Publishing status card. | Static “Chờ xác thực”; not one of a verified API status values. | Visible; not a server state. | EV-01 |
| **#23 `AD21-EL-23`** | Missing-detail and locked-actions notice. | Copy says there is no independent detail endpoint and actions are temporarily locked until valid session; current inventory uses #96 for status read. This text is explanatory prototype copy, not API response. | Visible; info state. | EV-01, EV-05, EV-06 |
| **#24 `AD21-EL-24`** | “Nội dung bản tin”; content panel heading/icon and subtitle. | Static heading. | Visible. | — |
| **#25 `AD21-EL-25`** | “CHẾ ĐỘ XEM TĨNH”; view-mode badge. | Literal state. | Visible; describes prototype state only. | — |
| **#26 `AD21-EL-26`** | Notification title label/placeholder field. | Required-looking label; visible value `--`; implemented as static `div`, no input or validation. #96 local projection includes title; #94 local body update is DERIVED. | Read-only placeholder; no actual edit. | EV-05 |
| **#27 `AD21-EL-27`** | Channel label and placeholder field. | Static `--`; no selected value/model. | Read-only placeholder. | EV-01 |
| **#28 `AD21-EL-28`** | “In-App” channel chip. | Static chip; no confirmed mapping to local API channel `PUSH`. | Visible; not selected/bound. | EV-01 |
| **#29 `AD21-EL-29`** | “Email” channel chip. | Static chip; local fallback accepts `EMAIL`, but the HTML does not bind response data. | Visible; not selected/bound. | EV-01 |
| **#30 `AD21-EL-30`** | “Nội dung chi tiết”; content placeholder panel. | Static `--`; not textarea/editor. #96 local projection includes `content`, while #94 local update accepts `content` only as DERIVED body field. | Read-only placeholder. | EV-05 |
| **#31 `AD21-EL-31`** | Lock note “Dữ liệu bị khóa tự động theo cơ chế bảo vệ cấu trúc”. | Static lock icon/copy, no data-lock state from backend. | Visible. | — |
| **#32 `AD21-EL-32`** | Recipient label/placeholder. | Static `--`; #96 response does not include recipient; no source/selector. | Read-only placeholder. | EV-01 |
| **#33 `AD21-EL-33`** | “Cập nhật bản nháp”; disabled button. | Native button with `disabled`; no form/input/body exists. Direct #94 catalog has no request body; local server body is a DERIVED strict `{title, content}`. | Disabled; cannot submit. | EV-05 |
| **#34 `AD21-EL-34`** | “Tiến trình phân phối kênh”; delivery panel heading/icon. | Static heading and infrastructure copy. | Visible. | — |
| **#35 `AD21-EL-35`** | In-App delivery card and “Chờ dữ liệu” badge. | Static channel, subtitle and status; no binding. #96 does not return per-channel status; local channel token is `PUSH`, not approved as In-App. | Visible; no loaded state. | EV-01 |
| **#36 `AD21-EL-36`** | In-App progress bar, “Tỷ lệ hoàn tất”, `0 / 0 bản ghi`. | Static bar/count. #96 returns no delivery counts or completion ratio. | Visible; zero is mockup copy. | EV-01 |
| **#37 `AD21-EL-37`** | Email delivery card and “Chờ cổng gửi” badge. | Static SMTP pipeline copy; no provider/runtime evidence or per-channel status response. | Visible; no loaded state. | EV-01 |
| **#38 `AD21-EL-38`** | Email queue bar and “Chưa kích hoạt luồng” label. | Static bar/text; #96 has aggregate notification status only. | Visible; not queue telemetry. | EV-01 |
| **#39 `AD21-EL-39`** | “Hủy bỏ phát hành”; disabled button. | Native `disabled` button; no confirmation or click handler. API #95 is DELETE returning `DeleteResult`; local behavior is hard delete, not provider cancellation. | Disabled. | EV-06 |
| **#40 `AD21-EL-40`** | Cancel safety note. | Static text says cancellation is disabled to preserve safety; does not establish scheduler/provider cancellation semantics. | Visible. | EV-06 |
| **#41 `AD21-EL-41`** | “Cổng theo dõi tác vụ bất đồng bộ”; SH-07 panel heading/icon. | Static section heading. | Visible. | EV-07 |
| **#42 `AD21-EL-42`** | SH-07 handoff description. | Says admin can follow large sends through SH-07 when a valid Operation ID exists; inventory/API #18 handoff is conditional and unresolved. | Visible; design claim with blocker. | EV-07 |
| **#43 `AD21-EL-43`** | “Theo dõi qua cổng tác vụ bất đồng bộ (SH-07)”; disabled link/button. | Native disabled button. No route/ID; #18 is not registered in Study Server. | Disabled / “Đang khóa”. | EV-07 |
| **#44 `AD21-EL-44`** | Footer copyright and system label. | Literal `© 2025 Study2Work LMS. Hệ thống quản trị trung tâm.` | Visible. | — |
| **#45 `AD21-EL-45`** | Footer privacy policy link. | Anchor `href="#"`; no policy destination. | Enabled-looking; no destination. | EV-08 |
| **#46 `AD21-EL-46`** | Footer RBAC standards link. | Anchor `href="#"`; no standards destination. | Enabled-looking; no destination. | EV-08 |
| **#47 `AD21-EL-47`** | Footer technical support link. | Anchor `href="#"`; no support destination. | Enabled-looking; no destination. | EV-08 |

## 4. Conditional UI & state variations
- States theo inventory: expected: draft/scheduled/sending/delivered/failed; local fallback: QUEUED/SENT/FAILED
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/AD-21.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
