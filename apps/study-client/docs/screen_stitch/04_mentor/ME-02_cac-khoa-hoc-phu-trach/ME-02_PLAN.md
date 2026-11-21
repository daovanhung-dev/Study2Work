# ME-02 — Kế hoạch DD: Các khóa học phụ trách

> **Plan status:** COMPLETE — lập trước khi tạo marker map, ảnh chú thích và DD.<br>
> **Screen status:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

## 1. Phạm vi và nguồn

- **Screen ID / tên:** ME-02 — Các khóa học phụ trách (Page).
- **Route đề xuất:** `/mentor/courses`; **actor:** Mentor đã đăng nhập.
- **Nguồn màn hình:** `screen.png` 1100×1600 và `code.html` 47,810 bytes; giữ nguyên hai file này. SHA-256 ban đầu: PNG `fc133a37e6b5783d1d220145d07fb995be4d7bd0962c218e65d3d876c49a9bc4`, HTML `1f0287c63b92f85c98a34f2a8862ac14c7a93a6a080adc679c3d13e250559354`.
- **Expected:** inventory `list_screen.md` ME-02 row; AC-21 yêu cầu Mentor chọn course thuộc sở hữu/được phân công để tiếp tục luồng tạo lecture; API catalog #46 là `GET /api/v1/mentor/courses`, query `status/page/size`.
- **Current API #46:** router/module/test source hiện có. `MENTOR` Bearer guard chạy trước query; current query chỉ `courses.mentor_id = JWT sub` (direct owner), status tùy chọn `DRAFT|PUBLISHED`, page mặc định 1, size mặc định 20 và giới hạn 1–100. Sort cố định `created_at DESC, id ASC`; không có query tìm kiếm, level, kỳ học hay sort tùy chọn. Response trả Course cơ bản và pagination.
- **Skill routing:** đọc `.agents/context-manifest.json`; `createDD-markdown` loại trừ `web-ui-only-dd`, và registry không có skill UI-only. Không nạp API-DD skill như template cho screen UI.
- **Study Web:** source/package/router hiện không có trong checkout; ignored `dist` chỉ có route `/`. Mọi route màn hình vẫn `UNWIRED`, không suy ra từ HTML hoặc ảnh.

## 2. Khu vực marker dự kiến

Tọa độ dưới đây tính từ góc trái trên ảnh nguồn 1100×1600. Mỗi marker sẽ có một `ME02-EL-xx` duy nhất trong JSON và một hàng DD tương ứng. Repeated card element tách theo từng course để marker không che lẫn card khác.

