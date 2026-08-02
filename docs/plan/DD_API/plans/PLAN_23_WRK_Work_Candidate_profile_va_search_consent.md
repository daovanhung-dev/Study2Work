# PLAN 23 — Work — Candidate profile và search consent

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-23` |
| API trong phạm vi | `API-WRK-005`, `API-WRK-006`, `API-WRK-007` |
| Số API | 3 |
| Read-only / Mutation | 1 / 2 |
| Khối lượng lõi | 24 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho profile cá nhân, update nested data và opt-in/opt-out sourcing.

**Luồng nghiệp vụ trọng tâm:** Profile owner read/update under If-Match; consent preview/terms; opt-out chặn DB read ngay và phát high-priority deindex outbox.

**Điểm cần khóa:** PII không copy vào search document, consent version/expiry, deindex SLO <=5m.

**Dependency:** Plan 58 search removal.

## 3. Phạm vi

**In-scope**

- `API-WRK-005` — `GET /api/v1/me/candidate-profile`.
- `API-WRK-006` — `PATCH /api/v1/me/candidate-profile`.
- `API-WRK-007` — `PUT /api/v1/me/candidate-search-consent`.

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

- `01_TONG_QUAN_DU_AN.md:L768` — `CAP-WRK-001` / `UC-WRK-001`; rules ``BR-WRK-001`, `BR-WRK-011`, `BR-OPS-004`, `NFR-OPS-003``; diagrams ``AC-WRK-001`, `SEQ-WRK-003``; data ``CLS-WRK-001`; `TBL-WRK-004–013`, `TBL-WRK-042``; screens ``SCR-WRK-011–014``; test ``TC-WRK-001``.
- `01_TONG_QUAN_DU_AN.md:L769` — `CAP-WRK-002` / `UC-WRK-002`; rules ``BR-WRK-001–003`, `BR-WRK-012`, `PERM-WRK-020–021`, `NFR-OPS-007``; diagrams ``AC-WRK-001`, `SEQ-WRK-001``; data ``CLS-WRK-001`; `TBL-WRK-005`, `TBL-WRK-037–040``; screens ``SCR-WRK-012`, `SCR-WRK-016`, `SCR-WRK-036–038``; test ``TC-WRK-002``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-WRK-001` — `02_BIEU_DO_HE_THONG.md:L548` — AC-WRK-001 — Candidate privacy, search, invitation và opt-out.
- `SEQ-WRK-003` — `02_BIEU_DO_HE_THONG.md:L2156` — SEQ-WRK-003 — Apply, immutable snapshots và ATS transition.
- `SEQ-WRK-001` — `02_BIEU_DO_HE_THONG.md:L2080` — SEQ-WRK-001 — Candidate opt-in/search, sponsored label và opt-out SLA.
- `CLS-WRK-001` — `02_BIEU_DO_HE_THONG.md:L1266` — CLS-WRK-001 — Candidate, tenant, job, application và ATS snapshots.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-WRK-004` — `candidate_profiles` — `03_THIET_KE_CO_SO_DU_LIEU.md:L726 `.
- `TBL-WRK-005` — `candidate_search_preferences` — `03_THIET_KE_CO_SO_DU_LIEU.md:L733 `.
- `TBL-WRK-006` — `skills` — `03_THIET_KE_CO_SO_DU_LIEU.md:L740 `.
- `TBL-WRK-007` — `candidate_skills` — `03_THIET_KE_CO_SO_DU_LIEU.md:L747 `.
- `TBL-WRK-008` — `candidate_experiences` — `03_THIET_KE_CO_SO_DU_LIEU.md:L754 `.
- `TBL-WRK-009` — `candidate_educations` — `03_THIET_KE_CO_SO_DU_LIEU.md:L761 `.
- `TBL-WRK-010` — `cvs` — `03_THIET_KE_CO_SO_DU_LIEU.md:L768 `.
- `TBL-WRK-011` — `cv_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L775 `.
- `TBL-WRK-012` — `portfolio_items` — `03_THIET_KE_CO_SO_DU_LIEU.md:L782 `.
- `TBL-WRK-013` — `saved_jobs` — `03_THIET_KE_CO_SO_DU_LIEU.md:L789 `.
- `TBL-WRK-042` — `application_snapshots` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1002 `.
- `TBL-WRK-037` — `candidate_search_documents` — `03_THIET_KE_CO_SO_DU_LIEU.md:L964 `.
- `TBL-WRK-038` — `candidate_invitations` — `03_THIET_KE_CO_SO_DU_LIEU.md:L971 `.
- `TBL-WRK-039` — `talent_lists` — `03_THIET_KE_CO_SO_DU_LIEU.md:L978 `.
- `TBL-WRK-040` — `talent_list_items` — `03_THIET_KE_CO_SO_DU_LIEU.md:L985 `.

**Screen và acceptance**

