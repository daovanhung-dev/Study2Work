from pydantic import BaseModel, Field, field_validator

class ChatLogRequest(BaseModel):
    prompt: str = Field(strict=True, max_length=8000)

    @field_validator("prompt")
    @classmethod
    def reject_blank_prompt(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("prompt không được rỗng hoặc chỉ có khoảng trắng")
        return value
