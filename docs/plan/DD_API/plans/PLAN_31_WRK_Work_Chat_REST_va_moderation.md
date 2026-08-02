# PLAN 31 — Work — Chat REST và moderation

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-31` |
| API trong phạm vi | `API-WRK-031`, `API-WRK-032`, `API-WRK-033`, `API-WRK-034` |
| Số API | 4 |
| Read-only / Mutation | 1 / 3 |
| Khối lượng lõi | 32 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho message history, send, read receipt và tombstone delete.

**Luồng nghiệp vụ trọng tâm:** REST là source of truth; send khóa conversation, kiểm participant/assignment/application writable, dedupe clientMessageId, insert+outbox rồi publish; read cursor monotonic; delete giữ sequence/hash/audit.

**Điểm cần khóa:** Commit-before-publish, reconnect reconciliation, 15-minute delete window, no attachment V1.

**Dependency:** Plan 59 realtime.

## 3. Phạm vi

**In-scope**

- `API-WRK-031` — `GET /api/v1/applications/{id}/conversation/messages`.
- `API-WRK-032` — `POST /api/v1/applications/{id}/conversation/messages`.
- `API-WRK-033` — `POST /api/v1/applications/{id}/conversation/read-receipts`.
- `API-WRK-034` — `DELETE /api/v1/applications/{id}/conversation/messages/{messageId}`.

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

- `01_TONG_QUAN_DU_AN.md:L775` — `CAP-WRK-008` / `UC-WRK-008`; rules ``BR-WRK-013–014`, `BR-OPS-003`, `NFR-OPS-004``; diagrams ``AC-WRK-003`, `SEQ-WRK-005``; data ``CLS-WRK-002`; `TBL-WRK-053–056``; screens ``SCR-WRK-021`, `SCR-WRK-042`, `SCR-OPS-026``; test ``TC-WRK-008``.
- `01_TONG_QUAN_DU_AN.md:L777` — `CAP-WRK-010` / `UC-WRK-010`; rules ``BR-WRK-018`, `PERM-OPS-001–003`, `PERM-WRK-012`, `BR-OPS-001–002``; diagrams ``AC-OPS-001`, `SEQ-OPS-001``; data ``CLS-WRK-002`; `TBL-WRK-035–036`, `TBL-WRK-060–061``; screens ``SCR-OPS-009–011`, `SCR-OPS-017–018`, `SCR-OPS-021`, `SCR-OPS-024–026``; test ``TC-WRK-010``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-WRK-003` — `02_BIEU_DO_HE_THONG.md:L622` — AC-WRK-003 — Interview và chat theo application.
- `SEQ-WRK-005` — `02_BIEU_DO_HE_THONG.md:L2315` — SEQ-WRK-005 — Chat commit-before-publish, duplicate send và reconnect.
- `AC-OPS-001` — `02_BIEU_DO_HE_THONG.md:L802` — AC-OPS-001 — Moderation, deletion, legal hold và recovery.
- `SEQ-OPS-001` — `02_BIEU_DO_HE_THONG.md:L2554` — SEQ-OPS-001 — Moderation action, deletion fan-out và DLQ replay.
- `CLS-WRK-002` — `02_BIEU_DO_HE_THONG.md:L1384` — CLS-WRK-002 — Interview, chat, university và moderation.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-WRK-053` — `conversations` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1083 `.
- `TBL-WRK-054` — `messages` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1090 `.
- `TBL-WRK-055` — `conversation_read_cursors` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1097 `.
- `TBL-WRK-056` — `websocket_connection_leases` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1104 `.
- `TBL-WRK-035` — `job_review_decisions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L950 `.
- `TBL-WRK-036` — `job_status_history` — `03_THIET_KE_CO_SO_DU_LIEU.md:L957 `.
- `TBL-WRK-060` — `moderation_reports` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1293 `.
- `TBL-WRK-061` — `audit_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1300 `.

**Screen và acceptance**

