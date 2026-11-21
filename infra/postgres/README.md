# Study2Work V1-PILOT — PostgreSQL DDL

Bộ SQL này được sinh từ `03_THIET_KE_CO_SO_DU_LIEU.md`.

## Cấu trúc

- `00_bootstrap_databases.sql`: tạo `identity_db`, `study_db`, `work_db`.
- `01_identity_db.sql`: 20 bảng IAM.
- `02_study_db.sql`: 60 bảng Study.
- `03_work_db.sql`: 98 bảng Work/AI/Payment/University.
- `setup_all.sh`: chạy toàn bộ theo đúng thứ tự.

Tổng số bảng: 178.

## Chạy

```bash
PGUSER=postgres \
PGHOST=127.0.0.1 \
PGPORT=5432 \
./infra/postgres/setup_all.sh
```

Hoặc chạy từng file bằng `psql -v ON_ERROR_STOP=1`.

## Nguyên tắc đã giữ từ tài liệu

- Ba database vật lý tách biệt; không tạo foreign key xuyên database.
- UUID nghiệp vụ không tự sinh trong PostgreSQL; ứng dụng phải cấp UUID v7.
- `timestamptz` dùng UTC; tiền dùng `bigint`.
- Enum PostgreSQL được tạo theo danh mục chuẩn của tài liệu.
- `ENTITY`/`TENANT_ENTITY` tự tăng `row_version` và cập nhật `updated_at` bằng trigger.
- `APPEND` bị chặn UPDATE/DELETE.
- `IMMUTABLE` bị chặn hard DELETE; các chuyển trạng thái một chiều vẫn phải đi qua service/procedure theo tài liệu.
- Bảng `TENANT_ENTITY` có `UNIQUE(tenant_id,id)`; FK tới bảng tenant khác dùng khóa ghép `(tenant_id,parent_id)` khi có thể xác định trực tiếp.
- RLS tenant được bật cho các bảng `TENANT_ENTITY` trong `work_db`; request phải thiết lập `SET LOCAL app.tenant_id`.
- Các constraint/index biểu diễn trực tiếp và an toàn đã được tạo.
- Mỗi bảng giữ lại toàn bộ mô tả ràng buộc/chỉ mục liên quan dưới dạng comment `-- SPEC:` để không làm mất các quy tắc nghiệp vụ chưa thể mã hóa bằng CHECK/FK cục bộ.

## Lưu ý triển khai

Đây là baseline DDL cho database trống. Tài liệu nguồn còn quy định nhiều invariant liên hàng, state-machine, kiểm tra tệp CLEAN, xác minh quyền sở hữu, thanh toán, AI review, retention và concurrency. Các invariant đó không được tự suy diễn thành trigger nguy hiểm; chúng được giữ dưới dạng `-- SPEC:` và cần được hiện thực trong migration/service/procedure tương ứng trước production.

Tài liệu nguồn cũng chỉ định Identity/Study dùng Alembic và Work dùng migration Prisma có rà soát SQL; vì vậy bộ này phù hợp để bootstrap/schema-reference và có thể được tách tiếp thành migration chính thức.
