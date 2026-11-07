# ME-03 — Kế hoạch DD: Workspace khóa học của mentor

> **Plan status:** COMPLETE — lập trước marker map, ảnh chú thích và DD.
> **Screen status:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

## 1. Phạm vi và bằng chứng

- **Screen ID / route đề xuất:** ME-03 — `/mentor/courses/:courseId`; actor Mentor.
- **Expected:** `list_screen.md` ME-03 row; AC-22 workspace nội dung và AC-26 theo dõi tiến độ. Inventory chỉ định GET #49 và #65 sau khi xác định course qua ME-02/#46; liên kết ME-04, ME-06, ME-16; expected states loading/no-content/partial/error.
- **Current assets:** `screen.png` 1234×1600, SHA-256 `4874aa947cdbb6526c4dda6fb29603cfa6e9ed88f644ac335966e9aa4fefbcb7`; `code.html` 43,129 bytes, SHA-256 `268bb2385f79d049f3d2d77ce6ebc95333b33694f835dfcd5f1a11953cffdde5`. Giữ nguyên cả hai. HTML là mockup tĩnh, 12 anchor `href="#"`, 15 button, một input; không form, fetch/XHR, event listener hay API binding.
- **API #49 current source:** GET `.../mentor/courses/{course_id}/content`, `MENTOR` Bearer JWT, signed-int64 path; direct owner `courses.mentor_id = JWT sub`; trả flat `Content[]` active rows, mọi status, `parent_id` liên kết node, không pagination. Empty là 200 `DESIGN_RESOURCE_RETRIEVED`; lỗi 401/403/404/500. Content type/status/payload subtype và revision semantics còn mở.
- **API #65 current source:** GET `.../mentor/courses/{course_id}/progress`, cùng guard/path/direct-owner predicate; trả local derived `Page<MentorStudentProgress>` cho toàn ACTIVE Student roster và PUBLISHED lesson denominator. Formula floor-average; không page/size, module/event/risk/rating data. Catalog vẫn `Page<Course>`; response, eligibility/formula và unbounded page còn chờ duyệt. Errors 401/403/404/500.
- **UI source status:** Study Web không có editable `src/`, `package.json` hoặc router; route runtime `UNWIRED`. PNG/HTML có dữ liệu mẫu: course metadata, module KPIs, risk/actions, activity, quality, repositories, AI callout và Excel export mà #49/#65 không cung cấp.
- **Design target:** `.agents/web-study/design.md` là intended UI target: Ocean palette, Inter/system font, responsive 1120px content, controls ≥44px and accessible state/focus. Mockup dùng Plus Jakarta Sans/Tailwind CDN, palette khác, nội dung dày và controls nhỏ; ghi nhận là design discrepancy, không coi là source runtime.

## 2. Kế hoạch marker

Tọa độ tính trên ảnh nguồn 1234×1600, gốc trên-trái; ảnh chú thích xuất 2× (2468×3200). Mỗi marker có một hàng cùng ID trong DD và một node trong JSON/SVG. Nhóm danh sách lặp chỉ gom khi cùng một container/hành vi; module, risk row và repository item được tách riêng.

| # | Element dự kiến | Điểm đặt (x,y) |
|---:|---|---:|
| 1 | Brand/logo Mentor Portal | 14,22 |
| 2 | Điều hướng Mentor toàn cục | 245,46 |
| 3 | Header search học viên/bài tập | 733,15 |
| 4 | Notification button và badge | 997,18 |
| 5 | Mentor avatar/tên/chức danh mẫu | 1210,52 |
| 6 | Breadcrumb quay về ME-02 | 15,56 |
| 7 | Nhãn API synchronized và cohort | 1090,87 |
| 8 | Mã course, status, lần cập nhật | 33,122 |
| 9 | Course title | 745,181 |
| 10 | Mentor, số học viên, chuẩn học thuật | 790,212 |
| 11 | Average progress và chênh cohort | 1018,223 |
| 12 | CTA tạo bài giảng ME-04 | 40,245 |
| 13 | CTA cây nội dung ME-06 | 252,245 |
| 14 | CTA bảng chấm bài ME-09 | 470,245 |
| 15 | CTA gửi thông báo ME-14 | 687,245 |
| 16 | CTA báo cáo tiến độ ME-16 | 890,245 |
| 17 | Làm mới số liệu | 973,293 |
| 18 | Xuất dữ liệu Excel | 1010,293 |
| 19 | Heading tổng quan cấu trúc chương trình | 16,344 |
| 20 | Tile số chương học | 210,405 |
| 21 | Tile bài giảng đã duyệt | 400,405 |
| 22 | Tile bản nháp đang sửa | 576,405 |
| 23 | Heading phân bố tiến độ theo module | 16,548 |
| 24 | Module 1 card/progress | 590,617 |
| 25 | Module 2 card/progress | 590,708 |
| 26 | Module 3 card/progress | 590,802 |
| 27 | Module 4/Capstone card | 590,897 |
| 28 | Weekly learning-velocity metric | 16,976 |
| 29 | Weekly activity line chart | 592,1062 |
| 30 | Heading hoạt động học vụ gần nhất | 16,1118 |
| 31 | Ba dòng activity sample | 590,1301 |
| 32 | CTA xem toàn bộ hoạt động | 541,1098 |
| 33 | Heading danh sách cần quan tâm | 1016,343 |
| 34 | Risk threshold/count summary | 1040,381 |
| 35 | At-risk Student row 1 | 1043,415 |
| 36 | At-risk Student row 2 | 1043,516 |
| 37 | At-risk Student row 3 | 1043,608 |
| 38 | CTA xem toàn bộ at-risk learners | 1028,674 |
| 39 | Heading chất lượng bài giảng | 1016,748 |
| 40 | Satisfaction rating/reviews tile | 1045,827 |
| 41 | Chapter drop-off tile | 1045,874 |
| 42 | Materials satisfaction progress | 1045,923 |
| 43 | Code-review response KPI | 1045,966 |
| 44 | Heading kho tài nguyên/repository | 1016,1025 |
| 45 | Repository item Git | 1035,1072 |
| 46 | Repository item Figma | 1035,1131 |
| 47 | Repository item Sandbox | 1035,1193 |
| 48 | AI Mentor Copilot callout | 1040,1281 |
| 49 | Footer brand/introduction | 20,1377 |
| 50 | Footer academic standards | 395,1378 |
| 51 | Footer partner network | 650,1378 |
| 52 | Footer Mentor support | 900,1378 |
| 53 | Copyright/certification/policy links | 1215,1585 |

