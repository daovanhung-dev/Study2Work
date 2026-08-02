# PLAN 57 — Internal — AI callback, progress rebuild và search removal

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-57` |
| API trong phạm vi | `API-INT-008`, `API-INT-009`, `API-INT-010` |
| Số API | 3 |
| Read-only / Mutation | 0 / 3 |
| Khối lượng lõi | 24 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho provider callback và hai operational jobs.

**Luồng nghiệp vụ trọng tâm:** AI callback verifies provider signature/idempotency and transitions job; progress rebuild recomputes snapshots from facts; search removal confirms candidate deindex while DB predicate already blocks.

**Điểm cần khóa:** Worker retry/DLQ, source-of-truth DB, no HTTP inside TX, stale callback handling.

**Dependency:** Plans 11,23,37,49–51.

## 3. Phạm vi

**In-scope**

- `API-INT-008` — `POST work /internal/v1/ai-provider-callbacks/{provider}`.
- `API-INT-009` — `POST study /internal/v1/progress-rebuild-jobs`.
- `API-INT-010` — `POST work /internal/v1/search-index-removals`.

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

- `01_TONG_QUAN_DU_AN.md:L762` — `CAP-STU-003` / `UC-STU-003`; rules ``BR-STU-008–009`, `BR-STU-015`, `PERM-STU-010`, `NFR-OPS-003``; diagrams ``AC-STU-002`, `SEQ-STU-002``; data ``CLS-STU-002`; `TBL-STU-027–032`, `TBL-STU-049``; screens ``SCR-STU-010`, `SCR-STU-015–016`, `SCR-STU-019`, `SCR-OPS-015``; test ``TC-STU-003``.
- `01_TONG_QUAN_DU_AN.md:L769` — `CAP-WRK-002` / `UC-WRK-002`; rules ``BR-WRK-001–003`, `BR-WRK-012`, `PERM-WRK-020–021`, `NFR-OPS-007``; diagrams ``AC-WRK-001`, `SEQ-WRK-001``; data ``CLS-WRK-001`; `TBL-WRK-005`, `TBL-WRK-037–040``; screens ``SCR-WRK-012`, `SCR-WRK-016`, `SCR-WRK-036–038``; test ``TC-WRK-002``.
- `01_TONG_QUAN_DU_AN.md:L789` — `CAP-OPS-003` / `UC-OPS-003`; rules ``BR-INT-009`, `BR-OPS-003`, `BR-OPS-008`, `NFR-OPS-001–012``; diagrams ``AC-OPS-001`, `SEQ-OPS-001``; data ``CLS-INT-001`; `TBL-IAM-018–020`, `TBL-STU-052–055`, `TBL-WRK-063–064`, `TBL-WRK-070``; screens ``SCR-OPS-021`; worker/alert/runbook là `SYSTEM``; test ``TC-OPS-003``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-STU-002` — `02_BIEU_DO_HE_THONG.md:L416` — AC-STU-002 — Học bài, assessment, file scan và completion.
- `SEQ-STU-002` — `02_BIEU_DO_HE_THONG.md:L1881` — SEQ-STU-002 — Lesson progress và quiz auto-grade.
- `AC-WRK-001` — `02_BIEU_DO_HE_THONG.md:L548` — AC-WRK-001 — Candidate privacy, search, invitation và opt-out.
- `SEQ-WRK-001` — `02_BIEU_DO_HE_THONG.md:L2080` — SEQ-WRK-001 — Candidate opt-in/search, sponsored label và opt-out SLA.
- `AC-OPS-001` — `02_BIEU_DO_HE_THONG.md:L802` — AC-OPS-001 — Moderation, deletion, legal hold và recovery.
- `SEQ-OPS-001` — `02_BIEU_DO_HE_THONG.md:L2554` — SEQ-OPS-001 — Moderation action, deletion fan-out và DLQ replay.
- `CLS-STU-002` — `02_BIEU_DO_HE_THONG.md:L1059` — CLS-STU-002 — Enrollment, progress, assessment, file và evidence.
- `CLS-WRK-001` — `02_BIEU_DO_HE_THONG.md:L1266` — CLS-WRK-001 — Candidate, tenant, job, application và ATS snapshots.
- `CLS-INT-001` — `02_BIEU_DO_HE_THONG.md:L1654` — CLS-INT-001 — Liên kết logic giữa ba database.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-STU-027` — `course_enrollments` — `03_THIET_KE_CO_SO_DU_LIEU.md:L450 `.
- `TBL-STU-028` — `block_progress_facts` — `03_THIET_KE_CO_SO_DU_LIEU.md:L457 `.
- `TBL-STU-029` — `lesson_progress_facts` — `03_THIET_KE_CO_SO_DU_LIEU.md:L464 `.
- `TBL-STU-030` — `progress_snapshots` — `03_THIET_KE_CO_SO_DU_LIEU.md:L471 `.
- `TBL-STU-031` — `course_completions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L478 `.
- `TBL-STU-032` — `path_completions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L485 `.
- `TBL-STU-049` — `admin_adjustments` — `03_THIET_KE_CO_SO_DU_LIEU.md:L616 `.
- `TBL-WRK-005` — `candidate_search_preferences` — `03_THIET_KE_CO_SO_DU_LIEU.md:L733 `.
- `TBL-WRK-037` — `candidate_search_documents` — `03_THIET_KE_CO_SO_DU_LIEU.md:L964 `.
- `TBL-WRK-038` — `candidate_invitations` — `03_THIET_KE_CO_SO_DU_LIEU.md:L971 `.
- `TBL-WRK-039` — `talent_lists` — `03_THIET_KE_CO_SO_DU_LIEU.md:L978 `.
- `TBL-WRK-040` — `talent_list_items` — `03_THIET_KE_CO_SO_DU_LIEU.md:L985 `.
- `TBL-IAM-018` — `outbox_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L234 `.
- `TBL-IAM-019` — `consumer_inbox` — `03_THIET_KE_CO_SO_DU_LIEU.md:L242 `.
- `TBL-IAM-020` — `outbox_delivery_attempts` — `03_THIET_KE_CO_SO_DU_LIEU.md:L249 `.
- `TBL-STU-052` — `outbox_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L638 `.
- `TBL-STU-053` — `consumer_inbox` — `03_THIET_KE_CO_SO_DU_LIEU.md:L645 `.
- `TBL-STU-054` — `report_snapshots` — `03_THIET_KE_CO_SO_DU_LIEU.md:L652 `.
- `TBL-STU-055` — `outbox_delivery_attempts` — `03_THIET_KE_CO_SO_DU_LIEU.md:L659 `.
- `TBL-WRK-063` — `outbox_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1314 `.
- `TBL-WRK-064` — `consumer_inbox` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1321 `.
- `TBL-WRK-070` — `outbox_delivery_attempts` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1363 `.

**Screen và acceptance**

- Screens: `SCR-STU-010`, `SCR-STU-015`, `SCR-STU-016`, `SCR-STU-019`, `SCR-OPS-015`, `SCR-WRK-012`, `SCR-WRK-016`, `SCR-WRK-036`, `SCR-WRK-037`, `SCR-WRK-038`, `SCR-OPS-021`.
- Acceptance: `TC-STU-003`, `TC-WRK-002`, `TC-OPS-003`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-STU-008` — `01_TONG_QUAN_DU_AN.md:L358` — Completion chỉ tái sử dụng khi đúng cùng `courseVersionId`; course có stable ID giống nhau nhưng version khác không được tự kế thừa completion hoặc progress..
- `BR-STU-009` — `01_TONG_QUAN_DU_AN.md:L359` — Nguồn sự thật tiến độ là completion fact của content block, lesson và assessment. Course/path percent chỉ là snapshot server tính, có thể rebuild và client không được ghi trực tiếp..
- `BR-STU-015` — `01_TONG_QUAN_DU_AN.md:L365` — Điều chỉnh progress/review đã ghi chỉ qua nghiệp vụ correction append-only có actor/reason; không xóa hoặc update fact gốc và không có learner API để recalculate/reset..
- `PERM-STU-010` — `01_TONG_QUAN_DU_AN.md:L158` — `study.progress.adjust` — Study Admin được ủy quyền.
- `NFR-OPS-003` — `01_TONG_QUAN_DU_AN.md:L650` — p95 server latency: read đồng bộ ≤ 800 ms, mutation đồng bộ ≤ 1,5 giây; không tính phần việc đã công bố async. Query report lớn bắt buộc async/export..
- `BR-WRK-001` — `01_TONG_QUAN_DU_AN.md:L373` — Career profile mặc định `PRIVATE`. Chỉ candidate tự bật `SEARCHABLE`; không tenant, recruiter hoặc admin thông thường nào được bật thay..
- `BR-WRK-002` — `01_TONG_QUAN_DU_AN.md:L374` — Candidate search chỉ chứa field public đã chọn, skill/kinh nghiệm tổng quát và availability; không trả email, phone, CV file, địa chỉ chi tiết, application, Study evidence hoặc thuộc tính nhạy cảm..
- `BR-WRK-003` — `01_TONG_QUAN_DU_AN.md:L375` — Opt-out phải làm hồ sơ biến mất khỏi kết quả và cache trong tối đa 5 phút. Snapshot/audit hợp pháp đã có trong application không bị xóa bởi opt-out tìm kiếm..
- `BR-WRK-012` — `01_TONG_QUAN_DU_AN.md:L384` — Invitation chỉ là lời mời có hạn; không tạo application, không cấp contact và không mở chat. Candidate phải chủ động submit application..
- `PERM-WRK-020` — `01_TONG_QUAN_DU_AN.md:L171` — `work.candidates.search` — Enterprise Owner/Admin, Recruiter có entitlement.
- `PERM-WRK-021` — `01_TONG_QUAN_DU_AN.md:L172` — `work.candidates.invite` — Enterprise Owner/Admin, Recruiter có entitlement.
- `NFR-OPS-007` — `01_TONG_QUAN_DU_AN.md:L654` — Candidate opt-out được kiểm end-to-end và đáp ứng hard limit 5 phút gồm DB projection, index, cache và active search response..
- `BR-INT-009` — `01_TONG_QUAN_DU_AN.md:L404` — Event duplicate/stale bị bỏ qua theo aggregate version; event gap vào retry/catch-up. Poison event vào DLQ và không được đánh dấu thành công giả..
- `BR-OPS-003` — `01_TONG_QUAN_DU_AN.md:L450` — Notification và side effect ngoài transaction được tạo qua outbox với dedupe key. Retry exponential có giới hạn; hết retry vào DLQ và cảnh báo..
- `BR-OPS-008` — `01_TONG_QUAN_DU_AN.md:L455` — Restore backup phải áp lại deletion/revocation ledger trước khi mở traffic để dữ liệu đã xóa/thu hồi không sống lại..
- `NFR-OPS-001` — `01_TONG_QUAN_DU_AN.md:L648` — Hệ thống pilot hỗ trợ 5.000 account, 500 DAU và 50 RPS đỉnh trong 15 phút mà không vượt 80% connection pool/CPU kéo dài hoặc mất request đã acknowledge..
- `NFR-OPS-002` — `01_TONG_QUAN_DU_AN.md:L649` — Availability theo tháng của Identity, Study core và Work core đạt ít nhất 99,0%; dependency ngoài được đo riêng nhưng hệ thống phải thể hiện degraded state an toàn..
- `NFR-OPS-004` — `01_TONG_QUAN_DU_AN.md:L651` — Chat server acknowledgement sau khi persist p95 ≤ 2 giây; reconnect/history không mất hoặc nhân đôi message theo client key..
- `NFR-OPS-005` — `01_TONG_QUAN_DU_AN.md:L652` — RPO toàn bộ PostgreSQL ≤ 15 phút; RTO cho Identity/Study/Work core ≤ 4 giờ. Restore drill thực hiện ít nhất mỗi quý trong pilot..
- `NFR-OPS-006` — `01_TONG_QUAN_DU_AN.md:L653` — Outbox/event projection p95 ≤ 60 giây khi bình thường; evidence export p95 ≤ 2 phút. Backlog, oldest age, retry và DLQ có alert..
- `NFR-OPS-008` — `01_TONG_QUAN_DU_AN.md:L655` — File scan p95 ≤ 2 phút cho file trong giới hạn V1 khi scanner khỏe; pending/failed luôn fail closed, có trạng thái và retry rõ ràng..
- `NFR-OPS-009` — `01_TONG_QUAN_DU_AN.md:L656` — Mọi request có trace ID; mutation quan trọng liên kết audit/outbox/provider transaction. Log JSON có severity, service, environment và không chứa secret/PII payload..
- `NFR-OPS-010` — `01_TONG_QUAN_DU_AN.md:L657` — Web đạt WCAG 2.2 AA cho luồng chính: keyboard, focus, label, contrast, error announcement và reduced motion; responsive từ 360 px, hỗ trợ hai phiên bản major mới nhất của Chrome, Edge, Firefox, Safari..
- `NFR-OPS-011` — `01_TONG_QUAN_DU_AN.md:L658` — API/event/database migration và tài liệu phải pass contract/trace validator; không phát hành khi có reference mất, duplicate method+path hoặc enum/state mâu thuẫn..
- `NFR-OPS-012` — `01_TONG_QUAN_DU_AN.md:L659` — Backup mã hóa, kiểm restore; secret quay vòng; high/critical security finding, cross-tenant leak hoặc payment integrity failure là release blocker..

