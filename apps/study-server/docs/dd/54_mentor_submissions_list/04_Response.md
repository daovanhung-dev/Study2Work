---
title: "Response"
order: 4
dd_id: "54"
api_name: "Lấy submissions"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json |
| Success HTTP status | 200 |
| Success business code | DESIGN_RESOURCE_RETRIEVED |
| Contract data type | ApiEnvelope<Page<Submission>> |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---:|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 4 | Fixed by branch | N/A | Success 200; errors 401/403/409/422/500. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 4 | true on success, false on error | Always present | Shared envelope. |
| 3 | businessCode | Business code | businessCode | string | No | API catalog | Catalog literal | 4 | Fixed by branch | Always present | DESIGN_* code. |
| 4 | message | Message | message | string | No | Application | Safe message | 4 | Fixed by branch | Always present | English text follows current API #46/#49 style. |
| 5 | data | Page<Submission> | data | object / null | Yes | N/A | N/A | 3/4 | Page object on success; null on error | Null on error | Fallback to resolve list/select versus previous singular type. |
| 5.1 | data.items | Submission list | items | Submission[] | No | assignment_submissions (candidate) | Selected columns | 2/3 | Map each row | Empty array when no matches | Ordered by `submitted_at DESC, id DESC`. |
| 5.1.1 | data.items[].id | Submission ID | id | int64 | No | assignment_submissions | id | 2/3 | Direct | Positive integer | BIGSERIAL candidate. |
| 5.1.2 | data.items[].assignment_id | Assignment ID | assignment_id | int64 | No | assignment_submissions | assignment_id | 2/3 | Direct | Required after inner join | Nullable DDL rows are excluded. |
| 5.1.3 | data.items[].user_id | Student ID | user_id | int64 | No | assignment_submissions | user_id | 2/3 | Direct | Required after inner join to users | Not accepted from request. |
| 5.1.4 | data.items[].content | Submission content | content | string | Yes | assignment_submissions | content | 2/3 | Preserve nullable value | Omitted when null | Candidate DDL permits NULL. |
| 5.1.5 | data.items[].files | Submitted files | files | UploadAsset[] | No | uploads (candidate) | id, file_name, url, content_type, size_bytes, status | 2/3 | Exact URL + owner + purpose + course lookup | Empty array if no matching metadata | Derived relation; at most one item from `file_url`. |
| 5.1.6 | data.items[].status | Submission status | status | SubmissionStatus/string | No | assignment_submissions | status | 2/3 | Preserve database value | Exact stored value | Enum/lifecycle unresolved. |
| 5.1.7 | data.items[].submitted_at | Submission time | submitted_at | date-time | No | assignment_submissions | submitted_at | 2/3 | ISO date-time serialization | Always present | DDL is TIMESTAMP; timezone semantics remain open. |
| 5.1.8 | data.items[].score | Score | score | decimal-string | Yes | assignment_submissions | score | 2/3 | `str(DB value)` | Omitted when null | Candidate NUMERIC(6,2). |
| 5.1.9 | data.items[].feedback | Grader feedback | feedback | string | Yes | assignment_submissions | feedback | 2/3 | Preserve nullable value | Omitted when null | Disclosure timing remains open. |
| 5.2 | data.pagination | Page metadata | pagination | PageMeta | No | Query result | page/size/total | 4 | Derived from request and count | Always present | `total_pages=0` when total is 0. |
| 5.2.1 | data.pagination.page | Current page | page | int32 | No | Request | page | 1/4 | Default 1 | Positive integer | 1-based. |
| 5.2.2 | data.pagination.size | Fixed page size | size | int32 | No | Shared constant | DEFAULT_SIZE | 4 | Value 20 | Always 20 | Reuses the project shared default. |
| 5.2.3 | data.pagination.total | Matching records | total | int64 | No | COUNT query | COUNT(*) | 2/4 | Direct integer | Non-negative | Uses same access and filter predicates as list query. |
| 5.2.4 | data.pagination.total_pages | Page count | total_pages | int32 | No | Count + size | N/A | 4 | Ceiling division | 0 when total=0 | Derived. |
| 6 | meta | Envelope metadata | meta | object | No | N/A | N/A | 4 | Empty object | Always present | Pagination stays inside `data.pagination`. |
| 7 | traceId | Trace ID | traceId | uuid | No | Trace context | Request trace ID | 4 | Propagate UUID | Always present | Shared convention. |

