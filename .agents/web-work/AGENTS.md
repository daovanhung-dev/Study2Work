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
own session. Student ST-02 calls #04 read-only; ST-03 calls #04/#13/#14 for
supported profile and avatar fields, while Bio remains gated. ST-04 calls #08
then Student-authenticated #15; free enrollment calls #19 and verifies through
#20, while paid courses hand off to ST-05. The #15 catalog actor still says
Public, which conflicts with the authenticated current source. ST-05 calls #08
while #16 stays gated; ST-06/ST-07 remain payment/result gates. ST-01 calls
#20/#38, ST-08 calls #20, ST-09 calls #20/#37
after ACTIVE enrollment, ST-10 calls #22 and explicit #23, and ST-11 calls
#24 after handoff. ST-26 calls #43–#45 for list/unread/page and mark-one/all;
it retries the last valid page if rows shrink and steps back if separate
COUNT/LIST snapshots return an empty page with positive total. Typed deep links
and screenshot-only notification panels remain unsupported, and #45's response
differs from the catalog.
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

Với yêu cầu tạo UTC/testcase từ Study Screen DD hiện có, load `utc-screen` và
workflow `utc-screen-generation` qua `study/AGENTS.md`. Đây là lập kế hoạch
kiểm thử từ DD; không thay workflow triển khai màn hình hoặc skill authoring
Web/API DD.

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
