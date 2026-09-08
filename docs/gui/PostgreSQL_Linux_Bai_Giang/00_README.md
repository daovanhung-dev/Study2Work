# PostgreSQL trên Linux — Giáo trình thực hành

> Mục tiêu: cài PostgreSQL trên Linux, vận hành service, tạo user/database/schema, thiết kế bảng có khóa chính/khóa ngoại, sử dụng các lệnh thường gặp và kết nối bằng Visual Studio Code.

## Phạm vi

- Hệ điều hành chính: **Debian/Ubuntu**, ưu tiên Debian.
- PostgreSQL: **PostgreSQL 18** (nhánh stable hiện hành tại thời điểm biên soạn 2026-09-08).
- Công cụ client:
  - `psql` — terminal chính thức của PostgreSQL.
  - **PostgreSQL extension by Microsoft** trong Visual Studio Code.
- Không dùng PostgreSQL 19 beta cho môi trường học/production.

## Cấu trúc bài học

1. [01 — Cài đặt và setup](01_Cai_dat_va_setup.md)
2. [02 — Khởi động và kiểm tra sau cài đặt](02_Khoi_dong_sau_khi_cai.md)
3. [03 — Tài khoản, DB, bảng, cột, PK, FK](03_User_DB_Table_Column_PK_FK.md)
4. [04 — Tổng hợp lệnh hay dùng](04_Lenh_PostgreSQL_hay_dung.md)
5. [05 — Kết nối PostgreSQL với VS Code](05_Ket_noi_VSCode.md)

## Sơ đồ tư duy

```text
Linux
│
├─ package: postgresql / postgresql-18
├─ service: systemd
│  └─ PostgreSQL cluster
│     ├─ database: postgres
│     ├─ database: template0
│     ├─ database: template1
│     └─ database: appdb
│        ├─ schema: public
│        ├─ table: departments
│        └─ table: employees
│
└─ client
   ├─ psql
   └─ VS Code + PostgreSQL by Microsoft
```

## Quy ước ví dụ

- Database: `appdb`
- Role đăng nhập: `app_user`
- Schema: `public`
- Bảng: `departments`, `employees`
- Port mặc định PostgreSQL: `5432`

> Không dùng role superuser `postgres` cho ứng dụng chạy hằng ngày. Hãy tạo một role riêng với đúng quyền cần thiết.

## Nguồn chính thức

- PostgreSQL Linux downloads: https://www.postgresql.org/download/linux/
- PostgreSQL Debian packages: https://www.postgresql.org/download/linux/debian/
- PostgreSQL Documentation 18: https://www.postgresql.org/docs/current/
- Microsoft PostgreSQL extension for VS Code: https://learn.microsoft.com/en-us/azure/postgresql/developer/vs-code-extension/vs-code-overview
- Visual Studio Marketplace — PostgreSQL by Microsoft: https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql
- Debian PostgreSQL tools: https://manpages.debian.org/trixie/postgresql-common/
