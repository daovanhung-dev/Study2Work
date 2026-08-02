# PLAN 20 — Study — Pre-publish, publish, archive và content issue

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-20` |
| API trong phạm vi | `API-STU-055`, `API-STU-056`, `API-STU-057`, `API-STU-058`, `API-STU-059` |
| Số API | 5 |
| Read-only / Mutation | 1 / 4 |
| Khối lượng lõi | 40 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho pre-check, atomic publish, archive và xử lý content issues.

**Luồng nghiệp vụ trọng tâm:** Pre-check tổng hợp rights/asset/policy/reviewer; publish khóa stable+version và swap current atomically; archive không xóa version được pin; issue list/update theo workflow.

**Điểm cần khóa:** Atomic version swap, enrollment pinning, cache invalidation, reviewer race.

**Dependency:** Plan 19; trusted grants Plan 54.

## 3. Phạm vi

**In-scope**

- `API-STU-055` — `POST /api/v1/admin/content/{kind}/{id}/versions/{versionId}/pre-publish-checks`.
- `API-STU-056` — `POST /api/v1/admin/content/{kind}/{id}/versions/{versionId}/publish`.
- `API-STU-057` — `POST /api/v1/admin/content/{kind}/{id}/archive`.
- `API-STU-058` — `GET /api/v1/admin/content-issues`.
- `API-STU-059` — `PUT /api/v1/admin/content-issues/{id}/status`.

**Out-of-scope**

- Không tạo DD cho API ngoài danh sách trên.
- Không sửa BD, template hoặc DD đã approved ngoài phạm vi.
- Không tự tạo endpoint, request/response field, table/column, role, business code, transaction hoặc business rule.
- Không triển khai source code, OpenAPI hoặc migration trong plan này.

## 4. Nguồn bắt buộc và truy vết

- `04_DAC_TA_API.md`: contract HTTP/internal/realtime, quy ước dùng chung, endpoint row, error và transaction matrix.
- `03_THIET_KE_CO_SO_DU_LIEU.md`: table/column/constraint/index/transaction/retention.
- `02_BIEU_DO_HE_THONG.md`: activity, sequence, class, lỗi và cạnh tranh.
- `01_TONG_QUAN_DU_AN.md`: capability, use case, rule, permission, NFR, state machine và acceptance.
- `05_DAC_TA_MAN_HINH.md`: consumer/screen/CTA/validation để kiểm coverage, không thay API source.

**Dòng traceability liên quan**

- `01_TONG_QUAN_DU_AN.md:L765` — `CAP-STU-006` / `UC-STU-006`; rules ``BR-STU-007`, `BR-STU-013–014`, `PERM-STU-001–005``; diagrams ``AC-STU-003`, `SEQ-STU-004``; data ``CLS-STU-001`; `TBL-STU-009–025`, `TBL-STU-035–036``; screens ``SCR-OPS-003–011``; test ``TC-STU-006``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-STU-003` — `02_BIEU_DO_HE_THONG.md:L465` — AC-STU-003 — Soạn và publish content version.
- `SEQ-STU-004` — `02_BIEU_DO_HE_THONG.md:L1978` — SEQ-STU-004 — Pre-publish, atomic version swap và cache invalidation.
- `CLS-STU-001` — `02_BIEU_DO_HE_THONG.md:L931` — CLS-STU-001 — Study profile, RBAC và curriculum versioning.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-STU-009` — `learning_paths` — `03_THIET_KE_CO_SO_DU_LIEU.md:L320 `.
- `TBL-STU-010` — `learning_path_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L327 `.
- `TBL-STU-011` — `courses` — `03_THIET_KE_CO_SO_DU_LIEU.md:L334 `.
- `TBL-STU-012` — `course_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L341 `.
- `TBL-STU-013` — `path_course_items` — `03_THIET_KE_CO_SO_DU_LIEU.md:L348 `.
- `TBL-STU-014` — `chapters` — `03_THIET_KE_CO_SO_DU_LIEU.md:L355 `.
- `TBL-STU-015` — `lessons` — `03_THIET_KE_CO_SO_DU_LIEU.md:L362 `.
- `TBL-STU-016` — `content_blocks` — `03_THIET_KE_CO_SO_DU_LIEU.md:L369 `.
- `TBL-STU-017` — `content_rights_attestations` — `03_THIET_KE_CO_SO_DU_LIEU.md:L376 `.
- `TBL-STU-018` — `content_review_decisions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L383 `.
- `TBL-STU-019` — `trusted_publisher_grants` — `03_THIET_KE_CO_SO_DU_LIEU.md:L390 `.
- `TBL-STU-020` — `assessments` — `03_THIET_KE_CO_SO_DU_LIEU.md:L399 `.
- `TBL-STU-021` — `assessment_placements` — `03_THIET_KE_CO_SO_DU_LIEU.md:L406 `.
- `TBL-STU-022` — `quiz_questions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L413 `.
- `TBL-STU-023` — `quiz_options` — `03_THIET_KE_CO_SO_DU_LIEU.md:L420 `.
- `TBL-STU-024` — `rubrics` — `03_THIET_KE_CO_SO_DU_LIEU.md:L427 `.
- `TBL-STU-025` — `rubric_criteria` — `03_THIET_KE_CO_SO_DU_LIEU.md:L434 `.
- `TBL-STU-035` — `file_objects` — `03_THIET_KE_CO_SO_DU_LIEU.md:L509 `.
- `TBL-STU-036` — `malware_scan_results` — `03_THIET_KE_CO_SO_DU_LIEU.md:L517 `.

**Screen và acceptance**

- Screens: `SCR-OPS-003`, `SCR-OPS-004`, `SCR-OPS-005`, `SCR-OPS-006`, `SCR-OPS-007`, `SCR-OPS-008`, `SCR-OPS-009`, `SCR-OPS-010`, `SCR-OPS-011`.
- Acceptance: `TC-STU-006`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-STU-007` — `01_TONG_QUAN_DU_AN.md:L357` — Published path/course version là bất biến. Publish version mới atomically đổi current version và đánh dấu bản cũ `SUPERSEDED`; enrollment cũ tiếp tục pin bản cũ..
- `BR-STU-013` — `01_TONG_QUAN_DU_AN.md:L363` — Mỗi assessment placement thuộc đúng một scope: path version, course version, chapter hoặc lesson. Quan hệ không hợp lệ bị chặn ở application và database constraint..
- `BR-STU-014` — `01_TONG_QUAN_DU_AN.md:L364` — Trusted publisher không được bỏ qua rights check, HTML/Markdown sanitization, malware scan, cấu trúc curriculum, rubric hoặc audit. Author không tự có quyền publish..
- `PERM-STU-001` — `01_TONG_QUAN_DU_AN.md:L150` — `study.content.read_admin` — Content Author/Publisher, Study Admin.
- `PERM-STU-002` — `01_TONG_QUAN_DU_AN.md:L151` — `study.content.write` — Content Author/Publisher, Study Admin.
- `PERM-STU-003` — `01_TONG_QUAN_DU_AN.md:L152` — `study.content.publish` — Content Publisher, Study Admin.
- `PERM-STU-004` — `01_TONG_QUAN_DU_AN.md:L153` — `study.content.archive` — Study Admin.
- `PERM-STU-005` — `01_TONG_QUAN_DU_AN.md:L154` — `study.content_issues.manage` — Content Publisher, Study Admin.

