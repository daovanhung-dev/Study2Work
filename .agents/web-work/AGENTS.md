# Web context router

```text
CONTEXT_STATUS: VERIFIED_WORK_WEB
scopes:
  - apps/study-client/
  - apps/work-client/web/
```

Study web dùng Vue; Work web dùng React. Work router giữ route catalog hiện có,
`DomainPage` ủy quyền cho `WorkFeaturePage`, và `src/shared/api/work.ts` là
ranh giới API typed của Work.

Task cụ thể chỉ đọc đúng web app:

1. `architecture.md`, `conventions.md`, `dependencies.md`.
2. `package.json`, router/entrypoint và feature files liên quan.
3. Shared API/session/UI dependency và tests trực tiếp.

Không trộn Vue pattern với React pattern.

Work web dùng React Query cho server state và Zod để parse response. Access
token tiếp tục ở memory theo session flow hiện tại; Work request chỉ gửi
Bearer. Mutation sinh idempotency key và gửi `If-Match` khi có version. Các
screen có loading/error/retry state và không dùng dữ liệu mock tĩnh.
