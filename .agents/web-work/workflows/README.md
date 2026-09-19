# Work Web workflow

Task web phải đọc `.agents/project/design.md`, chọn Vue hoặc React app, rồi trace `route -> page/layout ->
React Query/local state -> apiRequest -> Express route -> response envelope`.
Không dùng server layer order cho frontend và không trộn Vue patterns từ Study
web.

Với route mới hoặc API change, kiểm tra `router.tsx`, page component,
`shared/api/work.ts`, role guard và legacy-web OpenAPI. Chạy `npm run typecheck`
và `npm test`; giữ test cho role access, Bearer/credentials boundary và 401
token clearing. Route chưa có server API chỉ được mô tả là placeholder, không tự
thêm nghiệp vụ.

Với route/UI change, kiểm tra cả breakpoint 320/375/768/1024/1440px, keyboard
focus, text overflow, contrast, loading/error/empty state và
`prefers-reduced-motion`. Không đổi route, API, auth, navigation semantics hay
thêm persistence cho placeholder.

Mọi task phải chọn đúng Study Vue hoặc Work React subcontext, dùng
`.agents/worklog/TEMPLATE.md` và ghi command không chạy được là
`DECLARED_NOT_RUNNABLE`.
