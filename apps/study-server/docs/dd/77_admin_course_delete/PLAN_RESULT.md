# Kết quả plan — API #77

## Phạm vi

Implement `DELETE /api/v1/admin/courses/{course_id}` from catalog and AC-32, then update its Markdown DD/context and review linked #73–#76 behavior. No catalog, diagram, DDL or migration change. Study Server DD stays Markdown-only.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Phân loại/context | `coding`, secondary `test/docs`, scope `server-study`; router, context-map, scope context và API workflow đã nạp. |
| Worklog preflight | Deno selector chọn #74/#75/#76; cả ba đã đọc trước khi inspect sâu; không thiếu. |
| Skill/template | Registry xác nhận `createDD-markdown`; dùng 8 template sheets hiện hữu và giữ nguyên appendix suffix. |
| Catalog | Giữ nguyên DELETE path, Bearer/Admin, `course_id:int64!`, không body/query, `ApiEnvelope<DeleteResult>`, HTTP 200 và đúng error set 401/403/404/422/500. |
| AC-32 | Đọc toàn bộ flow: list #73 → detail #74 → metadata #75 hoặc status + audit #76 hoặc soft-delete theo policy #77 → reload. |
| DB/source | Đối chiếu legacy BIGINT và V1-PILOT UUID; dùng `status='DELETED'`/`updated_at` theo API #72 và dependency relations từ legacy DDL. Live schema chưa xác minh. |
| Plan trước code | Classification, source trace, discrepancies và implementation plan được ghi vào worklog trước runtime/DD/context edits. |
| Implementation | Thêm API #77 module/route, Admin/int64 validation, dependency checks, atomic soft-delete, safe rollback và focused HTTP tests. |
| AC-32 macro-review | Rà linked #73–#76 visibility/mutation boundaries; giữ nguyên contract/code của các API đó trong one-API scope, ghi rõ restore/writer gaps trong DD. |
| Authoring/static review | Cập nhật 8 sheet + 3 report, giữ Draft, đánh dấu fallback `DERIVED`, chuẩn bị kiểm tra appendix/links/examples. |

## Quyết định tài liệu

- `DeleteResult` giữ đúng ba field `id`, `status="deleted"`, `deleted_at`; `deleted_at` map từ persisted `courses.updated_at` theo API #72.
- AC-32 soft-delete intent là direct; status marker, timestamp mapping, blocker set/422 và repeated-delete 404 là `DERIVED`.
- Blocker set: any enrollment, active `contents`, lesson, quiz or assignment. No child delete/cascade.
- Shared role `ADMIN` is used; dedicated course-management permission remains open.
- No #76 audit side effect, new relation/column, migration, Idempotency-Key or error code is added.
- Application tests and local HTTP/OpenAPI checks were run; they use fake DB sessions and do not prove live schema/deployment.
- #73/#74 continue to expose `DELETED`; #76 may replace the marker, and Mentor writers were not changed. These linked lifecycle questions remain open.

## Trạng thái

`Draft — Needs Confirmation`; local implementation is verified, but dependency/marker policy, finer Admin permission, live schema, post-delete visibility/restore and retry semantics require owner confirmation.
