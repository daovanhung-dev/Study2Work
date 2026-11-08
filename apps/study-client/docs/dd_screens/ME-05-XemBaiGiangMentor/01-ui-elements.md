# ME-05 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ME-05_markers.json](../../screen_stitch/04_mentor/ME-05_xem-bai-giang-mentor/ME-05_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ME-05-EL-001` | `ME05-EL-01` | Brand Study2Work Mentor Portal |
| #2 | `ME-05-EL-002` | `ME05-EL-02` | Điều hướng Mentor toàn cục |
| #3 | `ME-05-EL-003` | `ME05-EL-03` | Ô tìm kiếm header |
| #4 | `ME-05-EL-004` | `ME05-EL-04` | Thông báo và badge đếm mẫu |
| #5 | `ME-05-EL-005` | `ME05-EL-05` | Tài khoản Mentor hiển thị |
| #6 | `ME-05-EL-006` | `ME05-EL-06` | Breadcrumb về danh sách khóa học |
| #7 | `ME-05-EL-007` | `ME05-EL-07` | Breadcrumb Workspace course |
| #8 | `ME-05-EL-008` | `ME05-EL-08` | Badge trạng thái lecture |
| #9 | `ME-05-EL-009` | `ME05-EL-09` | Mã lecture mẫu |
| #10 | `ME-05-EL-010` | `ME05-EL-10` | Nhãn tác giả mẫu |
| #11 | `ME-05-EL-011` | `ME05-EL-11` | Tiêu đề lecture |
| #12 | `ME-05-EL-012` | `ME05-EL-12` | Action Sao chép liên kết |
| #13 | `ME-05-EL-013` | `ME05-EL-13` | Action Xem trước ST-11 |
| #14 | `ME-05-EL-014` | `ME05-EL-14` | Action Đổi trạng thái |
| #15 | `ME-05-EL-015` | `ME05-EL-15` | Action Chỉnh sửa bài giảng |
| #16 | `ME-05-EL-016` | `ME05-EL-16` | Player video-looking và controls mẫu |
| #17 | `ME-05-EL-017` | `ME05-EL-17` | Dải mốc thời gian/chapter |
| #18 | `ME-05-EL-018` | `ME05-EL-18` | Ghi chú học thuật |
| #19 | `ME-05-EL-019` | `ME05-EL-19` | Action sao chép code mẫu |
| #20 | `ME-05-EL-020` | `ME05-EL-20` | Khối code mẫu |
| #21 | `ME-05-EL-021` | `ME05-EL-21` | Panel tài liệu đính kèm |
| #22 | `ME-05-EL-022` | `ME05-EL-22` | Action Tải xuống PDF |
| #23 | `ME-05-EL-023` | `ME05-EL-23` | Action Mở xem PDF |
| #24 | `ME-05-EL-024` | `ME05-EL-24` | Link GitHub mẫu |
| #25 | `ME-05-EL-025` | `ME05-EL-25` | Panel analytics mẫu |
| #26 | `ME-05-EL-026` | `ME05-EL-26` | Panel thảo luận bài học mẫu |
| #27 | `ME-05-EL-027` | `ME05-EL-27` | Action Trả lời ngay |
| #28 | `ME-05-EL-028` | `ME05-EL-28` | Link Xem tất cả thảo luận ST-25 |
| #29 | `ME-05-EL-029` | `ME05-EL-29` | Panel cấu trúc khóa học |
| #30 | `ME-05-EL-030` | `ME05-EL-30` | Row bài học trước |
| #31 | `ME-05-EL-031` | `ME05-EL-31` | Row bài giảng đang chọn |
| #32 | `ME-05-EL-032` | `ME05-EL-32` | Row bài học tiếp theo |
| #33 | `ME-05-EL-033` | `ME05-EL-33` | Footer thông tin và liên kết |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 3. Element specification — 33 markers

Marker coordinates are source-image pixels with origin at top-left. Every marker ID below appears exactly once in `ME-05_markers.json`, the SVG overlay and `screen_annotated.png`.

