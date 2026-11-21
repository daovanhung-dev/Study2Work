---
title: "Data Mapping"
order: 5
dd_id: "35"
api_name: "Tạo/nộp submission"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
Student Bearer -> validate role -> parse path/body
-> candidate assignment lookup -> check access/deadline (rules open)
-> AC-17 INSERT/UPDATE Submission as SUBMITTED (branch rule open)
-> map candidate Submission response -> ApiEnvelope
~~~

API #35 is design-only. This flow keeps current source behavior separate from the expected catalog and AC-17 design.

## Request Usage Matrix

| Request field | Source | Step | Validation | Query/mutation use | Response use | Gap |
|---|---|---:|---|---|---|---|
| Authorization | Authorization header | 0 | Bearer JWT; Student role per catalog | Authenticated principal | Candidate source for data.user_id | API #35 route/guard is not wired. |
| assignment_id | Path | 1–3 | Required int64 | Candidate assignment lookup and assignment_submissions.assignment_id | data.assignment_id | Positivity, parse-failure and access rules are unspecified. |
| text | JSON body | 1/5 | Required string per catalog | Candidate assignment_submissions.content | data.content | Length, empty behavior and required-vs-optional storage policy unresolved. |
| file refs | JSON body, exact catalog notation | 1/5 | Required string per catalog | Candidate source for file references/file_url | data.files[] | JSON key, encoding, cardinality and UploadAsset binding unresolved. |
| Content-Type | Header | 1 | application/json is draft convention | Select JSON parser | None | Catalog does not state media type. |
| Idempotency-Key | Header | N/A | Not in API #35 catalog | Shared guideline applies to retryable mutations | None | Retryability/header applicability unresolved; not added to the contract. |

## Query Matrix

| Query ID | Purpose | Base table | Candidate columns | Candidate condition | Join/result | Branch and status |
|---|---|---|---|---|---|---|
| Q1 | Locate assignment and candidate deadline | assignments | id, course_id, due_at | assignments.id = path assignment_id | No join established; candidate assignment row | Query shape/publish/access predicate are design candidates, not runtime SQL. |
| Q2 | Find existing submission only if upsert is approved | assignment_submissions | id, assignment_id, user_id, status | Candidate assignment_id = path ID and user_id = authenticated principal | May return zero, one or multiple rows; no uniqueness guarantee | Branch predicate and multi-row behavior SOURCE_REQUIRED; do not choose insert/update from this candidate alone. |

- No exact SQL, course/enrollment join, visibility predicate or lock behavior is defined by the sources.
- DB table design and checked-in DDL are not evidence of live schema.

## Mutation Matrix

| Mutation ID | Operation | Target table/API | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| M1 | INSERT or UPDATE candidate per AC-17 | assignment_submissions (design candidate) | Assignment + authenticated user; exact row key and branch unresolved | assignment_id, user_id, content, file_url, submitted_at, status | Path, Bearer principal, text/file refs, time generator, AC-17 status | Not specified | 07_assignment_submissions_insert_update.md | SOURCE_REQUIRED | Preserve catalog 409/422/500; rollback behavior depends on transaction policy. |

## Response Source Matrix

| Response field | Type | Source type | Candidate source | Step | Transform | Gap |
|---|---|---|---|---:|---|---|
| data.id | int64 | Candidate database value | assignment_submissions.id | 5 | Generated ID only if source confirms database generation | ID generator/return mechanism SOURCE_REQUIRED. |
| data.assignment_id | int64 | Path / candidate row | path assignment_id / assignment_submissions.assignment_id | 2/5 | Direct candidate mapping | DDL permits NULL despite required logical field. |
| data.user_id | int64 | Auth principal / candidate row | validated token subject / assignment_submissions.user_id | 0/5 | Must not come from request | API #35 auth integration is not wired; DDL permits NULL. |
| data.content | string? | Request / candidate row | text / assignment_submissions.content | 1/5 | Candidate direct mapping | Required request versus optional response/nullable column; empty/null rule open. |
| data.files[] | UploadAsset[] | API #34 reference / SOURCE_REQUIRED | No confirmed physical collection source | 1/5 | No transform selected | One file_url column does not define UploadAsset[] mapping. |
| data.status | SubmissionStatus | AC-17 / candidate row | AC-17 says SUBMITTED; assignment_submissions.status | 5 | Initial value candidate SUBMITTED | Full enum and update transition rules open. |
| data.submitted_at | date-time | Generator / candidate row | assignment_submissions.submitted_at | 5 | SOURCE_REQUIRED | Clock source, timezone and serialization unspecified. |
| data.score | decimal-string? | Candidate row | assignment_submissions.score | 5 | SOURCE_REQUIRED | Grading and decimal conversion not defined for API #35. |
| data.feedback | string? | Candidate row | assignment_submissions.feedback | 5 | SOURCE_REQUIRED | API #35 does not define value or disclosure rule. |
| success | boolean | Envelope constant | Shared ApiEnvelope | 6 | true on success; false on error | Always present. |
| businessCode | string | Catalog branch | API #35 business code | 6 | Exact catalog value | Preserve catalog codes only. |
| message | string | Safe branch message | Application policy | 6 | Safe illustrative text | Exact message/localization is open. |
| data | object/null | Envelope branch | Submission or null | 6 | ApiEnvelope<Submission> / null on error | Shared API Guidelines. |
| meta | object | Envelope | Shared ApiEnvelope | 6 | {} unless supported metadata applies | No API-specific shape. |
| traceId | uuid | Correlation generator | Shared middleware/guideline | 6 | Propagate request trace ID | Current API #35 runtime unverified. |

