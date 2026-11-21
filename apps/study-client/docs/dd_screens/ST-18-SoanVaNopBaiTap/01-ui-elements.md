# ST-18 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-18_markers.json](../../screen_stitch/03_student/ST-18_soan-va-nop-bai-tap/ST-18_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-18-EL-001` | `ST18-EL-01` | Header Study2Work logo and brand |
| #2 | `ST-18-EL-002` | `ST18-EL-02` | Header course search field |
| #3 | `ST-18-EL-003` | `ST18-EL-03` | Primary navigation group: Home, Courses, My Courses, Progress, Community |
| #4 | `ST-18-EL-004` | `ST18-EL-04` | Notifications control and unread indicator |
| #5 | `ST-18-EL-005` | `ST18-EL-05` | Student avatar, name and profile control |
| #6 | `ST-18-EL-006` | `ST18-EL-06` | Breadcrumb trail and current screen |
| #7 | `ST-18-EL-007` | `ST18-EL-07` | Assignment identifier and draft-status chips |
| #8 | `ST-18-EL-008` | `ST18-EL-08` | Assignment title |
| #9 | `ST-18-EL-009` | `ST18-EL-09` | Assignment brief and supporting description |
| #10 | `ST-18-EL-010` | `ST18-EL-10` | Deadline countdown card and due timestamp |
| #11 | `ST-18-EL-011` | `ST18-EL-11` | Submission and appeal policy information banner |
| #12 | `ST-18-EL-012` | `ST18-EL-12` | Rubric version and readiness badge |
| #13 | `ST-18-EL-013` | `ST18-EL-13` | Section 01 heading and delivery requirements summary |
| #14 | `ST-18-EL-014` | `ST18-EL-14` | Required-field badge |
| #15 | `ST-18-EL-015` | `ST18-EL-15` | GitHub repository URL input |
| #16 | `ST-18-EL-016` | `ST18-EL-16` | GitHub repository validation status |
| #17 | `ST-18-EL-017` | `ST18-EL-17` | Repository visibility/collaborator helper note |
| #18 | `ST-18-EL-018` | `ST18-EL-18` | Live demo/deployment URL input |
| #19 | `ST-18-EL-019` | `ST18-EL-19` | Deployment availability/status indicator |
| #20 | `ST-18-EL-020` | `ST18-EL-20` | Deployment URL accessibility helper note |
| #21 | `ST-18-EL-021` | `ST18-EL-21` | Self-evaluation checklist heading and explanation |
| #22 | `ST-18-EL-022` | `ST18-EL-22` | Checklist row: Source Code Clean Architecture and score |
| #23 | `ST-18-EL-023` | `ST18-EL-23` | Checklist row: Deployment and HTTP status |
| #24 | `ST-18-EL-024` | `ST18-EL-24` | Checklist row: Vitest coverage and percentage |
| #25 | `ST-18-EL-025` | `ST18-EL-25` | Checklist row: Architecture PDF attachment and size |
| #26 | `ST-18-EL-026` | `ST18-EL-26` | Section 02 attachments heading and description |
| #27 | `ST-18-EL-027` | `ST18-EL-27` | Displayed maximum attachment size: 50 MB |
| #28 | `ST-18-EL-028` | `ST18-EL-28` | File drop zone and upload affordance |
| #29 | `ST-18-EL-029` | `ST18-EL-29` | Choose file from device button |
| #30 | `ST-18-EL-030` | `ST18-EL-30` | Advertised file-format support text |
| #31 | `ST-18-EL-031` | `ST18-EL-31` | Successfully uploaded files count |
| #32 | `ST-18-EL-032` | `ST18-EL-32` | Uploaded file row 1: name, type, size and 100% status |
| #33 | `ST-18-EL-033` | `ST18-EL-33` | Uploaded file 1 preview/open action |
| #34 | `ST-18-EL-034` | `ST18-EL-34` | Uploaded file 1 remove action |
| #35 | `ST-18-EL-035` | `ST18-EL-35` | Uploaded file row 2: name, type, size and 100% status |
| #36 | `ST-18-EL-036` | `ST18-EL-36` | Uploaded file 2 preview/open action |
| #37 | `ST-18-EL-037` | `ST18-EL-37` | Uploaded file 2 remove action |
| #38 | `ST-18-EL-038` | `ST18-EL-38` | Assigned mentor card heading |
| #39 | `ST-18-EL-039` | `ST18-EL-39` | Mentor avatar, name and role |
| #40 | `ST-18-EL-040` | `ST18-EL-40` | Mentor availability and response-time status |
| #41 | `ST-18-EL-041` | `ST18-EL-41` | Mentor evaluation process and numbered steps |
| #42 | `ST-18-EL-042` | `ST18-EL-42` | Draft version history heading |
| #43 | `ST-18-EL-043` | `ST18-EL-43` | Current draft entry, timestamp and autosave badge |
| #44 | `ST-18-EL-044` | `ST18-EL-44` | Previous draft entry, timestamp and restore action |
| #45 | `ST-18-EL-045` | `ST18-EL-45` | Section 03 reflection/editor heading and summary |
| #46 | `ST-18-EL-046` | `ST18-EL-46` | Formatting toolbar: bold, italic, code, lists, quote and link |
| #47 | `ST-18-EL-047` | `ST18-EL-47` | Submission reflection text editor |
| #48 | `ST-18-EL-048` | `ST18-EL-48` | Markdown support note |
| #49 | `ST-18-EL-049` | `ST18-EL-49` | Current reflection character count |
| #50 | `ST-18-EL-050` | `ST18-EL-50` | Academic-integrity commitment checkbox |
| #51 | `ST-18-EL-051` | `ST18-EL-51` | Academic-integrity statement and policy text |
| #52 | `ST-18-EL-052` | `ST18-EL-52` | Draft autosave status and last-saved timestamp strip |
| #53 | `ST-18-EL-053` | `ST18-EL-53` | Save draft button |
| #54 | `ST-18-EL-054` | `ST18-EL-54` | Cancel and return to assignment button |
| #55 | `ST-18-EL-055` | `ST18-EL-55` | Confirm assignment submission primary button |
| #56 | `ST-18-EL-056` | `ST18-EL-56` | Footer brand, description and certification badges |
| #57 | `ST-18-EL-057` | `ST18-EL-57` | Footer Study navigation group |
| #58 | `ST-18-EL-058` | `ST18-EL-58` | Footer community navigation group |
| #59 | `ST-18-EL-059` | `ST18-EL-59` | Footer support and legal navigation group |
| #60 | `ST-18-EL-060` | `ST18-EL-60` | Copyright notice |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả elements

