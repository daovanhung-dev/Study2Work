# Verification Report — API #50 Tạo nội dung mới

## Phạm vi

Kiểm tra tĩnh bộ DD Markdown API #50, catalog/AC-22/AC-33, schema boundary, route/helper wiring và template appendix. Chỉ thay đổi tài liệu trong `apps/study-server/docs/dd/50_mentor_content_create/` cùng worklog task. Không sửa runtime, DB, catalog, diagram hoặc client. Không chạy application tests vì task docs-only và endpoint chưa có implementation.

## Deliverable manifest

| File | Vai trò | Trạng thái |
|---|---|---|
| `00_Cover.md` | Cover | PASS |
| `01_Lich_su.md` | Lịch sử | PASS |
| `02_Overview.md` | Overview | PASS |
| `03_Request.md` | Request + request usage | PASS |
| `04_Response.md` | Response + Content projection | PASS |
| `05_Data_Mapping.md` | Query, logical mutation, mapping matrices | PASS |
| `06_Error.md` | Exact catalog errors | PASS |
| `07_table.md` | Logical insert mapping / physical gap | PASS |
| `PLAN_RESULT.md` | Plan and pre-authoring matrices | PASS |
| `OPEN_QUESTIONS.md` | Source/approval gaps | PASS |
| `VERIFICATION_REPORT.md` | Verification record | PASS |

## Contract and source checks

| Check | Result | Evidence level |
|---|---|---|
| API #50 request and response contract | Method/path, four required body fields, HTTP 201 and `DESIGN_RESOURCE_CREATED`, `ApiEnvelope<Content>` match catalog row #50 | PASS — DIRECT catalog |
| Error set | Exactly 401/403/422/500 and matching `DESIGN_*` codes; no 404 added | PASS — DIRECT catalog |
| Content response coverage | All eight fields `id`, `course_id`, `content_type`, `title`, `payload`, `status`, `parent_id`, `order` are mapped or explicitly marked unresolved/derived | PASS — static matrix check |
| AC-22 flow | POST → logical `INSERT Content` → reload tree recorded; no physical SQL invented | PASS — diagram |
| AC-33 state | Queue condition `status=PENDING_REVIEW` recorded; initial POST state labeled `DERIVED` and requires confirmation | PASS — diagram + evidence classification |
| Physical schema | Legacy generic Content relation absent; pilot `content_blocks` differs from BIGINT Content contract; no live schema claim | PASS — DDL/design artifact comparison |
| Runtime route/module/test | No API #50 route/module/test was found; endpoint remains `UNWIRED` / `NOT_FOUND` | PASS — current-source scan |
| Middleware error integration | `DESIGN_CONTRACT_PATHS` excludes `/api/v1/mentor/content`; generic validation/unhandled fallbacks use non-catalog codes unless route is added | PASS — current helper; conditional future discrepancy |

## Document integrity checks

- 8 main sheet front matters use `dd_id: "50"` and `Draft — Needs Confirmation`.
- All 8 template appendix tails byte-match the corresponding API #49/template appendix.
- Request matrix covers Authorization and all four body fields; response matrix covers the complete catalog Content shape and envelope.
- The request and response JSON examples parse syntactically; the request enum member is explicitly a non-executable placeholder.
- Markdown code fences are balanced; no trailing whitespace in new DD files.
- `git diff --check` returned no diagnostics for tracked changes. A separate static script checked whitespace in the untracked API #50 files.
- Exact 11-file set was confirmed after report creation.

## Limitations and handoff

- These checks verify document consistency only. They do not prove runtime behavior, DB migration, live schema, or API readiness.
- Initial `PENDING_REVIEW`, root `parent_id=null`, and next-sibling order are design proposals requiring confirmation; physical Content persistence, payload/enum contracts, Mentor identity/assignment, missing-course error mapping and ID allocation remain open.
- No application tests were run. Full AC-22/AC-33 macro-review of #49–#53 is complete with open questions; see the section below.

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