## 5. Chi tiết từng API

### API-STU-055 — `POST /api/v1/admin/content/{kind}/{id}/versions/{versionId}/pre-publish-checks`

- **Nguồn contract:** `04_DAC_TA_API.md:L195`.
- **Actor/quyền:** Author/publisher.
- **Input/validation → output:** `If-Match` → immutable check report.
- **Xử lý và dữ liệu:** Read rights, structure, links syntax, all assets CLEAN, rubric/questions, accessibility metadata; W check snapshot.
- **Vận hành:** Idempotency; event check completed.
- **Lỗi đặc thù:** `VERSION_CONFLICT`.
- **Màn hình/consumer:** `SCR-OPS-007`.
- **Capability/use case:** `CAP-STU-006`, `UC-STU-006`.

**Tác vụ khi tạo DD cho API này**

1. Tách riêng từng header, path, query, body field và token/session-derived input; không suy diễn field từ UI nếu API source không nêu.
2. Lập Request Usage Matrix: mỗi field phải trỏ tới validation, query, branch, loop, mutation hoặc response usage.
3. Phân rã `Xử lý và dữ liệu` thành step Data Mapping theo đúng thứ tự: auth → permission/tenant → validation → query/check → branch/loop → mutation/TX → outbox → response.
4. Với mọi `R:`/query: xác nhận table ID/name/cột/index tại `03_THIET_KE_CO_SO_DU_LIEU.md`; mỗi selected column, JOIN và condition một dòng.
5. Với mọi `W:`/mutation: tạo Mutation Matrix và một DB Mapping file cho từng table/operation khác bản chất; mỗi DB column một row.
6. Map từng response path về DB/query/generated/fixed/calculated source. Field chưa có nguồn phải ghi `SOURCE_REQUIRED`, không tự tạo.
7. Tạo từng Error row từ lỗi đặc thù và lỗi dùng chung thực sự có branch; không đưa toàn bộ catalog lỗi vào API một cách máy móc.
8. Kiểm tra idempotency, `If-Match`, lock, transaction boundary, rollback, audit, event/outbox, cache và rate limit đúng nguồn.
9. Đối chiếu screen/consumer để kiểm coverage, nhưng không dùng UI âm thầm thay đổi API contract.

