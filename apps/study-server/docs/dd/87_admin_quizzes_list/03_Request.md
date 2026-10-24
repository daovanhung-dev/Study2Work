---
title: "Request"
order: 3
dd_id: "87"
api_name: "Lấy danh sách quiz"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | GET |
| URI | /api/v1/admin/quizzes |
| Character encoding | UTF-8 |
| Content-Type | N/A — không có request body. |
| Authentication | Bearer JWT |
| Role | Admin; AC-35 yêu cầu thêm quiz-management permission. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | Principal cần role Admin và quiz-management permission; guard hiện chưa có trong Study. | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-authorization) |
| 2 | Trace ID | X-Trace-Id | No | UUID | Correlation header theo middleware convention; không phải filter nghiệp vụ. | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-authorization) |

## Path parameters

Không có path parameter.

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | Course filter | course | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | Số nguyên 64-bit | SOURCE_REQUIRED | Không có predicate nếu vắng mặt (DERIVED) | Candidate exact-match filter tới quizzes.course_id; physical schema chưa xác minh. | [Step 1](./05_Data_Mapping.md#step-1-validate-query) |
| 2 | Quiz status filter | status | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | Text | Enum/casing SOURCE_REQUIRED | Không có predicate nếu vắng mặt (DERIVED) | Candidate exact-match filter tới quizzes.status; không tự tạo status whitelist. | [Step 1](./05_Data_Mapping.md#step-1-validate-query) |
| 3 | Page index | page | int32 | No | 1 (DERIVED) | SOURCE_REQUIRED | Số nguyên 32-bit | Trang từ 1 (DERIVED) | 1 (DERIVED) | Page 1-based; đề xuất size nội bộ cố định 20 theo API #07. Catalog không khai báo size hoặc pagination response. | [Step 1](./05_Data_Mapping.md#step-1-validate-query) |

> Catalog không quy định trim/case normalization, range của course, status enum, page default, page size, sort hoặc lỗi parse query. Các đề xuất page được đánh dấu DERIVED.

## Request body

N/A — catalog không khai báo body; GET chỉ nhận các query đã liệt kê.

## Ví dụ Request data

~~~text
GET /api/v1/admin/quizzes?course=9001&status=DRAFT&page=1 HTTP/1.1
Authorization: Bearer <admin-access-token>
~~~

Ví dụ minh họa tên query. DRAFT chỉ là giá trị xuất hiện trong legacy DDL; enum/casing của API chưa được xác nhận. Page 1/default 1 và page size 20 là proposal DERIVED.

## Quy tắc input đang mở

- Catalog chỉ định course:int64, status:string và page:int32; không quy định positivity/range, trim, case normalization hoặc enum.
- Course/status exact-match semantics là proposal DERIVED.
- Invalid int64/int32 query có thể bị framework parse từ chối; catalog không liệt kê 400/422 hoặc business code tương ứng.
- Query page không có size; fixed size 20 chỉ là đề xuất theo API #07.
- Không thêm query size, sort hoặc search text vì catalog không khai báo.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `1.Request`
- Dimension: `A1:BR34`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `62`
- Số vùng merge: `25`

<details>
<summary>Danh sách vùng merge</summary>

- `S16:T16`
- `U16:V16`
- `W18:X18`
- `W19:X19`
- `U19:V19`
- `S19:T19`
- `U18:V18`
- `S17:T17`
- `S18:T18`
- `AK18:BA18`
- `S15:T15`
- `U15:V15`
- `W15:X15`
- `U14:V14`
- `W14:X14`
- `W17:X17`
- `S13:T14`
- `U13:X13`
- `U17:V17`
- `W16:X16`
- `Y13:AA14`
- `AB14:AD14`
- `AE14:AG14`
- `AB13:AG13`
- `AH13:AJ14`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | HTTP method |  |
| 2 | `L2` | GET/POST |  |
| 3 | `B3` | URI |  |
| 4 | `B4` | Code ký tự |  |
| 4 | `L4` | UTF-8 |  |
| 6 | `B6` | Request header |  |
| 7 | `B7` | Name |  |
| 7 | `J7` | Field name |  |
| 7 | `V7` | Giá trị |  |
| 7 | `AK7` | Giải thích |  |
| 8 | `B8` | Contents type |  |
| 8 | `J8` | Content-Type |  |
| 8 | `V8` | application/json |  |
| 8 | `AK8` | Thực hiện request bằng json data |  |
| 9 | `B9` | Basic authen |  |
| 9 | `J9` | Authorization |  |
| 9 | `V9` | Token |  |
| 11 | `B11` | Request data |  |
| 12 | `B12` | No |  |
| 12 | `C12` | Key name |  |
| 12 | `S12` | Nội dung check |  |
| 12 | `AK12` | Giải thích |  |
| 13 | `S13` | Bắt buộc |  |
| 13 | `U13` | Số ký tự |  |
| 13 | `Y13` | Loại ký tự |  |
| 13 | `AB13` | Format |  |
| 13 | `AH13` | Giá trị hợp lệ |  |
| 14 | `C14` | Logic |  |
| 14 | `K14` | Vật lý |  |
| 14 | `U14` | Tối thiểu |  |
| 14 | `W14` | Tối đa |  |
| 15 | `B15` | 1 |  |
| 15 | `S15` | ○ |  |
| 15 | `U15` | 1 |  |
| 15 | `W15` | 20 |  |
| 15 | `Y15` | halfsize |  |
| 16 | `B16` | 2 |  |
| 16 | `S16` | ○ |  |
| 16 | `U16` | 1 |  |
| 16 | `W16` | 8 |  |
| 16 | `Y16` | halfsize |  |
| 16 | `AB16` | datetime |  |
| 16 | `AE16` | yyyyMMdd |  |
| 17 | `S17` | ○ |  |
| 17 | `U17` | 1 |  |
| 17 | `W17` | 1 |  |
| 17 | `Y17` | halfsize |  |
| 17 | `AB17` | numberic |  |
| 17 | `AH17` | 2,3,4 |  |
| 18 | `S18` | ○ |  |
| 18 | `U18` | 1 |  |
| 18 | `Y18` | fullsize |  |
| 19 | `S19` | ○ |  |
| 19 | `U19` | 1 |  |
| 25 | `B25` | Ví dụ về Request data |  |
| 26 | `L26` | { |  |
| 27 | `M27` | "tnorsh_pln_id" : "0000000001", |  |
| 28 | `M28` | "yt_ymd":" 20201001", |  |
| 29 | `M29` | "yt_hmi":" 0830", |  |
| 30 | `M30` | "excpt_id":" 001", |  |
| 31 | `M31` | "bik_desc":" 計画削除" |  |
| 32 | `L32` | } |  |

</details>
