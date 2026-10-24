# Kết quả plan — API #79 Lấy chi tiết Content

## Phạm vi

Tạo DD Markdown cho `GET /api/v1/admin/content/{content_id}` theo catalog và AC-33. Không sửa runtime, schema/migration, catalog, diagram hoặc client. Study workflow chỉ yêu cầu Markdown folder; không tạo ZIP.

## Input/source manifest

| Source | Đơn vị/phạm vi đọc | Evidence sử dụng | Status |
|---|---|---|---|
| `docs/lists/list_api.md` | API #79, #78–#81 và reusable Content | Direct path/auth/input/response/errors; Content fields | DIRECT |
| `AC_UNICA/00_AC_API_INDEX.md` | Toàn bộ AC-33 entry | Admin actor, pending precondition, four endpoint sequence | DIRECT |
| `AC_04_ADMIN_MANAGEMENT.drawio` | Toàn bộ trang AC-33 nodes/edges | #78 queue, #79 reads content/version/author, #80/#81 branches, reload | DIRECT |
| DD #78 | Overview/Request/Response/Mapping/Open Questions/Report | Queue state, response contract mismatch, revision/stale-item questions | Existing Draft evidence |
| DD #69 and #74 | Admin detail response/mapping patterns | Keep catalog singleton; distinguish direct Page from derived singleton | Pattern/reference only |
| Legacy `DB.sql`, `DB_UNICA_TABLES.md` | Relation inventory | No generic Content/version/author relation | Legacy artifact |
| V1-PILOT `02_study_db.sql` | course_versions, content_blocks, content_review_decisions | UUID model, course-version creator, reviewer decision-log boundary | PILOT ARTIFACT; live DB unknown |
| Current Study router/auth/middleware/responses/tests | API #79 path/module/guard/error/test scan | Route absent; Student-only guard; allowlist/error discrepancies | CURRENT SOURCE |
| Registered createDD-markdown template/skill/workflow | Manifest, skill, eight sheets, Study workflow | 11-file Markdown delivery; appendices and no ZIP | REGISTRY-WIRED |

## API Requirement Matrix

| Requirement | Source | DD coverage | Status |
|---|---|---|---|
| GET path + Bearer Admin | Catalog #79; AC-33 | Cover/Overview/Request/Mapping/Error | DIRECT requirement; runtime guard absent |
| Required `content_id:int64!` | Catalog #79 | Request + Request Usage/Query matrices | DIRECT |
| Success | Catalog #79 | Response/Mapping | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Content>` DIRECT |
| Errors | Catalog #79 | Error/Mapping | Exact 401/403/404/500 only |
| Detail workflow | AC-33 nodes n5–n7 | Overview/Mapping/Open Questions | #78 selection → #79 detail → decision |
| Metadata read | AC-33 node n6 | Overview/Mapping/Response/Open Questions | `content/version/author` read intent DIRECT; schema/response discrepancy |
| No mutation in #79 | GET route + AC-33 | Overview/Mutation Matrix/table mapping | Read-only; #80/#81 own decisions/audit |

## Quyết định tài liệu

- Giữ exact catalog contract, nhất là `ApiEnvelope<Content>` và tám Content fields; không thêm version/author/reviewer fields.
- Ghi discrepancy AC-33 n6 `content/version/author` so với catalog/reusable schema. Version/author reads là Q2/Q3 logical `SOURCE_REQUIRED`, không viết SQL.
- Candidate Q1 lọc `Content.id = :content_id`. Không thêm `PENDING_REVIEW` predicate cho detail; trạng thái row được trả như đã đọc. Đây là `DERIVED`, stale-item policy mở.
- Không chọn legacy resources/lessons hoặc pilot UUID `content_blocks` làm Content table. Không chuyển đổi UUID sang BIGINT.
- Phân biệt pilot `course_versions.created_by_subject_id` (Course version creator) và `content_review_decisions.reviewer_subject_id` (reviewer); chưa có Content author mapping.
- #79 không ghi decision/audit hoặc thay đổi status; `07_table.md` là `N/A — READ-ONLY API`.
- Giữ Admin auth, error allowlist và `data:null`/`{}` helper mismatch như integration gaps.

## Trạng thái

`Draft — Needs Confirmation`; chưa implementation-ready do AC-33 metadata projection, Content/version/author persistence, revision identity qua #78–#81, Admin guard, pending/stale detail rule và error integration chưa được quyết định. AC-33 macro-review #78–#81 đã hoàn tất ở mức tài liệu; các câu hỏi chưa có nguồn được giữ lại trong [báo cáo review nhóm](../81_admin_content_reject/VERIFICATION_REPORT.md).
