# ST-08 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-08-TC-001` | Planning ref / not run | `AC-13` | See source acceptance section | P1 |

## 2. Test planning references

### ST-08-TC-001 — Acceptance planning reference (AC-13)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-08](../../screen_stitch/03_student/ST-08_khoa-hoc-cua-toi/ST-08.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-13`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-08_khoa-hoc-cua-toi/ST-08.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blockers

### Blockers / quyết định cần đóng

1. **BLOCKER — API #20 response:** catalog `ApiEnvelope<UserProfile>` không biểu diễn course list; API owner cần chốt payload, fields, identifier, enrollment/course projection, empty response và cập nhật nguồn canonical. Xem Q-20-01/Q-20-04.
2. **BLOCKER — #20 filter/paging:** chốt `status` semantics, values/default/case, page indexing/size/max/order/metadata; xem Q-20-02/Q-20-03.
3. **BLOCKER — API #21 query/response:** grammar `course_id list hoặc aggregate?:string`, progress DTO, merge key, scope/formula, empty behavior và identity binding cần quyết định; xem Q-21-01…Q-21-05.
4. **BLOCKER — AC/inventory orchestration:** xác nhận #21 luôn được gọi hay chỉ khi #20 thiếu progress, thứ tự/parallelism và partial-failure behavior.
5. **BLOCKER — loaded UI:** cần thiết kế/duyệt filter, course list/card, progress display, pagination, loading/partial/error/access-denied states; current asset chỉ có empty state.
6. **BLOCKER — navigation contract:** card → ST-09 cần course identifier và behavior khi enrollment không còn hợp lệ; ST-20/session handoff/back behavior chưa có runtime route.
7. **BLOCKER — Study Web:** checkout không có app source/router/entrypoint nên không thể xác minh hoặc implement route, auth guard, API calls, responsive/accessibility behavior.
8. **BLOCKER — AC-13 empty branch:** decision node labels `NO → empty state`, but both `EMPTY` and `HAS DATA` edges target the same course/progress render node. Clarify the target/transition before finalizing the empty-state flow.
9. **BLOCKER — database model:** checked-in legacy BIGINT and V1-PILOT UUID DDL use different course, enrollment and progress relations; API #20/#21 have no query source selecting either. Live schema remains unverified.
10. **BLOCKER — Study Web design alignment:** source HTML's remote font/CDN, Plus Jakarta Sans and 1440px width diverge from the intended guide; no approved exception or implementation is present.
11. **BLOCKER — runtime:** API #20/#21 have no route/module/query/test source, Study Web has no editable source/router, and the database/runtime were not verified.

### Checklist nghiệm thu

- [x] Kế hoạch riêng được ghi trước DD/annotation; scope chỉ ST-08.
- [x] Giữ nguyên `screen.png` và `code.html`; hashes gốc được ghi trong `ST-08_PLAN.md`/`ST-08_markers.json`.
- [x] Vì `screen.png` không thể hiện header và có band đen, tạo `screen_rendered.png` từ HTML tĩnh, ghi rõ provenance; không gọi là runtime capture.
- [x] `screen_annotated.png` có 9 marker; mỗi marker ánh xạ tới đúng một element row bên dưới và trong marker JSON.
- [x] Ghi rõ mỗi element/event có bằng chứng static, expected design hay missing source; API status không bị mô tả thành runtime.
- [x] Ghi luồng ST-07 → ST-08, ST-08 → ST-09/ST-20 và liên kết ST-01/SH-02 có điều kiện.
- [x] Ghi các HTTP/business codes hiện có trong catalog cùng response type và các khác biệt AC/inventory.
- [x] Ghi loading, empty, loaded, partial-progress, filtered và error state expectations; phân biệt với UI hiện hữu.
- [x] Rà soát lại AC-13 decision edges, hai thế hệ checked-in Study DDL và Study Web design guide; các nhánh/projection/design khác biệt được giữ là blocker.
- [ ] DD READY: chờ chốt API #20/#21 payload/query/mapping, loaded-state design, navigation/auth/error behavior và hoàn tất traceability không còn quyết định nghiệp vụ mở.
- [ ] IMPLEMENTATION READY: chờ Study Web source/router/session và API #20/#21 được nối theo contract đã duyệt.
- [ ] RUNTIME VERIFIED: chưa chạy app/API, chưa xác minh database live.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 0. Rà soát bổ sung 2026-11-07 (phiên sau ST-07)

