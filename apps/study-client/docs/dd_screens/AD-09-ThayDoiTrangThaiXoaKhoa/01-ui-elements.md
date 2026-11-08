# AD-09 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-09_markers.json](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/AD-09_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-09-EL-001` | `not supplied in marker JSON` | Study2Work LMS Admin brand |
| #2 | `AD-09-EL-002` | `not supplied in marker JSON` | Admin navigation: Tổng quan |
| #3 | `AD-09-EL-003` | `not supplied in marker JSON` | Admin navigation: Người dùng |
| #4 | `AD-09-EL-004` | `not supplied in marker JSON` | Active Admin navigation: Khóa học & Nội dung |
| #5 | `AD-09-EL-005` | `not supplied in marker JSON` | Admin navigation: Kiểm duyệt |
| #6 | `AD-09-EL-006` | `not supplied in marker JSON` | Admin navigation: Báo cáo |
| #7 | `AD-09-EL-007` | `not supplied in marker JSON` | Static SYSTEM NORMAL badge |
| #8 | `AD-09-EL-008` | `not supplied in marker JSON` | Notifications button without handler |
| #9 | `AD-09-EL-009` | `not supplied in marker JSON` | Static Admin identity and avatar |
| #10 | `AD-09-EL-010` | `not supplied in marker JSON` | Global breadcrumb trail |
| #11 | `AD-09-EL-011` | `not supplied in marker JSON` | Static RBAC assurance badge |
| #12 | `AD-09-EL-012` | `not supplied in marker JSON` | Local course-management breadcrumb trail |
| #13 | `AD-09-EL-013` | `not supplied in marker JSON` | Static API #74/#76/#77 gate-policy line |
| #14 | `AD-09-EL-014` | `not supplied in marker JSON` | Back-to-detail link; href targets course list |
| #15 | `AD-09-EL-015` | `not supplied in marker JSON` | Static safety-shield icon |
| #16 | `AD-09-EL-016` | `not supplied in marker JSON` | Status/delete coordination heading |
| #17 | `AD-09-EL-017` | `not supplied in marker JSON` | Static safe-protection gate badge |
| #18 | `AD-09-EL-018` | `not supplied in marker JSON` | Static action-page description |
| #19 | `AD-09-EL-019` | `not supplied in marker JSON` | Target coordination information card heading |
| #20 | `AD-09-EL-020` | `not supplied in marker JSON` | Static automatic RBAC comparison badge |
| #21 | `AD-09-EL-021` | `not supplied in marker JSON` | Target Course card; prototype says none selected |
| #22 | `AD-09-EL-022` | `not supplied in marker JSON` | Current status card; prototype says undetermined |
| #23 | `AD-09-EL-023` | `not supplied in marker JSON` | Static enrollment-constraint warning |
| #24 | `AD-09-EL-024` | `not supplied in marker JSON` | Action-selector legend and single-choice note |
| #25 | `AD-09-EL-025` | `not supplied in marker JSON` | Draft action radio option; default checked |
| #26 | `AD-09-EL-026` | `not supplied in marker JSON` | Archive action radio option |
| #27 | `AD-09-EL-027` | `not supplied in marker JSON` | Permanent-delete action radio option |
| #28 | `AD-09-EL-028` | `not supplied in marker JSON` | Reason label, required cue and ISO claim |
| #29 | `AD-09-EL-029` | `not supplied in marker JSON` | Disabled audit-reason textarea and lock |
| #30 | `AD-09-EL-030` | `not supplied in marker JSON` | Static reason-disabled helper copy |
| #31 | `AD-09-EL-031` | `not supplied in marker JSON` | Static data-protection policy card |
| #32 | `AD-09-EL-032` | `not supplied in marker JSON` | Cancel and return link |
| #33 | `AD-09-EL-033` | `not supplied in marker JSON` | Disabled Confirm action button |
| #34 | `AD-09-EL-034` | `not supplied in marker JSON` | Static data-retention safeguard footer claim |
| #35 | `AD-09-EL-035` | `not supplied in marker JSON` | Footer copyright notice |
| #36 | `AD-09-EL-036` | `not supplied in marker JSON` | Data privacy footer link |
| #37 | `AD-09-EL-037` | `not supplied in marker JSON` | RBAC standards footer link |
| #38 | `AD-09-EL-038` | `not supplied in marker JSON` | System technical support footer link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Tọa độ marker theo `screen.png` 1538×1600. Static copy/value là current prototype content, không phải backend data. Events EV-01…EV-06 được mô tả ở phần D.

