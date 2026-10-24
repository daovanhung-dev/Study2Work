# Verification Report — API #47 Tạo lecture

## Phạm vi

Kiểm tra tĩnh bộ DD Markdown cho API #47, contract catalog, flow AC-21, mapping candidate và các liên kết. Không xác minh runtime/API vì endpoint chưa có source.

## Deliverable manifest

| File | Vai trò | Trạng thái |
|---|---|---|
| 00_Cover.md | Cover | PASS |
| 01_Lich_su.md | Lịch sử | PASS |
| 02_Overview.md | Overview | PASS |
| 03_Request.md | Request | PASS |
| 04_Response.md | Response | PASS |
| 05_Data_Mapping.md | Flow và ma trận | PASS |
| 06_Error.md | Error cases | PASS |
| 07_lessons_insert.md | Mapping INSERT lessons | PASS |
| PLAN_RESULT.md | Plan, source coverage và pre-authoring matrices | PASS |
| OPEN_QUESTIONS.md | Gaps/blockers | PASS |
| VERIFICATION_REPORT.md | Verification record | PASS |

## Contract/source checks

| Check | Expected evidence | Result |
|---|---|---|
| API contract | Method/path/actor/request/response/201 and exact 401/403/404/422/500 catalog errors | PASS — exact catalog row and error set retained |
| AC-21 | #46 → #34 → Object Storage → #47 → #48 sequence | PASS — source diagram flow recorded |
| AC-22 boundary | Content workflow remains separate from Lecture | PASS — separate workflow and ambiguity documented |
| Schema boundary | Legacy lessons candidate not combined with V1-PILOT UUID model | PASS — both artifacts distinguished; live schema unverified |
| Query/mutation/response matrices | Every field accounted for; unresolved assets/content marked | PASS — unresolved mappings remain SOURCE_REQUIRED |
| DB mapping | Each changed physical column has one row and M1 references this file | PASS — legacy lessons columns individually mapped |
| Template/links/examples | Appendices/front matter/headings/JSON/relative links valid | PASS — final static validation passed, including exact template appendix suffixes |
| Current source | #47 has no wired route/module/test source | PASS — status recorded as UNWIRED / NOT_FOUND |
| AC-21 macro review #46–#48 | Reviewed ownership, DRAFT/read-after-create, schema split, Lecture projection, assets and envelope consistency after #48 DD creation | PASS WITH OPEN QUESTIONS — asset resolver, assignment/identity, live schema, enums and null behavior remain open |

## Template fingerprints

| Template file | SHA-256 |
|---|---|
| 00_Cover.md | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md | c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6 |
| 03_Request.md | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md | 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b |
| 06_Error.md | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

## Runtime/validation boundary

- Runtime tests: Not run; API #47 is UNWIRED / NOT_FOUND and task is documentation-only.
- assets[] is a required Lecture field with no source mapping. DD remains Draft — Needs Confirmation and is not an implementation approval.
- Study scope creates Markdown only; no ZIP is produced.
- `deno run --allow-read --allow-env scripts/validate-agent-context.mjs` remains a repository-level check; its known unrelated DB Admin/source-baseline result is recorded in the task worklog.