| # / Element ID | Name, type, location | Data, default/validation, visibility/state | Event/result |
|---|---|---|---|
| 1 `ME05-EL-01` | Brand/logo and Mentor Portal link; header left. | Static shell copy; no API field. Visible in mockup. | EV-20; `href="#"`, destination unresolved. |
| 2 `ME05-EL-02` | Global Mentor navigation links. | Static labels Dashboard, courses, grading, support, notifications. No route map in HTML. | EV-20; links are `#`, no navigation wired. |
| 3 `ME05-EL-03` | Header search input. | Text input, placeholder for learners/assignments; no default, max length, query/API contract or submit action specified. | EV-21; typing/search result behavior unwired. |
| 4 `ME05-EL-04` | Notification icon and badge. | Badge `3` is sample content; no notification response/state source in ME-05. | EV-22; open/list/read action not wired here. |
| 5 `ME05-EL-05` | Mentor avatar/name/role block. | `TS. Trần Hoàng Long` and role label are sample static text; not returned by #48. | EV-23; account menu/sign-out behavior not present. |
| 6 `ME05-EL-06` | Breadcrumb “Khóa học phụ trách”. | Course list destination expected ME-02; current href `#`. | EV-03; route and preserved return context unresolved. |
| 7 `ME05-EL-07` | Breadcrumb Workspace course. | Course code/title are sample; #48 only provides `course_id`, not displayed course name/code. | EV-04; ME-03 destination needs route resolution by numeric course ID. |
| 8 `ME05-EL-08` | Lecture status badge. | Candidate source `data.status`; exact display labels/colors for all status values are not defined. `DELETED` is not returned by #48. | Read-only; status action is separately #14 and blocked. |
| 9 `ME05-EL-09` | Lecture identifier chip. | Candidate `data.id:int64`; `#LEC-8910` is sample formatting, no prefix/display format contract. | Read-only; no copy semantics specified. |
| 10 `ME05-EL-10` | Author label. | Screenshot names a Mentor; #48 response has no `author` or Mentor profile. Do not derive identity from title or client token. | Read-only; source required. |
| 11 `ME05-EL-11` | Lecture title. | `data.title:string` from `lessons.name`; API #47 requires title length ≤200 on create. #48 has no edit validation. | Read-only mapping; actual title comes from #48, not sample text. |
| 12 `ME05-EL-12` | “Sao chép liên kết” button. | No default route/share token or clipboard logic. | EV-05; route canonicalization and clipboard success/error feedback need decision. |
| 13 `ME05-EL-13` | “Xem trước ST-11” button. | Cross-link to Student screen in mockup; #48 gives no preview token/access rule. | EV-06; preview/Student authorization path is blocked. |
| 14 `ME05-EL-14` | “Đổi trạng thái” menu button. | #48 is GET only; `data.status` is display value. No Mentor mutation endpoint in this flow. | EV-07; do not enable or call invented endpoint. |
| 15 `ME05-EL-15` | “Chỉnh sửa bài giảng” button. | No Mentor lecture update endpoint in ME-05 inventory/API #48. | EV-08; disabled/removed until API and route are approved. |
| 16 `ME05-EL-16` | Video-looking player, overlay transcript and controls. | Mocked poster, media URL/codec, transcript, caption, time/duration, volume, speed, watermark and fullscreen states have no #48 source; HTML contains no `<video>`/`source`. | EV-09; play/pause/seek/volume/speed/caption/fullscreen are visual only. Media contract is a blocker. |
| 17 `ME05-EL-17` | Chapter/timeline quick-jump strip. | Three labels/time ranges in screenshot are sample; #48 returns no chapter list, start/end time, watched state or seek URL. | EV-10; chapter selection cannot seek without media/chapter contract. |
| 18 `ME05-EL-18` | Academic notes/architecture text panel. | Candidate `data.content:string|null`, but current #47 stores decimal text from int64. Formatting, sanitization, empty/null fallback and Markdown support unresolved. | Read-only candidate; do not render mock prose as loaded data. |
| 19 `ME05-EL-19` | Copy code icon/button. | Copies hardcoded code in mockup; #48 has no `code_sample` field. | EV-11; source selection, clipboard API and feedback need approval. |
| 20 `ME05-EL-20` | TypeScript code snippet block. | Hardcoded example, syntax/language not from #48. No line-count/wrapping contract. | Read-only sample only; hide until source is approved. |
| 21 `ME05-EL-21` | Resources/attachments panel. | Map only #48 `data.assets[]`; no links => valid empty array. Asset fields include `name`, `url`, `content_type`, `size_bytes`, `status`. No MIME allowlist. | Read-only list; asset presentation/empty-state design open. |
| 22 `ME05-EL-22` | “Tải xuống” asset action. | Candidate file metadata from #21; #48 URL may be a public URL produced by #34, but provider reachability/access not verified. | EV-12; download authorization, disposition, progress/failure behavior unresolved. |
| 23 `ME05-EL-23` | “Mở xem PDF” action. | Mockup label assumes PDF; `content_type` may be other MIME and no viewer contract exists. | EV-13; validate MIME and decide viewer/target policy before enabling. |
| 24 `ME05-EL-24` | “Mở GitHub” external link. | Repository/branch/clone text is sample and absent from #48 assets unless an asset link is separately confirmed. | EV-14; no external URL source/allowlist. |
| 25 `ME05-EL-25` | Analytics panel and chart. | Views, retention, duration, rating/votes, dropout chart and “realtime” badge are not #48 fields; shown values are mock data. | EV-15; hide until a source/metric definition is assigned. |
| 26 `ME05-EL-26` | Lesson discussion preview cards. | Author, question/answer text, timestamps, likes and reply state absent from #48. | EV-16; discussion model/API and privacy policy missing. |
| 27 `ME05-EL-27` | “Trả lời ngay” action. | Needs discussion ID and Mentor reply contract; neither is in #48. | EV-16; no navigation or mutation is wired. |
| 28 `ME05-EL-28` | “Xem tất cả 8 thảo luận (ST-25)” link. | Count and ST-25 label are sample; ST-25 is Student-facing in inventory, not an approved Mentor destination. | EV-17; product must specify Mentor discussion route/access. |
| 29 `ME05-EL-29` | Course structure panel. | Chapter name/outline and current content absent from #48. ME-06/#49 is a separate content-tree flow. | EV-18; clarify whether this screen embeds ME-06 or just links to it. |
| 30 `ME05-EL-30` | Previous lesson row. | Lesson title/order/status are sample; no predecessor list or course curriculum in #48. | EV-18; no link target can be derived. |
| 31 `ME05-EL-31` | Selected lesson row. | Selected styling is mockup state; #48 gives current lecture `id/course_id/order`, not a full tree. | EV-18; selection state is route-derived only after route design. |
| 32 `ME05-EL-32` | Next lesson row. | Lesson title/type/duration/next ID are sample and not #48 fields. | EV-18; no next-lesson navigation contract. |
| 33 `ME05-EL-33` | Footer brand, policy and support links. | Static copy and `href="#"`; no route/support destination in this mockup. | EV-20; destinations not wired. |

## 4. Conditional UI & state variations
- States theo inventory: loading/ready/not-found
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/04_mentor/ME-05_xem-bai-giang-mentor/ME-05.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
