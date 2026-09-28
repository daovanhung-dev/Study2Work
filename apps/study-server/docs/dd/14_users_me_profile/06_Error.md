---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các trường hợp lỗi normative của API #14 theo `list_api.md`, được tách khỏi current runtime vì endpoint chưa wired.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication error | `Yes` | `Authorization/JWT` | Thiếu header, header không phải Bearer, token sai chữ ký/hết hạn, claim `sub`/`roles` không hợp lệ hoặc user identity không xác nhận được. | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `N/A — envelope message` | `05_Data_Mapping.md`, steps `0.1/0.2/2.5/6.2` | `No` | Theo contract và current API #4 pattern. |
| 2 | Authorization error | `Yes` | `roles` | JWT hợp lệ nhưng không chứa role `STUDENT`. | `403` | `DESIGN_ACCESS_DENIED` | `N/A — envelope message` | `05_Data_Mapping.md`, step `0.3/6.3` | `No` | Không tạo role/business code mới. |
| 3 | Required/length/type validation | `Yes` | `full_name` | Thiếu, `NULL`, không phải string hoặc vượt quá 150 ký tự. | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — fieldErrors` | `05_Data_Mapping.md`, step `2.1/6.4` | `No` | Max 150 theo current schema; blank policy TBD. |
| 4 | Required/type validation | `Yes` | `bio` | Thiếu, `NULL` hoặc không phải string theo contract. | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — fieldErrors` | `05_Data_Mapping.md`, step `2.2/6.4` | `No` | Persistence column chưa có source; validation contract vẫn được ghi nhận. |
| 5 | Required/length/type validation | `Yes` | `phone` | Thiếu, `NULL`, không phải string hoặc vượt quá 20 ký tự. | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — fieldErrors` | `05_Data_Mapping.md`, step `2.3/6.4` | `No` | Contract required nhưng schema nullable; blank/clear policy TBD. |
| 6 | Format/required validation | `TBD` | `avatar_url` | Nếu semantics được khóa là required mà field thiếu/null, hoặc giá trị không phải URI theo policy được phê duyệt. | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — fieldErrors` | `05_Data_Mapping.md`, step `2.4/6.4` | `No` | `avatar_url...:uri!` chưa giải quyết requiredness/nullable. |
| 7 | Request parsing/format validation | `Yes` | `request body` | Body không phải JSON object hoặc không parse được theo request contract. | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — fieldErrors` | `05_Data_Mapping.md`, step `1.1/6.4` | `No` | Không tự thêm media type ngoài current convention. |
| 8 | Authentication inconsistency | `TBD` | `users` | JWT hợp lệ nhưng không có row `users.id = JWT.sub`, hoặc affected rows bằng `0`. | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `N/A — envelope message` | `05_Data_Mapping.md`, steps `2.5/3.4/6.2` | `No` | Contract không khai báo `404`; kế thừa current API #4 mapping, cần review khi implementation. |
| 9 | Database/system error | `No` | `users` | SQL update, commit, reload hoặc `UserProfile` mapping thất bại. | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | `05_Data_Mapping.md`, steps `3.4/3.5/4.2/6.5` | `Yes — nếu transaction đã bắt đầu` | Không trả raw SQL, stack trace, token hoặc credential. |

> Mỗi error case và mỗi field validation nằm trên một row riêng. `DESIGN_*` codes ở đây là design proposal theo `code_http.md`, chưa phải runtime catalog proof.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/06_Error.md`.
- Sheet logic: `4.Error`.

