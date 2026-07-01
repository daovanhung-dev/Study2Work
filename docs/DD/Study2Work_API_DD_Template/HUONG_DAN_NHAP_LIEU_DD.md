# Hướng dẫn nhập liệu API Detail Design (DD) – Study2Work

> **Mục tiêu:** hướng dẫn điền đầy đủ bộ tài liệu DD cho **một API**, để Product/BA, Backend, Frontend/Mobile, QA, DevOps và AI coding cùng hiểu một API theo cùng một cách.  
> **Phạm vi:** áp dụng cho các thư mục `01_Overview` đến `06_Error` trong template.  
> **Đầu ra mong đợi:** sau khi điền xong, đội phát triển có thể triển khai API, tích hợp client, viết test, theo dõi vận hành mà không tự suy đoán business rule, quyền, dữ liệu, lỗi hoặc behavior khi cạnh tranh dữ liệu.

---

## 1. Nguyên tắc nhập liệu bắt buộc

1. **Một thư mục DD chỉ mô tả một API operation.** Không gom `create + update + delete` vào một bộ DD.
2. **Điền dữ liệu thật, không giữ placeholder.** Trước khi `Approved`, không được còn `{{...}}`, `TBD`, `TODO` không có owner và deadline.
3. **Không mô tả bằng câu chung chung.**
   - Không tốt: `Student có quyền submit bài.`
   - Đúng: `Student chỉ được tạo submission cho assignment đang ACTIVE và learnerId của enrollment phải trùng actorUserId trong JWT.`
4. **Phân biệt contract và implementation.** DD phải chỉ rõ behavior bắt buộc; tên class/table/repository chỉ ghi khi đã được xác nhận bởi domain model/ERD/architecture.
5. **Mọi thông tin client nhìn thấy phải nhất quán giữa Request, Response và Error.** HTTP status, `businessCode`, field name và message không được mâu thuẫn.
6. **Không đưa secret hoặc dữ liệu nhạy cảm vào tài liệu.** Không ghi password thật, JWT thật, API key, refresh token, OTP, raw CV, email/phone thật của người dùng.
7. **Dùng thời gian UTC trong metadata, log và ví dụ timestamp.** Format: `YYYY-MM-DDTHH:mm:ssZ`.
8. **JSON dùng `camelCase`; database dùng `snake_case`; enum dùng `UPPER_SNAKE_CASE`.**
9. **Mọi mutation phải có mô tả authorization, transaction, concurrency, audit và error mapping.**
10. **Không tự tạo database field/bảng/rule.** Nếu chưa quyết định, ghi Open Item trong `02_History/History.md`, nêu owner, tác động và ngày cần quyết định.

---

## 2. Chuẩn bị dữ liệu trước khi điền

Thu thập tối thiểu các thông tin sau trước khi tạo DD:

| Nhóm thông tin | Cần xác định | Nguồn tham chiếu ưu tiên |
|---|---|---|
| Nghiệp vụ | Mục đích, actor, trigger, success condition, out-of-scope | Requirement, Use Case, Activity Diagram, Product ticket |
| API contract | Method, endpoint, auth, request/response fields, pagination, idempotency | Product flow, UI flow, OpenAPI draft |
| Domain | Aggregate owner, state, invariant, business rules | Domain Model, Business Code |
| Dữ liệu | Table, column, relation, index, unique constraint, soft delete | ERD, migration, database design |
| Quyền | Role, permission, ownership/relationship condition | Permission matrix, Use Case |
| Vận hành | Timeout, cache, rate limit, logging, metrics, event, retry | Architecture guide, DevOps/SRE conventions |
| Kiểm thử | Happy case, boundary, invalid input, permission, conflict, dependency failure | QA strategy, acceptance criteria |

### 2.1. Trình tự điền khuyến nghị

```text
1. 01_Overview     → chốt định danh, mục tiêu, quyền, phạm vi
2. 03_Request      → chốt input contract và validation
3. 04_Response     → chốt output contract, empty/success/error behavior
4. 05_DataMapping  → mô tả runtime flow, DB, rule, transaction, event
5. 06_Error        → chuẩn hóa toàn bộ lỗi và client recovery
6. 02_History      → tạo version ban đầu, review/approval trail
7. API_DD_CHECKLIST → self-review trước khi gửi review
```

> Không nên điền DataMapping trước khi Request/Response chưa chốt. Không nên `Approved` trước khi Error và checklist hoàn tất.

---

## 3. Quy ước định danh khi nhập liệu

### 3.1. API code và document ID

| Loại | Format | Ví dụ |
|---|---|---|
| API business code | `<MODULE>-<ACTION>-<NNN>` | `LEARN-ASSIGNMENT-SUBMIT-001` |
| Document ID | `DD-API-<MODULE>-<ACTION>-<NNN>` | `DD-API-LEARN-ASSIGNMENT-SUBMIT-001` |
| Business rule | `BR-<MODULE>-<NNN>` | `BR-LEARN-014` |
| Query ID | `Q-<NNN>` | `Q-01` |
| External call | `EXT-<NNN>` | `EXT-01` |
| Change record | `CHG-<NNN>` | `CHG-001` |
| Test case/fixture | `<API_CODE>-<TYPE><NN>` | `LEARN-ASSIGNMENT-SUBMIT-001-E03` |

### 3.2. Version

