# PLAN 50 — AI — Match explanation và shortlist suggestion

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-50` |
| API trong phạm vi | `API-AIX-003`, `API-AIX-004` |
| Số API | 2 |
| Read-only / Mutation | 0 / 2 |
| Khối lượng lõi | 16 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho AI hỗ trợ recruiter trên application/job.

**Luồng nghiệp vụ trọng tâm:** Create async job from immutable application/job snapshots; exclude protected attributes; output is explanation/suggestion only, human must decide ATS action.

**Điểm cần khóa:** No autonomous rejection/ranking mutation, fairness/provenance and tenant scope.

**Dependency:** Plans 38–39, Plan 49/52.

## 3. Phạm vi

**In-scope**

- `API-AIX-003` — `POST /api/v1/enterprises/{enterpriseId}/applications/{applicationId}/ai-match-explanations`.
- `API-AIX-004` — `POST /api/v1/enterprises/{enterpriseId}/jobs/{jobId}/ai-shortlist-jobs`.

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

- `01_TONG_QUAN_DU_AN.md:L785` — `CAP-AIX-002` / `UC-AIX-002`; rules ``BR-AIX-002–007`, `PERM-WRK-070–071`, `NFR-OPS-006``; diagrams ``AC-AIX-001`, `SEQ-AIX-001``; data ``CLS-AIX-001`; `TBL-AIX-004–007`, `TBL-WRK-041–042``; screens ``SCR-WRK-039–040``; test ``TC-AIX-002``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-AIX-001` — `02_BIEU_DO_HE_THONG.md:L767` — AC-AIX-001 — AI request, policy guard và human approval.
- `SEQ-AIX-001` — `02_BIEU_DO_HE_THONG.md:L2508` — SEQ-AIX-001 — AI async inference, safety gate và human-applied revision.
- `CLS-AIX-001` — `02_BIEU_DO_HE_THONG.md:L1584` — CLS-AIX-001 — AI job, provenance, review và human-applied revision.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-AIX-004` — `ai_jobs` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1134 `.
- `TBL-AIX-005` — `ai_outputs` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1142 `.
- `TBL-AIX-006` — `ai_human_reviews` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1149 `.
- `TBL-AIX-007` — `match_score_snapshots` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1156 `.
- `TBL-WRK-041` — `applications` — `03_THIET_KE_CO_SO_DU_LIEU.md:L994 `.
- `TBL-WRK-042` — `application_snapshots` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1002 `.

**Screen và acceptance**

- Screens: `SCR-WRK-039`, `SCR-WRK-040`.
- Acceptance: `TC-AIX-002`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-AIX-002` — `01_TONG_QUAN_DU_AN.md:L436` — AI chỉ tạo CV/JD draft, writing suggestion, match explanation và shortlist suggestion. Output không tự publish, gửi, apply, thay đổi ATS, reject, offer hoặc hire..
- `BR-AIX-003` — `01_TONG_QUAN_DU_AN.md:L437` — Người dùng phải nhìn thấy nhãn AI, review và chủ động accept/edit/reject. Bản accept lưu nội dung người dùng xác nhận, không giả định AI đúng..
- `BR-AIX-004` — `01_TONG_QUAN_DU_AN.md:L438` — Matching chỉ dùng skill, kinh nghiệm, học vấn công khai, tiêu chí job và preference nghề nghiệp được phép; loại gender, tuổi/ngày sinh, ảnh, dân tộc, tôn giáo, khuyết tật, tình trạng hôn nhân, địa chỉ chi tiết, payment và sponsored status..
- `BR-AIX-005` — `01_TONG_QUAN_DU_AN.md:L439` — Raw file, contact, chat riêng, feedback mật và Study history chưa được chọn không gửi vào AI. Evidence chỉ dùng field cấu trúc đã consent cho application tương ứng..
- `BR-AIX-006` — `01_TONG_QUAN_DU_AN.md:L440` — Input được giới hạn, phân tách khỏi system instruction và kiểm prompt injection; output phải qua schema validation, safety filter và không được thực thi như lệnh/tool call..
- `BR-AIX-007` — `01_TONG_QUAN_DU_AN.md:L441` — Lỗi/timeout AI không chặn tạo/sửa CV, job, apply hoặc ATS thủ công. Retry có giới hạn; người dùng không bị trừ credit lần hai cho retry kỹ thuật cùng task..
- `PERM-WRK-070` — `01_TONG_QUAN_DU_AN.md:L180` — `work.ai.match_explain` — Recruiter được phân công có entitlement.
- `PERM-WRK-071` — `01_TONG_QUAN_DU_AN.md:L181` — `work.ai.shortlist_suggest` — Enterprise Owner/Admin, lead recruiter có entitlement.
- `NFR-OPS-006` — `01_TONG_QUAN_DU_AN.md:L653` — Outbox/event projection p95 ≤ 60 giây khi bình thường; evidence export p95 ≤ 2 phút. Backlog, oldest age, retry và DLQ có alert..

## 5. Chi tiết từng API

### API-AIX-003 — `POST /api/v1/enterprises/{enterpriseId}/applications/{applicationId}/ai-match-explanations`

- **Nguồn contract:** `04_DAC_TA_API.md:L407`.
- **Actor/quyền:** Assigned recruiter +`PERM-WRK-070`.
- **Input/validation → output:** Job/application snapshot versions → async job.
- **Xử lý và dữ liệu:** Use only application snapshots and allowlisted job criteria; explicitly exclude name, age/date of birth, gender, photo, address granularity, university prestige proxy, contact, evidence; deterministic feature manifest stored.
- **Vận hành:** Idempotency; access/audit; 10/hour/member.
- **Lỗi đặc thù:** `AI_INPUT_INCOMPLETE`, `AI_DISABLED`, `APPLICATION_NOT_FOUND`.
- **Màn hình/consumer:** `SCR-WRK-040`.
- **Capability/use case:** `CAP-AIX-002`, `UC-AIX-002`.

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

### API-AIX-004 — `POST /api/v1/enterprises/{enterpriseId}/jobs/{jobId}/ai-shortlist-jobs`

- **Nguồn contract:** `04_DAC_TA_API.md:L408`.
- **Actor/quyền:** `PERM-WRK-071` + human reviewer.
- **Input/validation → output:** Explicit application IDs <=100, criteria version → async suggestions.
- **Xử lý và dữ liệu:** Snapshot allowed fields; output rank band/reasons/uncertainty only. Never write application status, reject, offer or hire.
- **Vận hành:** Idempotency; audit selected population/excluded fields.
- **Lỗi đặc thù:** `AI_BATCH_TOO_LARGE`, `HUMAN_REVIEWER_REQUIRED`, `AI_DISABLED`.
- **Màn hình/consumer:** `SCR-WRK-039`.
- **Capability/use case:** `CAP-AIX-002`, `UC-AIX-002`.

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