## 3. Event/source trace plan

| Event | Trigger / intended flow | Source / gate |
|---|---|---|
| ME03-EV-01 | Enter route, validate `courseId` context | Route proposed; no Study Web router. #49/#65 independently validate signed-int64 and direct owner. |
| ME03-EV-02 | Load curriculum tree | API #49; no body/query; read-only; 200 flat `Content[]` or 401/403/404/500. |
| ME03-EV-03 | Load class progress roster | API #65; no body/query; current response locally DERIVED, unlike catalog `Page<Course>`. |
| ME03-EV-04 | Compose loading/empty/partial/error state | Inventory defines states; independent-request ordering, partial semantics, retry/cache and shared-denial UI are not approved. |
| ME03-EV-05 | Refresh data | Prototype title indicates refresh; proposed refetch #49/#65, but focus/cancel/error policy is not sourced. |
| ME03-EV-06 | Export Excel | No ME-03 export API/file contract. Blocked. |
| ME03-EV-07 | Create lecture | Navigate to ME-04 with current `courseId`; target route is proposed; API #34/#47 handled by ME-04, not called here. |
| ME03-EV-08 | Open content tree | Navigate to ME-06 with `courseId`; inventory link and route proposal; client wiring absent. |
| ME03-EV-09 | Open grading queue | Prototype ME-09 action; not a ME-03 inventory link. Do not claim course filter or route handoff without approval. |
| ME03-EV-10 | Send reminder | Prototype ME-14 action; no recipient/notification orchestration in ME-03 contract. |
| ME03-EV-11 | Schedule one-on-one | No route/API/scheduling contract found in ME-03 inventory. |
| ME03-EV-12 | Open full at-risk list | No target screen/API/eligibility definition in ME-03 contract. |
| ME03-EV-13 | Open rubric | Prototype points to ME-09; route/data and permission handoff not in ME-03 inventory. |
| ME03-EV-14 | Open full activity feed or activity row | No activity list endpoint or destination in ME-03 inventory. |
| ME03-EV-15 | Open repository item | Source anchors are `#`; URL allowlist, external-link policy and source-of-truth are absent. |
| ME03-EV-16 | Open/use AI Mentor Copilot | Sample claim has no API, workflow or AI output evidence in ME-03 contract. |
| ME03-EV-17 | Header search / notification | No matching ME-03 search or unread-notification source; header controls are static. |
| ME03-EV-18 | Global navigation, breadcrumb and footer links | Use only inventory route proposals; current HTML anchors are `#`; history/return-state policy absent. |

## 4. Blockers and acceptance gate

- **ME03-B01 — access contract:** AC-22/AC-26 say Mentor has management/analytics permission; #49/#65 only enforce `MENTOR` role and direct owner. Assigned Mentor branch in AC-21/#46 is not supported. Resolve before route access behavior can be DD READY.
- **ME03-B02 — course summary:** no Mentor course detail API supplies code/cohort/standard/enrollment/update summary; #46 is paginated and has only basic Course fields. Direct entry and refresh context need an approved source.
- **ME03-B03 — API #65 contract:** catalog response `Page<Course>` conflicts with current derived `Page<MentorStudentProgress>`; full-roster page has no request bound. Owner approval/schema update is required.
- **ME03-B04 — unsupported panels:** per-module progress, student risk, weekly event feed, ratings/drop-off, repo resources, AI summary and Excel export are not produced by #49/#65 or listed as ME-03 APIs.
- **ME03-B05 — #49 semantics:** Content type/status/payload subtype and revision/publish rules remain open; flat Content tree is not verified as lesson/module structure.
- **ME03-B06 — client/runtime:** Study Web route/session/API wiring is absent; mockup labels and anchor destinations are not functional evidence.
- **ME03-B07 — visual/accessibility:** mockup tokens/font/control density conflict with the intended Study design guide; resolve during UI implementation planning.

Plan is accepted when: source hashes are preserved; all planned markers align once across plan/JSON/SVG/image/DD; every visible interactive/sample-data region is covered; API calls and error/status behavior trace to current source; unsourced behaviors stay blocked; relative links resolve; tracker and worklog separate DD, implementation and runtime states. Tests and runtime are not part of this docs-only verification.
