# ST-25 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-25_markers.json](../../screen_stitch/03_student/ST-25_chi-tiet-thread-va-phan-hoi/ST-25_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-25-EL-001` | `ST25-EL-01` | Study2Work logo / brand |
| #2 | `ST-25-EL-002` | `ST25-EL-02` | Primary Student navigation |
| #3 | `ST-25-EL-003` | `ST25-EL-03` | Global search |
| #4 | `ST-25-EL-004` | `ST25-EL-04` | Notifications |
| #5 | `ST-25-EL-005` | `ST25-EL-05` | Student profile menu |
| #6 | `ST-25-EL-006` | `ST25-EL-06` | Semester and enrollment status strip |
| #7 | `ST-25-EL-007` | `ST25-EL-07` | Discussion breadcrumb |
| #8 | `ST-25-EL-008` | `ST25-EL-08` | Back to discussion list |
| #9 | `ST-25-EL-009` | `ST25-EL-09` | Save discussion action |
| #10 | `ST-25-EL-010` | `ST25-EL-10` | Topic tag chips |
| #11 | `ST-25-EL-011` | `ST25-EL-11` | Topic views, replies and time |
| #12 | `ST-25-EL-012` | `ST25-EL-12` | Topic title |
| #13 | `ST-25-EL-013` | `ST25-EL-13` | Thread status/details panel |
| #14 | `ST-25-EL-014` | `ST25-EL-14` | Topic author and roles |
| #15 | `ST-25-EL-015` | `ST25-EL-15` | Linked course/module card |
| #16 | `ST-25-EL-016` | `ST25-EL-16` | Topic like/reaction |
| #17 | `ST-25-EL-017` | `ST25-EL-17` | Topic body |
| #18 | `ST-25-EL-018` | `ST25-EL-18` | Related discussion panel |
| #19 | `ST-25-EL-019` | `ST25-EL-19` | Topic code block and copy |
| #20 | `ST-25-EL-020` | `ST25-EL-20` | Mentor Office Hour CTA |
| #21 | `ST-25-EL-021` | `ST25-EL-21` | Source URL and View Code |
| #22 | `ST-25-EL-022` | `ST25-EL-22` | Replies heading and count |
| #23 | `ST-25-EL-023` | `ST25-EL-23` | Reply sort selector |
| #24 | `ST-25-EL-024` | `ST25-EL-24` | Accepted-solution banner |
| #25 | `ST-25-EL-025` | `ST25-EL-25` | Accepted reply author and votes |
| #26 | `ST-25-EL-026` | `ST25-EL-26` | Accepted reply body |
| #27 | `ST-25-EL-027` | `ST25-EL-27` | Accepted reply code and copy |
| #28 | `ST-25-EL-028` | `ST25-EL-28` | Accepted reply actions |
| #29 | `ST-25-EL-029` | `ST25-EL-29` | Secondary reply author and reactions |
| #30 | `ST-25-EL-030` | `ST25-EL-30` | Secondary reply body and code |
| #31 | `ST-25-EL-031` | `ST25-EL-31` | Secondary reply action |
| #32 | `ST-25-EL-032` | `ST25-EL-32` | Reply composer heading |
| #33 | `ST-25-EL-033` | `ST25-EL-33` | Composer author avatar |
| #34 | `ST-25-EL-034` | `ST25-EL-34` | Formatting toolbar and Markdown hint |
| #35 | `ST-25-EL-035` | `ST25-EL-35` | Reply textarea |
| #36 | `ST-25-EL-036` | `ST25-EL-36` | Discussion participation rule |
| #37 | `ST-25-EL-037` | `ST25-EL-37` | Send reply button |
| #38 | `ST-25-EL-038` | `ST25-EL-38` | Footer brand and description |
| #39 | `ST-25-EL-039` | `ST25-EL-39` | Footer navigation/contact columns |
| #40 | `ST-25-EL-040` | `ST25-EL-40` | Footer certification/legal strip |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Marker trên ảnh dùng ID `ST25-EL-01`…`ST25-EL-40`; xem [`screen_annotated.png`](../../screen_stitch/03_student/ST-25_chi-tiet-thread-va-phan-hoi/screen_annotated.png) và [`ST-25_markers.json`](../../screen_stitch/03_student/ST-25_chi-tiet-thread-va-phan-hoi/ST-25_markers.json). Các nhóm composite liệt kê đầy đủ child control bên dưới.

