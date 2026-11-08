# SH-07 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [SH-07_markers.json](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `SH-07-EL-001` | `SH07-EL-01` | Header brand |
| #2 | `SH-07-EL-002` | `SH07-EL-02` | Primary navigation group |
| #3 | `SH-07-EL-003` | `SH07-EL-03` | Login link |
| #4 | `SH-07-EL-004` | `SH07-EL-04` | Register CTA |
| #5 | `SH-07-EL-005` | `SH07-EL-05` | Decorative account icon |
| #6 | `SH-07-EL-006` | `SH07-EL-06` | Specification Gate banner |
| #7 | `SH-07-EL-007` | `SH07-EL-07` | View Contract Spec button |
| #8 | `SH-07-EL-008` | `SH07-EL-08` | Breadcrumb and proposed route |
| #9 | `SH-07-EL-009` | `SH07-EL-09` | Page title and supporting description |
| #10 | `SH-07-EL-010` | `SH07-EL-10` | System status badge |
| #11 | `SH-07-EL-011` | `SH07-EL-11` | Mock environment badge |
| #12 | `SH-07-EL-012` | `SH07-EL-12` | Target route and displayed Operation ID |
| #13 | `SH-07-EL-013` | `SH07-EL-13` | Copy Operation ID button |
| #14 | `SH-07-EL-014` | `SH07-EL-14` | Backend integration gate badge |
| #15 | `SH-07-EL-015` | `SH07-EL-15` | Operation type metric |
| #16 | `SH-07-EL-016` | `SH07-EL-16` | Server-authorized origin metric |
| #17 | `SH-07-EL-017` | `SH07-EL-17` | Disabled execution-progress metric |
| #18 | `SH-07-EL-018` | `SH07-EL-18` | Anti-faking policy and guardrails |
| #19 | `SH-07-EL-019` | `SH07-EL-19` | Return to course list CTA |
| #20 | `SH-07-EL-020` | `SH07-EL-20` | Return home CTA |
| #21 | `SH-07-EL-021` | `SH07-EL-21` | Developer hand-off heading and environment badge |
| #22 | `SH-07-EL-022` | `SH07-EL-22` | Developer hand-off explanation |
| #23 | `SH-07-EL-023` | `SH07-EL-23` | Schema mismatch diagnostic code fragment |
| #24 | `SH-07-EL-024` | `SH07-EL-24` | Lifecycle reference heading |
| #25 | `SH-07-EL-025` | `SH07-EL-25` | QUEUED lifecycle reference card |
| #26 | `SH-07-EL-026` | `SH07-EL-26` | RUNNING lifecycle reference card |
| #27 | `SH-07-EL-027` | `SH07-EL-27` | SUCCEEDED lifecycle reference card |
| #28 | `SH-07-EL-028` | `SH07-EL-28` | FAILED lifecycle reference card |
| #29 | `SH-07-EL-029` | `SH07-EL-29` | EXPIRED lifecycle reference card |
| #30 | `SH-07-EL-030` | `SH07-EL-30` | Orchestration model heading |
| #31 | `SH-07-EL-031` | `SH07-EL-31` | Client, API Gateway, Queue and Worker diagram |
| #32 | `SH-07-EL-032` | `SH07-EL-32` | Orchestration diagram caption |
| #33 | `SH-07-EL-033` | `SH07-EL-33` | Footer brand and platform descriptor |
| #34 | `SH-07-EL-034` | `SH07-EL-34` | Footer navigation group |
| #35 | `SH-07-EL-035` | `SH07-EL-35` | Copyright text |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 3. Ảnh và marker

- [Ảnh nguồn nguyên trạng](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/screen.png) kích thước 1503×1600; được giữ nguyên.
- [Ảnh chú thích](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/screen_annotated.png) có **35 marker #1–#35** cho mọi component nhìn thấy trong trạng thái mặc định. Circle đặt sát component/margin để giữ nội dung đọc được.
- [Marker map](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07_markers.json) lưu một ánh xạ duy nhất từ số tới Element ID và tọa độ pixel gốc.
- [Kế hoạch trước DD/annotation](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07_PLAN.md) chứa marker inventory, event plan, source trace và acceptance gates.
- [HTML prototype](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/code.html) là design/mock source, không phải UI runtime.
- Contract Spec modal được `hidden` trong trạng thái ảnh mặc định; modal và controls được mô tả ở phần element/event nhưng không có marker trên ảnh mặc định.

