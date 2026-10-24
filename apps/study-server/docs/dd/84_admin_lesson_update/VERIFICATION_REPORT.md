# Báo cáo kiểm chứng — API #84

## Phạm vi

- Kiểm chứng tĩnh nội dung Markdown API #84.
- Không đổi source code, schema, catalog hoặc diagram.
- Không chạy application tests; route/module/test API #84 hiện không tồn tại.

## Template fingerprint

SHA-256 baseline của bộ template registry createDD-markdown:

| File | SHA-256 |
|---|---|
| 00_Cover.md | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md | c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6 |
| 03_Request.md | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md | 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b |
| 06_Error.md | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

## Checks

| Check | Result | Status |
|---|---|---|
| Catalog and AC-34 contract | PUT path, Admin/Bearer, path ID, Lesson envelope, 200 and exact success/error set preserved; body absent in both sources. | Static pass |
| Current source | No Admin lesson route/view/test; Admin guard absent; middleware allowlist excludes path. | Static pass; runtime not verified |
| Schema mapping | Legacy BIGINT and V1-PILOT UUID/versioned kept distinct; live schema unverified. | Static pass with open questions |
| Exact package | 8 template sheets + PLAN_RESULT, OPEN_QUESTIONS, VERIFICATION_REPORT (11 files total). | Pass |
| Appendix parity | All 8 sheet appendices byte-match their registered template suffixes. | 8/8 pass |
| Contract/JSON | Catalog success code plus all five error codes match; four JSON examples parse. | Pass |
| Markdown tables/fences/links/whitespace | Across all 11 files: 34 tables / 401 data rows have consistent widths, 14 fences balance, 38 local links/anchors resolve, no trailing whitespace. | PASS |
| `git diff --check` | No diagnostics. | Pass |
| Application tests | Not run; documentation task. | Not run |
| Context validator | No context page/registry change planned. | Not applicable |

## Limits

Static documentation checks do not establish API implementation, SQL executability, live-schema compatibility, or approval of the Admin policy/body proposal.

## AC-34 macro-review

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`; document-level review only, not owner approval or runtime verification.
- API #84 remains a metadata update proposal; status/audit belong to #85 and delete/reference policy belongs to #86. AC-34 reloads through #82 after success, whose response cardinality and `type` filter remain unresolved.
- See the [consolidated review matrix](../86_admin_lesson_delete/VERIFICATION_REPORT.md#ac-34-macro-review).
