# Kết quả plan — API #74

- Trạng thái DD: `Draft — Needs Confirmation`; runtime implementation is local source, not product approval.
- Folder: `74_admin_course_detail/`.
- Contract: `GET /api/v1/admin/courses/{course_id}`, Bearer JWT, `ApiEnvelope<Page<Course>>`, success 200, errors 401/403/404/500 theo catalog.
- Source ordering reviewed: AC-32 activity diagram → legacy/V1-PILOT schema artifacts → API catalog/reusable schemas; checked-in sources conflict or omit permission, counter and live-schema decisions.
- Local auth fallback: shared JWT role `ADMIN`; dedicated course-management permission is not independently enforced because no policy source exists.
- Local query fallback: bound read of legacy BIGINT `courses LEFT JOIN users`, without status filter; no category/counter join. Live schema is not verified.
- Local response fallback: one `Course` inside `Page<Course>` with metadata 1/1/1/1; malformed/out-of-int64 path maps to 404. Incomplete required projection and query errors map to safe 500 with rollback.
- Middleware registers the dynamic route template and matches FastAPI route templates; `error_response` emits `data:null`.
- No schema, catalog, diagram or business-code changes were made for this API.
- Verification: focused #74 tests 15 passed; linked #06/#08/#69/#73/#74 set 80 passed; full Study suite 845 passed; Ruff passed; OpenAPI declares the route. Fake DB tests do not verify live schema/deployment.
- Remaining owner questions: dedicated permission, AC-32 counters, legacy-vs-pilot/live schema, category relation, null/orphan policy and CourseStatus casing.

See [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md) for commands and boundaries.
