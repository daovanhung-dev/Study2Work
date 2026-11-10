# ME-04 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ME-04_markers.json](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/ME-04_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ME-04-EL-001` | `ME04-EL-01` | Brand/logo Mentor Portal |
| #2 | `ME-04-EL-002` | `ME04-EL-02` | Điều hướng Mentor toàn cục |
| #3 | `ME-04-EL-003` | `ME04-EL-03` | Tìm kiếm header |
| #4 | `ME-04-EL-004` | `ME04-EL-04` | Notification button và badge |
| #5 | `ME-04-EL-005` | `ME04-EL-05` | Tài khoản Mentor hiện tại |
| #6 | `ME-04-EL-006` | `ME04-EL-06` | Quay lại Workspace ME-03 |
| #7 | `ME-04-EL-007` | `ME04-EL-07` | Breadcrumb course |
| #8 | `ME-04-EL-008` | `ME04-EL-08` | Course code mẫu trên breadcrumb |
| #9 | `ME-04-EL-009` | `ME04-EL-09` | Tiêu đề trang tạo bài giảng |
| #10 | `ME-04-EL-010` | `ME04-EL-10` | Badge “ME-04 Authoring” |
| #11 | `ME-04-EL-011` | `ME04-EL-11` | Nhãn auto-save mẫu |
| #12 | `ME-04-EL-012` | `ME04-EL-12` | CTA xem trước (Preview) |
| #13 | `ME-04-EL-013` | `ME04-EL-13` | Header khối định vị lecture |
| #14 | `ME-04-EL-014` | `ME04-EL-14` | Select chương/module |
| #15 | `ME-04-EL-015` | `ME04-EL-15` | Badge Bloom-Tech level |
| #16 | `ME-04-EL-016` | `ME04-EL-16` | Select thứ tự/vị trí bài |
| #17 | `ME-04-EL-017` | `ME04-EL-17` | Input tiêu đề lecture |
| #18 | `ME-04-EL-018` | `ME04-EL-18` | Bộ đếm ký tự tiêu đề |
| #19 | `ME-04-EL-019` | `ME04-EL-19` | Input thời lượng ước tính |
| #20 | `ME-04-EL-020` | `ME04-EL-20` | Hiển thị khung độ khó |
| #21 | `ME-04-EL-021` | `ME04-EL-21` | Header khối media/video |
| #22 | `ME-04-EL-022` | `ME04-EL-22` | Chip API #34 |
| #23 | `ME-04-EL-023` | `ME04-EL-23` | Card file video đã tải |
| #24 | `ME-04-EL-024` | `ME04-EL-24` | Thumbnail video |
| #25 | `ME-04-EL-025` | `ME04-EL-25` | Tên và metadata file |
| #26 | `ME-04-EL-026` | `ME04-EL-26` | Progress/status “100% Hoàn tất” |
| #27 | `ME-04-EL-027` | `ME04-EL-27` | Nút xem phát thử media |
| #28 | `ME-04-EL-028` | `ME04-EL-28` | Nút thay thế/retry media |
| #29 | `ME-04-EL-029` | `ME04-EL-29` | Nút xóa media khỏi danh sách |
| #30 | `ME-04-EL-030` | `ME04-EL-30` | Vùng kéo/thả/chọn tệp |
| #31 | `ME-04-EL-031` | `ME04-EL-31` | Hướng dẫn MIME/dung lượng mẫu |
| #32 | `ME-04-EL-032` | `ME04-EL-32` | Input URL stream HLS/Vimeo |
| #33 | `ME-04-EL-033` | `ME04-EL-33` | Header tóm tắt và code sample |
| #34 | `ME-04-EL-034` | `ME04-EL-34` | Chọn chế độ Markdown |
| #35 | `ME-04-EL-035` | `ME04-EL-35` | Chọn chế độ WYSIWYG |
| #36 | `ME-04-EL-036` | `ME04-EL-36` | Thanh công cụ định dạng: B/I/U/H2/H3/list/quote/code/image |
| #37 | `ME-04-EL-037` | `ME04-EL-37` | Vùng nội dung Markdown/WYSIWYG gồm văn bản và code mẫu |
| #38 | `ME-04-EL-038` | `ME04-EL-38` | Header attachments/source code |
| #39 | `ME-04-EL-039` | `ME04-EL-39` | Nút thêm attachment |
| #40 | `ME-04-EL-040` | `ME04-EL-40` | Card attachment PDF |
| #41 | `ME-04-EL-041` | `ME04-EL-41` | Nút gỡ attachment PDF |
| #42 | `ME-04-EL-042` | `ME04-EL-42` | Card attachment ZIP |
| #43 | `ME-04-EL-043` | `ME04-EL-43` | Nút gỡ attachment ZIP |
| #44 | `ME-04-EL-044` | `ME04-EL-44` | Header cấu hình phân phối/publish |
| #45 | `ME-04-EL-045` | `ME04-EL-45` | Radio Video bài giảng chính |
| #46 | `ME-04-EL-046` | `ME04-EL-46` | Radio Bài đọc chuyên sâu |
| #47 | `ME-04-EL-047` | `ME04-EL-47` | Radio Hướng dẫn thực hành Lab |
| #48 | `ME-04-EL-048` | `ME04-EL-48` | Toggle Guest Preview |
| #49 | `ME-04-EL-049` | `ME04-EL-49` | Toggle khóa điều kiện tiên quyết |
| #50 | `ME-04-EL-050` | `ME04-EL-50` | Radio Lưu nháp |
| #51 | `ME-04-EL-051` | `ME04-EL-51` | Radio Gửi duyệt/Publish |
| #52 | `ME-04-EL-052` | `ME04-EL-52` | Header kiểm định QA |
| #53 | `ME-04-EL-053` | `ME04-EL-53` | Badge điểm QA 100% |
| #54 | `ME-04-EL-054` | `ME04-EL-54` | Giải thích QA |
| #55 | `ME-04-EL-055` | `ME04-EL-55` | Danh sách checklist QA |
| #56 | `ME-04-EL-056` | `ME04-EL-56` | CTA tạo bài giảng & gửi duyệt |
| #57 | `ME-04-EL-057` | `ME04-EL-57` | CTA lưu bản nháp |
| #58 | `ME-04-EL-058` | `ME04-EL-58` | CTA hủy bỏ |
| #59 | `ME-04-EL-059` | `ME04-EL-59` | Chú thích ISO/EduTrust/AC |
| #60 | `ME-04-EL-060` | `ME04-EL-60` | Footer Study2Work và các nhóm liên kết |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 3. Ma trận element

