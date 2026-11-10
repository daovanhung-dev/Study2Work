# AD-23 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-23_markers.json](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/AD-23_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-23-EL-001` | `AD23-EL-01` | Study2Work brand / portal mark |
| #2 | `AD-23-EL-002` | `AD23-EL-02` | Navigation: Tổng quan |
| #3 | `AD-23-EL-003` | `AD23-EL-03` | Navigation: Người dùng |
| #4 | `AD-23-EL-004` | `AD23-EL-04` | Navigation: Khóa học & Nội dung |
| #5 | `AD-23-EL-005` | `AD23-EL-05` | Navigation: Kiểm duyệt |
| #6 | `AD-23-EL-006` | `AD23-EL-06` | Navigation: Báo cáo |
| #7 | `AD-23-EL-007` | `AD23-EL-07` | System Normal status |
| #8 | `AD-23-EL-008` | `AD23-EL-08` | Notifications bell |
| #9 | `AD-23-EL-009` | `AD23-EL-09` | Admin identity/avatar |
| #10 | `AD-23-EL-010` | `AD23-EL-10` | Global breadcrumb |
| #11 | `AD-23-EL-011` | `AD23-EL-11` | RBAC verification badge |
| #12 | `AD-23-EL-012` | `AD23-EL-12` | Local moderation breadcrumb |
| #13 | `AD-23-EL-013` | `AD23-EL-13` | Return-to-AD-22 header button |
| #14 | `AD-23-EL-014` | `AD23-EL-14` | Screen title |
| #15 | `AD-23-EL-015` | `AD23-EL-15` | Target discussion panel heading/icon |
| #16 | `AD-23-EL-016` | `AD23-EL-16` | Target load-status badge |
| #17 | `AD-23-EL-017` | `AD23-EL-17` | Discussion ID summary card |
| #18 | `AD-23-EL-018` | `AD23-EL-18` | Course summary card |
| #19 | `AD-23-EL-019` | `AD23-EL-19` | Author summary card |
| #20 | `AD-23-EL-020` | `AD23-EL-20` | Discussion status summary card |
| #21 | `AD-23-EL-021` | `AD23-EL-21` | Audit/policy banner icon |
| #22 | `AD-23-EL-022` | `AD23-EL-22` | Audit/policy banner heading |
| #23 | `AD-23-EL-023` | `AD23-EL-23` | Audit/policy banner copy |
| #24 | `AD-23-EL-024` | `AD23-EL-24` | Thread panel heading/icon |
| #25 | `AD-23-EL-025` | `AD23-EL-25` | Thread display-mode badge |
| #26 | `AD-23-EL-026` | `AD23-EL-26` | Empty-thread icon |
| #27 | `AD-23-EL-027` | `AD23-EL-27` | Empty-thread title |
| #28 | `AD-23-EL-028` | `AD23-EL-28` | Empty-thread explanatory copy |
| #29 | `AD-23-EL-029` | `AD23-EL-29` | Empty-thread return-to-AD-22 CTA |
| #30 | `AD-23-EL-030` | `AD23-EL-30` | Moderation action panel heading/icon |
| #31 | `AD-23-EL-031` | `AD23-EL-31` | Safety-lock badge |
| #32 | `AD-23-EL-032` | `AD23-EL-32` | Action-group label |
| #33 | `AD-23-EL-033` | `AD23-EL-33` | Hide-temporarily option card |
| #34 | `AD-23-EL-034` | `AD23-EL-34` | Lock-comments option card |
| #35 | `AD-23-EL-035` | `AD23-EL-35` | Warn-author option card |
| #36 | `AD-23-EL-036` | `AD23-EL-36` | Permanent-delete option card |
| #37 | `AD-23-EL-037` | `AD23-EL-37` | Reason input label |
| #38 | `AD-23-EL-038` | `AD23-EL-38` | Disabled reason textarea |
| #39 | `AD-23-EL-039` | `AD23-EL-39` | Audit-note copy |
| #40 | `AD-23-EL-040` | `AD23-EL-40` | Disabled apply-decision button |
| #41 | `AD-23-EL-041` | `AD23-EL-41` | Cancel/return link |
| #42 | `AD-23-EL-042` | `AD23-EL-42` | Footer copyright |
| #43 | `AD-23-EL-043` | `AD23-EL-43` | Footer privacy link |
| #44 | `AD-23-EL-044` | `AD23-EL-44` | Footer RBAC standards link |
| #45 | `AD-23-EL-045` | `AD23-EL-45` | Footer support link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Coordinates below are marker centers in original `screen.png` pixels. Marker IDs in the image, JSON and table are one-to-one. “Prototype state” describes only the static HTML; future states are not implied.

