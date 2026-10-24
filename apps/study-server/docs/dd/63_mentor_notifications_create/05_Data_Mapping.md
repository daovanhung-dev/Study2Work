---
title: "Data Mapping"
order: 5
dd_id: "63"
api_name: "Tạo và phát thông báo"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Luồng xử lý đề xuất

1. Xác thực Bearer JWT và role Mentor.
2. Đọc các field theo đúng kiểu catalog; phân tích recipients/channels chỉ sau khi format được duyệt.
3. Xác minh Mentor quản lý course và mọi recipient thuộc tập học viên đủ điều kiện của course. Request trực tiếp thiếu course_id nên bước này `SOURCE_REQUIRED`; khuyến nghị thêm course_id.
4. Tạo Notification và liên kết recipient trong một thao tác logic nhất quán; chưa có target vật lý hoặc contract transaction.
5. Tạo Operation và đưa yêu cầu phát Push/Email vào queue; cơ chế persistence/queue là `SOURCE_REQUIRED`.
6. Trả HTTP 202 sau khi job được chấp nhận; provider delivery xảy ra bất đồng bộ. Không coi đã tiếp nhận là đã gửi.
7. UI dùng ID đã được contract nối để gọi #64 lấy delivery status; ID handoff chưa được xác định.

### Mục lục

