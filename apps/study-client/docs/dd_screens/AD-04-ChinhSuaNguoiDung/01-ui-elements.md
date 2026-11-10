# AD-04 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-04_markers.json](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-04-EL-001` | `not supplied in marker JSON` | Study2Work / LMS / Admin Portal brand |
| #2 | `AD-04-EL-002` | `not supplied in marker JSON` | Primary admin navigation group |
| #3 | `AD-04-EL-003` | `not supplied in marker JSON` | System Normal status pill |
| #4 | `AD-04-EL-004` | `not supplied in marker JSON` | Notifications icon |
| #5 | `AD-04-EL-005` | `not supplied in marker JSON` | Admin identity and avatar |
| #6 | `AD-04-EL-006` | `not supplied in marker JSON` | Global breadcrumb trail |
| #7 | `AD-04-EL-007` | `not supplied in marker JSON` | RBAC verification badge |
| #8 | `AD-04-EL-008` | `not supplied in marker JSON` | User management/detail/edit breadcrumb |
| #9 | `AD-04-EL-009` | `not supplied in marker JSON` | Back to AD-03 link |
| #10 | `AD-04-EL-010` | `not supplied in marker JSON` | Record-code badge |
| #11 | `AD-04-EL-011` | `not supplied in marker JSON` | Write-lock / gate active badge |
| #12 | `AD-04-EL-012` | `not supplied in marker JSON` | Page title and subtitle |
| #13 | `AD-04-EL-013` | `not supplied in marker JSON` | API #69/#70 reference card |
| #14 | `AD-04-EL-014` | `not supplied in marker JSON` | ReadOnly Enforcement state |
| #15 | `AD-04-EL-015` | `not supplied in marker JSON` | Update Body Gate warning banner |
| #16 | `AD-04-EL-016` | `not supplied in marker JSON` | API documentation button |
| #17 | `AD-04-EL-017` | `not supplied in marker JSON` | Edit form heading and subtitle |
| #18 | `AD-04-EL-018` | `not supplied in marker JSON` | Target profile heading / Active ID badge |
| #19 | `AD-04-EL-019` | `not supplied in marker JSON` | Edit disabled badge |
| #20 | `AD-04-EL-020` | `not supplied in marker JSON` | Target avatar, name, organization and ID |
| #21 | `AD-04-EL-021` | `not supplied in marker JSON` | Full-name label, input and helper |
| #22 | `AD-04-EL-022` | `not supplied in marker JSON` | Last-edited, actor and compliance metadata |
| #23 | `AD-04-EL-023` | `not supplied in marker JSON` | Email field, readonly badge and helper |
| #24 | `AD-04-EL-024` | `not supplied in marker JSON` | Security and legal rules card heading |
| #25 | `AD-04-EL-025` | `not supplied in marker JSON` | Role select, RBAC schema badge and helper |
| #26 | `AD-04-EL-026` | `not supplied in marker JSON` | Status select and Active badge |
| #27 | `AD-04-EL-027` | `not supplied in marker JSON` | Versioned data-policy notice |
| #28 | `AD-04-EL-028` | `not supplied in marker JSON` | Admin-notes label, textarea and limit badge |
| #29 | `AD-04-EL-029` | `not supplied in marker JSON` | API #69 sync-readiness progress |
| #30 | `AD-04-EL-030` | `not supplied in marker JSON` | API #69 Fetch Account Meta Verified line |
| #31 | `AD-04-EL-031` | `not supplied in marker JSON` | API #70 Body Payload Mutation Locked line |
| #32 | `AD-04-EL-032` | `not supplied in marker JSON` | Internal audit-history note |
| #33 | `AD-04-EL-033` | `not supplied in marker JSON` | RBAC token session claim |
| #34 | `AD-04-EL-034` | `not supplied in marker JSON` | System-policy locked-submit note |
| #35 | `AD-04-EL-035` | `not supplied in marker JSON` | Cancel action |
| #36 | `AD-04-EL-036` | `not supplied in marker JSON` | Save changes button |
| #37 | `AD-04-EL-037` | `not supplied in marker JSON` | Manual unlock/help callout |
| #38 | `AD-04-EL-038` | `not supplied in marker JSON` | Send request button |
| #39 | `AD-04-EL-039` | `not supplied in marker JSON` | Copyright/system footer text |
| #40 | `AD-04-EL-040` | `not supplied in marker JSON` | Privacy/RBAC/support footer links |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Element ID khớp với marker JSON và ảnh chú thích. Các trạng thái dưới đây phân biệt nội dung tĩnh của prototype và behavior dự kiến; copy như “verified”, “85%”, “gate active” không phải server state.

