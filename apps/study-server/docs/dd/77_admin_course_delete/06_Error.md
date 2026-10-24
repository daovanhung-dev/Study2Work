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
- Endpoint chưa có route/Admin guard; các hàng dưới là design branches, không phải runtime evidence.
- Dependency-block 422 là đề xuất `DERIVED`; catalog có code này nhưng chưa định nghĩa điều kiện hoặc error detail.
- Không thêm HTTP status, business code hoặc error-message ID ngoài catalog.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Token thiếu, sai hoặc hết hạn | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No | Status/code DIRECT; route/auth chưa wire. |
| 2 | Authorization | Admin policy | Course-management permission | Principal hợp lệ nhưng không có Admin/course-management permission | 403 | `DESIGN_ACCESS_DENIED` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No | Status/code DIRECT; policy SOURCE_REQUIRED. |
| 3 | Not found | Candidate Q1 | `course_id` | Không tìm thấy course sau authorization | 404 | `DESIGN_RESOURCE_NOT_FOUND` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-2-get-thong-tin) | No | Code/status DIRECT; no-row mapping DERIVED. |
| 4 | Validation/policy | Path or approved dependency rule | `course_id` / dependency set | Path không hợp lệ hoặc policy được duyệt chặn soft-delete | 422 | `DESIGN_VALIDATION_ERROR` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-3-check-policy-and-soft-delete) | Candidate rollback only if transaction began | Code/status DIRECT; malformed path and dependency mapping DERIVED/SOURCE_REQUIRED. |
| 5 | System error | Query/mutation/commit/mapping | Delete pipeline | Lỗi DB, mutation, timestamp source hoặc transaction | 500 | `DESIGN_INTERNAL_ERROR` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-4-check-mutation-result) | Rollback if approved transaction began | Không trả raw SQL/policy details; storage target chưa xác định. |

## Candidate branch questions — không phải HTTP contract

| Condition | Candidate or question | Status |
|---|---|---|
| `course_id` malformed/overflow | Catalog có 422; parser/middleware mapping chưa có source. | SOURCE_REQUIRED |
| Course không tồn tại | Candidate 404 sau khi Admin authorization thành công. | DERIVED |
| Enrollment tồn tại | Proposal là 422 nếu policy duyệt enrollment là blocker; status/retention rule chưa xác định. | DERIVED / SOURCE_REQUIRED |
| Content tồn tại | Relation/predicate chưa được chọn; không suy diễn generic Content thành `lessons`/`content_blocks`. | SOURCE_REQUIRED |
| Course đã soft-delete | Repeat DELETE có thể success, 404 hoặc policy result; chưa có idempotency/lifecycle rule. | SOURCE_REQUIRED |
| Query/mutation/commit/timestamp lỗi | Catalog 500 `DESIGN_INTERNAL_ERROR`; rollback scope tùy approved transaction. | Code/status DIRECT; transaction SOURCE_REQUIRED |

## Error envelope discrepancy

- API guideline yêu cầu error `data:null` và `meta.fieldErrors` cho field-level validation.
- Current `error_response()` đổi data vắng mặt thành `{}`.
- `DESIGN_CONTRACT_PATHS` chưa có Admin course path; middleware dùng exact `request.url.path` membership nên route có numeric `course_id` cần dynamic/route-aware mapping khi wire.
- API #77 chưa wired; đây là discrepancy hiện tại và yêu cầu tích hợp tương lai, không phải response runtime của endpoint.

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
