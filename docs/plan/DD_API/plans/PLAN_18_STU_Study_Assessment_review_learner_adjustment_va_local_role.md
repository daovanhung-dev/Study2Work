# PLAN 18 — Study — Assessment review, learner adjustment và local role

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-18` |
| API trong phạm vi | `API-STU-047`, `API-STU-048`, `API-STU-049`, `API-STU-050`, `API-STU-060` |
| Số API | 5 |
| Read-only / Mutation | 1 / 4 |
| Khối lượng lõi | 40 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho hàng đợi reviewer, quyết định attempt, override primary path, điều chỉnh progress và gán local role.

**Luồng nghiệp vụ trọng tâm:** Admin/reviewer query theo permission; review dùng claim/optimistic version; override/adjustment append audit và không rewrite fact; role assignment diff dưới MFA/If-Match.

**Điểm cần khóa:** Two-reviewer race, maker-checker, before/after audit, không sửa lịch sử.

**Dependency:** Plan 13; Operations audit Plan 55.

## 3. Phạm vi

**In-scope**

- `API-STU-047` — `GET /api/v1/admin/assessment-reviews`.
- `API-STU-048` — `POST /api/v1/admin/assessment-attempts/{attemptId}/reviews`.
- `API-STU-049` — `POST /api/v1/admin/learners/{learnerId}/primary-path-overrides`.
- `API-STU-050` — `POST /api/v1/admin/learners/{learnerId}/progress-adjustments`.
- `API-STU-060` — `PUT /api/v1/admin/local-role-assignments/{userId}`.

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
- `01_TONG_QUAN_DU_AN.md:L762` — `CAP-STU-003` / `UC-STU-003`; rules ``BR-STU-008–009`, `BR-STU-015`, `PERM-STU-010`, `NFR-OPS-003``; diagrams ``AC-STU-002`, `SEQ-STU-002``; data ``CLS-STU-002`; `TBL-STU-027–032`, `TBL-STU-049``; screens ``SCR-STU-010`, `SCR-STU-015–016`, `SCR-STU-019`, `SCR-OPS-015``; test ``TC-STU-003``.
- `01_TONG_QUAN_DU_AN.md:L763` — `CAP-STU-004` / `UC-STU-004`; rules ``BR-STU-010–013`, `BR-STU-015`, `PERM-STU-006`, `NFR-OPS-008``; diagrams ``AC-STU-002`, `SEQ-STU-002–003``; data ``CLS-STU-002`; `TBL-STU-020–025`, `TBL-STU-033–039`, `TBL-STU-059``; screens ``SCR-STU-017–018`, `SCR-OPS-012–013``; test ``TC-STU-004``.
- `01_TONG_QUAN_DU_AN.md:L767` — `CAP-STU-008` / `UC-STU-008`; rules ``BR-STU-015`, `PERM-STU-009–014`, `BR-OPS-001–003``; diagrams ``AC-OPS-001`, `SEQ-OPS-001``; data ``CLS-STU-001–002`; `TBL-STU-003–006`, `TBL-STU-049–050`, `TBL-STU-054``; screens ``SCR-OPS-012–016`, `SCR-OPS-021`, `SCR-OPS-024``; test ``TC-STU-008``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-STU-001` — `02_BIEU_DO_HE_THONG.md:L379` — AC-STU-001 — Standalone course, onboarding và primary-path switch.
- `SEQ-STU-001` — `02_BIEU_DO_HE_THONG.md:L1828` — SEQ-STU-001 — Standalone enrollment và primary-path switch cạnh tranh.
- `AC-STU-002` — `02_BIEU_DO_HE_THONG.md:L416` — AC-STU-002 — Học bài, assessment, file scan và completion.
- `SEQ-STU-002` — `02_BIEU_DO_HE_THONG.md:L1881` — SEQ-STU-002 — Lesson progress và quiz auto-grade.
- `SEQ-STU-003` — `02_BIEU_DO_HE_THONG.md:L1923` — SEQ-STU-003 — Upload quarantine, scan, submit và hai reviewer cạnh tranh.
- `AC-OPS-001` — `02_BIEU_DO_HE_THONG.md:L802` — AC-OPS-001 — Moderation, deletion, legal hold và recovery.
- `SEQ-OPS-001` — `02_BIEU_DO_HE_THONG.md:L2554` — SEQ-OPS-001 — Moderation action, deletion fan-out và DLQ replay.
- `CLS-STU-001` — `02_BIEU_DO_HE_THONG.md:L931` — CLS-STU-001 — Study profile, RBAC và curriculum versioning.
- `CLS-STU-002` — `02_BIEU_DO_HE_THONG.md:L1059` — CLS-STU-002 — Enrollment, progress, assessment, file và evidence.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-STU-002` — `learner_profiles` — `03_THIET_KE_CO_SO_DU_LIEU.md:L267 `.
- `TBL-STU-007` — `onboarding_submissions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L304 `.
- `TBL-STU-008` — `path_recommendation_runs` — `03_THIET_KE_CO_SO_DU_LIEU.md:L311 `.
- `TBL-STU-009` — `learning_paths` — `03_THIET_KE_CO_SO_DU_LIEU.md:L320 `.
- `TBL-STU-010` — `learning_path_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L327 `.
- `TBL-STU-026` — `primary_path_periods` — `03_THIET_KE_CO_SO_DU_LIEU.md:L443 `.
- `TBL-STU-027` — `course_enrollments` — `03_THIET_KE_CO_SO_DU_LIEU.md:L450 `.
- `TBL-STU-028` — `block_progress_facts` — `03_THIET_KE_CO_SO_DU_LIEU.md:L457 `.
- `TBL-STU-029` — `lesson_progress_facts` — `03_THIET_KE_CO_SO_DU_LIEU.md:L464 `.
- `TBL-STU-030` — `progress_snapshots` — `03_THIET_KE_CO_SO_DU_LIEU.md:L471 `.
- `TBL-STU-031` — `course_completions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L478 `.
- `TBL-STU-032` — `path_completions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L485 `.
- `TBL-STU-049` — `admin_adjustments` — `03_THIET_KE_CO_SO_DU_LIEU.md:L616 `.
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
- `TBL-STU-003` — `service_roles` — `03_THIET_KE_CO_SO_DU_LIEU.md:L274 `.
- `TBL-STU-004` — `service_permissions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L281 `.
- `TBL-STU-005` — `service_role_permissions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L288 `.
- `TBL-STU-006` — `service_role_assignments` — `03_THIET_KE_CO_SO_DU_LIEU.md:L295 `.
- `TBL-STU-050` — `audit_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L623 `.
- `TBL-STU-054` — `report_snapshots` — `03_THIET_KE_CO_SO_DU_LIEU.md:L652 `.

**Screen và acceptance**

- Screens: `SCR-STU-011`, `SCR-STU-012`, `SCR-STU-013`, `SCR-OPS-015`, `SCR-STU-010`, `SCR-STU-015`, `SCR-STU-016`, `SCR-STU-019`, `SCR-STU-017`, `SCR-STU-018`, `SCR-OPS-012`, `SCR-OPS-013`, `SCR-OPS-014`, `SCR-OPS-016`, `SCR-OPS-021`, `SCR-OPS-024`.
- Acceptance: `TC-STU-002`, `TC-STU-003`, `TC-STU-004`, `TC-STU-008`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-STU-002` — `01_TONG_QUAN_DU_AN.md:L352` — Onboarding chỉ bắt buộc trước khi chọn primary path. Hoàn tất onboarding là đơn điệu; chỉnh profile tạo recommendation run mới nhưng không đưa trạng thái lùi..
- `BR-STU-003` — `01_TONG_QUAN_DU_AN.md:L353` — Mỗi learner có tối đa một primary path period `ACTIVE`; selection/switch dùng transaction lock và partial unique constraint..
- `BR-STU-004` — `01_TONG_QUAN_DU_AN.md:L354` — Self-switch bị khóa đúng 168 giờ tính theo UTC kể từ lần primary path thay đổi gần nhất. Initial selection và chọn sau khi path đã `COMPLETED` không bị cooldown..
- `BR-STU-005` — `01_TONG_QUAN_DU_AN.md:L355` — Admin chỉ bypass cooldown khi có `PERM-STU-009` (`study.primary_path.override`), nhập reason và xác nhận tác động; path mới vẫn có `nextSwitchAllowedAt = changedAt + 168 giờ`..
- `BR-STU-006` — `01_TONG_QUAN_DU_AN.md:L356` — Switch đóng period cũ bằng `SWITCHED_OUT`, tạo period mới atomically và không xóa course enrollment, progress, attempt, review, completion hay evidence..
- `PERM-STU-009` — `01_TONG_QUAN_DU_AN.md:L157` — `study.primary_path.override` — Learner Support được ủy quyền, Study Admin.
- `BR-OPS-010` — `01_TONG_QUAN_DU_AN.md:L457` — Mutation quan trọng dùng idempotency/optimistic version theo hợp đồng; conflict không silently overwrite và trả current version an toàn để client tải lại..
- `BR-STU-008` — `01_TONG_QUAN_DU_AN.md:L358` — Completion chỉ tái sử dụng khi đúng cùng `courseVersionId`; course có stable ID giống nhau nhưng version khác không được tự kế thừa completion hoặc progress..
- `BR-STU-009` — `01_TONG_QUAN_DU_AN.md:L359` — Nguồn sự thật tiến độ là completion fact của content block, lesson và assessment. Course/path percent chỉ là snapshot server tính, có thể rebuild và client không được ghi trực tiếp..
- `BR-STU-015` — `01_TONG_QUAN_DU_AN.md:L365` — Điều chỉnh progress/review đã ghi chỉ qua nghiệp vụ correction append-only có actor/reason; không xóa hoặc update fact gốc và không có learner API để recalculate/reset..
- `PERM-STU-010` — `01_TONG_QUAN_DU_AN.md:L158` — `study.progress.adjust` — Study Admin được ủy quyền.
- `NFR-OPS-003` — `01_TONG_QUAN_DU_AN.md:L650` — p95 server latency: read đồng bộ ≤ 800 ms, mutation đồng bộ ≤ 1,5 giây; không tính phần việc đã công bố async. Query report lớn bắt buộc async/export..
- `BR-STU-010` — `01_TONG_QUAN_DU_AN.md:L360` — Assessment V1 chỉ có `QUIZ`, `TEXT`, `LINK`, `FILE`. Quiz auto-grade; ba loại còn lại manual review theo rubric và mỗi lần resubmit tạo attempt mới..
- `BR-STU-011` — `01_TONG_QUAN_DU_AN.md:L361` — File assessment phải ở trạng thái `CLEAN` trước khi submit/download/review; infected hoặc scan failed không tạo attempt. Object lưu private, URL tải có hạn và được cấp sau authorization..
- `BR-STU-012` — `01_TONG_QUAN_DU_AN.md:L362` — Link assessment chỉ chấp nhận HTTPS tối đa 2.048 ký tự; backend không fetch, resolve preview hoặc follow redirect để tránh SSRF. Text tối đa 20.000 ký tự..
- `BR-STU-013` — `01_TONG_QUAN_DU_AN.md:L363` — Mỗi assessment placement thuộc đúng một scope: path version, course version, chapter hoặc lesson. Quan hệ không hợp lệ bị chặn ở application và database constraint..
- `PERM-STU-006` — `01_TONG_QUAN_DU_AN.md:L155` — `study.assessments.review` — Assessment Reviewer, Study Admin.
- `NFR-OPS-008` — `01_TONG_QUAN_DU_AN.md:L655` — File scan p95 ≤ 2 phút cho file trong giới hạn V1 khi scanner khỏe; pending/failed luôn fail closed, có trạng thái và retry rõ ràng..
- `PERM-STU-011` — `01_TONG_QUAN_DU_AN.md:L159` — `study.roles.manage` — Study Admin.
- `PERM-STU-012` — `01_TONG_QUAN_DU_AN.md:L160` — `study.community.moderate` — Community Moderator, Study Admin.
- `PERM-STU-013` — `01_TONG_QUAN_DU_AN.md:L161` — `study.reports.read` — Study Admin.
- `PERM-STU-014` — `01_TONG_QUAN_DU_AN.md:L162` — `study.audit.read` — Study Admin, Security Auditor theo scope.
- `BR-OPS-001` — `01_TONG_QUAN_DU_AN.md:L448` — Audit/security/payment webhook/ledger/application history/evidence snapshot/AI review/outbox là append-only; không cascade delete làm mất lịch sử..
- `BR-OPS-002` — `01_TONG_QUAN_DU_AN.md:L449` — Audit chứa actor, effective role/tenant, action, resource, before/after đã redact, reason, IP/device tối thiểu, trace ID và thời điểm UTC; không chứa secret/token/raw password..
- `BR-OPS-003` — `01_TONG_QUAN_DU_AN.md:L450` — Notification và side effect ngoài transaction được tạo qua outbox với dedupe key. Retry exponential có giới hạn; hết retry vào DLQ và cảnh báo..