| Tình huống | Document/API version | Ví dụ |
|---|---|---|
| Tạo DD mới | `1.0.0` | Initial approved version |
| Sửa typo/link, không đổi behavior | tăng patch | `1.0.1` |
| Thêm optional field hoặc behavior tương thích | tăng minor | `1.1.0` |
| Xóa/đổi required field, endpoint, HTTP semantic hoặc error semantic | tăng major | `2.0.0` |

### 3.3. Field semantics

| Giá trị | Ý nghĩa cần ghi rõ trong DD |
|---|---|
| Key không xuất hiện | Client không gửi field; server có thể reject hoặc áp dụng default. |
| `null` | Client gửi rõ không có giá trị; chỉ hợp lệ khi field `Nullable = Yes`. |
| `""` | Chuỗi rỗng; không mặc định tương đương `null`. |
| `[]` | Danh sách rỗng hợp lệ hoặc không hợp lệ tùy rule. |
| `{}` | Object rỗng; chỉ hợp lệ khi nested schema cho phép. |
| Server-generated | Client không được gửi hoặc giá trị gửi bị bỏ qua/reject; ví dụ `createdAt`, `actorUserId`. |

---

# 4. Hướng dẫn nhập `01_Overview/Overview.md`

## 4.1. Mục tiêu của Overview

Overview trả lời trong một lần đọc: **API là gì, vì sao tồn tại, ai gọi, điều kiện gọi, ảnh hưởng gì, thành công thế nào, giới hạn ở đâu, phụ thuộc vào thành phần nào**.

## 4.2. Cách điền từng phần

### A. Document metadata

| Field | Cách nhập | Ví dụ |
|---|---|---|
| `API document ID` | Dùng đúng convention document ID. | `DD-API-LEARN-ASSIGNMENT-SUBMIT-001` |
| `API business code` | Một code ổn định, không dùng tên UI. | `LEARN-ASSIGNMENT-SUBMIT-001` |
| `API name` | Động từ + business artifact + mục đích. | `Submit assignment submission` |
| `Module` | Module nghiệp vụ sở hữu API. | `Learning & Practice` |
| `Bounded context` | Context sở hữu rule/dữ liệu chính. | `Practice & Assessment` |
| `Owner team` | Team chịu trách nhiệm phát triển/vận hành. | `Learning Platform Team` |
| `Document status` | `Draft`, `In Review`, `Approved`, `Deprecated`. | `Draft` |
| `Created/Last updated` | UTC; không dùng ngày tương đối. | `2026-07-01T12:00:00Z` |
| `Related release / epic / ticket` | Ticket thật hoặc ID được team thống nhất. | `S2W-184` |

### B. API identity and protocol

- **HTTP method:** chọn theo semantic, không theo thói quen.
  - `GET`: đọc, không tạo side effect.
  - `POST`: tạo resource, command hoặc action không idempotent mặc định.
  - `PUT`: thay thế toàn bộ resource; chỉ dùng nếu semantic này đúng.
  - `PATCH`: cập nhật một phần.
  - `DELETE`: xóa/soft-delete hoặc chuyển state theo đặc tả.
- **Endpoint:** chỉ ghi path, ví dụ `/api/v1/assignments/{assignmentId}/submissions`; không ghi domain hoặc environment secret.
- **Authentication:** ghi chính xác scheme (`Bearer JWT`, `None`, `API key`, `mTLS`).
- **Authorization policy:** phải có tên policy và điều kiện cụ thể, ví dụ `StudentOwnActiveAssignmentPolicy`.
- **Idempotency:** bắt buộc đánh giá cho API create, payment, publish event, upload, gửi email hoặc action có side effect. Nêu header, phạm vi key và TTL khi áp dụng.
- **Rate limit/timeout:** ghi số đo được, ví dụ `30 requests/minute/user`, `p95 < 500 ms`, không ghi `nhanh` hoặc `hợp lý`.

### C. Business purpose

Viết 3–6 câu, bao gồm:

1. Hành vi nghiệp vụ người dùng muốn hoàn thành.
2. Artifact nghiệp vụ thay đổi/tạo/truy vấn.
3. Lợi ích trong hành trình Study2Work.
4. Màn hình/flow sẽ dùng kết quả.
5. Những việc API không chịu trách nhiệm.

**Ví dụ tốt**

> API cho phép Student nộp bài thực hành cho một assignment đang mở trong lộ trình học được enrollment. Hệ thống tạo hoặc cập nhật assignment submission theo policy nộp bài, lưu thời điểm nộp và trạng thái để Mentor review. Kết quả được dùng tại trang Assignment Detail và Mentor Review Queue. API không chấm điểm tự động, không gửi notification trực tiếp trong transaction và không thay thế workflow review của Mentor.

### D. Actor, precondition, invariant và scope

- **Primary actor:** người chủ động kích hoạt API.
- **Technical caller:** ứng dụng gọi thật, như `web-student`, `mobile-app`, `web-admin`.
- **Precondition:** điều kiện phải đúng trước khi chạy. Mỗi điều kiện phải có component kiểm tra và error code nếu sai.
- **Domain invariant:** quy tắc không bao giờ được vi phạm, ví dụ `submission không được chuyển từ REVIEWED về DRAFT bằng API submit`.
- **Out of scope:** giúp ngăn code creep. Ghi rõ tính năng liên quan nhưng API này không làm.

