# PLAN 52 — Operations — Verification case queue và decision

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-52` |
| API trong phạm vi | `API-OPS-001`, `API-OPS-002` |
| Số API | 2 |
| Read-only / Mutation | 1 / 1 |
| Khối lượng lõi | 16 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho admin list/claim/read verification cases và quyết định approve/reject.

**Luồng nghiệp vụ trọng tâm:** Query enterprise/university cases under permission; decision locks case/version, validates documents CLEAN/reviewer separation, updates tenant verification and emits events.

**Điểm cần khóa:** Cross-tenant admin scope, reviewer race, reason required, immutable decision.

**Dependency:** Plans 32,41.

## 3. Phạm vi

**In-scope**

- `API-OPS-001` — `GET /api/v1/admin/verification-cases`.
- `API-OPS-002` — `POST /api/v1/admin/verification-cases/{id}/decisions`.

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

- `01_TONG_QUAN_DU_AN.md:L770` — `CAP-WRK-003` / `UC-WRK-003`; rules ``BR-WRK-004–005`, `PERM-WRK-001–004`, `NFR-OPS-012``; diagrams `N/A — CRUD tenant/membership được kiểm qua authorization và constraint, không có saga ngoài verification review`; data ``CLS-WRK-001`; `TBL-WRK-014–018``; screens ``SCR-WRK-030–032`, `SCR-OPS-017–018``; test ``TC-WRK-003``.
- `01_TONG_QUAN_DU_AN.md:L777` — `CAP-WRK-010` / `UC-WRK-010`; rules ``BR-WRK-018`, `PERM-OPS-001–003`, `PERM-WRK-012`, `BR-OPS-001–002``; diagrams ``AC-OPS-001`, `SEQ-OPS-001``; data ``CLS-WRK-002`; `TBL-WRK-035–036`, `TBL-WRK-060–061``; screens ``SCR-OPS-009–011`, `SCR-OPS-017–018`, `SCR-OPS-021`, `SCR-OPS-024–026``; test ``TC-WRK-010``.
- `01_TONG_QUAN_DU_AN.md:L787` — `CAP-OPS-001` / `UC-OPS-001`; rules ``BR-WRK-018`, `BR-OPS-001–002`, `PERM-OPS-001–003`, `PERM-OPS-005``; diagrams ``AC-OPS-001`, `SEQ-OPS-001``; data ``CLS-WRK-002`; `TBL-WRK-015`, `TBL-WRK-020`, `TBL-WRK-035`, `TBL-WRK-060–061``; screens ``SCR-OPS-009–011`, `SCR-OPS-017–018`, `SCR-OPS-024–025``; test ``TC-OPS-001``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-OPS-001` — `02_BIEU_DO_HE_THONG.md:L802` — AC-OPS-001 — Moderation, deletion, legal hold và recovery.
- `SEQ-OPS-001` — `02_BIEU_DO_HE_THONG.md:L2554` — SEQ-OPS-001 — Moderation action, deletion fan-out và DLQ replay.
- `CLS-WRK-001` — `02_BIEU_DO_HE_THONG.md:L1266` — CLS-WRK-001 — Candidate, tenant, job, application và ATS snapshots.
- `CLS-WRK-002` — `02_BIEU_DO_HE_THONG.md:L1384` — CLS-WRK-002 — Interview, chat, university và moderation.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-WRK-014` — `enterprise_tenants` — `03_THIET_KE_CO_SO_DU_LIEU.md:L798 `.
- `TBL-WRK-015` — `enterprise_verification_cases` — `03_THIET_KE_CO_SO_DU_LIEU.md:L805 `.
- `TBL-WRK-016` — `enterprise_memberships` — `03_THIET_KE_CO_SO_DU_LIEU.md:L813 `.
- `TBL-WRK-017` — `enterprise_invites` — `03_THIET_KE_CO_SO_DU_LIEU.md:L820 `.
- `TBL-WRK-018` — `trusted_publisher_grants` — `03_THIET_KE_CO_SO_DU_LIEU.md:L827 `.
- `TBL-WRK-035` — `job_review_decisions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L950 `.
- `TBL-WRK-036` — `job_status_history` — `03_THIET_KE_CO_SO_DU_LIEU.md:L957 `.
- `TBL-WRK-060` — `moderation_reports` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1293 `.
- `TBL-WRK-061` — `audit_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1300 `.
- `TBL-WRK-020` — `university_verification_cases` — `03_THIET_KE_CO_SO_DU_LIEU.md:L843 `.

**Screen và acceptance**

