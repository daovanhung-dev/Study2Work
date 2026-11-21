# VERIFICATION_REPORT — Study API #62

## Kết quả

- API #62 đã được wire cục bộ: `GET /api/v1/mentor/courses/{course_id}/students`.
- Response hiện là `ApiEnvelope<UserSummary[]>`; catalog và node AC-25 đã đồng bộ, không có pagination input/output.
- DD vẫn `Draft — Needs Confirmation` vì response/schema/owner policy là fallback DERIVED; API #63 recipient-string encoding vẫn mở.
- Implementation chỉ đọc legacy BIGINT `courses`, `enrollments`, `users`; không thêm bảng/migration, không commit và không gọi dịch vụ ngoài.
- Live DB schema, migration state, service deployment và API #63 integration chưa được xác minh.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| API #62 TestClient | 18 passed; bao gồm auth/role, signed-int64 path, 404/403 scope, active Student roster, empty result, projection/query errors, trace và OpenAPI. | PASS; 1 upstream Starlette/httpx deprecation warning |
| Linked API regression | API #49 và #54: 32 passed. | PASS; 1 upstream Starlette/httpx deprecation warning |
| Full Study suite | `uv run pytest -q`: 615 passed. | PASS; 1 upstream Starlette/httpx deprecation warning |
| Ruff | `uv run ruff check app tests`: all checks passed. | PASS |
| OpenAPI/import | 32 unique `/api/v1` paths, 33 operations; #62 exposes int64 path and array response model. | PASS |
| DD static checks | 11 Markdown files; 8 sheet front matters/source appendices; JSON examples parse; local links resolve. | PASS |
| Diagram | AC-03 Draw.io XML parses; AC-25 #62 output is `ApiEnvelope<UserSummary[]>`. | PASS |
| Whitespace | `git diff --check`. | PASS |
| Context validator | Full validator reports missing DB Admin context/source plus broad tracked-source drift in the shared dirty worktree. `--skip-drift` leaves only the unrelated DB Admin gaps; no Study Server page/reference error was reported. | FAILED — repository baseline/out of scope |
| Live database/deployment | Not accessed. | NOT_VERIFIED_HERE |

## Quyết định còn cần owner xác nhận

- Chấp thuận `UserSummary[]` không phân trang thay cho contract ban đầu `Page<Course>`.
- Xác nhận runtime schema là legacy BIGINT và active enrollment chỉ là `status='ACTIVE'`.
- Xác nhận direct `courses.mentor_id` ownership là đủ; assigned Mentor chưa được cấp quyền.
- Chốt cách API #63 serialize `recipients:string!` từ numeric user IDs.

Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md), [PLAN_RESULT.md](./PLAN_RESULT.md) và [worklog](../../../../../.agents/worklog/2026-10-25/implement-api62.md).
