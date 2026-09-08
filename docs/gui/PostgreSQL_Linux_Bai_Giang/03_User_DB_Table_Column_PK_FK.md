# 03 — Tạo tài khoản, database, bảng, cột, khóa chính và khóa ngoại

## 1. Mục tiêu

Sau phần này bạn có thể:

- hiểu `ROLE` và `USER`;
- tạo account đăng nhập;
- tạo database và owner;
- tạo table;
- thêm/sửa/xóa column;
- tạo `PRIMARY KEY`;
- tạo `FOREIGN KEY`;
- cấp quyền cơ bản cho application user.

---

# Phần A — User và Role

## 2. PostgreSQL dùng khái niệm ROLE

Trong PostgreSQL:

```text
ROLE = thực thể có thể sở hữu object và có privilege
```

Role có thể:

- được dùng như user;
- được dùng như group;
- có hoặc không có quyền `LOGIN`.

`CREATE USER` thực chất là alias của `CREATE ROLE`, nhưng `CREATE USER` mặc định có `LOGIN`.

### Tạo role đăng nhập

Đăng nhập quản trị:

```bash
sudo -u postgres psql
```

Tạo role:

```sql
CREATE ROLE app_user WITH LOGIN;
```

### Đặt password an toàn trong `psql`

```text
\password app_user
```

`psql` sẽ hỏi password mà không cần ghi plaintext password vào SQL history.

### Kiểm tra role

```text
\du
```

### Xóa role

```sql
DROP ROLE app_user;
```

> Chỉ xóa khi role không còn sở hữu object hoặc dependency cần xử lý.

---

## 3. Các thuộc tính role quan trọng

Ví dụ:

```sql
CREATE ROLE app_user
WITH
    LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE;
```

Ý nghĩa:

| Thuộc tính | Ý nghĩa |
|---|---|
| `LOGIN` | được đăng nhập |
| `NOLOGIN` | role nhóm/role quyền, không login |
| `SUPERUSER` | bỏ qua hầu hết kiểm soát quyền |
| `CREATEDB` | được tạo database |
| `CREATEROLE` | được quản trị role theo phạm vi PostgreSQL cho phép |
| `REPLICATION` | dùng cho replication |
| `CONNECTION LIMIT n` | giới hạn connection |

Khuyến nghị application user:

```text
LOGIN
NOSUPERUSER
NOCREATEDB
NOCREATEROLE
```

Không cấp `SUPERUSER` cho application chỉ để "cho chạy được".

---

# Phần B — Database

## 4. Tạo database

### Cách 1 — SQL

```sql
CREATE DATABASE appdb;
```

### Tạo database có owner

```sql
CREATE DATABASE appdb OWNER app_user;
```

Để tạo database, role thực thi phải là superuser hoặc có privilege `CREATEDB`.

### Cách 2 — command-line

```bash
createdb appdb
```

`createdb` là wrapper của SQL `CREATE DATABASE`.

---

## 5. Kết nối vào database

Trong `psql`:

```text
\c appdb
```

Hoặc:

```text
\connect appdb
```

Từ shell:

```bash
psql -h 127.0.0.1 -p 5432 -U app_user -d appdb
```

Các tham số:

```text
-h = host
-p = port
-U = username
-d = database
```

---

# Phần C — Table và Column

## 6. Tạo bảng đầu tiên

Ta thiết kế:

```text
departments
└─ id PK

employees
├─ id PK
└─ department_id FK -> departments.id
```

### Bảng `departments`

```sql
CREATE TABLE departments (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL UNIQUE
);
```

### Bảng `employees`

```sql
CREATE TABLE employees (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name varchar(150) NOT NULL,
    email varchar(255) NOT NULL UNIQUE,
    salary numeric(12,2) CHECK (salary >= 0),
    department_id bigint,
    created_at timestamptz NOT NULL DEFAULT now(),

    CONSTRAINT fk_employees_department
        FOREIGN KEY (department_id)
        REFERENCES departments(id)
        ON DELETE SET NULL
);
```

---

## 7. Giải thích từng thành phần

### `bigint`

Số nguyên 64-bit, phù hợp cho ID có phạm vi lớn.

### `GENERATED ALWAYS AS IDENTITY`

PostgreSQL tự sinh giá trị từ sequence ẩn.

Ví dụ insert:

```sql
INSERT INTO departments (name)
VALUES ('Engineering');
```

Không cần truyền `id`.

### `PRIMARY KEY`

```sql
id bigint ... PRIMARY KEY
```