- Screens: `SCR-WRK-030`, `SCR-WRK-031`, `SCR-WRK-032`, `SCR-OPS-017`, `SCR-OPS-018`, `SCR-OPS-009`, `SCR-OPS-010`, `SCR-OPS-011`, `SCR-OPS-021`, `SCR-OPS-024`, `SCR-OPS-025`, `SCR-OPS-026`.
- Acceptance: `TC-WRK-003`, `TC-WRK-010`, `TC-OPS-001`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-WRK-004` — `01_TONG_QUAN_DU_AN.md:L376` — Mọi enterprise/university query lấy tenant từ active membership phía server và lọc bằng tenant key; resource ID do client gửi không bao giờ đủ để cấp quyền. Composite tenant constraint ngăn liên kết chéo tenant..
- `BR-WRK-005` — `01_TONG_QUAN_DU_AN.md:L377` — Enterprise phải `VERIFIED` mới publish job, search candidate, gửi invitation hoặc mua quyền lợi tenant. Suspension chặn mutation mới nhưng giữ audit/history..
- `PERM-WRK-001` — `01_TONG_QUAN_DU_AN.md:L163` — `work.enterprise.profile.manage` — Enterprise Owner/Admin.
- `PERM-WRK-002` — `01_TONG_QUAN_DU_AN.md:L164` — `work.enterprise.verification.submit` — Enterprise Owner/Admin.
- `PERM-WRK-003` — `01_TONG_QUAN_DU_AN.md:L165` — `work.enterprise.members.read` — Enterprise Owner/Admin.
- `PERM-WRK-004` — `01_TONG_QUAN_DU_AN.md:L166` — `work.enterprise.members.manage` — Enterprise Owner/Admin.
- `NFR-OPS-012` — `01_TONG_QUAN_DU_AN.md:L659` — Backup mã hóa, kiểm restore; secret quay vòng; high/critical security finding, cross-tenant leak hoặc payment integrity failure là release blocker..
- `BR-WRK-018` — `01_TONG_QUAN_DU_AN.md:L390` — Moderation takedown giữ revision, application và audit; chặn discovery/apply mới nhưng không xóa lịch sử tuyển dụng hợp pháp..
- `PERM-OPS-001` — `01_TONG_QUAN_DU_AN.md:L199` — `operations.verification.review` — Platform Moderator được ủy quyền.
- `PERM-OPS-002` — `01_TONG_QUAN_DU_AN.md:L200` — `operations.job_review` — Platform Moderator.
- `PERM-OPS-003` — `01_TONG_QUAN_DU_AN.md:L201` — `operations.trusted_publisher.manage` — Platform Admin được ủy quyền.
- `PERM-WRK-012` — `01_TONG_QUAN_DU_AN.md:L169` — `work.jobs.submit_review` — Enterprise Owner/Admin, Recruiter được ủy quyền.
- `BR-OPS-001` — `01_TONG_QUAN_DU_AN.md:L448` — Audit/security/payment webhook/ledger/application history/evidence snapshot/AI review/outbox là append-only; không cascade delete làm mất lịch sử..
- `BR-OPS-002` — `01_TONG_QUAN_DU_AN.md:L449` — Audit chứa actor, effective role/tenant, action, resource, before/after đã redact, reason, IP/device tối thiểu, trace ID và thời điểm UTC; không chứa secret/token/raw password..
- `PERM-OPS-005` — `01_TONG_QUAN_DU_AN.md:L203` — `operations.break_glass.use` — Incident responder được chỉ định.

## 5. Chi tiết từng API

### API-OPS-001 — `GET /api/v1/admin/verification-cases`

- **Nguồn contract:** `04_DAC_TA_API.md:L422`.
- **Actor/quyền:** `PERM-OPS-001` + MFA.
- **Input/validation → output:** Page/type/status/age → enterprise/university cases.
- **Xử lý và dữ liệu:** Work DB query indexed type/status/submitted; documents accessed separately via signed URL.
- **Vận hành:** No cache; audit.
- **Lỗi đặc thù:** —.
- **Màn hình/consumer:** `SCR-OPS-017`.
- **Capability/use case:** `CAP-WRK-003`, `UC-WRK-003`, `CAP-WRK-010`, `UC-WRK-010`, `CAP-OPS-001`, `UC-OPS-001`.

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

### API-OPS-002 — `POST /api/v1/admin/verification-cases/{id}/decisions`

- **Nguồn contract:** `04_DAC_TA_API.md:L423`.
- **Actor/quyền:** `PERM-OPS-001`, not submitter.
- **Input/validation → output:** Approve/reject/request-info, reason/checklist, If-Match → decision.
- **Xử lý và dữ liệu:** TX L case/tenant; append decision, update tenant verification projection; no delete docs.
- **Vận hành:** Idempotency; high-risk audit/notification.
- **Lỗi đặc thù:** `SELF_REVIEW_FORBIDDEN`, `VERIFICATION_CONFLICT`, `VERSION_CONFLICT`.
- **Màn hình/consumer:** `SCR-OPS-018`.
- **Capability/use case:** `CAP-WRK-003`, `UC-WRK-003`, `CAP-WRK-010`, `UC-WRK-010`, `CAP-OPS-001`, `UC-OPS-001`.

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

1. 2 folder API DD tương ứng.
2. `PLAN_RESULT.md` cập nhật trạng thái từng API.
3. `VERIFICATION_REPORT.md` cho scope của plan.
4. `OPEN_QUESTIONS.md` nếu còn ảnh hưởng contract/DB/security/transaction.
5. `BUSINESS_CODE_DELTA.md` chỉ khi có code mới được nguồn approved xác nhận.

## 9. Điều kiện dừng

- Dừng API cụ thể nếu không xác định được request/response contract, target DB table/column, permission, transaction hoặc business code bắt buộc.
- Không được báo `DONE` cho API còn `SOURCE_REQUIRED`, conflict chưa quyết định hoặc validation chưa đạt.

Quay lại: [00_API_DD_PLAN_INDEX.md](../00_API_DD_PLAN_INDEX.md)
