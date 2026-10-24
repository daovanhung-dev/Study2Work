---
title: "Data Mapping"
order: 5
dd_id: "83"
api_name: "Lấy lesson detail"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

Admin Bearer JWT -> xác thực role/lesson-management permission -> validate `lesson_id` -> Q1 đọc một lesson theo ID -> kiểm tra row/mapping -> map reusable Lesson -> HTTP 200 hoặc exact catalog error. AC-34 bước “Đọc lesson + dependencies” còn thiếu định nghĩa dependency output; không truy vấn dependencies khi không có response/use rule.

# Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Validate data input](#step-1-validate-data-input)
- [2. Get thông tin](#step-2-get-thong-tin)
- [3. Check kết quả](#step-3-check-ket-qua)
- [4. Map response](#step-4-map-response)
- [5. Trả response](#step-5-tra-response)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

### 0.1. Xác thực và authorization

- Xác thực Bearer JWT và role Admin theo catalog.
- Yêu cầu lesson-management permission theo tiền điều kiện AC-34.
- Token thiếu/sai/hết hạn -> HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Principal không có role Admin hoặc permission -> HTTP 403 `DESIGN_ACCESS_DENIED`.
- Current `app/utils/auth.py` chỉ có Student guard; Admin claims, permission source và guard chưa có.
- Hoàn thành authorization trước Q1 để không làm lộ lesson tồn tại cho caller không đủ quyền.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Authorization header | Bearer credential | Token hợp lệ/chưa hết hạn | DIRECT requirement; route chưa wired. |
| Principal policy | Admin role | Principal có role Admin | DIRECT; claim source chưa có. |
| Admin policy | lesson-management permission | Principal được phép quản lý bài học | AC-34 precondition; implementation SOURCE_REQUIRED. |

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. `lesson_id`

- Path parameter required, kiểu int64 theo catalog.
- Không thêm minimum/positive constraint; catalog không khai báo.
- ID parse được nhưng không tìm thấy row -> 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Path không parse được int64 -> candidate 404 để giữ error set catalog; đây là DERIVED proposal. FastAPI/middleware hiện có thể trả 422 generic nếu future route không xử lý riêng.
- Không có body/query parameters.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Q1 — candidate đọc lesson theo ID

Đây là candidate query trên legacy DDL, không phải truy vấn đã xác minh trên live schema.

~~~sql
SELECT
    l.id,
    l.course_id,
    l.name AS title,
    l.content,
    l.video_url,
    l.sort_order AS "order",
    l.status
FROM lessons AS l
WHERE l.id = :lesson_id
~~~

- Bind `lesson_id` làm parameter; không nội suy path string vào SQL.
- Không lọc theo `status`; Admin cần đọc lesson ở lifecycle khác nhau trước thao tác #84/#85.
- Không JOIN `courses`, `resources` hoặc `lesson_progress`; contract chỉ trả `Lesson`, còn dependency reads chưa có field/use rule.
- Q1 trả tối đa một row theo khóa chính candidate. Không chạy count query/order/pagination.
- Legacy `course_id` nullable; không thêm `IS NOT NULL` để che row không map được reusable Lesson.

### 2.2. Candidate field mapping

| Logical response field | Candidate legacy column | Transform | Status |
|---|---|---|---|
| `id` | `lessons.id` | Copy | Candidate BIGINT mapping. |
| `course_id` | `lessons.course_id` | Copy | Nullable DDL conflicts with required contract. |
| `title` | `lessons.name` | Alias `name -> title` | API #09 precedent. |
| `content` | `lessons.content` | Copy | Nullable; API #09 returns null in its optional model. |
| `video_url` | `lessons.video_url` | Copy | Nullable; API #09 returns null in its optional model. |
| `order` | `lessons.sort_order` | Alias `sort_order -> order` | API #09 precedent. |
| `status` | `lessons.status` | Preserve source value | Enum/casing unresolved. |

### 2.3. Dependency relations from AC-34/ERD

- AC-34 n5 says “Đọc lesson + dependencies”, but does not identify dependency fields, counts or response location.
- Legacy ERD shows `resources.lesson_id -> lessons.id` and `lesson_progress.lesson_id -> lessons.id`; the DB guide lists both as lesson references.
- The catalog response contains no resource/progress/dependency field. Do not query or expose these records in #83 until their purpose and output contract are defined.
- API #86 explicitly requires progress/reference checks during delete. #86 must check current references at mutation time; a detail-time read cannot safely authorize later deletion.

### 2.4. Schema boundary

- Legacy `DB.sql` has BIGINT lesson ID and columns suitable as candidates for most `Lesson` fields.
- Legacy `lessons.course_id` has no `NOT NULL` constraint although reusable `Lesson.course_id` is required.
- V1-PILOT uses UUID ID plus chapter/course-version fields and does not establish the legacy mapping.
- Live target schema/version is unverified; do not mix or cast these models.

<a id="step-3-check-ket-qua"></a>

## 3. Check kết quả

### 3.1. Lesson tồn tại

- Nếu Q1 trả một row và required fields map được, tiếp tục map response.
- `course_id=NULL` không thể thỏa reusable `Lesson.course_id:int64`; candidate mapping failure dùng 500 `DESIGN_INTERNAL_ERROR`, cần owner chốt dữ liệu/nullability policy.
- Không lọc lesson vì `status`; current public curriculum’s `PUBLISHED` predicate không áp dụng cho Admin detail.

### 3.2. Không có lesson

- Nếu Q1 không trả row, trả HTTP 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Lesson soft-deleted có được xem là “không có” hay không chưa xác định; legacy schema không có deleted marker và #86 policy còn mở.

### 3.3. Lỗi truy vấn/mapping

- Query/database/mapping exception -> HTTP 500 `DESIGN_INTERNAL_ERROR`.
- Không trả raw SQL, stack trace hoặc database detail cho client.

<a id="step-4-map-response"></a>

## 4. Map response

### 4.1. Reusable `Lesson`

- `data.id = row.id`.
- `data.course_id = row.course_id`.
- `data.title = row.name`.
- `data.content = row.content`.
- `data.video_url = row.video_url`.
- `data.order = row.sort_order`.
- `data.status = row.status`.
- Không thêm resources, progress, counters, timestamps hoặc dependency fields.
- Nếu `content`/`video_url` source NULL thì serialize `null` là proposal theo API #09 model/test precedent; cần chốt optional-field wire behavior.
- Không dựng/chuẩn hóa LessonStatus whitelist khi enum members/casing chưa có nguồn.

### 4.2. Envelope

- Thành công: `success=true`, code `DESIGN_RESOURCE_RETRIEVED`, HTTP 200, `data` là một object Lesson, `meta={}` candidate, `traceId` theo middleware convention.
- Lỗi: giữ exact catalog codes/statuses. API guideline muốn `data:null`, nhưng current `error_response` mặc định `{}` và path chưa allowlist #83.

<a id="step-5-tra-response"></a>

## 5. Trả response

### 5.1. Thành công

- Sau Q1 và mapping thành công, trả HTTP 200 `DESIGN_RESOURCE_RETRIEVED` với một `Lesson`.
- Message wording chưa được catalog cố định; không thêm field nghiệp vụ.

### 5.2. Lỗi

- 401 `DESIGN_AUTHENTICATION_REQUIRED` — Bearer credential thiếu/sai.
- 403 `DESIGN_ACCESS_DENIED` — role Admin/lesson permission không đạt.
- 404 `DESIGN_RESOURCE_NOT_FOUND` — lesson không tồn tại; malformed ID -> 404 chỉ là proposal.
- 500 `DESIGN_INTERNAL_ERROR` — query hoặc mapping thất bại.
- Không tạo 422/409 hoặc business code mới.

## Request Usage Matrix

| Request item | Data Mapping step | Validation | Query usage | Response usage | Status/gap |
|---|---|---|---|---|---|
| Authorization Bearer | 0 | Authenticate token | Không đưa vào SQL | Không map | DIRECT; guard SOURCE_REQUIRED |
| Admin role | 0 | Require Admin | Check trước Q1 | Không map | DIRECT |
| lesson-management permission | 0 | Require permission | Check trước Q1 | Không map | AC-34 DIRECT; policy SOURCE_REQUIRED |
| `lesson_id` | 1/2 | Required int64; no extra range | Q1 bind `:lesson_id` | `data.id` | DIRECT type; invalid parse -> 404 DERIVED |
| Request body | — | Not declared | None | None | DIRECT absence |
| Query parameters | — | Not declared | None | None | DIRECT absence |

## Query Matrix

| Query ID | Mục đích | Type | Base table | Column | JOIN/condition | Result/branch | Status |
|---|---|---|---|---|---|---|---|
| Q1 | Read one lesson | SELECT | Legacy `lessons AS l` candidate | `l.id` | `l.id = :lesson_id` | Row exists -> map; absent -> 404 | Physical mapping candidate |
| Q1 | Map course ID | SELECT | Legacy `lessons AS l` candidate | `l.course_id` | Same row | Required response field | Nullable schema discrepancy |
| Q1 | Map title | SELECT | Legacy `lessons AS l` candidate | `l.name` | Same row | Alias to `title` | API #09 precedent |
| Q1 | Map content | SELECT | Legacy `lessons AS l` candidate | `l.content` | Same row | Optional response field | Null handling DERIVED |
| Q1 | Map video URL | SELECT | Legacy `lessons AS l` candidate | `l.video_url` | Same row | Optional response field | Null handling DERIVED |
| Q1 | Map order | SELECT | Legacy `lessons AS l` candidate | `l.sort_order` | Same row | Alias to `order` | API #09 precedent |
| Q1 | Map status | SELECT | Legacy `lessons AS l` candidate | `l.status` | Same row; no status predicate | Lesson status | Enum members unknown |
| Q-dependencies | No approved read | N/A | `resources`, `lesson_progress` are possible relations only | No selected fields | AC n5 lacks output/use rule | No query included | SOURCE_REQUIRED |
| Q-count | Not applicable | N/A | N/A | N/A | No count/page contract | None | N/A |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields/audit | Transaction/failure |
|---|---|---|---|---|---|
| N/A | None — READ ONLY | N/A | API #83 is GET; later changes use #84–#86 | No mutation/audit write | No transaction/commit; read failures -> catalog 500 |

## Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Data Mapping step | Transform | Null/empty rule | Gap/status |
|---|---|---|---|---|---|---|---|
| `success` | boolean | Envelope | Branch result | 5 | true/false | Required | DIRECT convention |
| `businessCode` | string | Catalog | #83 branch code | 5 | Exact literal | Required | DIRECT |
| `message` | string | Application | Safe message | 5 | Localized text | Wording unspecified | DERIVED wording |
| `data` | object | Query result | Q1 single row | 4 | Map one Lesson | Required on success | DIRECT response type |
| `data.id` | int64 | DB candidate | `lessons.id` | 4 | Copy | Required | Legacy candidate |
| `data.course_id` | int64 | DB candidate | `lessons.course_id` | 4 | Copy | Required; source NULL cannot map | DDL discrepancy |
| `data.title` | string | DB candidate | `lessons.name` | 4 | `name -> title` | Required | API #09 precedent |
| `data.content` | string? | DB candidate | `lessons.content` | 4 | Copy | NULL candidate | Optional; confirm null/omit |
| `data.video_url` | uri? | DB candidate | `lessons.video_url` | 4 | Copy | NULL candidate | Optional; confirm null/omit |
| `data.order` | int32 | DB candidate | `lessons.sort_order` | 4 | `sort_order -> order` | Required | API #09 precedent |
| `data.status` | LessonStatus | DB candidate | `lessons.status` | 4 | Preserve stored string | Required | Enum/casing SOURCE_REQUIRED |
| `meta` | object | Envelope convention | N/A | 4/5 | Empty object candidate | `{}` success | Current helper convention |
| `traceId` | uuid | Middleware | Header or generated UUID | 0/5 | Propagate/generate | Required | Current Study convention |
| Dependencies | Not in response schema | No approved source/output | N/A | N/A | Do not emit | Not applicable | AC diagram conflict |

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