### Trích từ DD nguồn: 6. Đặc tả element

Kích thước/vị trí theo ảnh nguồn 1503×1600. Chỉ marker #1–#35 hiện trên ảnh mặc định; hidden modal có bảng riêng. Điều kiện focus/hover/disabled target tuân theo [Study Web design guide](../../../../../.agents/web-study/design.md), trong khi HTML hiện tại không thực thi toàn bộ accessibility behavior này.

| # / Element ID | Tên, loại, vị trí | Data, validation, constraints | Hiển thị / trạng thái | Event |
|---|---|---|---|---|
| **#1 `SH07-EL-01`** | Brand/logo header, anchor. | Icon + label tĩnh; `href="#"`, `data-path="trang-chu"`; route SH-01 `/` chỉ là proposal. | Visible; hover style. Không có route runtime. | `EV-08` |
| **#2 `SH07-EL-02`** | Primary nav group: Trang chủ/Khóa học/Tìm kiếm. | Ba anchor tĩnh, `href="#"`; proposed targets `/`, `/courses`, `/courses/search`. Không có search/query payload. | Desktop only (`hidden md:flex`); không có menu thay thế ở mobile. | `EV-09` |
| **#3 `SH07-EL-03`** | Link Đăng nhập. | `href="#"`, proposed `/login`; không mang `returnTo` hoặc operation ID. | Visible/hover; focus-visible chưa được source thể hiện. | `EV-09` |
| **#4 `SH07-EL-04`** | CTA Đăng ký. | `href="#"`, proposed `/register`; không gửi form. | Visible/hover. | `EV-09` |
| **#5 `SH07-EL-05`** | Account icon, `div` + icon. | 32×32px; không button/link/role/accessible name/click handler. Không có account data. | Trang trí trong prototype; không mô tả như profile action. | Không có |
| **#6 `SH07-EL-06`** | Specification Gate banner, alert/card ở đầu trang. | Static title, status `D (Design Only)`, `API #18 Blocked`, copy nói server cung cấp Operation ID và nêu UUID/int64 conflict. Không bind runtime status. | Luôn visible trong prototype. Cần Product xác định đây là developer hand-off hay user-facing state; không đưa mock status/environment vào production mà không duyệt. | Không có; state default `DESIGN_GATE` |
| **#7 `SH07-EL-07`** | Button “Xem Contract Spec”. | Button, no payload; toggles `#tech-specs-modal.hidden`. | Visible; hover only. Chưa có dialog semantics/focus handling. | `EV-02` |
| **#8 `SH07-EL-08`** | Breadcrumb `SH-07 / Hạ tầng bất đồng bộ / /operations/:operationId`. | Copy tĩnh; route mẫu. Path parameter name camelCase khác API field `operation_id`. | Visible; breadcrumb segments không phải link trong HTML. | Không có |
| **#9 `SH07-EL-09`** | H1 và supporting description. | Copy tĩnh “Theo dõi Tác vụ Bất đồng bộ” và mô tả lifecycle; không có user/operation data. | Visible. H1/H2 order cần giữ đúng khi triển khai. | Không có |
| **#10 `SH07-EL-10`** | System telemetry badge. | Text `Gated / Unavailable`, red dot; tĩnh, không lấy health API. | Visible; màu có kèm nhãn text. Không được tuyên bố backend health thật. | Không có |
| **#11 `SH07-EL-11`** | Environment badge. | Text `STAGING-MOCK-07`; prototype literal, không config/runtime. | Visible trong mock; ẩn/loại trong production trừ khi có environment contract được duyệt. | Không có |
| **#12 `SH07-EL-12`** | Target Reference Route và Operation ID. | DOM `#param-op-id`; route segment nếu match, nếu không thì UUID fallback giả. Canonical type chưa xác định; không có nguồn producer trong component. | Visible; current mock string. Target chỉ hiển thị ID server-issued và đã qua validation theo contract. | `EV-01` |
| **#13 `SH07-EL-13`** | Copy Operation ID button. | `navigator.clipboard.writeText(innerText)`; không kiểm tra source ID hợp lệ, không có success/error UI. | Visible; target disabled/hidden nếu ID chưa được xác nhận. Accessible name hiện là `title` và icon-only. | `EV-04` |
| **#14 `SH07-EL-14`** | Badge “Chờ tích hợp backend / Gated (Design Only)”. | Static label/icon; không phải operation state. | Visible; error-colored badge. Không map sang FAILED/EXPIRED. | Không có |
| **#15 `SH07-EL-15`** | Metric “Loại tác vụ”. | Text “Đồng bộ thanh toán / Xuất báo cáo”; `ST-06 / AD-25` là mock context; không có `OperationKind` values trong contract. | Visible; target lấy kind đã được schema duyệt; không dùng literal này làm enum. | Không có |
| **#16 `SH07-EL-16`** | Metric “Nguồn gốc khởi tạo”. | Text `Server-Authorized only` / “Client cấm tự cấp phát”; nguyên tắc không tự tạo ID phù hợp mục tiêu, nhưng metric hiện tĩnh. | Visible; không hiển thị `owner_id` hoặc claim. | Không có |
| **#17 `SH07-EL-17`** | Metric “Tiến độ thực thi”. | `Vô hiệu hóa (No Fake %)`; không có numeric progress field trong Operation schema. | Visible, error color + text; không tạo phần trăm giả. | Không có |
| **#18 `SH07-EL-18`** | Anti-faking policy panel và ba guardrail chips. | Tĩnh: không thanh %, không countdown giả, không link download giả. Không chứa API data. | Visible. Đây là prototype guidance; giữ các nguyên tắc chống khẳng định kết quả chưa có evidence. | Không có |
| **#19 `SH07-EL-19`** | CTA “Quay lại danh sách khóa học (GS-01)”. | Anchor `href="#"`, `data-path="khoa-hoc"`; `/courses` là proposal; không có safe-origin input. | Visible; route không hoạt động. Không quay về GS-01 mặc định khi caller là payment/notification/export nếu chưa duyệt. | `EV-07` |
| **#20 `SH07-EL-20`** | CTA “Về trang chủ (SH-01)”. | Anchor `href="#"`, `data-path="trang-chu"`; `/` là proposal. | Visible; không truyền operation/context. | `EV-08` |
| **#21 `SH07-EL-21`** | Developer hand-off heading và badge `ENV: HANDOFF_STRICT`. | Static developer-facing copy/badge; không có role/feature flag. | Visible trong prototype cho mọi người xem; privacy/audience gate chưa có. Block đưa nguyên trạng vào production. | Không có |
| **#22 `SH07-EL-22`** | Developer hand-off paragraph. | Nói route được gọi trực tiếp khi không có status hợp lệ từ API Gateway; đây là prototype explanation, không phải runtime error reason/HTTP behavior. | Visible static. Không show raw URL/error nội bộ cho người dùng. | Không có |
| **#23 `SH07-EL-23`** | Schema conflict code fragment. | HTML ghi expected UUIDv4, “Returned in DB migration: int64/BigInt”, migration v2.4. Current API row int64 nhưng Study migration 009 chỉ có notification `operation_id UUID`, không có generic operation migration/table. Text prototype không được coi là DB evidence. | Visible static diagnostic; chỉ dùng để chỉ ra discrepancy, không copy thành client error/runtime state. | Không có |
| **#24 `SH07-EL-24`** | Lifecycle reference heading/subtitle/icon. | Copy gọi đây là “Hợp đồng Thiết kế”, nhưng không có approved enum registry. | Visible static reference. | Không có |
| **#25 `SH07-EL-25`** | QUEUED reference card. | Copy nói accepted vào RabbitMQ/Redis queue; không có current Study worker/broker evidence. API #63 dùng QUEUED cho notification outbox riêng. | Visible reference card; không phải current operation status. | Không có |
| **#26 `SH07-EL-26`** | RUNNING reference card. | Copy về worker và external I/O; status chưa có trong reusable enum member list (members chưa định nghĩa). | Visible reference card; không phải live state. | Không có |
| **#27 `SH07-EL-27`** | SUCCEEDED reference card. | Copy gợi ý official result/S3 presigned URL; không có generic `result_url` field trong Operation schema. | Visible reference card; không tạo download. | Không có |
| **#28 `SH07-EL-28`** | FAILED reference card. | Copy có `error_code`; schema chỉ có `OperationError {reason,message}` riêng và chưa map vào Operation. | Visible reference card; error contract chưa chốt. | Không có |
| **#29 `SH07-EL-29`** | EXPIRED reference card. | Copy nói retention 24h/15 phút; không có source về TTL, EXPIRED enum hay expiration timestamp. | Visible reference card; không tuyên bố expiration policy. | Không có |
| **#30 `SH07-EL-30`** | Orchestration model heading. | Copy tĩnh, không có architecture source xác nhận API Gateway/queue-worker trong Study. | Visible; diagram conceptual prototype only. | Không có |
| **#31 `SH07-EL-31`** | SVG Client → API Gateway → Queue/Worker diagram. | SVG literals mô tả client no self-ID, auth/dispatch/emit ID, worker lifecycle. Không có endpoint/queue implementation source xác nhận. | Visible; không làm bằng chứng runtime architecture. Decorative SVG cần accessible label hoặc hidden semantics theo design guide. | Không có |
| **#32 `SH07-EL-32`** | Orchestration caption. | Tĩnh: server tạo task, trả ID, client chuyển SH-07; producer responses hiện không đồng nhất như bảng source ở §2. | Visible; không dùng để giải quyết discrepancy. | Không có |
| **#33 `SH07-EL-33`** | Footer brand + descriptor. | Static labels/icons; không phải data operation. | Visible; icon decorative. | Không có |
| **#34 `SH07-EL-34`** | Footer navigation group, bốn anchors. | `href="#"`; labels Chương trình đào tạo, Tra cứu chứng chỉ, Quy chế học vụ, Hỗ trợ học viên; targets chưa được xác nhận. | Visible; source target href không sử dụng được. | `EV-10` |
| **#35 `SH07-EL-35`** | Copyright. | Static `© 2025`. Năm/legal copy chưa có source cập nhật. | Visible. | Không có |

