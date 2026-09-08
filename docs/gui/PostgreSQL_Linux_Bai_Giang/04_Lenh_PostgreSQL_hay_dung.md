# 04 — Tổng hợp các lệnh PostgreSQL hay dùng

> Cheat sheet dành cho ghi chép và thực hành hằng ngày.

# 1. Linux / service

| Mục đích | Lệnh |
|---|---|
| Version client | `psql --version` |
| Xem cluster Debian | `pg_lsclusters` |
| Status service | `sudo systemctl status postgresql` |
| Start | `sudo systemctl start postgresql` |
| Stop | `sudo systemctl stop postgresql` |
| Restart | `sudo systemctl restart postgresql` |
| Reload | `sudo systemctl reload postgresql` |
| Auto-start | `sudo systemctl enable postgresql` |
| Kiểm tra server | `pg_isready` |
| Kiểm tra host/port | `pg_isready -h 127.0.0.1 -p 5432` |

Cluster Debian cụ thể:

```bash
sudo pg_ctlcluster 18 main status
sudo pg_ctlcluster 18 main start
sudo pg_ctlcluster 18 main stop
sudo pg_ctlcluster 18 main restart
sudo pg_ctlcluster 18 main reload
```

---

# 2. Kết nối `psql`

## Local admin

```bash
sudo -u postgres psql
```

## TCP

```bash
psql -h 127.0.0.1 -p 5432 -U app_user -d appdb
```

## Buộc hỏi password trước

```bash
psql -h 127.0.0.1 -U app_user -d appdb -W
```

Tham số:

```text
-h host
-p port
-U user
-d database
-W password prompt
```

---

# 3. Meta-command trong `psql`

> Meta-command bắt đầu bằng `\` và do `psql` xử lý, không phải SQL server.

| Lệnh | Ý nghĩa |
|---|---|
| `\?` | help meta-command |
| `\h` | help SQL |
| `\q` | thoát |
| `\l` | liệt kê database |
| `\c appdb` | chuyển database |
| `\conninfo` | xem connection hiện tại |
| `\du` | liệt kê role |
| `\dn` | liệt kê schema |
| `\dt` | liệt kê table |
| `\d employees` | mô tả table |
| `\di` | liệt kê index |
| `\df` | liệt kê function |
| `\x` | toggle expanded output |
| `\timing` | hiển thị thời gian query |
| `\password app_user` | đổi password role |

Có thể chạy file SQL:

```text
\i /path/to/file.sql
```

---

# 4. Thông tin server

```sql
SELECT version();
SELECT current_user;
SELECT current_database();
```

```sql
SHOW config_file;
SHOW hba_file;
SHOW data_directory;
SHOW port;
SHOW listen_addresses;
```

---

# 5. Role / user

## Tạo role login

```sql
CREATE ROLE app_user WITH LOGIN;
```

Đặt password:

```text
\password app_user
```

## Tạo user

```sql
CREATE USER app_user;
```

`CREATE USER` tương đương role có `LOGIN`.

## Thay đổi role

```sql
ALTER ROLE app_user CREATEDB;
ALTER ROLE app_user NOCREATEDB;
```

## Xóa role

```sql
DROP ROLE app_user;
```

---

# 6. Database

## Tạo

```sql
CREATE DATABASE appdb;
```

Owner:

```sql
CREATE DATABASE appdb OWNER app_user;
```

## Xóa

```sql
DROP DATABASE appdb;
```

Command-line:

```bash
createdb appdb
dropdb appdb
```

---

# 7. Schema

## Tạo

```sql
CREATE SCHEMA app;
```

## Xóa

```sql
DROP SCHEMA app;
```

Nếu có object:

```sql
DROP SCHEMA app CASCADE;
```

---

# 8. Table

## Tạo

```sql
CREATE TABLE users (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username varchar(100) NOT NULL UNIQUE,
    created_at timestamptz NOT NULL DEFAULT now()
);
```

## Xóa

```sql
DROP TABLE users;
```

Có điều kiện:

```sql
DROP TABLE IF EXISTS users;
```

---

# 9. Column

## Thêm

```sql
ALTER TABLE users
ADD COLUMN email varchar(255);
```

## Xóa

```sql
ALTER TABLE users
DROP COLUMN email;
```

## Rename

```sql
ALTER TABLE users
RENAME COLUMN username TO login_name;
```

## Đổi type

```sql
ALTER TABLE users
ALTER COLUMN login_name TYPE varchar(150);
```

## Default

```sql
ALTER TABLE users
ALTER COLUMN created_at SET DEFAULT now();
```

Xóa default:

```sql
ALTER TABLE users
ALTER COLUMN created_at DROP DEFAULT;
```

---

# 10. Constraint

## Primary key

```sql
ALTER TABLE users
ADD CONSTRAINT pk_users PRIMARY KEY (id);
```

## Foreign key

```sql
ALTER TABLE employees
ADD CONSTRAINT fk_employees_department
FOREIGN KEY (department_id)
REFERENCES departments(id);
```

## Unique

```sql
ALTER TABLE users
ADD CONSTRAINT uq_users_login_name UNIQUE (login_name);
```

## Check

```sql
ALTER TABLE employees
ADD CONSTRAINT ck_salary_nonnegative
CHECK (salary >= 0);
```

## Drop constraint

```sql
ALTER TABLE employees
DROP CONSTRAINT ck_salary_nonnegative;
```

---

# 11. CRUD

## INSERT

```sql
INSERT INTO users (username)
VALUES ('hung');
```

Nhiều row:

```sql
INSERT INTO users (username)
VALUES
    ('hung'),
    ('an'),
    ('binh');
