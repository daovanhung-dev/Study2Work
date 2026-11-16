from pydantic import BaseModel


class CreatePaymentRequest(BaseModel):
    order_id: int
    provider: str
