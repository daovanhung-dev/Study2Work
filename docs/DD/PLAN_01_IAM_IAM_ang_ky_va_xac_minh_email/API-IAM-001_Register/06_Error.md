---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Error contract của registration. Endpoint-specific HTTP status/message chưa được source định nghĩa được giữ `TBD`/`SOURCE_REQUIRED`.

## Error cases

<a id="error-content-type"></a>
<a id="error-idempotency-key"></a>
<a id="error-email-required"></a>
<a id="error-email-format"></a>
<a id="error-password-required"></a>
<a id="error-password-policy-failed"></a>
<a id="error-agreement-version-invalid"></a>
<a id="error-locale-invalid"></a>
<a id="error-rate-limit"></a>
<a id="error-idempotency-key-reused"></a>
<a id="error-request-in-progress"></a>
<a id="error-email-already-registered"></a>
<a id="error-dependency-unavailable"></a>
<a id="error-system"></a>

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
| ---: | --- | --- | --- | --- | ---: | --- | --- | --- | ---: | --- |
| 1 | Header validation | ○ | Content-Type | Không phải application/json | 400 | SOURCE_REQUIRED | N/A | [1.1](./05_Data_Mapping.md#dm-1-1) | No | Canonical field-level code chưa có. |
| 2 | Header validation | ○ | Idempotency-Key | Thiếu hoặc ngoài 16–128 ký tự | 400 | SOURCE_REQUIRED | N/A | [1.1](./05_Data_Mapping.md#dm-1-1) | No | Register bắt buộc key. |
| 3 | Input validation | ○ | email | Thiếu/null/blank | 400 | SOURCE_REQUIRED | N/A | [1.3](./05_Data_Mapping.md#dm-1-3) | No | Không lộ account existence. |
| 4 | Input validation | ○ | email | Sai format canonical | 400 | SOURCE_REQUIRED | N/A | [1.3](./05_Data_Mapping.md#dm-1-3) | No | Validator SOURCE_REQUIRED. |
| 5 | Input validation | ○ | password | Thiếu/null | 400 | PASSWORD_POLICY_FAILED | N/A | [1.3](./05_Data_Mapping.md#dm-1-3) | No | Field error không echo password. |
| 6 | Input validation | ○ | password | Length ngoài 12–128 hoặc vi phạm policy | 400 | PASSWORD_POLICY_FAILED | N/A | [1.3](./05_Data_Mapping.md#dm-1-3) | No | Policy ngoài length SOURCE_REQUIRED. |
| 7 | Business validation | ○ | agreementVersions | Thiếu, version cũ hoặc không hợp lệ | 400 | AGREEMENT_VERSION_INVALID | N/A | [1.4](./05_Data_Mapping.md#dm-1-4) | No | Catalog/table agreement thiếu. |
| 8 | Input validation | ○ | locale | Không thuộc allowlist | 400 | SOURCE_REQUIRED | N/A | [1.5](./05_Data_Mapping.md#dm-1-5) | No | Allowlist/source code missing. |
| 9 | Rate limit | - | email hash | Vượt 3 request/giờ/email hash | 429 | SOURCE_REQUIRED | N/A | [1.5](./05_Data_Mapping.md#dm-1-5) | No | Có Retry-After khi biết. |
| 10 | Idempotency | - | Idempotency-Key | Cùng key nhưng request hash khác | 409 | IDEMPOTENCY_KEY_REUSED | N/A | [2.5](./05_Data_Mapping.md#dm-2-2) | No | Tạo key mới sau khi xác nhận intent. |
| 11 | Idempotency | - | Idempotency-Key | Request cùng key đang chạy | TBD | REQUEST_IN_PROGRESS | N/A | [2.5](./05_Data_Mapping.md#dm-2-2) | No | HTTP status chưa được nguồn định nghĩa. |
| 12 | Duplicate account | - | email | Active normalized email đã tồn tại | TBD | EMAIL_ALREADY_REGISTERED | N/A | [3.3.2](./05_Data_Mapping.md#dm-3-3) | No | CONFLICT: sequence yêu cầu generic accepted; điều kiện phát code cần quyết định. |
| 13 | Dependency | - | Identity DB/KMS | Dependency tạm thời unavailable | 503 | DEPENDENCY_UNAVAILABLE | N/A | [4.2](./05_Data_Mapping.md#dm-4-2) | Yes | Retry theo Retry-After; kiểm idempotency trước retry. |
| 14 | System error | - | - | Unhandled lỗi trước COMMIT | 500 | SOURCE_REQUIRED | N/A | [4.2](./05_Data_Mapping.md#dm-4-2) | Yes | Không trả stack trace/SQL/secret. |

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