Tọa độ marker là pixel trên ảnh nguồn; `screen_annotated.png` xuất 2×. Element nhóm chỉ gộp các control con khi cùng vùng/chức năng; toolbar và editor vẫn liệt kê control con tại cột nội dung. Mọi ID dưới đây ánh xạ duy nhất tới marker cùng số.

Sau visual review, marker #3 và #25 được chuyển khỏi vùng nhãn/marker lân cận; JSON, SVG và annotated PNG được tạo lại sau bản tọa độ cuối trong `ME-04_PLAN.md` rồi xem lại.

| Element ID | Tên/loại/vị trí | Data, default, validation, hiển thị/trạng thái | Event |
|---|---|---|---|
| ME04-EL-01 | Logo/brand, global header | Static mockup; đích route không được wire. | EV-21 |
| ME04-EL-02 | Navigation Mentor | Dashboard, course list, grading, support, notifications trong mockup; tất cả `href="#"`. | EV-21 |
| ME04-EL-03 | Search input header | Mockup text; không có query source/API/handoff ở ME-04. | EV-21 |
| ME04-EL-04 | Notification icon + badge | Badge `3` là sample; API Mentor notification #63/#64 có trong backend source nhưng target/link của header chưa được xác định tại screen này. | EV-21 |
| ME04-EL-05 | Mentor identity/avatar | Tên/chức danh mẫu, không lấy từ #46 course list; không coi là authenticated profile runtime. | — |
| ME04-EL-06 | Link quay lại Workspace | Target đề xuất ME-03 với cùng `courseId`; chưa có browser route/history policy. | EV-20 |
| ME04-EL-07 | Breadcrumb tên course | Giá trị sample; nguồn có thể đối chiếu từ #46 `Course.title`, nhưng không có detail endpoint. | EV-01 |
| ME04-EL-08 | Course code sample | `FE-REACT-ENT-2025` không có trong Course projection #46; không phải route ID theo source. | EV-01 |
| ME04-EL-09 | Page title | Static title “Thêm bài giảng mới vào giáo trình”. | — |
| ME04-EL-10 | Badge Authoring | Static status badge; không biểu thị persisted draft/status. | — |
| ME04-EL-11 | Auto-save status label | Text “Đã tự động lưu…” nhưng HTML không có autosave timer/API. Không được hiển thị như persisted status. | — |
| ME04-EL-12 | Preview button | Không có preview API/state/route contract cho unsaved lecture. | EV-11 |
| ME04-EL-13 | Metadata section header | Section container; no backend object mapping. | — |
| ME04-EL-14 | Select chương/module | Sample options; #46 không trả module hierarchy, #47 không nhận module ID. | EV-02 |
| ME04-EL-15 | Bloom-Tech level text | Static classification; không có field/rule trong #46/#47. | — |
| ME04-EL-16 | Select order/lesson position | Sample `Bài số 16/48`; only #47 `order:int32`, no max/order lookup or positivity rule. | EV-02 |
| ME04-EL-17 | Input title | Mockup prefilled; #47 requires string ≤200, no minimum/trim rule. UI required marker is not runtime validation. | EV-03 |
| ME04-EL-18 | Character counter | `78/120` sample contradicts #47 max 200; needs approved UI limit. | EV-03 |
| ME04-EL-19 | Duration input | Text sample “35 phút”; no duration field in #47 request/response. | EV-03 |
| ME04-EL-20 | Difficulty indicator | Four-dot/“Senior Standard” sample; no #47 field or scoring formula. | — |
| ME04-EL-21 | Media section header | Group container for media actions. | — |
| ME04-EL-22 | `API #34 Upload CDN` chip | Static annotation, not upload status or provider guarantee. | EV-04/05 |
| ME04-EL-23 | Existing uploaded video card | Filename, length, codec, HLS and URL are mock data; current #34 response provides only UploadAsset metadata. | EV-04/05/06 |
| ME04-EL-24 | Video thumbnail | Static preview; no thumbnail generation/URL contract in #34 response. | EV-05 |
| ME04-EL-25 | File name/size/duration/encoding metadata | Only `name` and `size_bytes` map to #34 UploadAsset; duration and encoding/transcode state have no source. | EV-05 |
| ME04-EL-26 | Progress/completion indicator | “100% Hoàn tất” sample. #34 source returns after upload completion; streaming progress events are not part of response. | EV-04/05 |
| ME04-EL-27 | Preview media button | Mockup control; preview source and modal/player behavior unspecified. | EV-11 |
| ME04-EL-28 | Replace media button | No replace endpoint; a new #34 upload would create another persisted asset. | EV-06 |
| ME04-EL-29 | Remove media button | No upload delete route; client-only deselection is not remote cleanup. | EV-07 |
| ME04-EL-30 | Drag/drop/select zone | Mockup has no `<input type=file>`, form, drop handler or click handler. API #34 needs multipart binary. | EV-04 |
| ME04-EL-31 | File type/size guidance | Mockup claims MP4/WebM/MOV, codecs, 2 GB; #34 source has no MIME allowlist or app size cap. | EV-04 |
| ME04-EL-32 | Stream URL input | URL sample; #47 has no `video_url` field and #34 uploads file bytes only. | EV-08 |
| ME04-EL-33 | Summary/editor header | Static heading; no persisted editor schema in current API. | — |
| ME04-EL-34 | Markdown toggle | Mockup button only; no client state handler/editor library. | EV-09 |
| ME04-EL-35 | WYSIWYG toggle | Mockup button only; no client state handler/editor library. | EV-09 |
| ME04-EL-36 | Formatting toolbar composite | Child actions B/I/U/H2/H3/list/quote/code/image; grouped marker; HTML has buttons but no listeners. | EV-09 |
| ME04-EL-37 | Rich-text/code content surface | Sample paragraphs/code; HTML has no textarea/contenteditable. #47 accepts `content:int64` then stores decimal string. | EV-03/09 |
| ME04-EL-38 | Attachment section heading | Static label “Tài liệu đính kèm & Mã nguồn mẫu”. | EV-10 |
| ME04-EL-39 | Add attachment control | No listener/file picker in HTML. Future upload must use #34 then retain asset ID. | EV-04/10 |
| ME04-EL-40 | PDF attachment card | `name/size` sample; #47 can return linked UploadAsset once ID resolved. | EV-10 |
| ME04-EL-41 | Remove PDF control | No server delete. Removing ID locally after upload leaves the #34 record/object. | EV-07 |
| ME04-EL-42 | ZIP attachment card | Same source boundary as PDF card. | EV-10 |
| ME04-EL-43 | Remove ZIP control | No server delete. | EV-07 |
| ME04-EL-44 | Publish configuration header | Static section, not API state. | — |
| ME04-EL-45 | Radio “Video bài giảng chính” | One of three static types; #47 has no type field. | EV-12 |
| ME04-EL-46 | Radio “Bài đọc chuyên sâu” | Same unsupported type field. | EV-12 |
| ME04-EL-47 | Radio “Hướng dẫn thực hành Lab” | Same unsupported type field. | EV-12 |
| ME04-EL-48 | Guest Preview toggle | No API #47 field or guest-access policy. | EV-13 |
| ME04-EL-49 | Prerequisite toggle | No prerequisite field, relationship, or validation endpoint. | EV-14 |
| ME04-EL-50 | Radio “Lưu nháp” | #47 always persists `PUBLISHED`; no draft endpoint. | EV-15/16 |
| ME04-EL-51 | Radio “Gửi duyệt (Publish)” | Label conflicts with #47 immediate `PUBLISHED` insertion; no review state in response. | EV-15/17 |
| ME04-EL-52 | QA panel heading | Mock quality panel, no QA API. | — |
| ME04-EL-53 | “100% Đạt” badge | Unsupported calculated result; no rule/evidence source. | — |
| ME04-EL-54 | QA explanatory copy | Claims conditions/policy not returned by #47. | — |
| ME04-EL-55 | QA checklist group | SEO, video codec, code snippet, microlearning rules are mockup-only; no validation service/formula. | — |
| ME04-EL-56 | Primary create/submit button | Current HTML fake handler only; intended future action is #47 after uploads and approved data mapping. | EV-17/18/19 |
| ME04-EL-57 | “Lưu bản nháp” button | No API to persist draft; do not call #47 because that publishes. | EV-16 |
| ME04-EL-58 | Cancel button | Intended return ME-03; dirty-state confirmation/upload cleanup not specified. | EV-20 |
| ME04-EL-59 | ISO/EduTrust/AC reference note | Static copy; not a validation/certification response. | — |
| ME04-EL-60 | Footer links/content | Static `span`/copy and placeholder targets; route destinations not established. | EV-21 |

## 4. Conditional UI & state variations
- States theo inventory: draft/uploading/creating/422/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/ME-04.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