Khóa chính:

- xác định duy nhất mỗi row;
- không được `NULL`;
- không được trùng;
- PostgreSQL tự tạo unique index để thực thi constraint.

Một bảng chỉ có tối đa một `PRIMARY KEY`, nhưng primary key có thể gồm nhiều cột.

### `NOT NULL`

```sql
full_name varchar(150) NOT NULL
```

Cột bắt buộc có giá trị.

### `UNIQUE`

```sql
email varchar(255) NOT NULL UNIQUE
```

Không cho hai row có cùng email.

### `CHECK`

```sql
salary numeric(12,2) CHECK (salary >= 0)
```

Ràng buộc dữ liệu theo biểu thức boolean.

### `DEFAULT`

```sql
created_at timestamptz NOT NULL DEFAULT now()
```

Nếu `INSERT` không truyền giá trị, PostgreSQL dùng `now()`.

---

# Phần D — Foreign Key

## 8. Khóa ngoại

```sql
FOREIGN KEY (department_id)
REFERENCES departments(id)
```

Ý nghĩa:

```text
employees.department_id
        ↓
phải tham chiếu đến
        ↓
departments.id
```

Nếu `department_id = 10`, PostgreSQL yêu cầu department có `id = 10`, trừ khi giá trị là `NULL`.

Foreign key giúp giữ **referential integrity**.

---

## 9. Hành vi khi xóa record được tham chiếu

### `ON DELETE NO ACTION`

Mặc định.

Ngăn thao tác xóa nếu còn row phụ thuộc, trừ trường hợp constraint deferred phù hợp.

### `ON DELETE RESTRICT`

Chặn xóa referenced row một cách chặt hơn.

### `ON DELETE CASCADE`

```sql
FOREIGN KEY (department_id)
REFERENCES departments(id)
ON DELETE CASCADE
```

Xóa department sẽ tự xóa các row con tham chiếu tới nó.

Dùng khi row con không thể tồn tại độc lập.

### `ON DELETE SET NULL`

```sql
ON DELETE SET NULL
```

Xóa department -> `employees.department_id` được đặt `NULL`.

Cột foreign key phải cho phép `NULL`.

---

# Phần E — Thêm/sửa/xóa cột

## 10. Thêm column

```sql
ALTER TABLE employees
ADD COLUMN phone varchar(30);
```

Có default:

```sql
ALTER TABLE employees
ADD COLUMN is_active boolean NOT NULL DEFAULT true;
```

---

## 11. Xóa column

```sql
ALTER TABLE employees
DROP COLUMN phone;
```

Nếu có dependency bên ngoài:

```sql
ALTER TABLE employees
DROP COLUMN phone CASCADE;
```

> Cẩn thận với `CASCADE`: nó có thể xóa object phụ thuộc.

---

## 12. Đổi tên column

```sql
ALTER TABLE employees
RENAME COLUMN full_name TO name;
```

---

## 13. Đổi kiểu dữ liệu

```sql
ALTER TABLE employees
ALTER COLUMN salary TYPE numeric(14,2);
```

Nếu PostgreSQL không tự convert được, có thể cần `USING`.

---

## 14. Thêm `NOT NULL`

```sql
ALTER TABLE employees
ALTER COLUMN email SET NOT NULL;
```

Dữ liệu hiện có phải thỏa constraint.

Xóa:

```sql
ALTER TABLE employees
ALTER COLUMN email DROP NOT NULL;
```

---

# Phần F — Thêm constraint sau khi đã tạo table

## 15. Thêm primary key

```sql
ALTER TABLE some_table
ADD CONSTRAINT pk_some_table
PRIMARY KEY (id);
```

## 16. Thêm foreign key

```sql
ALTER TABLE employees
ADD CONSTRAINT fk_employees_department
FOREIGN KEY (department_id)
REFERENCES departments(id);
```

## 17. Xóa constraint

Xem tên constraint:

```text
\d employees
```

Xóa:

```sql
ALTER TABLE employees
DROP CONSTRAINT fk_employees_department;
```

---

# Phần G — Dữ liệu mẫu

## 18. Insert

```sql
INSERT INTO departments (name)
VALUES
    ('Engineering'),
    ('Sales'),
    ('Finance');
```

```sql
INSERT INTO employees (
    full_name,
    email,
    salary,
    department_id
)
VALUES (
    'Nguyen Van A',
    'a@example.com',
    25000000,
    1
);
```

---

## 19. Select

```sql
SELECT *
FROM employees;
```

Join:

