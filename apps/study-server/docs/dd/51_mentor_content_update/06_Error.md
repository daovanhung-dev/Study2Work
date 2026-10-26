---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "51"
api_name: "Cập nhật nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các lỗi runtime của API #51 dùng đúng status/business code trong catalog. Body validation dựa trên body `DERIVED`; path malformed maps 404 theo implementation convention của API #48. Các lỗi database không đưa SQL detail ra response.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Yes | `Authorization` | Thiếu/sai Bearer, JWT không hợp lệ | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | N/A | Step 0 | No | Catalog direct. |
| 2 | Authorization | Yes | role | JWT không có role `MENTOR` | 403 | `DESIGN_ACCESS_DENIED` | N/A | Step 0 | No | Catalog direct. |
| 3 | Resource | Yes | `content_id` | Signed-int64 parse lỗi hoặc Content absent/soft-deleted | 404 | `DESIGN_RESOURCE_NOT_FOUND` | N/A | Steps 1–2 | Yes | Invalid path -> 404 is current implementation convention. |
| 4 | Authorization | Yes | stored course owner | `courses.mentor_id` không khớp principal | 403 | `DESIGN_ACCESS_DENIED` | N/A | Step 3 | Yes | Direct-owner fallback derived from #49. |
| 5 | Validation | Yes | body | Thiếu field, sai type, `payload` không phải object hoặc có field thừa | 422 | `DESIGN_VALIDATION_ERROR` | N/A | Step 1 | No | Validation rules derived from API #50 request model. |
| 6 | System error | No | Q1/Q2/Q3 | Query/serialization/version/update projection fails | 500 | `DESIGN_INTERNAL_ERROR` | N/A | Steps 2–5 | Yes | Safe message; rollback transaction. |
| 7 | System error | No | transaction | Commit fails | 500 | `DESIGN_INTERNAL_ERROR` | N/A | Step 6 | Yes | Rollback attempted; private DB detail is not returned. |

Catalog code set is exactly 401/403/404/422/500. No 409 is added; row lock serializes concurrent API #51 updates but no optimistic conflict token is defined.

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