### API-STU-056 — `POST /api/v1/admin/content/{kind}/{id}/versions/{versionId}/publish`

- **Nguồn contract:** `04_DAC_TA_API.md:L196`.
- **Actor/quyền:** `PERM-STU-003` + MFA; trusted grant still requires checks.
- **Input/validation → output:** Check ID,`If-Match`, publish note → published version.
- **Xử lý và dữ liệu:** TX L stable/version; revalidate fresh successful check/requester rights/trusted grant; DRAFT→PUBLISHED, previous→SUPERSEDED, atomically swap current pointer.
- **Vận hành:** Idempotency required; event/cache invalidation/audit; no external call in TX.
- **Lỗi đặc thù:** `PUBLISH_CHECK_STALE`, `RIGHTS_INCOMPLETE`, `FILE_NOT_CLEAN`, `CONTENT_VERSION_NOT_EDITABLE`, `VERSION_CONFLICT`.
- **Màn hình/consumer:** `SCR-OPS-007`.
- **Capability/use case:** `CAP-STU-006`, `UC-STU-006`.

**Tác vụ khi tạo DD cho API này**

1. Tách riêng từng header, path, query, body field và token/session-derived input; không suy diễn field từ UI nếu API source không nêu.
2. Lập Request Usage Matrix: mỗi field phải trỏ tới validation, query, branch, loop, mutation hoặc response usage.
3. Phân rã `Xử lý và dữ liệu` thành step Data Mapping theo đúng thứ tự: auth → permission/tenant → validation → query/check → branch/loop → mutation/TX → outbox → response.
4. Với mọi `R:`/query: xác nhận table ID/name/cột/index tại `03_THIET_KE_CO_SO_DU_LIEU.md`; mỗi selected column, JOIN và condition một dòng.
5. Với mọi `W:`/mutation: tạo Mutation Matrix và một DB Mapping file cho từng table/operation khác bản chất; mỗi DB column một row.
6. Map từng response path về DB/query/generated/fixed/calculated source. Field chưa có nguồn phải ghi `SOURCE_REQUIRED`, không tự tạo.
7. Tạo từng Error row từ lỗi đặc thù và lỗi dùng chung thực sự có branch; không đưa toàn bộ catalog lỗi vào API một cách máy móc.
8. Kiểm tra idempotency, `If-Match`, lock, transaction boundary, rollback, audit, event/outbox, cache và rate limit đúng nguồn.
9. Đối chiếu screen/consumer để kiểm coverage, nhưng không dùng UI âm thầm thay đổi API contract.

### API-STU-057 — `POST /api/v1/admin/content/{kind}/{id}/archive`

- **Nguồn contract:** `04_DAC_TA_API.md:L197`.
- **Actor/quyền:** `PERM-STU-004` + MFA.
- **Input/validation → output:** Reason, If-Match → archived stable entity.
- **Xử lý và dữ liệu:** TX prevent new enrollment/catalog; existing pinned enrollment remains usable; no version delete.
- **Vận hành:** Idempotency; audit/event.
- **Lỗi đặc thù:** `CONTENT_HAS_ACTIVE_DEPENDENCY`, `VERSION_CONFLICT`.
- **Màn hình/consumer:** `SCR-OPS-003`.
- **Capability/use case:** `CAP-STU-006`, `UC-STU-006`.

