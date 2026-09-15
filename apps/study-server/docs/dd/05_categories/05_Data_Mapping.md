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

| Request field | Source | Validate | Query usage | Response usage | Gap |
|---|---|---|---|---|---|
| `locale` | `query["locale"]` khi có | Optional; `string` shape/type | Locale filter/selection nếu category source hỗ trợ | Không map trực tiếp vào response | Enum, fallback và translation semantics TBD |

## Query Matrix

| Query ID | Mục đích | Type | Base table/API | Column/field | Condition | Result variable | Branch |
|---|---|---|---|---|---|---|---|
| `Q1` | Đọc danh mục đang hoạt động | `READ` | `Category source/store (physical target TBD)` | `id`, `name`, `slug`, `description` | `active = true`; áp dụng `locale` nếu source hỗ trợ | `active_categories` | Result → map page; empty → 200 empty page |

## Mutation Matrix

| Mutation ID | Operation | Target table/API | Record condition | Fields | Value sources | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| `M1` | `N/A — READ ONLY` | `N/A` | `N/A` | `N/A` | `N/A` | [07_table.md](./07_table.md) | `N/A` | Không tạo/update/delete DB record |

## Response Source Matrix

| Response field | Type | Source type | Source | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `success` | `boolean` | Branch constant | Processing result | `5.1/5.2/5.3` | `true` only on successful read | `N/A` | N/A |
| `businessCode` | `string` | Branch constant | Contract | `5.1/5.2/5.3` | Fixed `DESIGN_*` code | `N/A` | N/A |
| `message` | `string` | Branch message | Application | `5.1/5.2/5.3` | Fixed by branch | Text TBD | N/A |
| `data.items[].id` | `int64` | Category source | Category source `id` | `4.3` | Direct mapping | `N/A` | Physical source TBD |
| `data.items[].name` | `string` | Category source | Category source `name` | `4.3` | Locale-aware when supported | `N/A` | Locale semantics TBD |
| `data.items[].slug` | `string` | Category source | Category source `slug` | `4.3` | Direct mapping | `N/A` | Physical source TBD |
| `data.items[].description` | `string` | Category source optional | Category source `description` | `4.3` | Direct mapping | `TBD — null/omit` | Physical source TBD |
| `data.pagination.page` | `int32` | Derived | Result page | `5.1` | Fixed `1` | `N/A` | Single-page convention |
| `data.pagination.size` | `int32` | Derived | Result count | `5.1` | `total` | `0` when empty | Single-page convention |
| `data.pagination.total` | `int64` | Derived | Count of active categories | `4.3` | Count result | `0` when empty | Physical count query TBD |
| `data.pagination.total_pages` | `int32` | Derived | Single-page rule | `5.1` | Fixed `1` | `1` | Single-page convention |
| `meta` | `object` | Envelope default | `N/A` | `5.1/5.2/5.3` | `{}` | `{}` | No extra metadata contract |
| `traceId` | `uuid` | Correlation generator | `N/A` | `5.1/5.2/5.3` | None | `TBD — exact generator` | Generator TBD |

## 0. Check quyền

### 0.1. Public endpoint

- API là public theo contract; không đọc hoặc decode Bearer token.
- Không có authorization query hoặc role check.

## 1. Cache-first condition

### 1.1. Check client cache

- UI kiểm tra cache category trước khi gọi API.
- Nếu cache hit và còn được UI chấp nhận: dùng cache, không gửi request.
- Nếu cache miss: tiếp tục xử lý `2`.
- Cache TTL, cache headers và invalidation policy chưa được source xác nhận; không tự đặt giá trị.

## 2. Get request data

### 2.1. Get request header

- `authorization`: không có; endpoint public.
- `content_type`: không bắt buộc vì GET không có request body.

### 2.2. Get query

- `locale`: lấy từ `query["locale"]` nếu được gửi.
- Không nhận `page`, `size`, `sort` hoặc query field khác ngoài contract.

## 3. Validate data input

### 3.1. Validate locale

- Nếu `locale` không phải `string`: trả [06_Error.md](./06_Error.md#error-cases) với `422 DESIGN_VALIDATION_ERROR`.
- Nếu `locale` không được gửi: tiếp tục xử lý `4`.
- Không tự thêm enum, length, canonicalization hoặc fallback locale.

## 4. Get active categories

### 4.1. Resolve category source

- Đọc từ category store/source chứa danh mục đang hoạt động.
- Physical table/index/API chưa được ERD hoặc contract xác nhận; không tự đặt tên bảng hoặc column vật lý.

### 4.2. Apply active/locale condition

- Chỉ lấy category đang hoạt động theo flow AC-03.
- Áp dụng `locale` khi category source hỗ trợ; nếu không có locale-specific source, giữ discrepancy/TBD thay vì tự đặt fallback.

### 4.3. Map category records

- Map từng record sang `Category.id`, `Category.name`, `Category.slug`, `Category.description`.
- Không có record vẫn là kết quả hợp lệ: `items = []`, `total = 0`.
- Nếu source read/map lỗi: đi tới `5.3`.

## 5. Check result and map response

### 5.1. Thành công

- `HTTPStatus = 200`.
- `success = true`.
- `businessCode = "DESIGN_RESOURCE_RETRIEVED"`.
- `data.items` chứa các category active.
- `data.pagination = {page: 1, size: total, total, total_pages: 1}`.
- `meta = {}`; `traceId` là request correlation UUID.
- Response schema: [04_Response.md](./04_Response.md).

### 5.2. Validation error

- HTTP `422`.
- `success = false`.
- `businessCode = "DESIGN_VALIDATION_ERROR"`.
- `data = {}`.
- Chi tiết: [06_Error.md](./06_Error.md#error-cases).

### 5.3. Internal error

- HTTP `500`.
- `success = false`.
- `businessCode = "DESIGN_INTERNAL_ERROR"`.
- `data = {}`.
- Không trả raw query, stack trace hoặc physical source detail.
- Chi tiết: [06_Error.md](./06_Error.md#error-cases).


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
