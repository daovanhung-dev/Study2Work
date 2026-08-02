# PLAN 38 — Work ATS — List/detail, assignee và note

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-38` |
| API trong phạm vi | `API-WRK-054`, `API-WRK-055`, `API-WRK-056`, `API-WRK-057` |
| Số API | 4 |
| Read-only / Mutation | 2 / 2 |
| Khối lượng lõi | 32 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho ATS read model, application detail, assignment và recruiter notes.

**Luồng nghiệp vụ trọng tâm:** List/detail tenant-first with immutable snapshots/evidence state; assignee update exact active members; notes append with visibility/audit and protected-attribute policy.

**Điểm cần khóa:** No candidate PII leakage beyond consent/snapshot, membership validity, note privacy.

**Dependency:** Plan 28/29.

## 3. Phạm vi

**In-scope**

- `API-WRK-054` — `GET /api/v1/enterprises/{enterpriseId}/applications`.
- `API-WRK-055` — `GET /api/v1/enterprises/{enterpriseId}/applications/{applicationId}`.
- `API-WRK-056` — `PUT /api/v1/enterprises/{enterpriseId}/applications/{applicationId}/assignees`.
- `API-WRK-057` — `POST /api/v1/enterprises/{enterpriseId}/applications/{applicationId}/notes`.

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

- `01_TONG_QUAN_DU_AN.md:L772` — `CAP-WRK-005` / `UC-WRK-005`; rules ``BR-WRK-008–012`, `PERM-WRK-030–034`, `BR-OPS-010``; diagrams ``AC-WRK-002`, `SEQ-WRK-003``; data ``CLS-WRK-001`; `TBL-WRK-041–048`, `TBL-WRK-072–073``; screens ``SCR-WRK-017–019`, `SCR-WRK-039–040``; test ``TC-WRK-005``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-WRK-002` — `02_BIEU_DO_HE_THONG.md:L582` — AC-WRK-002 — Job revision, apply và ATS.
- `SEQ-WRK-003` — `02_BIEU_DO_HE_THONG.md:L2156` — SEQ-WRK-003 — Apply, immutable snapshots và ATS transition.
- `CLS-WRK-001` — `02_BIEU_DO_HE_THONG.md:L1266` — CLS-WRK-001 — Candidate, tenant, job, application và ATS snapshots.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-WRK-041` — `applications` — `03_THIET_KE_CO_SO_DU_LIEU.md:L994 `.
- `TBL-WRK-042` — `application_snapshots` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1002 `.
- `TBL-WRK-043` — `application_evidence_selections` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1009 `.
- `TBL-WRK-044` — `evidence_export_requests` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1016 `.
- `TBL-WRK-045` — `application_evidence_snapshots` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1023 `.
- `TBL-WRK-046` — `application_status_history` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1030 `.
- `TBL-WRK-047` — `application_assignments` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1037 `.
- `TBL-WRK-048` — `application_notes` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1044 `.
- `TBL-WRK-072` — `application_offer_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1375 `.
- `TBL-WRK-073` — `application_offer_state_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1382 `.

**Screen và acceptance**

