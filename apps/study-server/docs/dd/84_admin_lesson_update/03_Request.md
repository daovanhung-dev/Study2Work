---
title: "Request"
order: 3
dd_id: "84"
api_name: "Cập nhật lesson"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: markdown
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | PUT |
| URI | `/api/v1/admin/lessons/{lesson_id}` |
| Character encoding | UTF-8 |
| Content-Type | application/json là DERIVED cho body proposal; catalog chưa xác nhận body/content type. |
| Authentication | Bearer JWT |
| Role | Admin; lesson-management permission theo AC-34. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | `Authorization` | Yes | `Bearer <token>` | Principal cần Admin và lesson-management permission; guard/policy chưa có trong Study. | [Step 0](./05_Data_Mapping.md#step-0-check-quyen) |
| 2 | Content type | `Content-Type` | DERIVED | `application/json` | Candidate header nếu JSON body được duyệt. | [Step 1](./05_Data_Mapping.md#step-1-nhan-request) |
| 3 | Trace ID | `X-Trace-Id` | No | UUID | Current Study trace middleware convention; không phải input nghiệp vụ. | [Step 0](./05_Data_Mapping.md#step-0-check-quyen) |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | Lesson ID | `lesson_id` | int64 | Yes | Chưa đặc tả | Chưa đặc tả | Số nguyên 64-bit | Chỉ xác nhận type int64 | N/A | ID lesson; candidate predicate tới lessons.id. | [Step 1](./05_Data_Mapping.md#step-1-nhan-request) |

## Query parameters

N/A — catalog và AC-34 diagram không khai báo query parameter.

## Request body

Catalog và diagram chỉ khai báo `path{lesson_id:int64!}`. Các field dưới đây là candidate DERIVED để cụ thể hóa UPDATE; chưa được duyệt.

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Tiêu đề lesson | `title` | string | Yes, proposal | Chưa đặc tả | 200 legacy candidate | Unicode | N/A | N/A | N/A | Map candidate tới legacy lessons.name VARCHAR(200); không xác nhận live validation. | [Step 2](./05_Data_Mapping.md#step-2-check-body-proposal) |
| 2 | Nội dung lesson | `content` | string or null | Yes, proposal | Chưa đặc tả | Chưa đặc tả | Unicode | N/A | N/A | Null-to-clear candidate | Null/omission semantics cần xác nhận. | [Step 2](./05_Data_Mapping.md#step-2-check-body-proposal) |
| 3 | URL video | `video_url` | uri or null | Yes, proposal | Chưa đặc tả | Chưa đặc tả | Unicode | URI candidate | Chưa đặc tả | Null-to-clear candidate | Scheme/host/length validation chưa có nguồn. | [Step 2](./05_Data_Mapping.md#step-2-check-body-proposal) |
| 4 | Thứ tự lesson | `order` | int32 | Yes, proposal | Chưa đặc tả | Chưa đặc tả | N/A | Số nguyên 32-bit | N/A | N/A | Map candidate tới legacy lessons.sort_order; range/uniqueness chưa xác nhận. | [Step 2](./05_Data_Mapping.md#step-2-check-body-proposal) |

> “Yes, proposal” là một phương án full replacement để review. Requiredness, omission/null behavior và PUT semantics cần owner xác nhận.

Không gửi lesson_id trong body. Không gửi course_id vì chưa có rule chuyển course. Không gửi status vì API #85 quản lý trạng thái. Không gửi timestamps hoặc fields ngoài proposal.

## Ví dụ Request data — DERIVED

```http
PUT /api/v1/admin/lessons/501
Authorization: Bearer <admin-access-token>
Content-Type: application/json
X-Trace-Id: 00000000-0000-0000-0000-000000000084

{
  "title": "Giới thiệu khóa học",
  "content": "Nội dung đã cập nhật",
  "video_url": "https://example.com/lesson-501.mp4",
  "order": 2
}
```

Ví dụ minh họa body candidate; không xác nhận field rules hoặc replacement semantics.

## Quy tắc input đang mở

- Catalog xác nhận lesson_id:int64!; minimum/positive constraint chưa được đặc tả.
- Catalog có 422 DESIGN_VALIDATION_ERROR nhưng không chỉ rõ field validation rules.
- Body fields, requiredness, null/omission, title rules, URI policy, order bounds/uniqueness và Content-Type cần owner xác nhận.

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