**Tác vụ khi tạo DD cho API này**

1. Tách riêng từng header, path, query, body field và token/session-derived input; không suy diễn field từ UI nếu API source không nêu.
2. Lập Request Usage Matrix: mỗi field phải trỏ tới validation, query, branch, loop, mutation hoặc response usage.
3. Phân rã `Xử lý và dữ liệu` thành step Data Mapping theo đúng thứ tự: auth → permission/tenant → validation → query/check → branch/loop → mutation/TX → outbox → response.
4. Với mọi `R:`/query: xác nhận table ID/name/cột/index tại `03_THIET_KE_CO_SO_DU_LIEU.md`; mỗi selected column, JOIN và condition một dòng.
5. Với mọi `W:`/mutation: tạo Mutation Matrix và một DB Mapping file cho từng table/operation khác bản chất; mỗi DB column một row.
6. Map từng response path về DB/query/generated/fixed/calculated source. Field chưa có nguồn phải ghi `SOURCE_REQUIRED`, không tự tạo.
7. Tạo từng Error row từ lỗi đặc thù và lỗi dùng chung thực sự có branch; không đưa toàn bộ catalog lỗi vào API một cách máy móc.
8. Kiểm tra idempotency, `If-Match`, lock, transaction boundary, rollback, audit, event/outbox, cache và rate limit đúng nguồn.
9. Đối chiếu screen/consumer để kiểm coverage, nhưng không dùng UI âm thầm thay đổi API contract.

### API-STU-058 — `GET /api/v1/admin/content-issues`

- **Nguồn contract:** `04_DAC_TA_API.md:L198`.
- **Actor/quyền:** `PERM-STU-005`.
- **Input/validation → output:** Page/status/severity/target → issue queue.
- **Xử lý và dữ liệu:** Indexed status/severity/reported; access sanitized.
- **Vận hành:** Private.
- **Lỗi đặc thù:** —.
- **Màn hình/consumer:** `SCR-OPS-008`.
- **Capability/use case:** `CAP-STU-006`, `UC-STU-006`.

**Tác vụ khi tạo DD cho API này**

1. Tách riêng từng header, path, query, body field và token/session-derived input; không suy diễn field từ UI nếu API source không nêu.
2. Lập Request Usage Matrix: mỗi field phải trỏ tới validation, query, branch, loop, mutation hoặc response usage.
3. Phân rã `Xử lý và dữ liệu` thành step Data Mapping theo đúng thứ tự: auth → permission/tenant → validation → query/check → branch/loop → mutation/TX → outbox → response.
4. Với mọi `R:`/query: xác nhận table ID/name/cột/index tại `03_THIET_KE_CO_SO_DU_LIEU.md`; mỗi selected column, JOIN và condition một dòng.
5. Với mọi `W:`/mutation: tạo Mutation Matrix và một DB Mapping file cho từng table/operation khác bản chất; mỗi DB column một row.
6. Map từng response path về DB/query/generated/fixed/calculated source. Field chưa có nguồn phải ghi `SOURCE_REQUIRED`, không tự tạo.
7. Tạo từng Error row từ lỗi đặc thù và lỗi dùng chung thực sự có branch; không đưa toàn bộ catalog lỗi vào API một cách máy móc.
8. Kiểm tra idempotency, `If-Match`, lock, transaction boundary, rollback, audit, event/outbox, cache và rate limit đúng nguồn.
9. Đối chiếu screen/consumer để kiểm coverage, nhưng không dùng UI âm thầm thay đổi API contract.

### API-STU-059 — `PUT /api/v1/admin/content-issues/{id}/status`

- **Nguồn contract:** `04_DAC_TA_API.md:L199`.
- **Actor/quyền:** `PERM-STU-005`.
- **Input/validation → output:** Status, resolution, If-Match → issue.
- **Xử lý và dữ liệu:** TX append issue event + update projection; terminal reopen requires reason.
- **Vận hành:** Idempotency; audit/notification.
- **Lỗi đặc thù:** `INVALID_ISSUE_TRANSITION`, `VERSION_CONFLICT`.
- **Màn hình/consumer:** `SCR-OPS-008`.
- **Capability/use case:** `CAP-STU-006`, `UC-STU-006`.

