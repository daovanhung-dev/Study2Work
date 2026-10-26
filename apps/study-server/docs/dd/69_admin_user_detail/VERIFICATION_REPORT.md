# Báo cáo kiểm chứng — API #69

- DD status: Draft — Needs Confirmation.
- Endpoint: `GET /api/v1/admin/users/{user_id}`.
- Runtime status: route, module và focused HTTP tests có trong Study source; legacy user table, mapping quyền Admin và live deployment chưa xác minh.
- Direct contract: `ApiEnvelope<UserProfile>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; direct errors đúng 401/403/404/500.
- Local fallback: shared JWT role `ADMIN`; đọc candidate legacy BIGINT `users`; malformed/out-of-range ID và không có row đều trả 404; bio bị omit, avatar/phone nullable được giữ null.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Coding worklog preflight | Selector tìm thấy 62 coding worklogs; đã chọn và đọc #34/#47/#48, cùng worklog implementation #68 và DD #69. | PASS |
| Plan trước code | Source trace, discrepancies và implementation plan được ghi trước khi sửa runtime. | PASS |
| Contract/source trace | Catalog, AC-31, #68–#72 boundary, API #04 profile, API #48 path fallback, auth, middleware và DDL đã đối chiếu. | PASS — SOURCE REVIEW |
| Focused API #69 suite | 13 TestClient tests passed; một cảnh báo deprecation Starlette/httpx hiện hữu. | PASS |
| Full Study suite | `751 passed, 1 warning in 31.37s`. | PASS |
| Ruff | `./.venv/bin/ruff check app tests` — all checks passed. | PASS |
| OpenAPI | 39 `/api/v1` path templates, 40 operations; #69 có required int64 `user_id`, required Authorization và đúng 200/401/403/404/500. | PASS |
| DD package | 8 sheets và 3 reports; appendix Excel của 8 sheets được giữ nguyên byte-for-byte so với `HEAD`. | PASS — STATIC |
| DD Markdown/JSON/links | Relative links resolve; ví dụ JSON parse; fenced blocks cân bằng; không có trailing whitespace. | PASS — STATIC |
| AC-31 macro-review | Rà trạng thái hiện tại #68–#72; #68–#71 có route/module/focused HTTP tests local; #72 delete đã được wire và có focused HTTP tests, dùng status marker DERIVED. Boundaries và câu hỏi schema/policy vẫn được giữ. | PASS — DOCUMENT REVIEW |
| Context pages/manifest | Cập nhật route/runtime/security/database/architecture/module/test/source-status; 6 source paths mới có trong manifest và đều tồn tại. | PASS — STATIC |
| Context validator `--skip-drift` | Study paths không có lỗi; validator vẫn báo thiếu context/source và links của DB Admin ngoài scope. | PARTIAL — BASELINE |
| Context validator mặc định | Cùng lỗi DB Admin và thêm `CONTEXT_STALE` do worktree changes hiện có; không thay snapshot commit để che drift. | PARTIAL — BASELINE |
| `git diff --check` | Không có diagnostics. | PASS |

## AC-31 group macro-review

Status: `VERIFIED_WITH_OPEN_QUESTIONS` — document-level review of APIs #68–#72.

- #68 list trả `ApiEnvelope<Page<UserProfile>>`; #69 đọc một `UserProfile`. Hai API có runtime route/module/focused HTTP tests local.
- #69 dùng profile allowlist của API #04, bỏ `bio` chưa có nguồn mapping và không đọc credential. Enum/null policy, PII access, audit và lifecycle visibility vẫn cần chủ sở hữu xác nhận.
- #70 sở hữu profile/role update; #71 sở hữu trạng thái account; #72 sở hữu ý định delete/anonymize. Các mutation không nằm trong handler #69.
- #72 hiện dùng `status=DELETED`, response timestamp alias từ `updated_at`, giữ dependent rows và trả 404 khi lặp; các lựa chọn này DERIVED, chưa có owner approval hoặc live schema evidence.
- Legacy user-linked relations chỉ là DDL context; không suy luận cascade hoặc hard-delete.
- Test dùng fake DB sessions. APIs #68–#72 có local route/OpenAPI/test evidence; điều đó không xác nhận live schema, migration deployment, policy Admin, hoặc hành vi PII/lifecycle ngoài ứng dụng.

## Open status

Các câu hỏi về live schema, quyền Admin riêng/tenant/MFA, bio và enum/null policy, PII/audit, visibility sau #71/#72 và deployment còn trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md). DD giữ trạng thái `Draft — Needs Confirmation`.
