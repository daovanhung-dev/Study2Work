# PLAN 49 — AI — CV/JD generation, job status và human review

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-49` |
| API trong phạm vi | `API-AIX-001`, `API-AIX-002`, `API-AIX-005`, `API-AIX-006` |
| Số API | 4 |
| Read-only / Mutation | 1 / 3 |
| Khối lượng lõi | 32 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho tạo async AI writing job, poll status và human accept/edit/reject.

**Luồng nghiệp vụ trọng tâm:** Snapshot input/model/prompt/policy, queue job, safety/schema gate; GET status/output safe; review append-only và chỉ explicit human action mới tạo content revision.

**Điểm cần khóa:** Prompt injection, PII minimization, provenance, kill switch, no automatic save.

**Dependency:** Plan 58 provider callback; Plan 52 governance.

## 3. Phạm vi

**In-scope**

- `API-AIX-001` — `POST /api/v1/me/cvs/{cvId}/ai-writing-jobs`.
- `API-AIX-002` — `POST /api/v1/enterprises/{enterpriseId}/jobs/{jobId}/ai-jd-jobs`.
- `API-AIX-005` — `GET /api/v1/ai-jobs/{aiJobId}`.
- `API-AIX-006` — `POST /api/v1/ai-jobs/{aiJobId}/reviews`.

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
- `01_TONG_QUAN_DU_AN.md:L776` — `CAP-WRK-009` / `UC-WRK-009`; rules ``BR-WRK-017`, `BR-PAY-006`, `BR-AIX-002–003`, `PERM-WRK-060``; diagrams ``AC-WRK-001`, `AC-PAY-001`, `SEQ-WRK-001`, `SEQ-PAY-001``; data ``CLS-WRK-001`, `CLS-PAY-001`, `CLS-AIX-001`; `TBL-WRK-010–011`, `TBL-PAY-010–013``; screens ``SCR-WRK-013`, `SCR-WRK-022`, `SCR-WRK-034`, `SCR-WRK-043``; test ``TC-WRK-009``.
- `01_TONG_QUAN_DU_AN.md:L784` — `CAP-AIX-001` / `UC-AIX-001`; rules ``BR-AIX-001–003`, `BR-AIX-005–007`, `PERM-AIX-001` chỉ áp dụng kill switch`; diagrams ``AC-AIX-001`, `SEQ-AIX-001``; data ``CLS-AIX-001`; `TBL-AIX-001–006`, `TBL-WRK-010–011`, `TBL-WRK-033``; screens ``SCR-WRK-013`, `SCR-WRK-034``; test ``TC-AIX-001``.
- `01_TONG_QUAN_DU_AN.md:L785` — `CAP-AIX-002` / `UC-AIX-002`; rules ``BR-AIX-002–007`, `PERM-WRK-070–071`, `NFR-OPS-006``; diagrams ``AC-AIX-001`, `SEQ-AIX-001``; data ``CLS-AIX-001`; `TBL-AIX-004–007`, `TBL-WRK-041–042``; screens ``SCR-WRK-039–040``; test ``TC-AIX-002``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-WRK-001` — `02_BIEU_DO_HE_THONG.md:L548` — AC-WRK-001 — Candidate privacy, search, invitation và opt-out.
- `SEQ-WRK-003` — `02_BIEU_DO_HE_THONG.md:L2156` — SEQ-WRK-003 — Apply, immutable snapshots và ATS transition.
- `AC-PAY-001` — `02_BIEU_DO_HE_THONG.md:L729` — AC-PAY-001 — Checkout, callback, entitlement và reversal.
- `SEQ-WRK-001` — `02_BIEU_DO_HE_THONG.md:L2080` — SEQ-WRK-001 — Candidate opt-in/search, sponsored label và opt-out SLA.
- `SEQ-PAY-001` — `02_BIEU_DO_HE_THONG.md:L2415` — SEQ-PAY-001 — Checkout VNPAY/MoMo, IPN/webhook và entitlement once.
- `AC-AIX-001` — `02_BIEU_DO_HE_THONG.md:L767` — AC-AIX-001 — AI request, policy guard và human approval.
- `SEQ-AIX-001` — `02_BIEU_DO_HE_THONG.md:L2508` — SEQ-AIX-001 — AI async inference, safety gate và human-applied revision.
- `CLS-WRK-001` — `02_BIEU_DO_HE_THONG.md:L1266` — CLS-WRK-001 — Candidate, tenant, job, application và ATS snapshots.
- `CLS-PAY-001` — `02_BIEU_DO_HE_THONG.md:L1501` — CLS-PAY-001 — Order, provider event, ledger, entitlement và promotion.
- `CLS-AIX-001` — `02_BIEU_DO_HE_THONG.md:L1584` — CLS-AIX-001 — AI job, provenance, review và human-applied revision.

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
- `TBL-PAY-010` — `entitlements` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1235 `.
- `TBL-PAY-011` — `credit_ledger_entries` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1242 `.
- `TBL-PAY-012` — `promotion_campaigns` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1249 `.
- `TBL-PAY-013` — `sponsored_placements` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1256 `.
- `TBL-AIX-001` — `ai_model_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1113 `.
- `TBL-AIX-002` — `ai_prompt_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1120 `.
- `TBL-AIX-003` — `ai_policy_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1127 `.
- `TBL-AIX-004` — `ai_jobs` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1134 `.
- `TBL-AIX-005` — `ai_outputs` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1142 `.
- `TBL-AIX-006` — `ai_human_reviews` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1149 `.
- `TBL-WRK-033` — `job_revisions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L936 `.
- `TBL-AIX-007` — `match_score_snapshots` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1156 `.
- `TBL-WRK-041` — `applications` — `03_THIET_KE_CO_SO_DU_LIEU.md:L994 `.