## 5. Chi tiết từng API

### API-STU-047 — `GET /api/v1/admin/assessment-reviews`

- **Nguồn contract:** `04_DAC_TA_API.md:L182`.
- **Actor/quyền:** `PERM-STU-006`.
- **Input/validation → output:** Page/status/type/assignee/age → queue.
- **Xử lý và dữ liệu:** Tenant-free Study role scope; index status/assigned/created; only CLEAN file attempts.
- **Vận hành:** No shared cache; audit export only.
- **Lỗi đặc thù:** `PERMISSION_DENIED`.
- **Màn hình/consumer:** `SCR-OPS-012`.
- **Capability/use case:** `CAP-STU-004`, `UC-STU-004`, `CAP-STU-008`, `UC-STU-008`.

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

### API-STU-048 — `POST /api/v1/admin/assessment-attempts/{attemptId}/reviews`

- **Nguồn contract:** `04_DAC_TA_API.md:L183`.
- **Actor/quyền:** `PERM-STU-006`.
- **Input/validation → output:** Decision PASSED/NEEDS_REVISION/FAILED, rubric scores, feedback,`If-Match`.
- **Xử lý và dữ liệu:** TX L attempt; validate rubric/range/current UNDER_REVIEW; append review; update current result/version; completion recompute from facts.
- **Vận hành:** Idempotency required; review/completion events; full audit.
- **Lỗi đặc thù:** `REVIEW_CONFLICT`, `RUBRIC_INVALID`, `ATTEMPT_NOT_REVIEWABLE`.
- **Màn hình/consumer:** `SCR-OPS-013`.
- **Capability/use case:** `CAP-STU-004`, `UC-STU-004`, `CAP-STU-008`, `UC-STU-008`.

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

