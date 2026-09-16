# Web context router

```text
CONTEXT_STATUS: VERIFIED_REACT_EXPRESS_SPLIT
scopes:
  - apps/study-client/
  - apps/work-client/web/
```

Study web dùng Vue; Work web dùng React. Work router giữ route catalog hiện có,
`src/shared/api/work.ts` là ranh giới API typed của Work và backend tương ứng là
`apps/work-server/src/routes/api_routes.ts`.

Task cụ thể chỉ đọc đúng web app:

1. `architecture.md`, `conventions.md`, `dependencies.md`.
2. `package.json`, router/entrypoint và feature files liên quan.
3. Shared API/auth/UI dependency và tests trực tiếp.

Không trộn Vue pattern với React pattern.

Work web dùng React Query cho server state và Zod để parse response. JWT được
lưu với key `access_token` ở localStorage theo contract hiện tại; mọi Work
request chỉ gửi đúng một Bearer header và dùng `credentials: omit`. Không dùng
cookie/session, query-string token hay Neon credential trong browser. Các screen
có loading/error/empty state và không tự thêm nghiệp vụ cho các route chưa có API.