### E. References, dependencies và data impact

- Link/ID phải trỏ được đến artefact thật trong repository hoặc ticket system.
- `Data impact summary` chỉ là tóm tắt; chi tiết table/column/predicate phải ở DataMapping.
- External dependency phải nêu protocol, timeout, failure policy, data classification; không chỉ ghi tên service.

## 4.3. Quality gate Overview

Overview đủ điều kiện chuyển sang bước tiếp theo khi:

- Một người không tham gia thiết kế vẫn biết chính xác actor, endpoint, success outcome và permission condition.
- Có ít nhất một precondition, authorization condition, postcondition và out-of-scope rõ ràng.
- Không có các từ không đo được: `nhanh`, `đầy đủ`, `cần thiết`, `có quyền`, `nếu hợp lệ` mà không nêu điều kiện.

---

# 5. Hướng dẫn nhập `02_History/History.md`

## 5.1. Khi nào cần thêm history

Thêm một dòng Change log khi thay đổi bất kỳ nội dung nào sau đây:

- Endpoint, HTTP method, header bắt buộc, request/response field.
- Required/nullable/default/enum/validation rule.
- HTTP status, business code, message semantic.
- Role, permission, ownership policy.
- Query, transaction, concurrency, cache, external dependency.
- Business rule, scoring, state transition.
- Data migration, privacy, logging, rate limit, timeout.

Không cần tạo dòng mới cho lỗi format hoàn toàn không ảnh hưởng hiểu biết hoặc behavior, nhưng vẫn cần cập nhật version patch nếu tài liệu đã `Approved`.

## 5.2. Cách điền Change log

| Cột | Cách nhập đúng |
|---|---|
| `Version` | Version sau thay đổi. |
| `Date (UTC)` | Ngày thay đổi tài liệu, không phải ngày dự kiến deploy. |
| `Change type` | Chọn một trong các loại template; không nhập tự do. |
| `Area changed` | Liệt kê file/phần thay đổi, ví dụ `Request, Response, Error`. |
| `Summary` | Một câu mô tả thay đổi cụ thể; có field/code khi cần. |
| `Reason / ticket` | Ticket, incident hoặc lý do nghiệp vụ có thể truy vết. |
| `Breaking?` | `Yes` nếu client cũ có thể lỗi/đổi behavior. |
| `Client action` | Việc client cần làm; không ghi `N/A` khi breaking. |
| `DB / migration impact` | Nêu migration, backfill, dual-read/write hoặc `N/A`. |

## 5.3. Quy tắc breaking change

Một thay đổi được xem là breaking khi:

- Thêm request field bắt buộc.
- Xóa/đổi tên/đổi kiểu/đổi semantic response field.
- Đổi default làm client nhận kết quả khác.
- Đổi HTTP status hoặc business code mà client đang xử lý.
- Đổi endpoint/method, authorization, pagination format hoặc sort default quan trọng.

Với breaking change, bắt buộc điền `Change detail record`, `Deprecation and migration plan` và deployment order.

---

# 6. Hướng dẫn nhập `03_Request/Request.md`

## 6.1. Mục tiêu của Request

Request là **hợp đồng input đầy đủ**, không phải chỉ một JSON sample. Người đọc phải phân biệt được path/query/header/cookie/body, field bắt buộc, `null`, default, validation, transform và dữ liệu server tự sinh.

## 6.2. Request summary

Điền cho toàn bộ API:

- `Request content type`: dùng `application/json; charset=utf-8` trừ upload/download/multipart.
- `Max request size`: ghi rõ đơn vị, ví dụ `1 MB JSON body`, `10 MB/file`.
- `DTO/schema`: ghi tên contract dự kiến, ví dụ `SubmitAssignmentRequestDto`.
- `Caller(s)`: chỉ rõ app/service được phép gọi.

## 6.3. URL, query, header, cookie

### Path parameter

- Dùng cho identity của resource trên URL, ví dụ `assignmentId`.
- Với UUID, ghi exact format `UUID v4 string` nếu hệ thống yêu cầu v4.
- Nêu behavior khi resource không tồn tại ở Error/DataMapping, không chỉ format error.

### Query parameter

- Chỉ dùng cho filter, sort, pagination, mode hoặc optional behavior.
- Nêu default chính xác, allowable values và canonicalization.
- Với list API, nêu toàn bộ: `page`, `pageSize`, `cursor`, `sortBy`, `sortDirection`, filter; không để client tự đoán.

### Header

| Header | Khi dùng | Lưu ý bắt buộc |
|---|---|---|
| `Authorization` | API authenticated | Mask hoàn toàn trong log. |
| `Idempotency-Key` | Mutation dễ bị gửi lặp | Nêu TTL, scope và behavior cùng key + cùng/different payload. |
| `If-Match` | Update cần chống stale data | Nêu ETag/version source và response khi mismatch. |
| `X-Request-Id` | Correlation từ client | Server vẫn phải tạo/propagate `traceId`. |
| `X-Timezone` | Timezone hiển thị/interpret input | Server lưu UTC; không dùng làm auth/data ownership. |

### Cookie

Chỉ tạo phần cookie khi API thật sự sử dụng cookie. Với auth cookie, bắt buộc nêu `HttpOnly`, `Secure`, `SameSite`, rotate/expiry và CSRF policy ở nơi phù hợp.

