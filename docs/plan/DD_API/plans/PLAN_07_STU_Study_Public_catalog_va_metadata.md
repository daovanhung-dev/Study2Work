# PLAN 07 — Study — Public catalog và metadata

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-07` |
| API trong phạm vi | `API-STU-001`, `API-STU-002`, `API-STU-003`, `API-STU-004`, `API-STU-005`, `API-STU-006` |
| Số API | 6 |
| Read-only / Mutation | 6 / 0 |
| Khối lượng lõi | 48 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Trung bình |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho danh sách/chi tiết learning path, course, sample lesson và taxonomy skill công khai.

**Luồng nghiệp vụ trọng tâm:** Anonymous truy vấn revision đã publish, filter/sort allowlist, visibility và cache/ETag; sample lesson chỉ trả nội dung được phép.

**Điểm cần khóa:** Read-only, published revision pinning, CDN cache và không lộ nội dung private.

**Dependency:** Content publish Plans 20–21.

## 3. Phạm vi

**In-scope**

- `API-STU-001` — `GET /api/v1/catalog/learning-paths`.
- `API-STU-002` — `GET /api/v1/catalog/learning-paths/{slug}`.
- `API-STU-003` — `GET /api/v1/catalog/courses`.
- `API-STU-004` — `GET /api/v1/catalog/courses/{slug}`.
- `API-STU-005` — `GET /api/v1/catalog/sample-lessons/{lessonId}`.
- `API-STU-006` — `GET /api/v1/metadata/skills`.

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

- `01_TONG_QUAN_DU_AN.md:L760` — `CAP-STU-001` / `UC-STU-001`; rules ``BR-STU-001`, `BR-STU-007–009`, `NFR-OPS-003``; diagrams ``AC-STU-001`, `SEQ-STU-001``; data ``CLS-STU-001–002`; `TBL-STU-009–016`, `TBL-STU-027``; screens ``SCR-STU-002–006`, `SCR-STU-014–016``; test ``TC-STU-001``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-STU-001` — `02_BIEU_DO_HE_THONG.md:L379` — AC-STU-001 — Standalone course, onboarding và primary-path switch.
- `SEQ-STU-001` — `02_BIEU_DO_HE_THONG.md:L1828` — SEQ-STU-001 — Standalone enrollment và primary-path switch cạnh tranh.
- `CLS-STU-001` — `02_BIEU_DO_HE_THONG.md:L931` — CLS-STU-001 — Study profile, RBAC và curriculum versioning.
- `CLS-STU-002` — `02_BIEU_DO_HE_THONG.md:L1059` — CLS-STU-002 — Enrollment, progress, assessment, file và evidence.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-STU-009` — `learning_paths` — `03_THIET_KE_CO_SO_DU_LIEU.md:L320 `.
- `TBL-STU-010` — `learning_path_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L327 `.
- `TBL-STU-011` — `courses` — `03_THIET_KE_CO_SO_DU_LIEU.md:L334 `.
- `TBL-STU-012` — `course_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L341 `.
- `TBL-STU-013` — `path_course_items` — `03_THIET_KE_CO_SO_DU_LIEU.md:L348 `.
- `TBL-STU-014` — `chapters` — `03_THIET_KE_CO_SO_DU_LIEU.md:L355 `.
- `TBL-STU-015` — `lessons` — `03_THIET_KE_CO_SO_DU_LIEU.md:L362 `.
- `TBL-STU-016` — `content_blocks` — `03_THIET_KE_CO_SO_DU_LIEU.md:L369 `.
- `TBL-STU-027` — `course_enrollments` — `03_THIET_KE_CO_SO_DU_LIEU.md:L450 `.

**Screen và acceptance**

- Screens: `SCR-STU-002`, `SCR-STU-003`, `SCR-STU-004`, `SCR-STU-005`, `SCR-STU-006`, `SCR-STU-014`, `SCR-STU-015`, `SCR-STU-016`.
- Acceptance: `TC-STU-001`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-STU-001` — `01_TONG_QUAN_DU_AN.md:L351` — Mọi course có current published version đều independently enrollable. Learner `ACTIVE` và đã xác minh email không cần onboarding hoặc primary path để học standalone..
- `BR-STU-007` — `01_TONG_QUAN_DU_AN.md:L357` — Published path/course version là bất biến. Publish version mới atomically đổi current version và đánh dấu bản cũ `SUPERSEDED`; enrollment cũ tiếp tục pin bản cũ..
- `BR-STU-008` — `01_TONG_QUAN_DU_AN.md:L358` — Completion chỉ tái sử dụng khi đúng cùng `courseVersionId`; course có stable ID giống nhau nhưng version khác không được tự kế thừa completion hoặc progress..
- `BR-STU-009` — `01_TONG_QUAN_DU_AN.md:L359` — Nguồn sự thật tiến độ là completion fact của content block, lesson và assessment. Course/path percent chỉ là snapshot server tính, có thể rebuild và client không được ghi trực tiếp..
- `NFR-OPS-003` — `01_TONG_QUAN_DU_AN.md:L650` — p95 server latency: read đồng bộ ≤ 800 ms, mutation đồng bộ ≤ 1,5 giây; không tính phần việc đã công bố async. Query report lớn bắt buộc async/export..

