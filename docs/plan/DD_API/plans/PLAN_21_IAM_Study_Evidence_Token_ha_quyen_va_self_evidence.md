# PLAN 21 — Study Evidence — Token hạ quyền và self evidence

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-21` |
| API trong phạm vi | `API-IAM-025`, `API-STU-061`, `API-STU-062` |
| Số API | 3 |
| Read-only / Mutation | 2 / 1 |
| Khối lượng lõi | 24 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho token exchange audience study-evidence và đọc evidence của chính learner.

**Luồng nghiệp vụ trọng tâm:** Identity cấp JWT 5 phút scope allowlist; Study xác minh audience/scope/owner; list/detail chỉ ISSUED và signed artifact URL riêng khi CLEAN.

**Điểm cần khóa:** Audience separation, nonce/session/authVersion, owner predicate, revoked/hidden behavior.

**Dependency:** Plan 57 internal evidence export.

## 3. Phạm vi

**In-scope**

- `API-IAM-025` — `POST /api/v1/auth/token-exchanges`.
- `API-STU-061` — `GET /api/v1/me/evidence`.
- `API-STU-062` — `GET /api/v1/me/evidence/{evidenceId}`.

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

- `01_TONG_QUAN_DU_AN.md:L764` — `CAP-STU-005` / `UC-STU-005`; rules ``BR-STU-016`, `BR-INT-004–009`, `NFR-OPS-006``; diagrams ``AC-INT-001`, `SEQ-INT-001``; data ``CLS-STU-002`, `CLS-INT-001`; `TBL-STU-031–032`, `TBL-STU-040–041`, `TBL-WRK-043–045``; screens ``SCR-WRK-017`, `SCR-WRK-019`, `SCR-WRK-040``; test ``TC-STU-005``.
- `01_TONG_QUAN_DU_AN.md:L773` — `CAP-WRK-006` / `UC-WRK-006`; rules ``BR-INT-004–009`, `BR-WRK-011`, `NFR-OPS-006``; diagrams ``AC-INT-001`, `SEQ-INT-001``; data ``CLS-INT-001`; `TBL-STU-040–041`, `TBL-WRK-043–045`, `TBL-WRK-069``; screens ``SCR-WRK-017`, `SCR-WRK-019`, `SCR-WRK-040``; test ``TC-WRK-006``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-INT-001` — `02_BIEU_DO_HE_THONG.md:L663` — AC-INT-001 — Chọn evidence khi apply và đồng bộ bất đồng bộ.
- `SEQ-INT-001` — `02_BIEU_DO_HE_THONG.md:L2206` — SEQ-INT-001 — Evidence selected-at-apply khi Study sẵn sàng hoặc gián đoạn.
- `CLS-STU-002` — `02_BIEU_DO_HE_THONG.md:L1059` — CLS-STU-002 — Enrollment, progress, assessment, file và evidence.
- `CLS-INT-001` — `02_BIEU_DO_HE_THONG.md:L1654` — CLS-INT-001 — Liên kết logic giữa ba database.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-STU-031` — `course_completions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L478 `.
- `TBL-STU-032` — `path_completions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L485 `.
- `TBL-STU-040` — `evidence_records` — `03_THIET_KE_CO_SO_DU_LIEU.md:L547 `.
- `TBL-STU-041` — `evidence_export_requests` — `03_THIET_KE_CO_SO_DU_LIEU.md:L555 `.
- `TBL-WRK-043` — `application_evidence_selections` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1009 `.
- `TBL-WRK-044` — `evidence_export_requests` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1016 `.
- `TBL-WRK-045` — `application_evidence_snapshots` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1023 `.
- `TBL-WRK-069` — `application_evidence_state_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1356 `.

**Screen và acceptance**

