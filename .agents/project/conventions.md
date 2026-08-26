# Convention và workflow đã xác minh

## Repository-wide

- UTF-8, LF, final newline, trim trailing whitespace.
- Indent 2 spaces; Python 4 spaces (`.editorconfig`).
- Không thay đổi secret/example value thành credential thật và không log token,
  password, DB credential, raw SQL hay upstream sensitive body.
- API mới hướng tới envelope `success`, `businessCode`, `message`, `data`,
  `meta`, `traceId`; kiểm tra scope vì AI runtime chưa áp dụng contract này.
- `X-Trace-Id` là header chung ở Study/Work intent; Work runtime đã implement,
  Study đang bị mismatch import.

## Python server

- Python `>=3.12`, type hints, snake_case function/value, PascalCase class.
- Study Ruff: line length 100, double quotes, E/F/I/B/UP/SIM; mypy strict.
- DB helper Study/AI là synchronous SQLAlchemy và named parameters; helper không
  commit. View/use case sở hữu transaction nếu module thực sự tồn tại.
- Không tự chuyển raw SQL/SQLAlchemy sang ORM hoặc ngược lại. AI hiện không gọi
  DB; Study chưa có query module/domain schema.
- Actual AI module dùng `model.py`, `validate.py`, `query.py`, `view.py`; Study
  không còn module để xác nhận tên `module.py` hay `model.py`. Không invent
  package layout để chữa import nếu requirement chưa chốt ownership.

## Work TypeScript server

- Strict TypeScript, NodeNext ESM, import nội bộ dùng suffix `.js`.
- Nest DI modules/controllers/services, Fastify adapter, global guard/pipe/
  interceptor/filter, Prisma client.
- camelCase value/function, PascalCase class/type, decorator metadata.
- Không áp bốn-file Python hoặc raw-SQL convention của Study lên Work.

## Workflow theo task type

### coding

```text
requirement/contract còn tồn tại
  -> existing module pattern trong đúng scope
  -> request/model/DTO
  -> validation/permission
  -> query/repository/service dependency
  -> orchestration/controller/view
  -> tests
  -> business-code + HTTP catalog
  -> context liên quan
```

Nếu scope dùng bốn layer Python và source đã xác nhận, ưu tiên model/module ->
validate -> query -> view, rồi router. Ngoại lệ chỉ khi task thật sự chạm một
layer hoặc source có architecture khác; ghi lý do trong plan.

### fix

Reproduce trước, trace toàn call flow, xác định root cause và smallest owning
layer, thêm regression test. Không sửa symptom hoặc refactor lân cận nếu chưa
cần.

### docs

Đối chiếu source và test/contract hiện hành. Gắn `NOT_FOUND`, `UNWIRED`,
`DECLARED_NOT_RUNNABLE` thay vì viết requirement thay nguồn bị thiếu.

### test

Đọc requirement/contract, implementation, business rule và error paths. Không
viết assertion chỉ để hợp thức hóa implementation sai hoặc stale test.

## Checklist trước edit

1. Endpoint/function nằm ở scope/module nào?
2. Caller, callee và public interface nào bị tác động?
3. Có DB/external side effect hoặc transaction không?
4. Business code/HTTP/response contract nào phải giữ?
5. Existing tests nào đang đúng, stale hoặc bị block?
6. Có nguồn đủ để thêm field/table/rule không?

## Checklist sau edit

1. Import/build/typecheck phù hợp scope.
2. Happy path + validation/error + dependency failure liên quan.
3. Query params/placeholders, commit/rollback và async/await đúng.
4. Trace/envelope/business code/HTTP không đổi ngoài requirement.
5. Không có unrelated diff; context được cập nhật nếu architecture đổi.