**Tác vụ khi tạo DD cho API này**

1. Tách riêng từng header, path, query, body field và token/session-derived input; không suy diễn field từ UI nếu API source không nêu.
2. Lập Request Usage Matrix: mỗi field phải trỏ tới validation, query, branch, loop, mutation hoặc response usage.
3. Phân rã `Xử lý và dữ liệu` thành step Data Mapping theo đúng thứ tự: auth → permission/tenant → validation → query/check → branch/loop → mutation/TX → outbox → response.
4. Với mọi `R:`/query: xác nhận table ID/name/cột/index tại `03_THIET_KE_CO_SO_DU_LIEU.md`; mỗi selected column, JOIN và condition một dòng.
5. Với mọi `W:`/mutation: tạo Mutation Matrix và một DB Mapping file cho từng table/operation khác bản chất; mỗi DB column một row.
6. Map từng response path về DB/query/generated/fixed/calculated source. Field chưa có nguồn phải ghi `SOURCE_REQUIRED`, không tự tạo.
7. Tạo từng Error row từ lỗi đặc thù và lỗi dùng chung thực sự có branch; không đưa toàn bộ catalog lỗi vào API một cách máy móc.
8. Kiểm tra idempotency, `If-Match`, lock, transaction boundary, rollback, audit, event/outbox, cache và rate limit đúng nguồn.
9. Đối chiếu screen/consumer để kiểm coverage, nhưng không dùng UI âm thầm thay đổi API contract.


## 6. Quy trình thực thi chi tiết

### Bước 0 — Nạp baseline bắt buộc

1. Đọc toàn bộ `createDD_MARKDOWN_SKILL.md` trước khi thao tác.
2. Mở đủ 8 file trong `DD_API_Template_MD/`; ghi fingerprint và heading/table/link baseline.
3. Đọc hai bộ mẫu chỉ để học style; không sao chép nghiệp vụ, table, column, role, error hoặc SQL.
4. Xác nhận 5 tài liệu BD đều đọc được; nếu thiếu một nguồn liên quan thì dừng API bị ảnh hưởng với `BLOCKED — MISSING SOURCE`.

### Bước 1 — Khóa phạm vi và source of truth

1. Tạo API Requirement Matrix chỉ cho các API trong plan.
2. Ghi rõ API ID, method/path, actor, auth, permission, input/output, screen, business rules, tables, transaction và event.
3. Phân loại từng dữ kiện `DIRECT`, `DERIVED`, `ASSUMPTION`, `CONFLICT` hoặc `UNSUPPORTED`.
4. API name canonical chưa có nguồn phải để `SOURCE_REQUIRED`; không biến endpoint slug thành tên approved.
5. Bất kỳ khác biệt giữa API, diagram, DB và screen phải vào `OPEN_QUESTIONS.md`; không chọn âm thầm.

### Bước 2 — Tạo bốn ma trận trước authoring

1. **Request Usage Matrix:** một row cho từng request/header/path/query/body/token field.
2. **Query Matrix:** một row cho từng query; liệt kê base table, alias, từng column, JOIN/ON, WHERE, GROUP/HAVING, ORDER, pagination, lock và result variable.
3. **Mutation Matrix:** một row cho từng INSERT/UPDATE/DELETE/UPSERT; ghi target table, record condition, field/value source, audit, TX và failure behavior.
4. **Response Source Matrix:** một row cho từng response path, kể cả nested/array; ghi source, transform và null/empty/omit rule.
5. Không điền template khi còn gap chưa được đánh dấu.

### Bước 3 — Tạo folder DD từ template

1. Copy nguyên folder template; không sửa template gốc.
2. Đặt folder theo `<API_ID>_<API_NAME>` khi có approved name; nếu chưa có, dùng working name có nhãn `DERIVED` và giữ trạng thái Draft.
3. Giữ `00_Cover.md` đến `07_table.md`, prefix, YAML, heading và table header.
4. Duplicate `07_table.md` thành `07+_<table>_<operation>.md` đúng từng mutation; read-only ghi `N/A — READ-ONLY API` theo template.

### Bước 4 — Thiết kế `05_Data_Mapping.md` trước

