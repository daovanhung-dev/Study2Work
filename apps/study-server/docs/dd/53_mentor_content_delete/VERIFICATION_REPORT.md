# Verification Report — API #53 Xóa nội dung Mentor

## Phạm vi

Kiểm tra DD Markdown #53, exact catalog contract, AC-22/AC-33, current Study source/schema, template appendix equality, Markdown integrity và macro-review nhóm #49–#53. Đây là docs-only task; không chạy application tests và không khẳng định API runtime hoặc live schema.

## Deliverable manifest

| File | Vai trò | Trạng thái |
|---|---|---|
| 00_Cover.md | Cover | PASS |
| 01_Lich_su.md | Lịch sử | PASS |
| 02_Overview.md | Overview | PASS |
| 03_Request.md | Request | PASS |
| 04_Response.md | Response | PASS |
| 05_Data_Mapping.md | Flow/query/mutation/response mapping | PASS |
| 06_Error.md | Error | PASS |
| 07_content_soft_delete.md | Logical soft-delete mapping | PASS |
| PLAN_RESULT.md | Plan and pre-authoring matrices | PASS |
| OPEN_QUESTIONS.md | Contract/schema/lifecycle gaps | PASS |
| VERIFICATION_REPORT.md | Verification record | PASS |

## Template fingerprints

Template nguồn được đọc từ registry-wired DD_API_Template_MD. Tám appendix trong output khớp nguyên văn suffix tương ứng của template.

| Template | SHA256 |
|---|---|
| 00_Cover.md | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md | c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6 |
| 03_Request.md | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md | 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b |
| 06_Error.md | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

Output manifest SHA256 cho 10 file DD/report khác, không gồm verification report tự tham chiếu: de6c23f23c245f240fe21b4361a655e4fad722904b7373f4ce2b6bc58aae2ac7.

## Verification checks

| Check | Evidence | Result |
|---|---|---|
| Catalog contract | DELETE path, Mentor Bearer, int64 path, no body/query, ApiEnvelope<DeleteResult>, HTTP 200 and exact 401/403/404/422/500 code set match row #53. | PASS |
| AC-22 | Diagram confirms managed-course precondition, DELETE/soft delete, then tree reload. Dependency details remain proposals. | PASS |
| AC-33 | PENDING_REVIEW, APPROVED/PUBLISHED + audit and REJECTED + reason are recorded; approval/publication ambiguity is preserved. | PASS |
| Current route/source | Search under Study app/tests found no API #53 route/module/test. DESIGN_CONTRACT_PATHS also excludes the endpoint. | PASS — static source only |
| Current error behavior | Middleware uses generic validation/internal codes outside DESIGN_CONTRACT_PATHS; error_response defaults missing data to an empty object. | PASS — source read |
| Schema boundary | Legacy DB has no generic Content table. V1-PILOT content_blocks has UUID ID and lesson_id; no physical Content tombstone/SQL is invented. | PASS — live schema unverified |
| Requirement/mapping | Path input and all envelope/DeleteResult fields are individually mapped. No request body/query or extra error code was added. | PASS |
| Dependency proposal | Direct child via parent_id is DERIVED, 422 proposal; no cascade/reparent. Other dependencies and physical predicate remain open. | PASS |
| Markdown integrity | Exact 11-file manifest; all eight template appendix suffixes match; 2 JSON examples parse; relative links resolve; table widths, fences and trailing whitespace pass. | PASS |
| Diff check | git diff --check returned no diagnostics. Custom validation also covered untracked DD files. | PASS |
| AC-22/AC-33 macro-review | #49–#53 read/write/revision/review/publish/delete flow reconciled; related reports and open questions updated. | VERIFIED_WITH_OPEN_QUESTIONS |
| Application tests | Not run because this is documentation-only and API #53 is unwired. | NOT_RUN |
| Context validator | Not run; no context page or registry was changed. | NOT_APPLICABLE |

## AC-22/AC-33 Macro-review #49–#53

Status: VERIFIED_WITH_OPEN_QUESTIONS. The review findings and affected questions are recorded in this report group and each linked DD.

- #49 describes a tree but returns one Content object; active-tree shape and deleted-item filtering remain unresolved.
- #50/#51 propose PENDING_REVIEW for newly created Content/revisions; root placement and update body/version behavior remain DERIVED.
- #52 owns publication status in the proposed separation. AC-33 does not clarify whether approval alone sets APPROVED or also publishes.
- #53 proposes direct-child blocking, no cascade, unpublish-first for PUBLISHED, and history-preserving soft delete. Dependency coverage, pending-review withdrawal and storage remain open.
- Generic Content/version schema, Mentor principal/assignment, payload/enums/readiness, audit/tombstone fields and middleware integration are not source-backed.
- Application tests were not run; no runtime or live database readiness is claimed.

## Remaining questions

See [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md). DD status remains Draft — Needs Confirmation.