## 6.4. Field dictionary

Mỗi field và nested field phải có một dòng. Với array, phải mô tả cả `items[]` và từng field trong item.

| Thuộc tính | Cách điền |
|---|---|
| `Logical field` | Tên mang ý nghĩa nghiệp vụ, ví dụ `submissionContent`. |
| `JSON path` | Path thực trên payload, ví dụ `attachments[].fileId`. |
| `Type` | Kiểu transport chính xác: `string`, `integer`, `number`, `boolean`, `array<object>`, `object`, `null` khi được phép. |
| `Required` | Key có bắt buộc phải xuất hiện không. |
| `Nullable` | Value có thể là `null` không; không suy ra từ Required. |
| `Default` | Giá trị server áp dụng khi key không có; ghi `N/A` nếu không có. |
| `Format / constraint` | UUID, ISO-8601, regex, `minLength`, `maxLength`, min/max, maxItems. |
| `Enum / allowed` | Liệt kê toàn bộ allowed values hoặc reference enum catalog. |
| `Source` | `Body`, `Path`, `Query`, `Header`, `JWT claim`, server-generated. |
| `Classification` | `Public`, `Internal`, `PII`, `Sensitive`, `Credential`, `Token`. |
| `Example` | Giá trị giả lập nhưng realistic, không chứa secret thật. |

### Ví dụ field dictionary tốt

| Logical field | JSON path | Type | Required | Nullable | Default | Constraint | Source | Classification | Example |
|---|---|---:|---:|---:|---|---|---|---|---|
| Assignment identifier | `assignmentId` | string | Y | N | N/A | UUID | Path | Internal | `6ed8ea6e-3a6a-4eae-9c78-6dc9c2a0c501` |
| Submission content | `content` | string | N | N | `""` | maxLength 20,000; sanitized Markdown | Body | Internal | `# API Design\nI completed section 1.` |
| Attachment ID | `attachments[].fileId` | string | Y | N | N/A | UUID; maxItems 10 | Body | Internal | `b4b0e1c3-6f70-4a0e-8bf5-16259a7f4319` |
| Submit mode | `submitMode` | string | Y | N | N/A | `DRAFT`, `SUBMIT` | Body | Internal | `SUBMIT` |

## 6.5. Validation và transform

Tách ba lớp validation:

| Lớp | Ví dụ | Error phù hợp |
|---|---|---|
| Syntax/DTO | UUID sai, body thiếu field required, string vượt max length | `400` hoặc `422` validation error |
| Cross-field | `submitMode=SUBMIT` yêu cầu ít nhất content hoặc attachment | `422` validation error |
| Business validation | Assignment đóng, user không enrollment, đã vượt lượt nộp | `403`, `404`, `409` hoặc business error tùy policy |

Transform phải ghi trước khi dùng dữ liệu: `trim`, lowercase, normalize Unicode, parse timezone, sanitize HTML/Markdown, deduplicate array, clamp pageSize. Không tự động transform các field như password/token trừ khi policy yêu cầu.

## 6.6. Request examples

Mỗi API nên có tối thiểu:

1. **Happy request:** hợp lệ, đầy đủ header/body.
2. **Minimal valid request:** chỉ field bắt buộc và default behavior.
3. **Representative invalid request:** ít nhất một case boundary/format/cross-field.
4. **cURL/HTTP example:** có method, URL, header và body; token luôn redacted.

---

# 7. Hướng dẫn nhập `04_Response/Response.md`

## 7.1. Mục tiêu của Response

Response mô tả tất cả kết quả client có thể nhận: thành công, created, no content, empty list, async accepted, validation, auth, permission, not found, conflict, rate limit, dependency failure và internal error khi áp dụng.

## 7.2. Response matrix phải điền trước

Mỗi outcome phải có một dòng trong response matrix:

| Outcome | HTTP | Khi dùng |
|---|---:|---|
| Success object | `200` | Query/action thành công và có payload. |
| Created | `201` | Tạo resource mới; có thể kèm `Location`. |
| No content | `204` | Thành công không có body; dùng có chủ đích. |
| Empty collection | `200` + `data: []` | Query hợp lệ nhưng không có record match. |
| Async accepted | `202` | Request được nhận nhưng kết quả chưa hoàn thành. |
| Validation | `400`/`422` | Input syntax/cross-field không hợp lệ. |
| Unauthenticated | `401` | Missing/invalid/expired auth. |
| Forbidden | `403` | Actor xác thực nhưng không đủ quyền. |
| Not found | `404` | Resource không tồn tại hoặc không visible theo policy. |
| Conflict/state | `409`/`412` | Duplicate, stale update, invalid state, precondition failed. |
| Rate limit | `429` | Vượt policy request. |
| Dependency/system | `502`/`503`/`504`/`500` | Lỗi dependency hoặc lỗi nội bộ đã được mask. |

## 7.3. Response envelope

Các field envelope phải nhất quán:

| Field | Quy tắc |
|---|---|
| `businessCode` | Code ổn định; không dùng message làm code. |
| `message` | Safe, dễ hiểu, không lộ SQL/stack trace/PII. |
| `timestamp` | UTC ISO-8601 do server sinh. |
| `traceId` | Có ở mọi response application; có thể map `X-Trace-Id`. |
| `data` | Object, array hoặc `null` theo scenario; phải mô tả semantic. |
| `pagination` | Chỉ có cho list/search API theo policy rõ ràng. |
| `errors` | Chỉ dùng với error payload; mỗi field error phải map được về request field/rule. |

