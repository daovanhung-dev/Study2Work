---
title: "Request"
order: 3
dd_id: "82"
api_name: "Lấy danh sách lesson"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | GET |
| URI | `/api/v1/admin/lessons` |
| Character encoding | UTF-8 |
| Content-Type | N/A — không có request body. |
| Authentication | Bearer JWT |
| Role | Admin; lesson-management permission là tiền điều kiện AC-34. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | Principal phải có role Admin và quyền quản lý bài học; Admin guard hiện chưa có trong Study. | [Step 0](./05_Data_Mapping.md#0-check-quyen) |
| 2 | Trace ID | X-Trace-Id | No | UUID | Correlation header theo middleware convention; không phải filter nghiệp vụ. | [Step 0](./05_Data_Mapping.md#0-check-quyen) |

## Path parameters

Không có path parameter.

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | Course ID | `course` | int64 | No | Chưa đặc tả | Chưa đặc tả | Số nguyên 64-bit | Chưa đặc tả | Không có predicate khi vắng mặt (DERIVED) | Filter exact match candidate tới logical `course_id`; physical legacy mapping chưa được xác nhận. | [Step 1](./05_Data_Mapping.md#1-validate-data-input) |
| 2 | Lesson status | `status` | string | No | Chưa đặc tả | Chưa đặc tả | Text | LessonStatus members/casing chưa đầy đủ | Không có predicate khi vắng mặt (DERIVED) | Filter exact match proposal; không áp dụng mặc định `PUBLISHED`. | [Step 1](./05_Data_Mapping.md#1-validate-data-input) |
| 3 | Lesson type | `type` | string | No | Chưa đặc tả | Chưa đặc tả | Text | Chưa có nguồn type cho Lesson | Chưa xác định | Query trực tiếp từ catalog; field/predicate `SOURCE_REQUIRED`, không bỏ qua khi được gửi. | [Step 1](./05_Data_Mapping.md#1-validate-data-input) |

Catalog không khai báo pagination, `size`, `sort` hay filter khác; không thêm vào request.

## Request body

N/A — catalog không khai báo body; method GET chỉ nhận các query đã liệt kê.

## Ví dụ Request data

~~~text
GET /api/v1/admin/lessons?course=42&status=DRAFT
Authorization: Bearer <admin-access-token>
~~~

Ví dụ minh họa tên và kiểu query. `DRAFT` là giá trị có mặt trong legacy DDL, nhưng enum và casing hoàn chỉnh của API #82 chưa được xác nhận. Exact-match semantics là DERIVED.

~~~text
GET /api/v1/admin/lessons?type=video
Authorization: Bearer <admin-access-token>
~~~

`type` có trong catalog; ví dụ này không khẳng định giá trị hợp lệ hay cách lưu. Không thể triển khai đúng filter đến khi có field/relation nguồn và rule được duyệt.

## Quy tắc input đang mở

- Catalog chỉ định kiểu `course:int64`, `status:string`, `type:string`; không cho biết giới hạn số, enum, trim/case normalization hoặc range.
- Catalog chỉ liệt kê HTTP 401/403/500, không có mã validation 400/422. Quy tắc lỗi khi query parse sai cần được làm rõ khi thiết kế route.
- Không gửi `course`, `status` hay `type` nghĩa là thiếu filter tương ứng theo proposal; behavior này cần owner xác nhận.
- Query `type` không được bỏ qua hoặc ánh xạ sang loại content block nếu chưa có bằng chứng.

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
