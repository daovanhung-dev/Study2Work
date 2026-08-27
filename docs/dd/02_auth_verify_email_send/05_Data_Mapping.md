---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

## Request Usage Matrix

| Request field | Source | Validate | External/API usage | Response usage | Gap |
|---|---|---|---|---|---|
| `user_id` | `request["user_id"]` | Required; `int64` | Provider dispatch parameter | Không map trực tiếp vào response | User existence/match rule TBD |
| `email` | `request["email"]` | Required; `email` format | Provider dispatch parameter | Không map trực tiếp vào response | Token/link policy TBD |

## Query Matrix

| Query ID | Mục đích | Type | Base table/API | Column/field | Condition | Result variable | Branch |
|---|---|---|---|---|---|---|---|
| `Q1` | Không có DB query được source xác nhận | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không tự thêm existence/match check |

## Mutation Matrix

| Mutation ID | Operation | Target table/API | Record condition | Fields | Value sources | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| `M1` | `DISPATCH` | `Email Provider` | Verification enabled; request accepted | `user_id`, `email` | Request body | `N/A — external side effect` | `N/A` | Log/retry bất đồng bộ sau acceptance; không tạo DB record |

## Response Source Matrix

| Response field | Type | Source type | Source | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `success` | `boolean` | Branch constant | Processing result | `4.1/4.2/4.3` | `true` only for accepted | `N/A` | N/A |
| `businessCode` | `string` | Branch constant | Contract | `4.1/4.2/4.3` | Fixed `DESIGN_*` code | `N/A` | N/A |
| `message` | `string` | Branch message | Application | `4.1/4.2/4.3` | Fixed by branch | Text TBD | N/A |
| `data.status` | `string` | ActionResult | Dispatch acceptance | `4.1` | `accepted` design example | `N/A` | Allowed values TBD |
| `data.reason` | `string` | ActionResult optional | Dispatch result | `4.1` | Direct when supplied | Omit when absent | Reason values TBD |
| `meta` | `object` | Envelope default | N/A | `4.1/4.2/4.3` | `{}` | `{}` | No operation_id in API #2 contract |
| `traceId` | `uuid` | Correlation generator | N/A | `4.1/4.2/4.3` | None | `N/A` | Generator TBD |

## 0. Check quyền

### 0.1. Public endpoint

- API là public theo contract; không đọc hoặc decode Bearer token.
- Không có authorization query hoặc DB lookup.

## 1. Get request data

### 1.1. Get request header

- `content_type`: lấy từ `header["Content-Type"]`; request dùng `application/json`.
- `authorization`: không có; endpoint public, không yêu cầu Bearer token.

### 1.2. Get request body

- `user_id`: lấy từ `request["user_id"]`.
- `email`: lấy từ `request["email"]`.
- Không nhận `verification_enabled`, token, link, expiry hoặc retry fields.

## 2. Validate data input

### 2.1. Validate user ID

- Nếu `user_id` thiếu hoặc không phải `int64`: trả lỗi [06_Error.md — user_id validation](./06_Error.md#error-cases).
- Không tự kiểm tra `user_id` tồn tại vì source không xác nhận query/business rule.

### 2.2. Validate email

- Nếu `email` thiếu hoặc không đúng format `email`: trả lỗi [06_Error.md — email validation](./06_Error.md#error-cases).
- Không tự đặt min/max hoặc canonicalization rule ngoài type `email`.

## 3. Verification dispatch

### 3.1. Check verification condition

- API #2 chỉ được gọi trong AC-01 khi verification được bật.
- Nếu verification không bật: flow registration không dispatch API #2; request contract không thêm field điều khiển này.

### 3.2. Dispatch to Email Provider

- Gửi `user_id` và `email` tới Email Provider để tạo/gửi mã hoặc link xác thực.
- Token/link format, expiry, retry count, email template và provider request schema chưa được source xác nhận; không tự đặc tả.
- Không có local DB insert/update/delete hoặc transaction mapping được xác nhận; xem [07_table.md](./07_table.md).

### 3.3. Accept and retry

- Khi dispatch đã được chấp nhận/xếp xử lý: đi tới `4.1`; trả HTTP `202` và `DESIGN_OPERATION_ACCEPTED`.
- Nếu Email Provider lỗi sau acceptance: ghi log và retry bất đồng bộ; không đổi response contract và không tạo account/record trùng.
- Nếu lỗi nội bộ khiến request không thể được chấp nhận/dispatch: đi tới `4.3`; trả HTTP `500`.

## 4. Check result and map response

### 4.1. Accepted

- `HTTPStatus = 202`.
- `success = true`.
- `businessCode = "DESIGN_OPERATION_ACCEPTED"`.
- `data.status = "accepted"` (design example theo operation accepted).
- `data.reason` chỉ có khi có reason; contract chưa đặc tả giá trị.
- `meta = {}`; không thêm `operation_id`.
- `traceId`: request correlation/generator; exact generator TBD.
- Response schema: [04_Response.md](./04_Response.md).

### 4.2. Validation error

- HTTP `422`.
- `success = false`.
- `businessCode = "DESIGN_VALIDATION_ERROR"`.
- `data = {}`.
- Chi tiết: [06_Error.md — validation rows](./06_Error.md#error-cases).

### 4.3. Internal error

- HTTP `500`.
- `success = false`.
- `businessCode = "DESIGN_INTERNAL_ERROR"`.
- `data = {}`.
- Không trả raw upstream body, stack trace hoặc secret.
- Chi tiết: [06_Error.md — internal error](./06_Error.md#error-cases).


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

