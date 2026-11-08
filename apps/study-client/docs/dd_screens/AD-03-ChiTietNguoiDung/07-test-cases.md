# AD-03 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-03-TC-001` | Planning ref / not run | `AC-31` | See source acceptance section | P1 |

## 2. Test planning references

### AD-03-TC-001 — Acceptance planning reference (AC-31)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-03](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-31`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blockers

### Checklist nghiệm thu

- [x] AD-03 inventory, AC-31, API catalog/DD, backend route/module/query/model/auth/response, test source và UI assets đã được đối chiếu.
- [x] Có plan trước marker/annotation/DD; ảnh nguồn `screen.png` và `code.html` được giữ nguyên.
- [x] Tất cả thành phần nhìn thấy được đánh số; marker JSON/SVG có thứ tự và ánh xạ sang element ID trong mục C.
- [x] A–F mô tả tổng quan, flow, từng element, event/API/errors, states/navigation và checklist.
- [x] API #69 phân biệt contract trực tiếp, local source behavior và fallback `DERIVED`; response fields/error set không bị nhầm với prototype `204`.
- [x] Test source được đọc để truy vết, nhưng không tuyên bố chạy hoặc xác minh runtime/live DB.
- [ ] Admin user-management permission, tenant/MFA/policy được owner duyệt.
- [ ] Live legacy schema/grants/deployment hoặc schema UUID target được xác định.
- [ ] PII masking/visibility, enum labels và lifecycle status được duyệt.
- [ ] Audit API/event source, empty/count semantics, retention và compliance claims được xác nhận hoặc loại bỏ khỏi thiết kế.
- [ ] Study Web route/auth/client và visual design được wire theo `.agents/web-study/design.md`.
- [ ] Back/edit/action/footer destinations và disabled/enabled behavior được xác nhận xuyên AD-02/AD-04/AD-05.

### Open blockers

1. **Admin permission:** local `ADMIN` JWT claim là fallback cho AC-31 user-management permission; policy/tenant/MFA chưa được xác nhận.
2. **Schema:** local query nhắm legacy BIGINT `users`; live DB/deployment chưa xác minh, V1-PILOT dùng UUID model khác.
3. **PII and lifecycle:** email/phone masking, role/status enum, deleted/anonymized user visibility và audit requirements chưa chốt.
4. **Audit panel:** không có nguồn history/log/count/retention trong #69; các claim “0 bản ghi”, 180 ngày, automatic monitoring, RBAC Strict Audit và Nghị định cần nguồn/owner.
5. **Frontend/runtime:** Study Web `UNWIRED`; không có editable source/router/client để implement hoặc runtime-verify route.
6. **Visual consistency:** prototype dùng Plus Jakarta Sans/cobalt treatment; Study Web guide yêu cầu semantic ocean-blue tokens và Inter/system sans-serif. Cần design review khi wire.

**Kết quả:** API #69 `SOURCE-BACKED LOCALLY (R)`; screen `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Chỉ xử lý AD-03 trong phiên này.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 2. Bằng chứng đã rà soát

