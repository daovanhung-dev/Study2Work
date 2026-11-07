# ST-08 — Kế hoạch chi tiết

> Kế hoạch ban đầu: 2026-11-06; rà soát bổ sung: 2026-11-07
>
> Trạng thái: PLAN COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED

## 0. Rà soát bổ sung 2026-11-07 (phiên sau ST-07)

- Phiên hiện tại vẫn chỉ rà soát **ST-08**. Bộ artifact của ST-08 đã tồn tại trước phiên này; phần kế hoạch ngày 2026-11-06 ghi lại lần dựng đầu tiên. Không dựng lại ảnh/marker nếu kiểm tra tĩnh hiện tại không phát hiện lỗi; giữ nguyên PNG/HTML nguồn.
- Hash hiện tại: `screen.png` `665e39c4c1de2cbe417ce092b269aaaa4adc807fc0bb534c2714ab9f2213c21a`; `code.html` `7b8effee5a5ee1dfd7a0ebb5a051af5710785ac0f0c452863fb2b9e057c2298f`; `screen_rendered.png` `95d1f7bacd0ff05ebf9db81f970fc775afbdece30eb10d7374ecf2f551d12ab9`; `screen_annotated.png` `59ce04ce833c65db94fd0768b4a9c62acc8ae07a851952f28b3921c0fe564cdc`. Dimensions lần lượt: 1280×1024, 1280×1024, 1280×1024, 2720×2048. Ảnh gốc không có header và có dải đen dưới footer; HTML render vẫn là ảnh tĩnh, không phải runtime.
- Rà soát lại inventory, AC-13, API catalog/DD #20/#21, Study Server route/module/test source, Study Web tree, design guide và DDL xác nhận các blocker gốc vẫn còn: #20/#21 chưa có route/module/query/test; response catalog `ApiEnvelope<UserProfile>` không biểu diễn course/progress; Study Web thiếu source/router; filter và loaded UI không có trong asset.
- Bổ sung blocker cần được phản ánh vào DD/tracker: (1) AC-13 ghi `NO → empty state; YES → render` nhưng hai cạnh `EMPTY` và `HAS DATA` cùng trỏ đến node “Hiển thị khóa học + % hoàn thành”; (2) DDL legacy BIGINT `enrollments`/`lesson_progress` khác DDL V1-PILOT UUID `course_enrollments`/`lesson_progress_facts`/`progress_snapshots`, và không có bằng chứng live schema; (3) HTML dùng Google Fonts/Tailwind CDN, Plus Jakarta Sans, `max-w-[1440px]`, primary cobalt `#004AC6` và header blur; Study Web guide định hướng Inter/system, không thêm remote import, ocean primary `#0B5F8A`, không dùng glass effect và chiều rộng khoảng 1120px.
- DD update scope: make its required content explicit under A–F headings (overview, flow, elements, events including API, state/navigation, acceptance); add the verified AC branch, schema-generation and design-system discrepancies; retain the existing 9-marker mapping and source assets if the static audit passes.
- Trước khi cập nhật marker map hoặc tracker, kế hoạch kiểm tra: xác minh lại hash/dimensions; parse JSON/SVG; đối chiếu 9 marker có thứ tự với 9 element row và ảnh; kiểm tra link Markdown; giữ trạng thái `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`; cập nhật ST-08 DD/inventory/global plan/worklog. Không chạy app/API tests hoặc runtime.

## 1. Phạm vi và phân loại

```text
primary_task_type: docs
secondary_task_types: []
project_scopes: [web-work, server-study]
cross_scope_dependencies: [ST-08 APIs #20/#21; Student session from SH-02; navigation to ST-09 and ST-20]
```

- Chỉ xử lý **ST-08 — Khóa học của tôi (Page)** trong phiên này.
- Inventory: route đề xuất /student/courses; AC-13; APIs #20/#21; actor Student; liên kết ST-09 và ST-20. Expected behavior là danh sách khóa đã ghi danh, filter trạng thái và progress.
- Inventory orchestration: GET #20 với page/status; GET #21 nếu cần progress chưa được response #20 cung cấp; merge theo course_id. AC-13 yêu cầu gọi #20 và #21 rồi hiển thị khóa học kèm tiến độ.
- Theo dd_screens/PLAN.md, ST-08 theo thứ tự W1 sau ST-03. Không làm Screen ID khác trong phiên này.
- Registry/manifest loại trừ web-ui-only-dd khỏi createDD-markdown; không có skill canonical cho UI-only DD. Không áp API DD template cho screen DD.

## 2. Asset baseline và hướng annotation