### Ví dụ thành công — HTTP 200

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Submissions retrieved.",
  "data": {
    "items": [
      {
        "id": 54001,
        "assignment_id": 1201,
        "user_id": 804,
        "content": "Illustrative submission text.",
        "files": [
          {
            "id": 34001,
            "name": "answer.pdf",
            "url": "https://storage.example/answer.pdf",
            "content_type": "application/pdf",
            "size_bytes": 12345,
            "status": "UPLOADED"
          }
        ],
        "status": "SUBMITTED",
        "submitted_at": "2026-10-24T09:30:00",
        "score": "8.50"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 1,
      "total_pages": 1
    }
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000054"
}
~~~

Example values are illustrative. File resolution is a DERIVED URL match and local tests do not verify the live database relation.

### Ví dụ lỗi — HTTP 403

~~~json
{
  "success": false,
  "businessCode": "DESIGN_ACCESS_DENIED",
  "message": "Access denied.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000054"
}
~~~

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `2.Response`
- Dimension: `A2:BR45`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `52`
- Số vùng merge: `15`

<details>
<summary>Danh sách vùng merge</summary>

- `B14:C15`
- `B16:C16`
- `B21:C21`
- `B22:BA22`
- `B23:C23`
- `B24:C24`
- `D14:S14`
- `T14:AK14`
- `AL14:BA15`
- `B20:C20`
- `B17:C17`
- `B18:C18`
- `T18:AB18`
- `AC18:AK18`
- `B19:BA19`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Giải thích |  |
| 4 | `C4` | Giá trị trả về khi call API |  |
| 9 | `B9` | Format |  |
| 9 | `L9` | JSON |  |
| 10 | `B10` | Code ký tự |  |
| 10 | `L10` | UTF-8 |  |
| 11 | `B11` | Content-Type |  |
| 11 | `L11` | application/json |  |
| 14 | `B14` | No |  |
| 14 | `D14` | Response item name |  |
| 14 | `T14` | Refer DB |  |
| 14 | `AL14` | Remarks |  |
| 15 | `D15` | Tên logic |  |
| 15 | `L15` | Tên vật lý |  |
| 15 | `T15` | Table nguồn get |  |
| 15 | `AC15` | Field nguồn get |  |
| 16 | `B16` | 1 |  |
| 16 | `D16` | HTTP Status |  |
| 16 | `L16` | HTTPStatus |  |
| 16 | `AL16` | Thành công: 200/ Phát sinh lỗi: 500/ Validate lỗi: 400 |  |
| 17 | `B17` | 2 |  |
| 17 | `D17` | Status |  |
| 17 | `L17` | status |  |
| 17 | `AL17` | Thành công: 1/phát sinh error: 2 |  |
| 18 | `B18` | 3 |  |
| 18 | `D18` | Nội dung response |  |
| 18 | `L18` | response |  |
| 19 | `B19` | Trường hợp thành công |  |
| 20 | `B20` | 3.1 |  |
| 21 | `B21` | 3.2 |  |
| 22 | `B22` | Các trường hợp lỗi của API |  |
| 23 | `B23` | 3.1 |  |
| 23 | `D23` | Error code |  |
| 23 | `M23` | error_code |  |
| 24 | `B24` | 3.2 |  |
| 24 | `D24` | Error Message id |  |
| 24 | `M24` | error_message_id |  |
| 26 | `B26` | Ví dụ |  |
| 27 | `M27` | Trường hợp thành công |  |
| 28 | `N28` | { |  |
| 29 | `O29` |   "status": 1, |  |
| 30 | `O30` |   "response":{ |  |
| 33 | `O33` | } |  |
| 34 | `N34` | } |  |
| 36 | `M36` | Trường hợp lỗi |  |
| 37 | `N37` | { |  |
| 38 | `O38` | "status" : 2 , |  |
| 39 | `O39` | "response" : {  |  |
| 40 | `P40` | "error_code" : "9999", |  |
| 41 | `P41` | "error_message_id" : "DLG000000" |  |
| 42 | `O42` |  } |  |
| 43 | `N43` |  } |  |

</details>
