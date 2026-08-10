# Ollama AI Service

Thư mục này chỉ cung cấp một đối tượng service sẵn sàng sử dụng. Không chứa router, endpoint hoặc logic FastAPI.

## Phụ thuộc

```bash
pip install httpx
```

## Sử dụng

```python
from service.ai import ai_service

result = await ai_service.generate(
    prompt="JWT là gì?",
)

print(result["answer"])
```

Chat:

```python
result = await ai_service.chat(
    messages=[
        {
            "role": "system",
            "content": "Bạn là trợ lý lập trình.",
        },
        {
            "role": "user",
            "content": "Viết middleware JWT bằng FastAPI.",
        },
    ],
)

print(result["answer"])
```

Kiểm tra kết nối:

```python
status = await ai_service.health_check()
```

Có thể khởi tạo đối tượng riêng:

```python
from service.ai import OllamaService

custom_ai = OllamaService(
    base_url="http://192.168.11.200:11434",
    model="qwen2.5-coder:1.5b",
    timeout=180,
)
```
