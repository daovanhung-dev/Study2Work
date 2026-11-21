---
title: "Request"
order: 3
dd_id: "76"
api_name: "Thay đổi trạng thái khóa học Admin"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | PATCH |
| URI | /api/v1/admin/courses/{course_id}/status |
| Character encoding | UTF-8 |
| Content-Type | `application/json` cho body `{status}`; body là fallback DERIVED vì catalog/diagram không khai báo. |
| Authentication | Bearer JWT |
| Role | Runtime kiểm tra shared `ADMIN`; AC-32 còn yêu cầu finer course-management permission chưa có source. |
| Direct input | path{course_id:int64!} |
| Query | Không khai báo. |
| Direct body | Không khai báo trong catalog/diagram. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | Authenticate Admin trước khi truy cập course; claim/policy mapping chưa có current source. | 0.1 |
| 2 | Idempotency key | Idempotency-Key | SOURCE_REQUIRED | Chưa đặc tả | API guideline áp dụng cho retryable mutations; catalog không khai báo header và audit retry semantics chưa chốt. Không coi đây là direct input. | Open question 11 |

Trace ID do shared middleware propagate/generate; không thêm thành request field. Header Idempotency-Key chưa thuộc direct contract.

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | Course ID | course_id | int64 | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | Số nguyên 64-bit | SOURCE_REQUIRED | Không có | ID khóa học cần đổi trạng thái. | 1.1 |

## Query parameters

N/A — catalog không khai báo query parameters.

## Request body

**Direct contract:** API catalog và AC-32 diagram không khai báo body schema.

**Candidate body — DERIVED, cần owner xác nhận:** Một target status bắt buộc để backend biết trạng thái cần đặt.

| No | Location | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | body | Trạng thái đích | status | CourseStatus candidate | Yes — DERIVED | N/A | N/A | Enum candidate | DRAFT, PUBLISHED, SUSPENDED candidate; exact enum/casing needs confirmation | Không có | Target status; catalog nêu semantic draft/published/suspended nhưng không khai báo body hoặc enum members. | 1.2 |

Runtime body chỉ có field `status`, strict và cấm field lạ; không nhận metadata, mentor, category, audit reason hay delete flag. Giá trị uppercase khớp legacy `courses.status` default và current API #06 published filter; casing vẫn là fallback DERIVED, chưa được owner duyệt. Pilot course version enum thiếu SUSPENDED và không được dùng làm nguồn enum cho legacy model.

## Ví dụ Request data

Ví dụ dưới đây là candidate, không phải contract trực tiếp đã duyệt.

~~~http
PATCH /api/v1/admin/courses/101/status
Authorization: Bearer <admin-access-token>
Content-Type: application/json

{
  "status": "PUBLISHED"
}
~~~

## Quy tắc input đang mở

- course_id:int64! là direct input; minimum, malformed/overflow mapping chưa được nguồn xác định.
- Body {status} là DERIVED vì catalog/diagram bỏ qua body.
- Target semantics draft/published/suspended lấy từ catalog title; serialization/casing uppercase chỉ là proposal theo legacy/API #06.
- Target ngoài tập candidate có thể map sang 422 DESIGN_VALIDATION_ERROR; catalog có code 422 nhưng không quy định field rule.
- Không có transition matrix; không tự cấm DRAFT→PUBLISHED, PUBLISHED→SUSPENDED hoặc chiều khác.
- Không suy ra readiness gate, enrollment restriction, content moderation hoặc audit reason.
- Runtime same-status behavior là DERIVED no-op: không đổi `updated_at` và không thêm audit row.
- Idempotency-Key cần được owner quyết định theo API guideline; chưa thêm thành required header.
- HTTP tests xác nhận body/status validation cục bộ; fake DB không xác nhận live schema.
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
