# Lệnh chạy script server

Các lệnh dưới đây chạy từ root của server con được ghi ở từng mục. Thay các giá trị mẫu bằng cấu hình đích của bạn; không ghi database URL hoặc credential thật vào tài liệu hay source.

## Study Server

Thư mục làm việc: [`apps/study-server/`](../../apps/study-server/).

### Tạo tài khoản Admin

Script yêu cầu cấu hình database tường minh và không tự đọc `.env`. Cài dependencies bằng `uv sync`, sau đó đặt ba biến môi trường sau trong shell hiện tại.

PowerShell:

```powershell
$env:STUDY_ADMIN_DATABASE_URL = "<PostgreSQL URL>"
$env:STUDY_ADMIN_DB_SCHEMA = "<schema đích>"
$env:STUDY_ADMIN_APP_ENV = "local"
uv run python scripts/create_admin.py
```

Bash:

```bash
read -r -s -p "Study DB URL: " STUDY_ADMIN_DATABASE_URL
printf '\n'
export STUDY_ADMIN_DATABASE_URL
export STUDY_ADMIN_DB_SCHEMA='dao_van_hung'
export STUDY_ADMIN_APP_ENV='local'
uv run python scripts/create_admin.py
unset STUDY_ADMIN_DATABASE_URL STUDY_ADMIN_DB_SCHEMA STUDY_ADMIN_APP_ENV
```

Script kiểm tra database/schema rồi yêu cầu xác nhận; họ tên, email và mật khẩu được nhập tương tác. Email đã tồn tại sẽ bị từ chối. Khi chủ động thao tác trên production, thay URL/schema bằng target production, đặt `STUDY_ADMIN_APP_ENV` thành `production` và thêm `--allow-production`; script vẫn yêu cầu xác nhận production tại prompt.

PowerShell:

```powershell
$env:STUDY_ADMIN_APP_ENV = "production"
uv run python scripts/create_admin.py --allow-production
```

Bash:

```bash
export STUDY_ADMIN_APP_ENV="production"
uv run python scripts/create_admin.py --allow-production
```

### Nạp seed cho API #11 và #15

Hai script seed dùng cấu hình Study hiện tại. Kiểm tra database/schema trong cấu hình ứng dụng trước khi chạy; các lệnh ghi hoặc cập nhật dữ liệu mẫu và không có chế độ dry-run.

```bash
uv run python scripts/seed_api_11_15.py
```

### Nạp seed cho API #21–#25

```bash
uv run python scripts/seed_api_21_25.py
```

## Work Server

Thư mục làm việc: [`apps/work-server/`](../../apps/work-server/).

Trước lần chạy đầu, cài dependencies và generate Prisma Client:

```bash
npm install
npm run prisma:generate
```

Chạy kiểm tra dữ liệu seed mà không kết nối database:

```bash
npm run seed:accounts -- --dry-run
```

Ghi seed vào Neon sau khi xác nhận target:

```bash
npm run seed:accounts -- --confirm-neon
```

Lệnh xác nhận chỉ chấp nhận database Neon, ghi dữ liệu seed và cập nhật `docs/seed_data/accounts.md` tại root repository. Work Server lấy cấu hình database từ `src/utils/constants.ts`, không đọc `.env`; hãy kiểm tra target trước khi dùng `--confirm-neon`. Dùng các npm script ở trên thay vì chạy helper nội bộ `scripts/prisma-with-constants.ts` trực tiếp.

## AI Server

Thư mục làm việc: [`apps/ai-server/`](../../apps/ai-server/). Hiện không có script vận hành dữ liệu riêng. Entry point `ai-server` được khai báo trong `pyproject.toml` chỉ in lời chào, không khởi động API; để chạy API, dùng lệnh Uvicorn trong [build_server.md](build_server.md).
