---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Error"
format: markdown
---

# Error

## Error mapping

| HTTP status / Code | Error | Condition | Source |
|---|---|---|---|
| `422` | `Validation Error` | Schema/password policy invalid | Explicit AC flow |
| `409` | `Conflict` | Email already exists | Explicit AC flow |

## Quy tắc

- Không tạo business code mới nếu diagram không định nghĩa.
- Lỗi authentication/authorization/validation chưa có HTTP status explicit được giữ `TBD`.
- System error envelope và trace/business code là `SOURCE_REQUIRED` trong target DD nếu diagram không khóa.
