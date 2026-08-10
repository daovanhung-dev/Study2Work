from pydantic import BaseModel

class ChatLogRequest(BaseModel):
    prompt: str