## 5. Chi tiết từng API

### API-STU-001 — `GET /api/v1/catalog/learning-paths`

- **Nguồn contract:** `04_DAC_TA_API.md:L126`.
- **Actor/quyền:** Public.
- **Input/validation → output:** Page,`q`, skill, level → published path cards.
- **Xử lý và dữ liệu:** R current`learning_paths` + `learning_path_versions`, aggregate courses; FTS/trigram + `(status,published_at)`; auth user gets own summary by separate indexed query.
- **Vận hành:** CDN/Redis 60s, ETag.
- **Lỗi đặc thù:** `INVALID_FILTER`.
- **Màn hình/consumer:** `SCR-STU-002`.
- **Capability/use case:** `CAP-STU-001`, `UC-STU-001`.

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

### API-STU-002 — `GET /api/v1/catalog/learning-paths/{slug}`

- **Nguồn contract:** `04_DAC_TA_API.md:L127`.
- **Actor/quyền:** Public.
- **Input/validation → output:** Slug → current published version, pinned course versions, prerequisites.
- **Xử lý và dữ liệu:** Join stable path/current version/composition by unique slug; old enrollment context never substituted.
- **Vận hành:** CDN 60s.
- **Lỗi đặc thù:** `PATH_NOT_FOUND`.
- **Màn hình/consumer:** `SCR-STU-003`.
- **Capability/use case:** `CAP-STU-001`, `UC-STU-001`.

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

### API-STU-003 — `GET /api/v1/catalog/courses`

- **Nguồn contract:** `04_DAC_TA_API.md:L128`.
- **Actor/quyền:** Public.
- **Input/validation → output:** Page, q, skill, level → standalone published courses.
- **Xử lý và dữ liệu:** Current published course version only; FTS/trigram; independently enrollable flag always true V1.
- **Vận hành:** CDN 60s.
- **Lỗi đặc thù:** `INVALID_FILTER`.
- **Màn hình/consumer:** `SCR-STU-004`.
- **Capability/use case:** `CAP-STU-001`, `UC-STU-001`.

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

### API-STU-004 — `GET /api/v1/catalog/courses/{slug}`

- **Nguồn contract:** `04_DAC_TA_API.md:L129`.
- **Actor/quyền:** Public.
- **Input/validation → output:** Slug → course/version curriculum preview and learner state.
- **Xử lý và dữ liệu:** Join current version/chapter/lesson summary; learner state pinned separately by user/course.
- **Vận hành:** CDN public fragment 60s; private fragment no-store.
- **Lỗi đặc thù:** `COURSE_NOT_FOUND`.
- **Màn hình/consumer:** `SCR-STU-005`.
- **Capability/use case:** `CAP-STU-001`, `UC-STU-001`.

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

### API-STU-005 — `GET /api/v1/catalog/sample-lessons/{lessonId}`

- **Nguồn contract:** `04_DAC_TA_API.md:L130`.
- **Actor/quyền:** Public.
- **Input/validation → output:** UUID → sanitized sample blocks/resources.
- **Xử lý và dữ liệu:** Predicate lesson sample flag + published version; signed media URL <=10 phút; no unsafe HTML.
- **Vận hành:** CDN metadata 60s.
- **Lỗi đặc thù:** `SAMPLE_NOT_AVAILABLE`.
- **Màn hình/consumer:** `SCR-STU-006`.
- **Capability/use case:** `CAP-STU-001`, `UC-STU-001`.

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

### API-STU-006 — `GET /api/v1/metadata/skills`

- **Nguồn contract:** `04_DAC_TA_API.md:L131`.
- **Actor/quyền:** Public.
- **Input/validation → output:** `q`, page → canonical active skills.
- **Xử lý và dữ liệu:** R skills FTS/trigram, sort normalized name.
- **Vận hành:** Cache 10 phút.
- **Lỗi đặc thù:** `INVALID_FILTER`.
- **Màn hình/consumer:** Nhiều màn.
- **Capability/use case:** `CAP-STU-001`, `UC-STU-001`.

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

1. 6 folder API DD tương ứng.
2. `PLAN_RESULT.md` cập nhật trạng thái từng API.
3. `VERIFICATION_REPORT.md` cho scope của plan.
4. `OPEN_QUESTIONS.md` nếu còn ảnh hưởng contract/DB/security/transaction.
5. `BUSINESS_CODE_DELTA.md` chỉ khi có code mới được nguồn approved xác nhận.

## 9. Điều kiện dừng

- Dừng API cụ thể nếu không xác định được request/response contract, target DB table/column, permission, transaction hoặc business code bắt buộc.
- Không được báo `DONE` cho API còn `SOURCE_REQUIRED`, conflict chưa quyết định hoặc validation chưa đạt.

Quay lại: [00_API_DD_PLAN_INDEX.md](../00_API_DD_PLAN_INDEX.md)
