# PLAN 54 — Operations — Audit export, break-glass và operational report

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-54` |
| API trong phạm vi | `API-OPS-007`, `API-OPS-008`, `API-OPS-009`, `API-OPS-010` |
| Số API | 4 |
| Read-only / Mutation | 2 / 2 |
| Khối lượng lõi | 32 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho audit search/export, break-glass session và vận hành report.

**Luồng nghiệp vụ trọng tâm:** Audit query redacted with cursor/date bounds; export async encrypted artifact; break-glass requires reason/MFA/expiry/alert; reports read snapshots/backlog/SLO.

**Điểm cần khóa:** Audit must not contain secrets/raw CV/chat/evidence, step-up 15m, immutable logs.

**Dependency:** All services; Plan 56–58 events/jobs.

## 3. Phạm vi

**In-scope**

- `API-OPS-007` — `GET /api/v1/admin/audit-logs`.
- `API-OPS-008` — `POST /api/v1/admin/audit-exports`.
- `API-OPS-009` — `POST /api/v1/admin/break-glass-sessions`.
- `API-OPS-010` — `GET /api/v1/admin/operational-reports`.

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

- `01_TONG_QUAN_DU_AN.md:L767` — `CAP-STU-008` / `UC-STU-008`; rules ``BR-STU-015`, `PERM-STU-009–014`, `BR-OPS-001–003``; diagrams ``AC-OPS-001`, `SEQ-OPS-001``; data ``CLS-STU-001–002`; `TBL-STU-003–006`, `TBL-STU-049–050`, `TBL-STU-054``; screens ``SCR-OPS-012–016`, `SCR-OPS-021`, `SCR-OPS-024``; test ``TC-STU-008``.
- `01_TONG_QUAN_DU_AN.md:L777` — `CAP-WRK-010` / `UC-WRK-010`; rules ``BR-WRK-018`, `PERM-OPS-001–003`, `PERM-WRK-012`, `BR-OPS-001–002``; diagrams ``AC-OPS-001`, `SEQ-OPS-001``; data ``CLS-WRK-002`; `TBL-WRK-035–036`, `TBL-WRK-060–061``; screens ``SCR-OPS-009–011`, `SCR-OPS-017–018`, `SCR-OPS-021`, `SCR-OPS-024–026``; test ``TC-WRK-010``.
- `01_TONG_QUAN_DU_AN.md:L787` — `CAP-OPS-001` / `UC-OPS-001`; rules ``BR-WRK-018`, `BR-OPS-001–002`, `PERM-OPS-001–003`, `PERM-OPS-005``; diagrams ``AC-OPS-001`, `SEQ-OPS-001``; data ``CLS-WRK-002`; `TBL-WRK-015`, `TBL-WRK-020`, `TBL-WRK-035`, `TBL-WRK-060–061``; screens ``SCR-OPS-009–011`, `SCR-OPS-017–018`, `SCR-OPS-024–025``; test ``TC-OPS-001``.
- `01_TONG_QUAN_DU_AN.md:L789` — `CAP-OPS-003` / `UC-OPS-003`; rules ``BR-INT-009`, `BR-OPS-003`, `BR-OPS-008`, `NFR-OPS-001–012``; diagrams ``AC-OPS-001`, `SEQ-OPS-001``; data ``CLS-INT-001`; `TBL-IAM-018–020`, `TBL-STU-052–055`, `TBL-WRK-063–064`, `TBL-WRK-070``; screens ``SCR-OPS-021`; worker/alert/runbook là `SYSTEM``; test ``TC-OPS-003``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-OPS-001` — `02_BIEU_DO_HE_THONG.md:L802` — AC-OPS-001 — Moderation, deletion, legal hold và recovery.
- `SEQ-OPS-001` — `02_BIEU_DO_HE_THONG.md:L2554` — SEQ-OPS-001 — Moderation action, deletion fan-out và DLQ replay.
- `CLS-STU-001` — `02_BIEU_DO_HE_THONG.md:L931` — CLS-STU-001 — Study profile, RBAC và curriculum versioning.
- `CLS-STU-002` — `02_BIEU_DO_HE_THONG.md:L1059` — CLS-STU-002 — Enrollment, progress, assessment, file và evidence.
- `CLS-WRK-002` — `02_BIEU_DO_HE_THONG.md:L1384` — CLS-WRK-002 — Interview, chat, university và moderation.
- `CLS-INT-001` — `02_BIEU_DO_HE_THONG.md:L1654` — CLS-INT-001 — Liên kết logic giữa ba database.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-STU-003` — `service_roles` — `03_THIET_KE_CO_SO_DU_LIEU.md:L274 `.
- `TBL-STU-004` — `service_permissions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L281 `.
- `TBL-STU-005` — `service_role_permissions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L288 `.
- `TBL-STU-006` — `service_role_assignments` — `03_THIET_KE_CO_SO_DU_LIEU.md:L295 `.
- `TBL-STU-049` — `admin_adjustments` — `03_THIET_KE_CO_SO_DU_LIEU.md:L616 `.
- `TBL-STU-050` — `audit_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L623 `.
- `TBL-STU-054` — `report_snapshots` — `03_THIET_KE_CO_SO_DU_LIEU.md:L652 `.
- `TBL-WRK-035` — `job_review_decisions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L950 `.
- `TBL-WRK-036` — `job_status_history` — `03_THIET_KE_CO_SO_DU_LIEU.md:L957 `.
- `TBL-WRK-060` — `moderation_reports` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1293 `.
- `TBL-WRK-061` — `audit_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1300 `.
- `TBL-WRK-015` — `enterprise_verification_cases` — `03_THIET_KE_CO_SO_DU_LIEU.md:L805 `.
- `TBL-WRK-020` — `university_verification_cases` — `03_THIET_KE_CO_SO_DU_LIEU.md:L843 `.
- `TBL-IAM-018` — `outbox_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L234 `.
- `TBL-IAM-019` — `consumer_inbox` — `03_THIET_KE_CO_SO_DU_LIEU.md:L242 `.
- `TBL-IAM-020` — `outbox_delivery_attempts` — `03_THIET_KE_CO_SO_DU_LIEU.md:L249 `.
- `TBL-STU-052` — `outbox_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L638 `.
- `TBL-STU-053` — `consumer_inbox` — `03_THIET_KE_CO_SO_DU_LIEU.md:L645 `.
- `TBL-STU-055` — `outbox_delivery_attempts` — `03_THIET_KE_CO_SO_DU_LIEU.md:L659 `.
- `TBL-WRK-063` — `outbox_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1314 `.
- `TBL-WRK-064` — `consumer_inbox` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1321 `.
- `TBL-WRK-070` — `outbox_delivery_attempts` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1363 `.

