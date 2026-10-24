# Verification Report — API #49 Lấy cây nội dung course

## Phạm vi

Kiểm tra tĩnh bộ DD Markdown API #49, catalog/AC-22, legacy và pilot schema boundary, route/module/test presence và template compliance. Không thay đổi Study runtime, DB schema, catalog hoặc diagram. Không chạy application tests.

## Deliverable manifest

| File | Vai trò | Trạng thái |
|---|---|---|
| `00_Cover.md` | Cover | PASS |
| `01_Lich_su.md` | Lịch sử | PASS |
| `02_Overview.md` | Overview | PASS |
| `03_Request.md` | Request | PASS |
| `04_Response.md` | Response | PASS |
| `05_Data_Mapping.md` | Flow và ma trận | PASS |
| `06_Error.md` | Error cases | PASS |
| `07_table.md` | Read-only mapping/N/A mutation | PASS |
| `PLAN_RESULT.md` | Plan và pre-authoring matrices | PASS |
| `OPEN_QUESTIONS.md` | Gaps/blockers | PASS |
| `VERIFICATION_REPORT.md` | Verification record | PASS |

## Contract/source checks

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector `docs` chọn #48, #41, #42; cả ba đã được đọc. | VERIFIED |
| API catalog #49 | GET/path/auth/response/status/exact errors match the row; no body/query. | PASS |
| AC-22 diagram | Parsed page AC22 nodes/edges: GET → read sections/lessons/content → CRUD/publish branch. | PASS |
| Current Study source | No #49 route/module/test; middleware allowlist excludes path #49, so future validation/unhandled fallback differs from catalog unless wired explicitly. | VERIFIED_WITH_DISCREPANCY |
| Schema boundary | Legacy ERD lacks generic Content; pilot hierarchy is UUID/versioned and separate; live DB unknown. | PASS_WITH_OPEN_QUESTIONS |
| Response mapping | All 8 Content fields listed; unresolved fields remain SOURCE_REQUIRED. | PASS_WITH_SOURCE_REQUIRED |
| Static Markdown validation | 11 files; 8 front matters and template appendix suffixes match; JSON parses; local links, table widths, fences and whitespace pass; exact catalog/error set and field coverage pass. | PASS |
| Error helper | Read current `responses.py` and `middleware.py`: default error data is `{}`; path #49 is outside contract allowlist; generic validation/internal fallbacks are conditional future behavior. | VERIFIED_STATIC_ONLY |
| Runtime tests | Not run; docs-only, API #49 unwired. | NOT_RUN |
| AC-22/AC-33 macro review #49–#53 | Linked DDs #49–#53 reconciled; open questions retained. | VERIFIED_WITH_OPEN_QUESTIONS |

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