| Element ID / marker | Tên, loại, vị trí và mục đích | Thuộc tính, nguồn, visibility/state/validation | Event |
|---|---|---|---|
| ST25-EL-01 | Study2Work logo/brand; góc trái header. | Static image/text; screenshot sample. Destination/route không được xác nhận. | EV-04 |
| ST25-EL-02 | Primary nav group: Trang chủ, Khóa học, Khóa học của tôi, Lộ trình học, Diễn đàn. | Static labels/links trong screenshot; HTML prototype links `#`. Không gán route. | EV-04 |
| ST25-EL-03 | Global search field. | Screenshot-only control; query/API/result semantics không thuộc API #41/#42. | EV-04 |
| ST25-EL-04 | Notification icon/badge. | Screenshot-only; no #43 notification integration evidence for this page. | EV-04 |
| ST25-EL-05 | Student profile menu/avatar/name. | Tên/role là sample; UserSummary thread author không đồng nghĩa session state. Menu handler absent. | EV-04 |
| ST25-EL-06 | Semester/enrollment strip. | Screenshot literal “Học kỳ Fall 2024”/status; source/API mapping, freshness and visibility unknown. | EV-04 |
| ST25-EL-07 | Discussion breadcrumbs: Diễn đàn → course/topic → Thread. | Display sample only; route parameters and course/topic labels need source; no runtime links. | EV-04 |
| ST25-EL-08 | Back-to-discussions button. | Visible target `/student/discussions` in fallback HTML/inventory; back-stack, filter/page return state unspecified. | EV-04 |
| ST25-EL-09 | Save discussion action. | Screenshot button; no save/bookmark endpoint, state or auth behavior in catalog. | EV-05 |
| ST25-EL-10 | Topic tags/chips. | Sample React/WebSocket/TanStack Query/Performance terms; tag taxonomy/filter behavior absent from #42 schema. | — |
| ST25-EL-11 | Topic views/reply/time metadata. | Sample count, relative time; not in Discussion schema/API #42; no counter field. | — |
| ST25-EL-12 | Topic title heading. | Screenshot sample title; reusable Discussion requires `title:string`, but DDL has no title source. Cannot derive from content. | — |
| ST25-EL-13 | Thread status/details card: solved status, author, time, reply count, course level. | `status` exists in Discussion schema but enum/visibility not defined; counters, status labels, level and dates are sample data without mapping. | — |
| ST25-EL-14 | Topic author card, avatar, role/course labels. | `Discussion.author:UserSummary` supports id/name/avatar shape, but API response/source and current-user role labels are unresolved; screenshot values are samples. | — |
| ST25-EL-15 | Course/module card and “Xem bài giảng Module 06” action. | Course/module/title/image are sample; #42 response Discussion has course_id but no course/module projection or lesson route. | EV-08 |
| ST25-EL-16 | Topic reaction/like button with count. | Screenshot-only; no reaction API, ownership, count source, duplicate policy or state. | EV-06 |
| ST25-EL-17 | Topic body/prose content. | Logical `Discussion.content:string`; API #42 DD maps candidate `discussions.content TEXT`. Populated text is static sample, not response evidence. | — |
| ST25-EL-18 | Related discussion panel: topic rows, previews, timestamps and “Xem thêm”. | No related-topic endpoint, relation/ranking rule, route or pagination contract for ST-25. | EV-09 |
| ST25-EL-19 | Topic code block and copy-code action. | Code is screenshot sample. Copy button/clipboard semantics and parser/highlighting not source-backed; no runtime action. | EV-07 |
| ST25-EL-20 | Mentor Office Hour help card/CTA. | Screenshot copy, mentor availability and appointment action; no scheduling API or destination source. | EV-10 |
| ST25-EL-21 | Source URL card and “Xem Code” action. | URL appears only in screenshot. Safe external target, new-tab behavior and destination verification absent. | EV-07 |
| ST25-EL-22 | Replies section heading and displayed count. | Count `2` is sample; #42 comments array may supply rows only under unresolved visibility/projection; no approved count field/rule. | — |
| ST25-EL-23 | Reply sort selector. | Screenshot label/options not a catalog query parameter; no approved allowed values or ordering semantics. | EV-11 |
| ST25-EL-24 | Accepted-solution badge/banner. | Screenshot moderator/solution state; DiscussionComment schema has no accepted/solution field; no API #41/#42 mutation/status. | — |
| ST25-EL-25 | Accepted reply author/role/vote summary. | UserSummary can structurally represent author when supplied; role tags/vote count not in comment schema; all values sample. | EV-06 |
| ST25-EL-26 | Accepted reply text. | `DiscussionComment.content:string` is logical schema, but #41 request `int64` and DDL TEXT conflict; body values are illustrative. | — |
| ST25-EL-27 | Accepted reply code block/copy action. | Code block is sample; copy action behavior not wired or specified. | EV-07 |
| ST25-EL-28 | Accepted reply action row: like, reply, accepted marker. | Like/vote and accept state lack endpoint/field; reply-to-comment ID behavior (root vs nested) unresolved. | EV-06, EV-12 |
| ST25-EL-29 | Secondary reply author/profile and reaction count. | `DiscussionComment.author` logical UserSummary only; role/likes/count sample, no current mapping. | EV-06 |
| ST25-EL-30 | Secondary reply text/code preview. | Comment content is string in reusable schema; no approved relation to composer conversion or rich Markdown parsing. | — |
| ST25-EL-31 | Secondary reply action (“Trả lời”). | Screenshot control; may imply nested reply, but API #41 DD assumes root-only path as DERIVED. | EV-12 |
| ST25-EL-32 | Reply composer heading. | Static prompt; no API/data behavior. Visibility expected for permitted Student only, but permission UX is unresolved. | EV-13 |
| ST25-EL-33 | Current-user avatar beside composer. | Screenshot sample avatar; source must be authenticated current profile, not topic author; Study Web session data unavailable. | EV-13 |
| ST25-EL-34 | Formatting toolbar/Markdown hint. | Child controls: bold, italic, inline code, link, list, Markdown help. Syntax, parser, escaping/sanitization and insertion behavior unspecified. | EV-14 |
| ST25-EL-35 | Reply textarea/editor. | User-entered string. API #41 body requires `content:int64`; blank/trim/length/character rules and conversion are unapproved. No autosave. | EV-13 |
| ST25-EL-36 | Discussion participation/safety rule note. | Screenshot static explanatory copy; not an authorization rule or server response. | — |
| ST25-EL-37 | Send-reply button. | Visible CTA; API #41 is expected target but not runnable and body mismatch blocks serialization. Pending UI duplicate guard is a proposal; no server idempotency. | EV-15 |
| ST25-EL-38 | Footer brand and purpose copy. | Static screenshot content, not API data. | — |
| ST25-EL-39 | Footer navigation/contact columns. | Static links/contact values; destination routes/support flow not verified. | EV-04 |
| ST25-EL-40 | Footer legal/meta strip. | Static copyright/policy links; destinations and runtime handlers are not verified. | EV-04 |

## 4. Conditional UI & state variations
- States theo inventory: loading/replying/moderated/closed
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-25_chi-tiet-thread-va-phan-hoi/ST-25.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
