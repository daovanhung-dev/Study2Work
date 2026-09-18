# Business code context

Catalog hiện hành:

- `apps/study-server/docs/business_code/code_event_server.md`
- `apps/study-server/docs/business_code/code_http.md`

Repository dùng identifier uppercase như `SYSTEM_HEALTH_LIVE`, không dùng mẫu
lowercase trong ví dụ generic. Giữ convention thực tế của từng scope.

## Trước khi thêm code

1. Search cả catalog và runtime của mọi server liên quan.
2. Kiểm tra code cùng nghĩa, module owner và HTTP mapping.
3. Xác nhận condition từ requirement/DD/contract/source.
4. Chỉ thêm khi identifier/meaning chưa tồn tại.
5. Cập nhật đúng catalog owner (`apps/study-server/docs/business_code/` cho
   Study), tests và module context trong cùng task.

HTTP status mô tả protocol; business code mô tả kết quả nghiệp vụ/hệ thống.
Không suy ra một khái niệm từ khái niệm còn lại.