- Screens: `SCR-WRK-017`, `SCR-WRK-018`, `SCR-WRK-019`, `SCR-WRK-039`, `SCR-WRK-040`.
- Acceptance: `TC-WRK-005`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-WRK-008` — `01_TONG_QUAN_DU_AN.md:L380` — Mỗi candidate chỉ có một application cho một job. Idempotent replay trả application cũ; submit khác payload sau khi đã có application trả conflict..
- `BR-WRK-009` — `01_TONG_QUAN_DU_AN.md:L381` — Application lifecycle là `SUBMITTED → UNDER_REVIEW → SHORTLISTED → INTERVIEWING → OFFERED → HIRED`, với terminal `REJECTED`, `WITHDRAWN`, `OFFER_DECLINED`; mọi transition ghi actor, thời điểm và reason bắt buộc khi reject..
- `BR-WRK-010` — `01_TONG_QUAN_DU_AN.md:L382` — Candidate có thể chuyển `WITHDRAWN` từ `SUBMITTED`, `UNDER_REVIEW`, `SHORTLISTED` hoặc `INTERVIEWING`; ở `OFFERED`, từ chối của candidate phải là `OFFER_DECLINED`. Recruiter có thể `REJECTED` ở mọi trạng thái trước `HIRED`. Job đóng không tự đổi application đang xử lý..
- `BR-WRK-011` — `01_TONG_QUAN_DU_AN.md:L383` — Khi apply, Work chụp bất biến job revision, career profile, CV và portfolio được chọn. Thay đổi hồ sơ/CV/job sau đó không sửa application snapshot..
- `BR-WRK-012` — `01_TONG_QUAN_DU_AN.md:L384` — Invitation chỉ là lời mời có hạn; không tạo application, không cấp contact và không mở chat. Candidate phải chủ động submit application..
- `PERM-WRK-030` — `01_TONG_QUAN_DU_AN.md:L173` — `work.applications.list` — Enterprise Owner/Admin, Recruiter.
- `PERM-WRK-031` — `01_TONG_QUAN_DU_AN.md:L174` — `work.applications.read_unassigned` — Enterprise Owner/Admin; Recruiter chỉ khi được phân công nếu không có quyền này.
- `PERM-WRK-032` — `01_TONG_QUAN_DU_AN.md:L175` — `work.applications.assign` — Enterprise Owner/Admin, lead recruiter.
- `PERM-WRK-033` — mở đúng catalog ID trong `01_TONG_QUAN_DU_AN.md`.
- `PERM-WRK-034` — `01_TONG_QUAN_DU_AN.md:L176` — `work.applications.offer_manage` — Enterprise Owner/Admin, Recruiter được ủy quyền và phân công.
- `BR-OPS-010` — `01_TONG_QUAN_DU_AN.md:L457` — Mutation quan trọng dùng idempotency/optimistic version theo hợp đồng; conflict không silently overwrite và trả current version an toàn để client tải lại..

## 5. Chi tiết từng API

### API-WRK-054 — `GET /api/v1/enterprises/{enterpriseId}/applications`

- **Nguồn contract:** `04_DAC_TA_API.md:L322`.
- **Actor/quyền:** `PERM-WRK-030`.
- **Input/validation → output:** Page/job/status/assignee/date/q → ATS rows.
- **Xử lý và dữ liệu:** Tenant predicate via application.enterprise_id; composite indexes; q searches snapshot-safe fields only.
- **Vận hành:** Private; export separate permission.
- **Lỗi đặc thù:** `INVALID_FILTER`.
- **Màn hình/consumer:** `SCR-WRK-039`.
- **Capability/use case:** `CAP-WRK-005`, `UC-WRK-005`.

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

### API-WRK-055 — `GET /api/v1/enterprises/{enterpriseId}/applications/{applicationId}`

- **Nguồn contract:** `04_DAC_TA_API.md:L323`.
- **Actor/quyền:** Assigned recruiter or`PERM-WRK-031`.
- **Input/validation → output:** → immutable snapshots, answers, history, evidence state, interviews/chat; contact only after application.
- **Xử lý và dữ liệu:** Predicate tenant; field-level permission; evidence body only READY/not hidden/revoked.
- **Vận hành:** PII access audit; no-store.
- **Lỗi đặc thù:** `APPLICATION_NOT_FOUND`, `EVIDENCE_ACCESS_WITHDRAWN`.
- **Màn hình/consumer:** `SCR-WRK-040`.
- **Capability/use case:** `CAP-WRK-005`, `UC-WRK-005`.

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

### API-WRK-056 — `PUT /api/v1/enterprises/{enterpriseId}/applications/{applicationId}/assignees`

- **Nguồn contract:** `04_DAC_TA_API.md:L324`.
- **Actor/quyền:** `PERM-WRK-032`.
- **Input/validation → output:** Active member IDs, If-Match → assignments.
- **Xử lý và dữ liệu:** TX L application; all assignees same tenant and recruiter role; at least one primary for writable recruiter chat.
- **Vận hành:** Idempotency; audit/event.
- **Lỗi đặc thù:** `ASSIGNEE_INVALID`, `VERSION_CONFLICT`.
- **Màn hình/consumer:** `SCR-WRK-040`.
- **Capability/use case:** `CAP-WRK-005`, `UC-WRK-005`.

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

### API-WRK-057 — `POST /api/v1/enterprises/{enterpriseId}/applications/{applicationId}/notes`

- **Nguồn contract:** `04_DAC_TA_API.md:L325`.
- **Actor/quyền:** Assigned recruiter.
- **Input/validation → output:** Text <=5000, visibility INTERNAL, clean file optional → append note.
- **Xử lý và dữ liệu:** Tenant/assignment predicate; append-only, sanitize; never visible candidate.
- **Vận hành:** Idempotency; PII audit.
- **Lỗi đặc thù:** `RECRUITER_NOT_ASSIGNED`, `FILE_NOT_CLEAN`.
- **Màn hình/consumer:** `SCR-WRK-040`.
- **Capability/use case:** `CAP-WRK-005`, `UC-WRK-005`.

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
