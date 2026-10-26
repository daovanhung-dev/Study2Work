---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "48"
api_name: "Tải lại lecture vừa tạo"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Bảng lỗi giữ đúng API catalog #48: chỉ 401, 403, 404 và 500 với business code tương ứng. Local runtime uses the shared Mentor guard, direct-owner check and integrity checks. Malformed/out-of-range IDs map to the existing 404 as an implementation decision. Không thêm 422, 409 hoặc 503.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Thiếu, sai định dạng hoặc token không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A | 0.1 | N/A | Catalog direct; shared Mentor guard runs before DB access. |
| 2 | Authorization | Role | role | Principal không có role Mentor | 403 | DESIGN_ACCESS_DENIED | N/A | 0.3 | N/A | Catalog direct. |
| 3 | Authorization | Course access | lecture_id/course owner | Lecture exists but `courses.mentor_id` differs from authenticated principal | 403 | DESIGN_ACCESS_DENIED | N/A | 0.3 | Read transaction rolled back | Direct-owner matches #46/#47; assigned-course relation remains unsupported. |
| 4 | Not found | Lecture lookup/path parse | lecture_id | No lesson exists, ID is malformed, or value is outside signed int64 | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A | 1/2.1 | Read transaction rolled back only for DB lookup | Malformed ID mapping is an implementation decision; catalog has no 422. |
| 5 | System/integrity | Parent course and required fields | lessons.course_id | Lecture row exists but course_id is NULL or parent course is missing | 500 | DESIGN_INTERNAL_ERROR | N/A | 2.1/4.2 | Read transaction rolled back | Lecture requires course_id for response and owner scope. |
| 6 | System/integrity | Upload link resolution | lesson_uploads.upload_id | Linked uploads metadata is missing or outside owner/purpose/course scope | 500 | DESIGN_INTERNAL_ERROR | N/A | Q2/4.2 | Read transaction rolled back | Do not expose metadata that fails scope. |
| 7 | System error | Database/read mapping | Q1/Q2 | Query or response mapping fails | 500 | DESIGN_INTERNAL_ERROR | N/A | 4.2 | Read transaction rolled back | Catalog direct; no internal details. |

> `error_response()` defaults to `data: null`, and API #48 uses this helper.
>
> Runtime maps malformed/out-of-range `lecture_id` to 404 to preserve the catalog error set. This mapping still needs contract-owner confirmation; no 422 was added.

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
