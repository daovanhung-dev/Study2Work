# 12 — Implementation Checklist

## API Contract

- [ ] Method đúng.
- [ ] Endpoint đúng.
- [ ] Request model đúng field/type.
- [ ] Auth requirement rõ.
- [ ] Success response đúng contract.
- [ ] Error cases được xử lý.

## Router

- [ ] Router mỏng.
- [ ] Có `Depends(get_db)` nếu cần DB.
- [ ] Không có SQL/business logic.
- [ ] Async/sync phù hợp call chain.

## Model

- [ ] Pydantic type cụ thể.
- [ ] Không chứa DB logic.

## Validate

- [ ] Required/blank.
- [ ] Length.
- [ ] Format.
- [ ] Range/enum khi cần.
- [ ] Không hard-code trace ID trong implementation đích.

## View

- [ ] Flow đọc từ trên xuống dễ hiểu.
- [ ] Normalize trước validation nếu cần.
- [ ] Business checks đúng thứ tự.
- [ ] Security helper dùng từ core.
- [ ] Query dùng từ module query.
- [ ] External calls dùng service.
- [ ] Mutation commit đúng boundary.
- [ ] Failure rollback khi cần.

## Query/DB

- [ ] Named parameters.
- [ ] Không SQL injection qua string interpolation.
- [ ] Column/table có nguồn xác nhận.
- [ ] Không commit trong query constant/helper cấp thấp.
- [ ] Không dùng global Session cho HTTP request.

## Response/Error

- [ ] `businessCode` nhất quán.
- [ ] `traceId` cùng request.
- [ ] Không expose exception/SQL raw.
- [ ] Không expose secret.

## External Service

- [ ] Timeout có kiểm soát.
- [ ] Exception được phân loại.
- [ ] Module không biết transport detail không cần thiết.

## Verification

- [ ] App/module import được.
- [ ] Happy path được kiểm tra nếu có môi trường.
- [ ] Validation failure được kiểm tra.
- [ ] DB conflict/not-found được kiểm tra khi liên quan.
- [ ] Transaction failure được kiểm tra khi nhiều mutation.
- [ ] Không còn typo/undefined identifier trong code đã chạm tới.
