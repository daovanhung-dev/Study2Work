# ME-09 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-09-TC-001` | Planning ref / not run | `AC-23` | See source acceptance section | P1 |

## 2. Test planning references

### ME-09-TC-001 — Acceptance planning reference (AC-23)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-09](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/ME-09.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-23`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/ME-09.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Điều hướng và tiêu chí nghiệm thu

### F.1. Điều hướng và dữ liệu truyền

| Từ/đến | Hành vi expected | Current evidence / giới hạn |
|---|---|---|
| ME-01 → ME-09 | Mở danh sách từ Mentor dashboard. | Inventory link; dashboard widget không xác nhận route runtime. |
| ME-09 → ME-10 | Chọn submission và truyền submission ID. | Current #54 trả item `id`; #55 nhận `submission_id` path. Loaded row và router chưa có. |
| ME-10 → ME-09 | Quay lại danh sách sau detail/grade/feedback. | ME-10 inventory liên kết ngược; refresh/invalidation/cache behavior chưa được xác định ở ME-09. |
| Header/footer links | Điều hướng tới Mentor pages/policy/support. | Tất cả anchor trong HTML là `#`; destination chưa được xác nhận. |

### F.2. Blockers cần quyết định

| Blocker | Cần xác nhận | Nguồn/ảnh hưởng |
|---|---|---|
| ME09-B01 — response cardinality | API/schema owner chấp thuận `Page<Submission>` hay giữ singular `Submission`; đồng bộ inventory/API DD/catalog/diagram. | [inventory](../../list_screen.md#L169), [AC-23 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio), [API #54 DD](../../../../study-server/docs/dd/54_mentor_submissions_list/02_Overview.md), current route/model. |
| ME09-B02 — loaded row design/fields | Duyệt row layout, deadline source, owner/student display field, course/assignment title, file display and pagination controls. | Inventory yêu cầu deadline/owner; #54 không trả due date/name/title; ảnh/HTML chỉ empty. |
| ME09-B03 — filters | Xác định course-option source và selected numeric ID; status enum/valid values/default mapping; hành vi page reset. | HTML options static; #54 query exact status và int64 course_id; status lifecycle/409 còn mở trong API DD. |
| ME09-B04 — search | Bỏ/disable search hoặc định nghĩa field/index/query endpoint tương thích. | #54 không có search param, assignment title; HTML input không có event. |
| ME09-B05 — refresh/claims | Quyết định refresh action, polling/auto-sync, 48-hour SLA, rubric and support destination. | HTML claims không được API #54 hoặc #55 current source chứng minh. |
| ME09-B06 — server contract | Chốt file URL producer #35, assigned-Mentor access, status lifecycle/409, nullable relations/timezone/live schema và error catalog. | [API #54 open questions](../../../../study-server/docs/dd/54_mentor_submissions_list/OPEN_QUESTIONS.md). |
| ME09-B07 — frontend runtime | Bổ sung editable Study Web source/router/auth/API integration trước khi triển khai và xác minh screen. | [Study Web context](../../../../../.agents/web-work/study/AGENTS.md) xác nhận `UNWIRED`. |

### F.3. Checklist nghiệm thu tài liệu

- [x] Ảnh gốc và HTML được bảo toàn; hai hash ghi trong plan/worklog.
- [x] Có ảnh chú thích 2× và 27 marker duy nhất, tuần tự; JSON/SVG/element IDs ánh xạ một-một.
- [x] Expected behavior và current source tách biệt; API #54 được trace route → guard/view → SQL → model/response → test source.
- [x] Tất cả visible element trong PNG/HTML được nhận diện; controls và navigation thiếu handler/route được nêu rõ.
- [x] Events, states, error/business code và ME-10 handoff được mô tả; loaded-state row được đánh dấu thiếu thay vì bịa.
- [ ] Contract cardinality, loaded row fields, filter/search semantics, API/schema open questions và Study Web wiring được duyệt/hoàn tất.
- [ ] Có thể khẳng định lập trình viên triển khai mà không cần tự quyết nghiệp vụ/API còn mở.

**Kết quả:** checklist artifact và source trace đạt cho phiên này; hai mục cuối chưa đạt nên ME-09 chưa phải `DD READY`. `IMPLEMENTATION BLOCKED` và `RUNTIME NOT VERIFIED` là các trạng thái độc lập, không được suy từ việc đã tạo ảnh/DD.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. Verification and completion rule

1. This plan was written before marker map, overlay, annotated image and DD authoring.
2. Created 27 ordered JSON markers and matching SVG IDs; static audit passed uniqueness, bounds and one-to-one mapping to 27 DD element rows.
3. Generated a 2× annotated PNG and visually inspected the full image. Moved marker #4 below the active nav and marker #22 above the policy strip to keep labels/icons unobscured.
4. Wrote ME-09 DD with expected/current split, element/event/state detail, API #54 route→view→query→response trace, ME-10 handoff, blockers and source links.
5. Updated the ME-09 row and current artifact checkpoint in `dd_screens/PLAN.md`; worklog records asset hashes, static audit and `git diff --check`.
6. API tests and screen runtime were not run. No live-schema or Study Web implementation claim is made.

### Result

- `screen.png` and `code.html` hashes match the pre-authoring values.
- Source PNG is 1600×1280; annotated PNG is 3200×2560.
- JSON/SVG contain 27 markers; element map contains 27 unique matching IDs; event sections E01–E09 are sequential; all relative DD links resolve.
- The design/API blockers in §3 remain open; screen status remains `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.

**Completion target:** deliver all static screen artifacts while retaining `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` until the listed contract/data/UI decisions are resolved.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
