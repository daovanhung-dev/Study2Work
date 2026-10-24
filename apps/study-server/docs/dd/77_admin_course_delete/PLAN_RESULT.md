# Kết quả plan — API #77

## Phạm vi

Tạo DD Markdown cho `DELETE /api/v1/admin/courses/{course_id}` theo catalog và AC-32; sau đó rà nhóm #73–#77. Không sửa runtime source, database/schema/migration, catalog hoặc diagram. Study Server workflow dùng folder Markdown, không đóng gói ZIP.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Phân loại/context | `docs`, scope `server-study`; router, context-map, worklog guide, scope context và API workflow đã nạp. |
| Worklog preflight | Deno selector chọn worklog #48/#49/#50; cả ba đã đọc trước khi inspect sâu. |
| Skill/template | Registry xác nhận `createDD-markdown` cho Web/API DD; đã dùng đủ 8 template và giữ appendix chuẩn. |
| Catalog | Giữ nguyên DELETE path, Bearer/Admin, `course_id:int64!`, không body/query, `ApiEnvelope<DeleteResult>`, HTTP 200 và đúng error set 401/403/404/422/500. |
| AC-32 | Đọc toàn bộ flow: list #73 → detail #74 → metadata #75 hoặc status + audit #76 hoặc soft-delete theo policy #77 → reload. |
| DB/source | Đối chiếu legacy DDL và V1-PILOT nhưng không ghép BIGINT với UUID; không có route/module/test #77, Admin guard hoặc physical delete marker đã xác nhận. |
| Plan trước authoring | Requirement, Request Usage, Query, Mutation và Response Source matrices được ghi trong worklog trước khi tạo folder DD. |
| Authoring/static review | Tạo 8 sheet và 3 report; phân biệt contract trực tiếp, proposal `DERIVED`, nguồn cần xác nhận và trạng thái `UNWIRED / NOT_FOUND`. |
| AC-32 macro-review | Hoàn tất rà tài liệu #73–#77; cập nhật open questions, plans, verification reports và worklogs của năm API. Còn các quyết định owner/schema/runtime được liệt kê riêng. |

## Quyết định tài liệu

- `DeleteResult` giữ trực tiếp ba field `id`, `status="deleted"`, `deleted_at`; không tự phát minh cột hoặc map `archived_at` thành delete timestamp.
- AC-32 soft-delete intent là direct. Hard delete/cascade không được suy ra. Dependency gate cho enrollment/content và 422 khi bị policy block chỉ là proposal `DERIVED`.
- Legacy `enrollments.course_id` và `lessons.course_id` là query candidates; không chứng minh dependency list hoàn chỉnh hoặc live FK. Generic content relation chưa được xác nhận.
- Không copy audit side effect của #76 sang #77. Transaction atomicity là proposal; schema, marker, actor/guard, retry và repeat-delete behavior còn mở.
- Macro-review giữ #75 metadata-only, #76 status + audit intent, #77 soft-delete-only. #73/#74/#75/#76 `Page<Course>` wrapper giữ theo catalog; #77 `DeleteResult` không bị ép vào Page.
- Không chạy application tests vì đây là docs-only task. Static DD verification không chứng minh route, Admin auth, live schema, DB mutation hoặc runtime.

## Trạng thái

`Draft — Needs Confirmation`; chưa implementation-ready do dependency/delete policy, Admin guard, physical soft-delete mapping, live schema, response/error integration, visibility và retry semantics chưa được quyết định.