## 7.4. Response field dictionary

Mỗi field trả về phải mô tả:

- JSON path và type.
- Nullable/empty policy.
- Source (`table column`, `derived`, `snapshot`, `external`, `server-generated`).
- Visibility policy: role nào nhận được field nào.
- Transform/mask: ví dụ email masking, avatar URL signing, timezone conversion.
- Example realistic.

Không trả toàn bộ database model vì tiện. Chỉ trả dữ liệu UI/consumer cần và được phép nhìn thấy.

## 7.5. Empty, not found và null

| Tình huống | Cách trả khuyến nghị |
|---|---|
| List query không có result | `200`, `data: []`, pagination total = 0. |
| Read by ID không tồn tại | `404`, not found business code. |
| Optional nested relation không có | Field `null` nếu schema quy định nullable. |
| Optional list relation không có item | Field `[]`, không dùng `null` trừ khi contract quy định khác. |
| Action thành công không có payload | `204` hoặc `200` với envelope theo contract; không dùng lẫn lộn. |

## 7.6. Pagination

Chọn **một** kiểu cho mỗi endpoint:

- `page/pageSize`: cần `page`, `pageSize`, `totalItems`, `totalPages`.
- `cursor`: cần `nextCursor`, `previousCursor` (nếu hỗ trợ), `hasNextPage`, `pageSize`.

Nêu sort default, sort field whitelist, cap page size và behavior khi cursor/page invalid.

---

# 8. Hướng dẫn nhập `05_DataMapping/DataMapping.md`

## 8.1. Mục tiêu của DataMapping

Đây là phần chi tiết nhất. Người implement phải biết từ request đến response:

```text
Input source → parse/normalize → authenticate → authorize → load data → apply rule
→ query/mutate DB → transaction/lock → audit/outbox → commit → cache/event/notification
→ response mapping → log/metric/trace
```

## 8.2. Runtime metadata và invariant

Điền rõ:

- `Controller / handler`, `Application service / use case`, `Aggregate / domain owner` dự kiến.
- Transaction type: read-only, required, requires new, async saga.
- Consistency: strong/eventual/read-your-writes.
- Concurrency model: unique constraint, optimistic lock, row lock, idempotency, hoặc `N/A` có lý do.
- Invariant phải được đánh số `INV-xx` và map sang error code cụ thể.

## 8.3. Runtime variable register

Mỗi biến ảnh hưởng logic phải có nguồn và policy.

| Variable | Source | Ví dụ |
|---|---|---|
| `actorUserId` | JWT `sub` claim sau khi verify | Không được lấy từ body. |
| `assignmentId` | Path parameter đã parse UUID | Không tự build từ client string. |
| `normalizedContent` | `body.content` sau trim/sanitize | Ghi exact transform. |
| `nowUtc` | Server clock | Dùng cho audit/timestamp/state time. |
| `traceId` | Gateway header hoặc server generator | Propagate xuyên log/event/external call. |
| `idempotencyKey` | Header | Chỉ dùng với scope/TTL quy định. |

Với mỗi biến sensitive/PII/credential, bắt buộc có `log/masking policy`.

## 8.4. Main flow

Mỗi bước phải có đủ: component, input, process, output, DB/external interaction, error mapping, transaction boundary.

**Mẫu bước tốt**

| Step | Component | Input | Process | Output | Failure mapping |
|---:|---|---|---|---|---|
| 6 | `AssignmentRepository` | `assignmentId` | Load active assignment, exclude `deleted_at IS NOT NULL`. | Assignment row or none. | `404 LEARN-ASSIGNMENT-NOT_FOUND-001` |
| 7 | `SubmissionPolicy` | assignment, enrollment, nowUtc | Verify assignment accepts submission and actor owns enrollment. | Allowed state. | `403/409` mapped code |
| 8 | `SubmissionRepository` | normalized payload, actorUserId | Insert/update submission with unique rule and version. | Persisted submission. | conflict/internal mapping |

Không được chỉ ghi: `Kiểm tra dữ liệu`, `Lưu database`, `Gửi notification`.

## 8.5. Business rule matrix

Mỗi rule cần có:

| Cột | Ý nghĩa |
|---|---|
| Rule ID | Ví dụ `BR-LEARN-014`. |
| Condition | Boolean/business condition cụ thể. |
| Decision | Cho phép, từ chối, transform, route async. |
| Owner | Aggregate/domain service/policy sở hữu rule. |
| Error code | Code trả về khi reject. |
| Test ID | Case để QA/automation verify. |

## 8.6. Database access mapping

Mỗi database access phải có một dòng riêng, kể cả read phục vụ authorization.

| Nội dung bắt buộc | Ví dụ |
|---|---|
| Repository/query name | `findActiveAssignmentById` |
| Operation | `READ`, `INSERT`, `UPDATE`, `DELETE` |
| Table/column | `assignment.id`, `assignment.status`, `assignment.deleted_at` |
| Predicate | `id = :assignmentId AND deleted_at IS NULL` |
| Expected cardinality | `0..1`, `0..N`, exactly `1` |
| Index/lock/constraint | `idx_assignment_active`, `FOR UPDATE`, unique key |
| Input/output | Input variables and returned projection |
| Error mapping | not found, conflict, foreign key, internal |

