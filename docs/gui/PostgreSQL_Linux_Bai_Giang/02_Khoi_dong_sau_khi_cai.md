# 02 — Khởi động và kiểm tra PostgreSQL sau khi cài

## 1. Mục tiêu

Sau phần này bạn có thể:

- kiểm tra PostgreSQL service;
- start/stop/restart/reload;
- kiểm tra cluster;
- đăng nhập `psql`;
- kiểm tra server đã sẵn sàng nhận kết nối;
- xác định config và data directory.

---

## 2. Ba lớp cần kiểm tra

Sau khi cài xong, kiểm tra theo thứ tự:

```text
1. Package đã cài?
2. PostgreSQL cluster có online?
3. Client có kết nối được?
```

---

## 3. Kiểm tra service bằng systemd

### Trạng thái

```bash
sudo systemctl status postgresql
```

### Khởi động

```bash
sudo systemctl start postgresql
```

### Dừng

```bash
sudo systemctl stop postgresql
```

### Restart

```bash
sudo systemctl restart postgresql
```

Dùng khi thay đổi cấu hình yêu cầu restart, ví dụ `listen_addresses`.

### Reload

```bash
sudo systemctl reload postgresql
```

Dùng để PostgreSQL đọc lại cấu hình có thể reload mà không cần restart.

### Enable khi boot

```bash
sudo systemctl enable postgresql
```

> Trên Debian, service tổng `postgresql` có thể quản lý một hoặc nhiều cluster. Để xem cluster cụ thể, dùng `pg_lsclusters`.

---

## 4. Quản lý cluster theo kiểu Debian

### Xem cluster

```bash
pg_lsclusters
```

### Start cluster cụ thể

```bash
sudo pg_ctlcluster 18 main start
```

### Stop

```bash
sudo pg_ctlcluster 18 main stop
```

### Restart

```bash
sudo pg_ctlcluster 18 main restart
```

### Reload

```bash
sudo pg_ctlcluster 18 main reload
```

### Status

```bash
sudo pg_ctlcluster 18 main status
```

Cấu trúc:

```text
pg_ctlcluster <version> <cluster-name> <action>
```

Ví dụ:

```text
version      = 18
cluster-name = main
action       = start | stop | restart | reload | status
```

---

## 5. Công cụ PostgreSQL upstream: `pg_ctl`

`pg_ctl` có thể:

```text
initdb
start
stop
restart
reload
status
promote
logrotate
```

Ví dụ kiểu upstream:

```bash
pg_ctl -D /path/to/data status
```

Với Debian package, nên ưu tiên:

```bash
pg_ctlcluster
```

vì tool này tự xác định đúng version, data path và configuration.

---

## 6. Kiểm tra server có nhận kết nối không

### `pg_isready`

```bash
pg_isready
```

Hoặc chỉ rõ host/port:

```bash
pg_isready -h 127.0.0.1 -p 5432
```

Khi server sẵn sàng, thường thấy:

```text
127.0.0.1:5432 - accepting connections
```

`pg_isready` kiểm tra trạng thái kết nối của PostgreSQL server.

---

## 7. Đăng nhập lần đầu

Trên server Debian:

```bash
sudo -u postgres psql
```

Bạn chuyển sang PostgreSQL role quản trị `postgres` thông qua Linux user `postgres`.

Prompt thường giống:

```text
postgres=#
```

Dấu `#` thường cho biết role hiện tại có quyền superuser.

Thoát:

```text
\q
```

---

## 8. Kiểm tra thông tin trong `psql`

### Version server

```sql
SELECT version();
```

### User hiện tại

```sql
SELECT current_user;
```

### Database hiện tại

```sql
SELECT current_database();
```

### Connection info

```text
\conninfo
```

### Liệt kê database

```text
\l
```

### Liệt kê role

```text
\du
```

---

## 9. Xác định đường dẫn config chính xác

Trong `psql`:

```sql
SHOW config_file;
SHOW hba_file;
SHOW data_directory;
SHOW port;
SHOW listen_addresses;
```

Ví dụ tư duy:

```text
config_file      -> postgresql.conf
hba_file         -> pg_hba.conf
data_directory   -> data thực tế
port             -> 5432
listen_addresses -> localhost / IP / *
```

