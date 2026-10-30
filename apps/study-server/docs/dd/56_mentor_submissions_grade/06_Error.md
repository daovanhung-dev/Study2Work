---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "56"
api_name: "Lưu điểm bài làm Mentor"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Only the API catalog error set is used. Implemented branch conditions are identified separately from DERIVED fallbacks.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Data Mapping reference | Rollback / remarks |
|---:|---|---|---|---|---:|---|---|---|
| 1 | Authentication | Bearer/JWT and role | Authorization | Missing/invalid auth or no MENTOR role | 401 | DESIGN_AUTHENTICATION_REQUIRED | 0 | Before DB mutation; shared guard |
| 2 | Authorization | Direct course owner | Mentor access | Existing submission belongs to another course owner | 403 | DESIGN_ACCESS_DENIED | 0 | Rollback locked read; direct-owner policy DERIVED |
| 3 | Resource | Path/row lookup | submission_id | Malformed/out-of-range path or no submission row | 404 | DESIGN_RESOURCE_NOT_FOUND | 1–2 | Rollback if transaction is open |
| 4 | Validation | Strict request model | score / rubric_items | Missing or wrong JSON type; score not int32; undeclared extra body field | 422 | DESIGN_VALIDATION_ERROR | 1 | Framework/body validation before mutation |
| 5 | Validation | Derived score bounds | score | score < 0 or score > assignment.max_score | 422 | DESIGN_VALIDATION_ERROR | 1 | DERIVED fallback; rollback locked read |
| 6 | System | Persistence/projection | Database, relation or response mapping | SQL, broken required relation, invalid max_score projection, failed mapping or commit | 500 | DESIGN_INTERNAL_ERROR | 2–4 | Safe response; rollback attempted |
| 7 | Success | Update | score/status | Valid owner and score; response projection succeeds | 200 | DESIGN_RESOURCE_UPDATED | 3–4 | Commit before success response |

No 400, 409, 503 or extra business code is added. Current dynamic route template is present in DESIGN_CONTRACT_PATHS, and generic middleware validation/system errors can use the catalog DESIGN_* mapping. error_response(None) emits data=null.
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
