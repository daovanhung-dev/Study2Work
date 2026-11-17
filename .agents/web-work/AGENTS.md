# Web context router

```text
CONTEXT_STATUS: VERIFIED_REACT_EXPRESS_SPLIT
scopes:
  - apps/study-client/
  - apps/work-client/web/
```

Canonical page graph: `INDEX.md`.

Study Web has a separate `study/` context. Its Angular 22 SPA has the shared
root/auth routes, Guest GS-01–GS-07, Student ST-01–ST-26, Mentor ME-01–ME-18,
and Admin AD-01–AD-25 route groups. Student and Mentor layouts authenticate
through API #03, check the role, and keep tokens in tab memory; Admin uses its
own session. Student ST-02/ST-03 remain profile gates; ST-04 calls #08 while
#15 stays gated; ST-05 calls #08 while #16 stays gated; ST-06/ST-07 remain
payment/result gates. ST-01 calls #20/#38, ST-08 calls #20, ST-09 calls #20/#37
after ACTIVE enrollment, ST-10 calls #22 and explicit #23, and ST-11 calls
#24 after handoff. ST-26 has no caller because #43–#45 are `SOURCE_ONLY`.
Mentor routes have screen-local callers for supported APIs, with some actions
still gated by request/contract gaps. Selected Admin GET callers use
`AdminApiService`; `AdminSessionService` is Admin-only. Live schema, browser
runtime, and deployment remain unverified. API descriptors do not prove a
screen caller exists. Recheck the current route and source before inferring
feature behavior.
Work Web uses React.
Work router giữ route catalog hiện có,
`src/shared/api/work.ts` là ranh giới fetch/Zod của Work và backend tương ứng là
`apps/work-server/src/routes/api_routes.ts`.

Task cụ thể phải chọn đúng subcontext:

- Study Web: `study/AGENTS.md` → `study/INDEX.md`; use its standalone Angular
  pattern and `gui/architech.md` for the scaffold architecture.
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

Không trộn Angular pattern của Study Web với React pattern của Work Web.

Work web dùng React Query cho server state và Zod để parse response. JWT được
lưu với key `access_token` ở localStorage; client decode payload để dựng role
guard nhưng server mới là nơi verify chữ ký. Mọi Work request chỉ gửi Bearer
header khi có token và dùng `credentials: omit`. Không dùng cookie/session,
query-string token hay Neon credential trong browser. Các screen có
loading/error/empty state và các route chưa có API chỉ hiển thị static/placeholder
UI.