- Screens: `SCR-WRK-021`, `SCR-WRK-042`, `SCR-OPS-026`, `SCR-OPS-009`, `SCR-OPS-010`, `SCR-OPS-011`, `SCR-OPS-017`, `SCR-OPS-018`, `SCR-OPS-021`, `SCR-OPS-024`, `SCR-OPS-025`.
- Acceptance: `TC-WRK-008`, `TC-WRK-010`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-WRK-013` — `01_TONG_QUAN_DU_AN.md:L385` — Mỗi application có tối đa một conversation 1–1. Chỉ candidate và recruiter active được phân công tham gia; application terminal chuyển conversation sang `READ_ONLY`..
- `BR-WRK-014` — `01_TONG_QUAN_DU_AN.md:L386` — REST history là nguồn sự thật của chat; WebSocket chỉ phân phối event. Client reconnect bằng cursor, message send idempotent và thứ tự chuẩn theo server sequence..
- `BR-OPS-003` — `01_TONG_QUAN_DU_AN.md:L450` — Notification và side effect ngoài transaction được tạo qua outbox với dedupe key. Retry exponential có giới hạn; hết retry vào DLQ và cảnh báo..
- `NFR-OPS-004` — `01_TONG_QUAN_DU_AN.md:L651` — Chat server acknowledgement sau khi persist p95 ≤ 2 giây; reconnect/history không mất hoặc nhân đôi message theo client key..
- `BR-WRK-018` — `01_TONG_QUAN_DU_AN.md:L390` — Moderation takedown giữ revision, application và audit; chặn discovery/apply mới nhưng không xóa lịch sử tuyển dụng hợp pháp..
- `PERM-OPS-001` — `01_TONG_QUAN_DU_AN.md:L199` — `operations.verification.review` — Platform Moderator được ủy quyền.
- `PERM-OPS-002` — `01_TONG_QUAN_DU_AN.md:L200` — `operations.job_review` — Platform Moderator.
- `PERM-OPS-003` — `01_TONG_QUAN_DU_AN.md:L201` — `operations.trusted_publisher.manage` — Platform Admin được ủy quyền.
- `PERM-WRK-012` — `01_TONG_QUAN_DU_AN.md:L169` — `work.jobs.submit_review` — Enterprise Owner/Admin, Recruiter được ủy quyền.
- `BR-OPS-001` — `01_TONG_QUAN_DU_AN.md:L448` — Audit/security/payment webhook/ledger/application history/evidence snapshot/AI review/outbox là append-only; không cascade delete làm mất lịch sử..
- `BR-OPS-002` — `01_TONG_QUAN_DU_AN.md:L449` — Audit chứa actor, effective role/tenant, action, resource, before/after đã redact, reason, IP/device tối thiểu, trace ID và thời điểm UTC; không chứa secret/token/raw password..

## 5. Chi tiết từng API

### API-WRK-031 — `GET /api/v1/applications/{id}/conversation/messages`

- **Nguồn contract:** `04_DAC_TA_API.md:L269`.
- **Actor/quyền:** Candidate owner or assigned recruiter.
- **Input/validation → output:** Cursor`before`, limit → ordered history and tombstones.
- **Xử lý và dữ liệu:** Authorize participant + conversation application; query`(conversation_id,sequence_no desc)`; REST is source of truth.
- **Vận hành:** Private no-store; cursor.
- **Lỗi đặc thù:** `CONVERSATION_NOT_AVAILABLE`.
- **Màn hình/consumer:** `SCR-WRK-021`, `SCR-WRK-042`.
- **Capability/use case:** `CAP-WRK-008`, `UC-WRK-008`.

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

### API-WRK-032 — `POST /api/v1/applications/{id}/conversation/messages`

- **Nguồn contract:** `04_DAC_TA_API.md:L270`.
- **Actor/quyền:** Candidate owner or currently assigned recruiter.
- **Input/validation → output:** Client message ID, plain text 1–5000 ký tự, replyTo optional → accepted message/sequence.
- **Xử lý và dữ liệu:** TX L conversation; verify application nonterminal/conversation writable/assignment; sanitize/control-character check; dedupe client ID; insert TEXT message + outbox; WebSocket publish after commit. V1 không hỗ trợ file/HTML trong chat; SYSTEM message chỉ worker được tạo.
- **Vận hành:** Idempotency required; ack SLO <=2s; audit moderation metadata; 30/min.
- **Lỗi đặc thù:** `CONVERSATION_READ_ONLY`, `RECRUITER_NOT_ASSIGNED`, `MESSAGE_INVALID`, `MESSAGE_DUPLICATE`.
- **Màn hình/consumer:** `SCR-WRK-021`, `SCR-WRK-042`.
- **Capability/use case:** `CAP-WRK-008`, `UC-WRK-008`.

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

### API-WRK-033 — `POST /api/v1/applications/{id}/conversation/read-receipts`

- **Nguồn contract:** `04_DAC_TA_API.md:L271`.
- **Actor/quyền:** Participant.
- **Input/validation → output:** Last sequence read → receipt.
- **Xử lý và dữ liệu:** Upsert monotonic max per participant; reject sequence beyond conversation.
- **Vận hành:** Idempotent; WebSocket receipt event.
- **Lỗi đặc thù:** `SEQUENCE_INVALID`.
- **Màn hình/consumer:** `SCR-WRK-021`, `SCR-WRK-042`.
- **Capability/use case:** `CAP-WRK-008`, `UC-WRK-008`.

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

### API-WRK-034 — `DELETE /api/v1/applications/{id}/conversation/messages/{messageId}`

- **Nguồn contract:** `04_DAC_TA_API.md:L272`.
- **Actor/quyền:** Message author within 15m or moderator.
- **Input/validation → output:** Reason → tombstone.
- **Xử lý và dữ liệu:** TX preserve immutable event/content hash and sequence, hide text body from normal reads; moderator requires reason.
- **Vận hành:** Idempotent; moderation audit/event.
- **Lỗi đặc thù:** `MESSAGE_DELETE_WINDOW_EXPIRED`, `MESSAGE_NOT_OWNED`.
- **Màn hình/consumer:** `SCR-WRK-021`, `SCR-OPS-026`.
- **Capability/use case:** `CAP-WRK-008`, `UC-WRK-008`, `CAP-WRK-010`, `UC-WRK-010`.

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