| # | Element dự kiến | Điểm đặt dự kiến (x,y) |
|---:|---|---:|
| 1 | Brand/logo Mentor Portal | 12,15 |
| 2 | Primary navigation Mentor | 656,28 |
| 3 | Header search học viên/bài tập | 858,43 |
| 4 | Notification button và badge mẫu | 904,15 |
| 5 | Mentor avatar, tên và chức danh mẫu | 1087,58 |
| 6 | Breadcrumb Dashboard → ME-02 | 300,61 |
| 7 | Context kỳ học, đồng bộ LMS, mã Mentor | 950,61 |
| 8 | Page chip, tiêu đề và mô tả | 575,179 |
| 9 | CTA báo cáo học vụ tổng thể | 583,111 |
| 10 | CTA tạo bài giảng mới | 936,111 |
| 11 | KPI khóa phụ trách chính | 26,194 |
| 12 | KPI tổng học viên | 254,194 |
| 13 | KPI tỷ lệ hoàn thành trung bình | 482,194 |
| 14 | KPI chuẩn Capstone | 710,194 |
| 15 | Search khóa học/tên/mã | 311,332 |
| 16 | Filter status | 535,332 |
| 17 | Filter cấp độ | 681,332 |
| 18 | Sort theo học viên/tiến độ/cập nhật | 900,332 |
| 19 | Active-filter chips (status và kỳ học) | 27,426 |
| 20 | Xóa tất cả bộ lọc | 506,426 |
| 21 | Tổng số khóa hiển thị | 910,426 |
| 22 | Course 1: thumbnail, level/status, mã và rating | 310,452 |
| 23 | Course 1: title và description | 902,450 |
| 24 | Course 1: submission-count badge | 490,524 |
| 25 | Course 1: student/curriculum/lab/progress metrics | 910,578 |
| 26 | Course 1: action links quản lý/chấm/progress | 330,643 |
| 27 | Course 1: CTA Workspace ME-03 | 526,680 |
| 28 | Course 2: thumbnail, level/status, mã và rating | 310,744 |
| 29 | Course 2: title và description | 902,742 |
| 30 | Course 2: submission-count badge | 490,811 |
| 31 | Course 2: student/curriculum/lab/progress metrics | 910,872 |
| 32 | Course 2: action links quản lý/chấm/analytics | 330,932 |
| 33 | Course 2: CTA Workspace ME-03 | 526,974 |
| 34 | Course 3: thumbnail, level/status, mã và rating | 310,1032 |
| 35 | Course 3: title và description | 902,1034 |
| 36 | Course 3: submission-count badge | 490,1099 |
| 37 | Course 3: student/curriculum/case/progress metrics | 910,1164 |
| 38 | Course 3: action links quản lý/chấm/progress | 330,1212 |
| 39 | Course 3: CTA Workspace ME-03 | 934,1238 |
| 40 | Pagination summary | 321,1300 |
| 41 | First/previous/page/next/last controls | 625,1300 |
| 42 | Page-size selector | 930,1298 |
| 43 | Footer brand và giới thiệu | 238,1415 |
| 44 | Footer tiêu chuẩn học thuật | 473,1415 |
| 45 | Footer liên kết viện-trường | 696,1415 |
| 46 | Footer hỗ trợ Mentor | 933,1415 |
| 47 | Copyright, certification và policy links | 950,1568 |

## 3. Event/source trace cần hoàn thiện

| Event | Trigger / luồng cần đặc tả | Source/gate |
|---|---|---|
| ME02-EV-01 | Vào page, auth và tải danh sách; loading/ready/empty/error/denied | #46 + current Mentor guard; Study Web route/session `UNWIRED` |
| ME02-EV-02 | Nhập search tên/mã course | #46 không có `q`/course-code field; không được gửi filter chưa hỗ trợ |
| ME02-EV-03 | Đổi status | API chỉ nhận đúng `DRAFT` hoặc `PUBLISHED`; UI labels không map rõ |
| ME02-EV-04 | Đổi level | Không có field/filter level trong #46 response/query |
| ME02-EV-05 | Đổi sort | Không có `sort` query; source order cố định theo created_at/id |
| ME02-EV-06 | Bỏ từng active-filter chip | HTML dùng CSS `:contains()` trong `querySelectorAll`, selector không hợp lệ; filter semantics chưa có contract |
| ME02-EV-07 | Xóa toàn bộ filter | Reset policy cho URL/page/status và unsupported filters chưa có; app/router `UNWIRED` |
| ME02-EV-08 | Chuyển trang/đổi page size | #46 hỗ trợ `page`, `size`; page>=1, size 1–100; xử lý stale response/cache chưa có UI source |
| ME02-EV-09 | Mở Workspace (ME-03) | Cần `Course.id` từ #46; route là proposal, client chưa wired |
| ME02-EV-10 | Mở quản lý nội dung (asset ghi ME-06) | Course ID cần truyền; inventory ME-02 chỉ liệt kê ME-03/ME-04/ME-16; xác nhận direct route hay đi qua ME-03 |
| ME02-EV-11 | Mở chấm bài (asset ghi ME-09) | Không có trong links ME-02 inventory; #54 nhận `course_id` nhưng không tạo route UI |
| ME02-EV-12 | Mở tiến độ học viên/analytics | ME-16/#65 trả progress từng Student; #66 activity proxy. Chỉ là source-backed dependency candidate, không xác nhận direct CTA |
| ME02-EV-13 | Tạo bài giảng mới | Route ME-04 yêu cầu `courseId`; CTA tổng không chỉ định course; cần chọn course/context |
| ME02-EV-14 | Xem báo cáo học vụ tổng thể | Destination/API/report period chưa có; #66 yêu cầu một `course_id` và trả activity proxy |
| ME02-EV-15 | Điều hướng qua header/breadcrumb | HTML anchors `#`; route proposals phải lấy từ inventory; không có client router |
| ME02-EV-16 | Header search, notification, profile | Search/API, unread notification, Mentor profile route/data chưa có nguồn cho ME-02 |

