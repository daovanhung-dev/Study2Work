---
title: "Error"
order: 6
dd_id: "98"
api_name: "Lấy đầy đủ thread + report detail"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "5. Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Catalog error set

| HTTP | Business code | Meaning | Direct/conditional handling |
|---:|---|---|---|
| 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Missing, malformed or invalid Bearer/JWT | DIRECT code; Admin authentication implementation absent |
| 403 | `DESIGN_ACCESS_DENIED` | Authenticated principal lacks Admin authorization | DIRECT code; Admin role guard/policy absent |
| 404 | `DESIGN_RESOURCE_NOT_FOUND` | Requested discussion cannot be found | DIRECT code; exact root/reply and concealment semantics unresolved |
| 500 | `DESIGN_INTERNAL_ERROR` | Internal query or required-field mapping failure | DIRECT code; route absent |

Success is HTTP 200 `DESIGN_RESOURCE_RETRIEVED`. Catalog #98 does not list 422; do not add it.

## Error branches and open behavior

| Branch | Expected code | Current evidence / unresolved |
|---|---|---|
| Bearer/JWT failure | 401 | Shared Study helper is Student-only; Admin guard/claims absent |
| Authenticated non-Admin | 403 | Admin authorization policy/scope absent |
| Discussion ID not found | 404 candidate | Catalog includes 404; exact lookup/concealment behavior not defined |
| Discussion ID points to reply | Not defined | Root-only interpretation is a DERIVED proposal; AC-37/#97 do not resolve target grain |
| Malformed/overflow path value | No code specified | Catalog omits 422; current FastAPI parse path may be intercepted before handler |
| Missing report relation/detail | 500 is not a substitute for unresolved schema | Report persistence absent; cannot define query or response projection |
| Query/mapping exception | 500 `DESIGN_INTERNAL_ERROR` | Current generic middleware would use fallback code if route not added to design allowlist |

## Envelope discrepancy

Shared API guidelines specify `data: null` for errors. Current `app/core/responses.py:error_response` turns absent/None data into `{}`. API #98 does not execute this helper today; document the discrepancy for future integration.

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
