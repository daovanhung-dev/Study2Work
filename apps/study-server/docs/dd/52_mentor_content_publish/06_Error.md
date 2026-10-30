---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "52"
api_name: "Publish/unpublish nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

API #52 giữ đúng năm lỗi trong catalog. Local route/test wiring có source; request body và các điều kiện phụ thuộc trạng thái vẫn là proposal DERIVED.

## Error cases

| No | HTTP status | Business code | Điều kiện theo contract | Data Mapping reference | Response/source rule | Status |
|---:|---:|---|---|---:|---|---|
| 1 | 401 | DESIGN_AUTHENTICATION_REQUIRED | Bearer JWT thiếu, sai hoặc hết hạn | 0 | Safe error envelope; không echo token/claims. | Code DIRECT; local HTTP test |
| 2 | 403 | DESIGN_ACCESS_DENIED | Principal không có role Mentor hoặc direct owner không khớp | 0 | Không tiết lộ owner internals; assigned-Mentor policy SOURCE_REQUIRED. | Code DIRECT; owner fallback DERIVED; local HTTP test |
| 3 | 404 | DESIGN_RESOURCE_NOT_FOUND | content_id sai int64 hoặc không ánh xạ tới active Content | 2 | Error envelope, không trả dữ liệu một phần. | Code DIRECT; local HTTP test; DDL/live mapping unverified |
| 4 | 422 | DESIGN_VALIDATION_ERROR | Body sai shape/type hoặc state không đủ điều kiện theo fallback | 1, 2, 3 | Không echo payload nhạy cảm; catalog giữ nguyên code. | Code DIRECT; body/state DERIVED; local HTTP test |
| 5 | 500 | DESIGN_INTERNAL_ERROR | Lỗi lookup/update, projection hoặc commit | 2–4 | Safe error; không trả SQL, schema, stack/provider detail. | Code DIRECT; local HTTP test; DB is fake |

## Nhánh cần xác nhận

| Tình huống | Code catalog hiện có | Cần chốt |
|---|---|---|
| APPROVED Content thiếu dữ liệu cần thiết | 422 candidate | Readiness criteria theo từng ContentType/payload chưa có nguồn. |
| PENDING_REVIEW hoặc REJECTED được yêu cầu publish | 422 candidate | State machine DERIVED; enum đầy đủ SOURCE_REQUIRED. |
| Unpublish Content đã PUBLISHED | 200 local fallback | Trở về APPROVED; transition DERIVED, cần xác nhận review semantics. |
| Request lặp lại target state | 200 local fallback | No-op/idempotency đã implement nhưng vẫn DERIVED. |
| Content không tồn tại với Mentor không có quyền | 403 hoặc 404 | Thứ tự check/anti-enumeration cần policy; giữ nguyên code set. |
| Path int64 sai/overflow | 404 local fallback | Parser trong view ánh xạ sai format/range về `DESIGN_RESOURCE_NOT_FOUND`; focused test đã pass. |

## Middleware integration

`/api/v1/mentor/content/{content_id}/publish` is now in `DESIGN_CONTRACT_PATHS`; local TestClient coverage confirms body-validation code `DESIGN_VALIDATION_ERROR`. Unexpected exception mapping is wired through the same middleware path. Fake DB tests do not prove live PostgreSQL/runtime behavior.

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
