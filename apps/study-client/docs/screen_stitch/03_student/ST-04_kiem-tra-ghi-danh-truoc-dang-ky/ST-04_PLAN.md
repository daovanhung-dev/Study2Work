# ST-04 — Detailed Design Plan

## 1. Phạm vi và thứ tự

- Screen: ST-04 “Kiểm tra ghi danh trước đăng ký”, inventory row 18, proposed route `/student/enroll/:courseId`.
- Chỉ xử lý ST-04 trong phiên này. Không author ST-05, ST-06, ST-07 hay ST-01.
- Trình tự: source/context/AC/API review → lưu plan này → nếu xác nhận HTML hợp lệ thì render thành ảnh phụ riêng, không ghi đè `screen.png` → marker JSON/SVG và `screen_annotated.png` → DD A–F → inventory/API reverse index/global plan/worklog → static audit.
- Giữ nguyên `screen.png` và `code.html`. `screen.png` hiện gần như trống và không thể làm nền ánh xạ element; nếu Chrome render `code.html` thành công, dùng `screen_rendered_from_html.png` làm visual evidence/base và nêu rõ provenance. Marker IDs dùng tọa độ CSS của HTML, không gán lên PNG gốc.
- Không suy ra business behavior từ shell, static copy, DDL hoặc API DD. API #15 identity/selection là blocker; không tạo route, API, field, guard, status, payment rule, data mapping, retry, cache hay transaction mới.
- Không chạy application tests/runtime. Test source được đọc chỉ để trace current API #08; không xem fake-session tests là live-schema evidence.

## 2. Evidence register và asset preservation

