# S2W Backend — Agent Entry Point

## Mục đích

File này là điểm vào bắt buộc cho AI agent khi làm việc với backend Study2Work (S2W).

Trước khi sửa hoặc tạo code, agent phải đọc toàn bộ thư mục `.agent/context/` theo thứ tự trong `00_INDEX.md`.

## Phạm vi context hiện tại

Context được xây dựng từ source `app(5).zip` tại thời điểm 2026-08-08.
Source hiện có là backend FastAPI skeleton, gồm các lớp chính:

```text
app/
├── main.py
├── api/
├── core/
├── module/
└── service/
```

Không suy diễn flow frontend vì source hiện tại không chứa VueJS/frontend.

## Nguyên tắc ưu tiên nguồn

Khi có xung đột, dùng thứ tự:

1. Yêu cầu mới nhất của người dùng.
2. Source code hiện tại.
3. DD/BD/schema/plan được người dùng cung cấp cho task hiện tại.
4. `.agent/context/`.
5. Best practice chung.

Context này mô tả cả **hiện trạng source** và **develop flow mục tiêu**. Không được coi phần mục tiêu là code đã tồn tại.

## Luồng coding chuẩn

```text
Client
  ↓
Middleware / Trace / Auth
  ↓
API Router
  ↓
Model
  ↓
View (business orchestration)
  ├─ Validate
  ├─ Query
  │    ↓
  │  Core Database
  │    ↓
  │  PostgreSQL
  └─ Service (AI/external systems)
  ↓
Standard Response
  ↓
Client
```

## Luật cốt lõi

- Router phải mỏng.
- `view.py` điều phối business flow.
- `validate.py` chỉ validation.
- `query.py` chỉ khai báo SQL/query constant của module.
- `core/` xử lý infrastructure dùng chung.
- `service/` bao external integration.
- Một HTTP request dùng một DB Session lifecycle.
- Mutation nhiều bước phải cùng transaction khi nghiệp vụ yêu cầu atomicity.
- Không hard-code trace ID.
- Không tự tạo JWT/business code/schema/table/column khi chưa có nguồn.
- Không đưa SQL vào router.
- Không tạo global SQLAlchemy Session dùng chung cho nhiều request.
- Không sửa unrelated files nếu task không yêu cầu.

## Khi bắt đầu một task coding

Agent phải:

1. Xác định module bị tác động.
2. Đọc `model.py`, `validate.py`, `query.py`, `view.py` của module đó.
3. Đọc core dependency mà module gọi.
4. Đọc schema/DD/BD liên quan nếu có.
5. Vẽ ngắn flow hiện tại trước khi sửa.
6. Chỉ sửa layer thực sự chịu trách nhiệm.
7. Rà lại import và flow end-to-end sau khi sửa.
8. Không tuyên bố chạy thành công nếu chưa thực sự kiểm tra được.

Chi tiết: `.agent/context/00_INDEX.md`.