## 5. Chi tiết từng API

### API-INT-008 — `POST work /internal/v1/ai-provider-callbacks/{provider}`

- **Nguồn contract:** `04_DAC_TA_API.md:L446`.
- **Actor/quyền:** Configured provider only if callback adapter enabled.
- **Input/validation → output:** Provider job/result signature → accepted.
- **Xử lý và dữ liệu:** Verify signature/job binding; append callback; schema/policy validation before AI result; Ollama default uses worker polling so endpoint disabled.
- **Vận hành:** Verify signature/job binding; append callback; schema/policy validation before AI result; Ollama default uses worker polling so endpoint disabled.
- **Lỗi đặc thù:** `CALLBACK_DISABLED`, `SIGNATURE_INVALID`.
- **Màn hình/consumer:** SYSTEM.
- **Capability/use case:** `CAP-OPS-003`, `UC-OPS-003`.

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

### API-INT-009 — `POST study /internal/v1/progress-rebuild-jobs`

- **Nguồn contract:** `04_DAC_TA_API.md:L447`.
- **Actor/quyền:** Study admin worker/service only.
- **Input/validation → output:** Learner/target/reason/source audit ID → job.
- **Xử lý và dữ liệu:** No learner access; dedupe job; rebuild snapshots from facts, append diff/audit; never rewrite facts.
- **Vận hành:** No learner access; dedupe job; rebuild snapshots from facts, append diff/audit; never rewrite facts.
- **Lỗi đặc thù:** `REBUILD_SCOPE_INVALID`.
- **Màn hình/consumer:** SYSTEM.
- **Capability/use case:** `CAP-STU-003`, `UC-STU-003`, `CAP-OPS-003`, `UC-OPS-003`.

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

### API-INT-010 — `POST work /internal/v1/search-index-removals`

- **Nguồn contract:** `04_DAC_TA_API.md:L448`.
- **Actor/quyền:** Work privacy worker.
- **Input/validation → output:** Candidate ID/consent event ID/deadline → result.
- **Xử lý và dữ liệu:** DB consent checked; delete search document; dedupe; alert if >5m.
- **Vận hành:** DB consent checked; delete search document; dedupe; alert if >5m.
- **Lỗi đặc thù:** `SEARCH_BACKEND_UNAVAILABLE` retry/DLQ.
- **Màn hình/consumer:** SYSTEM.
- **Capability/use case:** `CAP-WRK-002`, `UC-WRK-002`, `CAP-OPS-003`, `UC-OPS-003`.

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
