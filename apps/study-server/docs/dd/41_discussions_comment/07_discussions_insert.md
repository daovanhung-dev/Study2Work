---
title: "Định nghĩa discussions INSERT"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "41"
api_name: "Thêm bình luận/trả lời"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — discussions INSERT

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | discussions |
| Logical table | Discussion reply/comment |
| Operation | Candidate INSERT; design-only |
| Data Mapping step | 4 |
| Evidence | AC-19 reply branch; DB guide/ERD and checked-in DDL |

## Update mapping

**Áp dụng khi**

- Không có update mapping được xác định cho API #41.
- Activity diagram ghi “update counters”, nhưng schema hiện có không khai báo column/table counter; không dựng câu UPDATE vào field không tồn tại.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có physical counter target trong ERD/DDL. |

## Insert mapping

**Áp dụng khi**

- AC-19 chọn nhánh REPLY; diagram ghi INSERT Comment.
- Candidate reply là child row của topic; parent_id = discussion_id và course_id kế thừa từ topic là DERIVED.
- Đây là mapping đề xuất, không phải SQL được duyệt hoặc live schema đã xác minh.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| 1 | id | Reply ID | BIGSERIAL | N/A | N/A | Yes | ● | Database-generated candidate | Checked-in DDL | 4 | Live generation chưa xác minh. |
| 2 | course_id | Course ID | BIGINT | N/A | N/A | Logical Yes; DDL nullable |  | parent.course_id | Parent discussion | 4 | Kế thừa cùng course là DERIVED. |
| 3 | user_id | Reply author ID | BIGINT | N/A | N/A | Logical Yes; DDL nullable |  | Authenticated Student principal ID | Bearer JWT/current auth helper | 4 | Không nhận user ID từ request. |
| 4 | parent_id | Parent topic ID | BIGINT | N/A | N/A | Yes for reply |  | Path discussion_id | Request path | 4 | Direct-child reply là DERIVED; cần xác nhận nested reply policy. |
| 5 | content | Reply content | TEXT | N/A | N/A | Yes |  | Decimal string của request int64 (proposal) | Request body | 4 | DISCREPANCY với logical string; conversion cần xác nhận. |
| 6 | status | Discussion status | VARCHAR(20) | 20 | N/A | DDL default ACTIVE |  | Rely on DDL default (candidate) | Checked-in DDL | 4 | Enum/visibility policy chưa được duyệt. |
| 7 | created_at | Created time | TIMESTAMP | N/A | N/A | Yes |  | Server current timestamp (DERIVED) | Server clock | 4 | DDL NOT NULL, không có default; live behavior chưa xác minh. |
| 8 | updated_at | Updated time | TIMESTAMP | N/A | N/A | Yes |  | Same value as created_at (DERIVED) | Server clock | 4 | DDL NOT NULL, không có default. |

## Contract fields without a direct physical column

| API field | Contract requirement | Physical mapping | Status |
|---|---|---|---|
| Request/response content | Request int64; reusable DiscussionComment.content:string | DDL discussions.content TEXT | DISCREPANCY; decimal string conversion is provisional. |
| comments[].discussion_id | Required logical int64 parent topic ID | Physical discussions.parent_id | DERIVED field mapping; no separate discussion_id column. |
| Counter | AC-19 mentions updated counters | No counter field/table in ERD/DDL | SOURCE_REQUIRED if persisted counter is intended; read-time count is a proposal. |

## Delete mapping

**Áp dụng khi**

- N/A — API #41 does not declare DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|
| — | N/A | N/A | N/A | N/A | No DELETE is specified. |

## Candidate mapping boundary

- DB guide, ERD and checked-in DDL are design evidence; live database metadata was not inspected.
- course_id and user_id are nullable in DDL but required in logical guide/ERD.
- title has no physical source for the updated Discussion response.
- Status, content conversion, timestamps, the DERIVED active-enrollment/topic access gate, counter meaning, response pagination and thread projection require confirmation.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `table`
- Dimension: `A1:BA35`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `19`
- Số vùng merge: `5`

<details>
<summary>Danh sách vùng merge</summary>

- `W34:BA34`
- `W14:BA14`
- `W15:BA15`
- `W19:BA19`
- `W32:BA32`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `A2` | № |  |
| 2 | `B2` | Tên table |  |
| 3 | `B3` | SB |  |
| 3 | `S3` | Độ dài |  |
| 3 | `T3` | Dấu phẩy thập phân |  |
| 3 | `U3` | Bắt buộc |  |
| 3 | `V3` | Main key |  |
| 3 | `W3` | Nội dung setting |  |
| 4 | `B4` | № |  |
| 4 | `C4` | Item ID |  |
| 4 | `I4` | Item name |  |
| 4 | `O4` | Kiểu |  |
| 5 | `A5` | 1 |  |
| 5 | `B5` | table id |  |
| 5 | `I5` | table name |  |
| 6 | `B6` | Update |  |
| 6 | `I6` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  > 0 |  |
| 21 | `B21` | Insert |  |
| 21 | `I21` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  = 0 |  |

</details>

