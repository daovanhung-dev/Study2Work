---
title: "Request"
order: 3
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: markdown
dd_id: "52"
api_name: "Publish/unpublish nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| API ID | #52 |
| Method | PATCH |
| Endpoint | /api/v1/mentor/content/{content_id}/publish |
| Authentication | Bearer JWT |
| Authorization | role=Mentor; AC-22 also requires permission to manage the course containing Content. |
| Character encoding | UTF-8 |
| Content-Type | Not declared by catalog; application/json applies only if the proposed body is approved. |
| Path parameters | content_id |
| Query parameters | None declared |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer token | Authenticates Mentor; token shape and Mentor identity binding need confirmation. | 0.1 |
| 2 | Content-Type | Content-Type | Only if proposed body is approved | application/json | The catalog and diagram do not declare a body or content type. | 1 |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | Content identifier | content_id | int64 | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | Integer | Positive range/overflow behavior SOURCE_REQUIRED | N/A | Selects the Content whose publication state is requested. | 2.1 |

## Query parameters

Không có query parameter theo catalog và AC-22.

## Request body

### Canonical contract

Catalog row #52 và AC-22 PATCH node chỉ khai báo path content_id; body chưa được định nghĩa.

### Proposed body — DERIVED, cần contract owner xác nhận

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| 1 | Target publication state | published | boolean | Yes, if proposal accepted | N/A | N/A | JSON boolean | true/false | true=publish; false=unpublish | N/A | Requests the desired final state; avoids an implicit toggle. This field is not in the current catalog. | 3.1 |

### Proposed request example — not canonical or integration-ready

~~~json
{
  "published": true
}
~~~

The JSON example demonstrates only the proposed target-state field. It must not be treated as an approved request schema until the contract is updated.

## Request Usage Matrix

| Request item | Read/validate | Query or mutation use | Response use | Evidence/status |
|---|---|---|---|---|
| Authorization | Verify Bearer token and Mentor role | Resolve access to stored Content course | Never echo token or claims | Role DIRECT; principal binding SOURCE_REQUIRED |
| content_id | Required int64 path | Locate Content and current publication state | data.id | Type DIRECT; physical lookup SOURCE_REQUIRED |
| Canonical body | Not declared | None | None | Catalog and diagram DIRECT omission |
| Proposed published | Boolean target state | Choose publish or unpublish transition | Reflected in resulting data.status only | DERIVED; confirm request contract |
| Query parameters | None | None | None | DIRECT omission |

## Contract response khi request sai

Catalog khai báo HTTP 422 DESIGN_VALIDATION_ERROR. Chi tiết lỗi body chỉ có thể áp dụng nếu proposal published được chấp thuận. Không thêm 400, 409 hoặc business code mới.

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `1.Request`
- Dimension: `A1:BR34`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `62`
- Số vùng merge: `25`

<details>
<summary>Danh sách vùng merge</summary>

- `S16:T16`
- `U16:V16`
- `W18:X18`
- `W19:X19`
- `U19:V19`
- `S19:T19`
- `U18:V18`
- `S17:T17`
- `S18:T18`
- `AK18:BA18`
- `S15:T15`
- `U15:V15`
- `W15:X15`
- `U14:V14`
- `W14:X14`
- `W17:X17`
- `S13:T14`
- `U13:X13`
- `U17:V17`
- `W16:X16`
- `Y13:AA14`
- `AB14:AD14`
- `AE14:AG14`
- `AB13:AG13`
- `AH13:AJ14`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | HTTP method |  |
| 2 | `L2` | GET/POST |  |
| 3 | `B3` | URI |  |
| 4 | `B4` | Code ký tự |  |
| 4 | `L4` | UTF-8 |  |
| 6 | `B6` | Request header |  |
| 7 | `B7` | Name |  |
| 7 | `J7` | Field name |  |
| 7 | `V7` | Giá trị |  |
| 7 | `AK7` | Giải thích |  |
| 8 | `B8` | Contents type |  |
| 8 | `J8` | Content-Type |  |
| 8 | `V8` | application/json |  |
| 8 | `AK8` | Thực hiện request bằng json data |  |
| 9 | `B9` | Basic authen |  |
| 9 | `J9` | Authorization |  |
| 9 | `V9` | Token |  |
| 11 | `B11` | Request data |  |
| 12 | `B12` | No |  |
| 12 | `C12` | Key name |  |
| 12 | `S12` | Nội dung check |  |
| 12 | `AK12` | Giải thích |  |
| 13 | `S13` | Bắt buộc |  |
| 13 | `U13` | Số ký tự |  |
| 13 | `Y13` | Loại ký tự |  |
| 13 | `AB13` | Format |  |
| 13 | `AH13` | Giá trị hợp lệ |  |
| 14 | `C14` | Logic |  |
| 14 | `K14` | Vật lý |  |
| 14 | `U14` | Tối thiểu |  |
| 14 | `W14` | Tối đa |  |
| 15 | `B15` | 1 |  |
| 15 | `S15` | ○ |  |
| 15 | `U15` | 1 |  |
| 15 | `W15` | 20 |  |
| 15 | `Y15` | halfsize |  |
| 16 | `B16` | 2 |  |
| 16 | `S16` | ○ |  |
| 16 | `U16` | 1 |  |
| 16 | `W16` | 8 |  |
| 16 | `Y16` | halfsize |  |
| 16 | `AB16` | datetime |  |
| 16 | `AE16` | yyyyMMdd |  |
| 17 | `S17` | ○ |  |
| 17 | `U17` | 1 |  |
| 17 | `W17` | 1 |  |
| 17 | `Y17` | halfsize |  |
| 17 | `AB17` | numberic |  |
| 17 | `AH17` | 2,3,4 |  |
| 18 | `S18` | ○ |  |
| 18 | `U18` | 1 |  |
| 18 | `Y18` | fullsize |  |
| 19 | `S19` | ○ |  |
| 19 | `U19` | 1 |  |
| 25 | `B25` | Ví dụ về Request data |  |
| 26 | `L26` | { |  |
| 27 | `M27` | "tnorsh_pln_id" : "0000000001", |  |
| 28 | `M28` | "yt_ymd":" 20201001", |  |
| 29 | `M29` | "yt_hmi":" 0830", |  |
| 30 | `M30` | "excpt_id":" 001", |  |
| 31 | `M31` | "bik_desc":" 計画削除" |  |
| 32 | `L32` | } |  |

</details>