## 0. Authentication and authorization

### 0.1. Validate Student authentication

- Require Bearer JWT and Student role per API catalog.
- Current Study auth helper supports Bearer/JWT validation and Student role checks for wired APIs; API #35 does not call it because the route is absent.
- Missing or invalid authentication maps to API #35 catalog error 401.
- An authenticated non-Student role maps to catalog error 403.

### 0.2. Resolve actor identity

- Candidate principal identity is the authenticated token subject.
- Do not accept user_id from path, query or body.
- Exact API #35 claim-to-row mapping is not runtime-verified.

### 0.3. Check assignment permission

- AC-17 requires the Student to have permission to submit.
- The source does not define enrollment status, assignment/course visibility, ownership or direct-call predicate.
- Do not copy API #33's unresolved access query as if it were approved.
- If access is denied, use 403 DESIGN_ACCESS_DENIED per catalog; exact predicate is SOURCE_REQUIRED.

## 1. Validate request

### 1.1. Read path and body

- assignment_id: required int64 path parameter.
- text: required string body field per catalog.
- file refs: required string in the catalog's exact notation.
- The exact JSON property name and file-reference serialization remain unresolved.

### 1.2. Validate declared shape

- Catalog includes 422 DESIGN_VALIDATION_ERROR for request validation failures.
- Do not invent min/max text length, nonempty-text rule, file-reference format, file count, URL/ID syntax or duplicate-reference behavior.
- API catalog does not state a media type; application/json is documented as a draft convention only.
- Idempotency-Key is not declared for API #35; applicability under shared guidelines is open.

## 2. Locate assignment

### 2.1. Candidate lookup

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| assignments AS a | a.id | Assignment ID | Candidate lookup by path ID; design-only. |
| ↑ | a.course_id | Course association | Candidate context for access; DDL permits NULL. |
| ↑ | a.due_at | Assignment deadline | Nullable; DB table note says NULL means no deadline. |

- Candidate condition: a.id = path assignment_id.
- No course/enrollment join or visibility predicate is selected.
- If no assignment is found, return catalog 404 DESIGN_RESOURCE_NOT_FOUND.

### 2.2. Check permission and deadline

- AC-17 precondition says the assignment is not overdue and the Student has permission.
- Access predicate and deadline boundary/timezone are SOURCE_REQUIRED.
- AC-17 shows overdue/no permission as 403/409, and API #35 catalog includes both codes; the exact condition-to-code mapping is not stated.
- Do not equate every late submission or denied access to one code without owner policy.

## 3. Resolve submission branch

- AC-17 labels the operation INSERT/UPDATE and initial status SUBMITTED.
- It does not define whether an existing row is replaced, whether multiple attempts are allowed, or which status permits update.
- Candidate lookup Q2 uses assignment_id and authenticated user_id only as possible identifying values; DDL has no unique constraint on that pair.
- If zero/multiple matching rows exist, branch and conflict behavior remain SOURCE_REQUIRED.

## 4. Candidate submission mutation

### 4.1. Candidate insert

- Refer to [07_assignment_submissions_insert_update.md](./07_assignment_submissions_insert_update.md) for candidate table field mapping.
- Candidate assignment_id comes from the path.
- Candidate user_id comes from the authenticated Student principal.
- Candidate content comes from request text; requiredness/empty behavior is unresolved against nullable storage.
- Candidate file_url comes from file refs only if an approved mapping defines a single URL/reference; current sources do not.
- AC-17 supplies initial status SUBMITTED.
- submitted_at source, transaction boundary, ID generation and score/feedback initialization are SOURCE_REQUIRED.

### 4.2. Candidate update

- AC-17 mentions UPDATE but does not specify the target row key or eligible status.
- Do not overwrite score/feedback, replace files, reset submitted_at or change status transitions without an approved rule.
- Transaction and concurrency behavior are SOURCE_REQUIRED.

### 4.3. External calls

- AC-17 invokes API #34 POST /api/v1/uploads before API #35 when a file is needed.
- API #35's catalog body contains references, not binary file bytes.
- No direct Object Storage call is assigned to API #35 by the available sources.
- Asset binding, validation and cleanup across API #34 and #35 are unresolved.

## 5. Map response

- Return the logical Submission schema in the catalog.
- Candidate physical sources are listed in the response matrix and mapping sheet.
- The exact returned row/projection after an insert/update is not specified.
- files must remain UploadAsset[] in the logical contract; do not flatten it to file_url or invent an association table.
- Use only a status value supported by AC-17 for the initial submission: SUBMITTED.
- Preserve optional score and feedback as unresolved/absent unless a source defines values.

## 6. Return response

### 6.1. Success

- HTTP 201 DESIGN_RESOURCE_CREATED per API catalog.
- Return ApiEnvelope<Submission>.
- Use data=null on errors; include safe message, meta and traceId per API Guidelines.
- Do not add 503; it is not in the API #35 catalog error set.

### 6.2. Error

- Refer to [06_Error.md](./06_Error.md) for the exact API #35 status and business-code set.
- Error messages are illustrative; exact localized copy is not specified.
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
