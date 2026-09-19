# 07 — Viết Views.md và UI states

## View contract

Mỗi view/page/modal/widget có:

- View ID, route/entry point, actor và access condition.
- Feature/function/API/entity liên quan.
- Layout/component, displayed data và display condition.
- Input validation client/server và copy lỗi.
- Interaction → function/API → success/failure → navigation.
- Data fetch/cache/refresh/fallback.
- Responsive/accessibility rule.
- Analytics/audit event nếu áp dụng.

## States bắt buộc

Data-driven view phải mô tả ít nhất:

`Initial`, `Loading`, `Success`, `Empty`, `Validation Error`, `Business Error`,
`System/Network Error`, `Unauthorized`, `Forbidden`, `Offline` khi có liên quan.

Thông báo UI không được lộ stack trace, query, tên bảng, token hoặc thuật ngữ
nội bộ không dành cho người dùng.
