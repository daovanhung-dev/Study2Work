# AD-05 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-05-TC-001` | Planning ref / not run | `AC-31` | See source acceptance section | P2 |

## 2. Test planning references

### AD-05-TC-001 — Acceptance planning reference (AC-31)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-05](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-31`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

### Tài liệu và traceability

- [x] One Screen ID only: AD-05; plan was authored before marker/DD work.
- [x] Expected behavior and current implementation are separated; discrepancies and derived local behavior are labeled.
- [x] API #69/#71/#72 methods, paths, auth, input shape, success/error codes, response mapping and local behavior are traced to catalog/AC/source.
- [x] All 34 markers have one corresponding element row; visible static claims without source are called out.
- [x] Events cover load, action selection, status mutation, delete mutation, return navigation and controls with no source-backed handler.
- [x] UI/error/navigation states include no-selection, loading, auth/permission, not-found, validation, success and unknown error outcome.
- [ ] Approve #71 body/status allowlist, transition matrix, same-state behavior and mixed-invalid auth/body handling.
- [ ] Approve Admin permission mapping, tenant/scope/MFA, self/last-Admin safeguards and any dependency protection.
- [ ] Approve suspend/delete access-token and refresh-token behavior, reactivation and re-authentication semantics.
- [ ] Approve #72 soft delete vs anonymization/physical erase, retention, timestamp, dependent rows, repeat request and #68/#69 visibility.
- [ ] Define audit reason persistence, actor/record model, endpoint/event, validation and retention before enabling reason input.
- [ ] Decide no-selection/direct-entry, selected-ID handoff, return route and post-mutation refresh/redirect.
- [ ] Wire Study Web route, API client, auth guard, error states and live-deployment/schema verification.
- [ ] Reconcile screenshot wording/design with approved policies and Study Web design system.

### Completion decision

- **DD READY:** No. The document is traceable and suitable for policy review, but required user/security decisions and API contract gaps still block implementation-ready action semantics.
- **IMPLEMENTATION:** `BLOCKED`. Study Web app source/router/API client is `UNWIRED`, and permission, audit, status/session, deletion and navigation policies are unresolved.
- **RUNTIME:** `NOT VERIFIED`. No browser app route, live database, deployed API or runtime action was exercised. API test sources were inspected but not run in this screen session.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 2. Bằng chứng đã rà soát

| Nhóm | Nguồn | Kết luận cho AD-05 |
|---|---|---|
| Inventory/dependency | `list_screen.md` AD-02–AD-05; global plan | AD-05 dùng AC-31/#69/#71/#72; numeric user ID từ AD-02/AD-03; post-action inventory yêu cầu refresh #68; links AD-02/AD-03. Current state list `confirm/in-progress/success/dependency-conflict` chưa fully source-backed. |
| AC-31 | `AC_04_ADMIN_MANAGEMENT.drawio`, diagram AC-31 | Actor Admin có user-management permission; chọn user → #69 detail → UPDATE/#70, STATUS/#71 hoặc DELETE/#72 → reload list/detail. #71/#72 nodes path-only; delete says “soft delete/anonymize theo policy”. Diagram có “revoke session nếu cần”, không bắt buộc/all-token semantics. |
| API catalog #69/#71/#72 | `docs/lists/list_api.md` | #69 GET path int64/UserProfile. #71 PATCH status path int64, response UserProfile, 200 updated, 401/403/404/422/500; catalog không nêu body. #72 DELETE path int64, no body/query, response DeleteResult, 200 deleted, same error set. |
| API #71 DD | `docs/dd/71_admin_user_status/{02_Overview,03_Request,04_Response,05_Data_Mapping,06_Error,OPEN_QUESTIONS}.md` | Draft. Body `{status: ACTIVE|SUSPENDED}` và current-state matrix là `DERIVED`. Local transaction row-locks `users`, updates status/updated_at, revokes eligible refresh tokens only when suspending. Existing access JWT may remain usable; active restore does not restore revoked refresh rows. |
| API #72 DD | `docs/dd/72_admin_user_delete/{02_Overview,03_Request,04_Response,05_Data_Mapping,06_Error,OPEN_QUESTIONS}.md` | Draft. Direct request is path-only. Local `DELETED` marker, `updated_at AS deleted_at`, repeat/missing 404, no PII anonymization, dependent-row delete, audit or token revoke are all local `DERIVED` behaviors. |
| API #71 route/model/validation/query/view | `app/api/v1.py`, `api_71_admin_user_status/*` | FastAPI typed request body can be schema-validated before the endpoint/view auth guard. View then calls shared ADMIN guard, signed-int64 parser, current-status row lock, update and conditional refresh-token revoke. Strict body has one required field; unsupported current statuses map 422. |
| API #72 route/model/validation/query/view | `app/api/v1.py`, `api_72_admin_user_delete/*` | No body/query. Shared ADMIN guard precedes raw path parse and DB. One conditional UPDATE marks any non-DELETED current row; missing/already DELETED → 404. Safe DeleteResult is checked before commit; failures roll back. |
| Login/session/access guard | API #03 `view.py`/`query.py`; `app/utils/auth.py` | Login/refresh checks account status is ACTIVE; #71 suspension revokes only unrevoked, unexpired refresh rows. Shared access JWT guard validates claims/roles without a current status lookup; existing access JWT may remain valid until expiry. #72 itself revokes no refresh rows. |
| Downstream visibility | API #68 and #69 query | Neither read query filters DELETED; after #72 the record remains visible to Admin with status marker. #71 rejects current DELETED status (local 422). Visibility/hide/redirect owner policy remains open. |
| Test/context evidence | focused #71/#72 test sources; `.agents/server-study/tests.md` | Context records 21 #71 and 11 #72 passing at prior checkpoints. Tests were inspected, not run; fake DB sessions do not verify live schema/deployment or authorization policy. Tests do not characterize invalid typed body + missing/invalid auth order. |
| Visual/source HTML | `screen.png`, `code.html` | Static no-selection state, selected lock tab, disabled reason textarea/confirm, read-only/policy badges, “permanent delete”, compliance/audit/gate claims; anchors route to `/admin/users`, nav/footer `#`, no client requests/events. |
| Study Web boundary/design | `.agents/web-work/study/*`, `.agents/web-study/design.md`, current app root | `UNWIRED`; root contains `dist`, docs, node_modules and tsbuildinfo but no editable source/package/router/API client. Design guide is intended target, not runtime evidence; screenshot visual system differs. |

### Trích từ DD nguồn: 7. Execution and verification order

1. [x] Complete docs worklog preflight; read three exact-type worklogs; read project/scope contexts, manifest skill registry and Study Web design guide.
2. [x] Review inventory, AC-31, API catalog/Drafts/source/tests, target HTML/image and current Study Web root; record expected/current and discrepancies.
3. [x] Write this plan before marker JSON/SVG, annotation or AD-05 DD.
4. [x] Create ordered marker JSON/SVG and 2× annotation; preserve originals.
5. [x] Author A–F DD with one element row per marker; describe status/delete/audit/session/API/error/navigation flows without elevating derived source behavior to approved contract.
6. [x] Update `list_screen.md` AD-05 row/API #71/#72 source index and global plan/checkpoint.
7. [x] Verify original hashes, annotation dimensions, marker order/coordinates/1:1 rows, JSON/XML/links, 83 inventory/folder IDs, core bundle count, whitespace and scoped diff.
8. [x] Update worklog final verification; do not run app tests/runtime; do not process another Screen ID.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
