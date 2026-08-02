# PLAN 14 — Study — File upload, scan và download URL

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-14` |
| API trong phạm vi | `API-STU-030`, `API-STU-031`, `API-STU-032`, `API-STU-033` |
| Số API | 4 |
| Read-only / Mutation | 1 / 3 |
| Khối lượng lõi | 32 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho upload session, finalize, polling scan và cấp signed download URL.

**Luồng nghiệp vụ trọng tâm:** Khởi tạo multipart metadata; finalize kiểm size/hash rồi enqueue scan; status read; download chỉ CLEAN và re-authorize owner/purpose.

**Điểm cần khóa:** Malware quarantine, signed URL tối đa 5 phút, MIME/hash, no multipart payload lớn.

**Dependency:** Assessment/content APIs dùng chung.

## 3. Phạm vi

**In-scope**

- `API-STU-030` — `POST /api/v1/file-upload-sessions`.
- `API-STU-031` — `POST /api/v1/file-upload-sessions/{id}/finalize`.
- `API-STU-032` — `GET /api/v1/file-assets/{fileId}/status`.
- `API-STU-033` — `POST /api/v1/file-assets/{fileId}/download-urls`.

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

- `01_TONG_QUAN_DU_AN.md:L763` — `CAP-STU-004` / `UC-STU-004`; rules ``BR-STU-010–013`, `BR-STU-015`, `PERM-STU-006`, `NFR-OPS-008``; diagrams ``AC-STU-002`, `SEQ-STU-002–003``; data ``CLS-STU-002`; `TBL-STU-020–025`, `TBL-STU-033–039`, `TBL-STU-059``; screens ``SCR-STU-017–018`, `SCR-OPS-012–013``; test ``TC-STU-004``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-STU-002` — `02_BIEU_DO_HE_THONG.md:L416` — AC-STU-002 — Học bài, assessment, file scan và completion.
- `SEQ-STU-002` — `02_BIEU_DO_HE_THONG.md:L1881` — SEQ-STU-002 — Lesson progress và quiz auto-grade.
- `SEQ-STU-003` — `02_BIEU_DO_HE_THONG.md:L1923` — SEQ-STU-003 — Upload quarantine, scan, submit và hai reviewer cạnh tranh.
- `CLS-STU-002` — `02_BIEU_DO_HE_THONG.md:L1059` — CLS-STU-002 — Enrollment, progress, assessment, file và evidence.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-STU-020` — `assessments` — `03_THIET_KE_CO_SO_DU_LIEU.md:L399 `.
- `TBL-STU-021` — `assessment_placements` — `03_THIET_KE_CO_SO_DU_LIEU.md:L406 `.
- `TBL-STU-022` — `quiz_questions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L413 `.
- `TBL-STU-023` — `quiz_options` — `03_THIET_KE_CO_SO_DU_LIEU.md:L420 `.
- `TBL-STU-024` — `rubrics` — `03_THIET_KE_CO_SO_DU_LIEU.md:L427 `.
- `TBL-STU-025` — `rubric_criteria` — `03_THIET_KE_CO_SO_DU_LIEU.md:L434 `.
- `TBL-STU-033` — `assessment_attempts` — `03_THIET_KE_CO_SO_DU_LIEU.md:L494 `.
- `TBL-STU-034` — `assessment_answers` — `03_THIET_KE_CO_SO_DU_LIEU.md:L502 `.
- `TBL-STU-035` — `file_objects` — `03_THIET_KE_CO_SO_DU_LIEU.md:L509 `.
- `TBL-STU-036` — `malware_scan_results` — `03_THIET_KE_CO_SO_DU_LIEU.md:L517 `.
- `TBL-STU-037` — `attempt_files` — `03_THIET_KE_CO_SO_DU_LIEU.md:L524 `.
- `TBL-STU-038` — `assessment_reviews` — `03_THIET_KE_CO_SO_DU_LIEU.md:L531 `.
- `TBL-STU-039` — `assessment_review_scores` — `03_THIET_KE_CO_SO_DU_LIEU.md:L538 `.
- `TBL-STU-059` — `file_upload_sessions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L685 `.

**Screen và acceptance**

- Screens: `SCR-STU-017`, `SCR-STU-018`, `SCR-OPS-012`, `SCR-OPS-013`.
- Acceptance: `TC-STU-004`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-STU-010` — `01_TONG_QUAN_DU_AN.md:L360` — Assessment V1 chỉ có `QUIZ`, `TEXT`, `LINK`, `FILE`. Quiz auto-grade; ba loại còn lại manual review theo rubric và mỗi lần resubmit tạo attempt mới..
- `BR-STU-011` — `01_TONG_QUAN_DU_AN.md:L361` — File assessment phải ở trạng thái `CLEAN` trước khi submit/download/review; infected hoặc scan failed không tạo attempt. Object lưu private, URL tải có hạn và được cấp sau authorization..
- `BR-STU-012` — `01_TONG_QUAN_DU_AN.md:L362` — Link assessment chỉ chấp nhận HTTPS tối đa 2.048 ký tự; backend không fetch, resolve preview hoặc follow redirect để tránh SSRF. Text tối đa 20.000 ký tự..
- `BR-STU-013` — `01_TONG_QUAN_DU_AN.md:L363` — Mỗi assessment placement thuộc đúng một scope: path version, course version, chapter hoặc lesson. Quan hệ không hợp lệ bị chặn ở application và database constraint..
- `BR-STU-015` — `01_TONG_QUAN_DU_AN.md:L365` — Điều chỉnh progress/review đã ghi chỉ qua nghiệp vụ correction append-only có actor/reason; không xóa hoặc update fact gốc và không có learner API để recalculate/reset..
- `PERM-STU-006` — `01_TONG_QUAN_DU_AN.md:L155` — `study.assessments.review` — Assessment Reviewer, Study Admin.
- `NFR-OPS-008` — `01_TONG_QUAN_DU_AN.md:L655` — File scan p95 ≤ 2 phút cho file trong giới hạn V1 khi scanner khỏe; pending/failed luôn fail closed, có trạng thái và retry rõ ràng..

