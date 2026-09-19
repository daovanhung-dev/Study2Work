# A. Quy trình làm việc

1. Nhận nhiệm vụ
   Vào docs/devs/folder_của_mình/tasks
2. Setup môi trường

   1. Cài các công nghệ: NodeJS(prisma), React, Angular, VueJS, FastAPI(sqlachemy, pydantic, bcrypt, ***uv***), Flutter.
   2. Setup schema: vào apps/study-server/app/core/constants.py và sửa ()

   ```python
   DB_SCHEMA = "public" # => Thành schema của mình
   ```
3. Đọc tài liệu DD(apps/study-server/docs/dd): Overview => Req => Res => DataMapping(trong datamapping, <u>nếu file có bind đến file nào  thì đọc file</u>)
4. Tạo nhánh cá nhân:  vd: daovanhung_dev(có thể là fixbug, test, vvv.) => Không có nhánh thì không được coding
5. coding:
   model.py(Định nghĩa kiểu dữ liệu, đầu vào, đầu ra) => validate.py(bắt lỗi đầu vào và trả về res) => query.py(Code theo truy vấn, vd: 1 api có bao nhiêu truy vấn thì có từng đấy câu lệnh sql) => coding view.py(Tổng hợp tất cả logic của một 1 api, được viết theo datamapping) => Khai báo api vào `apps/study-server/app/api/v1.py`
   Phân loại theo Request trong dd:
   VD: URI`: /api/v1/auth/login`=> api thuộc nhóm auth
6. Test api:

   `Dùng thunder client`
   `cd đến dự án :   cd apps/study-server`

   ```powershell
   uv sync
   uv run ruff check .
   uv run ruff format --check .
   uv run mypy app
   uv run pytest
   uv run uvicorn app.main:app --reload
   ```
7. Sau khi làm nhiệm vụ
   Note nhiệm vụ vào trong worklogs
