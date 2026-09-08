# 05 — Kết nối PostgreSQL vào Visual Studio Code

## 1. Mục tiêu

Sau phần này bạn có thể:

- cài PostgreSQL extension chính thức của Microsoft;
- kết nối PostgreSQL local;
- kết nối PostgreSQL server từ máy workstation;
- chạy SQL trực tiếp trong VS Code;
- phân tích các lỗi kết nối thường gặp.

---

# Phần A — Extension

## 2. Cài extension

Trong VS Code:

```text
Ctrl + Shift + X
```

Tìm:

```text
PostgreSQL
```

Chọn:

```text
PostgreSQL
Publisher: Microsoft
```

Extension hiện tại trên Marketplace có ID:

```text
ms-ossdata.vscode-pgsql
```

Sau khi cài, VS Code có PostgreSQL view trong Activity Bar.

---

# Phần B — Thông số kết nối

## 3. Một connection PostgreSQL cần gì?

Tối thiểu:

```text
host
port
username
password
database
```

Ví dụ local:

```text
Server name:         localhost
Port:                5432
Authentication Type: Password
User name:           app_user
Password:            ********
Database name:       appdb
Connection Name:     Local appdb
```

Ví dụ remote:

```text
Server name:         192.168.1.10
Port:                5432
Authentication Type: Password
User name:           app_user
Password:            ********
Database name:       appdb
Connection Name:     Debian PostgreSQL
```

---

# Phần C — Chuẩn bị PostgreSQL

## 4. Tạo user và database trước

Trên server:

```bash
sudo -u postgres psql
```

Tạo role:

```sql
CREATE ROLE app_user WITH LOGIN;
```

Đặt password:

```text
\password app_user
```

Tạo DB:

```sql
CREATE DATABASE appdb OWNER app_user;
```

Thoát:

```text
\q
```

---

# Phần D — Test local trước khi dùng IDE

## 5. Test bằng `psql`

Trên chính server:

```bash
psql -h 127.0.0.1 -p 5432 -U app_user -d appdb
```

Nếu kết nối được bằng `psql` nhưng VS Code không kết nối được, khả năng cao vấn đề nằm ở:

- connection profile VS Code;
- password lưu sai;
- hostname/port;
- SSL mode hoặc extension config.

Nếu `psql` cũng không được, xử lý PostgreSQL/network trước.

---

# Phần E — Kết nối local VS Code

## 6. Mở PostgreSQL view

Microsoft Learn hướng dẫn:

```text
Ctrl + Alt + D
```

trên Windows/Linux, hoặc chọn biểu tượng PostgreSQL trong Activity Bar.

### Tạo connection

1. Trong `Connections`, chọn `Add New Connection`.
2. Chọn tab parameters.
3. Nhập:
   - Server name: `localhost`
   - Authentication Type: `Password`
   - User name: `app_user`
   - Password: password của role
   - Database name: `appdb`
   - Connection Name: ví dụ `Local appdb`
4. Chọn `Save & Connect`.

Khi thành công, server xuất hiện trong Connections tree.

Microsoft cho phép `Save Password` để lưu credential trong credential store của VS Code.

---

# Phần F — Chạy query

## 7. Mở New Query

Right-click connection/server:

```text
New Query
```

Ví dụ:

```sql
SELECT version();
SELECT current_user;
SELECT current_database();
```

Chạy query theo quickstart của Microsoft:

```text
Ctrl + Shift + E
```

trên Windows/Linux.

---

## 8. Tạo table từ VS Code

```sql
CREATE TABLE projects (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(150) NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);
```

Insert:

```sql
INSERT INTO projects (name)
VALUES
    ('Study PostgreSQL'),
    ('Backend API');
```

Query:

```sql
SELECT *
FROM projects
ORDER BY id;
```

---

# Phần G — Kết nối từ workstation đến PostgreSQL Linux server

Giả sử:

```text
PostgreSQL server IP = 192.168.1.10
Workstation IP       = 192.168.1.50
Database             = appdb
Role                 = app_user
Port                 = 5432
```

## 9. Bước 1 — server phải listen trên interface phù hợp

Trong `psql`:

```sql
SHOW config_file;
SHOW listen_addresses;
```

Mở `postgresql.conf`.

Cấu hình an toàn theo interface cụ thể:

```conf
listen_addresses = '192.168.1.10'
port = 5432
```

Hoặc nếu có lý do cần mọi interface:

```conf
listen_addresses = '*'
```

Sau đó restart:

```bash
sudo systemctl restart postgresql
```

> `listen_addresses` cần restart vì đây là tham số server-start.

---

## 10. Bước 2 — cho phép workstation trong `pg_hba.conf`

Tìm file:

```sql
SHOW hba_file;
```

Thêm rule:

```conf
host    appdb    app_user    192.168.1.50/32    scram-sha-256
```