| ID | Element / vị trí / mục đích | Thuộc tính, nguồn dữ liệu, validation | Hiển thị / trạng thái | Event |
|---:|---|---|---|---|
| #1 | Admin brand/logo, top left; nhận diện portal. | Static Study2Work LMS/Admin Portal identity. | Visible; static. | EV-06; no wired route. |
| #2 | Nav “Tổng quan”, header. | Anchor `href="#"`; destination not defined. | Visible; inactive. | EV-06. |
| #3 | Nav “Người dùng”, header. | Anchor `href="#"`. | Visible; inactive. | EV-06. |
| #4 | Nav “Khóa học & Nội dung”, header. | Active-style anchor `href="#"`; style only. | Visible; highlighted. | EV-06; no route. |
| #5 | Nav “Kiểm duyệt”, header. | Anchor `href="#"`. | Visible; inactive. | EV-06. |
| #6 | Nav “Báo cáo”, header. | Anchor `href="#"`. | Visible; inactive. | EV-06. |
| #7 | `SYSTEM NORMAL` badge. | Hard-coded status; no health endpoint/telemetry. | Visible; static badge. | EV-06; no polling. |
| #8 | Notification bell button. | Button with accessible label in HTML; no handler/state/API. | Visible; no-handler. | EV-06. |
| #9 | Admin name/role/avatar. | Static display, not read from auth session/current-user API. | Visible; static. | EV-06; no profile menu. |
| #10 | Global breadcrumb trail. | Static house and location text; not bound to router. | Visible. | EV-06. |
| #11 | “Chuẩn xác thực RBAC” badge. | Static assurance copy/icon; not an authorization result. | Visible; static. | EV-06. |
| #12 | Local course-management breadcrumbs. | Static `Quản trị đào tạo > Danh sách khóa học > Điều phối trạng thái khóa học`. | Visible; labels not route-bound here. | EV-05/EV-06. |
| #13 | `API GATE POLICY #74 • #76 • #77 • PROTECTION LOCK ENABLED`. | Static uppercase policy line; no live gate/lock call. | Visible; static. | EV-06. |
| #14 | Back-to-detail AD-07 link. | Anchor `/admin/courses` despite copy “quay lại chi tiết khóa học (AD-07)”. | Visible; enabled native link; destination mismatch. | EV-05. |
| #15 | Shield icon in action card. | Decorative visual only. | Visible. | No event. |
| #16 | “Điều phối trạng thái và gỡ bỏ khóa học” heading. | Static page/card title. | Visible; heading. | No event. |
| #17 | “CỔNG BẢO VỆ AN TOÀN” badge. | Static security claim; no auth/API state. | Visible; static. | EV-06. |
| #18 | Subtitle describing public/draft/archive/delete. | Static summary names publication, draft, archive or remove actions. Current #76 candidate enum lacks ARCHIVED; #77 is soft-delete. | Visible; static with API discrepancy. | EV-02/EV-06. |
| #19 | Target coordination card title. | Static “Thông tin mục tiêu điều phối”. | Visible. | No event. |
| #20 | “Tự động đối chiếu RBAC” badge. | Static RBAC assertion; local APIs do not provide this UI signal. | Visible; unverified. | EV-06. |
| #21 | Target Course info box. | Static target label; value says “Chưa chọn khóa học”; no route ID/data binding. | Visible; empty state in prototype. | EV-01 target; currently no load. |
| #22 | Current Course status box. | Static `Chưa xác định`; no #74 mapping. | Visible; unknown placeholder. | EV-01/EV-02 target. |
| #23 | Enrollment constraint warning. | Static advice to check enrolled learner count; #74 has no counter and #77 checks any enrollment row locally. | Visible; static; server is actual local check authority. | EV-04 target; no client check source. |
| #24 | Action selector legend + one-choice cue. | Fieldset/legend; text says choose one option. | Visible. | EV-02. |
| #25 | “Chuyển sang Bản nháp” radio. | Native `input[type=radio]`, `name=course_action`, value `draft`, initially `checked`; description says hide public search and close new enrollment. Those side effects are not defined by #76. | Visible; enabled in prototype; checked by default. | EV-02 only; no mutation. |
| #26 | “Lưu trữ khóa học” radio. | Native radio value `archive`; copy says stop new registration and preserve access. No ARCHIVED status in #76 candidate. | Visible; unselected. | EV-02 only; no approved API mapping. |
| #27 | “Xóa vĩnh viễn khóa học” radio. | Native radio value `delete`; copy says irreversible DB operation. Local #77 is soft-delete and dependency-conditional. | Visible; unselected; destructive styling. | EV-02 only; no #77 call. |
| #28 | Reason label, required marker and ISO-27001 claim. | Static `required` and compliance copy; reason absent from #76 candidate body, #76 audit row and #77. | Visible; unsupported policy claim. | No API event. |
| #29 | Audit-reason textarea + lock. | HTML textarea `disabled`, `id=audit_reason`, `rows=3`; no length/format rule. | Visible; Disabled. | No input event; not sent. |
| #30 | Text saying reason is disabled with system lock. | Static helper copy, no gate API. | Visible; static. | EV-06. |
| #31 | Data-protection policy card. | Static claim deletion disabled to preserve progress/credentials; no matching product policy source in #77. | Visible; static/unverified. | EV-06. |
| #32 | “Hủy và quay lại” link. | Anchor `/admin/courses`; no dirty-state guard or return ID. | Visible; enabled native link to proposed AD-06 list. | EV-05. |
| #33 | “Xác nhận áp dụng” button. | `type=button`, `disabled`, lock icon; no handler. | Visible; Disabled. | EV-03/EV-04 target only after API/policy approval. |
| #34 | Data-safeguard footer claim. | Static statement about lifetime academic-data retention; no endpoint/policy source. | Visible; static/unverified. | EV-06. |
| #35 | Footer copyright. | Static 2025 copyright text. | Visible. | No event. |
| #36 | Privacy-policy footer link. | Anchor `href="#"`; destination absent. | Visible. | EV-06. |
| #37 | RBAC standards footer link. | Anchor `href="#"`; destination absent. | Visible. | EV-06. |
| #38 | Technical-support footer link. | Anchor `href="#"`; destination absent. | Visible. | EV-06. |

**Element/event note:** The page is a static design artifact. Radio selection can change natively in the standalone HTML, and the registered listener is intentionally empty; that behavior is not Study Web runtime implementation. API status, RBAC, enrollment checks, audit and retention are not supplied to this UI by current source.

## 4. Conditional UI & state variations
- States theo inventory: confirm/working/conflict/done
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/AD-09.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