### API-STU-049 — `POST /api/v1/admin/learners/{learnerId}/primary-path-overrides`

- **Nguồn contract:** `04_DAC_TA_API.md:L184`.
- **Actor/quyền:** `PERM-STU-009` + MFA.
- **Input/validation → output:** Target version, bypassCooldown bool, reason >=20 → period.
- **Xử lý và dữ liệu:** Same lock/invariant as API-STU-014; bypass only explicit permission; always establishes new 168h cooldown.
- **Vận hành:** Idempotency; high-risk audit/event.
- **Lỗi đặc thù:** `OVERRIDE_REASON_REQUIRED`, `PATH_VERSION_NOT_PUBLISHED`.
- **Màn hình/consumer:** `SCR-OPS-015`.
- **Capability/use case:** `CAP-STU-002`, `UC-STU-002`, `CAP-STU-008`, `UC-STU-008`.

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

### API-STU-050 — `POST /api/v1/admin/learners/{learnerId}/progress-adjustments`

- **Nguồn contract:** `04_DAC_TA_API.md:L185`.
- **Actor/quyền:** `PERM-STU-010` + MFA.
- **Input/validation → output:** Target fact, corrected value, reason/evidence,`If-Match` → adjustment + rebuilt snapshots.
- **Xử lý và dữ liệu:** TX append adjustment, never delete original; recompute dependent completion under learner lock.
- **Vận hành:** Idempotency; immutable audit/event.
- **Lỗi đặc thù:** `ADJUSTMENT_INVALID`, `VERSION_CONFLICT`.
- **Màn hình/consumer:** `SCR-OPS-015`.
- **Capability/use case:** `CAP-STU-003`, `UC-STU-003`, `CAP-STU-008`, `UC-STU-008`.

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

### API-STU-060 — `PUT /api/v1/admin/local-role-assignments/{userId}`

- **Nguồn contract:** `04_DAC_TA_API.md:L200`.
- **Actor/quyền:** `PERM-STU-011` + MFA.
- **Input/validation → output:** Exact role codes, scopes, expiry, reason → assignments.
- **Xử lý và dữ liệu:** TX validate separation-of-duties; publisher/reviewer conflict policy; append assignment history.
- **Vận hành:** Idempotency; security audit/event.
- **Lỗi đặc thù:** `ROLE_SCOPE_INVALID`, `SEPARATION_OF_DUTIES_VIOLATION`.
- **Màn hình/consumer:** `SCR-OPS-016`.
- **Capability/use case:** `CAP-STU-008`, `UC-STU-008`.

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
