# PLAN 46 — Payment — Entitlement, refund và reconciliation

## 1. Thông tin kế hoạch

| Thuộc tính | Giá trị |
|---|---|
| Plan ID | `PLAN-46` |
| API trong phạm vi | `API-PAY-005`, `API-PAY-006`, `API-PAY-007`, `API-PAY-008`, `API-PAY-009` |
| Số API | 5 |
| Read-only / Mutation | 2 / 3 |
| Khối lượng lõi | 40 file template trước khi duplicate DB Mapping |
| Mức rủi ro | Rất cao |
| Trạng thái plan | `READY — SOURCE-GROUNDED`; API có source gap phải giữ Draft |

## 2. Mục tiêu và nghiệp vụ

Tạo DD cho entitlement read, refund request/approval và payment reconciliation.

**Luồng nghiệp vụ trọng tâm:** Entitlement đọc ledger-derived balance; refund maker-checker; approval/provider action; reconciliation compares provider/order/ledger and applies idempotent correction.

**Điểm cần khóa:** Append-only ledger, no negative balance, refund/chargeback do not rewrite SETTLED order.

**Dependency:** Plan 45/49.

## 3. Phạm vi

**In-scope**

- `API-PAY-005` — `GET /api/v1/billing/entitlements`.
- `API-PAY-006` — `POST /api/v1/billing/refund-requests`.
- `API-PAY-007` — `POST /api/v1/admin/refunds/{refundId}/approve`.
- `API-PAY-008` — `GET /api/v1/admin/payments/reconciliation`.
- `API-PAY-009` — `POST /api/v1/admin/payments/{orderId}/reconcile`.

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

- `01_TONG_QUAN_DU_AN.md:L776` — `CAP-WRK-009` / `UC-WRK-009`; rules ``BR-WRK-017`, `BR-PAY-006`, `BR-AIX-002–003`, `PERM-WRK-060``; diagrams ``AC-WRK-001`, `AC-PAY-001`, `SEQ-WRK-001`, `SEQ-PAY-001``; data ``CLS-WRK-001`, `CLS-PAY-001`, `CLS-AIX-001`; `TBL-WRK-010–011`, `TBL-PAY-010–013``; screens ``SCR-WRK-013`, `SCR-WRK-022`, `SCR-WRK-034`, `SCR-WRK-043``; test ``TC-WRK-009``.
- `01_TONG_QUAN_DU_AN.md:L782` — `CAP-PAY-002` / `UC-PAY-002`; rules ``BR-PAY-004–007`, `BR-OPS-003`, `NFR-OPS-006``; diagrams ``AC-PAY-001`, `SEQ-PAY-001``; data ``CLS-PAY-001`; `TBL-PAY-003`, `TBL-PAY-005–006`, `TBL-PAY-010–011``; screens ``SCR-WRK-022`, `SCR-WRK-043`; webhook là `SYSTEM``; test ``TC-PAY-002``.
- `01_TONG_QUAN_DU_AN.md:L783` — `CAP-PAY-003` / `UC-PAY-003`; rules ``BR-PAY-008–010`, `PERM-PAY-001–003`, `BR-OPS-001–002``; diagrams ``AC-PAY-001`, `SEQ-PAY-002``; data ``CLS-PAY-001`; `TBL-PAY-007–011``; screens ``SCR-WRK-022`, `SCR-WRK-043`, `SCR-OPS-019–020``; test ``TC-PAY-003``.

**Diagram/Class cần đọc toàn bộ section**

- `AC-WRK-001` — `02_BIEU_DO_HE_THONG.md:L548` — AC-WRK-001 — Candidate privacy, search, invitation và opt-out.
- `AC-PAY-001` — `02_BIEU_DO_HE_THONG.md:L729` — AC-PAY-001 — Checkout, callback, entitlement và reversal.
- `SEQ-WRK-001` — `02_BIEU_DO_HE_THONG.md:L2080` — SEQ-WRK-001 — Candidate opt-in/search, sponsored label và opt-out SLA.
- `SEQ-PAY-001` — `02_BIEU_DO_HE_THONG.md:L2415` — SEQ-PAY-001 — Checkout VNPAY/MoMo, IPN/webhook và entitlement once.
- `SEQ-PAY-002` — `02_BIEU_DO_HE_THONG.md:L2463` — SEQ-PAY-002 — Refund, chargeback và reconciliation.
- `CLS-WRK-001` — `02_BIEU_DO_HE_THONG.md:L1266` — CLS-WRK-001 — Candidate, tenant, job, application và ATS snapshots.
- `CLS-PAY-001` — `02_BIEU_DO_HE_THONG.md:L1501` — CLS-PAY-001 — Order, provider event, ledger, entitlement và promotion.
- `CLS-AIX-001` — `02_BIEU_DO_HE_THONG.md:L1584` — CLS-AIX-001 — AI job, provenance, review và human-applied revision.

**Bảng dữ liệu liên quan theo traceability**

