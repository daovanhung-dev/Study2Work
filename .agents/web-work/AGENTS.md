# Web context router

```text
CONTEXT_STATUS: SKELETON_ONLY
scopes:
  - apps/study-client/
  - apps/work-client/web/
```

Theo yêu cầu hiện tại, context web chỉ là cấu trúc. Root package files xác nhận
Study web dùng Vue và Work web dùng React; module/routing/state/API convention
chưa được deep-analyze.

Task cụ thể chỉ đọc đúng web app:

1. `architecture.md`, `conventions.md`, `dependencies.md`.
2. `package.json`, router/entrypoint và feature files liên quan.
3. Shared API/session/UI dependency và tests trực tiếp.

Không trộn Vue pattern với React pattern.