```

## SELECT

```sql
SELECT *
FROM users;
```

Điều kiện:

```sql
SELECT *
FROM users
WHERE id = 1;
```

Sắp xếp:

```sql
SELECT *
FROM users
ORDER BY id DESC;
```

Giới hạn:

```sql
SELECT *
FROM users
ORDER BY id DESC
LIMIT 10;
```

## UPDATE

```sql
UPDATE users
SET username = 'hung_dev'
WHERE id = 1;
```

## DELETE

```sql
DELETE FROM users
WHERE id = 1;
```

---

# 12. JOIN cơ bản

```sql
SELECT
    e.id,
    e.full_name,
    d.name AS department
FROM employees AS e
LEFT JOIN departments AS d
    ON d.id = e.department_id;
```

---

# 13. Transaction

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE id = 1;

UPDATE accounts
SET balance = balance + 100
WHERE id = 2;

COMMIT;
```

Nếu có lỗi:

```sql
ROLLBACK;
```

---

# 14. Quyền

## Database

```sql
GRANT CONNECT ON DATABASE appdb TO app_user;
```

## Schema

```sql
GRANT USAGE ON SCHEMA public TO app_user;
```

## Table

```sql
GRANT SELECT, INSERT, UPDATE, DELETE
ON employees
TO app_user;
```

Tất cả table hiện có:

```sql
GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA public
TO app_user;
```

## Sequence

```sql
GRANT USAGE, SELECT
ON ALL SEQUENCES IN SCHEMA public
TO app_user;
```

Thu hồi:

```sql
REVOKE DELETE ON employees FROM app_user;
```

---

# 15. Backup và restore

## Plain SQL dump

```bash
pg_dump -h 127.0.0.1 -U app_user -d appdb > appdb.sql
```

Restore plain SQL:

```bash
psql -h 127.0.0.1 -U app_user -d appdb < appdb.sql
```

## Custom-format dump

```bash
pg_dump -Fc -h 127.0.0.1 -U app_user -d appdb -f appdb.dump
```

Restore:

```bash
pg_restore -h 127.0.0.1 -U app_user -d appdb appdb.dump
```

`pg_restore` dùng cho archive được tạo bởi `pg_dump` ở format không phải plain-text.

> Backup/restore production cần thêm chiến lược quyền, consistency, size, retention và kiểm thử restore.

---

# 16. Diagnostics nhanh

## Server không lên

```bash
sudo systemctl status postgresql
pg_lsclusters
sudo pg_ctlcluster 18 main status
```

## Server không nhận connection

```bash
pg_isready -h 127.0.0.1 -p 5432
```

## Xem config path

```sql
SHOW config_file;
SHOW hba_file;
```

## Xem connection hiện tại

```text
\conninfo
```

## Xem table definition

```text
\d employees
```

---

# 17. 20 lệnh cần thuộc trước

```text
psql --version
pg_lsclusters
systemctl status postgresql
pg_isready
sudo -u postgres psql

\l
\c
\du
\dt
\d
\conninfo
\q

CREATE ROLE
CREATE DATABASE
CREATE TABLE
ALTER TABLE
INSERT
SELECT
UPDATE
DELETE
```

## Nguồn chính thức

- PostgreSQL — `psql`: https://www.postgresql.org/docs/current/app-psql.html
- PostgreSQL — SQL Commands: https://www.postgresql.org/docs/current/sql-commands.html
- PostgreSQL — Client Applications: https://www.postgresql.org/docs/current/reference-client.html
- PostgreSQL — `GRANT`: https://www.postgresql.org/docs/current/sql-grant.html
- PostgreSQL — `pg_dump`: https://www.postgresql.org/docs/current/app-pgdump.html
- PostgreSQL — `pg_restore`: https://www.postgresql.org/docs/current/app-pgrestore.html
- PostgreSQL — `pg_isready`: https://www.postgresql.org/docs/current/app-pg-isready.html
