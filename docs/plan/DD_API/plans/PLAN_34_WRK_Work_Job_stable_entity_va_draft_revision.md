# PLAN 34 — Work — Job stable entity và draft revision

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-34` |
| API trong phạm vi | `API-WRK-042`, `API-WRK-043`, `API-WRK-044`, `API-WRK-045` |
| Số API | 4 |
| Read-only / Mutation | 1 / 3 |
| Khối lượng lõi | 32 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho list tenant jobs, create job, create revision và patch draft.

**Luồng nghiệp vụ trọng tâm:** Tenant-first list; create stable+draft; revision copy current; patch typed fields/skills/screening under schema/sanitize/If-Match.

**Điểm cần khóa:** Immutable published revisions, tenant composite keys, protected-question policy.

**Dependency:** Plans 35–36; AI Plan 50/51.

## 3. Phạm vi

**In-scope**

- `API-WRK-042` — `GET /api/v1/enterprises/{enterpriseId}/jobs`.
- `API-WRK-043` — `POST /api/v1/enterprises/{enterpriseId}/jobs`.
- `API-WRK-044` — `POST /api/v1/enterprises/{enterpriseId}/jobs/{jobId}/revisions`.
- `API-WRK-045` — `PATCH /api/v1/enterprises/{enterpriseId}/jobs/{jobId}/revisions/{revisionId}`.

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

- `01_TONG_QUAN_DU_AN.md:L771` — `CAP-WRK-004` / `UC-WRK-004`; rules ``BR-WRK-005–007`, `PERM-WRK-010–013`, `BR-OPS-010``; diagrams ``AC-WRK-002`, `SEQ-WRK-002``; data ``CLS-WRK-001`; `TBL-WRK-032–036`, `TBL-WRK-074``; screens ``SCR-WRK-033–035`, `SCR-OPS-009–011``; test ``TC-WRK-004``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-WRK-002` — `02_BIEU_DO_HE_THONG.md:L582` — AC-WRK-002 — Job revision, apply và ATS.
- `SEQ-WRK-002` — `02_BIEU_DO_HE_THONG.md:L2119` — SEQ-WRK-002 — Job revision, review và publish cạnh tranh.
- `CLS-WRK-001` — `02_BIEU_DO_HE_THONG.md:L1266` — CLS-WRK-001 — Candidate, tenant, job, application và ATS snapshots.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-WRK-032` — `jobs` — `03_THIET_KE_CO_SO_DU_LIEU.md:L929 `.
- `TBL-WRK-033` — `job_revisions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L936 `.
- `TBL-WRK-034` — `job_skill_requirements` — `03_THIET_KE_CO_SO_DU_LIEU.md:L943 `.
- `TBL-WRK-035` — `job_review_decisions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L950 `.
- `TBL-WRK-036` — `job_status_history` — `03_THIET_KE_CO_SO_DU_LIEU.md:L957 `.
- `TBL-WRK-074` — `job_screening_questions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1389 `.

**Screen và acceptance**

- Screens: `SCR-WRK-033`, `SCR-WRK-034`, `SCR-WRK-035`, `SCR-OPS-009`, `SCR-OPS-010`, `SCR-OPS-011`.
- Acceptance: `TC-WRK-004`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-WRK-005` — `01_TONG_QUAN_DU_AN.md:L377` — Enterprise phải `VERIFIED` mới publish job, search candidate, gửi invitation hoặc mua quyền lợi tenant. Suspension chặn mutation mới nhưng giữ audit/history..
- `BR-WRK-006` — `01_TONG_QUAN_DU_AN.md:L378` — Job dùng stable entity và immutable revision. Sửa job đang published tạo draft revision mới; bản đang published vẫn phục vụ cho đến khi bản mới được duyệt và swap atomically..
- `BR-WRK-007` — `01_TONG_QUAN_DU_AN.md:L379` — Job lifecycle duy nhất là `DRAFT → REVIEW_PENDING → PUBLISHED ↔ PAUSED → CLOSED|EXPIRED|TAKEN_DOWN`; transition phải đúng quyền, version và audit..
- `PERM-WRK-010` — `01_TONG_QUAN_DU_AN.md:L167` — `work.jobs.read_admin` — Enterprise Owner/Admin, Recruiter.
- `PERM-WRK-011` — `01_TONG_QUAN_DU_AN.md:L168` — `work.jobs.author` — Enterprise Owner/Admin, Recruiter.
- `PERM-WRK-012` — `01_TONG_QUAN_DU_AN.md:L169` — `work.jobs.submit_review` — Enterprise Owner/Admin, Recruiter được ủy quyền.
- `PERM-WRK-013` — `01_TONG_QUAN_DU_AN.md:L170` — `work.jobs.publish_manage` — Enterprise Owner/Admin; trusted publisher theo grant có hạn.
- `BR-OPS-010` — `01_TONG_QUAN_DU_AN.md:L457` — Mutation quan trọng dùng idempotency/optimistic version theo hợp đồng; conflict không silently overwrite và trả current version an toàn để client tải lại..

