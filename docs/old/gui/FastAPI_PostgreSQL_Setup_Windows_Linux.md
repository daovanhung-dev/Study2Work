# Cài môi trường FastAPI kết nối PostgreSQL (Windows & Linux)

## Mục tiêu

Thiết lập môi trường phát triển cho **FastAPI + PostgreSQL** sử dụng
**SQLAlchemy Async**, **asyncpg** và **Alembic**.

> Theo Study2Work, schema phát triển hiện tại là `study_dev0`.

------------------------------------------------------------------------

## 1. Cài đặt PostgreSQL

### Linux (Ubuntu/Linux Mint)

``` bash
sudo apt update
sudo apt install postgresql postgresql-contrib libpq-dev -y
sudo systemctl enable --now postgresql
```

### Windows

``` powershell
winget install PostgreSQL.PostgreSQL
```

Cấu hình mặc định:

``` text
Host: 127.0.0.1
Port: 5432
User: postgres
```

------------------------------------------------------------------------

## 2. Tạo User và Database

Đăng nhập PostgreSQL:

**Linux**

``` bash
sudo -u postgres psql
```

**Windows**

``` powershell
psql -U postgres
```

Thực hiện:

``` sql
CREATE USER s2w_user WITH PASSWORD 's2w_password';

CREATE DATABASE s2w
    WITH OWNER = s2w_user
    ENCODING = 'UTF8';

GRANT ALL PRIVILEGES ON DATABASE s2w TO s2w_user;
```

Kiểm tra:

``` bash
psql -h 127.0.0.1 -p 5432 -U s2w_user -d s2w
```

------------------------------------------------------------------------

## 3. Tạo Virtual Environment

Thư mục:

``` text
apps/study-server
```

### Linux

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

``` powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Cài thư viện:

``` bash
python -m pip install --upgrade pip
pip install "fastapi[standard]" sqlalchemy asyncpg alembic pydantic-settings
```

------------------------------------------------------------------------

## 4. Cấu hình `.env`

``` env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=s2w
DB_USER=s2w_user
DB_PASSWORD=s2w_password
DB_SCHEMA=study_dev0

DATABASE_URL=postgresql+asyncpg://s2w_user:s2w_password@127.0.0.1:5432/s2w
```

> `DB_HOST` chỉ chứa địa chỉ máy chủ, không bao gồm cổng.

------------------------------------------------------------------------

## 5. Khởi tạo SQLAlchemy

``` python
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.app_debug,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

------------------------------------------------------------------------

## 6. Chạy FastAPI

``` bash
fastapi dev app/main.py
```

Hoặc:

``` bash
uvicorn app.main:app --reload
```

Truy cập:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

## 7. Kiểm tra

``` bash
python --version
psql --version
pip show fastapi sqlalchemy asyncpg
```

``` sql
SELECT current_database(), current_user;
```
