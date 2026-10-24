# Báo cáo kiểm chứng — API #86

## Phạm vi

- Kiểm chứng tĩnh nội dung Markdown API #86.
- Không sửa source code, schema, catalog hoặc diagram.
- Không chạy application tests; route/module/test API #86 hiện không tồn tại.
- Không tạo ZIP theo workflow của server-study.

## Checks

| Check | Result | Status |
|---|---|---|
| Catalog và AC-34 contract | DELETE path, Admin/Bearer, path ID, no body/query, DeleteResult, 200 và exact error set preserved. | Static pass |
| DeleteResult | id:int64, status literal deleted, deleted_at:date-time listed as required; timestamp mapping SOURCE_REQUIRED. | Static pass with open question |
| Current source | No Admin lesson route/module/test; Student-only guard; design-code allowlist excludes endpoint; live schema unverified. | Static pass; runtime not verified |
| Schema/dependencies | Legacy BIGINT references and V1-PILOT UUID restrictive relations kept separate; no delete marker or SQL invented. | Static pass |
| Exact package | 8 registered template sheets + 3 reports (11 files). | PASS |
| Appendix parity | All eight appendix suffixes byte-match the registered template; each appendix heading starts a line. | 8/8 PASS |
| Contract/JSON | Catalog success/error codes and all DeleteResult fields retained; 3 JSON blocks parse. | PASS |
| Markdown tables/fences/links/whitespace | Across all 11 files: 33 tables / 373 data rows have consistent widths; 16 fences balance; 36 local links and anchors resolve; no trailing whitespace. | PASS — STATIC |
| Fingerprints | Template pack and output payload SHA-256 are recorded below. | PASS |
| `git diff --check` | No diagnostics. | PASS |
| Application tests | Not run; docs task and endpoint unwired. | Not run |
| Context validator | No context page/registry change planned. | Not applicable |

## Fingerprints

| Fingerprint | Scope | SHA-256 |
|---|---|---|
| Registered template pack | Eight sorted template names + NUL + raw bytes + NUL | `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137` |
| DD output payload | Eight sheets, `OPEN_QUESTIONS.md`, and `PLAN_RESULT.md`; verification report excluded | `5ef471a04f122cdb32abe0e3edd67f0141079089ec69026ad91196a87010948f` |

<a id="ac-34-macro-review"></a>

## AC-34 macro-review #82–#86

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` — document-level comparison completed after all five DD folders were present. This does not mean owner approval or runtime verification.
- Diagram trace: Admin opens lesson management; #82 lists; #83 reads selected lesson and dependencies; Admin chooses update/status/delete; #84 updates, #85 changes status plus audit, or #86 deletes by policy; each mutation returns to the lesson list through #82.

| API | Group role | Coherence finding and remaining gap |
|---|---|---|
| #82 | List and post-mutation reload | Direct catalog response remains `ApiEnvelope<Lesson>` despite list intent. `type` has no source-backed Lesson field. After #86, deleted-item visibility cannot be filtered until marker and policy are selected. |
| #83 | Selected lesson detail | Returns the direct `Lesson` contract. AC-34 says “lesson + dependencies” but does not define dependency output; #86 rechecks current references/progress at delete time rather than relying on a stale detail read. |
| #84 | Metadata update | Candidate body contains metadata only. It excludes status (owned by #85), course reassignment, audit, and dependency mutation. Body/PUT semantics remain DERIVED. Success returns to #82 per diagram. |
| #85 | Status update and audit | AC-34 explicitly assigns `status + audit` here. Body field, enum and transitions remain unresolved; the physical audit model cannot be mapped between the legacy BIGINT Lesson and V1-PILOT UUID audit schema. Success returns to #82. |
| #86 | Conditional delete | Catalog requests progress/reference checks; legacy `resources` and `lesson_progress` are candidate relations. Soft-delete and 422 blocker are DERIVED proposals; exact references, physical marker, persisted `deleted_at`, repeated-delete behavior and visibility remain open. No cascade or audit is added. Success returns to #82. |

### Shared discrepancies and limits

- Keep the list/cardinality mismatch, #83 dependency output, #84 request body, #85 status transition/audit persistence, and #86 delete policy open; do not turn proposals into approved contract.
- Legacy BIGINT `lessons` references `resources.lesson_id` and `lesson_progress.lesson_id` and has no deletion marker. V1-PILOT uses UUID lessons, restrictive child references, and UUID audit events; these artifacts are distinct and neither proves the live schema.
- The checked-in source has no #82–#86 route/module/test; Admin authorization is absent, the middleware contract allowlist excludes these paths, and current error helper emits `data:{}` when the API guideline expects `data:null`.
- Static package, contract and document-level macro checks do not prove SQL executability, live-schema compatibility, implementation, owner approval, or runtime behavior.

## Limits

Static documentation checks do not establish API implementation, executable delete SQL, live-schema compatibility, approval of the dependency policy, persisted deleted_at mapping, or runtime error behavior.
