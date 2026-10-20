---
title: "Data Mapping"
order: 5
dd_id: "34"
api_name: "Upload file"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
Bearer JWT -> check Student/Mentor role -> parse multipart fields
-> validate only catalog-required shape -> send file to Object Storage
-> map storage/upload result to UploadAsset -> ApiEnvelope success/error
~~~

API #34 is design-only. The sequence below records contract-backed steps and keeps unspecified checks or mappings open.

## Request Usage Matrix

| Request field | Source | Data Mapping step | Validate | Storage/mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---|---|---|---|---|---|
| Authorization | header Authorization | 0.1-0.3 | Bearer JWT per catalog | Principal/role scope | 0.3 | No direct response mapping | Exact API #34 auth guard is not wired. |
| Content-Type | header Content-Type | 1.1 | multipart/form-data | Select multipart parser | 1.2 | No direct response mapping | Boundary/parser behavior is not documented for API #34. |
| file | multipart part file | 1.2, 3.1 | Required binary part per catalog | Object Storage write | 3.1-3.2 | Candidate input to name/content_type/size_bytes | MIME, size, filename and byte-inspection policies SOURCE_REQUIRED. |
| purpose | multipart part purpose | 1.2, 2.1 | Required UploadPurpose field | Purpose-specific scope/metadata is not specified | 2.1 | No direct response mapping | Enum values and role mapping SOURCE_REQUIRED. |
| course_id | multipart part course_id | 1.2, 2.1 | Optional int64 per catalog | Course association/authorization is not specified | 2.1 | No direct response mapping | Existence, ownership and role-specific requirement SOURCE_REQUIRED. |

## Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| N/A | No DB query is specified by API #34 contract or AC-17/AC-21. | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Any course ownership lookup remains SOURCE_REQUIRED; no query is invented. |

## Mutation Matrix

| Mutation ID | Operation | Target table/API | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| M1 | Upload binary object | External Object Storage | Object key and overwrite policy SOURCE_REQUIRED | File bytes and storage metadata | Required multipart file; exact metadata source open | Not specified | N/A — not a database table | No DB transaction specified; cleanup policy SOURCE_REQUIRED | 503/500 codes exist in catalog; provider condition mapping needs confirmation. |

## Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| data.id | int64 | SOURCE_REQUIRED | No table or ID generator found | 4.1 | SOURCE_REQUIRED | Required by UploadAsset | Asset identity source is undefined. |
| data.name | string | Request/storage candidate | Original filename or storage result not selected | 4.1 | SOURCE_REQUIRED | Required by UploadAsset | Filename normalization/retention is undefined. |
| data.url | uri | External result candidate | Object Storage upload result | 3.2/4.1 | Return storage URL; public/signed policy unresolved | Required by UploadAsset | URL shape, access and expiry are undefined. |
| data.content_type | string | Request/storage candidate | Multipart part or detected content not selected | 3.1/4.1 | SOURCE_REQUIRED | Required by UploadAsset | Trust/detection and supported values are undefined. |
| data.size_bytes | int64 | Uploaded binary candidate | Byte count source unspecified | 3.1/4.1 | SOURCE_REQUIRED | Required by UploadAsset | Measurement and maximum size are undefined. |
| data.status | UploadStatus | SOURCE_REQUIRED | No enum or metadata source found | 4.1 | SOURCE_REQUIRED | Required by UploadAsset | Values and lifecycle are undefined. |
| success | boolean | Envelope constant | Branch result | 5.1-5.5 | true on success; false on error | Always present | Shared envelope. |
| businessCode | string | Branch constant | API catalog | 5.1-5.5 | Catalog code for branch | Always present | Preserve API #34 code set. |
| message | string | Branch message | Application policy | 5.1-5.5 | Safe message | Always present | Exact text/localization undefined. |
| meta | object | Envelope default | N/A | 5.1-5.5 | {} unless supported error details | Always present | No upload-specific metadata schema. |
| traceId | uuid | Correlation generator | Shared middleware/API Guidelines | 5.1-5.5 | Request correlation UUID | Always present | API #34 runtime not verified. |

## 0. Check quyền

### 0.1. Get authorization header

- Read Authorization from the request header.
- Do not accept user_id or object key from the client.
- Parse multipart Content-Type and its boundary according to the selected server framework; API #34 parser is not implemented.

### 0.2. Validate Bearer JWT

- Require a valid Bearer JWT per API catalog.
- Current Study auth utilities expose a Student-only request guard for existing routes; no API #34 guard exists.
- The current access-claim parser normalizes role claims to uppercase; this is current helper behavior, not proof that API #34 supports Mentor.

