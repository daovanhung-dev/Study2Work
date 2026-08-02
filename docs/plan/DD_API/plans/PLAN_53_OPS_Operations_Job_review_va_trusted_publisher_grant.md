# PLAN 53 — Operations — Job review và trusted publisher grant

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-53` |
| API trong phạm vi | `API-OPS-003`, `API-OPS-004`, `API-OPS-005`, `API-OPS-006` |
| Số API | 4 |
| Read-only / Mutation | 1 / 3 |
| Khối lượng lõi | 32 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho review queue/decision và cấp/thu hồi trusted publisher.

**Luồng nghiệp vụ trọng tâm:** Job review list/decision under optimistic lock; grant time-bounded scope/reason; revoke immediate; all publish still automated policy check.

**Điểm cần khóa:** Two-reviewer race, maker-checker, grant expiry/revocation and audit.

**Dependency:** Plans 20,35.

## 3. Phạm vi

**In-scope**

- `API-OPS-003` — `GET /api/v1/admin/job-reviews`.
- `API-OPS-004` — `POST /api/v1/admin/job-reviews/{id}/decisions`.
- `API-OPS-005` — `POST /api/v1/admin/trusted-publisher-grants`.
- `API-OPS-006` — `POST /api/v1/admin/trusted-publisher-grants/{id}/revoke`.

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

- `01_TONG_QUAN_DU_AN.md:L765` — `CAP-STU-006` / `UC-STU-006`; rules ``BR-STU-007`, `BR-STU-013–014`, `PERM-STU-001–005``; diagrams ``AC-STU-003`, `SEQ-STU-004``; data ``CLS-STU-001`; `TBL-STU-009–025`, `TBL-STU-035–036``; screens ``SCR-OPS-003–011``; test ``TC-STU-006``.
- `01_TONG_QUAN_DU_AN.md:L771` — `CAP-WRK-004` / `UC-WRK-004`; rules ``BR-WRK-005–007`, `PERM-WRK-010–013`, `BR-OPS-010``; diagrams ``AC-WRK-002`, `SEQ-WRK-002``; data ``CLS-WRK-001`; `TBL-WRK-032–036`, `TBL-WRK-074``; screens ``SCR-WRK-033–035`, `SCR-OPS-009–011``; test ``TC-WRK-004``.
- `01_TONG_QUAN_DU_AN.md:L777` — `CAP-WRK-010` / `UC-WRK-010`; rules ``BR-WRK-018`, `PERM-OPS-001–003`, `PERM-WRK-012`, `BR-OPS-001–002``; diagrams ``AC-OPS-001`, `SEQ-OPS-001``; data ``CLS-WRK-002`; `TBL-WRK-035–036`, `TBL-WRK-060–061``; screens ``SCR-OPS-009–011`, `SCR-OPS-017–018`, `SCR-OPS-021`, `SCR-OPS-024–026``; test ``TC-WRK-010``.
- `01_TONG_QUAN_DU_AN.md:L787` — `CAP-OPS-001` / `UC-OPS-001`; rules ``BR-WRK-018`, `BR-OPS-001–002`, `PERM-OPS-001–003`, `PERM-OPS-005``; diagrams ``AC-OPS-001`, `SEQ-OPS-001``; data ``CLS-WRK-002`; `TBL-WRK-015`, `TBL-WRK-020`, `TBL-WRK-035`, `TBL-WRK-060–061``; screens ``SCR-OPS-009–011`, `SCR-OPS-017–018`, `SCR-OPS-024–025``; test ``TC-OPS-001``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-STU-003` — `02_BIEU_DO_HE_THONG.md:L465` — AC-STU-003 — Soạn và publish content version.
- `SEQ-STU-004` — `02_BIEU_DO_HE_THONG.md:L1978` — SEQ-STU-004 — Pre-publish, atomic version swap và cache invalidation.
- `AC-WRK-002` — `02_BIEU_DO_HE_THONG.md:L582` — AC-WRK-002 — Job revision, apply và ATS.
- `SEQ-WRK-002` — `02_BIEU_DO_HE_THONG.md:L2119` — SEQ-WRK-002 — Job revision, review và publish cạnh tranh.
- `AC-OPS-001` — `02_BIEU_DO_HE_THONG.md:L802` — AC-OPS-001 — Moderation, deletion, legal hold và recovery.
- `SEQ-OPS-001` — `02_BIEU_DO_HE_THONG.md:L2554` — SEQ-OPS-001 — Moderation action, deletion fan-out và DLQ replay.
- `CLS-STU-001` — `02_BIEU_DO_HE_THONG.md:L931` — CLS-STU-001 — Study profile, RBAC và curriculum versioning.
- `CLS-WRK-001` — `02_BIEU_DO_HE_THONG.md:L1266` — CLS-WRK-001 — Candidate, tenant, job, application và ATS snapshots.
- `CLS-WRK-002` — `02_BIEU_DO_HE_THONG.md:L1384` — CLS-WRK-002 — Interview, chat, university và moderation.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-STU-009` — `learning_paths` — `03_THIET_KE_CO_SO_DU_LIEU.md:L320 `.
- `TBL-STU-010` — `learning_path_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L327 `.
- `TBL-STU-011` — `courses` — `03_THIET_KE_CO_SO_DU_LIEU.md:L334 `.
- `TBL-STU-012` — `course_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L341 `.
- `TBL-STU-013` — `path_course_items` — `03_THIET_KE_CO_SO_DU_LIEU.md:L348 `.
- `TBL-STU-014` — `chapters` — `03_THIET_KE_CO_SO_DU_LIEU.md:L355 `.
- `TBL-STU-015` — `lessons` — `03_THIET_KE_CO_SO_DU_LIEU.md:L362 `.
- `TBL-STU-016` — `content_blocks` — `03_THIET_KE_CO_SO_DU_LIEU.md:L369 `.
- `TBL-STU-017` — `content_rights_attestations` — `03_THIET_KE_CO_SO_DU_LIEU.md:L376 `.
- `TBL-STU-018` — `content_review_decisions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L383 `.
- `TBL-STU-019` — `trusted_publisher_grants` — `03_THIET_KE_CO_SO_DU_LIEU.md:L390 `.
- `TBL-STU-020` — `assessments` — `03_THIET_KE_CO_SO_DU_LIEU.md:L399 `.
- `TBL-STU-021` — `assessment_placements` — `03_THIET_KE_CO_SO_DU_LIEU.md:L406 `.
- `TBL-STU-022` — `quiz_questions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L413 `.
- `TBL-STU-023` — `quiz_options` — `03_THIET_KE_CO_SO_DU_LIEU.md:L420 `.
- `TBL-STU-024` — `rubrics` — `03_THIET_KE_CO_SO_DU_LIEU.md:L427 `.
- `TBL-STU-025` — `rubric_criteria` — `03_THIET_KE_CO_SO_DU_LIEU.md:L434 `.
- `TBL-STU-035` — `file_objects` — `03_THIET_KE_CO_SO_DU_LIEU.md:L509 `.
- `TBL-STU-036` — `malware_scan_results` — `03_THIET_KE_CO_SO_DU_LIEU.md:L517 `.
- `TBL-WRK-032` — `jobs` — `03_THIET_KE_CO_SO_DU_LIEU.md:L929 `.
- `TBL-WRK-033` — `job_revisions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L936 `.
- `TBL-WRK-034` — `job_skill_requirements` — `03_THIET_KE_CO_SO_DU_LIEU.md:L943 `.
- `TBL-WRK-035` — `job_review_decisions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L950 `.
- `TBL-WRK-036` — `job_status_history` — `03_THIET_KE_CO_SO_DU_LIEU.md:L957 `.
- `TBL-WRK-074` — `job_screening_questions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1389 `.
- `TBL-WRK-060` — `moderation_reports` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1293 `.
- `TBL-WRK-061` — `audit_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1300 `.
- `TBL-WRK-015` — `enterprise_verification_cases` — `03_THIET_KE_CO_SO_DU_LIEU.md:L805 `.
- `TBL-WRK-020` — `university_verification_cases` — `03_THIET_KE_CO_SO_DU_LIEU.md:L843 `.

