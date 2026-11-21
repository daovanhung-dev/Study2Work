---
title: "Request"
order: 3
dd_id: "89"
api_name: "Cập nhật quiz"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | PUT |
| URI | /api/v1/admin/quizzes/{quiz_id} |
| Character encoding | UTF-8 |
| Content-Type | application/json cho outer body DERIVED được triển khai cục bộ. |
| Authentication | Bearer JWT |
| Role | Admin; implementation dùng shared `ADMIN`; AC-35 fine-grained quiz-management policy chưa có source. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | Shared ADMIN guard xác thực trước path/body parsing và DB; fine-grained quiz-management permission chưa có. | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-authorization) |
| 2 | Trace ID | X-Trace-Id | No | UUID | Correlation header theo current middleware/API Guidelines; không phải filter nghiệp vụ. | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-authorization) |
| 3 | Content type | Content-Type | DERIVED | application/json | Outer body chứa hai JSON strings theo proposal #88. | [Step 1](./05_Data_Mapping.md#step-1-validate-request) |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | Quiz ID | quiz_id | int64 | Yes | 1 | 9223372036854775807 | Số nguyên dương | Decimal digits | N/A | Local parser accepts positive IDs within signed int64. | [Step 1](./05_Data_Mapping.md#step-1-validate-request) |

> Catalog xác nhận quiz_id:int64!; positive-only parsing và invalid path → 422 là fallback DERIVED.

## Query parameters

N/A — catalog và AC-35 không khai báo query parameter.

## Request body — direct contract absence and local proposal

Catalog row #89 chỉ khai báo path, không có body. Runtime hiện nhận body dưới đây như DERIVED proposal; không coi đây là direct contract.

| No | Logical name | Field name | Type | Required | Basis | Description | Data Mapping reference |
|---:|---|---|---|---|---|---|---|
| 1 | Quiz configuration | config | string | Yes | DERIVED reuse từ body API #88 | Cập nhật candidate config Quiz; không phải direct catalog body. | [Step 1](./05_Data_Mapping.md#step-1-validate-request) |
| 2 | Question set | questions | string | Yes | DERIVED reuse từ #88 và AC-35 UPDATE | Full replacement candidate cho questions. | [Step 1](./05_Data_Mapping.md#step-1-validate-request) |

## JSON schema đề xuất bên trong các string — DERIVED

Outer body candidate vẫn giữ hai string như #88. Chỉ owner mới có thể xác nhận API #89 nhận body này.

### config

| Embedded key | Type đề xuất | Required | Candidate use | Status |
|---|---|---:|---|---|
| course_id | int64 | Yes | Course đích; đổi course được phép nếu target tồn tại. | DERIVED; no publication/enrollment gate |
| title | string | Yes | Map sang quizzes.name; tối đa 200 ký tự từ DDL candidate. | DERIVED |
| duration_minutes | int32 or null | No | Map sang time_limit_minutes; omit/null ghi NULL. | DERIVED |
| passing_score | decimal-string | Yes | Map sang passing_score; tối đa NUMERIC(5,2), từ -999.99 đến 999.99. | DERIVED |

### questions[]

| Embedded key | Type đề xuất | Required | Candidate use | Status |
|---|---|---:|---|---|
| text | string | Yes | Candidate map sang question_text. | DERIVED |
| type | string / QuestionType | Yes | Required logical response; local legacy column comes from migration 013. | DERIVED / owner review open |
| choices | array | Yes | Full child-set candidate; QuizChoice chưa định nghĩa. | DERIVED proposal |
| choices[].text | string | Yes | Candidate map sang choice_text. | DERIVED |
| choices[].is_correct | boolean | No | Candidate answer key input; khi thiếu validator mặc định false. | DERIVED |

> Body candidate không có question/choice IDs; implementation thay toàn bộ child set. `questions=[]` và `choices=[]` được chấp nhận. Validator reuse #88: title ≤200, duration trong int32, passing_score là decimal-string NUMERIC(5,2), QuestionType theo ba giá trị #88; không thêm answer-count rule.

## Ví dụ Request — DERIVED proposal

~~~http
PUT /api/v1/admin/quizzes/501
Authorization: Bearer <admin-access-token>
Content-Type: application/json
X-Trace-Id: 00000000-0000-0000-0000-000000000089

{
  "config": "{\"course_id\":9001,\"title\":\"Quiz đã cập nhật\",\"duration_minutes\":30,\"passing_score\":\"70.00\"}",
  "questions": "[{\"text\":\"Câu hỏi minh họa?\",\"type\":\"SINGLE_CHOICE\",\"choices\":[{\"text\":\"Phương án A\",\"is_correct\":true},{\"text\":\"Phương án B\",\"is_correct\":false}]}]"
}
~~~

Outer body đúng hai string theo proposal reuse từ #88. Request body, nested type và full replacement vẫn DERIVED; ví dụ không làm chúng thành direct catalog contract.

## Quy tắc input đang mở

- Runtime parser yêu cầu quiz_id dương trong signed-int64; sai path trả 422 theo catalog.
- Body outer/nested sai trả 422 theo catalog; schema này là DERIVED.
- Body là full replacement; duration omit/null được ghi NULL; arrays rỗng xóa toàn bộ child set.
- Course đích phải tồn tại; đổi course được cho phép; không kiểm tra course status/enrollment.
- Quiz có attempt hoặc answer history trả 422 trước mọi write; policy này DERIVED.
- Không thêm status, description, question score, quiz_id trong body hoặc query field.
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
