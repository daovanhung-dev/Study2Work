---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "API-STU-001"
status: "PARTIALLY COMPLETED — SOURCE GAPS"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | `JSON` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json` |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `success` | Success | `success` | `boolean` | `No` | `N/A` | `N/A` | `05_Data_Mapping.md#4-check-ket-qua-execute-query` | Fixed by branch | N/A | [DIRECT] |
| 2 | `businessCode` | Business code | `businessCode` | `string` | `No` | `N/A` | `N/A` | `05_Data_Mapping.md#4-check-ket-qua-execute-query` | Fixed by branch | N/A | Success code chưa có catalog field-level. [SOURCE_REQUIRED] |
| 3 | `message` | Message | `message` | `string` | `No` | `N/A` | `N/A` | `05_Data_Mapping.md#4-check-ket-qua-execute-query` | Fixed/catalog message | N/A | [SOURCE_REQUIRED] |
| 4 | `data` | Data | `data` | `array<object>` | `Yes` | `N/A` | `N/A` | `05_Data_Mapping.md#4-check-ket-qua-execute-query` | Object/array/null mapping | Theo endpoint | [DIRECT] |
| 5 | `meta` | Metadata | `meta` | `object` | `No` | `N/A` | `N/A` | `05_Data_Mapping.md#4-check-ket-qua-execute-query` | Generated | Luôn là object | [DIRECT] |
| 6 | `traceId` | Trace ID | `traceId` | `string` | `No` | `N/A` | `N/A` | `05_Data_Mapping.md#4-check-ket-qua-execute-query` | Request context generated | N/A | [DIRECT] |
| 7 | `data[].pathId` | Path ID | `pathId` | `string` | `No` | `learning_paths` | `id` | `05_Data_Mapping.md#4-check-ket-qua-execute-query` | Direct | N/A | [DERIVED] |
| 8 | `data[].slug` | Slug | `slug` | `string` | `No` | `learning_paths` | `slug` | `05_Data_Mapping.md#4-check-ket-qua-execute-query` | Direct | N/A | [DIRECT] |
| 9 | `data[].title` | Title | `title` | `string` | `No` | `learning_path_versions` | `title` | `05_Data_Mapping.md#4-check-ket-qua-execute-query` | Direct | N/A | [DIRECT] |
| 10 | `data[].summary` | Summary | `summary` | `string` | `No` | `learning_path_versions` | `summary` | `05_Data_Mapping.md#4-check-ket-qua-execute-query` | Direct | N/A | [DIRECT] |
| 11 | `data[].publishedAt` | Published at | `publishedAt` | `string` | `No` | `learning_path_versions` | `published_at` | `05_Data_Mapping.md#4-check-ket-qua-execute-query` | ISO-8601 UTC | N/A | [DERIVED] |

## Ví dụ thành công

```json
{
  "success": true,
  "businessCode": "SOURCE_REQUIRED",
  "message": "SOURCE_REQUIRED",
  "data": [],
  "meta": {},
  "traceId": "0198a4c0-2d18-7a42-a82a-32f56e93bd10"
}
```

## Ví dụ lỗi

```json
{
  "success": false,
  "businessCode": "INVALID_FILTER",
  "message": "SOURCE_REQUIRED",
  "data": null,
  "meta": {},
  "traceId": "0198a4c0-2d18-7a42-a82a-32f56e93bd10"
}
```

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `2.Response`
- Dimension: `A2:BR45`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `52`
- Số vùng merge: `15`

<details>
<summary>Danh sách vùng merge</summary>

- `B14:C15`
- `B16:C16`
- `B21:C21`
- `B22:BA22`
- `B23:C23`
- `B24:C24`
- `D14:S14`
- `T14:AK14`
- `AL14:BA15`
- `B20:C20`
- `B17:C17`
- `B18:C18`
- `T18:AB18`
- `AC18:AK18`
- `B19:BA19`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Giải thích |  |
| 4 | `C4` | Giá trị trả về khi call API |  |
| 9 | `B9` | Format |  |
| 9 | `L9` | JSON |  |
| 10 | `B10` | Code ký tự |  |
| 10 | `L10` | UTF-8 |  |
| 11 | `B11` | Content-Type |  |
| 11 | `L11` | application/json |  |
| 14 | `B14` | No |  |
| 14 | `D14` | Response item name |  |
| 14 | `T14` | Refer DB |  |
| 14 | `AL14` | Remarks |  |
| 15 | `D15` | Tên logic |  |
| 15 | `L15` | Tên vật lý |  |
| 15 | `T15` | Table nguồn get |  |
| 15 | `AC15` | Field nguồn get |  |
| 16 | `B16` | 1 |  |
| 16 | `D16` | HTTP Status |  |
| 16 | `L16` | HTTPStatus |  |
| 16 | `AL16` | Thành công: 200/ Phát sinh lỗi: 500/ Validate lỗi: 400 |  |
| 17 | `B17` | 2 |  |
| 17 | `D17` | Status |  |
| 17 | `L17` | status |  |
| 17 | `AL17` | Thành công: 1/phát sinh error: 2 |  |
| 18 | `B18` | 3 |  |
| 18 | `D18` | Nội dung response |  |
| 18 | `L18` | response |  |
| 19 | `B19` | Trường hợp thành công |  |
| 20 | `B20` | 3.1 |  |
| 21 | `B21` | 3.2 |  |
| 22 | `B22` | Các trường hợp lỗi của API |  |
| 23 | `B23` | 3.1 |  |
| 23 | `D23` | Error code |  |
| 23 | `M23` | error_code |  |
| 24 | `B24` | 3.2 |  |
| 24 | `D24` | Error Message id |  |
| 24 | `M24` | error_message_id |  |
| 26 | `B26` | Ví dụ |  |
| 27 | `M27` | Trường hợp thành công |  |
| 28 | `N28` | { |  |
| 29 | `O29` |   "status": 1, |  |
| 30 | `O30` |   "response":{ |  |
| 33 | `O33` | } |  |
| 34 | `N34` | } |  |
| 36 | `M36` | Trường hợp lỗi |  |
| 37 | `N37` | { |  |
| 38 | `O38` | "status" : 2 , |  |
| 39 | `O39` | "response" : {  |  |
| 40 | `P40` | "error_code" : "9999", |  |
| 41 | `P41` | "error_message_id" : "DLG000000" |  |
| 42 | `O42` |  } |  |
| 43 | `N43` |  } |  |

</details>