## 4. Blocker dự kiến

- `ME02-B01`: ownership/assignment semantics khác nhau giữa AC-21 và direct-owner predicate trong #46; không hiển thị course được assign nếu server chưa trả.
- `ME02-B02`: Study Web route/session shell vắng mặt; không có runtime interaction.
- `ME02-B03`: KPI tổng học viên/completion/Capstone, ratings, pending submission và “active course” không có trong response #46; #62/#65/#66 chỉ cung cấp các projection khác grain/ý nghĩa.
- `ME02-B04`: search tên/mã, level filter, semester filter và sort trong mockup không được #46 hỗ trợ.
- `ME02-B05`: status nhãn nghiệp vụ trong UI không ánh xạ được enum current `DRAFT|PUBLISHED`; không tự map `active/upcoming/archived`.
- `ME02-B06`: API #46 source có route nhưng API DD snapshot vẫn ghi `UNWIRED/NOT_FOUND`; giữ discrepancy, không coi Draft snapshot là current behavior.
- `ME02-B07`: direct CTA ME-06/ME-09 và overall report chưa khớp link inventory/route; “Tạo bài giảng mới” thiếu course ID.
- `ME02-B08`: pagination screenshot chọn 10/trang; API default 20; cần chốt UI default và empty/out-of-range presentation.
- `ME02-B09`: prototype dùng CDN/Plus Jakarta Sans, primary `#004ac6`, controls 32–40px, content 1440px; khác intended Study guide (Ocean #0B5F8A, Inter/system, controls >=44px, content ~1120px).
- `ME02-B10`: sample course code, title, level, rating, students, lectures/labs/progress, review and notice/support details không được xác nhận bởi API #46.

## 5. Verification plan và sequencing

1. **Plan first:** hoàn tất file này trước DD, JSON marker map hoặc ảnh chú thích.
2. Tạo `ME-02_markers.json` với 47 marker duy nhất, source pixel coordinates, element labels và mapping IDs.
3. Tạo SVG overlay + `screen_annotated.png` từ `screen.png`; kiểm tra kích thước/ratio, marker bounds, số marker và bố cục không che nội dung chính; mở ảnh kiểm tra trực quan.
4. Viết `ME-02.md`: overview/preconditions, expected/current separation, caller→guard→query/count/page→mapper→response/errors→test source trace, 47 element rows, event-by-event input/process/output/blocker, API mapping, states, navigation, security/accessibility, acceptance checklist.
5. Cập nhật đúng ME-02 row và current progress section trong `dd_screens/PLAN.md`; chỉ tăng số bộ file hiện diện, không đếm thành `DD READY`.
6. Ghi worklog preflight paths, source evidence, discrepancies, files và verification; chạy static artifact/link/whitespace checks. Không chạy app tests hoặc runtime.

### Static pass criteria

- Original PNG/HTML hashes không đổi; new annotated image đúng tỷ lệ với source.
- JSON chứa đủ marker #1–#47, ID `ME02-EL-01..47` duy nhất và tọa độ trong ảnh.
- DD có đúng 47 element ID rows ánh xạ marker; mỗi event có trigger/input/preconditions/steps/output/errors hoặc blocker.
- SVG và annotated image cùng thể hiện 47 markers; ảnh được xem trực tiếp.
- Relative Markdown links resolve; status trong DD/plan/worklog nhất quán.

### Status at plan completion

- `DD`: chưa soạn; dự kiến **BLOCKED** bởi các quyết định dữ liệu/route/filter trong B01–B10.
- `IMPLEMENTATION`: **BLOCKED** bởi source/UI wiring absent và unsupported fields/actions.
- `RUNTIME`: **NOT VERIFIED**.
- No source/API/DB implementation changes are in scope.
