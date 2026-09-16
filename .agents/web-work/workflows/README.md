# Work Web workflow

Task web phải chọn Vue hoặc React app, rồi trace `route -> page/layout ->
React Query/local state -> apiRequest -> Express route -> response envelope`.
Không dùng server layer order cho frontend và không trộn Vue patterns từ Study
web.

Với route mới hoặc API change, kiểm tra `router.tsx`, page component,
`shared/api/work.ts`, role guard và legacy-web OpenAPI. Chạy `npm run typecheck`
và `npm test`; giữ test cho role access, Bearer/credentials boundary và 401
token clearing. Route chưa có server API chỉ được mô tả là placeholder, không tự
thêm nghiệp vụ.