Không nên chỉnh file theo đường dẫn "đoán". Hãy dùng `SHOW ...` để lấy đường dẫn thật.

---

## 10. Thay đổi cấu hình và áp dụng

### Trường hợp cần remote connection

Ví dụ trong `postgresql.conf`:

```conf
listen_addresses = '192.168.1.10'
port = 5432
```

Hoặc nếu thực sự cần lắng nghe trên mọi interface:

```conf
listen_addresses = '*'
```

Sau khi đổi `listen_addresses`, restart:

```bash
sudo systemctl restart postgresql
```

### `pg_hba.conf`

Ví dụ chỉ cho một máy workstation:

```conf
host    appdb    app_user    192.168.1.50/32    scram-sha-256
```

Ý nghĩa:

```text
host             TCP/IP connection
appdb            database được phép
app_user         role được phép
192.168.1.50/32  duy nhất IP workstation này
scram-sha-256    phương thức password authentication
```

Sau khi thay đổi `pg_hba.conf`:

```bash
sudo systemctl reload postgresql
```

> PostgreSQL xét các record `pg_hba.conf` theo thứ tự. Record phù hợp đầu tiên sẽ được sử dụng.

---

## 11. Kiểm tra port từ Linux

Có thể xem process đang listen:

```bash
ss -ltnp | grep 5432
```

Nếu PostgreSQL chỉ local:

```text
127.0.0.1:5432
```

Nếu listen trên server LAN IP:

```text
192.168.1.10:5432
```

> `ss` là công cụ Linux, không phải PostgreSQL. Nó chỉ giúp xác minh network socket.

---

## 12. Quy trình kiểm tra chuẩn sau cài

```bash
psql --version
pg_lsclusters
sudo systemctl status postgresql
pg_isready
sudo -u postgres psql
```

Sau khi vào `psql`:

```sql
SELECT version();
SELECT current_user;
SELECT current_database();
SHOW port;
SHOW listen_addresses;
```

Sau đó:

```text
\conninfo
\l
\du
\q
```

---

## 13. Lỗi thường gặp

### `connection refused`

Kiểm tra:

```bash
pg_lsclusters
sudo systemctl status postgresql
pg_isready -h 127.0.0.1 -p 5432
```

Nguyên nhân thường:

- service/cluster chưa chạy;
- sai port;
- `listen_addresses` không đúng;
- firewall/network chặn.

### `no pg_hba.conf entry`

Server đã nhận connection nhưng không có rule HBA phù hợp.

Kiểm tra:

```sql
SHOW hba_file;
```

Sau đó thêm rule đúng database/user/IP.

### `password authentication failed`

Kiểm tra:

- đúng role?
- role có `LOGIN`?
- password đúng?
- HBA method phù hợp?

---

## 14. Ghi nhớ

```text
systemctl            = quản lý service Linux
pg_lsclusters        = xem cluster Debian
pg_ctlcluster        = điều khiển cluster Debian
pg_isready           = kiểm tra server nhận kết nối
psql                  = client terminal
SHOW config_file     = tìm postgresql.conf
SHOW hba_file        = tìm pg_hba.conf
```

## Nguồn chính thức

- PostgreSQL — Starting the Database Server: https://www.postgresql.org/docs/current/server-start.html
- PostgreSQL — `pg_ctl`: https://www.postgresql.org/docs/current/app-pg-ctl.html
- PostgreSQL — `psql`: https://www.postgresql.org/docs/current/app-psql.html
- PostgreSQL — `pg_isready`: https://www.postgresql.org/docs/current/app-pg-isready.html
- PostgreSQL — Connections and Authentication: https://www.postgresql.org/docs/current/runtime-config-connection.html
- PostgreSQL — `pg_hba.conf`: https://www.postgresql.org/docs/current/auth-pg-hba-conf.html
- Debian — `pg_ctlcluster`: https://manpages.debian.org/trixie/postgresql-common/pg_ctlcluster.1.en.html
- Debian — `pg_lsclusters`: https://manpages.debian.org/trixie/postgresql-common/pg_lsclusters.1.en.html