**Screen và acceptance**

- Screens: `SCR-OPS-012`, `SCR-OPS-013`, `SCR-OPS-014`, `SCR-OPS-015`, `SCR-OPS-016`, `SCR-OPS-021`, `SCR-OPS-024`, `SCR-OPS-009`, `SCR-OPS-010`, `SCR-OPS-011`, `SCR-OPS-017`, `SCR-OPS-018`, `SCR-OPS-025`, `SCR-OPS-026`.
- Acceptance: `TC-STU-008`, `TC-WRK-010`, `TC-OPS-001`, `TC-OPS-003`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-STU-015` — `01_TONG_QUAN_DU_AN.md:L365` — Điều chỉnh progress/review đã ghi chỉ qua nghiệp vụ correction append-only có actor/reason; không xóa hoặc update fact gốc và không có learner API để recalculate/reset..
- `PERM-STU-009` — `01_TONG_QUAN_DU_AN.md:L157` — `study.primary_path.override` — Learner Support được ủy quyền, Study Admin.
- `PERM-STU-010` — `01_TONG_QUAN_DU_AN.md:L158` — `study.progress.adjust` — Study Admin được ủy quyền.
- `PERM-STU-011` — `01_TONG_QUAN_DU_AN.md:L159` — `study.roles.manage` — Study Admin.
- `PERM-STU-012` — `01_TONG_QUAN_DU_AN.md:L160` — `study.community.moderate` — Community Moderator, Study Admin.
- `PERM-STU-013` — `01_TONG_QUAN_DU_AN.md:L161` — `study.reports.read` — Study Admin.
- `PERM-STU-014` — `01_TONG_QUAN_DU_AN.md:L162` — `study.audit.read` — Study Admin, Security Auditor theo scope.
- `BR-OPS-001` — `01_TONG_QUAN_DU_AN.md:L448` — Audit/security/payment webhook/ledger/application history/evidence snapshot/AI review/outbox là append-only; không cascade delete làm mất lịch sử..
- `BR-OPS-002` — `01_TONG_QUAN_DU_AN.md:L449` — Audit chứa actor, effective role/tenant, action, resource, before/after đã redact, reason, IP/device tối thiểu, trace ID và thời điểm UTC; không chứa secret/token/raw password..
- `BR-OPS-003` — `01_TONG_QUAN_DU_AN.md:L450` — Notification và side effect ngoài transaction được tạo qua outbox với dedupe key. Retry exponential có giới hạn; hết retry vào DLQ và cảnh báo..
- `BR-WRK-018` — `01_TONG_QUAN_DU_AN.md:L390` — Moderation takedown giữ revision, application và audit; chặn discovery/apply mới nhưng không xóa lịch sử tuyển dụng hợp pháp..
- `PERM-OPS-001` — `01_TONG_QUAN_DU_AN.md:L199` — `operations.verification.review` — Platform Moderator được ủy quyền.
- `PERM-OPS-002` — `01_TONG_QUAN_DU_AN.md:L200` — `operations.job_review` — Platform Moderator.
- `PERM-OPS-003` — `01_TONG_QUAN_DU_AN.md:L201` — `operations.trusted_publisher.manage` — Platform Admin được ủy quyền.
- `PERM-WRK-012` — `01_TONG_QUAN_DU_AN.md:L169` — `work.jobs.submit_review` — Enterprise Owner/Admin, Recruiter được ủy quyền.
- `PERM-OPS-005` — `01_TONG_QUAN_DU_AN.md:L203` — `operations.break_glass.use` — Incident responder được chỉ định.
- `BR-INT-009` — `01_TONG_QUAN_DU_AN.md:L404` — Event duplicate/stale bị bỏ qua theo aggregate version; event gap vào retry/catch-up. Poison event vào DLQ và không được đánh dấu thành công giả..
- `BR-OPS-008` — `01_TONG_QUAN_DU_AN.md:L455` — Restore backup phải áp lại deletion/revocation ledger trước khi mở traffic để dữ liệu đã xóa/thu hồi không sống lại..
- `NFR-OPS-001` — `01_TONG_QUAN_DU_AN.md:L648` — Hệ thống pilot hỗ trợ 5.000 account, 500 DAU và 50 RPS đỉnh trong 15 phút mà không vượt 80% connection pool/CPU kéo dài hoặc mất request đã acknowledge..
- `NFR-OPS-002` — `01_TONG_QUAN_DU_AN.md:L649` — Availability theo tháng của Identity, Study core và Work core đạt ít nhất 99,0%; dependency ngoài được đo riêng nhưng hệ thống phải thể hiện degraded state an toàn..
- `NFR-OPS-003` — `01_TONG_QUAN_DU_AN.md:L650` — p95 server latency: read đồng bộ ≤ 800 ms, mutation đồng bộ ≤ 1,5 giây; không tính phần việc đã công bố async. Query report lớn bắt buộc async/export..
- `NFR-OPS-004` — `01_TONG_QUAN_DU_AN.md:L651` — Chat server acknowledgement sau khi persist p95 ≤ 2 giây; reconnect/history không mất hoặc nhân đôi message theo client key..
- `NFR-OPS-005` — `01_TONG_QUAN_DU_AN.md:L652` — RPO toàn bộ PostgreSQL ≤ 15 phút; RTO cho Identity/Study/Work core ≤ 4 giờ. Restore drill thực hiện ít nhất mỗi quý trong pilot..
- `NFR-OPS-006` — `01_TONG_QUAN_DU_AN.md:L653` — Outbox/event projection p95 ≤ 60 giây khi bình thường; evidence export p95 ≤ 2 phút. Backlog, oldest age, retry và DLQ có alert..
- `NFR-OPS-007` — `01_TONG_QUAN_DU_AN.md:L654` — Candidate opt-out được kiểm end-to-end và đáp ứng hard limit 5 phút gồm DB projection, index, cache và active search response..
- `NFR-OPS-008` — `01_TONG_QUAN_DU_AN.md:L655` — File scan p95 ≤ 2 phút cho file trong giới hạn V1 khi scanner khỏe; pending/failed luôn fail closed, có trạng thái và retry rõ ràng..
- `NFR-OPS-009` — `01_TONG_QUAN_DU_AN.md:L656` — Mọi request có trace ID; mutation quan trọng liên kết audit/outbox/provider transaction. Log JSON có severity, service, environment và không chứa secret/PII payload..
- `NFR-OPS-010` — `01_TONG_QUAN_DU_AN.md:L657` — Web đạt WCAG 2.2 AA cho luồng chính: keyboard, focus, label, contrast, error announcement và reduced motion; responsive từ 360 px, hỗ trợ hai phiên bản major mới nhất của Chrome, Edge, Firefox, Safari..
- `NFR-OPS-011` — `01_TONG_QUAN_DU_AN.md:L658` — API/event/database migration và tài liệu phải pass contract/trace validator; không phát hành khi có reference mất, duplicate method+path hoặc enum/state mâu thuẫn..
- `NFR-OPS-012` — `01_TONG_QUAN_DU_AN.md:L659` — Backup mã hóa, kiểm restore; secret quay vòng; high/critical security finding, cross-tenant leak hoặc payment integrity failure là release blocker..

## 5. Chi tiết từng API

### API-OPS-007 — `GET /api/v1/admin/audit-logs`

- **Nguồn contract:** `04_DAC_TA_API.md:L428`.
- **Actor/quyền:** Scoped audit permission + MFA.
- **Input/validation → output:** Cursor, service, actor, target, action, date <=31d → redacted stream.
- **Xử lý và dữ liệu:** Query each service's own audit only; UI calls service host separately; immutable`(occurred_at,id)`; PII field access scoped.
- **Vận hành:** No cache; every query/export audited.
- **Lỗi đặc thù:** `AUDIT_SCOPE_DENIED`, `DATE_RANGE_TOO_LARGE`.
- **Màn hình/consumer:** `SCR-OPS-024`.
- **Capability/use case:** `CAP-STU-008`, `UC-STU-008`, `CAP-WRK-010`, `UC-WRK-010`, `CAP-OPS-001`, `UC-OPS-001`.

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

### API-OPS-008 — `POST /api/v1/admin/audit-exports`

- **Nguồn contract:** `04_DAC_TA_API.md:L429`.
- **Actor/quyền:** Export permission + step-up.
- **Input/validation → output:** Same filters, reason → async encrypted export.
- **Xử lý và dữ liệu:** Snapshot filters/authorization; short-lived signed download; watermark; retention 7d.
- **Vận hành:** Idempotency; immutable export audit.
- **Lỗi đặc thù:** `EXPORT_SCOPE_DENIED`, `EXPORT_TOO_LARGE`.
- **Màn hình/consumer:** `SCR-OPS-024`.
- **Capability/use case:** `CAP-STU-008`, `UC-STU-008`, `CAP-WRK-010`, `UC-WRK-010`, `CAP-OPS-001`, `UC-OPS-001`.

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

### API-OPS-009 — `POST /api/v1/admin/break-glass-sessions`

- **Nguồn contract:** `04_DAC_TA_API.md:L430`.
- **Actor/quyền:** Designated incident responder + hardware/recent MFA.
- **Input/validation → output:** Ticket ID, scope, max 60m, reason → elevated session.
- **Xử lý và dữ liệu:** Approval policy: second approver unless declared SEV-1; credentials time-bound; no silent role mutation.
- **Vận hành:** Idempotency; immediate security alert; full command/data audit.
- **Lỗi đặc thù:** `BREAK_GLASS_APPROVAL_REQUIRED`, `INCIDENT_TICKET_INVALID`.
- **Màn hình/consumer:** `SCR-OPS-025`.
- **Capability/use case:** `CAP-STU-008`, `UC-STU-008`, `CAP-WRK-010`, `UC-WRK-010`, `CAP-OPS-001`, `UC-OPS-001`.

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

### API-OPS-010 — `GET /api/v1/admin/operational-reports`

- **Nguồn contract:** `04_DAC_TA_API.md:L431`.
- **Actor/quyền:** Domain report permission.
- **Input/validation → output:** Report code/date/filter → aggregate metrics + freshness.
- **Xử lý và dữ liệu:** R daily metrics/projections; no warehouse V1; report definition/version returned.
- **Vận hành:** Cache 5m; access audit.
- **Lỗi đặc thù:** `REPORT_NOT_FOUND`, `DATA_NOT_FRESH` warning in meta.
- **Màn hình/consumer:** `SCR-OPS-021`.
- **Capability/use case:** `CAP-STU-008`, `UC-STU-008`, `CAP-WRK-010`, `UC-WRK-010`, `CAP-OPS-003`, `UC-OPS-003`.

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