| Nhóm | Nguồn | Kết luận dùng cho AD-03 |
|---|---|---|
| Inventory và handoff | `list_screen.md` AD-03, AD-02, AD-04, AD-05 | AD-03 là chi tiết tài khoản; từ AD-02/#68 nhận user đã chọn; đích kế tiếp AD-04 hoặc AD-05. Route đề xuất, trạng thái cũ `D`. |
| Activity | `AC_04_ADMIN_MANAGEMENT.drawio`, lane AC-31 | Admin đăng nhập và có quyền user management; chọn user → GET detail #69 → đọc profile/role → nhánh update #70, status #71 hoặc delete #72. Đây là flow nghiệp vụ trong diagram, không chứng minh quyền/endpoint đã được phê duyệt live. |
| API contract | `docs/lists/list_api.md` #69 | `GET /api/v1/admin/users/{user_id}`, Bearer JWT/Admin, path `user_id:int64!`, `ApiEnvelope<UserProfile>`, success 200; errors 401/403/404/500. Không có query/body/pagination. |
| API runtime | `app/api/v1.py`; `modules/admin/api_69_admin_user_detail/{validate,query,view,models}.py`; shared auth/response helpers | Route wire tới view. Shared guard kiểm tra Bearer/JWT và claim `ADMIN` trước parse path/query; guard-to-user-management mapping còn DERIVED. Raw signed-int64 parse; malformed/out-of-range và row missing map 404; safe allowlisted legacy `users` projection; query/mapping errors map 500; response `DESIGN_RESOURCE_RETRIEVED`. |
| Response schema | `UserProfile` từ API #04 và API #69 envelope model | `id:int`, `full_name:string`, `email:string`, `role:string`, `avatar_url:string|null`, `phone:string|null`, `status:string`, `created_at`, `updated_at`. `bio` không có trong runtime model; không trả `password_hash`. `meta` rỗng và `traceId` có trong envelope. |
| API DD / open questions | `docs/dd/69_admin_user_detail/02_Overview.md`, `03_Request.md`, `04_Response.md`, `06_Error.md`, `OPEN_QUESTIONS.md` | API DD `Draft — Needs Confirmation`. Legacy BIGINT table target, ADMIN policy mapping, path/no-row 404 derivation, enum values, PII/audit and lifecycle decisions remain open. |
| DB/source basis | `infra/postgres/study-server/DB.sql`; API #69 query | Checked-in legacy `users` has BIGSERIAL `id` and candidate profile columns. Query selects only the response allowlist and omits password hash. V1-PILOT UUID identity model differs; live schema/grants/deployment not verified. |
| Test evidence | `tests/modules/admin/api_69_admin_user_detail/test_admin_user_detail.py` | Source asserts safe field projection, auth before DB, malformed ID 404, no-row 404, query/mapping 500, no commit, OpenAPI int64/error set. Tests use fake sessions/rows and were inspected, not run. |
| Visual source | `screen.png`, `code.html` | Static detail screen in a no-selected-user/“CHƯA ĐỒNG BỘ” empty state. Edit/status controls disabled. Audit panel and 180-day retention, “RBAC Strict Audit Active”, system-normal/sync claims and 204/NULL_PAYLOAD text have no evidence in API #69. HTML has placeholder links and no request/interaction code. |
| Web boundary/design | `.agents/web-work/study/AGENTS.md`, `.agents/web-study/design.md`, current `apps/study-client/` root | Study Web is `UNWIRED`; root has `dist`, `docs`, `node_modules`, and `tsconfig.tsbuildinfo`, with no editable `src/`, package manifest, router or client. Prototype palette/typeface differs from the Study Web design guide. |

### Trích từ DD nguồn: 7. Execution and verification sequence

1. [x] Read goal objective, router/context/worklog requirements, exact-type docs worklogs, screen inventory, cross-scope boundaries, manifest, AC-31, API catalog/DD, current route/module/query/model/auth/response/test source, prototype and screenshot.
2. [x] Write this plan before marker JSON/SVG, annotation, or AD-03 DD.
3. [x] Create 32 unique, ordered marker definitions and matching SVG/2× annotated PNG without editing original assets.
4. [x] Write AD-03 A–F DD with one row per marker, API/event/error mapping, screen states, navigation handoff and unresolved decisions clearly separated.
5. [x] Update AD-03 inventory row and global tracker with source/API and independent DD/implementation/runtime statuses; add session checkpoint.
6. [x] Update worklog with completed trace and verification results.
7. [x] Verify original hashes unchanged; annotation dimensions 3200×2912; marker IDs unique/sequential/in-bounds; marker rows match DD; JSON/SVG/local links valid; 83 screen IDs/folders remain consistent; scoped diff passes whitespace checks.
8. [x] Do not run application tests or runtime; mark source tests `INSPECTED_NOT_RUN` and runtime `NOT_VERIFIED`.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