### Modal-only elements (ẩn trong ảnh nguồn mặc định, không có marker)

| Element ID | Thành phần | Current/source state và target constraint |
|---|---|---|
| `SH07-HIDDEN-01` | Dialog `#tech-specs-modal` | Ban đầu có class `hidden`; current div không có `role=dialog`, `aria-modal`, focus trap hoặc focus-return contract. Nếu giữ, dùng semantic dialog và quản lý keyboard/focus theo accessibility requirements đã duyệt. |
| `SH07-HIDDEN-02` | Modal heading, close icon và nút “Đóng cửa sổ” | Hai close handlers thêm class `hidden`; icon button chỉ có title; không có escape/backdrop behavior trong source. Close button event `EV-03`. |
| `SH07-HIDDEN-03` | API #18 sample | Ví dụ có ID UUID “Pending int64 debate”, lowercase status five-value, `operation_type`, `created_at`, `completed_at`, `result_url`, `error`; khác reusable Operation schema (`kind`, `submitted_at`, `updated_at`, `result?:Payment`). Đây là sample không chuẩn hóa. |
| `SH07-HIDDEN-04` | Frontend engineering note | Gợi ý poll 3000ms/backoff hoặc SSE `/operations/{id}/stream`; endpoint/cadence/backoff không có catalog/source approval. Ghi là blocker, không làm implementation instruction. |

## 4. Conditional UI & state variations
- States theo inventory: queued/running/succeeded/failed/expired
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