```sql
SELECT
    e.id,
    e.full_name,
    e.email,
    d.name AS department
FROM employees AS e
LEFT JOIN departments AS d
    ON d.id = e.department_id;
```

---

## 20. Update

```sql
UPDATE employees
SET salary = 30000000
WHERE id = 1;
```

Luôn kiểm tra `WHERE` trước khi update hàng loạt.

---

## 21. Delete

```sql
DELETE FROM employees
WHERE id = 1;
```

Không có `WHERE`:

```sql
DELETE FROM employees;
```

sẽ xóa toàn bộ row trong bảng.

---

# Phần H — Cấp quyền

## 22. Owner và privilege

Nếu database được tạo:

```sql
CREATE DATABASE appdb OWNER app_user;
```

thì `app_user` là owner của database.

Nếu table do một role khác tạo, application role có thể cần được cấp quyền.

### Cho phép kết nối database

```sql
GRANT CONNECT ON DATABASE appdb TO app_user;
```

### Cho phép dùng schema

```sql
GRANT USAGE ON SCHEMA public TO app_user;
```

### CRUD trên tất cả bảng hiện có trong schema

```sql
GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA public
TO app_user;
```

### Quyền với sequence

Với schema có sequence cần sử dụng:

```sql
GRANT USAGE, SELECT
ON ALL SEQUENCES IN SCHEMA public
TO app_user;
```

> Owner đã có quyền trên object của mình; không cần tự `GRANT` lại cho owner.

---

# Phần I — Bài thực hành tổng hợp

## 23. Kịch bản hoàn chỉnh

### Bước 1 — vào PostgreSQL

```bash
sudo -u postgres psql
```

### Bước 2 — tạo role

```sql
CREATE ROLE app_user WITH LOGIN;
```

```text
\password app_user
```

### Bước 3 — tạo database

```sql
CREATE DATABASE appdb OWNER app_user;
```

### Bước 4 — chuyển database

```text
\c appdb
```

### Bước 5 — tạo bảng

```sql
CREATE TABLE departments (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL UNIQUE
);

CREATE TABLE employees (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name varchar(150) NOT NULL,
    email varchar(255) NOT NULL UNIQUE,
    department_id bigint,
    CONSTRAINT fk_employees_department
        FOREIGN KEY (department_id)
        REFERENCES departments(id)
        ON DELETE SET NULL
);
```

### Bước 6 — thêm data

```sql
INSERT INTO departments (name)
VALUES ('Engineering');

INSERT INTO employees (full_name, email, department_id)
VALUES ('Nguyen Van A', 'a@example.com', 1);
```

### Bước 7 — kiểm tra

```sql
SELECT
    e.id,
    e.full_name,
    e.email,
    d.name AS department
FROM employees e
LEFT JOIN departments d
    ON d.id = e.department_id;
```

---

## 24. Ghi nhớ

```text
ROLE LOGIN           = tài khoản đăng nhập
CREATE DATABASE      = tạo database
CREATE TABLE         = tạo bảng
ALTER TABLE          = sửa cấu trúc bảng
PRIMARY KEY          = định danh duy nhất row
FOREIGN KEY          = đảm bảo quan hệ hợp lệ
GRANT                 = cấp quyền
```

## Nguồn chính thức

- PostgreSQL — `CREATE ROLE`: https://www.postgresql.org/docs/current/sql-createrole.html
- PostgreSQL — `CREATE USER`: https://www.postgresql.org/docs/current/sql-createuser.html
- PostgreSQL — `CREATE DATABASE`: https://www.postgresql.org/docs/current/sql-createdatabase.html
- PostgreSQL — `CREATE TABLE`: https://www.postgresql.org/docs/current/sql-createtable.html
- PostgreSQL — Identity Columns: https://www.postgresql.org/docs/current/ddl-identity-columns.html
- PostgreSQL — Constraints: https://www.postgresql.org/docs/current/ddl-constraints.html
- PostgreSQL — Modifying Tables: https://www.postgresql.org/docs/current/ddl-alter.html
- PostgreSQL — `GRANT`: https://www.postgresql.org/docs/current/sql-grant.html
- PostgreSQL — `INSERT`: https://www.postgresql.org/docs/current/sql-insert.html
- PostgreSQL — `SELECT`: https://www.postgresql.org/docs/current/sql-select.html
- PostgreSQL — `UPDATE`: https://www.postgresql.org/docs/current/sql-update.html
- PostgreSQL — `DELETE`: https://www.postgresql.org/docs/current/sql-delete.html
