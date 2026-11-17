# AD-21 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## Current Angular source tests

- `ad21-page.spec.ts` covers the #96 status projection, safe handling of large route IDs, source 404 rendering, disabled actions and the missing client handoff/poller for #18.
- `admin.routes.spec.ts` covers the registered `notifications/:notificationId` route.
- These source tests do not prove a live backend, database schema or deployed browser runtime. Results for the current task are recorded after the focused test run below.

### Current task verification

- Frontend: `npm test -- --include='src/app/features/admin/AD21/pages/ad21-page.spec.ts' --include='src/app/features/admin/admin.routes.spec.ts'` — 2 files, 4 tests passed.
- Backend: `uv run pytest -q tests/modules/shared/api_18_operations/test_operations.py tests/modules/admin/api_94_admin_notifications_update/test_admin_notifications_update.py tests/modules/admin/api_95_admin_notifications_delete/test_admin_notifications_delete.py tests/modules/admin/api_96_admin_notifications_status/test_admin_notification_status.py` — 65 passed, one upstream Starlette/httpx deprecation warning; fake DB only.
- Build: `npm run build` passed. Three existing Student CSS budget warnings were reported; no AD-21 budget warning.
- Browser: Firefox headless opened `/admin/notifications/901` and showed the Admin sign-in screen. No credentials were entered and GET #96 was not exercised; loaded-state browser runtime remains unverified.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-21-TC-001` | Planning ref / not run | `AC-36` | See source acceptance section | P1 |

## 2. Test planning references

### AD-21-TC-001 — Acceptance planning reference (AC-36)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-21](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/AD-21.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-36`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/AD-21.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Source screenshot and HTML are preserved; their original hashes are recorded in the plan.
- [x] Annotated image contains sequential markers #1–#47; JSON/SVG coordinates point to the same source-pixel positions.
- [x] Every marker maps to exactly one element row `AD21-EL-01`…`AD21-EL-47`.
- [x] Current static prototype and expected AC/API behavior are kept separate.
- [x] #94/#95/#96 direct catalog contracts are compared with local route/validator/query/view effects and errors.
- [x] API #18/SH-07 ID, owner, lifecycle and wiring blockers are visible.
- [x] No unsupported recipient/channel metrics, cancellation result, Operation polling or live-schema claim is added.
- [ ] Product/API owners approve notification model/grain, notification-management permission, lifecycle/status mapping, #94 body/edit gate, #95 cancel/delete/retention and dispatch coordination.
- [ ] API #18 ID/owner/status/producer mapping and Study runtime route/store are implemented or explicitly scoped.
- [x] Study Web route/page and read-only #96 caller exist in source; current focused verification is recorded below.
- [ ] #94/#95 mutations, #18 client handoff/poller, and all navigation/error handling are implemented and verified.
- **Disposition:** `DD BLOCKED` · `IMPLEMENTATION BLOCKED` · `RUNTIME NOT VERIFIED`.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: Source review và thứ tự

1. Đọc list_screen row 79, API reverse index #018/#094–#096 và global plan/checkpoint; xác nhận chỉ xử lý AD-21.
2. Đối chiếu AC-36 Admin permission, update/delete/status branches, direct API catalog và macro-review #92–#96; giữ nguyên khác biệt path-only contract/local body/effects.
3. Trace router → shared auth → validator → query/transaction → model/response/errors for #94/#95/#96. Inspect API #18 registration/store and SH-07; treat candidate DDL/test history as limited evidence.
4. Inspect AD-19/AD-20 handoff, exact screenshot/HTML and Study Web source tree. Never treat mockup/static copy as runtime state.
5. Save this plan before writing marker JSON/SVG, annotated PNG or `AD-21.md`.
6. Create 47 ordered element markers and map every marker to one DD row; cover shell, breadcrumbs, cards, status labels, disabled actions and footer.
7. Write A–F DD with current static behavior, expected-only flow, API exact contract/current local difference, errors, navigation, state matrix and blockers.
8. Update inventory row 79, reverse index #094/#095/#096 D→R (local source exists; API DD remains Draft), and global plan. Static-audit image/map/document/source hashes, counts, links, `git diff --check`; do not run application tests/runtime.

### Trích từ DD nguồn: Acceptance and known blockers

- Marker IDs #1–#47 must be unique, sequential, in image bounds, and map one-to-one to element rows in `AD-21.md`; JSON/SVG/image coordinates must match.
- Source image/HTML hashes stay unchanged; annotated PNG is 2850×3200 and visually checked at full page.
- Inventory/folders remain 83/83; core artifacts rise from 73/83 to 74/83 after the four required DD assets are added.
- API reverse rows #094/#095/#096 and #018 record local registered source; API DDs remain Draft and catalog contracts stay unchanged.
- Do not equate expected `draft/scheduled/sending/delivered/failed` with local `QUEUED/SENT/FAILED`; do not infer recipient/channel counts, delivery progress, notification cancellation, or Operation handoff.
- DD state: `DD BLOCKED`; implementation: `IMPLEMENTATION PARTIAL SOURCE`; runtime: `RUNTIME NOT VERIFIED`. Contract/permission/lifecycle/schema and SH-07 handoff remain unresolved.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
