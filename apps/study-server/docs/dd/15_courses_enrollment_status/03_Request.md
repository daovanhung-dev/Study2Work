---
title: "Request"
order: 3
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "1.Request"
format: markdown
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | GET |
| URI | /api/v1/courses/{course_id}/enrollment-status |
| Character encoding | UTF-8 |
| Content-Type | N/A — GET không có request body |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | No | N/A — public endpoint | Contract không yêu cầu Bearer token. | 05_Data_Mapping.md, step 0.1 |
| 2 | Content type | Content-Type | No | N/A — request không có body | Không có JSON body cần gửi. | 05_Data_Mapping.md, step 1.1 |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | Course ID | course_id | int64 | Yes | N/A — contract chưa đặc tả | N/A — contract chưa đặc tả | Integer path segment | N/A | N/A | ID course cần kiểm tra enrollment status. | 05_Data_Mapping.md, step 1.1/1.2 |

## Query parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Endpoint không có query parameter. | N/A |

## Request body

| No | Logical name | Physical name | Type | Required | Min | Max | Character type | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | GET endpoint không có request body. | N/A |

> Không nhận user_id, student_id, Bearer token hoặc user identity bổ sung ngoài contract.

## Ví dụ Request

```text
GET /api/v1/courses/101/enrollment-status HTTP/1.1
Host: api.example.test
```

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/03_Request.md.
- Sheet logic: 1.Request.
