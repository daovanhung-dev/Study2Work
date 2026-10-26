---
title: "Error"
order: 6
dd_id: "54"
api_name: "Lấy submissions"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Error status/code set follows the API #54 artifacts, with 422 added for the implemented positive query constraints. Current `error_response()` serializes error data as JSON null.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Yes | Authorization | Bearer token missing, malformed, invalid or claims invalid | 401 | DESIGN_AUTHENTICATION_REQUIRED | SOURCE_REQUIRED | 0.1 | No | Shared explicit MENTOR guard. |
| 2 | Authorization | Yes | Mentor course access | Actor lacks MENTOR role or explicitly requested existing course belongs to another Mentor | 403 | DESIGN_ACCESS_DENIED | SOURCE_REQUIRED | 0.3 | Yes for course mismatch | Direct-owner policy follows #46/#49. |
| 3 | State conflict | SOURCE_REQUIRED | SOURCE_REQUIRED | Catalog declares 409; AC-23 defines no trigger | 409 | DESIGN_STATE_CONFLICT | SOURCE_REQUIRED | 4.2 | No | Declared but currently unreachable; do not derive from empty results/status/page. |
| 4 | Input validation | Yes | course_id/page | Non-integer, non-positive or outside declared integer range | 422 | DESIGN_VALIDATION_ERROR | SOURCE_REQUIRED | 1 | No | Added to catalog/diagram for route constraints. |
| 5 | System error | Yes | Query/response mapping | Database error, count mismatch or malformed required projection | 500 | DESIGN_INTERNAL_ERROR | SOURCE_REQUIRED | 4.3 | Yes on read failure | Safe message only; no SQL or row data exposed. |

## Input validation and empty result

- Status is an optional exact string; unknown values produce an empty page if none match, not a new validation code.
- A missing course or a course with no submissions returns HTTP 200 with an empty Page; API #54 has no 404.
- Invalid `page` or `course_id` returns 422 using the registered request validation handler and exact path contract mapping.
- Error responses contain `data: null`; read-only requests never commit. Failed DB/mapping work is rolled back when a session transaction may be active.

> Error message IDs are SOURCE_REQUIRED; the API catalog defines status/business codes, not message identifiers.

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
