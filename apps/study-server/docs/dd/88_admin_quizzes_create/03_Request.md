---
title: "Request"
order: 3
dd_id: "88"
api_name: "Tạo quiz mới"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | POST |
| URI | /api/v1/admin/quizzes |
| Character encoding | UTF-8 |
| Content-Type | application/json |
| Authentication | Bearer JWT |
| Role | Admin; AC-35 yêu cầu thêm quiz-management permission. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer JWT | Principal cần role Admin và quiz-management permission; guard chưa có trong Study. | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-authorization) |
| 2 | Trace ID | X-Trace-Id | No | UUID | Correlation header theo API Guidelines/current middleware convention. | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-authorization) |

## Path parameters

Không có path parameter.

## Query parameters

Không có query parameter.

## Request body — direct contract

| No | Logical name | Field name | Type | Required | Format | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|
| 1 | Quiz configuration | config | string | Yes | Chuỗi UTF-8 | Direct catalog chỉ định string; embedded schema chưa được catalog định nghĩa. | [Step 1](./05_Data_Mapping.md#step-1-validate-and-parse-body) |
| 2 | Question set | questions | string | Yes | Chuỗi UTF-8 | Direct catalog chỉ định string; embedded schema chưa được catalog định nghĩa. | [Step 1](./05_Data_Mapping.md#step-1-validate-and-parse-body) |

## JSON schema đề xuất bên trong các string — DERIVED

Contract phía ngoài vẫn là hai trường string. Đề xuất parse nội dung như sau:

### config

| Embedded key | Type đề xuất | Required | Mapping/purpose | Status |
|---|---|---:|---|---|
| course_id | int64 | Yes | Course chứa quiz; candidate kiểm tra courses.id. | DERIVED |
| title | string | Yes | Tên quiz; candidate map sang quizzes.name. | DERIVED |
| duration_minutes | int32 | No | Thời lượng; candidate map sang quizzes.time_limit_minutes. | DERIVED |
| passing_score | decimal-string | Yes | Ngưỡng điểm đạt; candidate map sang quizzes.passing_score. | DERIVED |

### questions[]

| Embedded key | Type đề xuất | Required | Mapping/purpose | Status |
|---|---|---:|---|---|
| text | string | Yes | Question text; candidate map sang quiz_questions.question_text. | DERIVED |
| type | string / QuestionType | Yes | Logical QuizQuestion.type; enum values/storage chưa chốt. | Input mapping DERIVED theo response schema |
| choices | array | Yes | Answer choices; QuizChoice chưa định nghĩa. | DERIVED |
| choices[].text | string | Yes | Candidate choice text; map sang quiz_choices.choice_text. | DERIVED |
| choices[].is_correct | boolean | Yes | Candidate answer-key input; map sang quiz_choices.is_correct. | DERIVED; không phải output QuizChoice field |

> Max length title, số question/choice, enum QuestionType, số đáp án đúng và payload size chưa được direct contract quy định.

## Ví dụ Request data

~~~json
{
  "config": "{\"course_id\": 9001, \"title\": \"Quiz minh họa\", \"duration_minutes\": 30, \"passing_score\": \"70.00\"}",
  "questions": "[{\"text\":\"Câu hỏi minh họa?\",\"type\":\"SINGLE_CHOICE\",\"choices\":[{\"text\":\"Phương án A\",\"is_correct\":true},{\"text\":\"Phương án B\",\"is_correct\":false}]}]"
}
~~~

Ví dụ giữ đúng outer string types. Sau JSON decode lần hai, config thành object và questions thành array theo proposal DERIVED. SINGLE_CHOICE chỉ là ví dụ từ V1-PILOT, chưa chốt làm QuestionType API #88. is_correct là candidate input từ legacy DDL, chưa phải QuizChoice contract.

## Quy tắc input và lỗi

- Thiếu config/questions, outer type không phải string hoặc outer body sai schema: HTTP 422 DESIGN_VALIDATION_ERROR theo contract.
- Embedded JSON sai cú pháp hoặc shape theo proposal: đề xuất 422 DESIGN_VALIDATION_ERROR.
- Course ID không tồn tại: đề xuất 422 DESIGN_VALIDATION_ERROR; catalog không có 404.
- Không tự đặt giới hạn số question/choice, body size, passing_score range hoặc allowed QuestionType list.
- Không thêm query, path hoặc top-level body field ngoài catalog.
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