Reload:

```bash
sudo systemctl reload postgresql
```

Rule này chỉ cho:

```text
database = appdb
user     = app_user
client   = 192.168.1.50
auth     = SCRAM-SHA-256
```

Không nên dùng rule quá rộng kiểu:

```conf
host all all 0.0.0.0/0 trust
```

vì sẽ mở quyền quá mức và đặc biệt `trust` bỏ qua password authentication.

---

## 11. Bước 3 — network/firewall

PostgreSQL cần TCP port `5432` có thể đi từ workstation đến server.

Mục tiêu bảo mật:

```text
allow 5432 only from workstation/VPN/private network
```

Không nên public port `5432` ra toàn Internet nếu không có thiết kế bảo mật phù hợp.

---

## 12. Bước 4 — test từ workstation

Nếu workstation có `psql`:

```bash
psql -h 192.168.1.10 -p 5432 -U app_user -d appdb
```

Nếu lệnh này thành công, điền cùng thông số vào VS Code:

```text
Server name:   192.168.1.10
Port:          5432
User name:     app_user
Database name: appdb
```

---

# Phần H — Phân tích lỗi

## 13. `Connection refused`

Ý nghĩa thường gặp:

```text
TCP connection không đến được PostgreSQL listener
```

Kiểm tra server:

```bash
pg_lsclusters
sudo systemctl status postgresql
pg_isready -h 127.0.0.1 -p 5432
```

Kiểm tra SQL:

```sql
SHOW listen_addresses;
SHOW port;
```

Kiểm tra:

- đúng IP server?
- đúng port?
- PostgreSQL đang chạy?
- PostgreSQL listen trên interface đó?
- firewall có chặn?

---

## 14. `no pg_hba.conf entry`

Network đã tới PostgreSQL, nhưng authentication rule không cho phép.

Kiểm tra:

```sql
SHOW hba_file;
```

Tạo rule chính xác:

```conf
host appdb app_user 192.168.1.50/32 scram-sha-256
```

Sau đó:

```bash
sudo systemctl reload postgresql
```

---

## 15. `password authentication failed`

Kiểm tra role:

```text
\du
```

Đổi password:

```text
\password app_user
```

Test lại bằng `psql`.

---

## 16. `database "..." does not exist`

Liệt kê database:

```text
\l
```

Tạo:

```sql
CREATE DATABASE appdb OWNER app_user;
```

---

## 17. `role "..." does not exist`

Liệt kê:

```text
\du
```

Tạo:

```sql
CREATE ROLE app_user WITH LOGIN;
```

Đặt password:

```text
\password app_user
```

---

# Phần I — Checklist kết nối VS Code

```text
[ ] PostgreSQL service running
[ ] cluster online
[ ] role exists + LOGIN
[ ] role has password
[ ] database exists
[ ] psql can connect
[ ] correct host
[ ] correct port 5432
[ ] listen_addresses correct
[ ] pg_hba.conf allows client IP
[ ] firewall/network allows TCP 5432
[ ] VS Code PostgreSQL by Microsoft installed
[ ] VS Code profile uses correct DB/user/password
```

---

# Phần J — Kiến trúc khuyến nghị

Cho máy dev cùng LAN/VPN:

```text
Workstation + VS Code
        |
        | TCP 5432
        | only allowed client IP/VPN
        v
Linux Server
        |
        ├─ PostgreSQL
        ├─ appdb
        └─ app_user
```

Nguyên tắc:

1. Không dùng `postgres` superuser trong IDE cho công việc ứng dụng hằng ngày.
2. Tạo role riêng cho ứng dụng/dev.
3. Giới hạn client IP trong `pg_hba.conf`.
4. Ưu tiên private network/VPN.
5. Dùng password auth hiện đại như `scram-sha-256`.
6. Nếu triển khai qua mạng không tin cậy, cấu hình TLS thay vì chỉ mở port trực tiếp.

## Nguồn chính thức

- Microsoft Learn — PostgreSQL Extension Overview: https://learn.microsoft.com/en-us/azure/postgresql/developer/vs-code-extension/vs-code-overview
- Microsoft Learn — Quickstart Connect and Query PostgreSQL: https://learn.microsoft.com/vi-vn/azure/postgresql/developer/vs-code-extension/vs-code-connect
- Visual Studio Marketplace — PostgreSQL by Microsoft: https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql
- PostgreSQL — `psql`: https://www.postgresql.org/docs/current/app-psql.html
- PostgreSQL — Connections and Authentication: https://www.postgresql.org/docs/current/runtime-config-connection.html
- PostgreSQL — `pg_hba.conf`: https://www.postgresql.org/docs/current/auth-pg-hba-conf.html
- PostgreSQL — Password Authentication: https://www.postgresql.org/docs/current/auth-password.html
