---
title: "Error"
order: 6
dd_id: "78"
api_name: "Lấy pending content"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

- Direct catalog #78 khai báo 401/403/500; runtime giữ nguyên các code này.
- Runtime thêm 422 `DESIGN_VALIDATION_ERROR` cho `course`/`page` sai kiểu hoặc ngoài miền. Đây là fallback DERIVED theo API #73; catalog chưa được cập nhật.
- Queue rỗng hoặc page ngoài phạm vi trả 200 empty Page theo list semantics, không dùng 404.
- Query/mapping errors trả 500 an toàn; không lộ SQL, payload internals hoặc stack trace.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Shared Bearer/JWT guard | Authorization | Token thiếu, sai hoặc hết hạn | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No query | Direct catalog; shared guard local. |
| 2 | Authorization | Shared role guard | `ADMIN` role | Principal hợp lệ nhưng thiếu role Admin | 403 | `DESIGN_ACCESS_DENIED` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No query | Role guard current source; finer permission open. |
| 3 | Query validation | Raw query parser | `course` | Not signed-int64 or overflows | 422 | `DESIGN_VALIDATION_ERROR` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-1-validate-data-input) | No DB | DERIVED; direct catalog omits 422. |
| 4 | Query validation | Raw query parser | `page` | Not positive int32 | 422 | `DESIGN_VALIDATION_ERROR` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-1-validate-data-input) | No DB | DERIVED from Admin list convention. |
| 5 | System error | Count/list/map | Pending Content page | DB error, malformed count, invalid row/payload projection | 500 | `DESIGN_INTERNAL_ERROR` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-2-get-thong-tin) | Rollback | Safe response; no mutation. |

## Empty result and invalid filters

- Empty queue/no matching `type`/`course`, and page beyond the last page return 200 `DESIGN_RESOURCE_RETRIEVED` with `items=[]`.
- Unknown `type` is not an enum-validation error; it uses exact match and may return an empty Page.
- Invalid numeric `course`/`page` returns local derived 422; contract owner should add it to API #78's error row or choose another rule.
- No 404 is added because the endpoint is a queue, not a single resource lookup.

## Error envelope

- `error_response()` currently returns the canonical six-key envelope with `data:null` by default, plus trace ID and `X-Trace-Id`.
- `/api/v1/admin/content/pending` is registered in `DESIGN_CONTRACT_PATHS`, so framework errors for the route use DESIGN business-code integration.
- Local HTTP tests verify the helper envelope and codes; fake DB sessions do not verify PostgreSQL behavior.

## Linked API boundary

- #78 does not return detail/version/author metadata from #79.
- #78 does not approve/reject, change status, store a reason or append audit; those effects belong to #80/#81.

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
