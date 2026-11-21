

# Quy trình Dev

1. **Chuẩn bị môi trường** :
   +) Môi trường local dev: fastapi, angular,
   +) Extensions: Angular Language Service, Dart, Draw.io, Flutter, JavaScript and TypeScript Nightly, Office Viewer, Python, Thunder Client, Vue.
   +) Môi trường developer(Thư viện, package)
2. **Tạo nhánh cá nhân**
3. **Test môi trường:**

   1. Setup Schema(apps/study-server/app/core/constants.py):
      Chỉnh sửa: `DB_SCHEMA = "dao_van_hung" # Sua thanh Schema cua minh`
   2. Test api:
      1. Chạy dự án :

         ```Python
         cd apps/study-server
         ```
         ```Python
         uv sync
         uv run ruff check .
         uv run ruff format --check .
         uv run mypy app
         uv run pytest
         uv run uvicorn app.main:app --reload
         ```
      2. Vào Thunder Client:

         1. Chạy api

            ```
            127.0.0.1:8000/api/v1/hello
            ```
            test server
         2. Chạy api

            ```
            127.0.0.1:8000/api/v1/test/db
            ```
            test db
         3. Chạy  api

            ```
            127.0.0.1:8000/api/v1/auth/register
            ```
            test api #1
   3. **Đọc tài liệu DD:**
      1. Tài liệu DD có nhất là 7 file, thường sẽ là 7 file nếu api không làm thay đổi csdl;
      2. 00_Cover.md: Mô tả tổng quan api
      3. Mỗi một trường hợp trả về phải có business_code, nếu không có thì chứng tó đang thiếu hoặc sai logic => Cần confirm của leader