1. Nhận header/token/request, normalize và tạo biến; mỗi biến một dòng.
2. Xác thực JWT/service JWT, account projection, MFA/step-up và tenant scope.
3. Validate required/type/length/range/enum/format/unknown field; mỗi điều kiện một dòng.
4. Mô tả business check, state machine, permission, consent, entitlement và concurrency bằng branch cụ thể.
5. Viết từng query với mục đích, table/alias, từng cột, JOIN/ON, WHERE, ORDER/GROUP/HAVING, pagination/index/lock.
6. Viết transaction boundary, mutation order, audit column, outbox, commit/rollback và retry/failure behavior.
7. Map từng response field cụ thể; không dùng câu “map response” hoặc “truy vấn dữ liệu”.
8. Mỗi error branch liên kết tới anchor cụ thể trong `06_Error.md`; mỗi mutation liên kết hai chiều với DB Mapping.

### Bước 5 — Điền các file còn lại

1. `02_Overview.md`: mục đích, actor, auth, permission, source, tables read/write, TX, side effect, assumption/conflict, security/performance.
2. `03_Request.md`: mỗi input field một row, location rõ, validation/default/constraint và Data Mapping reference; JSON hợp lệ.
3. DB Mapping: mỗi column một row, source/value/audit/condition/step/TX; không thêm column không có schema.
4. `04_Response.md`: mỗi response path một row, source/transform/null rule; JSON success hợp lệ và không lộ dữ liệu nhạy cảm.
5. `06_Error.md`: mỗi lỗi một row, HTTP/business code/condition/handling/rollback/response/step.
6. `00_Cover.md` và `01_Lich_su.md`: metadata một hàng; unknown owner/version/date ghi `TBD — Cần xác nhận`.

### Bước 6 — Review chéo và kiểm chứng

1. Request → Data Mapping: 100% field được dùng hoặc giải thích.
2. Data Mapping → DB: table/column/alias/index/constraint tồn tại và đúng owner database.
3. DB/query → Response: 100% response field có source hoặc gap rõ.
4. Data Mapping → Error: 100% error branch có row; code/HTTP thống nhất.
5. Mutation → DB Mapping: mọi changed table/operation được bao phủ; transaction/rollback nhất quán.
6. Validate YAML, Markdown table, code fence, JSON, relative link/anchor, Unicode và one-field-per-line.
7. Chỉ báo `DONE` khi toàn bộ gate đạt; còn source gap dùng `PARTIALLY COMPLETED`, `BLOCKED` hoặc `NEEDS USER DECISION`.

## 7. Quality Gate riêng của plan

- [ ] Đủ DD folder cho toàn bộ API trong phạm vi, không thừa/thiếu API.
- [ ] Method/path/actor/permission khớp `04_DAC_TA_API.md`.
- [ ] Mọi source gap được ghi `SOURCE_REQUIRED`, `DERIVED` hoặc `CONFLICT`; không silently fill.
- [ ] Mỗi request/response/error/column/condition một row hoặc một dòng.
- [ ] Mỗi query có table, columns, JOIN/ON, WHERE, sort/group/pagination/index/lock khi áp dụng.
- [ ] Mỗi mutation có DB Mapping, audit, transaction, rollback và failure behavior.
- [ ] Request ↔ Data Mapping ↔ DB ↔ Response ↔ Error liên kết và nhất quán.
- [ ] JSON parse được; Markdown table/code fence/link/anchor hợp lệ.
- [ ] Có `PLAN_RESULT.md`, `VERIFICATION_REPORT.md`; có `OPEN_QUESTIONS.md` khi còn gap.

## 8. Deliverables của plan

1. 5 folder API DD tương ứng.
2. `PLAN_RESULT.md` cập nhật trạng thái từng API.
3. `VERIFICATION_REPORT.md` cho scope của plan.
4. `OPEN_QUESTIONS.md` nếu còn ảnh hưởng contract/DB/security/transaction.
5. `BUSINESS_CODE_DELTA.md` chỉ khi có code mới được nguồn approved xác nhận.

## 9. Điều kiện dừng

- Dừng API cụ thể nếu không xác định được request/response contract, target DB table/column, permission, transaction hoặc business code bắt buộc.
- Không được báo `DONE` cho API còn `SOURCE_REQUIRED`, conflict chưa quyết định hoặc validation chưa đạt.

Quay lại: [00_API_DD_PLAN_INDEX.md](../00_API_DD_PLAN_INDEX.md)
