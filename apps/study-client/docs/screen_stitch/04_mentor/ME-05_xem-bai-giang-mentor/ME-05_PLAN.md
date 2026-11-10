# ME-05 — Kế hoạch Detailed Design: Xem bài giảng Mentor

> **Plan status:** COMPLETE — plan được viết trước marker map, ảnh chú thích và DD; nguồn/API và blocker đã đối chiếu.
> **Screen status dự kiến:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

## 1. Phạm vi và bằng chứng đầu vào

- Phiên này chỉ xử lý **ME-05** (`/mentor/lectures/:lectureId`); ME-03, ME-06 và ST-11/ST-25 chỉ được tham chiếu làm đích hoặc nguồn đối chiếu.
- Phân loại: `primary_task_type: docs`; `secondary_task_types: [test]`; `project_scopes: [web-work, server-study]`; dependency: AC-21 → API #48 → màn chi tiết lecture và ME-03/ME-06.
- Expected từ [`list_screen.md` ME-05](../../../list_screen.md#L165): actor Mentor, AC-21, GET #48, trạng thái `loading/ready/not-found`, liên kết ME-03 và ME-06; không tự thêm API sửa lecture.
- Mục tiêu tổng `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md` yêu cầu mỗi phiên một Screen ID, lập plan trước, giữ ảnh gốc, tạo ảnh chú thích/marker map/DD truy vết source, cập nhật tracker và worklog, tách riêng ba trạng thái chất lượng.
- Ảnh nguồn `screen.png`: PNG RGB `841×1600`, SHA-256 `458ea549ae892b0825c48a62ec13655b8f631915070bd840c62bc8690c3f6a8f`; đã mở và xem toàn ảnh. Giữ nguyên.
- `code.html`: 43,487 bytes, SHA-256 `eb8861bb475621590248c0fe9913bafd891697e5c20717dcaf9041e2f0e2a3d2`; mockup tĩnh, 14 anchors (đều `href="#"`), 8 buttons, 1 input, không có form/video/source, không có inline handler hay fetch/XHR. Có các vùng mẫu không hiện thực dữ liệu/API.
- Study Web hiện có `dist/` và `docs/`, không có `src/`, package manifest hay router có thể xác nhận route; bundle/serving không phải runtime evidence. `.agents/web-work/study/` hiện ghi `UNWIRED`.
- UI-only DD không có skill canonical trong registry; `createDD-markdown` loại trừ `web-ui-only-dd`, nên không áp dụng template API như UI contract.

## 2. Source trace đã xác nhận trước authoring

### API #48 — đọc Lecture

- Route hiện đăng ký trong `apps/study-server/app/api/v1.py`: `GET /api/v1/mentor/lectures/{lecture_id}`, chuyển raw path/header/DB/trace vào `get_lecture`.
- Shared `validate_current_user_request(..., role="MENTOR")` chạy trước path parse và DB. Path phải parse được signed int64; malformed/out-of-range hiện trả 404 `DESIGN_RESOURCE_NOT_FOUND` theo source, dù catalog không khai báo 422.
- Query Q1 đọc `lessons` cùng `courses`; ẩn đúng status `DELETED`. Không có row → 404; `course_id`/parent thiếu → 500; `courses.mentor_id` khác principal đã xác thực → 403. AC-21 còn nêu course được phân công, nhưng source chỉ hỗ trợ direct owner.
- Query Q2 đọc association `lesson_uploads` theo `asset_position ASC, upload_id ASC`, resolve `uploads` cùng owner, purpose `LECTURE`, course; broken link/mapping hoặc SQL failure → safe 500 và rollback. Endpoint chỉ đọc, không ghi dữ liệu.
- Success 200 `DESIGN_RESOURCE_RETRIEVED` trả `ApiEnvelope<Lecture>` với `data.id`, `course_id`, `title`, nullable `content`, `assets[]` (`id/name/url/content_type/size_bytes/status`), `order`, `status`. `assets=[]` nếu không có link. Status trả nguyên văn trừ `DELETED`; enum chưa được catalog định nghĩa.
- Model #47 dùng lại `LectureResponse`; current #47 lưu `content:int64` thành chuỗi thập phân và tạo status `PUBLISHED`. #48 có thể trả `content:null` từ row cũ hoặc status khác theo source.
- API #48 có focused test source cho auth, owner, malformed/missing ID, parent/link integrity, thứ tự asset, nullable content, empty assets, safe errors và OpenAPI. Chỉ đọc test; không chạy test trong phiên này. Fake DB assertions không chứng minh migration/schema live.
- API DD #48 còn `Draft — Needs Confirmation`; live schema/migration 005, identity/assignment, content null/semantics, status enum, malformed path mapping và error envelope vẫn open. Legacy DDL/migrations là artifact checkout, không phải xác minh live DB. V1-PILOT schema dùng IDs/data model khác.

### UI hiện tại và discrepancy

- Ảnh là mockup populated: header/nav, breadcrumb, status/id/author/title, copy/preview/status/edit actions, video-looking player và chapter strip, academic note/code block, tài liệu, analytics, discussion cards, course outline và footer.
- HTML hiện chỉ có các anchor `#`, không có player `<video>`, route/API binding, upload/download authorization hay event handler. Dữ liệu mẫu về tác giả, course, video, views, retention, rating, discussion và outline không có trong response #48.
- #48 chỉ trả Lecture + UploadAsset metadata, không trả video URL, author profile, analytics, discussion/reply, course outline/adjacent lessons, preview permission, edit/status transition, download semantics hay routing. Không suy ra các phần này từ mockup.
- ME-04 tạo flow kỳ vọng #47 201 → `data.id` → ME-05 route → GET #48; route và redirect vẫn chưa có Study Web implementation. ME-05 có liên kết expected về ME-03/ME-06; course context chỉ có `course_id` trên #48, còn route của ME-06 cần course ID, không có API course detail.

## 3. Kế hoạch artifacts

1. Hoàn tất trace và trạng thái trong plan này trước các artifact tiếp theo.
2. Tạo `ME-05_markers.json` làm mapping chuẩn và `ME-05_markers_overlay.svg` có đúng một marker cho mỗi element.
3. Dựng `screen_annotated.png` ở scale 2, giữ nguyên khung gốc; marker tuần tự `#1…#33` đặt ở lề/đệm thành phần, tránh text/controls chính.
4. Mở ảnh annotated bằng image viewer, kiểm tra marker không chồng nhau/che nội dung; chỉnh marker map và dựng lại nếu cần.
5. Viết `ME-05.md` gồm overview, expected/current behavior riêng, API/data trace, element map 100%, event flow, state/error/access rules, links, blockers và acceptance.
6. Cập nhật hàng ME-05 cùng checkpoint count/pointer trong `dd_screens/PLAN.md`; viết worklog theo template với preflight 3 docs logs.
7. Chạy static artifact audit và `git diff --check`; không chạy tests, browser hay runtime.

### Marker inventory dự kiến

| # | Element dự kiến |
|---:|---|
| 1–5 | Brand, navigation, search, notifications, Mentor account |
| 6–7 | Breadcrumb về danh sách khóa học và workspace course |
| 8–11 | Lecture status, ID, author, title |
| 12–15 | Copy link, preview, change status, edit actions |
| 16–17 | Video-looking player/control group và chapter strip |
| 18–20 | Academic notes, copy-code control, code block |
| 21–24 | Resource panel, download, open PDF, external GitHub link |
| 25–28 | Analytics panel, discussion preview/reply, discussions link |
| 29–32 | Course structure panel, previous/current/next lesson rows |
| 33 | Footer information/navigation |

Markers chỉ nhận diện element nhìn thấy; không xác nhận chức năng giả lập đó có contract hoặc đang chạy.

## 4. Kiểm tra và tiêu chí kết thúc phiên

- Giữ nguyên hash `screen.png` và `code.html`.
- JSON có đúng 33 số liên tiếp và 33 ID duy nhất; SVG có 33 marker khớp JSON/DD; marker nằm trong tọa độ ảnh gốc; annotated PNG có kích thước đúng scale 2 và được xem trực quan.
- 100% element có mô tả; mọi nút/link/nhóm player/timeline có event entry hoặc ghi rõ `unwired/blocked`; API #48 fields/errors/access/effects đúng source; mọi route/field giả lập được đánh dấu gap.
- Tất cả relative links trong DD và worklog/tracker trỏ đúng file; checkpoint tăng 32/83 → 33/83 chỉ khi đủ 4 file cốt lõi; không sửa các Screen ID khác.
- Không chạy test/runtime; `DD READY` không được dùng nếu blockers còn chặn implementability, `IMPLEMENTATION BLOCKED` ghi phụ thuộc, `RUNTIME VERIFIED` giữ riêng và chưa đạt.