## 5. Chi tiết từng API

### API-WRK-042 — `GET /api/v1/enterprises/{enterpriseId}/jobs`

- **Nguồn contract:** `04_DAC_TA_API.md:L303`.
- **Actor/quyền:** `PERM-WRK-010`.
- **Input/validation → output:** Page/lifecycle/q/owner → jobs/current revision.
- **Xử lý và dữ liệu:** Tenant predicate +`(enterprise_id,lifecycle,updated_at)`.
- **Vận hành:** Private.
- **Lỗi đặc thù:** —.
- **Màn hình/consumer:** `SCR-WRK-033`.
- **Capability/use case:** `CAP-WRK-004`, `UC-WRK-004`.

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

### API-WRK-043 — `POST /api/v1/enterprises/{enterpriseId}/jobs`

- **Nguồn contract:** `04_DAC_TA_API.md:L304`.
- **Actor/quyền:** `PERM-WRK-011`.
- **Input/validation → output:** Title, owner, initial structured JD → stable job + DRAFT revision.
- **Xử lý và dữ liệu:** TX validate verified tenant/entitlement; create stable job/revision; sanitize content.
- **Vận hành:** Idempotency; audit.
- **Lỗi đặc thù:** `ENTERPRISE_NOT_VERIFIED`, `JOB_QUOTA_EXCEEDED`.
- **Màn hình/consumer:** `SCR-WRK-034`.
- **Capability/use case:** `CAP-WRK-004`, `UC-WRK-004`.

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

### API-WRK-044 — `POST /api/v1/enterprises/{enterpriseId}/jobs/{jobId}/revisions`

- **Nguồn contract:** `04_DAC_TA_API.md:L305`.
- **Actor/quyền:** `PERM-WRK-011`.
- **Input/validation → output:** Base revision ID/change note → DRAFT revision.
- **Xử lý và dữ liệu:** Tenant predicate; copy immutable revision; only one editable draft/job/member policy.
- **Vận hành:** Idempotency; audit.
- **Lỗi đặc thù:** `DRAFT_ALREADY_EXISTS`, `BASE_REVISION_INVALID`.
- **Màn hình/consumer:** `SCR-WRK-034`.
- **Capability/use case:** `CAP-WRK-004`, `UC-WRK-004`.

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

### API-WRK-045 — `PATCH /api/v1/enterprises/{enterpriseId}/jobs/{jobId}/revisions/{revisionId}`

- **Nguồn contract:** `04_DAC_TA_API.md:L306`.
- **Actor/quyền:** Author/`PERM-WRK-011`.
- **Input/validation → output:** Structured JD, skills, salary, location, questions,`If-Match` → draft.
- **Xử lý và dữ liệu:** TX L revision; DRAFT only; checks salary range, taxonomy, expiry, prohibited content, sanitized Markdown.
- **Vận hành:** Autosave; audit diff; no index until publish.
- **Lỗi đặc thù:** `JOB_REVISION_NOT_EDITABLE`, `VERSION_CONFLICT`, `JOB_CONTENT_POLICY_FAILED`.
- **Màn hình/consumer:** `SCR-WRK-034`.
- **Capability/use case:** `CAP-WRK-004`, `UC-WRK-004`.

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

1. 4 folder API DD tương ứng.
2. `PLAN_RESULT.md` cập nhật trạng thái từng API.
3. `VERIFICATION_REPORT.md` cho scope của plan.
4. `OPEN_QUESTIONS.md` nếu còn ảnh hưởng contract/DB/security/transaction.
5. `BUSINESS_CODE_DELTA.md` chỉ khi có code mới được nguồn approved xác nhận.

## 9. Điều kiện dừng

- Dừng API cụ thể nếu không xác định được request/response contract, target DB table/column, permission, transaction hoặc business code bắt buộc.
- Không được báo `DONE` cho API còn `SOURCE_REQUIRED`, conflict chưa quyết định hoặc validation chưa đạt.

Quay lại: [00_API_DD_PLAN_INDEX.md](../00_API_DD_PLAN_INDEX.md)