- Screens: `SCR-WRK-011`, `SCR-WRK-012`, `SCR-WRK-013`, `SCR-WRK-014`, `SCR-WRK-016`, `SCR-WRK-036`, `SCR-WRK-037`, `SCR-WRK-038`.
- Acceptance: `TC-WRK-001`, `TC-WRK-002`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-WRK-001` — `01_TONG_QUAN_DU_AN.md:L373` — Career profile mặc định `PRIVATE`. Chỉ candidate tự bật `SEARCHABLE`; không tenant, recruiter hoặc admin thông thường nào được bật thay..
- `BR-WRK-011` — `01_TONG_QUAN_DU_AN.md:L383` — Khi apply, Work chụp bất biến job revision, career profile, CV và portfolio được chọn. Thay đổi hồ sơ/CV/job sau đó không sửa application snapshot..
- `BR-OPS-004` — `01_TONG_QUAN_DU_AN.md:L451` — PII mã hóa khi truyền và khi lưu; object storage private theo namespace owner. Signed URL ngắn hạn, không được ghi vào audit/analytics/referrer..
- `NFR-OPS-003` — `01_TONG_QUAN_DU_AN.md:L650` — p95 server latency: read đồng bộ ≤ 800 ms, mutation đồng bộ ≤ 1,5 giây; không tính phần việc đã công bố async. Query report lớn bắt buộc async/export..
- `BR-WRK-002` — `01_TONG_QUAN_DU_AN.md:L374` — Candidate search chỉ chứa field public đã chọn, skill/kinh nghiệm tổng quát và availability; không trả email, phone, CV file, địa chỉ chi tiết, application, Study evidence hoặc thuộc tính nhạy cảm..
- `BR-WRK-003` — `01_TONG_QUAN_DU_AN.md:L375` — Opt-out phải làm hồ sơ biến mất khỏi kết quả và cache trong tối đa 5 phút. Snapshot/audit hợp pháp đã có trong application không bị xóa bởi opt-out tìm kiếm..
- `BR-WRK-012` — `01_TONG_QUAN_DU_AN.md:L384` — Invitation chỉ là lời mời có hạn; không tạo application, không cấp contact và không mở chat. Candidate phải chủ động submit application..
- `PERM-WRK-020` — `01_TONG_QUAN_DU_AN.md:L171` — `work.candidates.search` — Enterprise Owner/Admin, Recruiter có entitlement.
- `PERM-WRK-021` — `01_TONG_QUAN_DU_AN.md:L172` — `work.candidates.invite` — Enterprise Owner/Admin, Recruiter có entitlement.
- `NFR-OPS-007` — `01_TONG_QUAN_DU_AN.md:L654` — Candidate opt-out được kiểm end-to-end và đáp ứng hard limit 5 phút gồm DB projection, index, cache và active search response..

## 5. Chi tiết từng API

### API-WRK-005 — `GET /api/v1/me/candidate-profile`

- **Nguồn contract:** `04_DAC_TA_API.md:L238`.
- **Actor/quyền:** Candidate.
- **Input/validation → output:** → profile, completeness, privacy/search state/version.
- **Xử lý và dữ liệu:** R candidate profile/skills/experience/education; contact stays from Identity and is not copied into search document.
- **Vận hành:** Private no-store.
- **Lỗi đặc thù:** —.
- **Màn hình/consumer:** `SCR-WRK-011`.
- **Capability/use case:** `CAP-WRK-001`, `UC-WRK-001`.

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

### API-WRK-006 — `PATCH /api/v1/me/candidate-profile`

- **Nguồn contract:** `04_DAC_TA_API.md:L239`.
- **Actor/quyền:** Candidate.
- **Input/validation → output:** Allowlisted profile fields, skills, experiences, education,`If-Match` → profile.
- **Xử lý và dữ liệu:** TX L profile; validate dates/taxonomy; sanitize rich text; replace nested items with stable child IDs; version++.
- **Vận hành:** Idempotency optional; audit PII; enqueue search reindex only if opted-in.
- **Lỗi đặc thù:** `PROFILE_INVALID`, `DATE_RANGE_INVALID`, `VERSION_CONFLICT`.
- **Màn hình/consumer:** `SCR-WRK-011`.
- **Capability/use case:** `CAP-WRK-001`, `UC-WRK-001`.

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

### API-WRK-007 — `PUT /api/v1/me/candidate-search-consent`

- **Nguồn contract:** `04_DAC_TA_API.md:L240`.
- **Actor/quyền:** Candidate + step-up for opt-in.
- **Input/validation → output:** `enabled`, expiry optional, display fields allowlist, policy version, If-Match → state.
- **Xử lý và dữ liệu:** TX L profile; append consent event. Opt-in requires explicit preview/terms. Opt-out sets private synchronously and outbox high-priority deindex; API reads immediately exclude by DB predicate even before index removal.
- **Vận hành:** Idempotency; consent audit; deindex SLO <=5m.
- **Lỗi đặc thù:** `CONSENT_VERSION_INVALID`, `VERSION_CONFLICT`.
- **Màn hình/consumer:** `SCR-WRK-012`.
- **Capability/use case:** `CAP-WRK-001`, `UC-WRK-001`, `CAP-WRK-002`, `UC-WRK-002`.

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

1. 3 folder API DD tương ứng.
2. `PLAN_RESULT.md` cập nhật trạng thái từng API.
3. `VERIFICATION_REPORT.md` cho scope của plan.
4. `OPEN_QUESTIONS.md` nếu còn ảnh hưởng contract/DB/security/transaction.
5. `BUSINESS_CODE_DELTA.md` chỉ khi có code mới được nguồn approved xác nhận.

## 9. Điều kiện dừng

- Dừng API cụ thể nếu không xác định được request/response contract, target DB table/column, permission, transaction hoặc business code bắt buộc.
- Không được báo `DONE` cho API còn `SOURCE_REQUIRED`, conflict chưa quyết định hoặc validation chưa đạt.

Quay lại: [00_API_DD_PLAN_INDEX.md](../00_API_DD_PLAN_INDEX.md)