Không dùng raw SQL nối string với client input. Pseudocode SQL phải thể hiện parameter binding.

## 8.7. Transaction và concurrency

Bắt buộc phân tích nếu API có ghi dữ liệu hoặc side effect:

- Transaction bắt đầu ở bước nào.
- Những table write nào phải commit/rollback cùng nhau.
- Isolation level/lock/version/unique key nào bảo vệ race condition.
- Không gọi external HTTP lâu bên trong transaction, trừ khi có lý do và compensation rõ ràng.
- Event/notification/cache invalidation sau commit nên dùng outbox/job khi cần delivery tin cậy.

**Câu hỏi phải trả lời:**

1. Hai request giống nhau cùng lúc có tạo trùng không?
2. Hai người update cùng record có ghi đè không?
3. State transition có thể chạy hai lần không?
4. Idempotency key cùng payload và khác payload được xử lý ra sao?
5. Khi event/notification fail sau commit, core transaction có thành công hay rollback?

## 8.8. Cache, external service, AI, event

Chỉ điền các phần áp dụng, nhưng khi có dùng phải đủ chi tiết:

- Cache key, source of truth, TTL, invalidation trigger, failure fallback.
- External service: request mapping, response mapping, timeout, retry, circuit breaker, fallback, data classification, trace propagation.
- AI: prompt input classification, moderation, output review/approval, retention, failure behavior; AI result không tự trở thành source of truth nếu chưa có policy.
- Event/job: event name, payload field, producer, consumer, idempotency key, retry, DLQ, user-visible result.

## 8.9. Response lineage

Mỗi `data.*` response field phải truy ra được nguồn. Ví dụ:

| Response field | Source | Transform | Visibility |
|---|---|---|---|
| `data.id` | `assignment_submission.id` | UUID string | Owner/Mentor/Admin theo policy |
| `data.status` | `assignment_submission.status` | Enum serialize | Owner/Mentor/Admin |
| `data.submittedAt` | `assignment_submission.submitted_at` | UTC ISO-8601 | Owner/Mentor/Admin |
| `data.score` | `review.score` | `null` nếu chưa review | Owner sees only published score |

## 8.10. Observability

Điền các log checkpoint thực sự hữu ích:

- Request received: `traceId`, apiCode, actor/user (nếu được phép), masked request summary.
- Business rejected: ruleId, businessCode, resource ID an toàn.
- Success: duration, outcome, resource ID.
- Error: dependency/error class, duration, traceId; stack trace chỉ internal.

Không log raw password, JWT, refresh token, OTP, API key, raw PII hoặc full sensitive prompt.

---

# 9. Hướng dẫn nhập `06_Error/Error.md`

## 9.1. Mục tiêu của Error

Error thống nhất cách API từ chối request và xử lý lỗi kỹ thuật. Mỗi lỗi phải có ý nghĩa riêng, HTTP semantic đúng, message an toàn, client action, retry policy, log/alert owner và test ID.

## 9.2. Cách đặt business code

```text
<MODULE>-<CATEGORY_OR_BUSINESS_REASON>-<NNN>
```

Ví dụ:

```text
LEARN-VALIDATION-001
LEARN-ASSIGNMENT-NOT_FOUND-001
LEARN-SUBMISSION-STATE-001
LEARN-SUBMISSION-LIMIT-001
SYSTEM-RATE-LIMIT-001
SYSTEM-INTERNAL-001
```

Không dùng một code chung như `LEARN-FAILED-001` cho nhiều lý do không liên quan.

## 9.3. Chọn HTTP status đúng semantic

| HTTP | Dùng khi | Không dùng khi |
|---:|---|---|
| `400` | Payload/header/query malformed hoặc protocol invalid. | Business rule/state conflict. |
| `401` | Chưa authenticated hoặc token invalid/expired. | User đã authenticated nhưng không đủ quyền. |
| `403` | Authenticated nhưng không có role/permission/ownership. | Resource hoàn toàn không tồn tại. |
| `404` | Resource không tồn tại hoặc intentionally hidden theo visibility policy. | List empty hợp lệ. |
| `409` | Duplicate, invalid state, unique/version conflict. | Field syntax error đơn giản. |
| `412` | `If-Match`/precondition header không thỏa. | Không dùng `If-Match`. |
| `422` | Syntax hợp lệ nhưng field/cross-field validation không thỏa. | Gateway/protocol malformed. |
| `429` | Rate limit. | Dependency unavailable. |
| `500` | Unexpected internal error đã mask. | Expected validation/not-found/conflict. |
| `502/503/504` | Dependency bad gateway/unavailable/timeout. | Client input invalid. |

## 9.4. Error catalog

Mỗi dòng error phải điền:

- Trigger nghiệp vụ/kỹ thuật.
- Detection point: DTO, guard, policy, repository, aggregate, external adapter, global exception filter.
- Safe client message.
- `field/resource` nếu applicable.
- Client action: sửa input, login, quay lại list, refresh, retry có backoff, liên hệ support bằng traceId.
- Retry: `Y`, `N`, `Conditional`; nêu điều kiện.
- Severity, log checkpoint, alert owner.
- Test ID.

## 9.5. Error masking

Không trả cho client:

