---
title: "Request"
order: 3
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: markdown
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
| --- | --- |
| HTTP method | `POST` |
| URI | `/api/v1/auth/register` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json; charset=utf-8` |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
| ---: | --- | --- | ---: | --- | --- | --- |
| 1 | Contents type | `Content-Type` | Yes | `application/json; charset=utf-8` | Request JSON. | [1.1](./05_Data_Mapping.md#dm-1-1) |
| 2 | Idempotency key | `Idempotency-Key` | Yes | Random/UUID `16–128` ký tự | Bắt buộc cho register; scope theo principal + method + normalized path. | [1.1](./05_Data_Mapping.md#dm-1-1) |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
| ---: | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| N/A | N/A | N/A | N/A | No | N/A | N/A | N/A | N/A | N/A | N/A — Endpoint không có Path parameter. | N/A |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
| ---: | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| N/A | N/A | N/A | N/A | No | N/A | N/A | N/A | N/A | N/A | N/A — Endpoint không có Query parameter. | N/A |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
| ---: | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| 1 | Email | `email` | string | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | Unicode text | Email | Canonical email sau trim/normalize; case-insensitive | N/A | Dùng unique lookup và insert encrypted/normalized email. | [1.2](./05_Data_Mapping.md#dm-1-2) |
| 2 | Password | `password` | string | Yes | 12 | 128 | Unicode text | Password | Policy chi tiết SOURCE_REQUIRED | N/A | Chỉ dùng để tạo Argon2id hash; không persist/log raw password. | [1.3](./05_Data_Mapping.md#dm-1-3) |
| 3 | Agreement versions | `agreementVersions` | array<string> — DERIVED | TBD | SOURCE_REQUIRED | SOURCE_REQUIRED | Unicode text | Version identifiers | Exact document/version schema SOURCE_REQUIRED | N/A | Xác nhận các phiên bản điều khoản đã chấp nhận. | [1.4](./05_Data_Mapping.md#dm-1-4) |
| 3.1 | Agreement version item | `agreementVersions[]` | string — DERIVED | TBD | SOURCE_REQUIRED | SOURCE_REQUIRED | Unicode text | SOURCE_REQUIRED | Không null/blank; duplicate rule SOURCE_REQUIRED | N/A | Một version trên một item; physical acceptance schema chưa có. | [1.4](./05_Data_Mapping.md#dm-1-4) |
| 4 | Locale | `locale` | string | TBD | SOURCE_REQUIRED | 10 — DERIVED từ DB | Unicode text | Locale code | Allowlist SOURCE_REQUIRED | `vi-VN` — DERIVED từ DB default | Locale cho account pending. | [1.5](./05_Data_Mapping.md#dm-1-5) |

> Mỗi field nằm trên một row riêng. Exact agreement field schema và locale required/default chưa được canonical API contract định nghĩa.

## Ví dụ Request data

```json
{
  "email": "user@example.com",
  "password": "SOURCE_REQUIRED_VALID_PASSWORD",
  "agreementVersions": [
    "SOURCE_REQUIRED"
  ],
  "locale": "vi-VN"
}
```

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
