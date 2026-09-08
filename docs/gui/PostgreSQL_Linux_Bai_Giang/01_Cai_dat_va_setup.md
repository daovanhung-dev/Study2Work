# 01 — Cài đặt và setup PostgreSQL trên Linux

## 1. Mục tiêu

Sau phần này bạn có thể:

- phân biệt PostgreSQL server và client;
- cài PostgreSQL bằng package manager;
- chọn bản PostgreSQL phù hợp;
- kiểm tra version và cluster;
- hiểu các file/directory quan trọng.

---

## 2. Khái niệm trước khi cài

### PostgreSQL server

Process server chính là `postgres`.

Client như `psql`, ứng dụng backend hoặc IDE sẽ kết nối đến một PostgreSQL server đang chạy.

### Database cluster

Trong PostgreSQL, **cluster** là tập hợp nhiều database được quản lý bởi một PostgreSQL server instance.

Sau khi cluster được khởi tạo, thông thường có:

```text
postgres
template0
template1
```

- `postgres`: database mặc định cho utility/client.
- `template1`: template mặc định khi tạo database mới.
- `template0`: template "sạch", dùng khi cần tạo database không kế thừa thay đổi từ `template1`.

> "Cluster" ở đây không có nghĩa là nhiều máy server. Một máy PostgreSQL đơn cũng có một database cluster.

---

## 3. Chọn cách cài

PostgreSQL khuyến nghị dùng package manager của hệ điều hành khi có thể.

Trên Debian có hai cách chính.

### Cách A — dùng package có sẵn của Debian

```bash
sudo apt update
sudo apt install postgresql
```

Ưu điểm:

- đơn giản;
- tích hợp tốt với Debian;
- được quản lý bằng APT.

Nhược điểm:

- Debian cố định một major version cho mỗi release, nên có thể không phải version PostgreSQL mới nhất.

### Cách B — dùng PostgreSQL Apt Repository (PGDG)

Dùng cách này khi cần một major version cụ thể, ví dụ PostgreSQL 18.

#### Bước 1 — cài `postgresql-common`

```bash
sudo apt update
sudo apt install -y postgresql-common
```

#### Bước 2 — chạy script cấu hình repository chính thức

```bash
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
```

Script sẽ thêm PostgreSQL Apt Repository phù hợp với Debian/Ubuntu.

#### Bước 3 — cập nhật package index

```bash
sudo apt update
```

#### Bước 4 — cài PostgreSQL 18

```bash
sudo apt install postgresql-18
```

### Các package thường gặp

| Package | Chức năng |
|---|---|
| `postgresql-18` | PostgreSQL server |
| `postgresql-client-18` | client tools như `psql` |
| `postgresql-doc-18` | tài liệu |
| `libpq-dev` | header/library cho ứng dụng C/C++ hoặc package cần libpq |
| `postgresql-server-dev-18` | header để phát triển extension phía server |

---

## 4. Kiểm tra sau cài

### Kiểm tra `psql`

```bash
psql --version
```

Ví dụ:

```text
psql (PostgreSQL) 18.x
```

### Kiểm tra package

```bash
dpkg -l | grep postgresql
```

### Kiểm tra cluster trên Debian

```bash
pg_lsclusters
```

Ví dụ:

```text
Ver Cluster Port Status Owner    Data directory              Log file
18  main    5432 online postgres /var/lib/postgresql/18/main ...
```

Ý nghĩa:

- `Ver`: major version.
- `Cluster`: tên cluster, Debian thường dùng `main`.
- `Port`: port PostgreSQL.
- `Status`: `online` hoặc `down`.
- `Owner`: Linux user sở hữu cluster.
- `Data directory`: nơi chứa dữ liệu.

---

## 5. Data directory và config file

PostgreSQL upstream gọi nơi chứa dữ liệu của cluster là **data directory**.

Nếu cài thủ công, có thể tạo cluster bằng:

```bash
initdb -D /path/to/data
```

Nhưng với package Debian/Ubuntu, **không nên tự chạy `initdb` nếu package đã tạo cluster cho bạn**. Hãy dùng infrastructure của package.

### Ba file cấu hình quan trọng

PostgreSQL sử dụng:

```text
postgresql.conf
pg_hba.conf
pg_ident.conf
```

- `postgresql.conf`: cấu hình server.
- `pg_hba.conf`: Host-Based Authentication — quy định ai được kết nối, từ đâu và dùng phương thức xác thực nào.
- `pg_ident.conf`: mapping tên user khi cần.

Vị trí thực tế có thể khác tùy package.

Để PostgreSQL tự cho biết đường dẫn chính xác:

```sql
SHOW config_file;
SHOW hba_file;
SHOW data_directory;
```

Cách này tốt hơn việc đoán đường dẫn.

---

## 6. Port và địa chỉ lắng nghe

### Port

Port mặc định thường là:

```text
5432
```

Kiểm tra từ SQL:

```sql
SHOW port;
```

### `listen_addresses`

PostgreSQL mặc định thường chỉ lắng nghe local interface.

Kiểm tra:

```sql
SHOW listen_addresses;
```

Nguyên tắc:

- chỉ dùng local: `localhost`;
- cần client từ máy khác: cấu hình IP/interface cần thiết;
- tránh mở `*` ra Internet nếu không thực sự cần.

> `listen_addresses` chỉ quyết định server nghe trên interface nào. Quyền truy cập thực tế còn phụ thuộc `pg_hba.conf`, user/password, firewall và network.

---

## 7. Cài đặt tối thiểu đề xuất cho máy học

Nếu máy Debian dùng cho học/dev:

```bash
sudo apt update
sudo apt install -y postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
sudo apt update
sudo apt install -y postgresql-18
```

Kiểm tra:

```bash
psql --version
pg_lsclusters
```

Kết quả mong muốn:

```text
PostgreSQL 18.x
cluster 18/main
port 5432
status online
owner postgres
```

---

## 8. Lỗi thường gặp khi cài

### `psql: command not found`

Kiểm tra client package:

```bash
sudo apt install postgresql-client-18
```

### Không thấy cluster

```bash
pg_lsclusters
```

Nếu package không tự tạo cluster, cần dùng công cụ của package Debian (`pg_createcluster`) thay vì tự đoán cấu hình.

### Cài nhầm major version

Kiểm tra:

```bash
psql --version
pg_lsclusters
apt list --installed 2>/dev/null | grep postgresql
```

---

## 9. Ghi nhớ

```text
apt install postgresql
    ↓
PostgreSQL package
    ↓
database cluster
    ↓
postgres server
    ↓
port 5432
    ↓
psql / application / VS Code
```

## Nguồn chính thức

- PostgreSQL — Linux downloads: https://www.postgresql.org/download/linux/
- PostgreSQL — Debian download: https://www.postgresql.org/download/linux/debian/
- PostgreSQL — Creating a Database Cluster: https://www.postgresql.org/docs/current/creating-cluster.html
- PostgreSQL — File Locations: https://www.postgresql.org/docs/current/runtime-config-file-locations.html
- PostgreSQL — Connections and Authentication: https://www.postgresql.org/docs/current/runtime-config-connection.html
- Debian — `pg_lsclusters`: https://manpages.debian.org/trixie/postgresql-common/pg_lsclusters.1.en.html
