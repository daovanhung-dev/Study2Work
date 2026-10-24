# Verification Report — API #51 Cập nhật nội dung Mentor

## Phạm vi

Kiểm tra bộ DD Markdown API #51, catalog/diagram, schema boundary, route/test source, response/middleware helper, template appendices và logic cặp #50↔#51. Chỉ tạo `apps/study-server/docs/dd/51_mentor_content_update/` và worklog. Không sửa runtime, database, catalog, diagram hay client. Không chạy application tests vì đây là task docs-only và API #51 chưa có implementation.

## Deliverable manifest

| File | Vai trò | Trạng thái |
|---|---|---|
| `00_Cover.md` | Cover | PASS |
| `01_Lich_su.md` | Lịch sử | PASS |
| `02_Overview.md` | Overview | PASS |
| `03_Request.md` | Contract path + body proposal | PASS |
| `04_Response.md` | Envelope và Content projection | PASS |
| `05_Data_Mapping.md` | Query/mutation/response matrices | PASS |
| `06_Error.md` | Error cases | PASS |
| `07_table.md` | Logical Content/version mapping | PASS |
| `PLAN_RESULT.md` | Pre-authoring plan, sources and matrices | PASS |
| `OPEN_QUESTIONS.md` | Contract/schema/lifecycle questions | PASS |
| `VERIFICATION_REPORT.md` | Verification record | PASS |

## Template fingerprints

SHA256 của 8 file nguồn trong `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/`:

| Template | SHA256 |
|---|---|
| `00_Cover.md` | `fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63` |
| `01_Lich_su.md` | `d1cec6573433a9551812bf47552f8a44d7c533d790341047c410e1d57771e` |
| `02_Overview.md` | `c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6` |
| `03_Request.md` | `37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa` |
| `04_Response.md` | `5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8` |
| `05_Data_Mapping.md` | `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b` |
| `06_Error.md` | `e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b` |
| `07_table.md` | `4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356` |

All 8 DD sheets carry the expected `dd_id: "51"` and `Draft — Needs Confirmation` front matter. Their template appendix tails byte-match both API #50's corresponding appendix and the registered template.

## Contract and source checks

| Check | Result | Evidence |
|---|---|---|
| Catalog contract | `PUT /api/v1/mentor/content/{content_id}`, Bearer Mentor, `content_id:int64!`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, `ApiEnvelope<Content>` retained | PASS — catalog #51 |
| Request body | Catalog and AC-22 PUT node omit body; DD preserves that omission and separates the proposed `{content_type,title,payload}` replacement body as `DERIVED` | PASS — discrepancy explicit |
| AC-22 sequence | PUT → logical `UPDATE Content + version` → reload tree | PASS — diagram |
| AC-33 review evidence | Admin queue reads `PENDING_REVIEW` and reviewer reads content/version/author; transition of a new revision to pending is marked `DERIVED` | PASS — diagram + evidence boundary |
| Error set | Exactly 401/403/404/422/500 with the matching `DESIGN_*` codes; no concurrency 409 added | PASS — catalog + five error rows |
| Response coverage | All 8 Content fields mapped or marked derived/source-required; no undeclared `version` field added | PASS — static matrix check |
| Schema | Legacy schema has no generic Content/version mapping; V1-PILOT UUID `content_blocks` is not substituted | PASS — DDL/design artifacts; live schema remains unverified |
| Route/module/test | No API #51 route/module or API-specific test reference found in current app/tests source trees | PASS — current-source scan |
| Middleware/helper | `error_response` returns the six-key envelope with missing `data` as `{}`; path is absent from `DESIGN_CONTRACT_PATHS`, so generic validation/internal fallback codes apply if wired without allowlist update | PASS — current helper, conditional future discrepancy |

## Document integrity checks

- Exact pre-report manifest: 8 sheets + `PLAN_RESULT.md` + `OPEN_QUESTIONS.md`; adding this report gives 11 files.
- Template appendix comparison passed for all 8 sheets.
- Request fields and all Content response fields are covered; mutation values are listed field by field.
- Success and error JSON examples parse; example enum member is explicitly a non-executable placeholder.
- Relative Markdown links resolve; Markdown table widths are consistent; code fences are balanced; no trailing whitespace.
- `git diff --check` returned no diagnostics.
- `deno run --allow-read scripts/validate-contracts.mjs` could not start: `ajv/dist/2020.js` is not a declared Deno dependency, and `node`/`nodejs` are unavailable in PATH. Recorded as `DECLARED_NOT_RUNNABLE`; DD-specific catalog and markup checks above passed.
- SHA256 manifest of the 10 files present before this report (sorted filenames plus per-file SHA256): `b5eea46bffa619eb8a4506a164d8135ac7d8c6f99523564811244143351636d3`.

## Pair review and remaining scope

- API #50 create and #51 update use the same `Content` response shape. #51 derives its target course from the stored Content and does not accept a replacement course ID.
- Both pending-review transitions remain design proposals. #51 preserves existing tree placement while proposing a new version; physical schema/version semantics remain unresolved.
- Full AC-22/AC-33 macro-review of #49–#53 is complete with open questions, especially the relationship between Admin approval and Mentor publish/unpublish; see the section below.
- No application tests were run. These checks establish document consistency only, not API runtime, DB migration, or live schema readiness.

## AC-22/AC-33 Macro-review #49–#53

**Status:** VERIFIED_WITH_OPEN_QUESTIONS.

- Đã rà soát chuỗi AC-22: #49 đọc → #50 tạo → #51 cập nhật Content + version → #52 publish/unpublish → #53 soft delete; mỗi mutation reload tree theo diagram.
- #50/#51 cùng đề xuất PENDING_REVIEW cho Content/revision mới; đây vẫn là DERIVED.
- #52 sở hữu publication-status update; proposal #53 yêu cầu unpublish PUBLISHED qua #52 trước khi delete, không tự đổi Content.status.
- #53 dùng parent_id làm dependency trực tiếp duy nhất có thể suy ra; child hiện hữu chặn bằng 422 proposal; không cascade/reparent. Soft delete bảo toàn history theo proposal.
- AC-33 approve node ghi APPROVED/PUBLISHED + audit nên chưa thể xác định approval có tự publish hay không.
- #49 trả singular Content dù purpose là tree. Cách loại soft-deleted items khỏi #49, public views và AC-33 queue cần xác nhận.
- Generic Content persistence/version schema, Mentor principal/assignment, payload/enums, readiness, dependency set, soft-delete/audit fields và middleware mapping đều còn SOURCE_REQUIRED.
- Không chạy application tests; DD/source review không chứng minh API runtime hoặc live schema.

