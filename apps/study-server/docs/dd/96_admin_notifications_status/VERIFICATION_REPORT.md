# VERIFICATION_REPORT — Study API #96 Admin notification status

## Phạm vi

Kiểm tra tĩnh DD Markdown #96, direct catalog contract, AC-36 status path, response/source coverage, template appendix, links và source route absence. Không sửa runtime, DB schema, catalog hoặc diagram; không chạy application tests.

## Deliverable manifest

| File | Vai trò |
|---|---|
| `00_Cover.md` | Cover |
| `01_Lich_su.md` | Lịch sử |
| `02_Overview.md` | Overview |
| `03_Request.md` | Request |
| `04_Response.md` | Response |
| `05_Data_Mapping.md` | Data mapping |
| `06_Error.md` | Error |
| `07_table.md` | N/A — read-only |
| `PLAN_RESULT.md` | Plan and sources |
| `OPEN_QUESTIONS.md` | Gaps and decisions |
| `VERIFICATION_REPORT.md` | Static result |
| `AC-36_MACRO_REVIEW.md` | Cross-API document review #92–#96 |

## Static checks

| Check | Result | Status |
|---|---|---|
| Package manifest | 12 Markdown files: eight template sheet roles, three standard reports, and one AC-36 macro-review report | PASS — STATIC |
| Direct contract | Catalog row #96 matches GET/path/Admin Bearer/no body-query/`ApiEnvelope<Notification>`/200 and exact 401/403/404/500 set | PASS — STATIC |
| AC-36 flow | Diagram #96 → “Đọc delivery aggregate” → “Reload notification management” recorded; response mismatch retained | PASS — STATIC |
| Response coverage | All eight `Notification` fields plus envelope fields listed; no delivery counts or per-channel fields appended | PASS — STATIC |
| Template appendix | All eight sheet appendix suffixes match the verified #49 template-backed suffixes | PASS — STATIC |
| Markdown checks | 31 table blocks consistent; 2/2 JSON examples parse; code fences balanced; 20 local link targets resolve; no trailing whitespace; final newline present | PASS — STATIC |
| Source scan | No #96 route in Study router; catalog/router/matching-view intersection is 12/103 (#01–#09, #12–#14); 91 lack the source pair | PASS — STATIC |
| Runtime boundary | #08/#09 remain unverified after merge per scope context; #02 uses a dispatch stub. Source count is not a runtime-pass count. | SOURCE-ONLY |
| Application tests | Not run; documentation task | NOT_RUN |
| Runtime/deployment/live DB | Not checked | NOT_CHECKED |
| AC-36 macro-review | #92–#96 cross-review completed with unresolved owner decisions | VERIFIED_WITH_OPEN_QUESTIONS |

## Preserved discrepancies

- AC-36 aggregate-read intent has no direct response fields/source mapping in `Notification`.
- Legacy BIGINT row and V1-PILOT UUID learner/delivery schema are not approved Admin persistence.
- Admin permission, enum members, aggregate grain and #93 Operation bridge remain open.

## Kết quả

DD #96 remains `Draft — Needs Confirmation`. Static document checks passed. The linked AC-36 macro-review records the shared questions; it does not claim endpoint implementation, live schema or runtime acceptance.
