# Kết quả plan — API #73

## Phạm vi

Tạo DD Markdown cho `GET /api/v1/admin/courses` theo catalog và AC-32. Chỉ tạo tài liệu; không sửa source, schema, migration, catalog hoặc diagram. Study workflow yêu cầu Markdown và không tạo ZIP.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Phân loại | `docs`; `server-study`; không có cross-scope dependency. |
| Worklog preflight | Deno selector chọn #48/#49/#50; đọc đầy đủ cả ba trước khi inspect sâu. |
| Diagram/catalog | Đọc API #73 và reusable Course/Page/PageMeta; parse toàn bộ nodes/edges AC-32; chuỗi list → detail → update/status/delete → reload được giữ. |
| Source/schema | Không có route/module/test #73; đối chiếu API #06 source/tests, Admin list #68, legacy DDL, V1-PILOT và category gap. |
| Plan-before-authoring | Requirement, Request Usage, Query, Mutation, Response Source matrices được ghi trong worklog trước khi tạo folder DD. |
| Authoring | Tạo 8 template sheets và 3 reports; proposal được phân biệt khỏi contract trực tiếp. |
| Group review | Đã macro-review #73–#77 sau khi tạo DD #77; cập nhật open questions, plans và verification reports liên quan. |

## Quyết định tài liệu

- Giữ nguyên response direct `ApiEnvelope<Page<Course>>` và errors 401/403/422/500.
- Page default 1, fixed size 20, `id ASC`, empty list 200, exact-match filters và không default `PUBLISHED` là proposal `DERIVED` dựa trên API #06/#68 và Admin management intent.
- `category` là query field direct nhưng physical relation chưa có nguồn; không tạo `category_id`, bảng nối, JOIN hoặc behavior reject.
- Legacy BIGINT `courses/users` chỉ là query candidate; V1-PILOT UUID/versioned course model và live schema được tách.
- Map Course fields theo schema; Course.category optional được omit cho đến khi có source; không trả mentor PII ngoài UserSummary.
- Mentor missing/price invalid đề xuất safe 500 theo API #06; Admin recovery behavior vẫn cần owner xác nhận.
- `07_table.md` là N/A — READ-ONLY API.

## Trạng thái

Draft — Needs Confirmation. API #73 chưa wired/implementation-ready vì Admin guard, course-category relation, live schema và enum/casing chưa được xác nhận. AC-32 macro-review hoàn tất ở mức tài liệu; các gap còn lại cần owner/schema/runtime quyết định.
## Kết quả macro-review AC-32

#73 list giữ `Page<Course>`; filter category chưa có relation nguồn. Nếu #77 soft-delete thành công, ẩn khỏi list là đề xuất nhất quán nhưng predicate vật lý chưa được chốt. Các API #74–#76 giữ wrapper đúng catalog; #77 dùng `DeleteResult`. Admin guard, CourseStatus casing, counters, schema lựa chọn và error integration còn mở.