- `TBL-WRK-010` — `cvs` — `03_THIET_KE_CO_SO_DU_LIEU.md:L768 `.
- `TBL-WRK-011` — `cv_versions` — `03_THIET_KE_CO_SO_DU_LIEU.md:L775 `.
- `TBL-PAY-010` — `entitlements` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1235 `.
- `TBL-PAY-011` — `credit_ledger_entries` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1242 `.
- `TBL-PAY-012` — `promotion_campaigns` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1249 `.
- `TBL-PAY-013` — `sponsored_placements` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1256 `.
- `TBL-PAY-003` — `orders` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1186 `.
- `TBL-PAY-005` — `payment_attempts` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1200 `.
- `TBL-PAY-006` — `payment_webhook_events` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1207 `.
- `TBL-PAY-007` — `payment_reconciliations` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1214 `.
- `TBL-PAY-008` — `refunds` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1221 `.
- `TBL-PAY-009` — `chargebacks` — `03_THIET_KE_CO_SO_DU_LIEU.md:L1228 `.

**Screen và acceptance**

- Screens: `SCR-WRK-013`, `SCR-WRK-022`, `SCR-WRK-034`, `SCR-WRK-043`, `SCR-OPS-019`, `SCR-OPS-020`.
- Acceptance: `TC-WRK-009`, `TC-PAY-002`, `TC-PAY-003`.

**Rule/permission/NFR IDs phải reconcile**

- `BR-WRK-017` — `01_TONG_QUAN_DU_AN.md:L389` — Sponsored profile/job luôn có nhãn, slot/rank riêng và trường `organicScore` không đổi. Payment không được tăng match score, ATS score hoặc quyền xem field riêng tư..
- `BR-PAY-006` — `01_TONG_QUAN_DU_AN.md:L425` — Chỉ `SETTLED` tạo entitlement/credit ledger đúng một lần trong cùng transaction. Entitlement không được âm; mọi consume/refund/expire là ledger append-only..
- `BR-AIX-002` — `01_TONG_QUAN_DU_AN.md:L436` — AI chỉ tạo CV/JD draft, writing suggestion, match explanation và shortlist suggestion. Output không tự publish, gửi, apply, thay đổi ATS, reject, offer hoặc hire..
- `BR-AIX-003` — `01_TONG_QUAN_DU_AN.md:L437` — Người dùng phải nhìn thấy nhãn AI, review và chủ động accept/edit/reject. Bản accept lưu nội dung người dùng xác nhận, không giả định AI đúng..
- `PERM-WRK-060` — `01_TONG_QUAN_DU_AN.md:L179` — `work.promotions.manage` — Enterprise Owner/Admin có entitlement.
- `BR-PAY-004` — `01_TONG_QUAN_DU_AN.md:L423` — Webhook/IPN đã xác thực chữ ký và đối chiếu merchant/order/amount/currency là nguồn xác nhận. Return URL không được cấp entitlement hoặc tự đánh dấu thanh toán thành công..
- `BR-PAY-005` — `01_TONG_QUAN_DU_AN.md:L424` — Callback duplicate/out-of-order được lưu raw payload đã bảo vệ, xử lý idempotent và theo state precedence; late failure không hạ `SETTLED`. Amount/order mismatch vào review, không cấp quyền lợi..
- `BR-PAY-007` — `01_TONG_QUAN_DU_AN.md:L426` — Order chưa xác nhận quá thời hạn provider chuyển `EXPIRED`. `CANCELLED` chỉ được commit khi provider/chưa khởi tạo attempt xác nhận chưa thu tiền; verified success thắng trong cùng row lock. Callback success hợp lệ đến muộn được reconciliation xử lý và không cấp trùng..
- `BR-OPS-003` — `01_TONG_QUAN_DU_AN.md:L450` — Notification và side effect ngoài transaction được tạo qua outbox với dedupe key. Retry exponential có giới hạn; hết retry vào DLQ và cảnh báo..
- `NFR-OPS-006` — `01_TONG_QUAN_DU_AN.md:L653` — Outbox/event projection p95 ≤ 60 giây khi bình thường; evidence export p95 ≤ 2 phút. Backlog, oldest age, retry và DLQ có alert..
- `BR-PAY-008` — `01_TONG_QUAN_DU_AN.md:L427` — Refund chỉ do Finance Operator khởi tạo về provider gốc, không vượt settled amount trừ các refund trước. Hệ thống chỉ revoke phần entitlement chưa tiêu tương ứng; yêu cầu vượt giá trị chưa tiêu cần phê duyệt ngoại lệ và ghi debt/risk flag..
- `BR-PAY-009` — `01_TONG_QUAN_DU_AN.md:L428` — Provider-confirmed chargeback đóng băng entitlement còn lại, đặt risk flag và tạo case Finance. Quyền lợi đã tiêu không bị xóa lịch sử; debt được theo dõi, không tự trừ order khác..
- `BR-PAY-010` — `01_TONG_QUAN_DU_AN.md:L429` — Reconciliation chạy tự động hằng ngày và on-demand; sai lệch có severity, owner và audit. Không operator nào được sửa raw webhook hoặc ledger đã ghi..
- `PERM-PAY-001` — `01_TONG_QUAN_DU_AN.md:L193` — `billing.reconciliation.read` — Finance Operator.
- `PERM-PAY-002` — `01_TONG_QUAN_DU_AN.md:L194` — `billing.refunds.approve` — Finance Operator có maker/checker separation.
- `PERM-PAY-003` — `01_TONG_QUAN_DU_AN.md:L195` — `billing.reconciliation.execute` — Finance Operator được ủy quyền.
- `BR-OPS-001` — `01_TONG_QUAN_DU_AN.md:L448` — Audit/security/payment webhook/ledger/application history/evidence snapshot/AI review/outbox là append-only; không cascade delete làm mất lịch sử..
- `BR-OPS-002` — `01_TONG_QUAN_DU_AN.md:L449` — Audit chứa actor, effective role/tenant, action, resource, before/after đã redact, reason, IP/device tối thiểu, trace ID và thời điểm UTC; không chứa secret/token/raw password..

## 5. Chi tiết từng API

### API-PAY-005 — `GET /api/v1/billing/entitlements`

- **Nguồn contract:** `04_DAC_TA_API.md:L379`.
- **Actor/quyền:** Owner/tenant billing member.
- **Input/validation → output:** Page/type/status → balances/grants/expiry.
- **Xử lý và dữ liệu:** Query subject/tenant/status/expiry; ledger-derived balance.
- **Vận hành:** Private.
- **Lỗi đặc thù:** —.
- **Màn hình/consumer:** `SCR-WRK-022`, `SCR-WRK-043`.
- **Capability/use case:** `CAP-WRK-009`, `UC-WRK-009`, `CAP-PAY-002`, `UC-PAY-002`.

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

### API-PAY-006 — `POST /api/v1/billing/refund-requests`

- **Nguồn contract:** `04_DAC_TA_API.md:L380`.
- **Actor/quyền:** Purchaser/tenant billing member.
- **Input/validation → output:** Order, amount <= refundable, reason → request.
- **Xử lý và dữ liệu:** TX L settled order; validate consumed entitlement policy; create PENDING request, no immediate balance mutation.
- **Vận hành:** Idempotency; high-risk audit/finance queue.
- **Lỗi đặc thù:** `ORDER_NOT_REFUNDABLE`, `REFUND_AMOUNT_INVALID`, `ENTITLEMENT_ALREADY_CONSUMED`.
- **Màn hình/consumer:** `SCR-WRK-022`, `SCR-WRK-043`.
- **Capability/use case:** `CAP-WRK-009`, `UC-WRK-009`, `CAP-PAY-003`, `UC-PAY-003`.

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

### API-PAY-007 — `POST /api/v1/admin/refunds/{refundId}/approve`

- **Nguồn contract:** `04_DAC_TA_API.md:L381`.
- **Actor/quyền:** `PERM-PAY-002` + recent MFA, not requester.
- **Input/validation → output:** Amount/reason/If-Match → processing refund.
- **Xử lý và dữ liệu:** TX separation-of-duties; reserve refundable amount; append decision; provider adapter after commit.
- **Vận hành:** Idempotency required; immutable finance audit.
- **Lỗi đặc thù:** `SELF_APPROVAL_FORBIDDEN`, `REFUND_CONFLICT`, `VERSION_CONFLICT`.
- **Màn hình/consumer:** `SCR-OPS-020`.
- **Capability/use case:** `CAP-WRK-009`, `UC-WRK-009`, `CAP-PAY-003`, `UC-PAY-003`.

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

### API-PAY-008 — `GET /api/v1/admin/payments/reconciliation`

- **Nguồn contract:** `04_DAC_TA_API.md:L382`.
- **Actor/quyền:** `PERM-PAY-001` + MFA.
- **Input/validation → output:** Page/provider/date/state → mismatch queue.
- **Xử lý và dữ liệu:** Join provider events/orders/attempts/ledger by provider order key indexes.
- **Vận hành:** No cache; every export audit.
- **Lỗi đặc thù:** `DATE_RANGE_TOO_LARGE`.
- **Màn hình/consumer:** `SCR-OPS-019`.
- **Capability/use case:** `CAP-WRK-009`, `UC-WRK-009`, `CAP-PAY-003`, `UC-PAY-003`.

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

### API-PAY-009 — `POST /api/v1/admin/payments/{orderId}/reconcile`

- **Nguồn contract:** `04_DAC_TA_API.md:L383`.
- **Actor/quyền:** `PERM-PAY-003` + MFA.
- **Input/validation → output:** Provider evidence ref, action REQUERY/MARK_REVIEWED, reason → case.
- **Xử lý và dữ liệu:** Never manual SETTLED without verified provider record; append reconciliation run/result.
- **Vận hành:** Idempotency; finance audit.
- **Lỗi đặc thù:** `PROVIDER_EVIDENCE_REQUIRED`, `ORDER_ALREADY_FINAL`.
- **Màn hình/consumer:** `SCR-OPS-019`.
- **Capability/use case:** `CAP-WRK-009`, `UC-WRK-009`, `CAP-PAY-003`, `UC-PAY-003`.

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
