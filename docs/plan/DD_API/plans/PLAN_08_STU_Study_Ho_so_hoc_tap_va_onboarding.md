# PLAN 08 — Study — Hồ sơ học tập và onboarding

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-08` |
| API trong phạm vi | `API-STU-007`, `API-STU-008`, `API-STU-009`, `API-STU-010`, `API-STU-011` |
| Số API | 5 |
| Read-only / Mutation | 2 / 3 |
| Khối lượng lõi | 40 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho đọc/sửa study profile, lưu onboarding từng phần và complete onboarding.

**Luồng nghiệp vụ trọng tâm:** Profile projection được đọc/sửa theo owner/If-Match; onboarding draft nhận field allowlist; complete kiểm đủ dữ liệu, seal submission và phát event.

**Điểm cần khóa:** Optimistic concurrency, schema validation, state DRAFT→COMPLETED và audit PII.

**Dependency:** Identity projection Plan 56.

## 3. Phạm vi

**In-scope**

- `API-STU-007` — `GET /api/v1/me/study-profile`.
- `API-STU-008` — `PATCH /api/v1/me/study-profile`.
- `API-STU-009` — `GET /api/v1/me/onboarding`.
- `API-STU-010` — `PATCH /api/v1/me/onboarding`.
- `API-STU-011` — `POST /api/v1/me/onboarding/complete`.

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

- `01_TONG_QUAN_DU_AN.md:L761` — `CAP-STU-002` / `UC-STU-002`; rules ``BR-STU-002–006`, `PERM-STU-009`, `BR-OPS-010``; diagrams ``AC-STU-001`, `SEQ-STU-001``; data ``CLS-STU-001–002`; `TBL-STU-002`, `TBL-STU-007–010`, `TBL-STU-026``; screens ``SCR-STU-011–013`, `SCR-OPS-015``; test ``TC-STU-002``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-STU-001` — `02_BIEU_DO_HE_THONG.md:L379` — AC-STU-001 — Standalone course, onboarding và primary-path switch.
- `SEQ-STU-001` — `02_BIEU_DO_HE_THONG.md:L1828` — SEQ-STU-001 — Standalone enrollment và primary-path switch cạnh tranh.
- `CLS-STU-001` — `02_BIEU_DO_HE_THONG.md:L931` — CLS-STU-001 — Study profile, RBAC và curriculum versioning.
- `CLS-STU-002` — `02_BIEU_DO_HE_THONG.md:L1059` — CLS-STU-002 — Enrollment, progress, assessment, file và evidence.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-STU-002` — `learner_profiles` — `03_THIET_KE_CO_SO_DU_LIEU.md:L267 `.
- `TBL-STU-007` — `onboarding_submissions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L304 `.
- `TBL-STU-008` — `path_recommendation_runs` — `03_THIET_KE_CO_SO_DU_LIEU.md:L311 `.
- `TBL-STU-009` — `learning_paths` — `03_THIET_KE_CO_SO_DU_LIEU.md:L320 `.
- `TBL-STU-010` — `learning_path_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L327 `.
- `TBL-STU-026` — `primary_path_periods` — `03_THIET_KE_CO_SO_DU_LIEU.md:L443 `.

**Screen và acceptance**

- Screens: `SCR-STU-011`, `SCR-STU-012`, `SCR-STU-013`, `SCR-OPS-015`.
- Acceptance: `TC-STU-002`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-STU-002` — `01_TONG_QUAN_DU_AN.md:L352` — Onboarding chỉ bắt buộc trước khi chọn primary path. Hoàn tất onboarding là đơn điệu; chỉnh profile tạo recommendation run mới nhưng không đưa trạng thái lùi..
- `BR-STU-003` — `01_TONG_QUAN_DU_AN.md:L353` — Mỗi learner có tối đa một primary path period `ACTIVE`; selection/switch dùng transaction lock và partial unique constraint..
- `BR-STU-004` — `01_TONG_QUAN_DU_AN.md:L354` — Self-switch bị khóa đúng 168 giờ tính theo UTC kể từ lần primary path thay đổi gần nhất. Initial selection và chọn sau khi path đã `COMPLETED` không bị cooldown..
- `BR-STU-005` — `01_TONG_QUAN_DU_AN.md:L355` — Admin chỉ bypass cooldown khi có `PERM-STU-009` (`study.primary_path.override`), nhập reason và xác nhận tác động; path mới vẫn có `nextSwitchAllowedAt = changedAt + 168 giờ`..
- `BR-STU-006` — `01_TONG_QUAN_DU_AN.md:L356` — Switch đóng period cũ bằng `SWITCHED_OUT`, tạo period mới atomically và không xóa course enrollment, progress, attempt, review, completion hay evidence..
- `PERM-STU-009` — `01_TONG_QUAN_DU_AN.md:L157` — `study.primary_path.override` — Learner Support được ủy quyền, Study Admin.
- `BR-OPS-010` — `01_TONG_QUAN_DU_AN.md:L457` — Mutation quan trọng dùng idempotency/optimistic version theo hợp đồng; conflict không silently overwrite và trả current version an toàn để client tải lại..

