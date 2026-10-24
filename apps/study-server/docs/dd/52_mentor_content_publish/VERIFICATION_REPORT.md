# Verification Report — API #52 Publish/unpublish nội dung Mentor

## Phạm vi

Kiểm tra bộ DD Markdown #52, catalog/diagram, cross-API lifecycle, current Study route/middleware/schema evidence, template appendix equality và document integrity. Không sửa runtime, schema, catalog, diagram, client hoặc deployment. Không chạy application tests vì đây là task authoring tài liệu và API #52 chưa có implementation.

## Deliverable manifest

| File | Vai trò | Trạng thái |
|---|---|---|
| `00_Cover.md` | Cover | PASS |
| `01_Lich_su.md` | Lịch sử | PASS |
| `02_Overview.md` | Overview | PASS |
| `03_Request.md` | Request và proposal | PASS |
| `04_Response.md` | Content response | PASS |
| `05_Data_Mapping.md` | Flow/query/mutation/response matrices | PASS |
| `06_Error.md` | Error cases | PASS |
| `07_table.md` | Logical publication mapping | PASS |
| `PLAN_RESULT.md` | Plan and pre-authoring matrices | PASS |
| `OPEN_QUESTIONS.md` | Contract/schema/lifecycle questions | PASS |
| `VERIFICATION_REPORT.md` | Verification record | PASS |

## Template fingerprints

SHA256 của 8 template nguồn trong registry:

| Template | SHA256 |
|---|---|
| `00_Cover.md` | `fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63` |
| `01_Lich_su.md` | `d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e` |
| `02_Overview.md` | `c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6` |
| `03_Request.md` | `37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa` |
| `04_Response.md` | `5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8` |
| `05_Data_Mapping.md` | `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b` |
| `06_Error.md` | `e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b` |
| `07_table.md` | `4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356` |

All eight sheet appendices byte-match their registered template appendix. Front matter uses `dd_id: "52"` and `Draft — Needs Confirmation`.

## Contract and source checks

| Check | Result | Evidence |
|---|---|---|
| Catalog contract | Method/path/auth/path/response/200 and exact five error codes retained | PASS — catalog row #52 |
| Request direction | Catalog and AC-22 declare path only; proposed `published:boolean!` is separately labeled DERIVED | PASS — discrepancy explicit |
| AC-22 sequence | PATCH → UPDATE publication status → reload tree | PASS — diagram nodes/edges |
| AC-33 relation | PENDING_REVIEW queue and APPROVED/PUBLISHED approval text recorded; ambiguity remains open | PASS — diagram nodes/edges |
| Content response | All eight reusable Content fields are covered; no `is_published` or version field added | PASS — response/mapping matrices |
| Current route/module/test | No #52 method/path, `api_52` module or test reference found under Study app/tests source | PASS — static source search |
| Middleware/error helper | Future path is absent from `DESIGN_CONTRACT_PATHS`; missing error data currently serializes as `{}` | PASS — current source; integration discrepancy recorded |
| Schema | Legacy DDL has no generic Content/version relation; pilot `content_blocks` is UUID/lesson-bound and not substituted | PASS — DDL evidence; live schema remains unverified |

## Document integrity checks

- Exact manifest: 8 sheets + 3 reports = 11 files.
- Eight appendix tails match the registered Markdown template byte-for-byte.
- Catalog error set matches 401/403/404/422/500 with exact `DESIGN_*` codes; success remains 200 `DESIGN_RESOURCE_UPDATED`.
- All 8 Content response fields are listed individually; request body and state machine are labeled as proposals.
- Both JSON examples parse. Relative Markdown links resolve. Markdown table column counts, code fences and trailing whitespace pass static checks.
- `git diff --check` returned no diagnostics; a separate check covered untracked DD files.
- API inventory after authoring: 103 catalog endpoint IDs, 52 DD folders with all eight core sheets, 51 IDs without DD (#53–#103). 40 folders have all three reports; #01–#12 still lack those reports.
- Programming inventory: 12/103 catalog IDs have a matching router method/path and module `view.py`; 91 do not. #08/#09 source is present but runtime behavior was not verified after merge.
- Application tests were not run. These checks establish document/source consistency only, not endpoint runtime or live database readiness.

## Cross-API review and remaining scope

- #50 ↔ #52: initial `PENDING_REVIEW` proposal and readiness gate are recorded; status eligibility is still DERIVED.
- #51 ↔ #52: content version update and publication-status update are documented as separate logical operations; current revision selection remains unresolved.
- AC-22/AC-33 macro-review of #49–#53 is complete with open questions. Resolve whether Admin approval sets APPROVED only or publishes, and align tree visibility, creation, revision, publication and deletion; see the section below.
- No application tests were run; no claim is made about live schema, migration, or API readiness.

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

