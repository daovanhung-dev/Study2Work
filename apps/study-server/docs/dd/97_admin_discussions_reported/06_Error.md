---
title: "Error"
order: 6
dd_id: "97"
api_name: "Lấy reported discussions"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "5. Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Catalog error set

| HTTP | Business code | Meaning | Direct/conditional handling |
|---:|---|---|---|
| 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Missing, malformed or invalid Bearer/JWT | DIRECT code; shared auth helper |
| 403 | `DESIGN_ACCESS_DENIED` | Authenticated principal lacks Admin authorization | DIRECT code; shared `role="ADMIN"` guard |
| 422 | `DESIGN_VALIDATION_ERROR` | Invalid/non-positive/out-of-int32 `page` | Local `DERIVED` fallback; not listed in catalog |
| 500 | `DESIGN_INTERNAL_ERROR` | Internal read, query or required mapping failure | DIRECT code; wired locally |

Success is HTTP 200 `DESIGN_RESOURCE_RETRIEVED`. Catalog #97 does not list 404 or 422; implementation adds only the documented local 422 page-validation fallback.

## Error branches and open behavior

| Branch | Expected contract | Current evidence / unresolved |
|---|---|---|
| Bearer/JWT failure | 401 | Shared helper validates before page parse and DB access |
| Role/access failure | 403 | Shared `ADMIN` guard; fine-grained AC-37 permission remains unverified |
| Invalid `reason` / `severity` value | No error | Free-form exact-match filters; no taxonomy validation |
| Invalid `page` parse/range | 422 `DESIGN_VALIDATION_ERROR` | Local `DERIVED` fallback, with field detail |
| No matching report | 200 empty Page | `total=0`, `total_pages=0` |
| Missing required Discussion/author projection | 500 `DESIGN_INTERNAL_ERROR` | Does not fabricate required course/author/status fields |
| SQLAlchemy query failure | 500 `DESIGN_INTERNAL_ERROR` | Read transaction rollback, safe message, trace ID |
| Internal exception | 500 `DESIGN_INTERNAL_ERROR` | Route is in `DESIGN_CONTRACT_PATHS` |

## Envelope discrepancy

Shared API guidelines expect `data: null` on error. Current `app/core/responses.py:error_response` passes `None` through to JSON, so API #97 error responses contain `data: null`.

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
