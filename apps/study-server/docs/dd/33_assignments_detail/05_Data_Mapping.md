---
title: "Data Mapping"
order: 5
dd_id: "33"
api_name: "Lấy đề bài/rule/deadline"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

<a id="0-authentication-and-access"></a>

## 0. Authentication and access

### 0.1. Validate Student authentication and role

- Nhận `Authorization: Bearer <token>` theo API catalog.
- Current helper `validate_current_user_request()` xác thực Bearer/JWT, chuẩn hóa role và trả numeric `user_id` cho request hợp lệ.
- Nếu token thiếu hoặc không hợp lệ, catalog yêu cầu HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Nếu role không chứa `STUDENT`, current helper trả HTTP 403 `DESIGN_ACCESS_DENIED`.
- API #33 chưa được đăng ký/gọi helper này; đây là current helper behavior, không phải API runtime đã xác minh.

### 0.2. Candidate assignment/course access

| Source | Field/condition | Evidence | Status |
|---|---|---|---|
| API catalog | Bearer JWT; role=Student; request chỉ nhận `assignment_id`. | API #33 row trong `docs/lists/list_api.md`. | DIRECT contract. |
| Current Study auth helper | Bearer/JWT claims trả numeric `user_id` và role list. | `apps/study-server/app/utils/auth.py`. | CURRENT_BEHAVIOR; API #33 integration chưa verified. |
| Candidate resource | `assignments.id`, `assignments.course_id`. | DB table notes, ERD và checked-in DDL. | DESIGN_ONLY. |
| Possible membership source | `enrollments.user_id`, `enrollments.course_id`, `enrollments.status`. | DB table notes mô tả quan hệ user/course; AC-17 không nêu status hoặc predicate quyền. | DESIGN_ONLY / SOURCE_REQUIRED; không lập query quyền suy đoán. |

- Không nhận `user_id` từ request.
- Predicate để xác nhận quyền Student đọc assignment/course chưa được định nghĩa.
- Không giả định việc client đã mở API khác chứng minh quyền truy cập trực tiếp API #33.

### 0.3. Check result

- Authentication failure trả 401 theo catalog.
- Role/access denial trả 403 theo catalog; exact assignment/course predicate SOURCE_REQUIRED.
- Assignment lookup không có record trả 404 theo catalog.
- AC-17 nhắc overdue/no-permission là `403/409`; mapping riêng của trạng thái deadline chưa được chốt và catalog không có 409.

<a id="1-request-validation"></a>

## 1. Request validation

- Đọc `assignment_id` từ required path parameter trong [03_Request.md](./03_Request.md).
- Catalog xác định kiểu `int64`; min/max, positivity và parse-failure behavior chưa được xác định.
- Catalog API #33 không liệt kê 400 hoặc 422; không tự thêm status/business code cho path parse lỗi.
- API không có query parameter hoặc request body.

<a id="2-read-assignment"></a>

## 2. Read candidate Assignment

### 2.1. Candidate selected columns

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| assignments AS a | a.id | Assignment ID | Candidate lookup key; design-only. |
| ↑ | a.course_id | Course ID | Required by logical Assignment; DDL permits NULL. |
| ↑ | a.name | Assignment title | Candidate source for logical `title`. |
| ↑ | a.description | Assignment description | Nullable in DDL; optional contract field. |
| ↑ | a.due_at | Submission deadline | Nullable TIMESTAMP; time-zone/serialization rule SOURCE_REQUIRED. |
| ↑ | a.max_score | Maximum score | Required logical field; DDL permits NULL and has default 10. |

### 2.2. Candidate relation

| Target table | Join condition | Join type |
|---|---|---|
| assignments AS a | N/A | BASE |

- Candidate lookup condition: `a.id = path assignment_id`.
- No join, sort, pagination or live SQL statement is specified by the contract or AC-17.
- An access/membership query, if required, remains SOURCE_REQUIRED.

### 2.3. Candidate query result

- If no assignment matches the approved lookup, catalog error is HTTP 404 `DESIGN_RESOURCE_NOT_FOUND`.
- If one assignment is found, candidate fields map to logical `Assignment` as described in [04_Response.md](./04_Response.md).
- AC-17 does not define whether a GET request to an expired assignment returns the Assignment or an error.
- AC-17's “submission rule” does not map to fields in the reusable `Assignment` schema.

<a id="3-no-mutation"></a>

## 3. Mutation and external calls

### 3.1. Database mutation

- N/A — API #33 is GET/read-only.
- No insert, update or delete is assigned to API #33.
- Transaction: N/A.

### 3.2. External calls

- No external provider or storage call is described for API #33.
- Upload/object-storage steps belong to the later API #34 flow, not this GET endpoint.

<a id="4-map-assignment-response"></a>

## 4. Map candidate Assignment response

| Response field | Candidate source | Mapping | Status / gap |
|---|---|---|---|
| `data.id` | `assignments.id` | Direct candidate projection. | Design-only; API #33 runtime query absent. |
| `data.course_id` | `assignments.course_id` | Direct candidate projection. | Required in logical contract; DDL permits NULL. |
| `data.title` | `assignments.name` | Rename physical `name` to logical `title`. | DB table notes explicitly record this naming difference. |
| `data.description` | `assignments.description` | Candidate direct projection. | Optional logical field; NULL/omit behavior open. |
| `data.due_at` | `assignments.due_at` | Candidate timestamp projection. | Optional logical field; DDL has no timezone and API format rule is open. |
| `data.max_score` | `assignments.max_score` | Candidate decimal-string projection. | Required logical field; DDL permits NULL; scale/format rule open. |
| Submission rule | N/A | No field is added to `Assignment`. | AC-17 mentions a rule, but catalog/schema provide no shape or values. |
| `meta` / `traceId` | `ApiEnvelope<T>` schema | Standard response envelope. | Shared convention; API #33 runtime serialization is unverified. |

- Do not expose physical `created_at` or `updated_at`; they are absent from the logical `Assignment` response schema.
- Do not read `assignment_submissions` unless an approved access or rule contract requires it.

<a id="5-error-branches"></a>

## 5. Error branches

- Use only the API #33 catalog errors: 401, 403, 404 and 500.
- Missing/invalid authentication maps to 401 per catalog and current helper behavior.
- Non-Student role maps to 403 per catalog and current helper behavior.
- Denied assignment/course access maps to 403 per catalog; exact predicate is SOURCE_REQUIRED.
- Missing assignment maps to catalog 404.
- AC-17's 409 for an overdue or otherwise disallowed assignment conflicts with the API #33 catalog; do not add 409 in this DD.
- Invalid `assignment_id` parse/range behavior has no catalog mapping; do not invent 400/422.
- Unexpected data-access/internal failure maps to 500 `DESIGN_INTERNAL_ERROR`; do not expose SQL or stack traces.
- Error response uses `data = null` under the shared API Guidelines.

## 6. Return response

### 6.1. Success

- HTTP 200.
- `businessCode = DESIGN_RESOURCE_RETRIEVED`.
- Return `ApiEnvelope<Assignment>` with only the fields present in the approved reusable schema.
- The contract does not define submission-rule fields or NULL/omission serialization for optional fields.

### 6.2. Error

- Use only the business codes in [06_Error.md](./06_Error.md).
- The response example does not decide deadline handling, assignment visibility or path parse behavior.
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

