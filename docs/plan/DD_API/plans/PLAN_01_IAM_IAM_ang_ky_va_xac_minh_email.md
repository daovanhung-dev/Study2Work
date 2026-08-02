# PLAN 01 — IAM — Đăng ký và xác minh email

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-01` |
| API trong phạm vi | `API-IAM-001`, `API-IAM-002`, `API-IAM-003` |
| Số API | 3 |
| Read-only / Mutation | 0 / 3 |
| Khối lượng lõi | 24 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho vòng đời guest đăng ký, phát token xác minh và kích hoạt tài khoản.

**Luồng nghiệp vụ trọng tâm:** Guest gửi email/password và agreement; hệ thống chống trùng/idempotency, băm mật khẩu, tạo user pending, phát token một lần; xác minh khóa token và kích hoạt; resend luôn trả generic accepted.

**Điểm cần khóa:** Chống enumeration, token one-time, Argon2id, idempotency và audit.

**Dependency:** Identity database; email delivery qua outbox.

## 3. Phạm vi

**In-scope**

- `API-IAM-001` — `POST /api/v1/auth/register`.
- `API-IAM-002` — `POST /api/v1/auth/verify-email`.
- `API-IAM-003` — `POST /api/v1/auth/resend-verification`.

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

- `01_TONG_QUAN_DU_AN.md:L757` — `CAP-IAM-001` / `UC-IAM-001`; rules ``BR-IAM-001`, `BR-IAM-002`, `BR-IAM-008`, `NFR-OPS-003``; diagrams ``AC-IAM-001`, `SEQ-IAM-001``; data ``CLS-IAM-001`; `TBL-IAM-001–005`, `TBL-IAM-018``; screens ``SCR-IAM-001–002``; test ``TC-IAM-001``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-IAM-001` — `02_BIEU_DO_HE_THONG.md:L332` — AC-IAM-001 — Đăng ký, xác minh, đăng nhập, MFA và refresh.
- `SEQ-IAM-001` — `02_BIEU_DO_HE_THONG.md:L1719` — SEQ-IAM-001 — Register, verify, login/MFA và tạo projection.
- `CLS-IAM-001` — `02_BIEU_DO_HE_THONG.md:L845` — CLS-IAM-001 — Identity, credential, session và security event.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-IAM-001` — `users` — `03_THIET_KE_CO_SO_DU_LIEU.md:L101 `.
- `TBL-IAM-002` — `user_emails` — `03_THIET_KE_CO_SO_DU_LIEU.md:L109 `.
- `TBL-IAM-003` — `password_credentials` — `03_THIET_KE_CO_SO_DU_LIEU.md:L117 `.
- `TBL-IAM-004` — `email_verification_tokens` — `03_THIET_KE_CO_SO_DU_LIEU.md:L125 `.
- `TBL-IAM-005` — `password_reset_tokens` — `03_THIET_KE_CO_SO_DU_LIEU.md:L134 `.
- `TBL-IAM-018` — `outbox_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L234 `.

**Screen và acceptance**

- Screens: `SCR-IAM-001`, `SCR-IAM-002`.
- Acceptance: `TC-IAM-001`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-IAM-001` — `01_TONG_QUAN_DU_AN.md:L338` — V1 chỉ đăng ký bằng email/password. Email được trim, normalize domain và so khớp không phân biệt hoa thường; mỗi email chỉ thuộc một platform user chưa anonymize..
- `BR-IAM-002` — `01_TONG_QUAN_DU_AN.md:L339` — Account phải xác minh email trước khi dùng API được bảo vệ. Password chỉ lưu Argon2id hash; Study và Work không được lưu password, verification token hoặc refresh token..
- `BR-IAM-008` — `01_TONG_QUAN_DU_AN.md:L345` — Reset password, resend verification và login dùng phản hồi công khai không tiết lộ email có tồn tại; rate limit kết hợp IP, normalized email và device signal..
- `NFR-OPS-003` — `01_TONG_QUAN_DU_AN.md:L650` — p95 server latency: read đồng bộ ≤ 800 ms, mutation đồng bộ ≤ 1,5 giây; không tính phần việc đã công bố async. Query report lớn bắt buộc async/export..

## 5. Chi tiết từng API

### API-IAM-001 — `POST /api/v1/auth/register`

- **Nguồn contract:** `04_DAC_TA_API.md:L87`.
- **Actor/quyền:** Anonymous.
- **Input/validation → output:** Body`email`, password 12–128 ký tự, agreement versions, locale; email normalize/case-insensitive → pending user và `verificationExpiresAt`.
- **Xử lý và dữ liệu:** TX: claim idempotency; unique email; Argon2id; W`platform_users`, `password_credentials`, `user_agreement_acceptances`, hashed `one_time_tokens`, `identity_outbox_events`; không trả biết email tồn tại.
- **Vận hành:** Idempotency bắt buộc;`identity.user.registered`; security audit; 3/giờ/email hash.
- **Lỗi đặc thù:** `EMAIL_ALREADY_REGISTERED` chỉ trả sau generic accepted flow; `PASSWORD_POLICY_FAILED`, `AGREEMENT_VERSION_INVALID`.
- **Màn hình/consumer:** `SCR-IAM-001`.
- **Capability/use case:** `CAP-IAM-001`, `UC-IAM-001`.

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

### API-IAM-002 — `POST /api/v1/auth/verify-email`

- **Nguồn contract:** `04_DAC_TA_API.md:L88`.
- **Actor/quyền:** Anonymous.
- **Input/validation → output:** `token` 32–512 ký tự → access/refresh token và account `ACTIVE`.
- **Xử lý và dữ liệu:** TX + L token hash`FOR UPDATE`; kiểm purpose/expiry/unused; set verified/status, consume token, create session/refresh, outbox.
- **Vận hành:** Idempotency bắt buộc; event`identity.user.verified`; 10/phút/IP.
- **Lỗi đặc thù:** `TOKEN_INVALID_OR_EXPIRED`, `TOKEN_ALREADY_USED`.
- **Màn hình/consumer:** `SCR-IAM-002`.
- **Capability/use case:** `CAP-IAM-001`, `UC-IAM-001`.

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

### API-IAM-003 — `POST /api/v1/auth/resend-verification`

- **Nguồn contract:** `04_DAC_TA_API.md:L89`.
- **Actor/quyền:** Anonymous.
- **Input/validation → output:** `email`; luôn trả accepted.
- **Xử lý và dữ liệu:** Nếu pending và cooldown hết: revoke token cũ, tạo token hash + email delivery/outbox; không tiết lộ trạng thái account.
- **Vận hành:** Dedupe 10 phút; 3/giờ/email hash.
- **Lỗi đặc thù:** `RESEND_COOLDOWN` chỉ khi session đã chứng minh ownership.
- **Màn hình/consumer:** `SCR-IAM-002`.
- **Capability/use case:** `CAP-IAM-001`, `UC-IAM-001`.

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