| ID | Element / loại / vị trí | Dữ liệu, thuộc tính, validation | Hiển thị / trạng thái / event |
|---:|---|---|---|
| #1 | Brand Study2Work/LMS/Admin Portal; brand block, header trái. | Text/logo tĩnh; không có API field. | Visible trong prototype; `EV-06`; route brand chưa có source. |
| #2 | Primary admin navigation; nhóm link header. | Nhãn tĩnh; anchor `href="#"`; route đích không xác định. | Visible; click không có điều hướng runtime; `EV-06`. |
| #3 | “SYSTEM NORMAL”; health/status pill header. | Static copy, không có health API #69/#70. | Visible nhưng không phải health state; không gắn API event. |
| #4 | Notifications icon/button header. | Không có count/data source; button không có handler. | Visible, không có state/click effect; `EV-06`. |
| #5 | Admin identity/avatar block, header phải. | Tên/role/avatar hard-coded; #69 trả profile user được xem, không phải admin hiện tại. | Visible; self-profile source ngoài contract này; `EV-06`. |
| #6 | Global breadcrumb trail. | Static labels; fragment placeholder, route ownership chưa xác định. | Visible; no confirmed navigation; `EV-06`. |
| #7 | RBAC verification badge. | Assertion tĩnh. API #69/#70 local guard không chứng minh policy toàn hệ thống. | Visible nhưng không verified; không lấy làm authorization decision. |
| #8 | Breadcrumb quản trị/danh sách/chỉnh sửa. | Label tĩnh; không chứa numeric `user_id` trong link state. | Visible; destination flow cần router contract; `EV-06`. |
| #9 | “Quay lại chi tiết tài khoản (AD-03)”; back link. | Prototype href `/admin/users/USR-9281-VN/details`; không khớp route AD-03 `/admin/users/:userId` hoặc int64 API path. | Visible/enabled trong ảnh; navigation blocker; `EV-04`. |
| #10 | Record-code badge `USR-9281-VN`. | String prototype ID, không có API mapping; #69/#70 nhận numeric signed-int64. | Visible hard-coded; không dùng làm path/body ID; `EV-01`. |
| #11 | “CHẾ ĐỘ KHÓA GHI (GATE ACTIVE)” badge. | Static gate claim; #69/#70 không có gate field/control API. | Visible; không xác minh/không cho phép bật-tắt mutation; `EV-05`. |
| #12 | Page title/subtitle. | Static page copy; không có profile/API field. | Visible; title mô tả chức năng nhưng không đồng nghĩa edit đã enabled. |
| #13 | API #69/#70 reference card. | Static API labels; không phải request telemetry. | Visible; không có call state; API status chỉ lấy từ source/catalog khi viết DD. |
| #14 | ReadOnly Enforcement state. | Static claim; không phản ánh server config hoặc API permission result. | Visible; không quyết định client permission. |
| #15 | Update Body Gate warning banner. | Static explanation/banner; chưa có gate contract. | Visible; prototype state only; `EV-05`. |
| #16 | “Tra cứu tài liệu API” button. | `type=button`; không handler/href. | Visible; không mở tài liệu; destination cần source; `EV-05`. |
| #17 | Form title/subtitle “Biểu mẫu điều chỉnh thông tin”. | Static section title. | Visible; form hiện không editable; không có event độc lập. |
| #18 | Target profile heading / Active ID badge. | Label và badge hard-coded; không lấy active state từ #69. | Visible; profile identity phải map từ #69 sau khi policy duyệt; `EV-01`. |
| #19 | “Vô hiệu hóa chỉnh sửa” badge. | Static copy, không có API flag hoặc client permission source. | Visible; đúng với disabled prototype controls; không được diễn giải là backend gate. |
| #20 | Avatar, tên, tổ chức và ID target profile. | Tên/ID hard-coded; `avatar_url`/`full_name`/`id` có thể map từ #69. Organization không có trong UserProfile. | Visible; #69 load state/error theo `EV-01`; chỉ render source-backed fields. |
| #21 | Full-name label/input/helper. | Prototype input disabled; candidate `full_name:string`, required, trim/nonblank, max 150 theo local #70 `DERIVED`. Helper government-ID assertion không có nguồn. | Disabled hiện tại; chỉ enable sau contract/policy; dirty/validation theo `EV-02`, save theo `EV-03`. |
| #22 | Last-edited, actor và compliance metadata. | `updated_at` có ở #69; actor/SSO và compliance score không có trong UserProfile. | Visible hard-coded; chỉ timestamp có thể map nếu format được duyệt; không gọi là audit; `EV-06`. |
| #23 | Email/read-only field. | Email string từ #69; không writable trong #70; email là PII. | Prototype disabled/read-only; masking/visibility policy open; không gửi trong PUT. |
| #24 | Security/legal rules card heading. | Static copy/heading, không có API field. | Visible; nội dung policy phải được owner xác nhận; `EV-06`. |
| #25 | Role select, RBAC Schema badge, helper. | Prototype options `student/lecturer/admin`; local #70 body allowlist `STUDENT|MENTOR|ADMIN` là `DERIVED`. Transition/self-admin/last-admin rules chưa có. | Disabled hiện tại; không map `lecturer` tự động; enable sau role policy; `EV-02/EV-03`. |
| #26 | Status select và Active badge. | Prototype options `active/locked/pending`; không thuộc #70 update. Status mutation thuộc API #71/AD-05. | Disabled; không đưa vào #70 body; option/lifecycle mapping chưa được duyệt. |
| #27 | Versioned data-policy notice. | Static version/policy text; không có policy version API. | Visible; nội dung cần nguồn owner; `EV-06`. |
| #28 | Admin-notes textarea và 500-char limit. | Static text, textarea disabled; adminNotes không có #69/#70. Max 500 chỉ là mockup assertion, không phải server validation. | Disabled; không lưu/gửi; yêu cầu notes cần contract/retention/PII decision. |
| #29 | API #69 sync-readiness progress, 85%. | Static percentage; #69 GET profile không trả sync percentage. | Visible mockup only; không show như progress data; `EV-06`. |
| #30 | API #69 Fetch Account Meta Verified line. | Static assertion; không có per-screen verification telemetry. | Visible mockup only; không phải event result. |
| #31 | API #70 Body Payload Mutation Locked line. | Static assertion; local PUT route tồn tại, nhưng route không dùng screen gate. | Visible mockup only; không chứng minh API mutation lock. |
| #32 | Internal audit-history note. | Audit claim; #69/#70 không trả audit rows hoặc ghi audit event. | Visible; không khẳng định log đã lưu; audit source/retention blocker; `EV-06`. |
| #33 | RBAC token session claim. | Static token validity/level; role update hiện không revoke access JWT. | Visible mockup only; không thay auth check; token effects cần security owner. |
| #34 | System-policy locked-submit note. | Static message; no gate/policy API. | Visible; Save thật vẫn disabled do prototype; `EV-05`. |
| #35 | Cancel button/anchor. | Prototype href `/admin/users`; intended destination AD-03 with same numeric ID per flow. Dirty confirmation/preservation policy unknown. | Visible/enabled; route mismatch; `EV-04`. |
| #36 | Save changes button. | Button disabled; no handler. If enabled after approval, send exact approved #70 body only. | Disabled; no loading/success/error state in prototype; `EV-03`. |
| #37 | Manual unlock/help callout. | Static callout “Cần mở khóa thủ công?”; no support/ticket API. | Visible; no state/workflow source; `EV-05`. |
| #38 | “Gửi yêu cầu” button. | Button without handler; no endpoint, ticket schema, destination or idempotency rule. | Visible but no operation; do not invent submit flow; `EV-05`. |
| #39 | Copyright/system footer text. | Static text `© 2025 Study2Work LMS`; no data source. | Visible; no event. |
| #40 | Privacy/RBAC/support footer links. | `href="#"` placeholders; destinations not defined. | Visible; no router/handlers; `EV-06`. |

## 4. Conditional UI & state variations
- States theo inventory: loading/ready/dirty/saving/validation-error/unauthenticated/forbidden/not-found/saved-refresh-error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
