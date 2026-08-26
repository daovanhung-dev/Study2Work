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
| `403` | `Forbidden` | No resource access | Explicit AC flow |
| `404` | `Not Found` | Resource does not exist | Explicit AC flow |

## Quy tắc

- Không tạo business code mới nếu diagram không định nghĩa.
- Lỗi authentication/authorization/validation chưa có HTTP status explicit được giữ `TBD`.
- System error envelope và trace/business code là `SOURCE_REQUIRED` trong target DD nếu diagram không khóa.