- Stack trace, class name, raw SQL, table/column/constraint name.
- Internal host, port, provider secret, service topology.
- Password, access token, refresh token, OTP.
- Dữ liệu profile của user khác.
- Lý do chi tiết có thể giúp enumerate account khi login/reset password, nếu security policy không cho phép.

## 9.6. Retry policy

| Nhóm lỗi | Retry | Quy tắc |
|---|---|---|
| Validation, permission, not found, invalid state | Không | User phải đổi input/context. |
| Auth expired | Có điều kiện | Refresh token tối đa một lần theo auth policy. |
| Conflict/ETag | Có điều kiện | Refetch rồi user xác nhận retry; không overwrite im lặng. |
| Rate limit | Có | Tôn trọng `Retry-After`. |
| Dependency timeout | Có điều kiện | Exponential backoff + jitter; chỉ khi idempotent/read-only. |
| Internal error | Có điều kiện | Chỉ retry khi request idempotent hoặc có idempotency key. |

---

# 10. Kiểm tra tính nhất quán giữa các file

| Thông tin | Phải giống ở đâu |
|---|---|
| API code, name, method, endpoint | Overview, Request, Response, DataMapping, History |
| Role/permission/ownership | Overview, Request, DataMapping, Error |
| Request field/validation | Request, DataMapping, Error, Response error example |
| Success business code | Overview, Response, DataMapping, Error (nếu catalog success convention) |
| Error HTTP/code/message | Response matrix/example, DataMapping failure branch, Error catalog |
| Table/field/query | Overview data impact summary, DataMapping, ERD/domain reference |
| Transaction/cache/event | Overview high-level, DataMapping, History nếu behavior thay đổi |
| TraceId/logging/metrics | Overview NFR, Response header/envelope, DataMapping, Error |
| Version/status/date | Overview, History, OpenAPI/release note |

---

# 11. Ví dụ rút gọn: `LEARN-ASSIGNMENT-SUBMIT-001`

> Đây là ví dụ minh họa cách điền. Tên entity/table/rule phải được thay bằng tên đã xác nhận trong ERD và Domain Model của dự án trước khi `Approved`.

## 11.1. Overview rút gọn

```text
API code: LEARN-ASSIGNMENT-SUBMIT-001
API name: Submit assignment submission
Method: POST
Endpoint: /api/v1/assignments/{assignmentId}/submissions
Primary actor: Student
Authentication: Bearer JWT
Permission: assignment.submission.create
Authorization: Student phải sở hữu enrollment active của learning path chứa assignment.
Success condition: Submission được persist với status SUBMITTED và emitted event sau commit.
Out of scope: Auto-grading, mentor review, notification synchronous.
```

## 11.2. Request rút gọn

```json
{
  "content": "# My solution\nRepository: https://github.com/example/study2work-assignment",
  "attachments": [
    {
      "fileId": "b4b0e1c3-6f70-4a0e-8bf5-16259a7f4319"
    }
  ],
  "submitMode": "SUBMIT"
}
```

| Field | Rule |
|---|---|
| `assignmentId` | Path UUID, required. |
| `content` | Optional string, max 20,000, sanitized Markdown. |
| `attachments` | Optional array, max 10; mỗi `fileId` phải tồn tại và thuộc actor. |
| `submitMode` | Required enum `DRAFT` hoặc `SUBMIT`. `SUBMIT` yêu cầu content hoặc ít nhất một attachment. |
| `Idempotency-Key` | Required; same key + same normalized payload trả kết quả đầu tiên, same key + different payload trả conflict. |

## 11.3. DataMapping rút gọn

```text
1. Parse assignmentId và body; tạo traceId, nowUtc.
2. Verify Bearer JWT; lấy actorUserId từ claim sub.
3. Validate DTO/cross-field; reject 422 khi submitMode=SUBMIT nhưng content và attachments đều rỗng.
4. Load assignment active by assignmentId; reject 404 khi không có hoặc soft-deleted.
5. Load enrollment của actor cho learning path; reject 403 khi không thuộc enrollment active.
6. Apply BR-LEARN-014: assignment phải ACCEPTING_SUBMISSION tại nowUtc; reject 409 nếu đóng/hết hạn.
7. Verify every fileId belongs to actor and is safe; reject 403/422 theo policy.
8. Trong transaction, create/update assignment_submission; unique/idempotency/version guard chống double submit.
9. Insert audit log và outbox event ASSIGNMENT_SUBMITTED; commit.
10. Post-commit invalidate cache/retry event delivery; map persisted submission vào response.
```

## 11.4. Success response rút gọn

```json
{
  "businessCode": "LEARN-ASSIGNMENT-SUBMIT-SUCCESS",
  "message": "Assignment submitted successfully.",
  "timestamp": "2026-07-01T12:00:00Z",
  "traceId": "7d176f5a-b29c-4cdf-a194-91507a16f5fb",
  "data": {
    "id": "f4878d16-1a0f-4ece-a04c-644ed0ae51d4",
    "assignmentId": "6ed8ea6e-3a6a-4eae-9c78-6dc9c2a0c501",
    "status": "SUBMITTED",
    "submittedAt": "2026-07-01T12:00:00Z"
  }
}
```

## 11.5. Error rút gọn

