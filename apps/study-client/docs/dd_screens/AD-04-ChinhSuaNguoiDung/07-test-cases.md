# AD-04 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-04-TC-001` | Planning ref / not run | `AC-31` | See source acceptance section | P1 |

## 2. Test planning references

### AD-04-TC-001 — Acceptance planning reference (AC-31)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-04](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-31`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Có plan lập trước marker/DD; screenshot gốc và HTML được hash trước/sau.
- [x] 40 marker tuần tự, unique và ánh xạ một-một đến 40 element rows; ảnh chú thích giữ nội dung gốc, render 2×.
- [x] Có A–F, route/actor/preconditions, expected/current separation, element properties, events, API/error handling, states/navigation và acceptance checklist.
- [x] #69/#70 được đối chiếu catalog, AC, API DD, route/model/validation/query/view/test source. Local body #70 được đánh dấu `DERIVED`, không coi là approved API contract.
- [x] Mô tả rõ numeric-ID mismatch, role/status/body mismatch, field preservation, no-op UI controls, Study Web `UNWIRED`, auth/body ordering uncertainty và unsupported gate/audit/support claims.
- [ ] Owner phê duyệt #70 body, role allowlist/mapping, permission, PII, lifecycle/token/audit policy, ID route, dirty navigation và support/gate actions.
- [ ] API DD/catalog/AC body và request-validation/auth ordering được thống nhất; live schema/deployment được xác minh.
- [ ] Study Web route/API client/UI implementation được nối và runtime được kiểm tra.

**Kết luận:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Các checklist chưa hoàn tất là các dependency thật, không được thay bằng giả định. API #70 được ghi source-backed locally trong inventory; điều này không đồng nghĩa body đã được phê duyệt.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 2. Bằng chứng đã rà soát

| Nhóm | Nguồn | Kết luận cho AD-04 |
|---|---|---|
| Inventory / dependency | `list_screen.md` AD-03/AD-04/AD-05; global tracker | AD-03 chọn user → AD-04 edit → quay về AD-03; inventory mô tả `GET #69 → PUT #70 → GET #69`, dirty state/cancel và `loading/dirty/saving/validation-error`. Route là đề xuất; blocker cũ là body PUT #70 chưa đặc tả. |
| AC-31 | `AC_04_ADMIN_MANAGEMENT.drawio`, node chọn Update | Sau khi đọc user/profile/role, Admin chọn Update → PUT #70 → reload list/detail. Diagram không định nghĩa request body/field rules. |
| API catalog | `docs/lists/list_api.md` #69/#70 | #69 GET detail: `user_id:int64!`, `ApiEnvelope<UserProfile>`, 200, 401/403/404/500. #70 PUT: cùng path int64, `ApiEnvelope<UserProfile>`, 200, 401/403/404/422/500. Catalog #70 không khai báo body, query hoặc writable fields. |
| API #70 DD | `docs/dd/70_admin_user_update/{02_Overview,03_Request,04_Response,05_Data_Mapping,06_Error,OPEN_QUESTIONS}.md` | `Draft — Needs Confirmation`. Body hiện chạy là full-replacement **DERIVED**: required `full_name`, `phone`, `avatar_url`, `role`; `phone`/`avatar_url` nullable; roles `STUDENT/MENTOR/ADMIN`. Body/role/persistence/policy cần owner confirmation. |
| API #70 route/model | `app/api/v1.py`; `api_70_admin_user_update/models.py` | PUT route khai báo `AdminUserUpdateRequest` typed body và OpenAPI candidate schema. Strict Pydantic body `extra=forbid`; đúng bốn keys đều required. |
| API #70 validation/view/query | `validate.py`, `view.py`, `query.py` | Local view auth guard `ADMIN`, signed-int64 path, trim/validate fields, one bound UPDATE of `full_name`, `phone`, `avatar_url`, `role`, `updated_at`; map safe `UserProfile`; commit after mapping; rollback on missing row/query/projection/commit failure. |
| Response / errors | API #04 `UserProfile`, API #70 envelope, response helper, `app/core/middleware.py` | 200 `DESIGN_RESOURCE_UPDATED`; data is safe UserProfile; errors 401/403/404/422/500 with JSON-null `data`. #70 preserves email/status/created_at; no audit or token side effect. Middleware maps Pydantic request errors to 422. |
| API #69 handoff | API #69 catalog/source and prior AD-03 DD | #69 returns profile with signed-int64 `id`, `full_name`, `email`, `role`, nullable `avatar_url`/`phone`, `status`, `created_at`, `updated_at`; no `adminNotes` or audit fields. The route/user role permission fallback and live schema remain open. |
| Focused tests/context | `tests/modules/admin/api_70_admin_user_update/test_admin_user_update.py`; `.agents/server-study/tests.md` | Context records 19 focused passing cases at a prior checkpoint; source covers auth before DB, normalization, body/path 422, no-row 404, safe projection and rollback. Tests were inspected, not run; fake DB sessions do not verify live schema. Auth with malformed body is not characterized. |
| Visual source | `screen.png`, `code.html` | Locked static form. Name/email/role/status/admin notes and Save are disabled; top back and Cancel use inconsistent paths; “Gửi yêu cầu” and API-doc buttons have no handlers. Hard-coded record ID `USR-9281-VN`, lecturer/locked values, sync/RBAC/audit/legal/compliance assertions do not map to #69/#70. |
| Web boundary/design | Study Web subcontext and `.agents/web-study/design.md`; current app root | Study Web remains `UNWIRED`, with no editable source/package/router/API client. Screenshot typography/palette/density differs from intended Study Web guide. |

### Trích từ DD nguồn: 7. Execution and verification order

1. [x] Read current objective, router/context/worklog preflight, exact-type docs worklogs, Study Web/Study Server contexts, inventory, AC, API #69/#70 catalog/DD/source/test source and AD-04 assets.
2. [x] Write this plan before marker JSON/SVG, annotation or AD-04 DD.
3. [x] Create ordered markers, JSON/SVG, and 2× annotation without editing originals.
4. [x] Author A–F AD-04 DD with one element row per marker, detailed events, local API body/status/error mapping, navigation, expected/current discrepancies and blockers.
5. [x] Update inventory/API source rows and global tracker/checkpoint; keep DD/implementation/runtime statuses separate.
6. [x] Update worklog after final verification.
7. [x] Verify source hashes unchanged, annotation dimensions 2560×2542, marker IDs/coordinates/order and 1:1 DD rows, JSON/SVG/local links, 83 inventory/folder match, core bundle count and scoped whitespace.
8. [ ] Do not run app tests/runtime; mark test source inspected-not-run and runtime not verified.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
