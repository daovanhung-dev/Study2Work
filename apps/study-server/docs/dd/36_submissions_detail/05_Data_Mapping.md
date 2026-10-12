---
title: "Data Mapping"
order: 5
dd_id: "36"
api_name: "Xác nhận dữ liệu đã nộp"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

## 0. Authentication and access

### 0.1. Authenticate Bearer token and Student role

- Read Authorization as Bearer JWT.
- Missing or invalid authentication returns 401 DESIGN_AUTHENTICATION_REQUIRED.
- Require the Student role per the API catalog; another role returns 403 DESIGN_ACCESS_DENIED.
- Current reusable Study helper validate_current_user_request validates Bearer/JWT claims and the Student role; API #36 does not call it because the route is not wired.

### 0.2. Apply submission access policy

- The caller identity must come from the authenticated principal; the request has no user_id field.
- Whether the caller must own the submission, satisfy enrollment/course access, or meet another predicate is SOURCE_REQUIRED.
- Do not return the row until an approved resource-access predicate has passed.
- The catalog includes both 403 and 404; whether a row owned by another Student is denied as 403 or masked as 404 is SOURCE_REQUIRED.

## 1. Validate request

### 1.1. Read path parameter

- submission_id is required and has catalog type int64.
- No query parameter or request body is declared.
- Positivity, numeric range and invalid-path parse behavior are not specified.
- The API catalog does not include 400 or 422; do not add either status to the contract.

## 2. Get submission information

### 2.1. Candidate query

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| assignment_submissions AS s | s.id | Submission ID | Candidate primary key lookup; design-only. |
| ↑ | s.assignment_id | Assignment ID | Candidate field; DDL permits NULL. |
| ↑ | s.user_id | Student ID | Candidate field; use in access evaluation only if approved. |
| ↑ | s.content | Submission content | Candidate nullable field. |
| ↑ | s.file_url | Stored file URL | Candidate single-file field; not an UploadAsset[] mapping. |
| ↑ | s.submitted_at | Submission time | Candidate TIMESTAMP; timezone semantics unresolved. |
| ↑ | s.score | Score | Candidate nullable field; Student disclosure policy unresolved. |
| ↑ | s.feedback | Feedback | Candidate nullable field; Student disclosure policy unresolved. |
| ↑ | s.status | Submission status | Candidate field; default SUBMITTED; full enum unresolved. |

### 2.2. Candidate lookup condition

- s.id = path submission_id.
- No assignment, enrollment, course, or asset join is selected because the access and files policies are not defined.
- Candidate table and key come from design artifacts; no runtime query or live schema is verified.

### 2.3. Check result and access

- If the candidate lookup returns zero rows, return 404 DESIGN_RESOURCE_NOT_FOUND.
- If a row is found, apply the approved access predicate before mapping or returning data.
- If access is denied, the catalog permits 403 DESIGN_ACCESS_DENIED; whether to mask the row as 404 is an open question.
- If multiple rows appear despite the candidate primary key, treat the physical schema/query behavior as SOURCE_REQUIRED; do not invent a selection rule.

## 3. Insert/Update information

- N/A — API #36 is read-only and the contract defines no mutation.
- Refer to [07_table.md](./07_table.md) for the read-only prototype disposition.

## 4. Check query result and return response

### 4.1. Success

- HTTPStatus = 200.
- businessCode = DESIGN_RESOURCE_RETRIEVED.
- Map each logical Submission field according to [04_Response.md](./04_Response.md).
- Keep files as UploadAsset[] in the logical contract; physical mapping remains SOURCE_REQUIRED.
- Do not reveal or suppress score/feedback based on an invented release rule.

### 4.2. Authentication and access errors

- Return 401 or 403 only with the matching catalog business code.
- See [06_Error.md](./06_Error.md) for the exact error set and unresolved row-masking behavior.

### 4.3. Resource not found

- HTTPStatus = 404.
- businessCode = DESIGN_RESOURCE_NOT_FOUND.
- data = null.

### 4.4. System error

- HTTPStatus = 500.
- businessCode = DESIGN_INTERNAL_ERROR.
- Return a safe message; do not expose SQL, stack traces or internal provider details.

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