### 0.3. Check allowed role

- Continue for a role allowed by the catalog: Student or Mentor.
- If authentication is absent/invalid, refer to [06_Error.md](./06_Error.md), case 1.
- If authenticated principal lacks an allowed role, refer to [06_Error.md](./06_Error.md), case 2.
- Purpose/course authorization rules are SOURCE_REQUIRED; do not infer them from the surrounding client flow.

## 1. Validate request

### 1.1. Check transport shape

- The API catalog declares multipart fields.
- The contract does not specify accepted part media type, maximum request size, or extra-field behavior.
- Do not apply API #13 JSON Data URL parsing to this endpoint.

### 1.2. Read multipart fields

- file: required binary part.
- purpose: required UploadPurpose part.
- course_id: optional int64 part.
- Rejecting or normalizing additional multipart fields is not specified.

### 1.3. Validate declared field shape

- If required file or purpose is absent, map to the catalog's 422 validation family; exact field error details are SOURCE_REQUIRED.
- If course_id is present, parse it as int64; positive range and resource-existence rules are SOURCE_REQUIRED.
- Do not invent supported purposes, MIME allowlist, file-size limit, filename policy, malware scan, or signature rules.

## 2. Resolve purpose and course scope

### 2.1. Check role-purpose relationship

- Catalog allows Student and Mentor roles.
- AC-17 uses the upload in a Student assignment-submission flow.
- AC-21 uses the upload in a Mentor lecture/media flow.
- The UploadPurpose values and allowed role-purpose pairs are not defined; retain SOURCE_REQUIRED.

### 2.2. Check course context

- course_id is optional in the catalog.
- AC-21 shows a selected course before upload; it does not define whether course_id is required for that purpose or how ownership is verified.
- AC-17 does not define whether the assignment's course must be sent or how it is bound to the uploaded file.
- Do not add a course lookup or claim an ownership check absent an approved rule.

## 3. Upload to Object Storage

### 3.1. Send binary object

- AC-17 describes Object Storage saving the submission file.
- AC-21 describes Object Storage saving media.
- Send the uploaded file to Object Storage as the external side effect required by those flows.
- Object key, bucket, metadata tags, overwrite behavior, streaming/buffering and retry policy are SOURCE_REQUIRED.
- No uploads DB table or physical metadata mapping is specified by the current ERD/table notes.

### 3.2. Check external result

- A successful upload must provide the information needed to form the required UploadAsset response.
- Whether the storage provider returns or the application generates id, url, name, content_type, size_bytes and status is SOURCE_REQUIRED.
- Public versus signed URL and expiry policy are SOURCE_REQUIRED.
- Map dependency-unavailable and unexpected failures only to the catalog error set; exact provider condition mapping is open.
- API #13 uses a separate avatar provider and its fixed key/error behavior is not reused.

## 4. Map UploadAsset response

### 4.1. Map required fields

- Map data.id as int64; source/generator is SOURCE_REQUIRED.
- Map data.name as string; original-versus-normalized filename is SOURCE_REQUIRED.
- Map data.url as URI; access/expiry policy is SOURCE_REQUIRED.
- Map data.content_type as string; request-versus-detected source is SOURCE_REQUIRED.
- Map data.size_bytes as int64; byte-count rule is SOURCE_REQUIRED.
- Map data.status as UploadStatus; enum values/lifecycle are SOURCE_REQUIRED.
- Do not add storage key, bucket name, or upload token to the response.

## 5. Return response

### 5.1. Success

- HTTPStatus = 201.
- success = true.
- businessCode = DESIGN_RESOURCE_CREATED.
- Return ApiEnvelope<UploadAsset> using only the catalog fields.
- meta = {} unless a separately approved envelope field applies.
- traceId follows the shared API Guidelines.

### 5.2. Authentication error

- Return HTTP 401 and DESIGN_AUTHENTICATION_REQUIRED.
- Set success = false and data = null.

### 5.3. Authorization error

- Return HTTP 403 and DESIGN_ACCESS_DENIED.
- Set success = false and data = null.

### 5.4. Validation error

- Return HTTP 422 and DESIGN_VALIDATION_ERROR.
- Set success = false and data = null.
- Keep field-level details safe and place them under the shared error metadata convention.

### 5.5. Dependency/internal error

- Use HTTP 503 with DESIGN_DEPENDENCY_UNAVAILABLE for a dependency-unavailable branch, or HTTP 500 with DESIGN_INTERNAL_ERROR for an unexpected internal branch.
- Exact provider failure classification remains open; do not copy API #13's 500-only behavior.
- Set success = false and data = null for either branch.
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
