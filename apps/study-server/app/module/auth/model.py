from pydantic import BaseModel


class RegisterRequest(BaseModel):
    display_name: str
    email: str
    phone: str
    password: str
