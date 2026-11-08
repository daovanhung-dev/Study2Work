# ME-07 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-07-TC-001` | Planning ref / not run | `AC-22` | See source acceptance section | P1 |

## 2. Test planning references

### ME-07-TC-001 — Acceptance planning reference (AC-22)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-07](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-22`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-07_tao-chinh-sua-noi-dung/ME-07.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 8. Acceptance criteria

1. `courseId` and optional `contentId` determine a documented create/edit mode; edit must locate an active matching row from #49 and must not confuse Content ID with lecture ID.
2. #49 fields map without fabricated data; all IDs/status/parent/order are preserved; version is reported as unavailable in the current response.
3. Create body contains exactly `course_id/content_type/title/payload`; edit uses only the source body when approved; no `sort_order`, `parent_id`, `status`, owner or version is added to current request bodies.
4. API responses are mapped precisely: #50 201 `DESIGN_RESOURCE_CREATED`; #51 200 `DESIGN_RESOURCE_UPDATED`; errors 401/403/404/422/500 as above. Empty collection, edit not-found, denied and network/server error have distinct UI states.
5. No save-success state before server success; no blind retry for ambiguous POST; #49 is refreshed after mutation per inventory; status/version effects are shown accurately.
6. All 31 marker IDs match one DD element and the image; every visible control has an event or explicit static/blocked state.
7. Study Web route/form, keyboard/accessibility/reflow, session handling, cache and deployed data are verified before `RUNTIME VERIFIED` is set.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 4. Event plan and state checklist

1. Resolve `courseId`/optional `contentId`; create/edit mode is proposed from route params only.
2. Edit path reads #49 collection to locate `contentId`, verifies it belongs to route course, maps current fields to form. Create path carries course ID from ME-06; whether to call #49 in create mode is open.
3. Title/type/order/content editor changes establish dirty state. Input rules are only candidates from mockup until approved; do not fabricate title length, type enum or payload requirements.
4. Save: #50 only if create and body contract is approved; #51 only if edit and derived body is confirmed. Disable duplicate submit; retry/idempotency/conflict are not source-backed.
5. On success, show server result and revalidate #49 before return to ME-06. On failure, keep draft input local, map 401/403/404/422/500 distinctly; exact client UX and session-refresh behavior remain unimplemented.
6. Cancel returns to ME-06 only after destination/unsaved-confirm policy is agreed; current anchor is `#`.
7. States to document separately: create-ready, edit-loading, ready, dirty, validating, saving, saved-await-refresh, access-denied, not-found, validation-error, server/network error, and conflict (design placeholder only; no API #51 version/409 source).

### Trích từ DD nguồn: 5. Acceptance checklist for this session

- Original image/HTML hashes unchanged.
- Plan exists before annotations and DD.
- 31 markers are sequential/unique/in-bounds, non-overlapping, and each maps to one DD element; SVG map and annotated PNG match.
- Every visible input/action/panel has a source mapping, static-only label or explicit `BLOCKED` status; all recognized events have a detailed ordered flow.
- Request/response/body/DB effects use current #49–#51 source; catalog/AC/API DD disagreements remain explicit.
- Statuses are separate: DD remains blocked while unapproved API decisions remain; implementation blocked due missing payload/order/editor/client source; runtime not verified.
- Static audit and `git diff --check` complete; no tests/browser/runtime/live DB probe.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
