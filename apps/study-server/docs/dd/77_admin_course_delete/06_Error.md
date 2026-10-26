---
title: "Error"
order: 6
dd_id: "77"
api_name: "Xóa khóa học Admin theo policy AC-32"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

- Giữ đúng HTTP status và business code của API catalog #77.
- Route/Admin guard/HTTP tests hiện có trong local Study source; tests dùng fake DB session.
- Dependency-block 422 là runtime fallback `DERIVED`; catalog có code nhưng không định nghĩa blocker predicate/message.
- Không thêm HTTP status, business code hoặc error-message ID ngoài catalog.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Shared Bearer/JWT guard | Authorization | Token thiếu, sai hoặc hết hạn | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No | Code/status DIRECT; local shared guard. |
| 2 | Authorization | Shared role guard | `ADMIN` role | Principal không có role `ADMIN` | 403 | `DESIGN_ACCESS_DENIED` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No | Finer course-management permission remains SOURCE_REQUIRED. |
| 3 | Not found | Q1 locked lookup | `course_id` | Course vắng hoặc status đã `DELETED` | 404 | `DESIGN_RESOURCE_NOT_FOUND` | `Course not found.` | [Data Mapping](./05_Data_Mapping.md#step-2-get-thong-tin) | Rollback lock transaction | No-row/repeat mapping DERIVED; exact code DIRECT. |
| 4 | Validation | Raw path parser | `course_id` | Malformed hoặc ngoài signed-int64 range | 422 | `DESIGN_VALIDATION_ERROR` | `Dữ liệu đầu vào không hợp lệ.` | [Data Mapping](./05_Data_Mapping.md#step-1-validate-data-input) | No DB transaction | 422 code DIRECT; parser mapping DERIVED. |
| 5 | Dependency policy | Q2 EXISTS checks | Enrollment/content | Any enrollment or active learning content exists | 422 | `DESIGN_VALIDATION_ERROR` | `Course with enrollments or content cannot be deleted.` | [Data Mapping](./05_Data_Mapping.md#step-3-check-policy-and-soft-delete) | Rollback lock transaction; no mutation | Blocker set and message DERIVED. |
| 6 | System error | Query/projection/commit | Delete pipeline | DB failure or invalid lock/dependency/RETURNING projection | 500 | `DESIGN_INTERNAL_ERROR` | `Course could not be deleted.` | [Data Mapping](./05_Data_Mapping.md#step-4-check-mutation-result) | Rollback | Safe response; no raw DB detail. |

## Candidate branch questions — không phải HTTP contract

| Condition | Candidate or question | Status |
|---|---|---|
| `course_id` malformed/overflow | Raw signed-int64 parser returns 422 before DB. | VERIFIED_LOCAL / DERIVED_MAPPING |
| Course missing/already `DELETED` | Q1 no-row returns 404; repeated DELETE is not idempotent. | VERIFIED_LOCAL / DERIVED_MAPPING |
| Enrollment exists | Any enrollment status blocks and returns 422. | DERIVED_POLICY |
| Active generic Content exists | `contents.deleted_at IS NULL` blocks and returns 422. | DERIVED_POLICY |
| Lesson/quiz/assignment exists | Any matching legacy learning record blocks and returns 422. | DERIVED_POLICY |
| Query/projection/commit failure | Catalog 500 `DESIGN_INTERNAL_ERROR`; view rolls back. | VERIFIED_LOCAL; live DB not verified |

## Error envelope discrepancy

- API guideline yêu cầu error `data:null` và `meta.fieldErrors` cho field-level validation.
- Current `error_response()` serializes omitted data as `null`.
- API #74 registered the shared Admin course path template; middleware matches API #77 via FastAPI route metadata.
- Local TestClient coverage verifies the error envelope and code branches; fake sessions do not prove PostgreSQL behavior.

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
