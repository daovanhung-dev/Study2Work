# ST-17 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-17_markers.json](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-17-EL-001` | `ST17-EL-01` | Header Study2Work logo and brand |
| #2 | `ST-17-EL-002` | `ST17-EL-02` | Primary navigation links |
| #3 | `ST-17-EL-003` | `ST17-EL-03` | Notifications control |
| #4 | `ST-17-EL-004` | `ST17-EL-04` | Student avatar and profile control |
| #5 | `ST-17-EL-005` | `ST17-EL-05` | Breadcrumb trail |
| #6 | `ST-17-EL-006` | `ST17-EL-06` | Assignment status, code and project-category chips |
| #7 | `ST-17-EL-007` | `ST17-EL-07` | Assignment title |
| #8 | `ST-17-EL-008` | `ST17-EL-08` | Assignment summary and description |
| #9 | `ST-17-EL-009` | `ST17-EL-09` | Progress and maximum-score summary |
| #10 | `ST-17-EL-010` | `ST17-EL-10` | Due-date summary |
| #11 | `ST-17-EL-011` | `ST17-EL-11` | Time-remaining summary |
| #12 | `ST-17-EL-012` | `ST17-EL-12` | Assigned mentor summary |
| #13 | `ST-17-EL-013` | `ST17-EL-13` | Grading SLA summary |
| #14 | `ST-17-EL-014` | `ST17-EL-14` | Video preview card |
| #15 | `ST-17-EL-015` | `ST17-EL-15` | Core objectives heading and introduction |
| #16 | `ST-17-EL-016` | `ST17-EL-16` | Objective card: Virtualization and Rendering |
| #17 | `ST-17-EL-017` | `ST17-EL-17` | Objective card: server-side filtering and debounce |
| #18 | `ST-17-EL-018` | `ST17-EL-18` | Objective card: dynamic RBAC |
| #19 | `ST-17-EL-019` | `ST17-EL-19` | Objective card: dynamic interface behavior |
| #20 | `ST-17-EL-020` | `ST17-EL-20` | Rubric heading and score summary |
| #21 | `ST-17-EL-021` | `ST17-EL-21` | Rubric criterion A: React architecture and TypeScript |
| #22 | `ST-17-EL-022` | `ST17-EL-22` | Rubric criterion B: state and query-cache engine |
| #23 | `ST-17-EL-023` | `ST17-EL-23` | Rubric criterion C: Lighthouse performance and Core Web Vitals |
| #24 | `ST-17-EL-024` | `ST17-EL-24` | Rubric criterion D: automated testing and Playwright E2E |
| #25 | `ST-17-EL-025` | `ST17-EL-25` | Attached resources heading and introduction |
| #26 | `ST-17-EL-026` | `ST17-EL-26` | Starter Kit resource and download action |
| #27 | `ST-17-EL-027` | `ST17-EL-27` | Figma specification resource and action |
| #28 | `ST-17-EL-028` | `ST17-EL-28` | API mock-data resource and action |
| #29 | `ST-17-EL-029` | `ST17-EL-29` | Submission requirements heading and introduction |
| #30 | `ST-17-EL-030` | `ST17-EL-30` | GitHub repository delivery requirement |
| #31 | `ST-17-EL-031` | `ST17-EL-31` | Vercel live-preview delivery requirement |
| #32 | `ST-17-EL-032` | `ST17-EL-32` | Technical PDF report delivery requirement |
| #33 | `ST-17-EL-033` | `ST17-EL-33` | Late-submission penalty notice |
| #34 | `ST-17-EL-034` | `ST17-EL-34` | Submission status card |
| #35 | `ST-17-EL-035` | `ST17-EL-35` | Deadline countdown and displayed deadline |
| #36 | `ST-17-EL-036` | `ST17-EL-36` | Compose and submit assignment action |
| #37 | `ST-17-EL-037` | `ST17-EL-37` | Pre-submit checklist heading and completion count |
| #38 | `ST-17-EL-038` | `ST17-EL-38` | Checklist item 1: responsive dashboard/report |
| #39 | `ST-17-EL-039` | `ST17-EL-39` | Checklist item 2: virtualization and test data |
| #40 | `ST-17-EL-040` | `ST17-EL-40` | Checklist item 3: Lighthouse score |
| #41 | `ST-17-EL-041` | `ST17-EL-41` | Checklist item 4: technical PDF |
| #42 | `ST-17-EL-042` | `ST17-EL-42` | Academic-integrity commitment note |
| #43 | `ST-17-EL-043` | `ST17-EL-43` | Mentor portrait, name and role |
| #44 | `ST-17-EL-044` | `ST17-EL-44` | Mentor biography |
| #45 | `ST-17-EL-045` | `ST17-EL-45` | Discord support action |
| #46 | `ST-17-EL-046` | `ST17-EL-46` | Office-hours scheduling action |
| #47 | `ST-17-EL-047` | `ST17-EL-47` | Submission history summary |
| #48 | `ST-17-EL-048` | `ST17-EL-48` | Footer brand, description and certifications |
| #49 | `ST-17-EL-049` | `ST17-EL-49` | Footer navigation and legal links |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả elements

