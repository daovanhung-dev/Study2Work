---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "39"
api_name: "Lấy danh sách thread"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các trường hợp dưới đây giữ nguyên error set của API #39 trong approved catalog. Quy tắc course access, query parsing và visibility chưa được đặc tả.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Bearer JWT | Authorization | Token thiếu hoặc không hợp lệ theo policy auth chung. | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A | 0.1 | N/A | Business code theo catalog. |
| 2 | Authorization | Student role/access | Principal/course_id | Sai role hoặc access bị từ chối theo predicate được xác nhận. | 403 | DESIGN_ACCESS_DENIED | N/A | 0.1–0.3 | N/A | Course access predicate chưa chốt. |
| 3 | System error | Discussion read/query | N/A | Lỗi nội bộ không được ánh xạ sang lỗi contract cụ thể. | 500 | DESIGN_INTERNAL_ERROR | N/A | 5.3 | N/A | Không trả SQL, stack trace hoặc storage detail. |

## Error envelope

Envelope lỗi dùng success=false, businessCode theo catalog, message client-safe, data=null, meta và traceId theo [API guidelines](../../../../../contracts/api-guidelines/README.md). Catalog không khai báo endpoint-specific message ID.

## Query validation chưa có contract

| No | Field | Unresolved condition | Status/code |
|---:|---|---|---|
| 1 | course_id | Query value không parse thành int64 hoặc nằm ngoài miền được API chấp nhận. | SOURCE_REQUIRED; catalog không liệt kê 400/422. |
| 2 | page | Query value không parse thành int32, nhỏ hơn miền cho phép hoặc vượt giới hạn. | SOURCE_REQUIRED; catalog không liệt kê 400/422. |
| 3 | sort | Sort value không thuộc allowlist hoặc sai syntax. | SOURCE_REQUIRED; catalog không liệt kê 400/422. |

> Catalog API #39 chỉ khai báo HTTP/business codes 200, 401, 403 và 500. Không thêm 404, 409 hoặc 422 nếu chưa cập nhật contract có thẩm quyền.
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

