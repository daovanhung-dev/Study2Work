# Báo cáo kiểm chứng — API #86

## Phạm vi

- Implement API #86 và đồng bộ tombstone visibility với các reader/writer trực tiếp.
- Không sửa catalog hoặc diagram; không thêm schema migration.
- Kiểm chứng source bằng HTTP tests với fake DB session; live database không được kết nối.
- Không tạo ZIP theo workflow của server-study.

## Checks

| Check | Result | Status |
|---|---|---|
| Catalog và AC-34 contract | DELETE path, Admin/Bearer, path ID, no body/query, DeleteResult, 200 và exact error set preserved. | Static pass |
| DeleteResult | id:int64 and literal `deleted`; DB-returned legacy `updated_at` maps to `deleted_at` by API #77 precedent. | DERIVED local mapping; live metadata unverified |
| Current source | DELETE route/module and shared ADMIN guard are wired; errors, int64 path, transaction and OpenAPI have local HTTP tests. | Source-backed locally |
| Schema/dependencies | Legacy BIGINT marker `status='DELETED'`; checks progress/resources/lesson_uploads; V1-PILOT UUID model stays separate. | DERIVED local mapping; live schema/FKs unverified |
| Exact package | 8 registered template sheets + 3 reports (11 files). | PASS |
| Appendix parity | All eight appendix suffixes byte-match the registered template; each appendix heading starts a line. | 8/8 PASS |
| Contract/JSON | Catalog success/error codes and all DeleteResult fields retained; 3 JSON blocks parse. | PASS |
| Markdown tables/fences/links/whitespace | Across all 11 files: 33 tables / 377 data rows have consistent widths; 18 fence markers balance; 36 local links and anchors resolve; no trailing whitespace. | PASS — STATIC |
| OpenAPI | 50 `/api/v1` route templates / 57 operations; DELETE shares `/admin/lessons/{lesson_id}`, documents int64 path, no body, and 401/403/404/422/500. | PASS |
| Ruff | `.venv/bin/ruff check app tests` | PASS |
| Fingerprints | Template pack and output payload SHA-256 are recorded below. | PASS |
| `git diff --check` | No diagnostics. | PASS |
| Application tests | API #86 focused: 15; linked #09/#12/#47/#48/#77/#82–#86: 180; full Study suite: 1093 passed. | PASS — fake DB sessions |
| Context validator | Deno validator reports missing DB Admin context/source paths and unavailable baseline commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`; no API #86/server-study missing-path finding. | PARTIAL — unrelated baseline |

## Fingerprints

| Fingerprint | Scope | SHA-256 |
|---|---|---|
| Registered template pack | Eight sorted template names + NUL + raw bytes + NUL | `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137` |
| DD output payload | Eight sheets, `OPEN_QUESTIONS.md`, and `PLAN_RESULT.md`; verification report excluded | `eb7455b53245ec89fc35e5553ddcca2d382d372272e067e583beb58561430195` |

<a id="ac-34-macro-review"></a>

## AC-34 macro-review #82–#86

- Status: `SOURCE_BACKED_WITH_OPEN_QUESTIONS` — contract/source/runtime comparison completed for APIs #82–#86. This does not mean owner approval or live DB verification.
- Diagram trace: Admin opens lesson management; #82 lists; #83 reads selected lesson and dependencies; Admin chooses update/status/delete; #84 updates, #85 changes status plus audit, or #86 deletes by policy; each mutation returns to the lesson list through #82.

| API | Group role | Coherence finding and remaining gap |
|---|---|---|
| #82 | List and post-mutation reload | Local source returns `ApiEnvelope<Lesson[]>` as a DERIVED list fallback against catalog `ApiEnvelope<Lesson>`, exact course/status filters, and 422 for supplied `type`; tombstone rows are excluded. |
| #83 | Selected lesson detail | Returns the direct `Lesson` contract and excludes `DELETED`; #86 rechecks current progress/resource/upload references at delete time. |
| #84 | Metadata update | Candidate body contains metadata only. It excludes status (owned by #85), course reassignment, audit, and dependency mutation. Body/PUT semantics remain DERIVED. Success returns to #82 per diagram. |
| #85 | Status update and audit | AC-34 explicitly assigns `status + audit` here. Body field, enum and transitions remain unresolved; the physical audit model cannot be mapped between the legacy BIGINT Lesson and V1-PILOT UUID audit schema. Success returns to #82. |
| #86 | Conditional delete | Uses a legacy `DELETED` status tombstone and DB `updated_at` response timestamp; any `lesson_progress`, `resources`, or `lesson_uploads` row blocks with catalog 422. Repeat delete maps to 404; no child cascade or new audit. Choices remain DERIVED pending owner approval/live DB verification. Success returns to #82. |

### Shared discrepancies and limits

- Keep the list/cardinality mismatch, #83 dependency output, #84 request body, #85 status/audit choices and #86 delete policy marked DERIVED/Draft; do not turn them into owner-approved contract.
- Legacy BIGINT `lessons` references progress/resources/uploads and has no dedicated deletion timestamp. V1-PILOT uses separate UUID lessons and restrictive child references; neither artifact proves live schema.
- APIs #82–#86 are locally wired with shared ADMIN role auth, the existing path template allowlist, and tested `data:null` errors. Fine-grained AC-34 permission remains unsupported.
- Fake-session HTTP tests prove local orchestration only; they do not prove SQL execution against the deployed schema, migration state, FK locks, owner approval or live behavior.

## Limits

Local source and fake-session tests do not establish deployed schema/migration state, FK lock behavior, dedicated permission, owner approval, or live API behavior.
