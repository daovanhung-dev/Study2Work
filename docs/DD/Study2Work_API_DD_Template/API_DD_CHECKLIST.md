# API DD Checklist – Study2Work

> Dùng checklist này ở vòng self-review, technical review và approval. Đánh dấu `[x]` chỉ khi tài liệu có thông tin cụ thể, không phải chỉ có placeholder.

## A. Identity và phạm vi

- [ ] API code tuân theo chuẩn module/action/sequence, ví dụ `AUTH-LOGIN-001`.
- [ ] Tên API mô tả một mục tiêu nghiệp vụ rõ ràng, không gom nhiều hành vi không liên quan.
- [ ] Module, bounded context, owner, reviewer, version, status và ngày cập nhật đã có.
- [ ] Endpoint, HTTP method, API version, base path và môi trường hỗ trợ đã xác định.
- [ ] Caller, trigger, use case/activity/sequence reference đã liên kết.
- [ ] Preconditions, postconditions, scope và out-of-scope đã mô tả.

## B. Security, quyền và dữ liệu

- [ ] Authentication scheme được xác định (`None`, `Bearer JWT`, OAuth callback, service-to-service...).
- [ ] Role/permission cần có đã nêu rõ.
- [ ] Ownership/relationship condition được mô tả rõ, không chỉ ghi chung chung “có quyền”.
- [ ] Rate limit, timeout, idempotency và concurrency rule đã quyết định.
- [ ] Các field `PII`, credential, token, internal data đã được đánh dấu và có quy tắc masking/logging.
- [ ] Audit log requirement và actor được xác định nếu API tạo/cập nhật/xóa dữ liệu quan trọng.

## C. Request

- [ ] Mọi path/query/header/cookie/body field đều có mặt trong bảng request.
- [ ] Mỗi field có JSON path, type, required, nullable, default, min/max, format, enum và example.
- [ ] Phân biệt rõ: field thiếu, `null`, chuỗi rỗng, `[]`, `{}` và default server-side.
- [ ] Validation syntax, cross-field validation và business validation được tách riêng.
- [ ] Canonicalization (trim, lowercase, timezone, dedupe, HTML sanitization...) được mô tả khi cần.
- [ ] Có request JSON hợp lệ, invalid request representative và header example.

## D. Response

- [ ] Có response matrix bao phủ success, created, empty, asynchronous, validation, auth/permission, not found, conflict, rate limit, dependency và internal error khi áp dụng.
- [ ] Mọi field response có JSON path, type, nullable, source, visibility và example.
- [ ] Mô tả rõ trường hợp danh sách rỗng khác với resource không tồn tại.
- [ ] Pagination/cursor/sort/filter response đầy đủ nếu API list/search.
- [ ] `businessCode`, `message`, `timestamp`, `traceId`, `data`, `errors` dùng nhất quán theo contract.
- [ ] Không có PII/secret/internal fields vô tình lộ ra response.

## E. Data mapping và nghiệp vụ

- [ ] Flow theo đúng runtime order: parse → validate → authN → authZ → load → rule → mutate/query → transaction → event → response.
- [ ] Mọi biến khởi tạo đã có nguồn, type, normalisation, lifetime và sensitivity.
- [ ] Mọi business rule có ID, điều kiện, quyết định, outcome và error code liên kết.
- [ ] Mọi repository method/query có purpose, input, output, table, column, predicate, index/lock và operation type (`READ/INSERT/UPDATE/DELETE`).
- [ ] Ghi rõ read-after-write, optimistic lock, row lock, unique constraint hoặc idempotency key nếu có nguy cơ race condition.
- [ ] Transaction boundary, commit condition, rollback condition và isolation/locking strategy đã quyết định.
- [ ] Cache key/TTL/invalidation và external call timeout/fallback/retry đã mô tả nếu áp dụng.
- [ ] Event/queue/job notification và tính chất sync/async đã rõ.
- [ ] Response mapping có nguồn cho từng field; derived/snapshot field được đánh dấu.

## F. Error và vận hành

- [ ] Mỗi lỗi có code nghiệp vụ ổn định, HTTP status, category, safe message, trigger, client action, retry policy, severity và owner.
- [ ] Validation errors chỉ ra field/kỳ vọng mà không tiết lộ dữ liệu nhạy cảm.
- [ ] Không dùng cùng một code cho các nguyên nhân nghiệp vụ khác nhau.
- [ ] Lỗi transient (timeout/dependency) tách khỏi lỗi không thể retry.
- [ ] Log checkpoints, `traceId`, masked fields, metric/alert threshold và dashboard owner đã nêu khi API critical.
- [ ] Có test cases tối thiểu cho mọi error category và state/permission boundary.

## G. Compatibility và review

- [ ] Mọi thay đổi breaking được gắn `BREAKING` trong History và có kế hoạch rollout/migration.
- [ ] OpenAPI/Swagger, DTO, validation schema, repository/service/controller và test name có thể map một-một tới DD.
- [ ] Người review xác nhận DD không mâu thuẫn với Domain Model, ERD, Business Code và kiến trúc module.
- [ ] Tài liệu không còn placeholder, sample secret hay TODO không có owner/due date.