Marker badges nằm ngoài ảnh nguồn trong hai gutter trắng. `x/y` trong [marker map](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17_markers.json) là tọa độ target trên ảnh gốc 667×1600; `badge_x/badge_y` là tọa độ badge trên annotation canvas. Giá trị hiển thị trong PNG là sample trừ khi được API/source hỗ trợ.

| # / Element ID | Tên, loại, vị trí và mục đích | Data, thuộc tính, điều kiện hiển thị và trạng thái | Event |
|---|---|---|---|
| 1 / `ST17-EL-01` | Logo/brand Study2Work ở header trái; brand link. | Hình tĩnh trong PNG; link `/` chỉ có trong prototype HTML, không chứng minh router. | `EV-07` |
| 2 / `ST17-EL-02` | Nhóm điều hướng header: Trang chủ, Khóa học, Khóa học của tôi, Lộ trình, Diễn đàn. | Destinations/auth gating chưa được xác minh trong Study Web; Guest HTML có tập link khác. | `EV-07` |
| 3 / `ST17-EL-03` | Notification icon/badge. | Count/destination không có trong #33 hoặc inventory ST-17; design-only. | `EV-07` |
| 4 / `ST17-EL-04` | Student avatar/name/profile. | “Nguyen Hanh / Học viên” là sample; identity phải tới từ auth/profile source được duyệt, không chứng minh assignment permission. | `EV-07` |
| 5 / `ST17-EL-05` | Breadcrumb links: Khóa học của tôi → Chuyên gia Frontend React & TypeScript → Đồ án. | `course_id` có thể có trong #33 nhưng course title và route mapping không có; ST-09 là related, không tự động là breadcrumb target. | `EV-07` |
| 6 / `ST17-EL-06` | Chip trạng thái Open, mã FE-CAPSTONE-101 và loại Dự án trọng tâm. | #33 không có status, code hoặc category; mọi giá trị là sample; không render làm server state. | `EV-02` |
| 7 / `ST17-EL-07` | Heading tên assignment. | Có thể map logical `Assignment.title:string`; response chưa wired, source mapping Draft. | `EV-02` |
| 8 / `ST17-EL-08` | Mô tả ngắn dưới heading. | Có thể map optional `Assignment.description:string`; null/omit handling chưa chốt; không tự thêm rich-text rendering. | `EV-02` |
| 9 / `ST17-EL-09` | Panel tỷ trọng/progress và max score. | #33 chỉ có `max_score:decimal-string`; 20% tổng kết/progress/100 điểm là sample, chưa có weight/progress contract. | `EV-02` |
| 10 / `ST17-EL-10` | Due-date summary card. | Candidate `due_at?:date-time`; optional null/omit và timezone không được định nghĩa. | `EV-03` |
| 11 / `ST17-EL-11` | “Còn lại 5 ngày” summary. | Không phải API field; nếu được phép tính, cần timezone/clock source đã duyệt; screenshot count là sample. | `EV-03` |
| 12 / `ST17-EL-12` | Assigned mentor summary. | Mentor name/source/ownership absent from `Assignment`; sample only. | `EV-02` |
| 13 / `ST17-EL-13` | SLA phản hồi/chấm bài. | No API #33 field or approved grading-time policy; “48h” là sample. | `EV-02` |
| 14 / `ST17-EL-14` | Video preview card, title and apparent play surface. | No video URL/resource field in #33; play/open behavior and access rule unspecified. | `EV-05` |
| 15 / `ST17-EL-15` | Section “Mục tiêu & Yêu cầu cốt lõi” and intro paragraph. | Editorial requirement content is not represented by #33 except possibly unstructured description; no section schema. | `EV-02` |
| 16 / `ST17-EL-16` | Objective card “Virtualization & Rendering”. | Copy/criteria are screenshot samples; no rubric/objective collection in #33. | `EV-02` |
| 17 / `ST17-EL-17` | Objective card “Server-side Filtering & Debounce”. | Copy/criteria are screenshot samples; no rubric/objective collection in #33. | `EV-02` |
| 18 / `ST17-EL-18` | Objective card “Phân quyền RBAC động”. | Copy/criteria are screenshot samples; no rubric/objective collection in #33. | `EV-02` |
| 19 / `ST17-EL-19` | Objective card “Cơ chế hiển thị giao diện động”. | Copy/criteria are screenshot samples; no rubric/objective collection in #33. | `EV-02` |
| 20 / `ST17-EL-20` | Rubric heading, total score and “4 trục kỹ năng” summary. | No rubric schema in `Assignment`; max score alone cannot produce total bands/axes. | `EV-02` |
| 21 / `ST17-EL-21` | Rubric criterion A — React 19 Architecture & TypeScript Strict Mode. | Criterion description/25-point value are sample; no rubric API or relation confirmed for #33. | `EV-02` |
| 22 / `ST17-EL-22` | Rubric criterion B — Zustand State & TanStack Query Cache Engine. | Criterion description/25-point value are sample; no rubric API or relation confirmed for #33. | `EV-02` |
| 23 / `ST17-EL-23` | Rubric criterion C — Lighthouse Performance/Zero CLS. | Criterion description/25-point value are sample; no rubric API or relation confirmed for #33. | `EV-02` |
| 24 / `ST17-EL-24` | Rubric criterion D — Automated Testing/Playwright E2E. | Criterion description/25-point value are sample; no rubric API or relation confirmed for #33. | `EV-02` |
| 25 / `ST17-EL-25` | Attached-resources heading and intro. | #33 has no resource collection or upload metadata. | `EV-05` |
| 26 / `ST17-EL-26` | Starter Kit row and download action. | Filename, size, URL, expiry and entitlement are not in #33; do not manufacture a download. | `EV-05` |
| 27 / `ST17-EL-27` | Figma spec row/action. | External destination/file ID/access is absent from #33 and inventory. | `EV-05` |
| 28 / `ST17-EL-28` | API mock-data row/action. | File name/size/download route are sample; no resource API in ST-17 contract. | `EV-05` |
| 29 / `ST17-EL-29` | Submission requirements heading and intro. | No structured submission-rule fields in `Assignment`; AC-17 rule source is unresolved. | `EV-02` |
| 30 / `ST17-EL-30` | GitHub Repository delivery criterion. | Sample requirement/URL; no field or validation policy in #33. | `EV-02` |
| 31 / `ST17-EL-31` | Vercel Live Preview delivery criterion. | Sample requirement/URL; no field or validation policy in #33. | `EV-02` |
| 32 / `ST17-EL-32` | Technical PDF report criterion. | Sample requirement/file; no field, format or validation policy in #33. | `EV-02` |
| 33 / `ST17-EL-33` | Late-submission penalty note. | “10%/24h” rule is not in #33/Assignment and is not approved; do not calculate or promise a penalty. | `EV-03` |
| 34 / `ST17-EL-34` | Sidebar status “Chưa nộp bài (Not Submitted)”. | `Assignment` has no submission status; no #36 `submission_id` is available from this screen. | `EV-02` |
| 35 / `ST17-EL-35` | Deadline countdown box/date. | Days/hours/minutes/seconds and date are sample. Server policy/timezone/boundary unresolved; countdown cannot enable/deny submission. | `EV-03` |
| 36 / `ST17-EL-36` | “Soạn và Nộp bài tập ngay” primary CTA. | Proposed transition to ST-18 with assignment path ID if eligibility is approved; no current frontend route. | `EV-06` |
| 37 / `ST17-EL-37` | Pre-submit checklist heading and 0/4 count. | Count/state/persistence not in #33 or inventory; cannot compute from rubric or submission status. | `EV-04` |
| 38 / `ST17-EL-38` | Checklist item 1 — responsive dashboard/report. | Checkbox-like sample UI; no completion source or save behavior. | `EV-04` |
| 39 / `ST17-EL-39` | Checklist item 2 — virtualization/test data. | Checkbox-like sample UI; no completion source or save behavior. | `EV-04` |
| 40 / `ST17-EL-40` | Checklist item 3 — Lighthouse score. | Checkbox-like sample UI; no completion source or save behavior. | `EV-04` |
| 41 / `ST17-EL-41` | Checklist item 4 — PDF. | Checkbox-like sample UI; no completion source or save behavior. | `EV-04` |
| 42 / `ST17-EL-42` | Integrity/commitment note. | Static copy in PNG; no policy identifier or acknowledgement contract. | `EV-02` |
| 43 / `ST17-EL-43` | Mentor profile image/name/role. | No mentor object in `Assignment`; name/avatar/role are samples. | `EV-02` |
| 44 / `ST17-EL-44` | Mentor biography. | No biography field in #33; sample editorial content. | `EV-02` |
| 45 / `ST17-EL-45` | Discord support action. | Contact target, authorization and external destination not supplied by #33/inventory. | `EV-05` |
| 46 / `ST17-EL-46` | Office-hours scheduling action. | Calendar/booking route/timezone unavailable; do not activate based on screenshot. | `EV-05` |
| 47 / `ST17-EL-47` | Submission history row/count. | #33 does not return submission ID/status/history; #36 requires a known submission ID and is not a list query. | `EV-02` |
| 48 / `ST17-EL-48` | Footer brand/description/certification badges. | Static marketing/certification content; not derived from assignment data. | `EV-07` |
| 49 / `ST17-EL-49` | Footer navigation/legal link group. | HTML contains placeholder `#` links and current destination behavior is unverified. | `EV-07` |

## 4. Conditional UI & state variations
- States theo inventory: loading/open/closed/not-found
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