**Screen và acceptance**

- Screens: `SCR-OPS-003`, `SCR-OPS-004`, `SCR-OPS-005`, `SCR-OPS-006`, `SCR-OPS-007`, `SCR-OPS-008`, `SCR-OPS-009`, `SCR-OPS-010`, `SCR-OPS-011`, `SCR-WRK-033`, `SCR-WRK-034`, `SCR-WRK-035`, `SCR-OPS-017`, `SCR-OPS-018`, `SCR-OPS-021`, `SCR-OPS-024`, `SCR-OPS-025`, `SCR-OPS-026`.
- Acceptance: `TC-STU-006`, `TC-WRK-004`, `TC-WRK-010`, `TC-OPS-001`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-STU-007` — `01_TONG_QUAN_DU_AN.md:L357` — Published path/course version là bất biến. Publish version mới atomically đổi current version và đánh dấu bản cũ `SUPERSEDED`; enrollment cũ tiếp tục pin bản cũ..
- `BR-STU-013` — `01_TONG_QUAN_DU_AN.md:L363` — Mỗi assessment placement thuộc đúng một scope: path version, course version, chapter hoặc lesson. Quan hệ không hợp lệ bị chặn ở application và database constraint..
- `BR-STU-014` — `01_TONG_QUAN_DU_AN.md:L364` — Trusted publisher không được bỏ qua rights check, HTML/Markdown sanitization, malware scan, cấu trúc curriculum, rubric hoặc audit. Author không tự có quyền publish..
- `PERM-STU-001` — `01_TONG_QUAN_DU_AN.md:L150` — `study.content.read_admin` — Content Author/Publisher, Study Admin.
- `PERM-STU-002` — `01_TONG_QUAN_DU_AN.md:L151` — `study.content.write` — Content Author/Publisher, Study Admin.
- `PERM-STU-003` — `01_TONG_QUAN_DU_AN.md:L152` — `study.content.publish` — Content Publisher, Study Admin.
- `PERM-STU-004` — `01_TONG_QUAN_DU_AN.md:L153` — `study.content.archive` — Study Admin.
- `PERM-STU-005` — `01_TONG_QUAN_DU_AN.md:L154` — `study.content_issues.manage` — Content Publisher, Study Admin.
- `BR-WRK-005` — `01_TONG_QUAN_DU_AN.md:L377` — Enterprise phải `VERIFIED` mới publish job, search candidate, gửi invitation hoặc mua quyền lợi tenant. Suspension chặn mutation mới nhưng giữ audit/history..
- `BR-WRK-006` — `01_TONG_QUAN_DU_AN.md:L378` — Job dùng stable entity và immutable revision. Sửa job đang published tạo draft revision mới; bản đang published vẫn phục vụ cho đến khi bản mới được duyệt và swap atomically..
- `BR-WRK-007` — `01_TONG_QUAN_DU_AN.md:L379` — Job lifecycle duy nhất là `DRAFT → REVIEW_PENDING → PUBLISHED ↔ PAUSED → CLOSED|EXPIRED|TAKEN_DOWN`; transition phải đúng quyền, version và audit..
- `PERM-WRK-010` — `01_TONG_QUAN_DU_AN.md:L167` — `work.jobs.read_admin` — Enterprise Owner/Admin, Recruiter.
- `PERM-WRK-011` — `01_TONG_QUAN_DU_AN.md:L168` — `work.jobs.author` — Enterprise Owner/Admin, Recruiter.
- `PERM-WRK-012` — `01_TONG_QUAN_DU_AN.md:L169` — `work.jobs.submit_review` — Enterprise Owner/Admin, Recruiter được ủy quyền.
- `PERM-WRK-013` — `01_TONG_QUAN_DU_AN.md:L170` — `work.jobs.publish_manage` — Enterprise Owner/Admin; trusted publisher theo grant có hạn.
- `BR-OPS-010` — `01_TONG_QUAN_DU_AN.md:L457` — Mutation quan trọng dùng idempotency/optimistic version theo hợp đồng; conflict không silently overwrite và trả current version an toàn để client tải lại..
- `BR-WRK-018` — `01_TONG_QUAN_DU_AN.md:L390` — Moderation takedown giữ revision, application và audit; chặn discovery/apply mới nhưng không xóa lịch sử tuyển dụng hợp pháp..
- `PERM-OPS-001` — `01_TONG_QUAN_DU_AN.md:L199` — `operations.verification.review` — Platform Moderator được ủy quyền.
- `PERM-OPS-002` — `01_TONG_QUAN_DU_AN.md:L200` — `operations.job_review` — Platform Moderator.
- `PERM-OPS-003` — `01_TONG_QUAN_DU_AN.md:L201` — `operations.trusted_publisher.manage` — Platform Admin được ủy quyền.
- `BR-OPS-001` — `01_TONG_QUAN_DU_AN.md:L448` — Audit/security/payment webhook/ledger/application history/evidence snapshot/AI review/outbox là append-only; không cascade delete làm mất lịch sử..
- `BR-OPS-002` — `01_TONG_QUAN_DU_AN.md:L449` — Audit chứa actor, effective role/tenant, action, resource, before/after đã redact, reason, IP/device tối thiểu, trace ID và thời điểm UTC; không chứa secret/token/raw password..
- `PERM-OPS-005` — `01_TONG_QUAN_DU_AN.md:L203` — `operations.break_glass.use` — Incident responder được chỉ định.

## 5. Chi tiết từng API

### API-OPS-003 — `GET /api/v1/admin/job-reviews`

- **Nguồn contract:** `04_DAC_TA_API.md:L424`.
- **Actor/quyền:** `PERM-OPS-002`.
- **Input/validation → output:** Page/status/risk/age → review queue.
- **Xử lý và dữ liệu:** R case/job revision/automated check; tenant data minimized.
- **Vận hành:** Private.
- **Lỗi đặc thù:** —.
- **Màn hình/consumer:** `SCR-OPS-009`.
- **Capability/use case:** `CAP-WRK-004`, `UC-WRK-004`, `CAP-WRK-010`, `UC-WRK-010`, `CAP-OPS-001`, `UC-OPS-001`.

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

### API-OPS-004 — `POST /api/v1/admin/job-reviews/{id}/decisions`

- **Nguồn contract:** `04_DAC_TA_API.md:L425`.
- **Actor/quyền:** `PERM-OPS-002`.
- **Input/validation → output:** Approve/reject/request-change, reason/policy codes, If-Match → case.
- **Xử lý và dữ liệu:** TX append decision; approval does not publish until API-WRK-047; reject returns job to draft policy.
- **Vận hành:** Idempotency; audit/notification.
- **Lỗi đặc thù:** `JOB_REVIEW_CONFLICT`, `POLICY_REASON_REQUIRED`.
- **Màn hình/consumer:** `SCR-OPS-010`.
- **Capability/use case:** `CAP-WRK-004`, `UC-WRK-004`, `CAP-WRK-010`, `UC-WRK-010`, `CAP-OPS-001`, `UC-OPS-001`.

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

### API-OPS-005 — `POST /api/v1/admin/trusted-publisher-grants`

- **Nguồn contract:** `04_DAC_TA_API.md:L426`.
- **Actor/quyền:** `PERM-OPS-003` + recent MFA.
- **Input/validation → output:** Subject/tenant, domain STUDY/WORK, scopes, validFrom/until, evidence, reason → grant.
- **Xử lý và dữ liệu:** Validate eligibility metrics or require`bootstrapPilot=true` + reason; append grant; separation from grantee.
- **Vận hành:** Idempotency; security audit/event.
- **Lỗi đặc thù:** `TRUST_ELIGIBILITY_FAILED`, `GRANT_PERIOD_INVALID`, `SELF_GRANT_FORBIDDEN`.
- **Màn hình/consumer:** `SCR-OPS-011`.
- **Capability/use case:** `CAP-STU-006`, `UC-STU-006`, `CAP-WRK-004`, `UC-WRK-004`, `CAP-WRK-010`, `UC-WRK-010`, `CAP-OPS-001`, `UC-OPS-001`.

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

### API-OPS-006 — `POST /api/v1/admin/trusted-publisher-grants/{id}/revoke`

- **Nguồn contract:** `04_DAC_TA_API.md:L427`.
- **Actor/quyền:** `PERM-OPS-003` + MFA.
- **Input/validation → output:** Reason → revoked.
- **Xử lý và dữ liệu:** TX append revocation; future publishes denied immediately; past content remains with audit.
- **Vận hành:** Idempotency; alert/event.
- **Lỗi đặc thù:** `GRANT_ALREADY_REVOKED`.
- **Màn hình/consumer:** `SCR-OPS-011`.
- **Capability/use case:** `CAP-STU-006`, `UC-STU-006`, `CAP-WRK-004`, `UC-WRK-004`, `CAP-WRK-010`, `UC-WRK-010`, `CAP-OPS-001`, `UC-OPS-001`.

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