- Phiên hiện tại vẫn chỉ rà soát **ST-08**. Bộ artifact của ST-08 đã tồn tại trước phiên này; phần kế hoạch ngày 2026-11-06 ghi lại lần dựng đầu tiên. Không dựng lại ảnh/marker nếu kiểm tra tĩnh hiện tại không phát hiện lỗi; giữ nguyên PNG/HTML nguồn.
- Hash hiện tại: `screen.png` `665e39c4c1de2cbe417ce092b269aaaa4adc807fc0bb534c2714ab9f2213c21a`; `code.html` `7b8effee5a5ee1dfd7a0ebb5a051af5710785ac0f0c452863fb2b9e057c2298f`; `screen_rendered.png` `95d1f7bacd0ff05ebf9db81f970fc775afbdece30eb10d7374ecf2f551d12ab9`; `screen_annotated.png` `59ce04ce833c65db94fd0768b4a9c62acc8ae07a851952f28b3921c0fe564cdc`. Dimensions lần lượt: 1280×1024, 1280×1024, 1280×1024, 2720×2048. Ảnh gốc không có header và có dải đen dưới footer; HTML render vẫn là ảnh tĩnh, không phải runtime.
- Rà soát lại inventory, AC-13, API catalog/DD #20/#21, Study Server route/module/test source, Study Web tree, design guide và DDL xác nhận các blocker gốc vẫn còn: #20/#21 chưa có route/module/query/test; response catalog `ApiEnvelope<UserProfile>` không biểu diễn course/progress; Study Web thiếu source/router; filter và loaded UI không có trong asset.
- Bổ sung blocker cần được phản ánh vào DD/tracker: (1) AC-13 ghi `NO → empty state; YES → render` nhưng hai cạnh `EMPTY` và `HAS DATA` cùng trỏ đến node “Hiển thị khóa học + % hoàn thành”; (2) DDL legacy BIGINT `enrollments`/`lesson_progress` khác DDL V1-PILOT UUID `course_enrollments`/`lesson_progress_facts`/`progress_snapshots`, và không có bằng chứng live schema; (3) HTML dùng Google Fonts/Tailwind CDN, Plus Jakarta Sans, `max-w-[1440px]`, primary cobalt `#004AC6` và header blur; Study Web guide định hướng Inter/system, không thêm remote import, ocean primary `#0B5F8A`, không dùng glass effect và chiều rộng khoảng 1120px.
- DD update scope: make its required content explicit under A–F headings (overview, flow, elements, events including API, state/navigation, acceptance); add the verified AC branch, schema-generation and design-system discrepancies; retain the existing 9-marker mapping and source assets if the static audit passes.
- Trước khi cập nhật marker map hoặc tracker, kế hoạch kiểm tra: xác minh lại hash/dimensions; parse JSON/SVG; đối chiếu 9 marker có thứ tự với 9 element row và ảnh; kiểm tra link Markdown; giữ trạng thái `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`; cập nhật ST-08 DD/inventory/global plan/worklog. Không chạy app/API tests hoặc runtime.

### Trích từ DD nguồn: 6. Outputs, acceptance and blockers

- [x] Created ST-08.md, ST-08_markers.json, ST-08_markers_overlay.svg, screen_rendered.png and screen_annotated.png after this plan.
- [x] DD includes overview, expected/current flow, each visible element, event sequence (including the ST-09 course-card relationship gap), API #20/#21 contract/status, state/navigation matrix, privacy/security, blockers and checklist.
- [x] Kept source PNG/HTML hashes unchanged; documented provenance of static HTML render.
- [x] Updated global tracker with separate DD/implementation/runtime statuses; artifact bundles advanced 16→17 and remaining incomplete bundles 67→66; next W1 pointer is ST-09. ST-09 was not started in this session.
- DD expected to remain BLOCKED because #20/#21 are not source-backed and their catalog/AC response types do not provide the list/progress payload; implementation blocked by absent Study Web and missing loaded-state/filter/progress design; runtime not verified.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