## 5. Chi tiết từng API

### API-STU-007 — `GET /api/v1/me/study-profile`

- **Nguồn contract:** `04_DAC_TA_API.md:L132`.
- **Actor/quyền:** Learner active.
- **Input/validation → output:** → profile, onboarding status, visibility.
- **Xử lý và dữ liệu:** R projection/profile/known skills by user PK.
- **Vận hành:** Private no-store.
- **Lỗi đặc thù:** `STUDY_PROJECTION_UNAVAILABLE`.
- **Màn hình/consumer:** `SCR-STU-023`.
- **Capability/use case:** `CAP-STU-002`, `UC-STU-002`.

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

### API-STU-008 — `PATCH /api/v1/me/study-profile`

- **Nguồn contract:** `04_DAC_TA_API.md:L133`.
- **Actor/quyền:** Learner active.
- **Input/validation → output:** Display name 1–100, bio <=1000, locale/timezone, skill IDs,`If-Match` → profile.
- **Xử lý và dữ liệu:** TX L profile; validate taxonomy; replace skill joins; profile version++.
- **Vận hành:** Idempotency optional; audit PII change.
- **Lỗi đặc thù:** `VERSION_CONFLICT`, `SKILL_NOT_FOUND`.
- **Màn hình/consumer:** `SCR-STU-023`.
- **Capability/use case:** `CAP-STU-002`, `UC-STU-002`.

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

### API-STU-009 — `GET /api/v1/me/onboarding`

- **Nguồn contract:** `04_DAC_TA_API.md:L134`.
- **Actor/quyền:** Learner active.
- **Input/validation → output:** → question schema, saved answers, status/version.
- **Xử lý và dữ liệu:** R onboarding + current configured questionnaire; never blocks standalone APIs.
- **Vận hành:** Private no-store.
- **Lỗi đặc thù:** —.
- **Màn hình/consumer:** `SCR-STU-011`.
- **Capability/use case:** `CAP-STU-002`, `UC-STU-002`.

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

### API-STU-010 — `PATCH /api/v1/me/onboarding`

- **Nguồn contract:** `04_DAC_TA_API.md:L135`.
- **Actor/quyền:** Learner active.
- **Input/validation → output:** Partial allowlisted answers,`If-Match` → saved draft.
- **Xử lý và dữ liệu:** TX L record; schema/type/range validate; status NOT_STARTED→IN_PROGRESS; version++.
- **Vận hành:** Idempotency optional; audit only category changes.
- **Lỗi đặc thù:** `ONBOARDING_ANSWER_INVALID`, `VERSION_CONFLICT`.
- **Màn hình/consumer:** `SCR-STU-011`.
- **Capability/use case:** `CAP-STU-002`, `UC-STU-002`.

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

### API-STU-011 — `POST /api/v1/me/onboarding/complete`

- **Nguồn contract:** `04_DAC_TA_API.md:L136`.
- **Actor/quyền:** Learner active.
- **Input/validation → output:** `If-Match` → completed record + recommendation run ID.
- **Xử lý và dữ liệu:** TX validate required answers; state COMPLETED; snapshot answers; create deterministic recommendation run/items.
- **Vận hành:** Idempotency required; event`study.onboarding.completed`; audit.
- **Lỗi đặc thù:** `ONBOARDING_INCOMPLETE`, `VERSION_CONFLICT`.
- **Màn hình/consumer:** `SCR-STU-011`.
- **Capability/use case:** `CAP-STU-002`, `UC-STU-002`.

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