- [0. Xác thực](#step-0-auth)
- [1. Nhận và kiểm tra request](#step-1-request)
- [2. Xác thực course/recipients](#step-2-recipient-scope)
- [3. Tạo Notification và recipients](#step-3-persist-notification)
- [4. Chấp nhận Operation và enqueue](#step-4-operation-queue)
- [5. Phát và cập nhật delivery](#step-5-delivery)
- [6. Trả response/lỗi](#step-6-response-errors)

<a id="step-0-auth"></a>

## 0. Xác thực

- Xác thực Bearer JWT; token thiếu/sai → 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Yêu cầu role Mentor theo catalog. Sai role/không có quyền → 403 `DESIGN_ACCESS_DENIED`.
- Lấy sender/owner identity từ principal; không lấy sender ID từ body.
- Study helper hiện dùng Student-specific guard; API #63 chưa wired. Mentor claim, key mapping và ownership/assignment relation là `SOURCE_REQUIRED`.

<a id="step-1-request"></a>

## 1. Nhận và kiểm tra request

| Field | Kiểu trực tiếp | Sử dụng | Validation/status |
|---|---|---|---|
| `recipients` | string! | Xác định danh sách Student mục tiêu | Encoding chưa rõ; CSV ID int64 là đề xuất DERIVED. |
| `title` | string! | Tiêu đề Notification | Không rỗng/trim là DERIVED; giới hạn 200 chỉ là schema candidate. |
| `content` | int64! | Nội dung hoặc mã tham chiếu nội dung | DISCREPANCY với nhập text; không parse thành body khi chưa sửa contract. |
| `channels` | string! | Chọn Push/Email | Encoding và token chưa định nghĩa; CSV tên channel là đề xuất DERIVED. |
| `course_id` | Không khai báo | Cần thiết để kiểm tra quyền và enrollment theo course | Không tự thêm vào request trực tiếp; cần cập nhật contract. |

- Lỗi hình dạng hoặc giá trị không hợp lệ được map về 422 `DESIGN_VALIDATION_ERROR` theo error set direct.
- Không đặt giới hạn số recipient/độ dài title/channel khi contract chưa quy định; mọi giới hạn phải được xác nhận trước triển khai.

<a id="step-2-recipient-scope"></a>

## 2. Xác thực course và recipients

- AC-25 precondition yêu cầu Mentor được phép gửi cho học viên thuộc course.
- #62 là GET roster theo course; #63 request trực tiếp không có course_id và `recipients` encoding chưa được định nghĩa.
- Vì vậy không có query/predicate hợp lệ để xác nhận toàn bộ recipients nằm trong đúng course đã chọn. Không suy ra course chỉ từ tập user IDs.
- Khuyến nghị DERIVED: nhận course_id, kiểm tra scope Mentor trước, rồi xác minh toàn bộ recipient IDs là Student thuộc tập enrollment đủ điều kiện; nếu một ID ngoài scope, từ chối toàn bộ request để tránh gửi một phần ngoài ý muốn.
- Không trả thông tin phân biệt recipient tồn tại/không tồn tại ngoài quyền; chi tiết 403/422 cần thống nhất chính sách quyền riêng tư.

<a id="step-3-persist-notification"></a>

## 3. Tạo Notification và recipients

### 3.1. M1 — logical Notification

| Logical field | Value source | Mapping rule/status |
|---|---|---|
| Notification ID | Persistence/job system | Catalog Notification ID int64 candidate; legacy BIGSERIAL; V1-PILOT UUID — conflict, SOURCE_REQUIRED. |
| `title` | Request `title` | Kiểu string trực tiếp; cả hai schema artifact candidate đều có max 200, chưa phải validation được duyệt. |
| `content` | Request `content` | Kiểu int64 trong catalog không map trực tiếp sang legacy TEXT hoặc pilot body varchar; DISCREPANCY. |
| Sender | Authenticated Mentor principal | Legacy `sender_id` BIGINT candidate; UUID pilot has no sender field; identity mapping SOURCE_REQUIRED. |
| Channels | Request `channels` | Legacy không có field channel; pilot lưu channel theo delivery row và cho phép IN_APP hoặc EMAIL; SOURCE_REQUIRED. |
| Created time | Persistence system | Legacy TIMESTAMP vs pilot timestamptz; timezone/clock contract SOURCE_REQUIRED. |

### 3.2. M2 — logical recipient associations

| Logical field | Value source | Mapping rule/status |
|---|---|---|
| Recipient identity | Parsed `recipients` | Chỉ dùng ID Student int64 candidate sau khi encoding và schema được duyệt. |
| Recipient relation | Notification ID + recipient ID | Diagram yêu cầu Notification + recipients; legacy chỉ có `notifications.user_id` nullable và không có bảng recipients; pilot tạo một notification UUID cho mỗi learner. Chưa chọn target. |
| Duplicate recipient | Repeated request ID | Khuyến nghị loại trùng giữ thứ tự đầu tiên; DERIVED, cần duyệt. |
| Course eligibility | Course + active enrollment | Body trực tiếp thiếu course_id; chưa thể kiểm tra an toàn cho tới khi contract được sửa. |

Không tạo SQL `INSERT`: bảng/khóa vật lý cho nhóm recipients chưa được xác nhận. Xem [07_table.md](./07_table.md).

<a id="step-4-operation-queue"></a>

## 4. Chấp nhận Operation và enqueue

- Tạo một logical Operation cho một lần POST được chấp nhận; idempotency phải ngăn retry tạo delivery trùng nếu policy được duyệt.
- Enqueue sau khi Notification/recipient data được chấp nhận bền vững; dùng queue/outbox chỉ là kiến trúc đề xuất, hiện không có Study schema/provider xác nhận.
- Nếu queue/dependency không thể nhận job trước khi API trả 202, map 503 `DESIGN_DEPENDENCY_UNAVAILABLE`.
- Sau 202, lỗi provider thuộc delivery lifecycle; không đổi response đã trả. API #64 cần mô hình đọc status được thống nhất.
- OperationKind/OperationStatus, initial state, ID allocation, persistence và retry policy là `SOURCE_REQUIRED`.

<a id="step-5-delivery"></a>

## 5. Phát và cập nhật delivery

- Worker/provider gửi từng notification theo recipients × channels đã được chấp nhận.
- Diagram xác nhận Push/Email nhưng không quy định provider, retry, timeout, thứ tự, partial failure hoặc status aggregation.
- V1-PILOT `notification_deliveries` là candidate khác model: UUID notification ID, channel IN_APP/EMAIL và status QUEUED/SENT/DELIVERED/FAILED/SUPPRESSED; không khớp đầy đủ Push/Email và int64 contract.
- Không map `notifications.is_read` sang delivery status; read state thuộc API #43–#45.
- Không phát lại hoặc retry tự động theo số lần cụ thể khi chưa có policy.

<a id="step-6-response-errors"></a>

## 6. Trả response/lỗi

- Khi job được chấp nhận, trả HTTP 202 `DESIGN_OPERATION_ACCEPTED` và `ApiEnvelope<Operation>`.
- Không trả thành công khi queue chưa nhận yêu cầu.
- Sau 202, client cần ID để gọi API #64; Operation.id UUID và #64 notification_id int64 hiện chưa có mapping.
- Không thêm HTTP status hoặc business code ngoài catalog; giữ exact code set trực tiếp.
- API Guidelines yêu cầu error `data:null`; current helper mặc định `{}` và path chưa allowlist. Đây là discrepancy khi wiring sau này.

## Request Usage Matrix

| Request item | Nguồn | Bước mapping | Cách dùng query/mutation | Khoảng trống |
|---|---|---|---|---|
| Authorization | Header | 0 | Lấy Mentor sender/owner | Guard và principal binding SOURCE_REQUIRED. |
| `recipients` | Body string | 1, 2, 3 | Parse IDs, validate roster, tạo recipient associations | Encoding và target schema SOURCE_REQUIRED. |
| `title` | Body string | 1, 3 | Notification title | Trim/length là DERIVED. |
| `content` | Body int64 | 1, 3 | Candidate body/reference | DISCREPANCY với text input/schema. |
| `channels` | Body string | 1, 4, 5 | Chọn channel và tạo delivery work | Encoding/enum/provider SOURCE_REQUIRED. |
| `course_id` | Not declared | 2 | Cần cho course authorization/eligibility | Proposed contract correction only. |
| `Idempotency-Key` | Đề xuất theo guideline dùng chung | 4 | Khử trùng retry | Chưa có rule key/storage riêng cho API. |

## Query Matrix

| Query ID | Loại | Nguồn/cột | Predicate/mục đích | Trạng thái |
|---|---|---|---|---|
| Q1 | SELECT course + enrollment | Chưa chọn giữa legacy BIGINT và V1-PILOT UUID model | Kiểm tra quyền Mentor và mọi recipient thuộc course | Không thể viết query chuẩn vì request trực tiếp thiếu course_id; SOURCE_REQUIRED. |
| Q2 | INSERT Notification | Thực thể logic | Lưu title/content/sender | Schema vật lý mâu thuẫn; chưa có SQL được duyệt. |
| Q3 | INSERT recipients | Quan hệ logic | Gắn Notification với từng learner | Legacy không có recipient table; pilot dùng UUID riêng cho mỗi learner, khác contract. |
| Q4 | Create Operation + enqueue | Logical Operation/external queue | Chấp nhận công việc async và trả 202 | Chưa có nguồn persistence/queue producer cho Study. |
| Q5 | Provider delivery | Push/Email external service | Gửi theo recipient/channel | Contract/provider credential/retry/status là SOURCE_REQUIRED. |

## Mutation Matrix

| Mutation ID | Thao tác logic | Target | Field/nguồn | Transaction/xử lý lỗi |
|---|---|---|---|---|
| M1 | INSERT | Notification | title, content, sender, channel intent | Logical write DIRECT; table/columns/id type SOURCE_REQUIRED. |
| M2 | INSERT | Recipient association(s) | Notification + selected recipient IDs | Logical write DIRECT; target/uniqueness SOURCE_REQUIRED. |
| M3 | Create/queue | Operation/delivery job | Authenticated owner, notification reference, selected channels | Needed for 202; physical store/queue contract SOURCE_REQUIRED. |

## Response Source Matrix

| Field response | Kiểu | Nguồn candidate | Quy tắc chuyển đổi/null | Trạng thái |
|---|---|---|---|---|
| Envelope `success` | boolean | Accepted branch | true chỉ khi đã được tiếp nhận | Convention. |
| Envelope `businessCode` | string | Catalog | `DESIGN_OPERATION_ACCEPTED` | DIRECT. |
| Envelope `message` | string | Application | Thông điệp an toàn | Câu chữ cụ thể là SOURCE_REQUIRED. |
| `data.id` | uuid | Operation | Định danh job | Schema DIRECT; #18 path type conflict. |
| `data.kind` | OperationKind | Operation | Giá trị enum | SOURCE_REQUIRED. |
| `data.status` | OperationStatus | Operation | Trạng thái đã tiếp nhận | Enum/lifecycle SOURCE_REQUIRED. |
| `data.owner_id` | int64 | Operation | Mentor ID | Identity mapping SOURCE_REQUIRED. |
| `data.submitted_at` | date-time | Operation | ISO-8601 | Nguồn clock/độ chính xác là SOURCE_REQUIRED. |
| `data.updated_at` | date-time | Operation | ISO-8601 | Lifecycle SOURCE_REQUIRED. |
| `data.completed_at` | date-time? | Operation | Optional | Ngữ nghĩa hoàn tất là SOURCE_REQUIRED. |
| `data.result` | Payment? | Operation schema | Optional, no value inferred | DISCREPANCY for notification result. |
| Nested Payment fields | Payment fields | Reusable Payment schema | Chỉ khi result thực sự là Payment | Không phù hợp notification job; DD này không dựng giá trị. |
| Notification ID cho #64 | int64 | Operation schema không có field nguồn | Cần được trả trong result/response đã duyệt | SOURCE_REQUIRED; chặn tích hợp. |
| Envelope `meta` | object | Shared envelope | `{}` example only | Shape DIRECT; chi tiết chưa được quy định. |
| Envelope `traceId` | uuid | Request context | Propagate trace | Quy ước dùng chung; chưa có route. |

## Luồng bàn giao giữa các API

- #62 dự kiến cung cấp tập recipient đã chọn, nhưng response trực tiếp là `Page<Course>`; roster projection vẫn là discrepancy contract.
- #63 cần course ID và encoding recipient để kiểm tra lại quyền; request trực tiếp không có course_id và chưa có rule encoding.
- #63 trả Operation; #64 nhận notification_id int64. Chưa có field hoặc mapping được duyệt để nối hai API.
- AC/API index liệt kê polling API #18; node #18 rời trong diagram và kiểu path ở catalog mâu thuẫn với quy ước/schema UUID.
- Rà soát các điểm này cùng nhau trong macro-review AC-25 sau khi có DD #64; trong lúc đó vẫn giữ nguyên giá trị trực tiếp từ catalog.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `3. Data mapping`
- Dimension: `B1:BB61`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `63`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Flow xử lý data |  |
| 4 | `D4` | 0. |  |
| 4 | `E4` | Check quyền |  |
| 5 | `E5` | ・ |  |
| 5 | `F5` | Thực hiện check quyền |  |
| 6 | `E6` | ・ |  |
| 6 | `F6` | Get count khi get data từ … |  |
| 7 | `G7` | Table get |  |
| 7 | `K7` | : |  |
| 8 | `G8` | Conditions |  |
| 8 | `K8` | : |  |
| 10 | `E10` | ・ |  |
| 10 | `F10` | Trường hợp giá trị get được lớn hơn 0, thực hiện các xử lý tiếp theo |  |
| 11 | `E11` | ・ |  |
| 11 | `F11` | Trường hợp giá trị get được bằng 0, trả về status 2 |  |
| 13 | `D13` | 1. |  |
| 13 | `E13` | validate data input |  |
| 14 | `F14` | refer sheet [４．Error] |  |
| 16 | `D16` | 2. |  |
| 16 | `E16` | Get thông tin… |  |
| 18 | `F18` | Table get |  |
| 18 | `K18` | Column get |  |
| 18 | `P18` | Chú thích |  |
| 18 | `U18` | Remarks |  |
| 29 | `F29` | Target table / join condition |  |
| 30 | `F30` | Target table |  |
| 30 | `N30` | Join condition |  |
| 30 | `AL30` | 結合種類 |  |
| 31 | `F31` | txn_ams_t0320 AS a |  |
| 32 | `F32` | txn_amm_v0002 AS b |  |
| 32 | `N32` | ON a . chy_typ = b . kbn_typ AND b . dmin_cd = A AND b . kbnknr_cd = 001 |  |
| 32 | `AL32` | LEFT JOIN |  |
| 33 | `F33` | txn_amm_v0002 AS c |  |
| 33 | `N33` | ON a . chy_typ = c . kbn_typ AND c . dmin_cd = A AND c . kbnknr_cd = Z02 |  |
| 33 | `AL33` | LEFT JOIN |  |
| 35 | `F35` | ・ |  |
| 35 | `G35` | Điều kiện get data |  |
| 37 | `F37` | ・ |  |
| 37 | `G37` | Điều kiện sort |  |
| 41 | `D41` | 3. |  |
| 41 | `E41` | Insert/Update thông tin … |  |
| 42 | `E42` | Update table…. |  |
| 43 | `E43` | ・ |  |
| 43 | `F43` | Items update |  |
| 44 | `F44` | ・ |  |
| 44 | `G44` | Refer sheet [xxxx] |  |
| 45 | `E45` | ・ |  |
| 45 | `F45` | Điều kiện get data |  |
| 46 | `F46` | ・ |  |
| 46 | `G46` | auth_user. id = user hiện tại theo token |  |
| 48 | `D48` | 4. |  |
| 48 | `E48` | check kết quả execute query  |  |
| 49 | `E49` | 1. Thành công |  |
| 50 | `F50` | HTTPStatus = 200 |  |
| 51 | `F51` | Trả về kết quả status = 1 |  |
| 52 | `E52` | 2. Lỗi hệ thống phát sinh |  |
| 53 | `F53` | HTTPStatus = 500 |  |
| 54 | `F54` | Trả về kết quả status = 2 |  |
| 55 | `E55` | 3. Validate lỗi |  |
| 56 | `F56` | HTTPStatus = 400 |  |
| 57 | `F57` | Trả về kết quả status = 2 |  |
| 58 | `E58` | 4. Ngoài trường hợp trên |  |
| 59 | `F59` | Trả về kết quả status = 2 |  |

</details>
