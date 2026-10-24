# Kết quả plan — API #78 Lấy pending content

## Phạm vi

Tạo DD Markdown cho `GET /api/v1/admin/content/pending` theo catalog và AC-33. Không sửa runtime, schema/migration, catalog, diagram hoặc client. Study workflow chỉ yêu cầu Markdown folder; không tạo ZIP.

## Input/source manifest

| Source | Đơn vị/phạm vi đọc | Evidence sử dụng | Status |
|---|---|---|---|
| `docs/lists/list_api.md` | Rows #78–#81, reusable Content/Page/PageMeta | Request/response/error contract, AC-33 endpoint order | DIRECT |
| `AC_UNICA/00_AC_API_INDEX.md` | AC-22 and AC-33 sections | Actors, preconditions, queue/review sequence | DIRECT |
| `AC_04_ADMIN_MANAGEMENT.drawio` | Full page AC-33 nodes and edges | Pending queue predicate, #79 detail, #80/#81 decisions, reload | DIRECT |
| `AC_03_MENTOR_TEACHING.drawio` | Full page AC-22 nodes and edges | Content create/update/publish/delete producer context | DIRECT logical flow |
| DD #49–#53 | Overview/request/response/mapping/open questions and linked lifecycle findings | Content projection, PENDING_REVIEW proposals, version/delete questions | Existing Draft evidence; proposals remain DERIVED |
| DD #68 and #73 | Response/list patterns | Cardinality mismatch and direct Page precedent | Related DD evidence; does not override catalog #78 |
| `DB_UNICA_TABLES.md`, legacy `DB.sql` | Content relation/table inventory | No generic Content queue relation | Legacy design artifact; live DB unknown |
| `infra/postgres/02_study_db.sql` | `content_blocks`, `content_review_decisions` | UUID/version/lesson model and append-only decision-log boundary | PILOT ARTIFACT; not catalog mapping |
| Current Study router/auth/middleware/responses/tests | API #78 path/module/guard/error scan | No route/module/test; Student-only guard; allowlist/error discrepancies | CURRENT SOURCE |
| Registered template/skill/workflow | Manifest, `createDD-markdown`, 8 templates, Study docs workflow | 11-file Markdown delivery and appendix baseline | Registry-wired |

## API Requirement Matrix

| Requirement | Source | DD coverage | Status |
|---|---|---|---|
| GET path + Bearer Admin | Catalog #78; AC-33 | Cover, Overview, Request, Mapping, Error | DIRECT requirement; runtime guard absent |
| Optional `type`, `course`, `page` | Catalog #78 | Request + usage/query matrices | DIRECT fields; interpretation partly open |
| Pending predicate | AC-33 diagram node n3 | Overview/Mapping/Response | DIRECT `status=PENDING_REVIEW` |
| Success contract | Catalog #78 | Response/Mapping | DIRECT `ApiEnvelope<Content>`; cardinality conflict retained |
| Errors | Catalog #78 | Error/Mapping | Exact 401/403/500 only |
| Detail/decision/reload sequence | AC-33 nodes n5–n12 | Overview/Mapping/Open Questions | #79 detail; #80 approve; #81 reject; #78 has no mutation |

## Quyết định tài liệu

- Giữ exact direct response `ApiEnvelope<Content>`. `Page<Content>` là proposal `DERIVED` riêng, cần owner/catalog correction vì endpoint/page query biểu thị list.
- Dùng `status=PENDING_REVIEW` làm logical fixed predicate. Không khẳng định mọi POST #50 hoặc update #51 đều thực sự đưa revision vào trạng thái này.
- `type` → `content_type` và `course` → `course_id` exact filters là candidate; physical table, enum/casing và live schema chưa xác nhận.
- Nếu Page được duyệt: candidate page 1-based/default 1, fixed size 20, `id ASC`, count cùng predicates, empty list 200. Không thêm query `size`/`sort` vào contract hiện tại.
- #78 chỉ map các field reusable của Content; author/version thuộc #79; approval/rejection/audit thuộc #80/#81.
- Legacy schema thiếu generic Content; V1-PILOT `content_blocks`/`content_review_decisions` không map trực tiếp sang Content BIGINT. Không viết executable SQL hoặc mutation mapping.
- Current Study source không có Admin route/guard; no application test or live DB verification was run.

## Trạng thái

`Draft — Needs Confirmation`; chưa implementation-ready do list cardinality/page contract, Content/version persistence, enum/type matching, queue version/deletion visibility, Admin guard và error integration chưa được quyết định. AC-33 macro-review #78–#81 đã hoàn tất ở mức tài liệu; các câu hỏi chưa có nguồn được giữ lại trong [báo cáo review nhóm](../81_admin_content_reject/VERIFICATION_REPORT.md).
