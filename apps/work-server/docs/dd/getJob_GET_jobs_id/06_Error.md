---
title: "Error"
order: 6
dd_id: "getJob"
api_name: "jobs.view.getJob"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
status: "Draft — Ready for Review"
---
# Error

## Giải thích

Lỗi không inline `res.json`; route/use-case throw typed error hoặc lỗi framework được centralized exception handler map về envelope chuẩn.

## Error cases

| No | Business code | HTTP | Message | Condition | Source |
| ---: | --- | --- | --- | --- | --- |
| 1 | INVALID_REQUEST | 400 | ID việc làm không hợp lệ. | Path id fails positive safe integer parser. | apps/work-server/src/modules/jobs/validate.ts |
| 2 | JOB_NOT_FOUND | 404 | Không tìm thấy việc làm. | JD findUnique returns null. | apps/work-server/src/modules/jobs/view.ts |
| 3 | INTERNAL_SERVER_ERROR | 500 | Lỗi máy chủ. | Unhandled error is mapped safely without exposing secret. | apps/work-server/src/core/exceptions.ts |

## Common envelope rule

- `success=false`.
- `data=null`.
- `meta={}` nếu không có field errors.
- `meta.fieldErrors` chỉ xuất hiện với Zod validation issues.
- `traceId` và response header `X-Trace-Id` luôn đồng nhất.


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
