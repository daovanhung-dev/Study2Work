# VERIFICATION_REPORT — Study API #60

## Kết quả

- DD status: `Draft — Needs Confirmation`; local fallback behavior is documented as `DERIVED`.
- Runtime: `SOURCE_BACKED` for the checked-in route/module and passing fake-DB TestClient coverage.
- API contract remains #60's POST route, required request fields, HTTP 200 `DESIGN_RESOURCE_UPDATED`, singleton `SupportRequest`, and catalog errors 401/403/404/422/500.
- No support migration, live database, API catalog, AC diagram, API #35/#47 contract, or API #61 source was changed by this task.

## Deliverable manifest

| Nhóm | File |
|---|---|
| Sheets | `00_Cover.md`, `01_Lich_su.md`, `02_Overview.md`, `03_Request.md`, `04_Response.md`, `05_Data_Mapping.md`, `06_Error.md`, `07_support_messages_insert.md`, `08_support_message_uploads_insert.md` |
| Reports | `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` |
| Tổng | 12 Markdown files; no ZIP per Study workflow. |

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Focused API #59/#60 tests | 34 passed; includes 13 API #59 regressions and 21 API #60 cases. | PASS |
| Full Study suite | 584 passed; one upstream Starlette/httpx TestClient deprecation warning. | PASS |
| Ruff | Changed runtime modules, route/middleware and API #60 tests pass `ruff check`. | PASS |
| OpenAPI | 30 `/api/v1` path templates and 31 operations; #60 path is present with `request_id` integer/int64 and required strict body fields. | PASS |
| DD structure | 12 Markdown files; 9 sheets have API #60 front matter and `Draft — Needs Confirmation`. | PASS |
| Template appendix | The seven base sheets and both split table mappings preserve exact source-template appendix bytes. | PASS |
| DD examples/links | JSON examples parse; all relative file targets exist. | PASS |
| Context manifest | All API #60 and shared projection source paths registered for server-study exist. | PASS |
| `git diff --check` | No whitespace errors. | PASS |
| Context validator | Deno validator reports missing DB Admin context/source paths and broad existing source drift in the dirty workspace; `--skip-drift` leaves only DB Admin failures outside this task. | BASELINE_FAILURE_OUT_OF_SCOPE |

## Runtime verification boundary

TestClient uses fake DB rows. These results verify route wiring, validation, owner/error mapping, transaction calls, response mapping and rollback branches; they do not verify PostgreSQL schema/application, migration 008 deployment, live concurrency, deployed authorization or Object Storage URL reachability.

## Open business decisions

- Confirm the local support BIGINT schema, direct course-owner policy, and `attachment_refs` JSON-array wire representation.
- Confirm nonblank/length rules, thread size limits, and replies after RESOLVED/CANCELLED.
- Complete AC-24 macro-review across APIs #58–#61 after API #61 implementation.

See [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md), [PLAN_RESULT.md](./PLAN_RESULT.md), and [API #59 DD](../59_mentor_support_request_detail/02_Overview.md).