| Error code | HTTP | Trigger | Client action |
|---|---:|---|---|
| `LEARN-VALIDATION-001` | 422 | `SUBMIT` không có content/attachment. | Bổ sung nội dung hoặc file. |
| `LEARN-ASSIGNMENT-NOT_FOUND-001` | 404 | Assignment không tồn tại/đã xóa. | Refresh hoặc quay lại danh sách. |
| `LEARN-SUBMISSION-FORBIDDEN-001` | 403 | Student không có enrollment active. | Không retry; dùng đúng tài khoản/course. |
| `LEARN-SUBMISSION-STATE-001` | 409 | Assignment đã đóng/hết hạn. | Không retry; hiển thị trạng thái assignment. |
| `LEARN-SUBMISSION-IDEMPOTENCY-001` | 409 | Same idempotency key nhưng payload khác. | Tạo request mới với key mới sau khi xác minh. |

---

# 12. Quy trình review và approval

## 12.1. Self-review trước khi gửi team

1. Xóa tất cả placeholder, secret, thông tin copy từ API khác không liên quan.
2. Chạy `API_DD_CHECKLIST.md` và đánh dấu bằng chứng thật, không đánh dấu theo cảm tính.
3. Đối chiếu field names với OpenAPI/DTO/ERD/domain model.
4. Kiểm tra success, empty, null, not found, permission, conflict, dependency failure.
5. Kiểm tra tất cả mutation có transaction/concurrency/audit/event mapping.

## 12.2. Review theo vai trò

| Vai trò | Trọng tâm review |
|---|---|
| Product Owner / BA | Business purpose, actor, scope, rules, client flow. |
| Tech Lead / Architect | Context owner, API semantic, boundary, transaction, event, versioning. |
| Backend | DTO, validation, repository, query, concurrency, error mapping. |
| Frontend / Mobile | Request/response, field semantics, empty/error state, retry UX. |
| QA | Acceptance matrix, boundary, permission, negative and race-condition cases. |
| DBA / Security | Data classification, index/query, authorization, secret/PII masking, retention. |
| DevOps / SRE | Timeout, rate limit, trace, metric, alert, dependency resilience. |

## 12.3. Điều kiện chuyển trạng thái

| Status | Điều kiện |
|---|---|
| `Draft` | Đang soạn, còn open item hoặc chưa đủ evidence. |
| `In Review` | DD hoàn thành self-review, có owner/reviewer, không còn placeholder quan trọng. |
| `Approved` | Review bắt buộc hoàn tất; contract/rule/error/data mapping nhất quán. |
| `Deprecated` | Có replacement, migration window, communication owner và telemetry theo dõi client cũ. |

---

# 13. Lỗi nhập liệu thường gặp và cách sửa

| Lỗi | Vì sao không đủ | Cách sửa |
|---|---|---|
| Chỉ có JSON sample | Không thể biết required/null/default/boundary. | Điền field dictionary và validation matrix. |
| Ghi `Student có quyền` | Không xác định ownership/relationship. | Viết condition kiểm tra dựa JWT/resource relation. |
| `200` cho mọi trường hợp | Client không phân biệt empty/not found/conflict/error. | Dùng HTTP semantic và business code đúng. |
| DataMapping chỉ ghi `save DB` | Không biết table, predicate, transaction, lock, error. | Điền repository/query mapping theo từng access. |
| Không mô tả race condition | Có thể double submit/overwrite/quota race. | Thêm unique/version/lock/idempotency và test parallel. |
| Mượn error code API khác | Code không còn ý nghĩa, client xử lý sai. | Tạo code theo module/reason unique. |
| Đưa table/SQL/stack trace vào client error | Rủi ro security và leak implementation. | Ghi technical detail ở internal log, response chỉ safe message. |
| Đổi field nhưng không update History | Mất audit/migration/rollback traceability. | Bump version, thêm changelog và migration plan khi breaking. |
| Copy DD cũ còn module/endpoint/table cũ | AI/dev triển khai sai context. | Search toàn thư mục theo API code/module cũ trước approval. |

---

# 14. Checklist nhập liệu nhanh

- [ ] Đã xác định API code, method, endpoint, version, owner, status.
- [ ] Đã mô tả actor, trigger, scope, precondition, invariant, postcondition, out-of-scope.
- [ ] Đã mô tả authentication, permission và ownership condition cụ thể.
- [ ] Đã mô tả mọi request source và field gồm missing/null/empty/default.
- [ ] Đã có success, empty, error response matrix và response field lineage.
- [ ] Đã mô tả flow runtime, variable source, business rule, DB queries, transaction, concurrency.
- [ ] Đã mô tả cache/external service/event/audit/log/metric nếu áp dụng.
- [ ] Đã có error catalog: HTTP, business code, message, retry, client action, alert/test.
- [ ] Đã cập nhật history và review trail.
- [ ] Đã chạy toàn bộ `API_DD_CHECKLIST.md`.

---

## Tài liệu liên quan

- [README.md](README.md): cấu trúc template, convention và Definition of Done.
- [API_DD_CHECKLIST.md](API_DD_CHECKLIST.md): checklist self-review/approval.
- [01_Overview/Overview.md](01_Overview/Overview.md)
- [02_History/History.md](02_History/History.md)
- [03_Request/Request.md](03_Request/Request.md)
- [04_Response/Response.md](04_Response/Response.md)
- [05_DataMapping/DataMapping.md](05_DataMapping/DataMapping.md)
- [06_Error/Error.md](06_Error/Error.md)
