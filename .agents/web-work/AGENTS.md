# Web context router

```text
CONTEXT_STATUS: VERIFIED_REACT_EXPRESS_SPLIT
scopes:
  - apps/study-client/
  - apps/work-client/web/
```

Canonical page graph: `INDEX.md`.

Study web dùng Vue và có subcontext riêng tại `study/`; Work web dùng React.
Work router giữ route catalog hiện có,
`src/shared/api/work.ts` là ranh giới fetch/Zod của Work và backend tương ứng là
`apps/work-server/src/routes/api_routes.ts`.

Task cụ thể phải chọn đúng subcontext, không áp Vue pattern lên React hoặc
ngược lại:

- Study Web: `study/AGENTS.md` → `study/INDEX.md`.
- Work Web: các page trực tiếp trong scope này.

Với task authoring hoặc review DD cho Web/API, load `createDD-markdown` từ skill
registry. Đây là boundary API Detail Design, không phải Mobile module DD;
Mobile/Flutter dùng `create-dd-from-bd-mobile`. Web UI-only DD hiện chưa có
skill canonical trong repository.

Task cụ thể chỉ đọc đúng web app:

1. `../project/design.md`, `architecture.md`, `conventions.md`,
   `dependencies.md`.
2. `package.json`, router/entrypoint và feature files liên quan.
3. Shared API/auth/UI dependency và tests trực tiếp.

Không trộn Vue pattern với React pattern.

Work web dùng React Query cho server state và Zod để parse response. JWT được
lưu với key `access_token` ở localStorage; client decode payload để dựng role
guard nhưng server mới là nơi verify chữ ký. Mọi Work request chỉ gửi Bearer
header khi có token và dùng `credentials: omit`. Không dùng cookie/session,
query-string token hay Neon credential trong browser. Các screen có
loading/error/empty state và các route chưa có API chỉ hiển thị static/placeholder
UI.
