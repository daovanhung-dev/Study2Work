---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các lỗi normative của API #15 theo contract design. Endpoint public nên không tạo lỗi authentication/authorization. Selection gap của Enrollment được giữ trong remarks/open questions, không invent business code mới.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Path/resource validation | TBD | course_id | Path không parse được thành int64; contract không khai báo 422 nên dùng candidate 404 theo pattern API #8. | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A — envelope message | 05_Data_Mapping.md, steps 1.1/1.2/5.2 | No | Derived handling; cần review nếu contract runtime bổ sung 422. |
| 2 | Not found | Yes | course | Q1 không trả course record cho course_id. | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A — envelope message | 05_Data_Mapping.md, steps 3.1/5.2 | No | Visibility predicate PUBLISHED cần confirmation. |
| 3 | Not found | Yes | enrollment | Q2 không trả enrollment record theo selection policy được phê duyệt. | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A — envelope message | 05_Data_Mapping.md, steps 3.2/5.2 | No | User identity và single-row rule còn SOURCE_REQUIRED. |
| 4 | Database/system error | No | courses/enrollments | SQL query, response mapping hoặc source resolution thất bại. | 500 | DESIGN_INTERNAL_ERROR | N/A — envelope message | 05_Data_Mapping.md, steps 3.3/5.3 | No | Không trả raw SQL, stack trace hoặc internal detail. |

> Không thêm lỗi 401, 403, 422 hoặc 409 vì contract API #15 không khai báo và endpoint được xác định là Public.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/06_Error.md.
- Sheet logic: 4.Error.