Các sample value chỉ mô tả ảnh. “Chưa có contract” nghĩa là không suy ra validation, persistence hoặc side effect.

| ID / Marker | Element, loại, vị trí | Data / thuộc tính / trạng thái | Event |
|---|---|---|---|
| ST18-EL-01 | Logo và brand, link/header | Tĩnh; destination trong HTML là #; hover/focus cần theo design guide. | EV-13 |
| ST18-EL-02 | Ô tìm kiếm khóa học, input/header | Placeholder tìm khóa học/kỹ năng/bài thi; không có search API/state trong ST-18 contract. | EV-13 |
| ST18-EL-03 | Nhóm nav chính, links/header | Trang chủ, khóa học, khóa học của tôi, tiến độ, diễn đàn; Study routes hiện không wire. | EV-13 |
| ST18-EL-04 | Notification icon/badge, button/header | Mẫu có chấm unread; notification count/data chưa có source. | EV-13 |
| ST18-EL-05 | Avatar, tên và profile, button/header | Tên/role là sample; nguồn profile/token route không thuộc contract ST-18. | EV-13 |
| ST18-EL-06 | Breadcrumb, navigation | Khóa học của tôi → course → capstone → ST-18; course names/IDs là sample; đường quay lại chưa được wire. | EV-11 |
| ST18-EL-07 | Assignment ID + draft chips, status labels/hero | ASSIGNMENT #01, Bản nháp mới; route ID thật từ path, status từ #33/#35 chưa được cung cấp. | EV-02 |
| ST18-EL-08 | Assignment title, heading/hero | Sample title; candidate #33 title, hiện #33 chưa có runtime projection. | EV-02 |
| ST18-EL-09 | Assignment brief, text/hero | Sample description; candidate #33 description?; không coi nội dung ảnh là server data. | EV-02 |
| ST18-EL-10 | Countdown và due time, status card/hero | Timestamp/digits sample; timezone, boundary, server clock và enforcement policy open; không tự khóa submit theo client clock. | EV-02 |
| ST18-EL-11 | Chính sách nộp bài/phúc khảo, info banner | Copy mẫu nói deadline và nhận bài; không có policy ID/appeal schema trong #33/#35. | EV-02 |
| ST18-EL-12 | Rubric/version badge | Rubric #4.2 Ready là sample; #33/#35 không trả rubric/version. | EV-02 |
| ST18-EL-13 | Section 01 heading/caption | Mã nguồn & Triển Khai Thực Tế; tĩnh trong design. | EV-03 |
| ST18-EL-14 | Required badge | Required state hiển thị; không chứng minh server validation hoặc hai URL có #35 wire fields. | EV-03 |
| ST18-EL-15 | GitHub URL, input | Sample URL; visible required; URL syntax, repo access check, save/send mapping chưa có contract. | EV-03 |
| ST18-EL-16 | GitHub validation status | Repo hợp lệ là sample success; API/check source và validation rules absent. | EV-03 |
| ST18-EL-17 | Repository visibility/collaborator note | Static helper; public/collaborator requirement là screenshot text, chưa thấy canonical contract. | EV-03 |
| ST18-EL-18 | Deployment URL, input | Sample Vercel URL; visible required; no #35 field mapping or URL validation contract. | EV-03 |
| ST18-EL-19 | Deployment status | Online (200 OK) sample; health-check endpoint/trigger/source unspecified. | EV-03 |
| ST18-EL-20 | Deployment helper note | Vercel/Netlify/Cloudflare copy; not a server validation rule. | EV-03 |
| ST18-EL-21 | Checklist heading and description | Four technical criteria; no checklist response/endpoint. | EV-02 |
| ST18-EL-22 | Checklist row: architecture | Green check/100% sample; read-only appearance; completion source undefined. | EV-02 |
| ST18-EL-23 | Checklist row: deployment | Green check/200 OK sample; no health-check integration. | EV-02 |
| ST18-EL-24 | Checklist row: test coverage | 92% sample; no CI/test artifact contract. | EV-02 |
| ST18-EL-25 | Checklist row: report | 3.4 MB sample; relation to attachment #34 not verified. | EV-02 |
| ST18-EL-26 | Section 02 heading/caption | Attachment/audit report heading; static label names API #34. | EV-04 |
| ST18-EL-27 | Tối đa 50MB badge | Design-only cap; current #34 application accepts any file size. | EV-04 |
| ST18-EL-28 | Drag/drop zone, file input region | Supports selecting candidate files in design; no current browser event handler. | EV-04 |
| ST18-EL-29 | Choose local file, button | Opens local picker in intended UX; allowed count/duplicate/size/MIME rules need approval. | EV-04 |
| ST18-EL-30 | Advertised formats/helper | PDF, DOCX, ZIP, PNG, WEBP and 50 MB are not enforced by current #34. | EV-04 |
| ST18-EL-31 | Uploaded-file count | “(2)” is sample; distinguish selected/uploading/uploaded/failed counts after behavior is approved. | EV-04 |
| ST18-EL-32 | File row 1 | Sample PDF name, 3.4 MB, Upload 100%; #34 response can supply name/size/status after a real upload. | EV-04 |
| ST18-EL-33 | File 1 preview action, icon button | #34 returns public-base URL; view access/target is unresolved; provide accessible name if implemented. | EV-05 |
| ST18-EL-34 | File 1 remove action, icon button | No upload-delete API; distinguish removing local selection from orphaning an uploaded object. | EV-06 |
| ST18-EL-35 | File row 2 | Sample PNG name, 850 KB, Upload 100%; same API mapping as row 1. | EV-04 |
| ST18-EL-36 | File 2 preview action, icon button | Same public URL/access limitation as file 1. | EV-05 |
| ST18-EL-37 | File 2 remove action, icon button | No delete/cleanup contract. | EV-06 |
| ST18-EL-38 | Mentor card heading | Static sample; #33 does not return mentor/rubric data. | EV-02 |
| ST18-EL-39 | Mentor avatar/name/role | All values are sample; no assignment mentor projection in #33. | EV-02 |
| ST18-EL-40 | Availability/response badge | Phản hồi trong vòng 48h sample; no SLA contract. | EV-02 |
| ST18-EL-41 | Review workflow text | Steps reference CI/CD, GitHub Webhook, code review and 1–1; no workflow/service contract. | EV-02 |
| ST18-EL-42 | Draft history heading | History source/version API absent. | EV-09 |
| ST18-EL-43 | Current draft row/timestamp/autosave badge | #03, timestamp and autosave are sample; no draft API or durable storage source. | EV-09 |
| ST18-EL-44 | Previous draft row/timestamp + restore action | #02 and timestamp sample; version identity and restore behavior absent. | EV-10 |
| ST18-EL-45 | Section 03/editor heading | Ghi chú cho Mentor & Tự Đánh Giá; not represented as a dedicated #35 field. | EV-07 |
| ST18-EL-46 | Formatting toolbar | Bold, italic, code, ordered/bullet list, quote, link. Markdown behavior is visual intent; toolbar serialization/keyboard contract unavailable. | EV-07 |
| ST18-EL-47 | Reflection text editor, textarea/editor | Sample note and 312-character count; #35 text is a candidate only; maximum length, empty/trim and markdown/plain encoding unresolved. | EV-07 |
| ST18-EL-48 | Markdown support note | UI claim; exact parser/sanitization/rendering policy absent. | EV-07 |
| ST18-EL-49 | Character counter | 312 ký tự sample; what counts (Unicode code points/graphemes/bytes) and any limit undefined. | EV-07 |
| ST18-EL-50 | Academic-integrity checkbox | Checked in screenshot; no corresponding #35 request field or required/gating rule. | EV-08 |
| ST18-EL-51 | Academic-integrity statement | Static policy copy; source/version, required acknowledgement and audit storage absent. | EV-08 |
| ST18-EL-52 | Sticky save-state strip | Đã tự động lưu vào máy chủ lúc 14:20:15 sample; autosave not backed by API/source. | EV-09 |
| ST18-EL-53 | Save draft button | No draft endpoint/behavior; do not call #35 because saving a draft is distinct from final submission. | EV-09 |
| ST18-EL-54 | Cancel/back button | Proposed return to ST-17; unsaved-change confirmation and cleanup behavior open. | EV-11 |
| ST18-EL-55 | Confirm submit button | Final mutation candidate #35; disable repeat clicks only as a future UI state after approved behavior; server idempotency is unresolved. | EV-12 |
| ST18-EL-56 | Footer brand/description/certifications | Static marketing/certification claims; not derived from assignment/API data. | — |
| ST18-EL-57 | Footer learning navigation group | Multiple placeholder links in companion HTML; destinations not runtime routes. | EV-13 |
| ST18-EL-58 | Footer community navigation group | Static design links; no current Study Web navigation. | EV-13 |
| ST18-EL-59 | Footer support/legal navigation group | Contact/policy destinations not specified by ST-18 contract. | EV-13 |
| ST18-EL-60 | Copyright/brand line | Static sample footer copy. | — |

## 4. Conditional UI & state variations
- States theo inventory: editing/uploading/submitting/failed/submitted
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-18_soan-va-nop-bai-tap/ST-18.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