| Evidence | Dùng cho | Trạng thái |
|---|---|---|
| [`screen.png`](./screen.png), 1280×1024, SHA-256 `7df0dac4e7598c3b336d5c5d78f5fd9a851526712aa7dd0fd7224a6ffe61ad7f` | Giữ làm asset gốc; visual review cho thấy chỉ nền sáng/dải màu, không có copy hoặc element UI đọc được. | Original retained; unusable as element map |
| [`screen_rendered_from_html.png`](./screen_rendered_from_html.png), 2560×2048 | Render riêng từ `code.html` bằng Chrome headless, viewport CSS 1280×1024 và scale 2; chụp sau `document.fonts.ready`. | HTML-derived visual base; original retained |
| [`code.html`](./code.html), 8,553 bytes, SHA-256 `24b0e361877b15db88298a29d806a2a17f0151e6685df71647d103477276f4fa` | Static page shell, breadcrumb, enrollment error card, back link và footer; không có API client/form/event logic. | Design prototype; rendered/readable as a static page |
| Inventory row 18 và ST-04 global row | Route candidate, AC-12, APIs #08/#15, expected states, downstream links và user-identity blocker. | Expected behavior |
| [AC-12 diagram](../../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), [AC/API index](../../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) | Student precondition, #08→#15, existing-enrollment/free-vs-paid branch, downstream order/payment/operation/enroll/reload chain. | Expected flow; #15 identity contradiction remains |
| [API catalog #08/#15](../../../../../../docs/lists/list_api.md) | Direct request/response/error/role declarations. | Design contract |
| [API #08 DD](../../../../../study-server/docs/dd/08_courses_detail/00_Cover.md), request/response/mapping | #08 public Course detail contract and source/DD mapping assumptions. | Draft |
| [API #15 DD](../../../../../study-server/docs/dd/15_courses_enrollment_status/00_Cover.md), overview/request/response/mapping/open questions | Public identity/selection, 404 meaning, visibility and enrollment-status gaps. | Draft; NEEDS USER DECISION |
| Current #08 route/module/shared model/query/mapper/test source | Actual published-course read, response, errors, join and current source/test boundary. | Local source-backed; tests not run here |
| Current Study router/source tree and API #15 search | Current Web route and #15/#16–#20 implementation boundary. | Study Web `UNWIRED`; #15 not found |
| [Legacy Study DDL](../../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../../infra/postgres/02_study_db.sql), database context | Candidate schema difference; no live schema inference. | Artifacts only; live DB unverified |
| [Study Web design guide](../../../../../../.agents/web-study/design.md) | Intended tokens, responsive layout, keyboard, focus and status accessibility. | Intended target only |

## 3. Expected behavior and current boundary

### Expected AC-12 path

```text
Student đã đăng nhập + course tồn tại
→ GET #08 published course detail
→ GET #15 check enrollment
→ already enrolled: existing AC/inventory My Courses branch
→ no enrollment + verified free branch: POST #19 (server checks identity/entitlement)
→ paid branch: ST-05/#16 order → ST-06/#17 payment → conditional #18 status
→ server verifies payment/entitlement → #19 → #20 reload → ST-08/My Courses
```

AC-12 calls #15 Public with only `course_id`, but expects a single user-specific Enrollment that contains `user_id`. The request has no identity selector; the legacy table does not establish unique `(user_id, course_id)` selection. This is a blocking contract contradiction. Do not resolve it by adding Bearer, user ID, selecting latest/active, or returning an aggregate. Course price alone is not proof of payment, entitlement or enrollment.

### Current behavior

- The exact HTML is an inert error-state prototype: public header nav including Sign In/Sign Up, breadcrumb, “Kiểm tra ghi danh” card, static cannot-confirm headline/body, `/courses` anchor and footer links. It has no retry action, course data, current-user state or interactive control.
- Original PNG does not depict this HTML. If the browser render works, preserve both sources and annotate only the separately named HTML render.
- Study Web has no editable app entry, router, package manifest or Student route. `/student/enroll/:courseId` is candidate only.
- #08 is currently composed and read-only. #15 has catalog/Draft DD only and no local route/module/query/model/test. No current Study Web/API source completes the AC-12 enrollment flow.

## 4. Planned element markers

Coordinates will be measured in the rendered HTML’s 1280×1024 CSS viewport after plan save; `screen_annotated.png` will be generated at 2× if rendering succeeds. Each visible target gets one `ST04-EL-01`… ID and one marker; grouped nav/footer elements list all contained links in the DD. Do not add markers to the blank original PNG.

| Planned marker | Target | Distinction to retain |
|---|---|---|
| #1 | Header Study2Work brand link | Static link `href="/"` |
| #2 | Header primary navigation group | Home, Courses, My Courses, Progress anchors |
| #3 | Header Sign In link | `href="/login"`; conflicts with AC-12 Student precondition context |
| #4 | Header Sign Up link | `href="/register"`; static public shell |
| #5 | Breadcrumb group | Home, Courses and current “Kiểm tra ghi danh” text |
| #6 | Enrollment verification icon | Static decorative/status icon; no server result source |
| #7 | Centered status card/surface | Layout container; no API-bound data source |
| #8 | H1 “Kiểm tra ghi danh” | Static title |
| #9 | Status headline “Chưa thể xác nhận thông tin ghi danh.” | Static copy; not a #15 error response |
| #10 | Supporting explanation | Static copy recommends return or retry later, but no retry control exists |
| #11 | “Quay lại danh sách khóa học” CTA | Anchor `href="/courses"`; does not carry course ID/query |
| #12 | Footer brand | Static Study2Work wordmark |
| #13 | Footer link group | Home, Courses, Sign In and Sign Up anchors |

If rendered layout materially differs, update this plan’s element targets/coordinates before marker JSON, SVG or annotated image.

## 5. Event plan

| Event | Element/trigger | Planned evidence boundary |
|---|---|---|
| EV-01 Route load/auth context | Browser load of candidate ST-04 route | AC-12 expects logged-in Student; current router/session guard is absent. Do not use the static public shell as proof of authenticated identity. |
| EV-02 Load published course (#08) | Route `courseId` available | Public GET by `course_id:int64`; current handler reads only PUBLISHED Course and returns `Page<Course>` singleton. Exact field/error mapping must follow source/catalog; no enrollment side effect. |
| EV-03 Check enrollment (#15) | Course exists and ST-04 attempts status lookup | Candidate public GET path only; response identity/row selection cannot be resolved. Current implementation absent; status cannot be determined safely. |
| EV-04 Branch to existing/free/paid path | Approved #15 result plus approved price/payment rule | AC-12 branches to My Courses, #19 or ST-05/#16. No branch may be executed from static copy or client-only price/callback. Downstream APIs are not implemented here. |
| EV-05 Return to course list | Activate #11 | Current anchor path `/courses`; no course ID or filter state is passed. Study route is not wired. |
| EV-06 Shell/footer navigation | Activate #1–#5/#12–#13 links | Static hrefs only; route availability and authenticated shell behavior are not proven. |

## 6. Blockers to carry into DD

- #15 Public request cannot identify the Student whose Enrollment is returned; multiple enrollments may match a course. Require an approved contract/selection rule before any status request or “already enrolled” result.
- AC-12 Student-authenticated precondition conflicts with the public shell and public #15; current Study Web has no route/session guard.
- #08 current response has `price`, `status`, `title`, `description`, `thumbnail_url`, `mentor`; it does not establish free-price threshold, currency, eligibility or payment completion. The API #08 Draft DD says INNER JOIN, current query uses LEFT JOIN with a mapper error for missing mentor.
- No approved exact behavior for #15 404 meaning, enrollment status enum, existing enrollment/duplicate path, price changes between screens, or API #19 idempotency/entitlement checks.
- Payment status must be server-verified; client callback is not proof. #16/#17/#18/#19/#20 current source absent; do not claim a functional enrollment result or My Courses reload.
- Screenshot is blank while HTML contains the error state; use explicit alternate-render provenance, retain original screenshot, and record its mismatch.
- Legacy BIGINT and pilot UUID/versioned enrollment structures differ; live DB/schema is unverified.
- Study Web visual guide conflicts with the HTML’s cobalt palette/Plus Jakarta Sans/remote CDN; no visual exception approved.

## 7. Completion/status criteria

- **Completed:** created `screen_rendered_from_html.png` (2560×2048) from the HTML at a 1280×1024 CSS viewport and device scale 2, after fonts loaded; original screenshot and HTML remain unchanged.
- **Completed:** browser-measured 13 targets and wrote `ST-04_markers.json`, overlay SVG and `screen_annotated.png`; final image visually reviewed.
- **Completed:** wrote A–F DD with all 13 visible targets and EV-01…EV-06, including API request/response/error boundaries and unresolved branches.
- **Completed:** updated ST-04 inventory/global row and API #08 reverse index to `R` from current local source evidence; #15 remains `D`/unwired.
- **Completed:** recorded `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, and `RUNTIME NOT VERIFIED` while identity/selection and enrollment/payment rules remain unresolved.
- **Completed:** static checks passed for marker/coordinate alignment, dimensions, JSON/XML, local links, original source hashes, 83-screen inventory/folder audit, core artifact count (79/83), and scoped `git diff --check`. No application test/runtime claim.

### Render and marker measurement record

- `screen.png` SHA-256 remains `7df0dac4e7598c3b336d5c5d78f5fd9a851526712aa7dd0fd7224a6ffe61ad7f`; `code.html` SHA-256 remains `24b0e361877b15db88298a29d806a2a17f0151e6685df71647d103477276f4fa`.
- Browser DOM bounds were captured with viewport 1280×1024 CSS px, `deviceScaleFactor=2`; `screen_rendered_from_html.png` and `screen_annotated.png` are both 2560×2048.
- `ST-04_markers.json` stores CSS target bounds and marker centers, plus raster centers at 2×. The visual review moved markers #1/#2/#3/#4/#12/#13 to whitespace/edge callouts so labels do not cover text.
