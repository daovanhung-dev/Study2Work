# Ollama AI Service

Thư mục này cung cấp Ollama service; caller trực tiếp phải quản lý vòng đời client. FastAPI mở client khi khởi động và đóng khi dừng.

## Phụ thuộc

```bash
pip install httpx
```

## Sử dụng

```python
from app.service.ai import OllamaService

service = OllamaService()
await service.start()  # Mở một AsyncClient cho service này
try:
    result = await service.generate(prompt="JWT là gì?")
    print(result["answer"])
    chat_result = await service.chat(messages=[
        {"role": "system", "content": "Bạn là trợ lý lập trình."},
        {"role": "user", "content": "Viết middleware JWT bằng FastAPI."},
    ])
    print(chat_result["answer"])
    status = await service.health_check()
    print(status["available"])
finally:
    await service.close()  # Đóng kể cả khi lời gọi thất bại
```

Có thể khởi tạo đối tượng riêng:

```python
from app.service.ai import OllamaService

custom_ai = OllamaService(
    base_url="http://192.168.11.200:11434",
    model="qwen2.5-coder:1.5b",
    timeout=180,
)
await custom_ai.start()
try:
    result = await custom_ai.generate(prompt="Xin chào")
finally:
    await custom_ai.close()
```

Các lời gọi `generate`, `chat`, `list_models`, `health_check` trong cùng khoảng giữa `start()` và `close()` dùng chung client. Nếu chưa gọi `start()` hoặc đã `close()`, service báo lỗi vòng đời; cần `start()` lại trước lời gọi mới. Không tạo client mới khi pool 100 kết nối đang bận: đợi tối đa 5 giây rồi trả lỗi `AIBusyError`. `OLLAMA_TIMEOUT` (mặc định 180 giây) áp dụng cho connect/read/write, không phải thời hạn tổng của request.
