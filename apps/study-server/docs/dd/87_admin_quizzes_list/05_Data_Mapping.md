---
title: "Data Mapping"
order: 5
dd_id: "87"
api_name: "Lấy danh sách quiz"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

### Mục lục

- [Step 0 — Authentication and authorization](#step-0-authentication-and-authorization)
- [Step 1 — Validate query](#step-1-validate-query)
- [Step 2 — Read quiz page](#step-2-read-quiz-page)
- [Step 3 — Read nested question data](#step-3-read-nested-question-data)
- [Step 4 — Map and build response](#step-4-map-and-build-response)
- [Step 5 — Return success or error](#step-5-return-success-or-error)

<a id="step-0-authentication-and-authorization"></a>
## Step 0 — Authentication and authorization

### 0.1. Xác thực Bearer và quyền Admin

- Nhận Authorization Bearer JWT theo API catalog.
- Nếu token thiếu hoặc không hợp lệ thì trả HTTP 401 DESIGN_AUTHENTICATION_REQUIRED.
- Nếu principal không có role Admin thì trả HTTP 403 DESIGN_ACCESS_DENIED.
- AC-35 yêu cầu quiz-management permission; nguồn ánh xạ permission sang claim/policy chưa được tìm thấy.
- Authorization phải được kiểm tra trước query quiz hoặc nested question data.
- Không dùng course filter thay cho authorization.

### 0.2. Current source boundary

| Item | Current evidence | Status |
|---|---|---|
| Admin Bearer guard | Study auth helper hiện kiểm tra Student; không có Admin helper | NOT_FOUND |
| Quiz-management permission | AC-35 nêu precondition; source policy không có | SOURCE_REQUIRED |
| Route #87 | Không có route/view/test | UNWIRED / NOT_FOUND |
| Middleware path | /api/v1/admin/quizzes chưa có trong DESIGN_CONTRACT_PATHS | Conditional future wiring gap |

<a id="step-1-validate-query"></a>
## Step 1 — Validate query

### 1.1. Đọc input

| Variable | Source | Type | Status |
|---|---|---|---|
| course_id | Query course | int64 | DIRECT type; lower/upper bound SOURCE_REQUIRED |
| quiz_status | Query status | string | DIRECT type; enum/casing SOURCE_REQUIRED |
| page | Query page | int32 | DIRECT type; default/range DERIVED |
| page_size | Internal proposal | int32 | Fixed 20 only if list pagination is approved; not request input |

### 1.2. Chuẩn hóa proposal

- Nếu course được gửi thì đề xuất bind course_id và filter bằng equality.
- Nếu status được gửi thì đề xuất giữ nguyên string và filter bằng equality.
- Không trim hoặc đổi case status khi enum/casing chưa được xác nhận.
- Nếu page vắng mặt thì proposal đặt page = 1.
- Nếu page < 1 thì proposal coi input không hợp lệ; catalog không có 400/422 code cho nhánh này.
- Nếu page được duyệt thì proposal dùng page_size = 20 theo fixed-size convention API #07.
- Không thêm query size hoặc sort vào contract.
- Query parser error mapping cần được chốt trước khi route được wire.

<a id="step-2-read-quiz-page"></a>
## Step 2 — Read quiz page

### 2.1. Q1 — Candidate quiz metadata page

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| Legacy quizzes AS q | q.id | Quiz ID | BIGSERIAL candidate; live schema chưa xác minh. |
| ↑ | q.course_id | Course ID | Nullable trong legacy DDL; response contract yêu cầu int64. |
| ↑ | q.name | Quiz title source | Alias candidate name → title. |
| ↑ | q.passing_score | Passing score | NUMERIC(5,2) → decimal-string candidate. |
| ↑ | q.time_limit_minutes | Duration source | Alias candidate; nullable. |
| ↑ | q.status | Filter field only | Không có status trong reusable Quiz response. |
| ↑ | N/A | description, created_at, updated_at | Không có trong reusable Quiz schema; không trả thêm. |

**Candidate filters**

- Nếu query course có giá trị thì q.course_id = :course_id.
- Nếu query status có giá trị thì q.status = :status.
- Nếu course/status vắng mặt thì không thêm predicate tương ứng (DERIVED).
- Không lọc status mặc định như DRAFT hoặc PUBLISHED.
- Không lọc theo quiz status nếu query status vắng mặt.

**Candidate ordering and page window**

- Candidate default order: q.id ASC để kết quả ổn định; DERIVED.
- Nếu page 1-based, fixed size 20 được duyệt thì LIMIT = 20.
- Nếu page 1-based, fixed size 20 được duyệt thì OFFSET = (page - 1) × 20.
- Page size/order chưa được contract chốt; không coi các giá trị này là runtime SQL.

### 2.2. Q1C — Candidate total count for Page proposal

- Chỉ chạy Q1C nếu owner duyệt response ApiEnvelope<Page<Quiz>>.
- Q1C dùng FROM quizzes AS q.
- Q1C dùng cùng predicate course/status như Q1.
- Q1C đếm q.id và trả total cho proposed PageMeta.
- Direct ApiEnvelope<Quiz> không khai báo total; count không thuộc direct contract.

### 2.3. Kết quả truy vấn

- Nếu list proposal được duyệt và không có row thì đề xuất HTTP 200 với items=[] và pagination theo PageMeta.
- Nếu catalog response singleton được giữ nguyên thì chưa có quy tắc chọn một Quiz từ kết quả list; đây là response cardinality discrepancy, không tự chọn row đầu.
- Không ánh xạ danh sách rỗng thành 404 vì catalog không khai báo 404.

<a id="step-3-read-nested-question-data"></a>
## Step 3 — Read nested question data

### 3.1. Q2 — Candidate question batch

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| Legacy quiz_questions AS qq | qq.id | Question ID | Candidate BIGSERIAL. |
| ↑ | qq.quiz_id | Parent Quiz | Candidate join/filter key. |
| ↑ | qq.question_text | Question text | Alias candidate question_text → text. |
| ↑ | qq.sort_order | Display order | Candidate order; tie-break id ASC là DERIVED. |
| ↑ | SOURCE_REQUIRED | QuestionType | Legacy table không có type; pilot field thuộc mô hình khác. |
| ↑ | N/A | qq.score | Có trong DDL nhưng không có trong QuizQuestion contract. |

**Candidate relation and order**

- Candidate relation: qq.quiz_id = q.id.
- Nếu Page list được duyệt thì chỉ đọc các quiz IDs thuộc trang hiện tại.
- Candidate question order: qq.sort_order ASC, qq.id ASC.
- Không lọc hoặc đổi status câu hỏi; nguồn không có rule đó.
- AC-35 diagram chỉ ghi “Query quizzes”; đọc nested questions là candidate theo reusable Quiz schema, cần xác nhận.

### 3.2. Q3 — Candidate choice batch

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| Legacy quiz_choices AS qc | qc.id | Candidate choice ID | Output field chưa có QuizChoice schema. |
| ↑ | qc.question_id | Parent question | Candidate relation key. |
| ↑ | qc.choice_text | Candidate text | Output property/name chưa được chốt. |
| ↑ | N/A | qc.is_correct | Không có trong QuizChoice contract; không đưa vào response nếu chưa được duyệt. |

**Candidate relation and gap**

- Candidate relation: qc.question_id = qq.id.
- Legacy quiz_choices không có sort_order; thứ tự choices SOURCE_REQUIRED.
- QuizChoice schema chưa định nghĩa property, type hoặc nullability.
- Không tự map is_correct sang field mới.
- Student API #28 không trả is_correct; API #87 là Admin nhưng contract hiện tại cũng không định nghĩa field này.

<a id="step-4-map-and-build-response"></a>
## Step 4 — Map and build response

### 4.1. Direct contract mapping

- response.success = true.
- response.businessCode = DESIGN_RESOURCE_RETRIEVED.
- response.message = thông điệp an toàn; nội dung cụ thể chưa được catalog định nghĩa.
- response.data.id = q.id.
- response.data.course_id = q.course_id; NULL không map được vào int64 required và cần xử lý theo policy được duyệt.
- response.data.title = q.name.
- response.data.duration_minutes = q.time_limit_minutes; null/omit policy cần xác nhận.
- response.data.passing_score = q.passing_score được serialize thành decimal-string; scale/rounding cần xác nhận.
- response.data.questions[] = question projection từ Q2 nếu schema list được duyệt.
- response.data.questions[].type = SOURCE_REQUIRED.
- response.data.questions[].choices[] = SOURCE_REQUIRED đến khi QuizChoice schema được định nghĩa.
- response.meta = object theo ApiEnvelope.
- response.traceId = trace của request theo envelope convention.
- Direct type ApiEnvelope<Quiz> không biểu diễn rõ collection hoặc page của endpoint này.

### 4.2. Page proposal mapping — chưa được duyệt

- data.items[] = Quiz rows của Q1 page result.
- data.pagination.page = page query hoặc default 1.
- data.pagination.size = fixed 20 proposal.
- data.pagination.total = Q1C result.
- data.pagination.total_pages = ceil(total / 20); nếu total=0 thì proposal trả 0.
- Nếu owner không duyệt Page proposal thì không dùng các field pagination này.

<a id="step-5-return-success-or-error"></a>
## Step 5 — Return success or error

### 5.1. Thành công

- HTTP 200.
- businessCode = DESIGN_RESOURCE_RETRIEVED.
- Empty list 200 với items=[] là proposal chỉ áp dụng khi collection response được duyệt.
- Không trả 404 cho danh sách rỗng.

### 5.2. Authentication/authorization error

- Token thiếu/sai: HTTP 401 DESIGN_AUTHENTICATION_REQUIRED.
- Không có role Admin hoặc quiz-management permission: HTTP 403 DESIGN_ACCESS_DENIED.
- Permission policy hiện chưa có source trong Study.

### 5.3. System error

- Query, database hoặc mapping failure: HTTP 500 DESIGN_INTERNAL_ERROR theo catalog.
- Nếu route được thêm nhưng middleware path chưa allowlist thì current generic handler có thể trả INTERNAL_SERVER_ERROR; đây là conditional future integration discrepancy.
- API Guidelines yêu cầu error data=null; current helper mặc định {} khi caller không truyền data.

### 5.4. Query validation gap

- Catalog không khai báo 400 hoặc 422 cho course/page parse error.
- Không tự gán thêm business code.
- Cần thống nhất FastAPI validation handler, middleware allowlist và catalog trước khi runtime implementation.
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