| Marker / Element ID | Tên, loại, vị trí và mục đích | Thuộc tính / nguồn / điều kiện và trạng thái | Sự kiện |
|---|---|---|---|
| #1 / AD23-EL-01 | Study2Work brand / logo, shell link, top-left. | Logo text/image is static; `href="#"`. Visible; no route target. | EV-09 |
| #2 / AD23-EL-02 | Nav “Tổng quan”, anchor, header. | Static label; `href="#"`; no active route behavior evidenced. | EV-09 |
| #3 / AD23-EL-03 | Nav “Người dùng”, anchor, header. | Static label; `href="#"`; no route behavior. | EV-09 |
| #4 / AD23-EL-04 | Nav “Khóa học & Nội dung”, anchor, header. | Static label; `href="#"`; no route behavior. | EV-09 |
| #5 / AD23-EL-05 | Nav “Kiểm duyệt”, anchor, header. | Static label; `href="#"`; no route behavior. | EV-09 |
| #6 / AD23-EL-06 | Nav “Báo cáo”, anchor, header. | Static label; `href="#"`; no route behavior. | EV-09 |
| #7 / AD23-EL-07 | “System Normal” status badge, header. | Static status text; no health source or live status feed. Read-only visual badge. | — |
| #8 / AD23-EL-08 | Notification bell, button/icon, header. | No handler or notification data source. Click outcome is not implemented. | EV-09 |
| #9 / AD23-EL-09 | Admin identity/avatar, header. | Static “Admin / Quản trị viên” display; current identity source/session binding is not present in prototype. | — |
| #10 / AD23-EL-10 | Global breadcrumb, shell. | Static breadcrumb text; individual navigation targets are not established by the prototype. | EV-09 |
| #11 / AD23-EL-11 | “Chuẩn xác thực RBAC” badge, shell. | Static copy, not authorization evidence. No permission query/source in HTML. | — |
| #12 / AD23-EL-12 | Local moderation breadcrumb, page header. | Static “Kiểm duyệt cộng đồng > Thảo luận bị báo cáo > Điều tra kiểm duyệt”; no route links are wired. | — |
| #13 / AD23-EL-13 | “Quay lại hàng đợi báo cáo (AD-22)” header button. | Button-like anchor to `#ad-22`; intended destination is AD-22, actual browser behavior stays within fragment. | EV-02 |
| #14 / AD23-EL-14 | Page title, heading. | Static text “Thẩm định và xử lý vi phạm nội dung thảo luận”; no bound data. | — |
| #15 / AD23-EL-15 | Target Discussion panel heading/icon. | Static “Đối chiếu chủ đề mục tiêu” card heading. | — |
| #16 / AD23-EL-16 | Target load-status badge. | Static “Chờ nạp bản ghi”; does not indicate an actual request/loading state. | — |
| #17 / AD23-EL-17 | Discussion ID summary card. | Displays “Chưa nạp tham số ID hợp lệ”; no ID in page state/URL is wired. Expected #98 path requires int64; no default ID. | EV-01 |
| #18 / AD23-EL-18 | Course summary card. | Placeholder `--`; no course field is returned by the visible summary. Current #98 projection has `course_id`, but no screen binding. | EV-01 |
| #19 / AD23-EL-19 | Author summary card. | Placeholder `--`; current #98 maps an author for Discussion/comments, but no frontend binding exists. | EV-01 |
| #20 / AD23-EL-20 | Discussion status summary card. | Placeholder `--`; current #98 projects `status`; no UI mapping/status vocabulary is approved here. | EV-01 |
| #21 / AD23-EL-21 | Audit/policy banner icon. | Static icon only. Does not prove a persistent audit mechanism exists. | — |
| #22 / AD23-EL-22 | Audit/policy banner heading. | Static integrity/policy claim. No source event store is connected. | — |
| #23 / AD23-EL-23 | Audit/policy banner copy. | States detail is unloaded and intervention is safety-locked while audit is standardized. Static copy; not response from a backend. | — |
| #24 / AD23-EL-24 | Thread panel heading/icon. | Static “Luồng thảo luận điều tra” label. | — |
| #25 / AD23-EL-25 | “Khung hiển thị” mode badge. | Static badge; no layout mode/state control. | — |
| #26 / AD23-EL-26 | Empty-thread icon. | Decorative icon for no selected/loaded content. No thread records in prototype. | — |
| #27 / AD23-EL-27 | Empty-thread title. | Static “Chưa chọn nội dung thẩm định”; no selection state source. | — |
| #28 / AD23-EL-28 | Empty-thread explanatory copy. | Instructs selecting a row from AD-22 to display thread and flag reason. Current #98 does not return report reason. | — |
| #29 / AD23-EL-29 | Open AD-22 CTA, button-like anchor. | `href="#ad-22"`; no actual router state or filter/page restoration. | EV-03 |
| #30 / AD23-EL-30 | Moderation action panel heading/icon. | Static “Hành động kiểm duyệt”. No action request state. | — |
| #31 / AD23-EL-31 | “Đã khóa an toàn” badge. | Static safety-lock claim; consistent with disabled controls but not tied to server state. | — |
| #32 / AD23-EL-32 | Action group label. | Static “Biện pháp xử lý vi phạm áp dụng”. No selected value/default. | — |
| #33 / AD23-EL-33 | “Ẩn nội dung tạm thời” option card, disabled radio. | Radio `name="moderation_action"`, disabled, no value. Logical hide action appears in AC; exact #99 token/state is undefined. | EV-04 |
| #34 / AD23-EL-34 | “Khóa bình luận” option card, disabled radio. | Disabled, no value. AC says lock at logical level; exact target and state mapping unresolved. | EV-04 |
| #35 / AD23-EL-35 | “Cảnh cáo tác giả” option card, disabled radio. | Disabled, no value. AC says warn at logical level; delivery channel/text and action token unresolved. | EV-04 |
| #36 / AD23-EL-36 | “Xóa bài đăng vĩnh viễn” option card, disabled radio. | Disabled, no value. Conflicts with AC's separate conditional #100 soft-delete/audit flow. Must not submit via #99. | EV-04; EV-07 |
| #37 / AD23-EL-37 | Reason label, textarea label. | Static instruction says reason is recorded in audit log; persistence is not source-backed. Catalog #99 requires `reason:string!`, but purpose/constraints need approval. | EV-05 |
| #38 / AD23-EL-38 | Reason textarea, disabled input. | Disabled; placeholder asks for valid Discussion ID before entering a record. No value/default, length, whitespace rule or validation is specified. | EV-05 |
| #39 / AD23-EL-39 | Audit-note copy. | Static claim of automatic audit record and administrator ID; actor mapping, storage, atomicity and retention are unresolved. | — |
| #40 / AD23-EL-40 | “Áp dụng quyết định kiểm duyệt” button, disabled. | Disabled; no submit handler/form. Candidate #99 requires `action` and `reason`; no request can be constructed from current controls. | EV-06 |
| #41 / AD23-EL-41 | “Hủy bỏ và quay lại” anchor/button. | `href="#ad-22"`; no unsaved decision state or confirmation. | EV-08 |
| #42 / AD23-EL-42 | Footer copyright text. | Static text; no behavior. | — |
| #43 / AD23-EL-43 | Footer privacy link. | Static anchor `href="#"`; no target route. | EV-09 |
| #44 / AD23-EL-44 | Footer RBAC standards link. | Static anchor `href="#"`; no target route or permission documentation binding. | EV-09 |
| #45 / AD23-EL-45 | Footer support link. | Static anchor `href="#"`; no target route. | EV-09 |

## 4. Conditional UI & state variations
- States theo inventory: loading/reviewing/processing/resolved/conflict
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-23_dieu-tra-kiem-duyet-thao-luan/AD-23.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