**Screen và acceptance**

- Screens: `SCR-WRK-011`, `SCR-WRK-012`, `SCR-WRK-013`, `SCR-WRK-014`, `SCR-WRK-022`, `SCR-WRK-034`, `SCR-WRK-043`, `SCR-WRK-039`, `SCR-WRK-040`.
- Acceptance: `TC-WRK-001`, `TC-WRK-009`, `TC-AIX-001`, `TC-AIX-002`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-WRK-001` — `01_TONG_QUAN_DU_AN.md:L373` — Career profile mặc định `PRIVATE`. Chỉ candidate tự bật `SEARCHABLE`; không tenant, recruiter hoặc admin thông thường nào được bật thay..
- `BR-WRK-011` — `01_TONG_QUAN_DU_AN.md:L383` — Khi apply, Work chụp bất biến job revision, career profile, CV và portfolio được chọn. Thay đổi hồ sơ/CV/job sau đó không sửa application snapshot..
- `BR-OPS-004` — `01_TONG_QUAN_DU_AN.md:L451` — PII mã hóa khi truyền và khi lưu; object storage private theo namespace owner. Signed URL ngắn hạn, không được ghi vào audit/analytics/referrer..
- `NFR-OPS-003` — `01_TONG_QUAN_DU_AN.md:L650` — p95 server latency: read đồng bộ ≤ 800 ms, mutation đồng bộ ≤ 1,5 giây; không tính phần việc đã công bố async. Query report lớn bắt buộc async/export..
- `BR-WRK-017` — `01_TONG_QUAN_DU_AN.md:L389` — Sponsored profile/job luôn có nhãn, slot/rank riêng và trường `organicScore` không đổi. Payment không được tăng match score, ATS score hoặc quyền xem field riêng tư..
- `BR-PAY-006` — `01_TONG_QUAN_DU_AN.md:L425` — Chỉ `SETTLED` tạo entitlement/credit ledger đúng một lần trong cùng transaction. Entitlement không được âm; mọi consume/refund/expire là ledger append-only..
- `BR-AIX-002` — `01_TONG_QUAN_DU_AN.md:L436` — AI chỉ tạo CV/JD draft, writing suggestion, match explanation và shortlist suggestion. Output không tự publish, gửi, apply, thay đổi ATS, reject, offer hoặc hire..
- `BR-AIX-003` — `01_TONG_QUAN_DU_AN.md:L437` — Người dùng phải nhìn thấy nhãn AI, review và chủ động accept/edit/reject. Bản accept lưu nội dung người dùng xác nhận, không giả định AI đúng..
- `PERM-WRK-060` — `01_TONG_QUAN_DU_AN.md:L179` — `work.promotions.manage` — Enterprise Owner/Admin có entitlement.
- `BR-AIX-001` — `01_TONG_QUAN_DU_AN.md:L435` — AI chạy bất đồng bộ qua provider adapter; provider mặc định V1 là Ollama. Mỗi task pin provider, model version, prompt policy version, input hash và output schema version..
- `BR-AIX-005` — `01_TONG_QUAN_DU_AN.md:L439` — Raw file, contact, chat riêng, feedback mật và Study history chưa được chọn không gửi vào AI. Evidence chỉ dùng field cấu trúc đã consent cho application tương ứng..
- `BR-AIX-006` — `01_TONG_QUAN_DU_AN.md:L440` — Input được giới hạn, phân tách khỏi system instruction và kiểm prompt injection; output phải qua schema validation, safety filter và không được thực thi như lệnh/tool call..
- `BR-AIX-007` — `01_TONG_QUAN_DU_AN.md:L441` — Lỗi/timeout AI không chặn tạo/sửa CV, job, apply hoặc ATS thủ công. Retry có giới hạn; người dùng không bị trừ credit lần hai cho retry kỹ thuật cùng task..
- `PERM-AIX-001` — `01_TONG_QUAN_DU_AN.md:L196` — `ai.kill_switch.manage` — AI Governance Owner/Platform Admin được ủy quyền.
- `BR-AIX-004` — `01_TONG_QUAN_DU_AN.md:L438` — Matching chỉ dùng skill, kinh nghiệm, học vấn công khai, tiêu chí job và preference nghề nghiệp được phép; loại gender, tuổi/ngày sinh, ảnh, dân tộc, tôn giáo, khuyết tật, tình trạng hôn nhân, địa chỉ chi tiết, payment và sponsored status..
- `PERM-WRK-070` — `01_TONG_QUAN_DU_AN.md:L180` — `work.ai.match_explain` — Recruiter được phân công có entitlement.
- `PERM-WRK-071` — `01_TONG_QUAN_DU_AN.md:L181` — `work.ai.shortlist_suggest` — Enterprise Owner/Admin, lead recruiter có entitlement.
- `NFR-OPS-006` — `01_TONG_QUAN_DU_AN.md:L653` — Outbox/event projection p95 ≤ 60 giây khi bình thường; evidence export p95 ≤ 2 phút. Backlog, oldest age, retry và DLQ có alert..

## 5. Chi tiết từng API

### API-AIX-001 — `POST /api/v1/me/cvs/{cvId}/ai-writing-jobs`

- **Nguồn contract:** `04_DAC_TA_API.md:L405`.
- **Actor/quyền:** CV owner + AI entitlement/consent.
- **Input/validation → output:** Revision, section, goal, source text <=10k, locale → async job.
- **Xử lý và dữ liệu:** Snapshot sanitized allowed fields; reserve entitlement; create AI job with model/prompt/policy version; outbox; no autonomous CV mutation.
- **Vận hành:** Idempotency; 10/hour; audit/provenance.
- **Lỗi đặc thù:** `AI_ENTITLEMENT_REQUIRED`, `AI_INPUT_POLICY_FAILED`, `AI_DISABLED`.
- **Màn hình/consumer:** `SCR-WRK-013`.
- **Capability/use case:** `CAP-WRK-001`, `UC-WRK-001`, `CAP-WRK-009`, `UC-WRK-009`, `CAP-AIX-001`, `UC-AIX-001`.

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

### API-AIX-002 — `POST /api/v1/enterprises/{enterpriseId}/jobs/{jobId}/ai-jd-jobs`

- **Nguồn contract:** `04_DAC_TA_API.md:L406`.
- **Actor/quyền:** Job editor + entitlement.
- **Input/validation → output:** Draft revision, requested sections/style → async job.
- **Xử lý và dữ liệu:** Tenant predicate; exclude hidden tenant/user data; snapshot JD; create job.
- **Vận hành:** Idempotency; audit.
- **Lỗi đặc thù:** `AI_ENTITLEMENT_REQUIRED`, `JOB_REVISION_NOT_EDITABLE`, `AI_DISABLED`.
- **Màn hình/consumer:** `SCR-WRK-034`.
- **Capability/use case:** `CAP-WRK-009`, `UC-WRK-009`, `CAP-AIX-001`, `UC-AIX-001`.

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

### API-AIX-005 — `GET /api/v1/ai-jobs/{aiJobId}`

- **Nguồn contract:** `04_DAC_TA_API.md:L409`.
- **Actor/quyền:** Requester/authorized tenant member.
- **Input/validation → output:** → job`QUEUED/RUNNING/SUCCEEDED/FAILED/CANCELLED`; khi SUCCEEDED có output review `DRAFT/ACCEPTED/EDITED_ACCEPT/REJECTED/EXPIRED`, draft output/provenance.
- **Xử lý và dữ liệu:** Owner/tenant predicate; job execution và human review là hai state machine tách biệt; render output như untrusted text, không HTML execution.
- **Vận hành:** Private no-store; polling 1/2s.
- **Lỗi đặc thù:** `AI_JOB_NOT_FOUND`, `AI_OUTPUT_BLOCKED`.
- **Màn hình/consumer:** AI-enabled screens.
- **Capability/use case:** `CAP-AIX-001`, `UC-AIX-001`, `CAP-AIX-002`, `UC-AIX-002`.

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

### API-AIX-006 — `POST /api/v1/ai-jobs/{aiJobId}/reviews`

- **Nguồn contract:** `04_DAC_TA_API.md:L410`.
- **Actor/quyền:** Authorized human.
- **Input/validation → output:** Decision`ACCEPTED/EDITED_ACCEPT/REJECTED`, edited output/reason, If-Match → review.
- **Xử lý và dữ liệu:** TX append review; accepted CV/JD suggestion still requires explicit separate editor save; shortlist acceptance does not transition ATS.
- **Vận hành:** Idempotency; immutable audit; quality metric event.
- **Lỗi đặc thù:** `AI_REVIEW_CONFLICT`, `AI_JOB_NOT_REVIEWABLE`, `VERSION_CONFLICT`.
- **Màn hình/consumer:** AI-enabled screens.
- **Capability/use case:** `CAP-AIX-001`, `UC-AIX-001`, `CAP-AIX-002`, `UC-AIX-002`.

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