## 5. Chi tiết từng API

### API-STU-030 — `POST /api/v1/file-upload-sessions`

- **Nguồn contract:** `04_DAC_TA_API.md:L160`.
- **Actor/quyền:** Authenticated Study user.
- **Input/validation → output:** Purpose, filename, expected MIME/size <=25MiB, SHA-256 → upload ID + signed PUT.
- **Xử lý và dữ liệu:** Validate allowlist PDF/PNG/JPEG/TXT/MD/CSV/ZIP; generate private quarantine key; W session/asset CREATED.
- **Vận hành:** Idempotency required; signed URL 15m; 20/giờ.
- **Lỗi đặc thù:** `FILE_TYPE_NOT_ALLOWED`, `FILE_TOO_LARGE`, `UPLOAD_QUOTA_EXCEEDED`.
- **Màn hình/consumer:** `SCR-STU-017`, admin editors.
- **Capability/use case:** `CAP-STU-004`, `UC-STU-004`.

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

### API-STU-031 — `POST /api/v1/file-upload-sessions/{id}/finalize`

- **Nguồn contract:** `04_DAC_TA_API.md:L161`.
- **Actor/quyền:** Upload owner.
- **Input/validation → output:** Actual checksum/size →`SCANNING` asset.
- **Xử lý và dữ liệu:** Verify object HEAD key/size/checksum/MIME sniff; TX mark uploaded, outbox scan job; never mark clean synchronously.
- **Vận hành:** Idempotency; event`study.file.scan_requested`.
- **Lỗi đặc thù:** `UPLOAD_INCOMPLETE`, `CHECKSUM_MISMATCH`, `MIME_SPOOFED`, `UPLOAD_SESSION_EXPIRED`.
- **Màn hình/consumer:** `SCR-STU-017`.
- **Capability/use case:** `CAP-STU-004`, `UC-STU-004`.

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

### API-STU-032 — `GET /api/v1/file-assets/{fileId}/status`

- **Nguồn contract:** `04_DAC_TA_API.md:L162`.
- **Actor/quyền:** Owner/authorized reviewer.
- **Input/validation → output:** → state/result-safe message.
- **Xử lý và dữ liệu:** Predicate owner or domain attachment permission; R latest scan result.
- **Vận hành:** Poll max 1/2s; private.
- **Lỗi đặc thù:** `FILE_NOT_FOUND`.
- **Màn hình/consumer:** `SCR-STU-017`, `SCR-OPS-012`.
- **Capability/use case:** `CAP-STU-004`, `UC-STU-004`.

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

### API-STU-033 — `POST /api/v1/file-assets/{fileId}/download-urls`

- **Nguồn contract:** `04_DAC_TA_API.md:L163`.
- **Actor/quyền:** Owner or explicitly authorized reviewer.
- **Input/validation → output:** Desired disposition → signed GET <=5m.
- **Xử lý và dữ liệu:** Require state CLEAN and authorized attachment; audit access; generate storage URL after DB check.
- **Vận hành:** Idempotency optional; 30/phút.
- **Lỗi đặc thù:** `FILE_NOT_CLEAN`, `FILE_ACCESS_DENIED`, `FILE_EXPIRED`.
- **Màn hình/consumer:** `SCR-STU-018`, `SCR-OPS-012`.
- **Capability/use case:** `CAP-STU-004`, `UC-STU-004`.

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