- Thư mục trước phiên có screen.png và code.html; chưa có ST-08_PLAN.md, ST-08.md, marker map hoặc ảnh đánh số.
- screen.png là PNG 1280×1024, SHA-256 665e39c4c1de2cbe417ce092b269aaaa4adc807fc0bb534c2714ab9f2213c21a. Ảnh có vùng trắng trống phía trên, main empty-state ở giữa và dải đen lớn dưới footer; header/navigation không hiện, nên không thể dùng làm ảnh toàn bộ page.
- code.html là HTML tĩnh hợp lệ, SHA-256 7b8effee5a5ee1dfd7a0ebb5a051af5710785ac0f0c452863fb2b9e057c2298f. Firefox headless render tạm tại 1280×1024 cho thấy header/nav, heading, empty-state card và footer đầy đủ. Bản render ở /tmp/st08_render.png được xem để so sánh; nó là render HTML tĩnh, không phải app runtime.
- Kế hoạch: giữ nguyên screen.png và code.html; tạo screen_rendered.png từ code.html như ảnh hiển thị đầy đủ có provenance; tạo screen_annotated.png bằng cách đánh số trên screen_rendered.png. Không sửa HTML để biến anchor tĩnh thành runtime.
- 9 planned markers: (1) header brand, (2) primary navigation, (3) page title, (4) empty-state surface/illustration, (5) empty-state heading, (6) explanatory copy, (7) CTA xem tiến độ, (8) footer brand, (9) footer navigation.
- Status filter, course cards, progress bars và pagination không xuất hiện trong PNG hoặc HTML; không tạo marker cho phần tử không có thiết kế. Ghi gap này đối với inventory/AC-13.

## 3. Expected behavior và current evidence

| Chủ đề | Expected/design source | Current evidence | Tác động |
|---|---|---|---|
| Actor/route | Student đăng nhập; route đề xuất /student/courses; AC-13 cho phép có thể chưa có enrollment. | Study Web không có app source/package/router/entrypoint. HTML có href thật nhưng không có router runtime trong checkout. | Không khẳng định session guard, route history hoặc live navigation. |
| Courses | API #20 theo catalog có status/page query; AC-13 mong Enrollment + Course list. | API #20 route/module/query/test không có trong Study Server source/tests. API DD Draft giữ response ApiEnvelope<UserProfile>, không map được course collection. | DISCREPANCY/BLOCKER; không thiết kế Course card payload như thể đã có contract. |
| Progress | AC-13 gọi API #21 để ghép progress; inventory nói gọi khi cần. | API #21 route/module/query/test không có source. Query grammar mơ hồ, response vẫn ApiEnvelope<UserProfile>, không có aggregate schema/formula. | DISCREPANCY/BLOCKER; không bịa progress %, denominator hoặc merge result. |
| Empty state | AC-13 diagram có nhánh empty khi không có khóa học sau khi ghép API results. | PNG/HTML hiển thị static empty copy “chưa có khóa học hoặc dữ liệu chưa cập nhật”; không fetch/API state. | Đây là design state, không phải kết quả API thật; wire empty shape chưa được chốt. |
| Filter/status/progress | Inventory mô tả lọc status và thanh tiến độ. | Không có filter control, course list/card, progress bar, pagination trong HTML hoặc source screenshot. | Loaded-state design thiếu; không tạo controls hoặc hành vi. |
| Navigation | Header/Footer link /student, /student/courses, /student/progress; empty CTA /student/progress. | Native anchors trong HTML; không có frontend runtime để resolve routes. | Expected map: ST-01, ST-08, ST-20; runtime chưa verify. |

## 4. Planned event coverage

- ST08-EV-01 load page / request API #20 (expected; current UI không gọi API).
- ST08-EV-02 request API #21 aggregate progress và merge theo course_id theo AC-13/inventory (expected; shape/query chưa chốt; current UI không gọi API).
- ST08-EV-03 change status filter theo inventory (expected design event nhưng element absent; giữ là gap, không tự tạo control).
- ST08-EV-04 empty-state CTA mở ST-20 route /student/progress.
- ST08-EV-05 header brand/navigation tới ST-01, ST-08 hoặc ST-20.
- ST08-EV-06 footer navigation tới ST-01, ST-08 hoặc ST-20.
- ST08-EV-07 chọn course card mở ST-09 theo liên kết inventory; card không có trong PNG/HTML nên sự kiện chưa thể gắn element hoặc triển khai.
- Static title, icon, empty heading/copy và footer brand không có event.

## 5. Planned source trace

- Read canonical ST-08 row, F04 flow, AC-13 API index and diagram, API catalog rows #20/#21, API #20/#21 DD/open questions.
- Recheck current Study Server route/module/query/test sources for both endpoints; classify each API as SOURCE_BACKED, UNWIRED, DECLARED_NOT_RUNNABLE or NOT_FOUND using current source, not catalog label alone.
- Inspect checked-in DDL and data mapping as candidate evidence only. Keep live schema unverified.
- Trace related screens: ST-01 (/student dashboard), ST-09 (/student course detail), ST-20 (/student progress), SH-02 Student session entry.
- No tests are requested; read existing test sources if any, but do not run them.

## 6. Outputs, acceptance and blockers

- [x] Created ST-08.md, ST-08_markers.json, ST-08_markers_overlay.svg, screen_rendered.png and screen_annotated.png after this plan.
- [x] DD includes overview, expected/current flow, each visible element, event sequence (including the ST-09 course-card relationship gap), API #20/#21 contract/status, state/navigation matrix, privacy/security, blockers and checklist.
- [x] Kept source PNG/HTML hashes unchanged; documented provenance of static HTML render.
- [x] Updated global tracker with separate DD/implementation/runtime statuses; artifact bundles advanced 16→17 and remaining incomplete bundles 67→66; next W1 pointer is ST-09. ST-09 was not started in this session.
- DD expected to remain BLOCKED because #20/#21 are not source-backed and their catalog/AC response types do not provide the list/progress payload; implementation blocked by absent Study Web and missing loaded-state/filter/progress design; runtime not verified.