- Screens: `SCR-WRK-017`, `SCR-WRK-019`, `SCR-WRK-040`.
- Acceptance: `TC-STU-005`, `TC-WRK-006`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-STU-016` — `01_TONG_QUAN_DU_AN.md:L366` — Completion hợp lệ phát hành evidence `ISSUED` gắn owner và exact source version. Revoke chuyển `REVOKED`, giữ lịch sử và phát event; không tái sử dụng ID đã thu hồi..
- `BR-INT-004` — `01_TONG_QUAN_DU_AN.md:L399` — Apply wizard dùng access token đúng audience Study để learner chỉ liệt kê evidence của chính mình; token Work hoặc service token không được dùng để browse toàn bộ Study history..
- `BR-INT-005` — `01_TONG_QUAN_DU_AN.md:L400` — Candidate chọn rõ từng evidence và consent version trước submit. Application transaction lưu selected ID, consent, export request và outbox; Study outage không rollback application..
- `BR-INT-006` — `01_TONG_QUAN_DU_AN.md:L401` — Worker Work gửi signed export request. Study kiểm owner, `ISSUED`, source/version và revocation rồi chỉ trả snapshot tối thiểu; Work lưu snapshot gắn duy nhất với `applicationId`..
- `BR-INT-007` — `01_TONG_QUAN_DU_AN.md:L402` — Evidence export state tại Work là `PENDING`, `READY`, `UNAVAILABLE`, `REVOKED` hoặc `HIDDEN`. `UNAVAILABLE`/timeout không được tự reject, hạ score hoặc ẩn application..
- `BR-INT-008` — `01_TONG_QUAN_DU_AN.md:L403` — Consent withdrawal chuyển snapshot sang `HIDDEN`; Study revocation chuyển `REVOKED`. Nội dung không còn hiển thị cho recruiter nhưng audit tối thiểu được giữ theo retention..
- `BR-INT-009` — `01_TONG_QUAN_DU_AN.md:L404` — Event duplicate/stale bị bỏ qua theo aggregate version; event gap vào retry/catch-up. Poison event vào DLQ và không được đánh dấu thành công giả..
- `NFR-OPS-006` — `01_TONG_QUAN_DU_AN.md:L653` — Outbox/event projection p95 ≤ 60 giây khi bình thường; evidence export p95 ≤ 2 phút. Backlog, oldest age, retry và DLQ có alert..
- `BR-WRK-011` — `01_TONG_QUAN_DU_AN.md:L383` — Khi apply, Work chụp bất biến job revision, career profile, CV và portfolio được chọn. Thay đổi hồ sơ/CV/job sau đó không sửa application snapshot..

## 5. Chi tiết từng API

### API-IAM-025 — `POST /api/v1/auth/token-exchanges`

- **Nguồn contract:** `04_DAC_TA_API.md:L221`.
- **Actor/quyền:** Authenticated active.
- **Input/validation → output:** `audience=study-evidence`, scopes allowlist, nonce → JWT 5 phút.
- **Xử lý và dữ liệu:** Kiểm client Work đã đăng ký, current session/authVersion/MFA policy; không gọi Study; ký token có`act`, `aud`, `scope`, `nonce`.
- **Vận hành:** Idempotency; security audit; 20/phút.
- **Lỗi đặc thù:** `AUDIENCE_NOT_ALLOWED`, `SCOPE_NOT_ALLOWED`, `SESSION_REVOKED`.
- **Màn hình/consumer:** `SCR-WRK-017`.
- **Capability/use case:** `CAP-STU-005`, `UC-STU-005`, `CAP-WRK-006`, `UC-WRK-006`.

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

### API-STU-061 — `GET /api/v1/me/evidence`

- **Nguồn contract:** `04_DAC_TA_API.md:L214`.
- **Actor/quyền:** Learner; token`aud=study-evidence`, scope `evidence:self:read`.
- **Input/validation → output:** Page, type/status → evidence`ISSUED` của chính mình; không trả file bí mật mặc định.
- **Xử lý và dữ liệu:** Predicate platform subject→Study projection→owner; R evidence/version/skill; token 5 phút; không nhận arbitrary learner ID.
- **Vận hành:** Private no-store; access audit; 60/phút.
- **Lỗi đặc thù:** `TOKEN_AUDIENCE_INVALID`, `EVIDENCE_NOT_AVAILABLE`.
- **Màn hình/consumer:** `SCR-WRK-017`.
- **Capability/use case:** `CAP-STU-005`, `UC-STU-005`, `CAP-WRK-006`, `UC-WRK-006`.

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

### API-STU-062 — `GET /api/v1/me/evidence/{evidenceId}`

- **Nguồn contract:** `04_DAC_TA_API.md:L215`.
- **Actor/quyền:** Cùng actor.
- **Input/validation → output:** → mô tả, issuer, version, issued/revoked state, preview-safe fields.
- **Xử lý và dữ liệu:** Predicate exact owner + ID; signed file URL riêng nếu evidence có artifact CLEAN.
- **Vận hành:** Private no-store; audit.
- **Lỗi đặc thù:** `EVIDENCE_NOT_FOUND`, `EVIDENCE_REVOKED`.
- **Màn hình/consumer:** `SCR-WRK-017`.
- **Capability/use case:** `CAP-STU-005`, `UC-STU-005`, `CAP-WRK-006`, `UC-WRK-006`.

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
