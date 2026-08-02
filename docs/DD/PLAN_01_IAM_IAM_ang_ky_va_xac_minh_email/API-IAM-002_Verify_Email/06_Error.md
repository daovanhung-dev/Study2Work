---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Error contract của verify-email. HTTP status cho endpoint-specific token codes chưa được canonical source định nghĩa.

## Error cases

<a id="error-content-type"></a>
<a id="error-idempotency-key"></a>
<a id="error-token-required"></a>
<a id="error-token-length"></a>
<a id="error-rate-limit"></a>
<a id="error-idempotency-key-reused"></a>
<a id="error-request-in-progress"></a>
<a id="error-token-invalid-or-expired"></a>
<a id="error-token-already-used"></a>
<a id="error-dependency-unavailable"></a>
<a id="error-system"></a>

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- | ---: | --- |
| 1 | Header validation | ○ | Content-Type | Không phải JSON | 400 | SOURCE_REQUIRED | N/A | [1.1](./05_Data_Mapping.md#dm-1-1) | No |  |
| 2 | Header validation | ○ | Idempotency-Key | Thiếu/ngoài 16–128 | 400 | SOURCE_REQUIRED | N/A | [1.1](./05_Data_Mapping.md#dm-1-1) | No |  |
| 3 | Input validation | ○ | token | Thiếu/null/blank | 400 | SOURCE_REQUIRED | N/A | [1.2](./05_Data_Mapping.md#dm-1-2) | No |  |
| 4 | Input validation | ○ | token | Length ngoài 32–512 | 400 | SOURCE_REQUIRED | N/A | [1.2](./05_Data_Mapping.md#dm-1-2) | No |  |
| 5 | Rate limit | - | IP hash | Vượt 10/phút/IP | 429 | SOURCE_REQUIRED | N/A | [1.3](./05_Data_Mapping.md#dm-1-3) | No | Retry-After khi biết. |
| 6 | Idempotency | - | Idempotency-Key | Cùng key khác request hash | 409 | IDEMPOTENCY_KEY_REUSED | N/A | [2.6](./05_Data_Mapping.md#dm-2-3) | No |  |
| 7 | Idempotency | - | Idempotency-Key | Request đang chạy | TBD | REQUEST_IN_PROGRESS | N/A | [2.6](./05_Data_Mapping.md#dm-2-3) | No | HTTP missing. |
| 8 | Token validation | - | token | Không tồn tại, sai purpose, revoked hoặc expired | TBD | TOKEN_INVALID_OR_EXPIRED | N/A | [3.3.2](./05_Data_Mapping.md#dm-3-3) | Yes | Không tạo session. |
| 9 | Token validation | - | token | Token đã consumed | TBD | TOKEN_ALREADY_USED | N/A | [3.3.2](./05_Data_Mapping.md#dm-3-3) | Yes | Không tạo session. |
| 10 | Dependency | - | Identity DB/KMS | Unavailable | 503 | DEPENDENCY_UNAVAILABLE | N/A | [4.2](./05_Data_Mapping.md#dm-4-2) | Yes |  |
| 11 | System error | - | - | Unhandled lỗi trước COMMIT | 500 | SOURCE_REQUIRED | N/A | [4.2](./05_Data_Mapping.md#dm-4-2) | Yes | No secret/stack. |

> Mỗi error case và mỗi field validation nằm trên một row riêng. `Error message ID` không tồn tại trong canonical API contract nên dùng `N/A` hoặc `SOURCE_REQUIRED`, không tự tạo ID.

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `4.Error`
- Dimension: `A1:BR13`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `30`
- Số vùng merge: `10`

<details>
<summary>Danh sách vùng merge</summary>

- `C10:F10`
- `G10:I10`
- `J10:N10`
- `O10:X10`
- `Y10:AA10`
- `G11:I11`
- `G12:I12`
- `G13:I13`
- `AB10:AF10`
- `AG10:BA10`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Giải thích |  |
| 4 | `C4` | Các trường hợp lỗi của API |  |
| 10 | `B10` | № |  |
| 10 | `C10` | Category |  |
| 10 | `G10` | Verify check |  |
| 10 | `J10` | Tên item |  |
| 10 | `O10` | Nội dung check |  |
| 10 | `Y10` | Error code |  |
| 10 | `AB10` | Error message ID |  |
| 10 | `AG10` | Remarks |  |
| 11 | `B11` | 1 |  |
| 11 | `C11` | system error |  |
| 11 | `G11` | - |  |
| 11 | `J11` | - |  |
| 11 | `O11` | Trường hợp lỗi truy cập DB |  |
| 11 | `Y11` | 9999 |  |
| 11 | `AB11` | DLG000000 |  |
| 12 | `B12` | 2 |  |
| 12 | `C12` | Check quyền |  |
| 12 | `G12` | - |  |
| 12 | `O12` | Trường hợp không có thông tin quyền tương ứng với user_id trong token |  |
| 12 | `Y12` | 1000 |  |
| 12 | `AB12` | STOCKERR1 |  |
| 12 | `AG12` | Trường hợp số record get được từ xử lý 0. của sheet [3.Data mapping] = 0 |  |
| 13 | `B13` | 3 |  |
| 13 | `C13` | check tồn tại |  |
| 13 | `G13` | 〇 |  |
| 13 | `O13` | Trường hợp không có thông tin parameter trong request data |  |
| 13 | `Y13` | 1001 |  |
| 13 | `AB13` | DLG000093 |  |

</details>
